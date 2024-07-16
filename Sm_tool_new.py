import streamlit as st
from streamlit_image_select import image_select
import math

# Define the CSS for the background colors and borders of each layer
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f0f0f0;
}
.layer-red {
    background-color: #ffcccc;
    padding: 20px;
    margin-bottom: 30px;
    border-radius: 10px;
}
.layer-yellow {
    background-color: #ffffcc;
    padding: 20px;
    margin-bottom: 30px;
    border-radius: 10px;
}
.layer-green {
    background-color: #ccffcc;
    padding: 20px;
    margin-bottom: 30px;
    border-radius: 10px;
}
.image-container {
    display: flex;
    flex-wrap: wrap;
    gap: 40px;  /* Increased gap between images */
    justify-content: space-around;
}
img.layer-yellow-selected {
    border: 50px solid yellow;
}
img.layer-green-selected {
    border: 50px solid green;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sample image URLs and product details
default_images = [
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg'
]

product_details = {
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG': {
        'Product Name': 'Product A',
        'First Live Date': '2023-01-01',
        'GMV Contributed': 'Rs 10,000',
        'Sourcing Factory': 'Factory X'
    },
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg': {
        'Product Name': 'Product B',
        'First Live Date': '2023-02-01',
        'GMV Contributed': 'Rs 20,000',
        'Sourcing Factory': 'Factory Y'
    },
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg': {
        'Product Name': 'Product C',
        'First Live Date': '2023-03-01',
        'GMV Contributed': 'Rs 30,000',
        'Sourcing Factory': 'Factory Z'
    }
}

# Function to create image gallery with navigation
def create_image_gallery(images, layer_name, border_class, show_buttons, start_index):
    if not images:
        st.write(f"No images in {layer_name} layer")
        return

    images_per_page = 3
    end_index = min(start_index + images_per_page, len(images))
    current_images = images[start_index:end_index]
    
    selected_img = image_select(
        label=f"Select an image from {layer_name} layer",
        images=current_images,
        use_container_width=False
    )
    
    col3, col4, col5 = st.columns([1, 1, 1])
    with col3:
        if start_index > 0:
            st.button("Previous", key=f"{layer_name}_prev", on_click=change_page, args=(layer_name, start_index - images_per_page))
    with col4:
        st.text(f"Page {start_index // images_per_page + 1} of {math.ceil(len(images) / images_per_page)}")
    with col5:
        if end_index < len(images):
            st.button("Next", key=f"{layer_name}_next", on_click=change_page, args=(layer_name, start_index + images_per_page))
    
    if selected_img:
        col1, col2 = st.columns([1, 1])
        with col1:
            details = product_details.get(selected_img, {})
            if details:
                st.write("**Product Details**")
                st.write(f"Product Name: {details.get('Product Name')}")
                st.write(f"First Live Date: {details.get('First Live Date')}")
                st.write(f"GMV Contributed: {details.get('GMV Contributed')}")
                st.write(f"Sourcing Factory: {details.get('Sourcing Factory')}")
        with col2:
            st.image(selected_img, width=300, caption=border_class, use_column_width=False)
        
        if show_buttons:
            col1, col2 = st.columns(2)
            with col1:
                forward_button = st.button(f"Forward to seller", key=f"{layer_name}_forward")
                if forward_button:
                    images.remove(selected_img)
                    st.session_state[f"{layer_name}_images"] = images
                    st.session_state.yellow_images.append(selected_img)
                    st.experimental_rerun()
            with col2:
                remove_button = st.button(f"Remove", key=f"{layer_name}_remove")
                if remove_button:
                    images.remove(selected_img)
                    st.session_state[f"{layer_name}_images"] = images
                    st.experimental_rerun()

# Function to handle page change
def change_page(layer_name, new_index):
    st.session_state[f"{layer_name}_index"] = new_index

st.title("The Tool")

# Initialize session state for indices and images
if "red_index" not in st.session_state:
    st.session_state.red_index = 0
if "yellow_index" not in st.session_state:
    st.session_state.yellow_index = 0
if "green_index" not in st.session_state:
    st.session_state.green_index = 0

if "red_images" not in st.session_state:
    st.session_state.red_images = default_images.copy()
if "yellow_images" not in st.session_state:
    st.session_state.yellow_images = []
if "green_images" not in st.session_state:
    st.session_state.green_images = []

# Red Layer
st.header("Out of Stock")
create_image_gallery(st.session_state.red_images, 'red', '', show_buttons=True, start_index=st.session_state.red_index)

# Yellow Layer
st.header("Forwarded to Seller")
create_image_gallery(st.session_state.yellow_images, 'yellow', 'layer-yellow-selected', show_buttons=False, start_index=st.session_state.yellow_index)

# Green Layer
st.header("In Stock")
create_image_gallery(st.session_state.green_images, 'green', 'layer-green-selected', show_buttons=False, start_index=st.session_state.green_index)
