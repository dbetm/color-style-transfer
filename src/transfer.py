import os
from typing import Tuple

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


# setup
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_ID = "gemini-2.5-flash-image-preview"


client = genai.Client(api_key=GOOGLE_API_KEY)
text_prompt = (
    "Recolor the target image using the provided color palette as reference." 
    " Apply the palette consistently across the entire image." 
    " Preserve details, textures, and natural shading while maintaining overall harmony and balance."
)


def transfer_color_style(target: Image.Image, palette_img: Image.Image) -> Tuple[Image.Image, bool]:
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[
            text_prompt,
            # the orden matters
            target,
            palette_img,
        ],
        config=types.GenerateContentConfig(
            #response_modalities=['Text', 'Image'],
            response_modalities=['Image'],
            top_p=0.6,
        ),
    )

    if response:
        for part in response.parts:
            if part.text:
                continue
            return part.as_image(), False

    return None, True