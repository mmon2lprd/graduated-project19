import streamlit as st
import pandas as pd
import datetime
from io import BytesIO
from PIL import Image
from DB_CONNECT import condb

mydb = condb()
c = mydb.cursor()


# Functions
@st.cache
def load_image(image_file):
    vetimg = Image.open(image_file)
    fp = BytesIO()
    vetimg.save(fp, "PNG")
    output = fp.getvalue()
    return output


def add_data(vet_name, vet_des, vet_date, vet_img):
    sql = "INSERT INTO vettable(vetName, vetDes, vetDate, vetImg) VALUES (%s, %s, %s, %s);"
    val = (vet_name, vet_des, vet_date, vet_img)
    c.execute(sql, val)
    mydb.commit()


def view_all_vetlists():
    c.execute('SELECT vetId, vetName, vetDes, vetDate FROM vettable ORDER BY vetId ASC;')
    data = c.fetchall()
    return data


def app():
    st.title("ลงทะเบียนพืช")
    timenow = datetime.datetime.now()
    Date = timenow.strftime('%Y-%m-%d')
    Time = timenow.strftime('%H:%M')
    st.subheader('ณ วันที่ {} เวลา {}'.format(Date, Time))
    # Display
    result = view_all_vetlists()
    clean_db = pd.DataFrame(result, columns=["รหัสพืช", "รายชื่อพืช", "คำบรรยายพืช"])
    st.dataframe(clean_db, height=200)
    # Input Form
    vet_name = st.text_input("ชื่อ :", max_chars=50)
    vet_des = st.text_area("คำบรรยาย :", height=250)
    image_file = st.file_uploader("แนบไฟล์รูป :", type=['png', 'jpg', 'jpeg'])
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        submitted = st.button(label='เพิ่มข้อมูล')
    if image_file is not None:
        file_details = {"FileName": image_file.name, "FileType": image_file.type}
        st.write(file_details)
        vet_img = load_image(image_file)
        st.image(vet_img, use_column_width='auto', output_format='PNG')
    else:
        vet_img = None
    if submitted:
        add_data(vet_name, vet_des, vet_date, vet_img)
        rowc = c.rowcount
        st.success("การลงทะเบียน{} สำเร็จ! จำนวน {} แถว".format(vet_name, rowc))
