import streamlit as st
import datetime
from io import BytesIO
from PIL import Image
import pandas as pd
from DB_CONNECT import condb
import base64
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

def add_data(farmsubdistrictID, farmerid, vilName, vilNo, quantityfarm, quantitybuilding, landprivileges, geox,
                     geoy, geoz, soilanalyze, wateranalyze, gapanalyze):
    sql = """INSERT INTO farmlocation(subdistrictID, farmerid, farmvil, farmvilno, quantityfarm, quantitybuilding, 
    landprivileges, geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    val = (farmsubdistrictID, farmerid, vilName, vilNo, quantityfarm, quantitybuilding, landprivileges, geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze)
    c.execute(sql, val)
    mydb.commit()

def view_all_farmlists():
    c.execute("""SELECT farmerid, prename, farmerfirstname, farmerlastname, farmid, farmvil, farmvilno, 
		subdistrictname, districtname, provincename, quantityfarm, quantitybuilding, 
		landprivileges, geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze 
        FROM farmlocation AS f LEFT JOIN farmertable USING(farmerid)
		LEFT JOIN addrsubdistrict AS sd ON f.subdistrictid = sd.subdistrictid
        NATURAL JOIN addrdistrict AS d 
        NATURAL JOIN addrprovince AS p;""")
    data = c.fetchall()
    return data

def view_province_farmlists(provinceID):
    c.execute("""SELECT farmerid, prename, farmerfirstname, farmerlastname, farmid, farmvil, farmvilno, 
		subdistrictname, districtname, provincename, quantityfarm, quantitybuilding, 
		landprivileges, geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze 
        FROM farmlocation AS f LEFT JOIN farmertable USING(farmerid)
		LEFT JOIN addrsubdistrict AS sd ON f.subdistrictid = sd.subdistrictid
        NATURAL JOIN addrdistrict AS d 
        NATURAL JOIN addrprovince AS p 
        WHERE p.provinceid = %s;""",provinceID)
    data = c.fetchall()
    return data

def view_district_farmlists(addrdistrictID):
    c.execute("""SELECT farmerid, prename, farmerfirstname, farmerlastname, farmid, farmvil, farmvilno, 
		subdistrictname, districtname, provincename, quantityfarm, quantitybuilding, 
		landprivileges, geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze 
        FROM farmlocation AS f LEFT JOIN farmertable USING(farmerid)
		LEFT JOIN addrsubdistrict AS sd ON f.subdistrictid = sd.subdistrictid
        NATURAL JOIN addrdistrict AS d 
        NATURAL JOIN addrprovince AS p 
        WHERE d.districtid = %s;""", addrdistrictID)
    data = c.fetchall()
    return data

def view_subdistrict_farmlists(addrsubdistrictID):
    c.execute("""SELECT farmerid, prename, farmerfirstname, farmerlastname, farmid, farmvil, farmvilno, 
		subdistrictname, districtname, provincename, quantityfarm, quantitybuilding, 
		landprivileges, geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze 
        FROM farmlocation AS f LEFT JOIN farmertable USING(farmerid)
		LEFT JOIN addrsubdistrict AS sd ON f.subdistrictid = sd.subdistrictid
        NATURAL JOIN addrdistrict AS d 
        NATURAL JOIN addrprovince AS p 
        WHERE sd.subdistrictid = %s;""", addrsubdistrictID)
    data = c.fetchall()
    return data

def view_farmerlists():
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

def edit_farm(farm_selected):
    #st.write([farm_selected]) Convert numpy.int64 to python int
    farm_selected = farm_selected.item()
    #st.write([farm_selected])
    c.execute("""SELECT farmid, farmvil, farmvilno, farmlocation.subdistrictid, quantityfarm, quantitybuilding, landprivileges, 
    geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze, farmerid 
    FROM addrsubdistrict RIGHT JOIN farmlocation USING(subdistrictid)
	LEFT JOIN farmertable USING(farmerid)
	WHERE farmid = %s;""",[farm_selected])
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

def update_data(farmid, farmvil, farmvilno, subdistrictid, quantityfarm, quantitybuilding, landprivileges,
                geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze):
    sql = """UPDATE farmlocation
          SET farmvil = %s, farmvilno = %s, subdistrictid = %s, quantityfarm = %s, quantitybuilding = %s, landprivileges = %s, 
          geox = %s, geoy = %s, geoz = %s, soilanalyze = %s, wateranalyze = %s, gapanalyze = %s
          WHERE farmid = %s;"""
    val = (farmvil, farmvilno, subdistrictid, quantityfarm, quantitybuilding, landprivileges,
                geox, geoy, geoz, soilanalyze, wateranalyze, gapanalyze,farmid)
    c.execute(sql, val)
    mydb.commit()

def delete_data(farmid):
    c.execute("DELETE FROM farmlocation WHERE farmid = %s",[farmid])
    mydb.commit()

def view_edit_farmlists(farm_farmer):
    c.execute("""SELECT farmid FROM farmlocation RIGHT JOIN farmertable USING(farmerid)
    WHERE farmerid = %s;""",farm_farmer)
    data = c.fetchall()
    return data

def convert_csv(data):
    csvfile = data.to_csv(index=False,header=True)
    b64 = base64.b64encode(csvfile.encode()).decode()
    filename_csv = "farmerlist_{}{}.csv".format(Date,Time)
    href_csv = f'<a href="data:file/csv;base64,{b64}" download="{filename_csv}"> ดาวน์โหลด CSV</a>'
    st.markdown(href_csv,unsafe_allow_html=True)

#main
def app():
    st.title("ลงทะเบียนพื้นที่เพาะปลูก")
    # DISPLAY
    with st.beta_expander("ดูที่อยู่แปลงทั้งหมด"):
        #st.subheader("รายชื่อข้อมูลสมาชิก")
        farmlist = view_all_farmlists()
        checked_province = st.checkbox('ระบุจังหวัด')
        if checked_province:
            pv = view_province()
            provincelist = pd.DataFrame(pv, columns=["จังหวัด"])
            provincename = st.selectbox('จังหวัด',(provincelist))
            provinceID = compare_pv(provincename)
            farmlist = view_province_farmlists(provinceID)
            checked_district = st.checkbox('ระบุอำเภอ')
            if checked_district:
                dt = view_district(provinceID)
                districtlist = pd.DataFrame(dt, columns=["อำเภอ"])
                districtname = st.selectbox('อำเภอ', districtlist)
                addrdistrictID = compare_dt(districtname, provinceID)
                farmlist = view_district_farmlists(addrdistrictID)
                checked_subdistrict = st.checkbox('ระบุตำบล')
                if checked_subdistrict:
                    sdt = view_subdistrict(addrdistrictID)
                    subdistrictlist = pd.DataFrame(sdt, columns=["ตำบล"])
                    subdistrictname = st.selectbox('ตำบล', subdistrictlist)
                    addrsubdistrictID = compare_sdt(subdistrictname, addrdistrictID, provinceID)
                    farmlist = view_subdistrict_farmlists(addrsubdistrictID)
        farmdata = pd.DataFrame(farmlist, columns=["รหัสสมาชิก", "คำนำหน้า", "ชื่อ", "นามสกุล", "รหัสแปลง",
                                                 "ชื่อบ้าน", "หมู่ที่", "ตำบล", "อำเภอ", "จังหวัด",
                                                 "พื้นที่ไร่", "จำนวนโรงเรือน", "เอกสารสิทธิการใช้ประโยชน์ที่ดิน", "พิกัดแปลง (X)",
                                                 "พิกัดแปลง (Y)", "ความสูง (Z)", "การตรวจวิเคราะห์ดิน", "การตรวจวิเคราะห์น้ำ", "การรับรองระบบ GAP"])
        st.dataframe(farmdata, height=200)
        convert_csv(farmdata)
    # INPUT FORM
    with st.beta_expander("เพิ่มข้อมูลที่อยู่แปลง"):
        mb = view_farmerlists()
        memberlist = pd.DataFrame(mb, columns=["ชื่อสมาชิก"])
        person_selected = st.selectbox("โปรดเลือกสมาชิก :", (memberlist))
        if person_selected is None:
            st.warning("กรุณาเพิ่มข้อมูลเกษตรกร")
        else:
            st.subheader("เพิ่มข้อมูลที่อยู่แปลงของ : {}".format(person_selected))
        #st.subheader("เพิ่มข้อมูลแปลง")
        farmerid = compare_farmerid(person_selected)
        st.write('ณ วันที่ {} เวลา {}'.format(Date, Time))
        #LAYOUT
        vilNoc, vilNamec = st.beta_columns([1,3])
        with vilNoc:
            vilNo = st.text_input("หมู่ที่ :", max_chars=2,key='vilno')
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
        farmsubdistrictID = compare_sdt(subdistrictname,addrdistrictID,provinceID)
        st.write("ขนาดพื้นที่")
        quantityfarmc, quantitybuildingc = st.beta_columns(2)
        with quantityfarmc:
            quantityfarm = st.number_input("จำนวนไร่ :",min_value=0,step=1,key='quantityfarm')
        with quantitybuildingc:
            quantitybuilding = st.number_input("จำนวนโรงเรือน :",min_value=0, step=1,key='quantitybuilding')
        landprivileges = st.text_input("เอกสารสิทธิการใช้ประโยชน์ที่ดิน :",key='landprivileges')
        st.write("พิกัดแปลง")
        geoxc, geoyc, geozc = st.beta_columns(3)
        with geoxc:
            geox = st.number_input("พิกัดแกน X :",min_value=0,step=1,key='geox')
        with geoyc:
            geoy = st.number_input("พิกัดแกน Y :", min_value=0, step=1,key='geoy')
        with geozc:
            geoz = st.number_input("พิกัดแกน Z (ความสูง) :", min_value=0, step=1,key='geoz')
        st.write("การตรวจวิเคราะห์")
        soil = st.radio("การตรวจวิเคราะห์ดิน :",options=('ได้ตรวจวิเคราะห์แล้ว','ยังไม่ได้ตรวจวิเคราะห์'),key='soil')
        if soil == 'ได้ตรวจวิเคราะห์แล้ว':
            soilanalyze = True
        else:
            soilanalyze = False
        water = st.radio("การตรวจวิเคราะห์น้ำ :", options=('ได้ตรวจวิเคราะห์แล้ว', 'ยังไม่ได้ตรวจวิเคราะห์'),key='water')
        if water == 'ได้ตรวจวิเคราะห์แล้ว':
            wateranalyze = True
        else:
            wateranalyze = False
        gap = st.radio("การรับรองระบบ GAP :", options=('ได้รับการรับรอง GAP', 'ยังไม่ได้รับการรับรอง GAP'),key='gap')
        if gap == 'ได้รับการรับรอง GAP':
            gapanalyze = True
        else:
            gapanalyze = False
        col1, col2, col3, col4, col5 = st.beta_columns(5)
        with col3:
            submitted = st.button(label='เพิ่มข้อมูล')
        if submitted:
            add_data(farmsubdistrictID, farmerid, vilName, vilNo, quantityfarm, quantitybuilding, landprivileges, geox,
                     geoy, geoz, soilanalyze, wateranalyze, gapanalyze)
            st.success("การลงทะเบียนที่อยู่แปลง: {} สำเร็จ!".format(person_selected))

    with st.beta_expander("แก้ไขข้อมูลที่อยู่แปลง"):
        fm = view_farmerlists()
        farmerchoice = pd.DataFrame(fm, columns=["ชื่อสมาชิก"])
        person_selected = st.selectbox("สมาชิก :", (farmerchoice))
        farm_farmer = compare_farmerid(person_selected) #one farmer has many farm
        if person_selected is None:
            st.warning("กรุณาเพิ่มข้อมูลเกษตรกร")
        else:
            mb = view_edit_farmlists(farm_farmer)
            farmlist = pd.DataFrame(mb, columns=["รหัสแปลง"])
            farm_selected = st.selectbox("รหัสแปลง :", (farmlist))
            if farm_selected is None:
                st.warning("กรุณาเพิ่มข้อมูลที่อยู่แปลง")
            else:
                # QUERY DATA
                thisfarm = edit_farm(farm_selected)
                st.dataframe(thisfarm)
                farmid = thisfarm[0]
                farmvil = thisfarm[1]
                farmvilno = thisfarm[2]
                subdistrictid = thisfarm[3]
                quantityfarm = thisfarm[4]
                quantitybuilding = thisfarm[5]
                landprivileges = thisfarm[6]
                geox = thisfarm[7]
                geoy = thisfarm[8]
                geoz = thisfarm[9]
                soilanalyze = thisfarm[10]
                wateranalyze = thisfarm[11]
                gapanalyze = thisfarm[12]
                farmerid = thisfarm[13]
                # LAYOUT
                st.subheader("แก้ไชข้อมูลสมาชิก : {} | รหัสแปลง : {}".format(person_selected,farm_selected))
                vilNoc, vilNamec = st.beta_columns([1, 3])
                with vilNoc:
                    new_vilNo = st.text_input("หมู่ที่ :",farmvilno, max_chars=2,key='vilnoedit')
                with vilNamec:
                    new_vilName = st.text_input("ชื่อบ้าน :",farmvil, max_chars=150, key='vilnameedit')
                pv = view_province_edit(provincename)
                provincelist = pd.DataFrame(pv, columns=["จังหวัด"])
                new_provincename = st.selectbox("จังหวัด :", (provincelist), key='provincenameedit')
                provinceID = compare_pv(provincename)
                dt = view_district_edit(provinceID,new_provincename)
                districtlist = pd.DataFrame(dt, columns=["อำเภอ"])
                new_districtname = st.selectbox("อำเภอ :", districtlist, key='districtnameedit')
                addrdistrictID = compare_dt(new_districtname, provinceID)
                sdt = view_subdistrict_edit(addrdistrictID,subdistrictname)
                subdistrictlist = pd.DataFrame(sdt, columns=["ตำบล"])
                new_subdistrictname = st.selectbox("ตำบล :", subdistrictlist, key='subdistrictnameedit')
                new_farmsubdistrictID = compare_sdt(new_subdistrictname, addrdistrictID, provinceID)
                st.write("ขนาดพื้นที่")
                quantityfarmc, quantitybuildingc = st.beta_columns(2)
                with quantityfarmc:
                    new_quantityfarm = st.number_input("จำนวนไร่ :",value=quantityfarm, min_value=0, step=1, key='quantityfarmedit')
                with quantitybuildingc:
                    new_quantitybuilding = st.number_input("จำนวนโรงเรือน :",value=quantitybuilding, min_value=0, step=1, key='quantitybuildingedit')
                new_landprivileges = st.text_input("เอกสารสิทธิการใช้ประโยชน์ที่ดิน :",landprivileges, key='landprivilegesedit')
                st.write("พิกัดแปลง")
                geoxc, geoyc, geozc = st.beta_columns(3)
                with geoxc:
                    new_geox = st.number_input("พิกัดแกน X :",value=geox, min_value=0, step=1, key='geoxedit')
                with geoyc:
                    new_geoy = st.number_input("พิกัดแกน Y :",value=geoy, min_value=0, step=1, key='geoyedit')
                with geozc:
                    new_geoz = st.number_input("พิกัดแกน Z (ความสูง) :",value=geoz, min_value=0, step=1, key='geozedit')
                st.write("การตรวจวิเคราะห์")
                if soilanalyze == True:
                    soilop = ('ได้ตรวจวิเคราะห์แล้ว','ยังไม่ได้ตรวจวิเคราะห์')
                else:
                    soilop = ('ยังไม่ได้ตรวจวิเคราะห์','ได้ตรวจวิเคราะห์แล้ว')
                soil = st.radio("การตรวจวิเคราะห์ดิน :",soilop, key='soiledit')
                if soil == 'ได้ตรวจวิเคราะห์แล้ว':
                    new_soilanalyze = True
                else:
                    new_soilanalyze = False
                if wateranalyze == True:
                    waterop = ('ได้ตรวจวิเคราะห์แล้ว','ยังไม่ได้ตรวจวิเคราะห์')
                else:
                    waterop = ('ยังไม่ได้ตรวจวิเคราะห์','ได้ตรวจวิเคราะห์แล้ว')
                water = st.radio("การตรวจวิเคราะห์น้ำ :", waterop, key='wateredit')
                if water == 'ได้ตรวจวิเคราะห์แล้ว':
                    new_wateranalyze = True
                else:
                    new_wateranalyze = False
                if gapanalyze == True:
                    gapop = ('ได้ตรวจวิเคราะห์แล้ว', 'ยังไม่ได้ตรวจวิเคราะห์')
                else:
                    gapop = ('ยังไม่ได้ตรวจวิเคราะห์', 'ได้ตรวจวิเคราะห์แล้ว')
                gap = st.radio("การรับรองระบบ GAP :",gapop, key='gapedit')
                if gap == 'ได้รับการรับรอง GAP':
                    new_gapanalyze = True
                else:
                    new_gapanalyze = False
                col1, col2, col3, col4 = st.beta_columns([1, 1, 1, 1])
                with col2:
                    editsubmitted = st.button(label='แก้ไขข้อมูล')
                with col3:
                    deletesubmitted = st.button(label='ลบข้อมูล')
                if editsubmitted:
                    update_data(farmid, new_vilName, new_vilNo, new_farmsubdistrictID, new_quantityfarm, new_quantitybuilding, new_landprivileges,
                                new_geox, new_geoy, new_geoz, new_soilanalyze, new_wateranalyze, new_gapanalyze)
                    st.success(
                        "แก้ไขที่อยู่รหัสแปลง : {} ของ {} สำเร็จ!".format(farmid, person_selected))
                if deletesubmitted:
                    delete_data(farmid)
                    st.error("ลบที่อยู่รหัสแปลง : {} ของ {} แล้ว!".format(farmid, person_selected))
