import streamlit as st
import pandas as pd
import gspread
import pytz 
from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh


# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hệ Thống Quan Trắc Codelcloud", layout="wide")
st_autorefresh(interval=30 * 1000, key="datarefresh")

# Chia làm 3 cột: Cột 1 (Logo trái), Cột 2 (Chữ trung tâm), Cột 3 (Hình bên phải)
# Tỉ lệ [1, 3, 1] giúp phần chữ ở giữa rộng nhất
col_left, col_center, col_right = st.columns([1, 3, 1])

with col_left:
    # Logo công ty bên trái
    st.image("image_cb2919.png", width=500)

with col_center:
    # Hàng chữ in đậm ở giữa
    st.markdown("""
        <div style="text-align: center; padding-top: 40px;">
            <h1 style="color: #003366; margin-bottom: 0; font-weight: bold;"> 
Giải Pháp Cho Nghành Môi Trường - 
<h1 style="color: #003366; margin-bottom: 0; font-weight: bold;"> An Toàn - Hiệu Quả - Tốc Độ - Chất Lượng - Tận Tâm</h1>
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # Tấm hình mới bạn muốn thêm vào bên góc phải
    # Đảm bảo file 'image_fe1d41.png' nằm cùng thư mục với file app.py
    try:
        st.image("image_fe1d41.png", width=500)
    except:
        st.write("Chưa tìm thấy file hình bên phải")

st.divider()

def get_data():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file("creds.json", scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open("QuanTracData_HeThongQuanTrac").sheet1
        
        values = sheet.get_all_values()
        if not values:
            return pd.DataFrame()
            
        # Lấy hàng đầu tiên làm tiêu đề và dữ liệu từ hàng thứ 2
        df = pd.DataFrame(values[1:], columns=values[0])
        
        # CHỈNH SỬA QUAN TRỌNG: Loại bỏ khoảng trắng thừa trong tên cột nếu có
        df.columns = df.columns.str.strip()
        
        # Loại bỏ các cột không có tên tiêu đề
        df = df.loc[:, df.columns != ''] 
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối dữ liệu: {e}")
        return pd.DataFrame()

st.markdown("""

    <style>
    /* Nền toàn trang xanh nhạt */
    .stApp {
        background-color: #CCFFFF;
    }

    /* Tiêu đề chính */
    h1 {
        color: #002D54 !important;
        font-weight: 850 !important;
    }

	.time-text {
        background-color: #FFFFFF;
        color: #002D54 !important;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 25px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
}

    /* Tag địa chỉ nổi bật */
    .location-tag {
        background-color: #FFFFFF;
        color: #002D54 !important;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 25px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
    }

    /* SỬA LỖI CHỮ TRẮNG/MỜ: ÉP MÀU XANH CHO CÁC TIÊU ĐỀ PHỤ */
    /* Chúng ta nhắm vào tất cả các cấp độ tiêu đề và div chứa subheader */
    [data-testid="stSubheader"] h3, 
    [data-testid="stMarkdownContainer"] h3,
    .stSubheader h3 {
        color: #002D54 !important;      /* Màu xanh Navy đậm */
        opacity: 1 !important;           /* Loại bỏ độ mờ của Streamlit */
        font-weight: 900 !important;     /* Độ đậm cực cao */
        font-size: 26px !important;
        text-transform: uppercase !important;
        border-left: 6px solid #0056B3 !important;
        padding-left: 15px !important;
        display: block !important;
    }
    /* Khung bao ngoài */
    [data-testid="stMetric"] {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2196f3;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* CHỈNH TÊN CHỈ TIÊU (SO2, CO, NO...) - Tăng mạnh mục tiêu */
    [data-testid="stMetricLabel"] > div {
        color: #3300FF !important;
        font-size: 25px !important; /* Chỉnh lại 40px để không bị vỡ khung */
        font-weight: 800 !important;
        line-height: 1.2 !important;
    }

    /* CHỈNH CON SỐ GIÁ TRỊ */
    [data-testid="stMetricValue"] > div {
        color: #3300FF  !important;
        font-size: 55px !important;
        font-weight: 800 !important;
    }
	st.write {
        color: #3300FF  !important;

    }

    /* CHỈNH ĐƠN VỊ (mg/Nm3, %) */
    [data-testid="stMetricValue"]  span {
        font-size: 25px !important;
    }

/* ĐOẠN CODE GIỮ NỀN TRẮNG TUYỆT ĐỐI CHO NHẬT KÝ */

    /* 1. Ép nền trắng cố định cho khung Nhật ký (Expander) ở mọi trạng thái */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D9E6 !important;
        border-radius: 12px !important;
    }

    /* 2. Loại bỏ hiệu ứng đổi màu khi di chuột vào (Hover) và khi click (Active) */
    div[data-testid="stExpander"]:hover, 
    div[data-testid="stExpander"]:active,
    div[data-testid="stExpander"]:focus-within {
        background-color: #FFFFFF !important;
        border: 1px solid #0056B3 !important; /* Viền xanh đậm hơn một chút khi tương tác */
    }

    /* 3. Đảm bảo phần tiêu đề chữ luôn hiển thị rõ trên nền trắng */
    div[data-testid="stExpander"] summary p {
        color: #003366 !important;
        font-weight: bold !important;
    }

    /* 4. Loại bỏ lớp phủ màu mặc định của Streamlit trên phần Summary */
    div[data-testid="stExpander"] summary {
        background-color: transparent !important;
    }
    
    div[data-testid="stExpander"] summary:hover {
        background-color: transparent !important;
    }
/* TẠO Ô CHỨA CHỈ TIÊU MÀU XANH DƯƠNG NỔI BẬT */
    div[data-testid="metric-container"] {
        background-color: #003366 !important; /* Nền xanh dương nổi bật */
        border: 1px solid #003366 !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0px 4px 15px rgba(0, 45, 84, 0.3) !important; /* Đổ bóng đậm hơn */
        transition: transform 0.2s ease-in-out;
    }

    /* Hiệu ứng phóng nhẹ khi đưa chuột vào ô chỉ tiêu */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0px 8px 20px rgba(0, 45, 84, 0.4) !important;
    }

    /* Đổi chữ của Con số dữ liệu sang màu TRẮNG để nổi trên nền xanh */
    [data-testid="stMetricValue"] {
        color: ##003366 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }

    /* Đổi chữ của Tên chỉ tiêu (Label) sang màu TRẮNG NHẠT */
    [data-testid="stMetricLabel"] {
        color: #003366 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("☁️ HỆ THỐNG QUAN TRẮC KHÍ THẢI - CODELCLOUD")
st.markdown('<div class="location-tag">📍 Khu Công nghiệp Gò Dầu, Long Thành, Đồng Nai</div>', unsafe_allow_html=True)

df = get_data()
if not df.empty:
    latest = df.iloc[-1] # Biến 'latest' được tạo ra tại đây

    # CHÈN DÒNG NÀY VÀO ĐÂY (Sau khi biến latest đã tồn tại)
    st.markdown(f"<div class='time-text'>🕒 Thời gian cập nhật: {latest.get('Timestamp', 'N/A')}</div>", unsafe_allow_html=True)

    
    # Ép kiểu dữ liệu thời gian và chuyển đổi múi giờ nếu cần
    update_time = latest.get('Timestamp', 'N/A')
    latest = df.iloc[-1]

    # --- KHỐI THÔNG SỐ CHÍNH ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Opacity", f"{latest.get('Opacity (%)', 0)} %")
    with m2:
        st.metric("Extinction", latest.get('Extinction', 0))
    with m3:
        # Khớp với 'Dust (mg/Nm3)' [cite: 19]
        st.metric("Bụi (Dust)", f"{latest.get('Dust (mg/Nm3)', 0)} mg/Nm3")
    with m4:
        # Khớp với 'Temp (C)' 
        st.metric("Nhiệt độ", f"{latest.get('Temp (C)', 0)} °C")

    st.divider()

    # --- KHỐI THÔNG SỐ KHÍ PHÁT THẢI (Sửa lỗi lấy nhầm giá trị) ---
    st.subheader("Thông số thành phần khí")
    c1, c2, c3, c4 = st.columns(4)
    c5, c6, c7, c8 = st.columns(4)

    with c1:
        # Khớp với 'S02 (mg/Nm3)' 
        st.metric("SO2", f"{latest.get('S02 (mg/Nm3)', 0)} mg/Nm3")
    with c2:
        # Khớp với 'C0 (mg/Nm3)' 
        st.metric("CO", f"{latest.get('C0 (mg/Nm3)', 0)} mg/Nm3")
    with c3:
        # Khớp với 'N0' (Cột cuối cùng trong file upload) [cite: 25]
        st.metric("NO", f"{latest.get('N0', 0)} mg/Nm3")
    with c4:
        # Khớp với 'N02 (mg/Nm3)' [cite: 22]
        st.metric("NO2", f"{latest.get('N02 (mg/Nm3)', 0)} mg/Nm3")
    
    with c5:
        # Khớp với 'N0X (mg/Nm3)' [cite: 22]
        st.metric("NOx (Tổng)", f"{latest.get('N0X (mg/Nm3)', 0)} mg/Nm3")
    with c6:
        # Khớp với 'HCl' [cite: 24]
        st.metric("HCl", f"{latest.get('HCl', 0)} mg/Nm3")
    with c7:
        # Khớp với 'O2 (%)' 
        st.metric("O2", f"{latest.get('O2 (%)', 0)} %")
    with c8:
        # Khớp với 'Flow (m3/h)' 
        st.metric("Lưu lượng", f"{latest.get('Flow (m3/h)', 0)} m3/h")

    with st.expander("Thông số kỹ thuật & Nhật ký"):
        st.markdown(f"""
            <p style='color: #002D54; font-size: 18px;'>
                <b style='color: #0056B3;'> Áp suất:</b> {latest.get('Pressure (kPa)', 0)} kPa | 
                <b style='color: #0056B3;'> Độ ẩm:</b> {latest.get('H2O (%)', 0)} %
            </p>
        """, unsafe_allow_html=True)
        st.dataframe(df.tail(10), use_container_width=True)
else:
    st.warning("Đang kết nối và chờ dữ liệu từ Google Sheets...")



import gspread
from google.oauth2.service_account import Credentials
import datetime
import time
import random

# --- 1. KẾT NỐI GOOGLE SHEETS ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("creds.json", scopes=scope)
client = gspread.authorize(creds)

try:
    sheet = client.open("QuanTracData_HeThongQuanTrac").sheet1
    print("🚀 Trình giả lập đang chạy. Dữ liệu sẽ thay đổi sau mỗi 30 giây...")
except Exception as e:
    print(f"❌ Lỗi kết nối Sheets: {e}")
    exit()

while True:
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # --- 2. TẠO GIÁ TRỊ NGẪU NHIÊN ---
        
        # Nhóm bụi và độ đục
        opacity = round(random.uniform(5.0, 15.0), 2)
        extinction = round(random.uniform(0.1, 0.8), 4)
        dust = round(random.uniform(100.0, 200.0), 1)
        
        # Nhóm khí phát thải (Dùng số 0 thay chữ O để khớp với App.py của bạn)
        s02 = round(random.uniform(25.0, 50.0), 2)
        c0 = round(random.uniform(2.0, 10.0), 2)
        c02 = round(random.uniform(10.0, 15.0), 2)
        
        # Thêm chỉ tiêu mới theo yêu cầu
        n0 = round(random.uniform(1.0, 9.0), 2)
        n02 = round(random.uniform(10.0, 30.0), 2)
        n0x = round(n0 + n02, 2)  # NOx = NO + NO2
        hcl = round(random.uniform(5.0, 15.0), 2)
        
        # Nhóm vật lý
        temp = round(random.uniform(90.0, 110.0), 1)
        flow = round(random.uniform(4500, 6000), 0)
        pressure = round(random.uniform(100, 105), 0)
        o2 = round(random.uniform(5.0, 8.0), 1)
        h2o = round(random.uniform(12.0, 15.0), 1)
        
        # Thông số kỹ thuật thiết bị
        dr1 = random.randint(10000, 10100)
        dt1 = random.randint(10050, 10150)
        dr2 = random.randint(9900, 10050)
        dt2 = random.randint(10000, 10100)

        # --- 3. ĐÓNG GÓI DỮ LIỆU ---
        # Danh sách này phải khớp 100% với số lượng và thứ tự cột trên Google Sheets
        row = [
            now,           # Cột A: Timestamp
            opacity,       # Cột B: Opacity (%)
            extinction,    # Cột C: Extinction
            dust,          # Cột D: Dust (mg/Nm3)
            temp,          # Cột E: Temp (C)
            flow,          # Cột F: Flow (m3/h)
            o2,            # Cột G: O2 (%)
            pressure,      # Cột H: Pressure (kPa)
            h2o,           # Cột I: H2O (%)
            s02,           # Cột J: S02 (mg/Nm3)
            c0,            # Cột K: C0 (mg/Nm3)
            c02,           # Cột L: C02 (mg/Nm3)
            n02,           # Cột M: N02 (mg/Nm3)
            n0x,           # Cột N: N0X (mg/Nm3)
            0,             # Cột O: Misalignment (%)
            0,             # Cột P: Delta Opacity (%)
            "Valid",       # Cột Q: Detector Valid
            "On",          # Cột R: Plant Status
            dr1,           # Cột S: DR1
            dt1,           # Cột T: DT1
            dr2,           # Cột U: DR2
            dt2,           # Cột V: DT2
            hcl,           # Cột W: HCl
            n0             # Cột X: N0
        ]
        
        # Gửi dữ liệu
        sheet.append_row(row)
        
        # In thông báo ra màn hình (Sửa lỗi f-string)
        print(f"✅ [{now}] Cập nhật: Dust={dust}, SO2={s02}, NO={n0}, NO2={n02}, NOx={n0x}, HCl={hcl}")
        
        # Đợi 30 giây
        time.sleep(30)
        
    except Exception as e:
        print(f"⚠️ Đang thử lại do lỗi: {e}")
        time.sleep(10)