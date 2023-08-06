import streamlit as st
import pandas as pd
import numpy as np

st.title("Test App")
uploaded_file = st.file_uploader(label="file upload", 
                                type=["csv", "xlsx"],
                                accept_multiple_files=True, 
                                help="please upload your file")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)