import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data sweeper", layout='wide')
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization")

uploaded_files = st.file_uploader("Upload your files (CSV Or Excel):",type =["csv","xlsx"],
accept_multiple_files = True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupporrted file type: {file_ext}")
            continue

# Display Info About The File

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        # Show 5 Rows Of Our DF

        st.write("Preview The Head Of The DataFrame")
        st.dataframe(df.head())

        # Options For Data Cleaning

        st.subheader("Data Cleaning Option")
        if st.checkbox(f"Clean Data For {file.name}"):
            col1, col2 =st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates From {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicate Removed")
            with col2:
                if st.button(f"Fill Missing Values For {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Have Been Filled!")
            # Chose Specific Coloumn To Keep Or Convert
        st.subheader("Select Columns To Convert")
        columns = st.multiselect(f"Chose Column For {file.name}", df.columns, default=df.columns)

            # Create Some Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization For {file.name}"):
            st.bar_chart(df.select_dtypes(include = 'number').iloc[:,:2])

        # Convert The File --> CSV To Excel
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to: ", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index = False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            
            elif conversion_type == "Excel":
                df.to_excel(buffer, index = False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            # Download Button
            st.download_button(
                label = f"Download {file.name} as {conversion_type}",
                data = buffer,
                file_name = file_name,
                mime = mime_type
            ) 
st.success("All File Processed!")