import streamlit as st
import pandas as pd
import datetime
from PIL import Image
from io import BytesIO
import requests
import os
import subprocess


# Function to resize the image
def resize_image(url, width, height):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((width, height), Image.LANCZOS)
    return img

# Function to log actions
def log_action(log_df, variant_id, AlertType, original_df):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([[variant_id, AlertType, current_time]], columns=['VariantId', 'AlertType', 'Timestamp'])
    log_df = pd.concat([log_df, log_entry], ignore_index=True)
    original_df.loc[original_df['VariantId'] == variant_id, 'AlertType'] = AlertType
    return log_df, original_df

# Function to run Git commands
def run_git_commands(file_paths, commit_message):
    # Define the SSH command to use the specific SSH key
    ssh_command = 'ssh -i ~/.ssh/id_rsa'
    
    # Update the Git configuration to use the specified SSH key
    subprocess.run(['git', 'config', '--global', 'core.sshCommand', ssh_command])
    
    # Configure the Git user name and email
    subprocess.run(['git', 'config', '--global', 'user.email', 'supplyanalytics@bijnis.com'])
    subprocess.run(['git', 'config', '--global', 'user.name', 'SupplyAnalytics'])
    
    try:
        for file_path in file_paths:
            subprocess.run(['git', 'add', file_path], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred while running Git commands: {e}")

# Function to display image gallery
def image_gallery(df, log_df, result_dict, images, layer_name, start_index):
    product_details = result_dict
    num_columns = 8

    cols = st.columns(num_columns)
    for idx, img_url in enumerate(images):
        col = cols[idx % num_columns]
        col.image(img_url)
        if img_url in product_details:
            details = product_details[img_url]
            col.write(f"{details['ProductName']}")
            
            button_cols = col.columns(2)
            unique_key_forward = f"{layer_name}_forward_{idx}_{img_url}"
            unique_key_remove = f"{layer_name}_remove_{idx}_{img_url}"
            
            forward_button = button_cols[0].button(r"$\textsf{+}$", key=unique_key_forward)
            if forward_button:
                log_df, original_df = log_action(log_df, details['VariantId'], 'Forwarded to seller', st.session_state.original_df)
                images.remove(img_url)
                st.session_state['yellow_images'].append(img_url)
                st.session_state['log_df'] = log_df
                original_df.to_csv('Inactive_variants_data.csv', index=False)
                log_df.to_csv('Log_DF.csv', index=False)
                # Run Git commands
                run_git_commands(['Inactive_variants_data.csv', 'Log_DF.csv'], 'Updated CSV files')
                st.rerun()
            
            remove_button = button_cols[1].button(r"$\textsf{-}$", key=unique_key_remove, type="primary")
            if remove_button:
                log_df, original_df = log_action(log_df, details['VariantId'], 'Removed', st.session_state.original_df)
                images.remove(img_url)
                st.session_state[f"{layer_name}_images"] = images
                st.session_state['log_df'] = log_df
                original_df.to_csv('Inactive_variants_data.csv', index=False)
                log_df.to_csv('Log_DF.csv', index=False)
                # Run Git commands
                run_git_commands(['Inactive_variants_data.csv', 'Log_DF.csv'], 'Updated CSV files')
                st.rerun()

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
            st.session_state.email = email
            st.rerun()
else:
    # Main application code
    # Load the original full dataframe
    if "original_df" not in st.session_state:
        st.session_state.original_df = pd.read_csv('Inactive_variants_data.csv')
    
    # Filter the dataframe based on the logged-in user's email
    email = st.session_state.email
    df = st.session_state.original_df[st.session_state.original_df['SmEmail'] == email]
    
    # Load persistent log_df
    if "log_df" not in st.session_state:
        if os.path.exists('Log_DF.csv'):
            st.session_state.log_df = pd.read_csv('Log_DF.csv')
        else:
            st.session_state.log_df = pd.DataFrame(columns=['VariantId', 'AlertType', 'Timestamp'])
    
    log_df = st.session_state.log_df

    if "red_images" not in st.session_state:
        st.session_state.red_images = df[df['AlertType'] == "INACTIVE"]['resizeUrl'].tolist()
    if "yellow_images" not in st.session_state:
        st.session_state.yellow_images = df[df['AlertType'] == "Forwarded to seller"]['resizeUrl'].tolist()
    if "green_images" not in st.session_state:
        st.session_state.green_images = []

    result_dict = {}
    for index, row in df.iterrows():
        result_dict[row['resizeUrl']] = {
            'VariantId': row['VariantId'],
            'ProductName': row['ProductName'],
            'Last 30 Days GMV': row['Last 30 Days GMV'],
            'SMName': row['SMName']
        }

    with st.container(border=True):
        st.header("Out of Stock")
        image_gallery(df, log_df, result_dict, st.session_state.red_images, 'red', start_index=st.session_state.red_index)
    with st.container(border=True):
        st.header("Forwarded to Seller")
        image_gallery(df, log_df, result_dict, st.session_state.yellow_images, 'yellow', start_index=st.session_state.yellow_index)
    with st.container(border=True):
        st.header("Live Variants")
