import streamlit as st
from st_clickable_images import clickable_images

with st.sidebar:
    choice = st.radio("Radio", [1, 2, 3])

images = ['https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg']

clicked = clickable_images([
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg'
], 
    titles=[f"Product #{str(i)}" for i in range(5)],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "2px", "height": "80px","width": "80px"},
    key="clicked_images"
)
product_details = {
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG': {
        'Product Name': 'Product A',
        'First Live Date': '2024-01-01',
        'GMV Contributed': 'Rs 10,000',
        'Sourcing Factory': 'Factory X'
    },
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg': {
        'Product Name': 'Product B',
        'First Live Date': '2024-02-01',
        'GMV Contributed': 'Rs 20,000',
        'Sourcing Factory': 'Factory Y'
    },
    'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg': {
        'Product Name': 'Product C',
        'First Live Date': '2024-03-01',
        'GMV Contributed': 'Rs 30,000',
        'Sourcing Factory': 'Factory Z'
    }
}

st.write(product_details)

st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")