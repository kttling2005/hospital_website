import streamlit as st
from streamlit_navigation_bar import st_navbar
from datetime import date

#ẩn thanh bar mặc định của
st.markdown(
    """
    <style>
    /* Ẩn thanh menu mặc định Streamlit (Deploy, Settings, ... ) */
    header {visibility: hidden;}
    /* Ẩn footer "Made with Streamlit" */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
#icon của google
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

#page config
st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

# xử lý trang
page = st.query_params.get("page", "home")

if page == "login":
    st.switch_page("pages/1_login.py")
elif page == "register":
    st.switch_page("pages/2_register.py")
elif page =="home":
#HTML
    st.markdown("""
    <html>
    <body>
    <div class="navbar">
        <div class="navbar-left">
            <span class="material-icons" style="vertical-align: middle;">help_outline</span>
            <span style="font-size:22px; vertical-align: middle;">Hướng dẫn</span>
        </div>
        <div>
            <a href="?page=login" target="_self">Đăng nhập</a>
            <a href="?page=register" target="_self">Đăng ký</a>
        </div>
    </div>
    
    <div class="logo-section">
        <div>
            <div class="logo-text">BrightEyes</div>
            <div class="logo-sub">Phòng khám mắt tiêu chuẩn quốc gia</div>
        </div>
        <div class="address"><span class="material-icons" style="vertical-align: middle;">location_on</span>
        Số 1, đường Lê Lợi, phường Minh Khai, thành phố Huế</div>
    </div>
    
    <div class="hospital-image">
        <img src="https://benhvienmat.vn/upload_images/images/old/2023/05/NTL_6039-1024x683.jpg" alt="hospital_image">
    </div>
    
    <div class="description">
        Phòng khám Mắt BrightEyes được thành lập với sứ mệnh mang đến cho cộng đồng một địa chỉ chăm sóc và bảo vệ đôi mắt đáng tin cậy. Trong hành trình hoạt động của mình, BrightEyes luôn hướng đến mục tiêu giúp mọi người nhìn thấy thế giới rõ ràng hơn – không chỉ bằng đôi mắt sáng khỏe, mà còn bằng niềm tin và sự an tâm trong từng lần thăm khám.
    
    Tại BrightEyes, chúng tôi hiểu rằng mỗi đôi mắt đều mang một câu chuyện riêng. Vì vậy, mọi quy trình khám và điều trị đều được thực hiện cẩn trọng, tận tâm và phù hợp với nhu cầu của từng người bệnh. Phòng khám được trang bị hệ thống máy móc, thiết bị nhãn khoa hiện đại đạt chuẩn quốc tế, phục vụ cho việc chẩn đoán và điều trị chính xác các tật khúc xạ, bệnh lý giác mạc, võng mạc, tăng nhãn áp, khô mắt cùng nhiều vấn đề thị giác khác.
    
    Đội ngũ bác sĩ và chuyên viên nhãn khoa tại BrightEyes đều có nhiều năm kinh nghiệm trong lĩnh vực mắt, từng công tác tại các bệnh viện lớn và được đào tạo chuyên sâu trong và ngoài nước. Họ không chỉ giỏi chuyên môn mà còn luôn đặt y đức lên hàng đầu, lấy sự hài lòng và sức khỏe của người bệnh làm trọng tâm trong mọi hoạt động.
    
    Bên cạnh công tác khám và điều trị, BrightEyes còn chú trọng vào việc tư vấn chăm sóc và bảo vệ mắt chủ động, giúp khách hàng hiểu rõ hơn về tầm quan trọng của việc kiểm tra thị lực định kỳ, cũng như cách duy trì thói quen sinh hoạt lành mạnh cho đôi mắt. Không gian phòng khám được thiết kế hiện đại, thân thiện và thoải mái, tạo cảm giác gần gũi cho mọi lứa tuổi – từ trẻ em, người đi học, đến người cao tuổi.
    
    Với triết lý hoạt động “Giữ gìn ánh sáng cho đôi mắt bạn”, BrightEyes không ngừng nỗ lực hoàn thiện chất lượng dịch vụ, đầu tư công nghệ mới và đào tạo đội ngũ y bác sĩ chuyên sâu hơn mỗi ngày. Chúng tôi tin rằng sự tận tâm và chuyên nghiệp sẽ là nền tảng giúp phòng khám trở thành nơi gửi gắm niềm tin của mọi khách hàng khi nghĩ đến sức khỏe thị giác.
    
    Phòng khám Mắt BrightEyes – nơi ánh sáng được chăm sóc bằng cả trái tim.
    </div>
    </body>
    </html>
    """, unsafe_allow_html=True
    )
    #CUSTOM CSS
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
    
    .logo-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        background: white;
        padding: 40px 40px 35px 40px;
    }
    
    .logo-text {
        color: #006699;
        font-weight: 800;
        font-size: 55px;
    }
    
    .logo-sub {
        font-size: 16px;
        color: #333;
    }
    
    /* Địa chỉ */
    .address {
        font-size: 18px;
        color: black;
    }
    
    /* Ảnh bệnh viện */
    .hospital-image {
        background-color: #e0e0e0;
        height: 390px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #888;
        font-size: 28px;
        font-weight: 600;
    }
    
    .hospital-image img{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Phần mô tả */
    .description {
        padding: 30px 40px;
        font-size: 18px;
        line-height: 1.6;
        text-align: justify;
    }
    
    /* Loại bỏ toàn bộ padding/margin mặc định của Streamlit */
    html, body, [data-testid="stAppViewContainer"], .main, .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Đảm bảo chiếm toàn màn hình */
    .stApp {
        height: 100vh;
        width: 100vw;
        overflow-x: hidden;
        overflow-y: auto;
    }
    
    </style>
    """
    ,unsafe_allow_html=True)