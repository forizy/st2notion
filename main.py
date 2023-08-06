import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2 import service_account
import gspread 


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)

gs = gspread.authorize(credentials=credentials)

def read_sheet(sheetName:str, worksheet:str) -> pd.DataFrame:
    daily_gs = gs.open_by_key(st.secrets["google_sheet_keys"]["daily_results_sheet"])
    daily_gs.worksheet("입력")

    df = pd.DataFrame(daily_gs.worksheet("입력").get_all_values())
    df.columns = [df.iloc[i].values for i in range(3)]

    df = df[3:].reset_index(drop=True)
    df.drop(df[df[df.columns[0]] == ""].index, inplace=True)
    for col in df.columns[8:]:
        df[col] = df[col].str.replace(",", "").astype(int)
    return df

df = read_sheet("daily_results_sheet", "입력")

st.title("Test App")

dff = df.copy()
dff.columns = ["".join(col) for col in dff.columns.values]
st.dataframe(dff)

df_monthly = df.groupby(by=df.columns[6]).sum()[df.columns[8]].reset_index()
df_monthly.columns = ["연월", "진료 합계"]
st.bar_chart(data=df_monthly, x=df_monthly.columns[0], y=df_monthly.columns[1])
