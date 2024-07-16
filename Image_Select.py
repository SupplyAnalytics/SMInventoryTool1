from streamlit_image_select import image_select
import numpy as np
import PIL

img = image_select(
    label="Select a cat",
    images=['https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-93eb6705-f4b2-49a0-b611-d6eea317b0b9.PNG',
        'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-ed183c0b-b00b-4bed-aa4d-5e80652083f7.jpeg',
       'https://bijnis.s3.amazonaws.com/PRODUCTION/uploads/uploadfile_1-cdd80568-6d42-499a-b4ba-085867bd393d.jpeg'
    ],
    captions=["Image1", "Image2", "Image3"],
)
