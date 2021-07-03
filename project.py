#Create Database
from DB_CONNECT import condb
#from ddl_db import create_table

#cdb = True
#ctb = True
#while cdb&ctb==True:
#    cdb = createdb()
#    ctb = create_table()


#Multiapp
from multiapp import MultiApp
from apps import home,vet_form,farmer_form,farm_form

app = MultiApp()
app.add_app("หน้าแรก",home.app)
app.add_app("ลงทะเบียนพืช", vet_form.app)
app.add_app("ลงทะเบียนเกษตรกร", farmer_form.app)
app.add_app("ลงทะเบียนพื้นที่เพาะปลูก",farm_form.app)

app.run()
condb()
