import streamlit as st
import pandas as pd
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Excel Viewer App", layout="wide")

st.title("ตรวจรางวัล")
st.write("เลือกไฟล์ที่ต้องการแสดงผลจากแถบด้านซ้าย")

# 1. รายชื่อไฟล์ที่คุณมี (สามารถเพิ่มชื่อไฟล์จริงเข้าไปได้เลย)
file_list = [
    "69.xlsx", "rt.xlsx"
]

# 2. สร้าง Sidebar สำหรับเลือกไฟล์
with st.sidebar:
    st.header("เมนูควบคุม")
    selected_file = st.selectbox("เลือกไฟล์ที่ต้องการดู:", file_list)
    
    st.divider()
    st.info("คำแนะนำ: ไฟล์เหล่านี้ต้องเก็บไว้ในโฟลเดอร์เดียวกับโค้ด Python")

# 3. ฟังก์ชันโหลดข้อมูล
@st.cache_data # ช่วยให้โหลดเร็วขึ้นถ้าเลือกไฟล์เดิมซ้ำ
def load_data(file_path):
    try:
        # ลองอ่านแบบ CSV (เนื่องจากไฟล์ที่อัปโหลดมาถูกแปลงเป็น CSV)
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ได้: {e}")
        return None

# 4. แสดงผลข้อมูล
if selected_file:
    st.subheader(f"📂 กำลังแสดงไฟล์: {selected_file}")
    
    data = load_data(selected_file)
    
    if data is not None:
        # ส่วนของการค้นหาข้อมูลในตาราง
        search_term = st.text_input("🔍 ค้นหาข้อมูลในตาราง:", "")
        
        if search_term:
            # กรองข้อมูลเบื้องต้น
            mask = data.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            filtered_data = data[mask]
        else:
            filtered_data = data

        # แสดงตารางแบบ Interactive
        st.dataframe(filtered_data, use_container_width=True)
        
        # แสดงสถิติเบื้องต้น
        st.write(f"จำนวนแถวทั้งหมด: {len(filtered_data)} แถว")
