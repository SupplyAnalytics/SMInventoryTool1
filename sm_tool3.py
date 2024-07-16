import streamlit as st
import pandas as pd
import gspread
import datetime
from google.oauth2 import service_account

def export_data():
    json_key_path = 'cred.json'

    # Load credentials from the JSON key file
    creds = service_account.Credentials.from_service_account_file(json_key_path, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    # Authorize the client using the credentials
    client = gspread.authorize(creds)
    # Open the Google Sheets document by title
    source_sheet_title = 'Variant_Logging_Data_Base'
    source_sheet = client.open(source_sheet_title)
    # Select a specific worksheet within the source document
    source_worksheet = source_sheet.worksheet('Logging Data Base') 
    # Read existing data from the sheet
    existing_data = source_worksheet.get_all_values()
    sheet_df = pd.DataFrame(existing_data[1:], columns=existing_data[0])
    return sheet_df

def log_action(log_df, variant_id, status, df):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([[variant_id, status, current_time]], columns=['VariantId', 'Status', 'Timestamp'])
    log_df = pd.concat([log_df, log_entry], ignore_index=True)
    df.loc[df['VariantId'] == variant_id, 'Status'] = status
    return log_df, df

def image_gallery(df, log_df, result_dict, images, layer_name, start_index):
    # Product details dictionary
    product_details = result_dict
    # Number of columns
    num_columns = 8
    i = 0

    # Display images and product details in a grid layout
    cols = st.columns(num_columns)
    for idx, img_url in enumerate(images):
        col = cols[idx % num_columns]
        col.image(img_url, width=80)
        if img_url in product_details:
            details = product_details[img_url]
            col.write(f"{details['Productname']}")
            col.write(f"{details['Last30DayGMV']}")
            
            button_cols = col.columns(2)
            forward_button = button_cols[0].button("++", key=f"{idx}_forward_{img_url}_{i}")
            if forward_button:
                log_df, df = log_action(log_df, details['VariantId'], 'Forwarded to seller', df)
                images.remove(img_url)
                st.session_state['yellow_images'].append(img_url)
                st.session_state['log_df'] = log_df
                df.to_csv('VLD.csv', index=False)
                st.rerun()
            remove_button = button_cols[1].button("--", key=f"{idx}_remove_{img_url}_{i}")
            if remove_button:
                log_df, df = log_action(log_df, details['VariantId'], 'Removed', df)
                images.remove(img_url)
                st.session_state[f"{layer_name}_images"] = images
                st.session_state['log_df'] = log_df
                df.to_csv('VLD.csv', index=False)
                st.rerun()
            log_df.to_csv('Log_DF.csv', index=False)
            i = i + 1

# df = export_data()
df = pd.read_csv('VLD.csv')

if "red_index" not in st.session_state:
    st.session_state.red_index = 0
if "yellow_index" not in st.session_state:
    st.session_state.yellow_index = 0
if "green_index" not in st.session_state:
    st.session_state.green_index = 0

if "red_images" not in st.session_state:
    st.session_state.red_images = df[df['Status'] == "Out of Stock"]['ImageUrl'].tolist()
if "yellow_images" not in st.session_state:
    st.session_state.yellow_images = df[df['Status'] == "Forwarded to seller"]['ImageUrl'].tolist()
if "green_images" not in st.session_state:
    st.session_state.green_images = []

if "log_df" not in st.session_state:
    st.session_state.log_df = pd.DataFrame(columns=['VariantId', 'Status', 'Timestamp'])

result_dict = {}
for index, row in df.iterrows():
    result_dict[row['ImageUrl']] = {
        'VariantId': row['VariantId'],
        'Productname': row['Productname'],
        'Last30DayGMV': row['Last30DayGMV'],
        'SM': row['SM']
    }

st.header("Out of Stock")
image_gallery(df, st.session_state.log_df, result_dict, st.session_state.red_images, 'red', start_index=st.session_state.red_index)

st.header("Forwarded to Seller")
image_gallery(df, st.session_state.log_df, result_dict, st.session_state.yellow_images, 'yellow', start_index=st.session_state.yellow_index)

st.header("Live Variants")
