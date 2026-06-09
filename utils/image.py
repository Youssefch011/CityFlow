"""
Image utility for CityFlow locations.
Loads local images from assets/images and converts them to base64 for HTML cards.
Works with filenames like "sagrada_familia.jpg" and paths like "assets/images/sagrada_familia.jpg".
"""

import base64
from pathlib import Path

IMAGE_FOLDER = Path("assets") / "images"


def get_image_path(filename):
    if filename is None:
        return None

    filename = str(filename).strip()
    if filename == "":
        return None

    path = Path(filename)

    # Allow project asset paths such as assets/cityflow_logo.png.
    if path.exists():
        return path

    # If locations.csv already contains assets/images/name.jpg, use it directly.
    if len(path.parts) >= 2 and path.parts[0] == "assets" and path.parts[1] == "images":
        return path

    # Otherwise, treat it as a simple file name inside assets/images.
    return IMAGE_FOLDER / path.name


def image_exists_locally(filename):
    image_path = get_image_path(filename)
    return bool(image_path and image_path.exists())


def get_safe_image(filename):
    image_path = get_image_path(filename)
    if image_path and image_path.exists():
        return str(image_path)
    return None


def image_to_base64(image_path):
    if not image_path:
        return None

    path = Path(image_path)
    if not path.exists():
        return None

    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_image_base64(filename):
    image_path = get_safe_image(filename)
    if not image_path:
        return None
    return image_to_base64(image_path)


def get_missing_images(locations_df):
    missing_images = []

    if "image" not in locations_df.columns:
        return ["The column 'image' does not exist in locations.csv"]

    for _, row in locations_df.iterrows():
        image_name = row["image"]
        if not image_exists_locally(image_name):
            missing_images.append(image_name)

    return missing_images


def show_image_if_exists(st, filename, caption=None):
    image_path = get_safe_image(filename)
    if image_path:
        st.image(image_path, caption=caption, use_container_width=True)
    else:
        st.info("Image not available yet.")
