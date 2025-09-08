from datetime import datetime


def build_result_filename(filename: str, format: str) -> str:
    now_str = datetime.now().strftime("%Y%m%d_%H%M")

    name_without_extension = filename.split(".")
    name_without_extension = "_".join(name_without_extension[:-1])

    return f"color_transfer_nano_banana_{name_without_extension}_{now_str}.{format}"