def main():
    st.title("ระบบจัดการฐานข้อมูลการวางแผนผลผลิต")

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

if __name__ == '__main__':
    main()