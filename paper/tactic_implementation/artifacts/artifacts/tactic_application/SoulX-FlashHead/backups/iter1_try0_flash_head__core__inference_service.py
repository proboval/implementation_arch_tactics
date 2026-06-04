# Copyright 2024-2025 The Alibaba Wan Team Authors. All rights reserved.
import os
import numpy as np
import time
import torch
import imageio
import librosa
from collections import deque
from loguru import logger
from datetime import datetime


class InferenceService:
    """
    Encapsulates shared inference orchestration logic for video generation.
    Supports both 'stream' and 'once' audio encoding modes.
    """

    def __init__(self, cached_audio_duration: float, frame_num: int, motion_frames_num: int, tgt_fps: int, sample_rate: int):
        self.cached_audio_duration = cached_audio_duration
        self.frame_num = frame_num
        self.motion_frames_num = motion_frames_num
        self.tgt_fps = tgt_fps
        self.sample_rate = sample_rate
        self.slice_len = frame_num - motion_frames_num
        self.human_speech_array_slice_len = self.slice_len * sample_rate // tgt_fps
        self.human_speech_array_frame_num = frame_num * sample_rate // tgt_fps

    def _encode_audio_once(self, pipeline, human_speech_array_all):
        """Encode audio once for all chunks (non-streaming mode)."""
        # pad audio with silence to avoid truncating the last chunk
        remainder = (len(human_speech_array_all) - self.human_speech_array_frame_num) % self.human_speech_array_slice_len
        if remainder > 0:
            pad_length = self.human_speech_array_slice_len - remainder
            human_speech_array_all = np.concatenate([human_speech_array_all, np.zeros(pad_length, dtype=human_speech_array_all.dtype)])

        # encode audio together
        audio_embedding_all = pipeline.encode_audio(human_speech_array_all)

        # split audio embedding into chunks
        # for Pro model: 33, 28, 28, 28, ...; For Lite model: 33, 24, 24, 24, ...
        audio_embedding_chunks_list = [
            audio_embedding_all[:, i * self.slice_len: i * self.slice_len + self.frame_num].contiguous()
            for i in range((audio_embedding_all.shape[1] - self.frame_num) // self.slice_len)
        ]
        return audio_embedding_chunks_list

    def _encode_audio_stream(self, pipeline, human_speech_array_all):
        """Encode audio in streaming mode with sliding window."""
        cached_audio_length_sum = int(self.sample_rate * self.cached_audio_duration)
        audio_end_idx = int(self.cached_audio_duration * self.tgt_fps)
        audio_start_idx = audio_end_idx - self.frame_num

        audio_dq = deque([0.0] * cached_audio_length_sum, maxlen=cached_audio_length_sum)

        # pad audio with silence to avoid truncating the last chunk
        remainder = len(human_speech_array_all) % self.human_speech_array_slice_len
        if remainder > 0:
            pad_length = self.human_speech_array_slice_len - remainder
            human_speech_array_all = np.concatenate([human_speech_array_all, np.zeros(pad_length, dtype=human_speech_array_all.dtype)])

        # split audio into chunks
        human_speech_array_slices = human_speech_array_all.reshape(-1, self.human_speech_array_slice_len)

        audio_embedding_chunks_list = []
        for human_speech_array in human_speech_array_slices:
            audio_dq.extend(human_speech_array.tolist())
            audio_array = np.array(audio_dq)
            audio_embedding = pipeline.encode_audio(audio_array, audio_start_idx, audio_end_idx)
            audio_embedding_chunks_list.append(audio_embedding)

        return audio_embedding_chunks_list

    def run(self, pipeline, audio_path: str, mode: str = 'stream', verbose: bool = True, rank: int = 0):
        """
        Run inference with shared orchestration logic.

        Args:
            pipeline: Initialized pipeline instance with encode_audio and run methods.
            audio_path: Path to input audio file.
            mode: 'stream' or 'once' for audio encoding strategy.
            verbose: Whether to log progress.
            rank: Process rank for distributed inference.

        Returns:
            List of generated video chunks (torch.Tensor).
        """
        # Load audio
        human_speech_array_all, _ = librosa.load(audio_path, sr=self.sample_rate, mono=True)

        # Select encoding strategy
        if mode == 'once':
            audio_embedding_chunks_list = self._encode_audio_once(pipeline, human_speech_array_all)
        elif mode == 'stream':
            audio_embedding_chunks_list = self._encode_audio_stream(pipeline, human_speech_array_all)
        else:
            raise ValueError(f"Unsupported audio_encode_mode: {mode}. Use 'stream' or 'once'.")

        generated_list = []
        for chunk_idx, audio_embedding_chunk in enumerate(audio_embedding_chunks_list):
            torch.cuda.synchronize()
            start_time = time.time()

            # inference
            video = pipeline.run(audio_embedding_chunk)

            if chunk_idx != 0:
                video = video[self.motion_frames_num:]

            torch.cuda.synchronize()
            end_time = time.time()
            if verbose and rank == 0:
                logger.info(f"Generate video chunk-{chunk_idx} done, cost time: {(end_time - start_time):.3f}s")

            generated_list.append(video.cpu())

        return generated_list


def save_video(frames_list, video_path, audio_path, fps):
    temp_video_path = video_path.replace('.mp4', '_tmp.mp4')
    with imageio.get_writer(temp_video_path, format='mp4', mode='I',
                            fps=fps, codec='h264', ffmpeg_params=['-bf', '0']) as writer:
        for frames in frames_list:
            frames = frames.numpy().astype(np.uint8)
            for i in range(frames.shape[0]):
                frame = frames[i, :, :, :]
                writer.append_data(frame)

    # merge video and audio
    cmd = ['ffmpeg', '-i', temp_video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-shortest', video_path, '-y']
    subprocess.run(cmd)
    os.remove(temp_video_path)


def save_video_from_generated_list(generated_list, audio_path, save_file, fps, rank=0):
    """Convenience wrapper to save generated video chunks."""
    if rank == 0:
        if save_file is None:
            output_dir = 'sample_results'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S-%f")[:-3]
            filename = f"res_{timestamp}.mp4"
            save_file = os.path.join(output_dir, filename)

        save_video(generated_list, save_file, audio_path, fps=fps)
        logger.info(f"Saving generated video to {save_file}")
        logger.info("Finished.")


# Import subprocess for save_video
import subprocess
