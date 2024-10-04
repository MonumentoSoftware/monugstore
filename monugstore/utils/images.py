from PIL import Image
import os


def create_thumbnail(image_path, thumbnail_path, size=(128, 128)):
    """
    Creates a thumbnail of the specified size from an image.

    :param image_path: Path to the original image.
    :param thumbnail_path: Path where the thumbnail will be saved.
    :param size: Size of the thumbnail (width, height). Default is (128, 128).
    """
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            img.save(thumbnail_path)

    except Exception as e:
        print(f"Error creating thumbnail: {e}")


def convert_to_webp(image_path, webp_path, quality=None):
    """
    Converts an image to WebP format, with an option for lossless or lossy compression.

    :param image_path: Path to the original image.
    :param webp_path: Path where the WebP image will be saved.
    :param quality: Optional quality level (0-100) for lossy compression.
                    If None, the conversion will be lossless.
    """
    try:
        with Image.open(image_path) as img:
            # Ensure the output path ends with .webp
            webp_path = webp_path.replace(os.path.splitext(webp_path)[1], ".webp")

            # If a quality level is provided, use lossy compression
            if quality is not None:
                img.save(webp_path, format='WEBP', quality=quality)
            else:
                img.save(webp_path, format='WEBP', lossless=True)

    except Exception as e:
        print(f"Error converting image to WebP: {e}")
