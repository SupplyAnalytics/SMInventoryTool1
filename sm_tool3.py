import streamlit as st
import pandas as pd
import datetime
from PIL import Image
from io import BytesIO
import requests


def resize_image(url, width, height):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((width, height),Image.LANCZOS)
    
    return img


def log_action(log_df, variant_id, status, df):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([[variant_id, status, current_time]], columns=['VariantId', 'Status', 'Timestamp'])
    log_df = pd.concat([log_df, log_entry], ignore_index=True)
    df.loc[df['VariantId'] == variant_id, 'Status'] = status
    return log_df, df

def image_gallery(df, log_df, result_dict, images, layer_name, start_index):
    product_details = result_dict
    num_columns = 8
    i = 0

    cols = st.columns(num_columns)
    for idx, img_url in enumerate(images):
        col = cols[idx % num_columns] 
        # image = resize_image(img_url, width = 160, height = 160) 
        col.image(img_url)
        if img_url in product_details:
            details = product_details[img_url]
            col.write(f"{details['Productname']}")
            # col.write(f"{details['Last30DayGMV']}")
            
            button_cols = col.columns(2)
            forward_button = button_cols[0].button(r"$\textsf{+}$", key=f"{idx}_forward_{img_url}_{i}")
            if forward_button:
                log_df, df = log_action(log_df, details['VariantId'], 'Forwarded to seller', df)
                images.remove(img_url)
                st.session_state['yellow_images'].append(img_url)
                st.session_state['log_df'] = log_df
                df.to_csv('VLD.csv', index=False)
                st.rerun()
            remove_button = button_cols[1].button(r"$\textsf{-}$", key=f"{idx}_remove_{img_url}_{i}", type="primary")
            if remove_button:
                log_df, df = log_action(log_df, details['VariantId'], 'Removed', df)
                images.remove(img_url)
                st.session_state[f"{layer_name}_images"] = images
                st.session_state['log_df'] = log_df
                df.to_csv('VLD.csv', index=False)
                st.rerun()
            log_df.to_csv('Log_DF.csv', index=False)
            i = i + 1

# Set up the page layout
st.set_page_config(layout="wide")



# Initialize session state variables if they don't exist
if "red_index" not in st.session_state:
    st.session_state.red_index = 0
if "yellow_index" not in st.session_state:
    st.session_state.yellow_index = 0
if "green_index" not in st.session_state:
    st.session_state.green_index = 0

# Login logic
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False




# Check if the user is logged in
if not st.session_state.logged_in:
    # Login form
    st.title("Login")
    email = st.text_input("Email")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1]) 
    with col1:
        Platform = st.selectbox("Select Platform", ["All", "Production", "Distribution", "BijnisExpress"], index=0)
    with col2:
        supercategory = st.selectbox("Select SuperCat", ["All", "Footwear", "Apparels"])
    with col3:
        subcategory = st.selectbox("Select Subcat", ["All"], index=0)
    with col4:
        price_ranges = st.slider("Select Price Range", 0, 5000, (0, 5000), step=50)
    if st.button("Submit"):
        if email:  # You can add more validation if needed
            st.session_state.logged_in = True
            st.rerun()
else:
    # Main application code
    df = pd.read_csv('Inactive_variants_data.csv')

    if "red_images" not in st.session_state:
        st.session_state.red_images = df[df['Status'] == "Out of Stock"]['resizeUrl'].tolist()
    if "yellow_images" not in st.session_state:
        st.session_state.yellow_images = df[df['Status'] == "Forwarded to seller"]['resizeUrl'].tolist()
    if "green_images" not in st.session_state:
        st.session_state.green_images = []

    if "log_df" not in st.session_state:
        st.session_state.log_df = pd.DataFrame(columns=['VariantId', 'Status', 'Timestamp'])

    result_dict = {}
    for index, row in df.iterrows():
        result_dict[row['resizeUrl']] = {
            'VariantId': row['VariantId'],
            'Productname': row['Productname'],
            'Last30DayGMV': row['Last30DayGMV'],
            'SM': row['SM']
        }

    
    with st.container(border = True):
        st.header("Out of Stock")
        image_gallery(df, st.session_state.log_df, result_dict, st.session_state.red_images, 'red', start_index=st.session_state.red_index)
    with st.container(border = True):
        st.header("Forwarded to Seller")
        image_gallery(df, st.session_state.log_df, result_dict, st.session_state.yellow_images, 'yellow', start_index=st.session_state.yellow_index)
    with st.container(border = True):
        st.header("Live Variants")
