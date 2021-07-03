import streamlit as st
import datetime
from io import BytesIO
from PIL import Image
import pandas as pd
import base64
from DB_CONNECT import condb
mydb = condb(1)
c = mydb.cursor()
timenow = datetime.datetime.now()
Date = timenow.strftime('%Y-%m-%d')
Time = timenow.strftime('%H:%M')
#function
@st.cache
def load_image(image_file):
    farmer_img = Image.open(image_file)
    fp = BytesIO()
    farmer_img.save(fp, "PNG")
    output = fp.getvalue()
    return output

def view_province():
    c.execute('SELECT provinceName FROM addrprovince;')
    data = c.fetchall()
    return data

def compare_pv(provincename):
    sql = "SELECT provinceid FROM addrprovince WHERE provinceName = %s;"
    var = [provincename]
    c.execute(sql,var)
    data = c.fetchone()
    return data

def compare_dt(districtname,provinceID):
    sql = "SELECT districtid FROM addrdistrict WHERE districtName = %s AND provinceid = %s;"
    dt = districtname
    pid = provinceID
    c.execute(sql, (dt, pid))
    data = c.fetchone()
    return data

def compare_sdt(subdistrictname,addrdistrictID,provinceID):
    sql = "SELECT subdistrictid FROM addrsubdistrict sd NATURAL JOIN addrdistrict dt " \
          "WHERE sd.subdistrictName = %s" \
          "AND dt.districtid = %s" \
          "AND dt.provinceid = %s;"
    sdt = subdistrictname
    dt = addrdistrictID
    p = provinceID
    c.execute(sql, (sdt,dt,p))
    data = c.fetchone()
    return data

def view_subdistrict(districtid):
    c.execute("SELECT DISTINCT subdistrictName FROM addrsubdistrict sd INNER JOIN addrdistrict d ON sd.districtID = d.districtID WHERE sd.districtID = %s;" ,districtid)
    data = c.fetchall()
    return data

def view_district(provinceID):
    c.execute("SELECT DISTINCT districtName FROM addrdistrict d INNER JOIN addrprovince p ON d.provinceID = p.provinceID WHERE d.provinceID = %s;" ,provinceID)
    data = c.fetchall()
    return data

def add_data(prename, firstname, lastname, farmeridTh, idTh, tel, addrNo, vilNo, vilName, addrsubdistrictID, farmer_date, farmer_img):
    sql = "INSERT INTO farmertable(prename, farmerfirstname, farmerlastname, farmeridTh, idth, farmertel, addrNo, addrvilNo, addrvil, subdistrictid, farmerdate, farmerimg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val = (prename, firstname, lastname, farmeridTh, idTh, tel, addrNo, vilNo, vilName, addrsubdistrictID, farmer_date, farmer_img)
    c.execute(sql, val)
    mydb.commit()

def view_all_farmerlists():
    c.execute("SELECT farmerid, prename, farmerfirstname, farmerlastname, farmeridTh, idth, addrNo,"
              "addrvilNo, addrvil, subdistrictname, districtname, provincename, postcode, farmertel "
              "FROM farmertable LEFT JOIN addrsubdistrict USING(subdistrictid)"
              "NATURAL JOIN addrdistrict "
              "NATURAL JOIN addrprovince;")
    data = c.fetchall()
    return data

def view_province_farmerlists(provinceID):
    c.execute("SELECT farmerid, prename, farmerfirstname, farmerlastname, farmeridTh, idth, addrNo,"
              "addrvilNo, addrvil, subdistrictname, districtname, provincename, postcode, farmertel "
              "FROM farmertable f LEFT JOIN addrsubdistrict sd USING(subdistrictid)"
              "NATURAL JOIN addrdistrict d "
              "NATURAL JOIN addrprovince p "
              "WHERE p.provinceid = %s;",provinceID)
    data = c.fetchall()
    return data

def view_district_farmerlists(addrdistrictID):
    c.execute("SELECT farmerid, prename, farmerfirstname, farmerlastname, farmeridTh, idth, addrNo,"
              "addrvilNo, addrvil, subdistrictname, districtname, provincename, postcode, farmertel "
              "FROM farmertable f LEFT JOIN addrsubdistrict sd USING(subdistrictid)"
              "NATURAL JOIN addrdistrict d "
              "NATURAL JOIN addrprovince p "
              "WHERE d.districtid = %s;", addrdistrictID)
    data = c.fetchall()
    return data

def view_subdistrict_farmerlists(addrsubdistrictID):
    c.execute("SELECT farmerid, prename, farmerfirstname, farmerlastname, farmeridTh, idth, addrNo,"
              "addrvilNo, addrvil, subdistrictname, districtname, provincename, postcode, farmertel "
              "FROM farmertable f LEFT JOIN addrsubdistrict sd USING(subdistrictid)"
              "NATURAL JOIN addrdistrict d "
              "NATURAL JOIN addrprovince p "
              "WHERE sd.subdistrictid = %s;", addrsubdistrictID)
    data = c.fetchall()
    return data

def view_edit_farmerlists():
    c.execute("SELECT CONCAT(farmerid,' ',prename,' ',farmerfirstname,' ',farmerlastname) AS memberrow "
              "FROM farmertable LEFT JOIN addrsubdistrict USING(subdistrictid) "
              "NATURAL JOIN addrdistrict "
              "NATURAL JOIN addrprovince;")
    data = c.fetchall()
    return data

def compare_farmerid(person_selected):
    sql = "SELECT farmerid FROM farmertable WHERE CONCAT(farmerid,' ',prename,' ',farmerfirstname,' ',farmerlastname) LIKE %s;"
    var = [person_selected]
    c.execute(sql, var)
    data = c.fetchone()
    return data

def edit_farmer(farmer_editid):
    c.execute("SELECT farmerid, prename, farmerfirstname, farmerlastname, farmeridTh, idth, addrNo,"
              "addrvilNo, addrvil, subdistrictname, districtname, provincename,farmerimg, farmertel, farmerdate "
              "FROM farmertable LEFT JOIN addrsubdistrict USING(subdistrictid)"
              "NATURAL JOIN addrdistrict "
              "NATURAL JOIN addrprovince "
              "WHERE farmerid = %s;", farmer_editid)
    data = c.fetchone()
    return data

def view_province_edit(provincename):
    c.execute('SELECT provinceName FROM addrprovince ORDER BY provinceName = %s DESC;', [provincename])
    data = c.fetchall()
    return data

def view_district_edit(provinceID,districtname):
    sql =  "SELECT districtName FROM addrdistrict d INNER JOIN addrprovince p ON d.provinceID = p.provinceID WHERE d.provinceID = %s ORDER BY districtName = %s DESC;"
    var = (provinceID,districtname)
    c.execute(sql,var)
    data = c.fetchall()
    return data

def view_subdistrict_edit(addrdistrictID,subdistrictname):
    sql ="SELECT subdistrictName FROM addrsubdistrict sd INNER JOIN addrdistrict d ON sd.districtID = d.districtID WHERE sd.districtID = %s ORDER BY subdistrictName = %s DESC;"
    var = (addrdistrictID,subdistrictname)
    c.execute(sql,var)
    data = c.fetchall()
    return data

def select_pil(params, outfile=None):
    sql_cmd = """
        SELECT farmerimg FROM farmertable WHERE farmerid = %s limit 1;
    """
    c.execute(sql_cmd, params)
    row = c.fetchone()
    if row:
        bytes_stream = BytesIO(row[0])
        img = Image.open(bytes_stream)
        return img
    return None

def update_data(prename, firstname, lastname, farmeridTh, idTh, tel, addrNo, vilNo, vilName, new_addrsubdistrictID, new_farmer_img, farmerid):
    sql = """UPDATE farmertable 
          SET prename = %s, farmerfirstname = %s, farmerlastname = %s, farmeridTh = %s, idth = %s, farmertel = %s, 
          addrNo = %s, addrvilNo = %s, addrvil = %s, subdistrictid = %s, farmerimg = %s 
          WHERE farmerid = %s;"""
    val = (prename, firstname, lastname, farmeridTh, idTh, tel, addrNo, vilNo, vilName, new_addrsubdistrictID, new_farmer_img, farmerid)
    c.execute(sql, val)
    mydb.commit()

def delete_data(farmerid):
    c.execute("DELETE FROM farmertable WHERE farmerid = %s",[farmerid])
    mydb.commit()

def convert_csv(data):
    csvfile = data.to_csv(index=False,header=True)
    b64 = base64.b64encode(csvfile.encode()).decode()
    filename_csv = "farmerlist_{}{}.csv".format(Date,Time)
    href_csv = f'<a href="data:file/csv;base64,{b64}" download="{filename_csv}"> ดาวน์โหลด CSV</a>'
    st.markdown(href_csv,unsafe_allow_html=True)

#main
def app():
    st.title("ลงทะเบียนเกษตรกร")
    # DISPLAY
    with st.beta_expander("ดูรายชื่อสมาชิกทั้งหมด"):
        #st.subheader("รายชื่อข้อมูลสมาชิก")
        farmerlist = view_all_farmerlists()
        checked_province = st.checkbox('ระบุจังหวัด')
        if checked_province:
            pv = view_province()
            provincelist = pd.DataFrame(pv, columns=["จังหวัด"])
            provincename = st.selectbox('จังหวัด', (provincelist))
            provinceID = compare_pv(provincename)
            farmerlist = view_province_farmerlists(provinceID)
            checked_district = st.checkbox('ระบุอำเภอ')
            if checked_district:
                dt = view_district(provinceID)
                districtlist = pd.DataFrame(dt, columns=["อำเภอ"])
                districtname = st.selectbox('อำเภอ', districtlist)
                addrdistrictID = compare_dt(districtname, provinceID)
                farmerlist = view_district_farmerlists(addrdistrictID)
                checked_subdistrict = st.checkbox('ระบุตำบล')
                if checked_subdistrict:
                    sdt = view_subdistrict(addrdistrictID)
                    subdistrictlist = pd.DataFrame(sdt, columns=["ตำบล"])
                    subdistrictname = st.selectbox('ตำบล', subdistrictlist)
                    addrsubdistrictID = compare_sdt(subdistrictname, addrdistrictID, provinceID)
                    farmerlist = view_subdistrict_farmerlists(addrsubdistrictID)
        farmerdata = pd.DataFrame(farmerlist, columns=["รหัสสมาชิก", "คำนำหน้า", "ชื่อ", "นามสกุล", "รหัสเกษตรกร",
                                                 "รหัสประจำตัวประชาชน", "บ้านเลขที่", "หมู่ที่", "ชื่อบ้าน", "ตำบล",
                                                 "อำเภอ", "จังหวัด", "รหัสไปรษณีย์", "เบอร์โทรศัพท์"])
        st.dataframe(farmerdata, height=200)
        convert_csv(farmerdata)

    # INPUT FORM
    with st.beta_expander("เพิ่มข้อมูลสมาชิก"):
        #st.subheader("เพิ่มข้อมูลสมาชิก")
        st.write('ณ วันที่ {} เวลา {}'.format(Date, Time))
        prenamec, firstnamec, lastnamec = st.beta_columns([1, 2, 2])
        with prenamec:
            options = ["นาย","นาง","นางสาว"]
            prename = st.selectbox("คำนำหน้า :",(options),key='prename')
        with firstnamec:
            firstname = st.text_input("ชื่อ :",max_chars=150,key='firstname')
        with lastnamec:
            lastname = st.text_input("นามสกุล :",max_chars=150,key='lastname')
        farmeridThc, idThc = st.beta_columns([1,2])
        with farmeridThc:
            farmeridTh = st.text_input("รหัสเกษตรกร :",max_chars=8,key='farmeridth')
        with idThc:
            idTh = st.text_input("รหัสประจำตัวประชาชน :",max_chars=13,key='idth')
        tel = st.text_input("เบอร์โทรศัพท์ :", max_chars=10,key='tel')
        addrNoc, vilNoc, vilNamec = st.beta_columns([1,1,3])
        with addrNoc:
            addrNo = st.text_input("บ้านเลขที่ :",key='addrno')
        with vilNoc:
            vilNo = st.text_input("หมู่ที่ :",key='vilno')
        with vilNamec:
            vilName = st.text_input("ชื่อบ้าน :",max_chars=150,key='vilname')
        pv = view_province()
        provincelist = pd.DataFrame(pv, columns=["จังหวัด"])
        provincename = st.selectbox("จังหวัด :", (provincelist),key='provincename')
        provinceID = compare_pv(provincename)
        dt = view_district(provinceID)
        districtlist = pd.DataFrame(dt, columns=["อำเภอ"])
        districtname = st.selectbox("อำเภอ :", districtlist,key='districtname')
        addrdistrictID = compare_dt(districtname,provinceID)
        sdt = view_subdistrict(addrdistrictID)
        subdistrictlist = pd.DataFrame(sdt, columns=["ตำบล"])
        subdistrictname = st.selectbox("ตำบล :", subdistrictlist,key='subdistrictname')
        addrsubdistrictID = compare_sdt(subdistrictname,addrdistrictID,provinceID)
        image_file = st.file_uploader("แนบไฟล์รูป :", type=['png', 'jpg', 'jpeg'],key='img_famer')
        farmer_date = timenow.strftime('%Y-%m-%d %H:%M:%S')
        col1, col2, col3, col4, col5 = st.beta_columns(5)
        with col3:
            submitted = st.button(label='เพิ่มข้อมูล')
        if image_file is not None:
            file_details = {"FileName": image_file.name, "FileType": image_file.type}
            st.write(file_details)
            farmer_img = load_image(image_file)
            st.image(farmer_img, use_column_width='250', output_format='PNG')
        else:
            farmer_img = load_image('none.png')
        if submitted:
            add_data(prename, firstname, lastname, farmeridTh, idTh, tel, addrNo, vilNo, vilName, addrsubdistrictID, farmer_date, farmer_img)
            st.success("การลงทะเบียนสมาชิก: {} {} {}สำเร็จ!".format(prename, firstname, lastname))

    # EDIT FORM
    with st.beta_expander("แก้ไชข้อมูลสมาชิก"):
        mb = view_edit_farmerlists()
        memberlist = pd.DataFrame(mb, columns=["ชื่อสมาชิก"])
        person_selected = st.selectbox("โปรดเลือกสมาชิก :",(memberlist))
        if person_selected is None:
            st.warning("กรุณาเพิ่มข้อมูลเกษตรกร")
        else:
            st.subheader("แก้ไชข้อมูลสมาชิก : {}".format(person_selected))
            #QUERY DATA
            farmer_editid = compare_farmerid(person_selected)
            thisfarmer = edit_farmer(farmer_editid)
            farmerid = thisfarmer[0]
            prename = thisfarmer[1]
            firstname = thisfarmer[2]
            lastname = thisfarmer[3]
            farmeridTh = thisfarmer[4]
            idTh = thisfarmer[5]
            addrNo = thisfarmer[6]
            vilNo = thisfarmer[7]
            vilName = thisfarmer[8]
            subdistrictname = thisfarmer[9]
            districtname = thisfarmer[10]
            provincename = thisfarmer[11]
            farmerimg = thisfarmer[12]
            tel = thisfarmer[13]
            farmerdate = thisfarmer[14]
            # LAYOUT
            a,img,b = st.beta_columns([1,1,1])
            with img:
                st.image(select_pil([farmerid]),person_selected)
            st.write("ลงทะเบียนเมื่อวันที : {} ".format(farmerdate))
            prenamec, firstnamec, lastnamec = st.beta_columns([1, 2, 2])
            with prenamec:
                mr = ["นาย"]
                miss = ["นางสาว"]
                mrs = ["นาง"]
                options = ["นาย","นาง","นางสาว"]
                if ([prename] == mr):
                    options = [prename,"นาง","นางสาว"]
                if ([prename] == mrs):
                    options = [prename,"นาย","นางสาว"]
                if ([prename] == miss):
                    options = [prename,"นาย","นาง"]
                new_prename = st.selectbox("คำนำหน้า :",(options))
            with firstnamec:
                new_firstname = st.text_input("ชื่อ :",firstname, max_chars=150)
            with lastnamec:
                new_lastname = st.text_input("นามสกุล :",lastname, max_chars=150)
            farmeridThc, idThc = st.beta_columns([1, 2])
            with farmeridThc:
                new_farmeridTh = st.text_input("รหัสเกษตรกร :",farmeridTh, max_chars=8)
            with idThc:
                new_idTh = st.text_input("รหัสประจำตัวประชาชน :",idTh, max_chars=13)
            new_tel = st.text_input("เบอร์โทรศัพท์ :",tel, max_chars=10)
            addrNoc, vilNoc, vilNamec = st.beta_columns([1, 1, 3])
            with addrNoc:
                new_addrNo = st.text_input("บ้านเลขที่ :",addrNo)
            with vilNoc:
                new_vilNo = st.text_input("หมู่ที่ :",vilNo)
            with vilNamec:
                new_vilName = st.text_input("ชื่อบ้าน :",vilName,max_chars=150)
            pv = view_province_edit(provincename)
            provincelist = pd.DataFrame(pv,columns=["จังหวัด"])
            new_provincename = st.selectbox("จังหวัด :", provincelist)
            provinceID = compare_pv(new_provincename)
            dt = view_district_edit(provinceID,districtname)
            districtlist = pd.DataFrame(dt, columns=["อำเภอ"])
            new_districtname = st.selectbox("อำเภอ :", districtlist)
            addrdistrictID = compare_dt(new_districtname, provinceID)
            sdt = view_subdistrict_edit(addrdistrictID,subdistrictname)
            subdistrictlist = pd.DataFrame(sdt, columns=["ตำบล"])
            new_subdistrictname = st.selectbox("ตำบล :", subdistrictlist)
            new_addrsubdistrictID = compare_sdt(new_subdistrictname, addrdistrictID, provinceID)
            image_file = st.file_uploader("แนบไฟล์รูป :", type=['png', 'jpg', 'jpeg'])
            col1, col2, col3, col4 = st.beta_columns([1,1,1,1])
            with col2:
                editsubmitted = st.button(label='แก้ไขข้อมูล')
            with col3:
                deletesubmitted = st.button(label='ลบข้อมูล')
            if image_file is not None:
                file_details = {"FileName": image_file.name, "FileType": image_file.type}
                st.write(file_details)
                new_farmer_img = load_image(image_file)
                st.image(new_farmer_img, use_column_width='auto', output_format='PNG')
            else:
                new_farmer_img = farmerimg
            if editsubmitted:
                update_data(new_prename, new_firstname, new_lastname, new_farmeridTh, new_idTh, new_tel, new_addrNo, new_vilNo, new_vilName, new_addrsubdistrictID, new_farmer_img,farmerid)
                st.success("แก้ไขทะเบียนสมาชิก {}: {} {} {}สำเร็จ!".format(farmerid, new_prename, new_firstname, new_lastname))
            if deletesubmitted:
                delete_data(farmerid)
                st.error("ลบข้อมูลสมาชิก {} : {} {} {}แล้ว!".format(farmerid, new_prename, new_firstname, new_lastname))

