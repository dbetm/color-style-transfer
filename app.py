import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison

from src.api import process
from src.utils import build_result_filename



FILE_FORMATS = ["jpg", "jpeg", "png", "webp"]



def reset():
    # Increment counter to create new file uploader instances
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    st.session_state.reset_counter += 1


def run():
    st.title("Color Style Transfer")
    st.write(
        "Upload a reference image to extract its colors, then a target photo to apply them using"
        " Google’s Nano Banana generative AI."
    )

    st.markdown("[GitHub repo](https://github.com/dbetm/color-style-transfer)")

    # Initialize reset counter
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0

    reference_file = st.file_uploader(
        "Choose a reference photo",
        type=FILE_FORMATS,
        key=f"ref_img_{st.session_state.reset_counter}"
    )
    target_file = st.file_uploader(
        "Choose a target photo",
        type=FILE_FORMATS,
        key=f"target_img_{st.session_state.reset_counter}"
    )

    if reference_file is not None and target_file is not None:
        target_filename = target_file.name

        st.image(reference_file, width=400, caption="Reference colors")
        st.image(target_file, width=400, caption="Target")

        with st.spinner("In progress..."):
            image_bytes, format, has_error = process(reference_file, target_file)

        if has_error:
            #st.image(image_bytes, width=600)
            st.error(
                body="Error while generating the final image, refresh and try again...",
                icon="🚨",
            )
        else:
            filename = build_result_filename(target_filename, format.lower())

            st.divider()
            st.success("Color transferred successfully!")

            # Interactive comparison slider
            image_comparison(
                img1=Image.open(target_file),
                img2=Image.open(image_bytes),
                label1="Original",
                label2="Result",
                width=600,
                in_memory=True,
            )

            st.download_button("Download", image_bytes, file_name=filename, on_click=reset)

        st.button("Clear", on_click=reset)
        st.info(body="App created by David Betancourt Montellano")



if __name__ == "__main__":
    run()