import streamlit as st
from io import BytesIO
from PIL import Image
from DB_CONNECT import condb
import numpy as np
mydb = condb()
c = mydb.cursor()

def app():
    st.title('หน้าแรก')
    st.write("ยินดีต้อนรับ")
