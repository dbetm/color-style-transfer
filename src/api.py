import io
import logging as logger
import time

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.img_utils import generate_color_palette, resize_image
from src.transfer import transfer_color_style


logger.basicConfig(level=logger.INFO)


def process(reference_file: UploadedFile, target_file: UploadedFile) -> tuple:
    reference = Image.open(reference_file)
    target = Image.open(target_file)

    logger.info(f"New reference image {reference.format}, width: {reference.width}, height: {reference.height}")
    logger.info(f"New target image {target.format}, width: {target.width}, height: {target.height}")

    logger.info("Resizing reference image...")
    reference = resize_image(reference, max_size=1200)
    color_palette_img = generate_color_palette(reference, target)

    logger.info("Generating composed image...")
    start_time = time.time()
    img_res, has_error = transfer_color_style(target, color_palette_img)
    end_time = time.time()
    logger.info(f"Time taken: {end_time - start_time} seconds")

    if has_error:
        return None, None, True

    buffer = io.BytesIO()
    format = "PNG"

    if (target.height * target.width) > 2_073_600: # 1080 * 1920
        format = "JPEG"

    img_res.save(buffer, format=format)
    buffer.seek(0)

    return buffer, format, has_error