import streamlit as st
from io import BytesIO
from PIL import Image
from DB_CONNECT import condb
import numpy as np
mydb = condb()
c = mydb.cursor()
def select_pil(params, outfile=None):
    sql_cmd = """
        SELECT vetImg FROM vettable WHERE vetId = %s limit 1;
    """
    c.execute(sql_cmd, params)
    row = c.fetchone()
    if row:
        bytes_stream = BytesIO(row[0])
        img = Image.open(bytes_stream)
        return img
    return None

def app():
    st.title('หน้าแรก')
    st.image(select_pil([3]))
    none = Image.open('none.png')
    st.image(none)
    st.write("")
    test = ['', 'A', 'B']
    result = st.selectbox('จังหวัด :', test)
    st.write(f'.... {result}')
