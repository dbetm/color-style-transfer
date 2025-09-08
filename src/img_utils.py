import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def get_k_representatives(pixels: np.array, k: int = 5, sort: bool = True) -> list:
    """Given an array (1, N*(r,g,b)), compute the k cluster and then return the centroids
    which are representatives of the pixels group given."""
    k_means_cluster = KMeans(n_clusters=k, n_init=5).fit(pixels)
    centroids = k_means_cluster.cluster_centers_

    # Sort the centroids by their proximity to the origin
    if sort:
        centroids_distances = np.linalg.norm(centroids, axis=1)
        sorted_centroids_indices = np.argsort(centroids_distances)
        return centroids[sorted_centroids_indices]

    return centroids


def resize_image(img: Image.Image, max_size: int = 1500) -> Image.Image:
    """Resize a PIL Image so its longest side is exactly max_size, preserving aspect ratio.
    This will upscale images smaller than max_size and downscale images larger than max_size.
    """
    width, height = img.size
    # Compute scaling factor so that the longest side becomes max_size
    scale = max_size / float(max(width, height))
    new_size = (int(round(width * scale)), int(round(height * scale)))

    # Use high-quality resampling filter
    return img.resize(new_size, Image.LANCZOS)


def image_to_flat_rgb_array(img: Image.Image):
    # Ensure RGB mode
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Convert to NumPy array (shape: H x W x 3)
    arr = np.array(img)

    # Reshape to flat list of (r,g,b) tuples
    return arr.reshape(-1, 3)


def get_base_img(height: int, width: int) -> Image.Image:
    return Image.new("RGB", (width, height), color="black")


def build_color_palette_img(dims: tuple, colors: np.array):
    slice_width = dims[1] // colors.shape[0]
    base_img = get_base_img(height=dims[0], width=dims[1])

    for idx, color in enumerate(colors):
        pixel = tuple(map(int, color))

        for y in range(0, dims[0]):
            start = idx*slice_width
            for x in range(start, start + slice_width):
                base_img.putpixel(xy=(x, y), value=pixel)

    return base_img


def generate_color_palette(reference: Image.Image, target: Image.Image):
    flatten_img = image_to_flat_rgb_array(reference)
    k_representative_colors = get_k_representatives(flatten_img, k=5, sort=True)

    color_palette_img = build_color_palette_img(
        (target.height, target.width), colors=k_representative_colors
    )
    return color_palette_img