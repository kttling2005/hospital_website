import streamlit as st
from datetime import datetime

# -----------------------------
# Cấu hình
# -----------------------------
st.set_page_config(page_title="Thành tựu 10 năm - Bệnh viện Mắt Ánh Sáng", layout="wide")

# -----------------------------
# Phục hồi cookies nếu session_state mất
# -----------------------------
if "cookies" not in st.session_state:
    if "session" in st.query_params:
        st.session_state["cookies"] = {"session": st.query_params["session"]}
    else:
        st.session_state["cookies"] = None

if not st.session_state["cookies"]:
    st.warning("⚠️ Bạn cần đăng nhập trước.")
    st.switch_page("pages/1_login.py")
    st.stop()

# -----------------------------
#  Dữ liệu người dùng
# -----------------------------
user = st.session_state.get("user", {})
username = user.get("username", "Bệnh nhân")

# Ẩn thanh bar mặc định của Streamlit
st.markdown(
    """
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Icon của Google
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)


session_token = st.session_state["cookies"].get("session", "")
# -------------------------------
# XỬ LÝ ĐIỀU HƯỚNG
# -------------------------------
page = st.query_params.get("page", "brighteyes_10years")

if page == "patient_appointment":
    st.switch_page("pages/6_patient_appointment.py")

if page == "patienthome":
    st.switch_page("pages/3_patienthome.py")
elif page=="brighteyes_10years":
    # HTML
    st.markdown(f"""
           <html>
           <body>
           <div class="navbar">
               <div class="navbar-left">
                   <span class="material-icons" style="vertical-align: middle;">help_outline</span>
                   <span style="font-size:22px; vertical-align: middle;">Hướng dẫn</span>
               </div>
               <div class="navbar-right">
                   <a href="?page=patienthome&session={session_token}" target="_self">Trang chủ</a>
                   <a href="?page=patient_appointment&session={session_token}" target="_self">Lịch khám</a>
                   <!-- Profile -->
                   <div class="profile-dropdown">
                       <div class="profile-avatar">
                           <img src="https://i.pinimg.com/1200x/ea/96/48/ea96485daff64bc586ffcc6db5a09490.jpg" alt="avatar">
                       </div>
                       <span class="material-icons chevron">expand_more</span>
                       <span style="font-size:18px;">{username}</span>
                   </div>
                   <a href="?logout=1" class="navbar-logout" target="_self">Đăng xuất</a>  
               </div>
           </div>
           </body>
           </html>
    """, unsafe_allow_html=True)

    # -------------------------------
    # CSS TÙY CHỈNH
    # -------------------------------
    st.markdown("""
           <style>
           .stApp {
               font-family: 'Arial', sans-serif;
               background-color: white;
               color: black;
               font-size: 32px;
           }

           .navbar {
               display: flex;
               justify-content: space-between;
               align-items: center;
               background-color: #0078C2;
               color: white;
               padding: 10px 30px;
               font-weight: bold;
               position: fixed;
               top: 0;
               left: 0;
               width:100%;
               z-index:999;
           }
           .navbar a {
               color: white;
               text-decoration: none;
               margin-left: 25px;
           }

           .navbar-left {
               display: flex;
               align-items: center;
               gap: 10px;
           }

           .navbar-right {
               display: flex;
               align-items: center;
               gap: 20px;
           }

           .profile-dropdown {
               display: flex;
               align-items: center;
               gap: 8px;
               cursor: pointer;
           }

           .profile-avatar {
               width: 40px;
               height: 40px;
               border: 2px solid white;
               border-radius: 50%;
               overflow: hidden;
           }

           .profile-avatar img {
               width: 100%;
               height: 100%;
               object-fit: cover;
               border-radius: 50%;
           }

           .chevron {
               font-size: 24px;
               color: white;
           }

    """, unsafe_allow_html=True)
    # -----------------------------
    # CSS style
    # -----------------------------
    st.markdown("""
    <style>
    body {
        background-color: #f8fafc;
    }
    .big-title {
        font-size: 36px;
        font-weight: 800;
        color: #004d99;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 40px;
    }
    .card {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
    }
    .metric-number {
        font-size: 32px;
        font-weight: 700;
        color: #0078d4;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    .year-highlight {
        color: #0078d4;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Tiêu đề
    # -----------------------------
    st.markdown("<div class='big-title'>HÀNH TRÌNH 10 NĂM - BỆNH VIỆN MẮT ÁNH SÁNG</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-title'>Từ năm 2015 đến {datetime.now().year}</div>", unsafe_allow_html=True)
    st.write("---")

    # -----------------------------
    # Thống kê
    # -----------------------------
    st.subheader("Thành tựu nổi bật sau 10 năm hoạt động")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-number'>1.000+</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Ca phẫu thuật mắt thành công</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-number'>98.7%</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Tỷ lệ hài lòng của bệnh nhân</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-number'>25+</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Giải thưởng y khoa trong & ngoài nước</div>", unsafe_allow_html=True)

    st.write("")

    # -----------------------------
    # Cột mốc thành tựu
    # -----------------------------
    st.subheader("Những cột mốc đáng nhớ")

    milestones = [
        ("2015", "Thành lập Bệnh viện Mắt Ánh Sáng với đội ngũ 20 bác sĩ và 5 phòng mổ hiện đại."),
        ("2017", "Thực hiện ca ghép giác mạc đầu tiên, mang lại ánh sáng cho bệnh nhân mù bẩm sinh."),
        ("2019", "Ứng dụng công nghệ laser ReLEx SMILE điều trị tật khúc xạ thế hệ mới."),
        ("2020", "Đạt chứng nhận ISO 9001:2015 về quản lý chất lượng y tế."),
        ("2022", "Hoàn thành 100.000 ca phẫu thuật đục thủy tinh thể an toàn và thành công."),
        ("2023", "Thành lập Trung tâm Nghiên cứu & Đào tạo Nhãn khoa tiên tiến."),
        ("2025", "Kỷ niệm 10 năm phát triển cùng mạng lưới 15 chi nhánh trên toàn quốc."),
    ]

    for year, desc in milestones:
        st.markdown(f"""
        <div class='card'>
            <b class='year-highlight'>{year}</b> – {desc}
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # Hình ảnh miễn phí bản quyền
    # -----------------------------
    st.write("---")
    st.subheader("Khoảnh khắc & hành trình phục hồi ánh sáng")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="text-align:center;">
            <img src="https://cdn.nhathuoclongchau.com.vn/unsafe/800x0/https://cms-prod.s3-sgn09.fptcloud.com/co_the_mo_mat_can_duoc_may_lan_6c8bfeb88d.jpeg"
                 alt="Ca phẫu thuật mắt bằng laser hiện đại"
                 style="width:100%; height:180px; object-fit:cover; border-radius:10px;"/>
            <p style="font-size:14px; color:gray;">Ca phẫu thuật mắt bằng laser hiện đại</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
                <div style="text-align:center;">
                    <img src="https://i.pinimg.com/736x/38/22/e8/3822e81ed832564d090d280d3d2535d8.jpg"
                         alt="Đội ngũ bác sĩ nhãn khoa tận tâm"
                         style="width:100%; height:180px; object-fit:cover; border-radius:10px;"/>
                    <p style="font-size:14px; color:gray;">Đội ngũ bác sĩ nhãn khoa tận tâm</p>
                </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style="text-align:center;">
                <img src="https://file.qdnd.vn/data/images/0/2021/02/26/vuongthuy/10022021vthuy146.jpg?dpi=150&quality=100&w=575"
                    alt="Bệnh nhân hạnh phúc sau khi hồi phục thị lực"
                    style="width:100%; height:180px; object-fit:cover; border-radius:10px;"/>
                <p style="font-size:14px; color:gray;">Bệnh nhân hạnh phúc sau khi hồi phục thị lực</p>
            </div>
        """, unsafe_allow_html=True)

    st.info("*“Tôi đã nhìn thấy thế giới rõ ràng hơn sau ca phẫu thuật tại Bệnh viện BrightEyes — cảm ơn vì đã trao lại ánh sáng cho tôi.”* — Bệnh nhân Nguyễn Thị Hạnh, 58 tuổi.")

    # -----------------------------
    # Kêu gọi hành động
    # -----------------------------
    st.write("---")
    st.markdown("### Tiếp bước hành trình vì đôi mắt sáng khỏe cho cộng đồng")
    st.markdown(""" 
     **Hotline:** 1900 1234  
     **Địa chỉ:** 123 Đường Ánh Dương, Quận Bình Minh, TP. Hồ Chí Minh
    """)

    st.caption("© 2025 Bệnh viện BrightEyes – Tận tâm vì đôi mắt Việt. | website developed by team19")
