import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ตรวจสอบคะแนนสอบกลางภาค DMC201", page_icon="📊", layout="centered")

# ปรับแต่งฟอนต์ TH Sarabun New และปรับขนาดตัวหนังสือให้เล็กลง เหมาะสำหรับการ Embed ใน Google Sites / Slides
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=TH+Sarabun+New&family=Sarabun:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], div, span, p, input, button {
        font-family: 'TH Sarabun New', 'Sarabun', sans-serif !important;
        font-size: 16px !important;
    }
    
    h1 {
        font-size: 24px !important;
        font-weight: 700 !important;
        margin-bottom: 0px !important;
    }
    
    h2, h3 {
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    .stAlert p {
        font-size: 15px !important;
        line-height: 1.4 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 22px !important;
        color: #1e3c72 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 ตรวจสอบคะแนนสอบกลางภาค (Midterm)")
st.subheader("รายวิชา DMC201 / DMR201 หลักการตลาด")

st.info("💡 กรอกรหัสนักศึกษาในช่องด้านล่าง เพื่อตรวจสอบคะแนนสอบกลางภาคส่วนบุคคล")

st.divider()

# Sheet ID สำหรับตารางคะแนนสอบ DMC201
GOOGLE_SHEET_ID = "1ffSH9pgmivD6Q0S_d_DGs-t6v63g1QjRVH0l9vLFv5Q"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        return pd.read_csv(SHEET_URL, dtype=str)
    except Exception as e:
        return None

df = load_data()

student_id = st.text_input("🔑 กรุณากรอกรหัสนักศึกษาของคุณ:", placeholder="เช่น 6704166")

if student_id:
    if df is not None and not df.empty:
        search_id = str(student_id).strip()
        
        # คอลัมน์ A (Index 0) คือ รหัสนักศึกษา
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.strip()
        
        student_row = df[df.iloc[:, 0] == search_id]
        
        if not student_row.empty:
            row_data = student_row.iloc[0]
            
            # ดึงข้อมูลจากตารางคะแนน (คอลัมน์ A-D)
            student_name = str(row_data.iloc[1]).strip() if pd.notna(row_data.iloc[1]) else "-" # B: ชื่อ - นามสกุล
            sec = str(row_data.iloc[2]).strip() if pd.notna(row_data.iloc[2]) else "-"          # C: SEC.
            score = str(row_data.iloc[3]).strip() if pd.notna(row_data.iloc[3]) else "-"        # D: คะแนนสอบ Midterm
            
            st.success(f"🔓 **ข้อมูลนักศึกษา:** {student_name}")
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="📌 กลุ่มเรียน (SEC)", value=f"{sec}")
            with col2:
                st.metric(label="💯 คะแนนสอบกลางภาค", value=f"{score} คะแนน")
            
        else:
            st.error(f"❌ ไม่พบรหัสนักศึกษา '{search_id}' ในระบบประกาศคะแนนสอบ")
    else:
        st.error("⚠️ ไม่สามารถเชื่อมต่อฐานข้อมูลได้ กรุณาตรวจสอบการตั้งค่าแชร์ไฟล์ Google Sheet ให้เป็น 'ทุกคนที่มีลิงก์'")
else:
    st.caption("ℹ️ ป้อนรหัสนักศึกษาของคุณในช่องด้านบน เพื่อค้นหาคะแนนสอบ")
