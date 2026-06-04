from abc import ABC, abstractmethod
from typing import List
import os
import re


class FileOperation(ABC):
    """Abstract base class for file operations with strategy pattern."""
    
    @abstractmethod
    def execute(self, file_path: str, content: str, **kwargs) -> str:
        """Execute the file operation and return result message."""
        pass
    
    def _validate_file_exists(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _write_file(self, file_path: str, content: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)


class FullReplaceOperation(FileOperation):
    """Full file content replacement strategy."""
    
    def execute(self, file_path: str, content: str, **kwargs) -> str:
        self._validate_file_exists(file_path)
        self._write_file(file_path, content)
        return f"File successfully updated: {file_path}\n{content}"


class LineRangeOperation(FileOperation):
    """Line range replacement strategy."""
    
    def execute(self, file_path: str, content: str, **kwargs) -> str:
        self._validate_file_exists(file_path)
        
        start_line = kwargs.get('start_line')
        end_line = kwargs.get('end_line')
        
        if start_line is None or end_line is None:
            raise ValueError("start_line and end_line are required for line range operation")
        
        original_content = self._read_file(file_path)
        lines = original_content.splitlines()
        
        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            raise ValueError("Invalid line numbers")
        
        lines[start_line-1:end_line] = content.splitlines()
        updated_content = '\n'.join(lines)
        self._write_file(file_path, updated_content)
        
        return f"File successfully updated: {file_path}\n{updated_content}"


class PatternReplaceOperation(FileOperation):
    """Pattern-based text search and replace strategy."""
    
    def execute(self, file_path: str, content: str, **kwargs) -> str:
        self._validate_file_exists(file_path)
        
        pattern = kwargs.get('search_pattern')
        replacement = kwargs.get('replacement_text')
        
        if pattern is None or replacement is None:
            raise ValueError("search_pattern and replacement_text are required for pattern operation")
        
        original_content = self._read_file(file_path)
        
        try:
            updated_content = re.sub(pattern, replacement, original_content)
        except re.error as e:
            raise ValueError(f"Invalid regular expression pattern: {str(e)}")
        
        self._write_file(file_path, updated_content)
        
        return f"File successfully updated: {file_path}\n{updated_content}"
