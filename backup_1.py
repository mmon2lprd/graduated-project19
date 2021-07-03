import streamlit as st
import pandas as pd
import datetime

#Database
import mysql.connector
createdb = mysql.connector.connect(host="localhost", user="root", passwd="root",auth_plugin='mysql_native_password')
cdb = createdb.cursor()
cdb.execute("CREATE DATABASE IF NOT EXISTS vetdb CHARSET UTF8 COLLATE utf8_general_ci;")
#Connect DB
mydb = mysql.connector.connect(host="localhost", user="root", passwd="root",database="vetdb",auth_plugin='mysql_native_password')
c = mydb.cursor()
print(mydb)
if(mydb):
    print('Connect database Successful!')

#Functions
def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS vettable(vet_id INT(4) ZEROFILL AUTO_INCREMENT,
              vet_name VARCHAR(50), vet_des VARCHAR(500),
              vet_date DATETIME, PRIMARY KEY(vet_id));""")

def add_data(vetName,vetDes,vetDate):
    sql = "INSERT INTO vettable(vet_name, vet_des, vet_date) VALUES (%s, %s, %s);"
    val = (vetName,vetDes,vetDate)
    c.execute(sql,val)
    mydb.commit()

def view_all_notes():
    c.execute('SELECT vet_id, vet_name, vet_des, vet_date FROM vettable')
    data = c.fetchall()
    return data

def main():
    #st.title("ระบบจัดการฐานข้อมูลการวางแผนผลผลิต")

    menu = ["หน้าแรก", "ลงทะเบียนเกษตรกร", "ลงทะเบียนพืช"]
    choice = st.sidebar.radio("Menu", menu)
    if choice == "หน้าแรก":
        st.subheader("ยินดีต้อนรับ")
        time = datetime.datetime.now()
        vetDate = time.strftime('%Y-%m-%d %H:%M:%S')
        st.write(vetDate)
    elif choice == "ลงทะเบียนเกษตรกร":
        st.subheader("ลงทะเบียนเกษตรกร")

    elif choice == "ลงทะเบียนพืช":
        st.subheader("ลงทะเบียนพืช")
        create_table()
        vetName = st.text_input("ชื่อ :", max_chars=50)
        vetDes = st.text_area("คำบรรยาย", height=250)
        # vet_pic = st.text_input("ระยะเวลาที่ใช้ในการปลูก")
        vetDate = datetime.datetime.now()
        # vetDate = time.strftime('%Y-%m-%d %H:%M:%S')
        if st.button("เพิ่มข้อมูล"):
            add_data(vetName, vetDes, vetDate)
            rowc = c.rowcount
            st.success("การลงทะเบียนพืช {} สำเร็จ! จำนวน {} แถว".format(vetName, rowc))

        # Display
        result = view_all_notes()
        clean_db = pd.DataFrame(result, columns=["รหัสพืช", "รายชื่อพืช", "คำบรรยายพืช", "เวลาที่ลงทะเบียน"])
        st.dataframe(clean_db)

if __name__ == '__main__':
    main()