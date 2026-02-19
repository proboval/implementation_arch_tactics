#!/usr/bin/env python3
"""
Create thumbnail grids from PowerPoint slides or HTML slide directories.

Input modes:
  - .pptx file: converts slides to PNG via LibreOffice, then creates grid
  - Directory of PNG/JPG: uses images directly
  - Directory of HTML: renders each HTML slide to PNG via Playwright, then creates grid

Output:
- Single grid: {prefix}.jpg (if slides fit in one grid)
- Multiple grids: {prefix}-1.jpg, {prefix}-2.jpg, etc.

Grid limits by column count:
- 3 cols: max 12 slides per grid (3×4)
- 4 cols: max 20 slides per grid (4×5)
- 5 cols: max 30 slides per grid (5×6) [default]
- 6 cols: max 42 slides per grid (6×7)

Usage:
    python thumbnail.py input.pptx [output_prefix] [--cols N]
    python thumbnail.py slides/ [output_prefix] [--cols N]

Examples:
    python thumbnail.py presentation.pptx
    python thumbnail.py slides/ grid --cols 4
    python thumbnail.py template.pptx analysis --outline-placeholders
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from inventory import extract_text_inventory
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation

# Constants
THUMBNAIL_WIDTH = 300  # Fixed thumbnail width in pixels
CONVERSION_DPI = 100  # DPI for image conversion
MAX_COLS = 6  # Maximum number of columns
DEFAULT_COLS = 5  # Default number of columns
JPEG_QUALITY = 95  # JPEG compression quality

# Grid layout constants
GRID_PADDING = 20  # Padding between thumbnails
BORDER_WIDTH = 2  # Border width around thumbnails
FONT_SIZE_RATIO = 0.12  # Font size as fraction of thumbnail width
LABEL_PADDING_RATIO = 0.4  # Label padding as fraction of font size


def find_soffice():
    """Find LibreOffice soffice executable."""
    soffice = shutil.which("soffice")
    if soffice:
        return soffice
    # Windows paths (Scoop, standard installs)
    home = Path.home()
    candidates = [
        home / "scoop/apps/libreoffice/current/LibreOffice/program/soffice.exe",
        Path("C:/Program Files/LibreOffice/program/soffice.exe"),
        Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def find_node():
    """Find Node.js executable."""
    node = shutil.which("node")
    if node:
        return node
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Create thumbnail grids from PowerPoint slides or HTML slide directories."
    )
    parser.add_argument("input", help="Input .pptx file, or directory of PNG/HTML slides")
    parser.add_argument(
        "output_prefix",
        nargs="?",
        default="thumbnails",
        help="Output prefix for image files (default: thumbnails, will create prefix.jpg or prefix-N.jpg)",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=DEFAULT_COLS,
        help=f"Number of columns (default: {DEFAULT_COLS}, max: {MAX_COLS})",
    )
    parser.add_argument(
        "--outline-placeholders",
        action="store_true",
        help="Outline text placeholders with a colored border",
    )

    args = parser.parse_args()

    # Validate columns
    cols = min(args.cols, MAX_COLS)
    if args.cols > MAX_COLS:
        print(f"Warning: Columns limited to {MAX_COLS} (requested {args.cols})")

    input_path = Path(args.input)

    # Detect input mode: directory of images/HTML, or .pptx file
    is_dir = input_path.is_dir()
    is_pptx = input_path.exists() and input_path.suffix.lower() == ".pptx"

    if not is_dir and not is_pptx:
        print(f"Error: Input must be a .pptx file or a directory of slides: {args.input}")
        sys.exit(1)

    # Construct output path (always JPG)
    output_path = Path(f"{args.output_prefix}.jpg")

    print(f"Processing: {args.input}")

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            placeholder_regions = None
            slide_dimensions = None

            if is_dir:
                # Directory mode: read existing PNG/JPG files, or render HTML slides
                slide_images = load_from_directory(input_path, Path(temp_dir))
            else:
                # PPTX mode
                if args.outline_placeholders:
                    print("Extracting placeholder regions...")
                    placeholder_regions, slide_dimensions = get_placeholder_regions(
                        input_path
                    )
                    if placeholder_regions:
                        print(f"Found placeholders on {len(placeholder_regions)} slides")

                slide_images = convert_to_images(input_path, Path(temp_dir))

            if not slide_images:
                print("Error: No slides found")
                sys.exit(1)

            print(f"Found {len(slide_images)} slides")

            # Create grids (max cols×(cols+1) images per grid)
            grid_files = create_grids(
                slide_images,
                cols,
                THUMBNAIL_WIDTH,
                output_path,
                placeholder_regions,
                slide_dimensions,
            )

            # Print saved files
            print(f"Created {len(grid_files)} grid(s):")
            for grid_file in grid_files:
                print(f"  - {grid_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def create_hidden_slide_placeholder(size):
    """Create placeholder image for hidden slides."""
    img = Image.new("RGB", size, color="#F0F0F0")
    draw = ImageDraw.Draw(img)
    line_width = max(5, min(size) // 100)
    draw.line([(0, 0), size], fill="#CCCCCC", width=line_width)
    draw.line([(size[0], 0), (0, size[1])], fill="#CCCCCC", width=line_width)
    return img


def get_placeholder_regions(pptx_path):
    """Extract ALL text regions from the presentation.

    Returns a tuple of (placeholder_regions, slide_dimensions).
    text_regions is a dict mapping slide indices to lists of text regions.
    Each region is a dict with 'left', 'top', 'width', 'height' in inches.
    slide_dimensions is a tuple of (width_inches, height_inches).
    """
    prs = Presentation(str(pptx_path))
    inventory = extract_text_inventory(pptx_path, prs)
    placeholder_regions = {}

    # Get actual slide dimensions in inches (EMU to inches conversion)
    slide_width_inches = (prs.slide_width or 9144000) / 914400.0
    slide_height_inches = (prs.slide_height or 5143500) / 914400.0

    for slide_key, shapes in inventory.items():
        # Extract slide index from "slide-N" format
        slide_idx = int(slide_key.split("-")[1])
        regions = []

        for shape_key, shape_data in shapes.items():
            # The inventory only contains shapes with text, so all shapes should be highlighted
            regions.append(
                {
                    "left": shape_data.left,
                    "top": shape_data.top,
                    "width": shape_data.width,
                    "height": shape_data.height,
                }
            )

        if regions:
            placeholder_regions[slide_idx] = regions

    return placeholder_regions, (slide_width_inches, slide_height_inches)


def load_from_directory(dir_path, temp_dir):
    """Load slide images from a directory of PNG/JPG files, or render HTML slides first.

    Prefers HTML slides (renders via Playwright). Falls back to existing images
    only when no HTML files are found. Filters out non-slide images (logo, thumbnails).
    """
    # Check for HTML files first — these are preferred (renders fresh PNGs)
    html_files = sorted(dir_path.glob("*.html"))
    if not html_files:
        # No HTML — try existing image files, filtering out non-slide images
        skip = {"logo", "thumbnail", "thumbnails"}
        images = sorted(
            f for f in list(dir_path.glob("*.png")) + list(dir_path.glob("*.jpg"))
            if f.stem.lower() not in skip
        )
        if images:
            print(f"Found {len(images)} image files in {dir_path}")
            return images
        raise RuntimeError(f"No PNG, JPG, or HTML files found in {dir_path}")

    print(f"Found {len(html_files)} HTML slides — rendering to PNG...")
    node = find_node()
    if not node:
        raise RuntimeError("Node.js not found. Required to render HTML slides.")

    screenshot_script = Path(__file__).parent / "screenshot.js"
    if not screenshot_script.exists():
        raise RuntimeError(f"screenshot.js not found at {screenshot_script}")

    png_dir = temp_dir / "png"
    result = subprocess.run(
        [node, str(screenshot_script), str(dir_path), str(png_dir)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"HTML screenshot failed: {result.stderr}")
    print(result.stdout.strip())

    images = sorted(png_dir.glob("*.png"))
    if not images:
        raise RuntimeError("No PNG files generated from HTML slides")
    return images


def convert_to_images(pptx_path, temp_dir):
    """Convert PowerPoint to PNG images, handling hidden slides."""
    # Detect hidden slides
    print("Analyzing presentation...")
    prs = Presentation(str(pptx_path))
    total_slides = len(prs.slides)

    hidden_slides = {
        idx + 1
        for idx, slide in enumerate(prs.slides)
        if slide.element.get("show") == "0"
    }

    print(f"Total slides: {total_slides}")
    if hidden_slides:
        print(f"Hidden slides: {sorted(hidden_slides)}")

    soffice = find_soffice()
    if not soffice:
        raise RuntimeError(
            "LibreOffice not found. Install via: scoop install libreoffice\n"
            "Or pass a directory of HTML/PNG slides instead of a .pptx file."
        )

    # Convert to PNG using LibreOffice
    print("Converting to PNG images...")
    result = subprocess.run(
        [soffice, "--headless", "--convert-to", "png",
         "--outdir", str(temp_dir), str(pptx_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice PNG conversion failed: {result.stderr}")

    # Collect generated PNG files
    visible_images = sorted(temp_dir.glob("*.png"))

    if not visible_images:
        raise RuntimeError("No PNG files generated by LibreOffice")

    # Create full list with placeholders for hidden slides
    all_images = []
    visible_idx = 0

    if visible_images:
        with Image.open(visible_images[0]) as img:
            placeholder_size = img.size
    else:
        placeholder_size = (1920, 1080)

    for slide_num in range(1, total_slides + 1):
        if slide_num in hidden_slides:
            placeholder_path = temp_dir / f"hidden-{slide_num:03d}.png"
            placeholder_img = create_hidden_slide_placeholder(placeholder_size)
            placeholder_img.save(placeholder_path, "PNG")
            all_images.append(placeholder_path)
        else:
            if visible_idx < len(visible_images):
                all_images.append(visible_images[visible_idx])
                visible_idx += 1

    return all_images


def create_grids(
    image_paths,
    cols,
    width,
    output_path,
    placeholder_regions=None,
    slide_dimensions=None,
):
    """Create multiple thumbnail grids from slide images, max cols×(cols+1) images per grid."""
    # Maximum images per grid is cols × (cols + 1) for better proportions
    max_images_per_grid = cols * (cols + 1)
    grid_files = []

    print(
        f"Creating grids with {cols} columns (max {max_images_per_grid} images per grid)"
    )

    # Split images into chunks
    for chunk_idx, start_idx in enumerate(
        range(0, len(image_paths), max_images_per_grid)
    ):
        end_idx = min(start_idx + max_images_per_grid, len(image_paths))
        chunk_images = image_paths[start_idx:end_idx]

        # Create grid for this chunk
        grid = create_grid(
            chunk_images, cols, width, start_idx, placeholder_regions, slide_dimensions
        )

        # Generate output filename
        if len(image_paths) <= max_images_per_grid:
            # Single grid - use base filename without suffix
            grid_filename = output_path
        else:
            # Multiple grids - insert index before extension with dash
            stem = output_path.stem
            suffix = output_path.suffix
            grid_filename = output_path.parent / f"{stem}-{chunk_idx + 1}{suffix}"

        # Save grid
        grid_filename.parent.mkdir(parents=True, exist_ok=True)
        grid.save(str(grid_filename), quality=JPEG_QUALITY)
        grid_files.append(str(grid_filename))

    return grid_files


def create_grid(
    image_paths,
    cols,
    width,
    start_slide_num=0,
    placeholder_regions=None,
    slide_dimensions=None,
):
    """Create thumbnail grid from slide images with optional placeholder outlining."""
    font_size = int(width * FONT_SIZE_RATIO)
    label_padding = int(font_size * LABEL_PADDING_RATIO)

    # Get dimensions
    with Image.open(image_paths[0]) as img:
        aspect = img.height / img.width
    height = int(width * aspect)

    # Calculate grid size
    rows = (len(image_paths) + cols - 1) // cols
    grid_w = cols * width + (cols + 1) * GRID_PADDING
    grid_h = rows * (height + font_size + label_padding * 2) + (rows + 1) * GRID_PADDING

    # Create grid
    grid = Image.new("RGB", (grid_w, grid_h), "white")
    draw = ImageDraw.Draw(grid)

    # Load font with size based on thumbnail width
    try:
        # Use Pillow's default font with size
        font = ImageFont.load_default(size=font_size)
    except Exception:
        # Fall back to basic default font if size parameter not supported
        font = ImageFont.load_default()

    # Place thumbnails
    for i, img_path in enumerate(image_paths):
        row, col = i // cols, i % cols
        x = col * width + (col + 1) * GRID_PADDING
        y_base = (
            row * (height + font_size + label_padding * 2) + (row + 1) * GRID_PADDING
        )

        # Add label with actual slide number
        label = f"{start_slide_num + i}"
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text(
            (x + (width - text_w) // 2, y_base + label_padding),
            label,
            fill="black",
            font=font,
        )

        # Add thumbnail below label with proportional spacing
        y_thumbnail = y_base + label_padding + font_size + label_padding

        with Image.open(img_path) as img:
            # Get original dimensions before thumbnail
            orig_w, orig_h = img.size

            # Apply placeholder outlines if enabled
            if placeholder_regions and (start_slide_num + i) in placeholder_regions:
                # Convert to RGBA for transparency support
                if img.mode != "RGBA":
                    img = img.convert("RGBA")

                # Get the regions for this slide
                regions = placeholder_regions[start_slide_num + i]

                # Calculate scale factors using actual slide dimensions
                if slide_dimensions:
                    slide_width_inches, slide_height_inches = slide_dimensions
                else:
                    # Fallback: estimate from image size at CONVERSION_DPI
                    slide_width_inches = orig_w / CONVERSION_DPI
                    slide_height_inches = orig_h / CONVERSION_DPI

                x_scale = orig_w / slide_width_inches
                y_scale = orig_h / slide_height_inches

                # Create a highlight overlay
                overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
                overlay_draw = ImageDraw.Draw(overlay)

                # Highlight each placeholder region
                for region in regions:
                    # Convert from inches to pixels in the original image
                    px_left = int(region["left"] * x_scale)
                    px_top = int(region["top"] * y_scale)
                    px_width = int(region["width"] * x_scale)
                    px_height = int(region["height"] * y_scale)

                    # Draw highlight outline with red color and thick stroke
                    # Using a bright red outline instead of fill
                    stroke_width = max(
                        5, min(orig_w, orig_h) // 150
                    )  # Thicker proportional stroke width
                    overlay_draw.rectangle(
                        [(px_left, px_top), (px_left + px_width, px_top + px_height)],
                        outline=(255, 0, 0, 255),  # Bright red, fully opaque
                        width=stroke_width,
                    )

                # Composite the overlay onto the image using alpha blending
                img = Image.alpha_composite(img, overlay)
                # Convert back to RGB for JPEG saving
                img = img.convert("RGB")

            img.thumbnail((width, height), Image.Resampling.LANCZOS)
            w, h = img.size
            tx = x + (width - w) // 2
            ty = y_thumbnail + (height - h) // 2
            grid.paste(img, (tx, ty))

            # Add border
            if BORDER_WIDTH > 0:
                draw.rectangle(
                    [
                        (tx - BORDER_WIDTH, ty - BORDER_WIDTH),
                        (tx + w + BORDER_WIDTH - 1, ty + h + BORDER_WIDTH - 1),
                    ],
                    outline="gray",
                    width=BORDER_WIDTH,
                )

    return grid


if __name__ == "__main__":
    main()
