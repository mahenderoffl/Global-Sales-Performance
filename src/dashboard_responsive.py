import streamlit as st
from data_processor import SalesDataProcessor, create_sample_data
from visualizations import SalesVisualizer
import os

def detect_device_type():
    """Automatically detect device type based on actual screen width using JavaScript."""
    # JavaScript to detect screen width and set device type
    screen_detection_js = """
    <script>
    function detectDevice() {
        const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        let deviceType = 'desktop';
        
        if (width <= 768) {
            deviceType = 'mobile';
        } else if (width <= 1024) {
            deviceType = 'tablet';
        } else {
            deviceType = 'desktop';
        }
        
        // Send device type to Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: deviceType
        }, '*');
        
        // Also store in localStorage for persistence
        localStorage.setItem('deviceType', deviceType);
        
        return deviceType;
    }
    
    // Detect on load and resize
    window.addEventListener('load', detectDevice);
    window.addEventListener('resize', detectDevice);
    
    // Initial detection
    detectDevice();
    </script>
    """
    
    # Inject JavaScript into the page
    st.markdown(screen_detection_js, unsafe_allow_html=True)
    
    # Try to get device type from localStorage or use screen width detection
    detection_component = """
    <script>
    function getDeviceType() {
        const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        
        if (width <= 768) {
            return 'mobile';
        } else if (width <= 1024) {
            return 'tablet';
        } else {
            return 'desktop';
        }
    }
    
    // Set the device type immediately
    const deviceType = getDeviceType();
    localStorage.setItem('currentDeviceType', deviceType);
    
    // Create a hidden element with the device type
    const deviceElement = document.createElement('div');
    deviceElement.id = 'device-type-detector';
    deviceElement.style.display = 'none';
    deviceElement.setAttribute('data-device', deviceType);
    document.body.appendChild(deviceElement);
    </script>
    """
    
    st.markdown(detection_component, unsafe_allow_html=True)
    
    # Auto-detect based on user agent and screen size heuristics
    # This is a fallback method since Streamlit runs server-side
    if 'auto_detected_device' not in st.session_state:
        # Default detection logic
        st.session_state.auto_detected_device = 'desktop'
    
    return st.session_state.auto_detected_device

def update_device_detection():
    """Update device detection based on screen characteristics."""
    # CSS and JavaScript for real-time device detection with stunning visual design
    device_detection_css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root Variables for Theme */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --dark-gradient: linear-gradient(135deg, #232526 0%, #414345 100%);
        --light-gradient: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        --glass-bg: rgba(255, 255, 255, 0.15);
        --glass-border: rgba(255, 255, 255, 0.2);
        --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-xl: 0 35px 60px -12px rgba(0, 0, 0, 0.3);
    }
    
    /* Global Styling */
    .stApp {
        background: #ffffff;
        font-family: 'Inter', sans-serif;
        color: #2d3748;
    }
    
    /* Main content area with enhanced styling */
    .main .block-container {
        background: rgba(255, 255, 255, 1.0);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        padding: 2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        color: #2d3748;
    }
    
    /* Sidebar styling with gradient */
    .css-1d391kg {
        background: var(--dark-gradient);
        border-radius: 0 20px 20px 0;
        border-right: 1px solid var(--glass-border);
        color: #ffffff;
    }
    
    /* Sidebar text styling */
    .css-1d391kg .stMarkdown {
        color: #ffffff;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #ffffff !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .css-1d391kg .stRadio label {
        color: #ffffff !important;
    }
    
    .css-1d391kg .stSelectbox label {
        color: #ffffff !important;
    }
    
    .css-1d391kg p {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Device detection CSS classes */
    .device-mobile { display: none; }
    .device-tablet { display: none; }
    .device-desktop { display: none; }
    
    /* Responsive breakpoints */
    @media (max-width: 768px) {
        .device-mobile { display: block !important; }
        .device-tablet { display: none !important; }
        .device-desktop { display: none !important; }
        body { --device-type: 'mobile'; }
        
        .main .block-container {
            padding: 1rem;
            border-radius: 15px;
            margin: 0.5rem;
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        .device-mobile { display: none !important; }
        .device-tablet { display: block !important; }
        .device-desktop { display: none !important; }
        body { --device-type: 'tablet'; }
    }
    
    @media (min-width: 1025px) {
        .device-mobile { display: none !important; }
        .device-tablet { display: none !important; }
        .device-desktop { display: block !important; }
        body { --device-type: 'desktop'; }
    }
    
    /* Header styling with gradient text */
    h1, h2, h3, h4, h5, h6 {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    
    /* Improve text visibility in main content */
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4 {
        color: #2d3748 !important;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main .block-container p {
        color: #4a5568 !important;
    }
    
    .main .block-container .stMarkdown {
        color: #2d3748;
    }
    
    /* Expander text styling */
    .streamlit-expanderHeader p {
        color: #2d3748 !important;
        font-weight: 500;
    }
    
    /* Metric cards with gradient borders */
    .metric-container {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid var(--glass-border);
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-xl);
        border: 1px solid rgba(102, 126, 234, 0.4);
    }
    
    /* Button styling with gradients */
    .stButton > button {
        background: var(--primary-gradient);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        background: var(--secondary-gradient);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.01);
    }
    
    /* File uploader styling with gradient hover effects */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stFileUploader"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    [data-testid="stFileUploader"]:hover::before {
        left: 100%;
    }
    
    [data-testid="stFileUploader"] label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover label {
        color: #667eea !important;
    }
    
    /* File uploader button styling */
    [data-testid="stFileUploader"] button {
        background: var(--primary-gradient) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="stFileUploader"] button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: var(--secondary-gradient) !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    [data-testid="stFileUploader"] button:hover::before {
        left: 100%;
    }
    
    /* Download button styling (if any exist) */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="stDownloadButton"] button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(135deg, #56f68a 0%, #4bffeb 100%) !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 30px rgba(67, 233, 123, 0.4) !important;
    }
    
    [data-testid="stDownloadButton"] button:hover::before {
        left: 100%;
    }
    
    /* Form submit button styling */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="stFormSubmitButton"] button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    [data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #fc7bb3 0%, #ffed59 100%) !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 15px 35px rgba(250, 112, 154, 0.4) !important;
    }
    
    [data-testid="stFormSubmitButton"] button:hover::before {
        left: 100%;
    }
    
    /* Checkbox styling with gradient hover */
    .stCheckbox {
        transition: all 0.3s ease;
    }
    
    .stCheckbox:hover {
        transform: translateY(-1px);
    }
    
    .stCheckbox label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stCheckbox:hover label {
        color: #667eea !important;
    }
    
    .stCheckbox input[type="checkbox"] {
        accent-color: #667eea;
        transition: all 0.3s ease;
    }
    
    .stCheckbox input[type="checkbox"]:hover {
        transform: scale(1.1);
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Slider styling with gradient effects */
    .stSlider {
        transition: all 0.3s ease;
    }
    
    .stSlider:hover {
        transform: translateY(-1px);
    }
    
    .stSlider label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stSlider:hover label {
        color: #667eea !important;
    }
    
    .stSlider [role="slider"] {
        background: var(--primary-gradient) !important;
        transition: all 0.3s ease;
    }
    
    .stSlider:hover [role="slider"] {
        background: var(--secondary-gradient) !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4);
        transform: scale(1.1);
    }
    
    /* Toggle switch styling */
    .stToggle {
        transition: all 0.3s ease;
    }
    
    .stToggle:hover {
        transform: translateY(-1px);
    }
    
    .stToggle label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stToggle:hover label {
        color: #667eea !important;
    }
    
    /* Selectbox and input styling */
    .stSelectbox > div > div {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid var(--glass-border);
        color: #2d3748;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    .stSelectbox label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stSelectbox:hover label {
        color: #667eea !important;
    }
    
    .stTextArea > div > div > textarea {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid var(--glass-border);
        color: #2d3748;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:hover {
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    .stTextArea > div > div > textarea:focus {
        border: 1px solid rgba(102, 126, 234, 0.8);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .stTextArea label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stTextArea:hover label {
        color: #667eea !important;
    }
    
    .stRadio label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stRadio:hover label {
        color: #667eea !important;
    }
    
    .stMultiSelect label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stMultiSelect:hover label {
        color: #667eea !important;
    }
    
    .stMultiSelect > div > div {
        transition: all 0.3s ease;
    }
    
    .stMultiSelect > div > div:hover {
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    /* Number input styling with gradient hover */
    .stNumberInput {
        transition: all 0.3s ease;
    }
    
    .stNumberInput:hover {
        transform: translateY(-1px);
    }
    
    .stNumberInput label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stNumberInput:hover label {
        color: #667eea !important;
    }
    
    .stNumberInput input {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        border: 1px solid var(--glass-border);
        color: #2d3748;
        transition: all 0.3s ease;
    }
    
    .stNumberInput input:hover {
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    .stNumberInput input:focus {
        border: 1px solid rgba(102, 126, 234, 0.8);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Date input styling with gradient hover */
    .stDateInput {
        transition: all 0.3s ease;
    }
    
    .stDateInput:hover {
        transform: translateY(-1px);
    }
    
    .stDateInput label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stDateInput:hover label {
        color: #667eea !important;
    }
    
    .stDateInput input {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        border: 1px solid var(--glass-border);
        color: #2d3748;
        transition: all 0.3s ease;
    }
    
    .stDateInput input:hover {
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    .stDateInput input:focus {
        border: 1px solid rgba(102, 126, 234, 0.8);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Time input styling with gradient hover */
    .stTimeInput {
        transition: all 0.3s ease;
    }
    
    .stTimeInput:hover {
        transform: translateY(-1px);
    }
    
    .stTimeInput label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stTimeInput:hover label {
        color: #667eea !important;
    }
    
    .stTimeInput input {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        border: 1px solid var(--glass-border);
        color: #2d3748;
        transition: all 0.3s ease;
    }
    
    .stTimeInput input:hover {
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    .stTimeInput input:focus {
        border: 1px solid rgba(102, 126, 234, 0.8);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Text input styling with gradient hover */
    .stTextInput {
        transition: all 0.3s ease;
    }
    
    .stTextInput:hover {
        transform: translateY(-1px);
    }
    
    .stTextInput label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stTextInput:hover label {
        color: #667eea !important;
    }
    
    .stTextInput input {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        border: 1px solid var(--glass-border);
        color: #2d3748;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:hover {
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    .stTextInput input:focus {
        border: 1px solid rgba(102, 126, 234, 0.8);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Color picker styling with gradient hover */
    .stColorPicker {
        transition: all 0.3s ease;
    }
    
    .stColorPicker:hover {
        transform: translateY(-1px);
    }
    
    .stColorPicker label {
        color: #2d3748 !important;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stColorPicker:hover label {
        color: #667eea !important;
    }
    
    .stColorPicker button {
        border-radius: 8px;
        transition: all 0.3s ease;
        border: 2px solid var(--glass-border);
    }
    
    .stColorPicker button:hover {
        border: 2px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
        transform: scale(1.05);
    }
    
    /* Sidebar expander hover effects */
    .css-1d391kg .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .css-1d391kg .streamlit-expanderHeader::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .css-1d391kg .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(102, 126, 234, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        transform: translateY(-1px);
    }
    
    .css-1d391kg .streamlit-expanderHeader:hover::before {
        left: 100%;
    }
    
    /* Metric cards enhanced hover effects */
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(116, 185, 255, 0.4);
    }
    
    /* Container with gradient borders */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"]:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #4a5568;
        font-weight: 500;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100%;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: white;
        box-shadow: var(--shadow-lg);
        transform: translateY(-1px);
    }
    
    .stTabs [aria-selected="true"]:hover {
        background: var(--secondary-gradient);
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid var(--glass-border);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .streamlit-expanderHeader::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    
    .streamlit-expanderHeader:hover::before {
        left: 100%;
    }
    
    .streamlit-expanderHeader:active {
        transform: translateY(0);
    }
    
    /* Chart containers with glassmorphism */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.2);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(102, 126, 234, 0.02) 100%);
    }
    
    /* Success/Info/Warning messages with gradients */
    .stSuccess {
        background: var(--success-gradient);
        border-radius: 12px;
        border: none;
        color: white;
    }
    
    .stInfo {
        background: var(--warning-gradient);
        border-radius: 12px;
        border: none;
        color: white;
    }
    
    .stError {
        background: var(--secondary-gradient);
        border-radius: 12px;
        border: none;
        color: white;
    }
    
    /* Auto-responsive containers */
    .auto-responsive-container {
        width: 100%;
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid var(--glass-border);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .auto-responsive-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .auto-responsive-container:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        transform: translateY(-3px);
    }
    
    .auto-responsive-container:hover::before {
        left: 100%;
    }
    
    /* Additional interactive elements hover effects */
    
    /* Progress bar styling with gradient hover */
    .stProgress {
        transition: all 0.3s ease;
    }
    
    .stProgress:hover {
        transform: translateY(-1px);
    }
    
    .stProgress > div > div {
        background: var(--primary-gradient) !important;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stProgress:hover > div > div {
        background: var(--secondary-gradient) !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Alert/Message boxes with gradient hover */
    .stAlert {
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stAlert::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stAlert:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .stAlert:hover::before {
        left: 100%;
    }
    
    /* Code block styling with gradient hover */
    .stCode {
        border-radius: 8px;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .stCode:hover {
        border: 1px solid rgba(102, 126, 234, 0.4);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
        transform: translateY(-1px);
    }
    
    /* DataFrame styling with gradient hover */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .stDataFrame:hover {
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    
    /* Image styling with gradient hover */
    .stImage {
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .stImage:hover {
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px) scale(1.01);
    }
    
    /* Sidebar elements enhanced hover */
    .css-1d391kg .stSelectbox > div > div:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(102, 126, 234, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .css-1d391kg .stRadio:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(102, 126, 234, 0.05) 100%);
        border-radius: 8px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    /* Footer styling */
    .footer-container {
        background: var(--dark-gradient);
        border-radius: 15px;
        margin-top: 2rem;
        padding: 1.5rem;
        border: 1px solid var(--glass-border);
    }
    
    .footer-container a {
        transition: all 0.3s ease;
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer-container a:hover {
        text-shadow: 0 0 10px currentColor;
        transform: scale(1.05);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.8s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Glow effects for special elements */
    .glow-effect {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .glow-effect:hover {
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
    }
    </style>
    
    <script>
    // Continuous device detection
    function updateDeviceType() {
        const width = window.innerWidth;
        let newDeviceType;
        
        if (width <= 768) {
            newDeviceType = 'mobile';
        } else if (width <= 1024) {
            newDeviceType = 'tablet';
        } else {
            newDeviceType = 'desktop';
        }
        
        // Update body class for CSS targeting
        document.body.className = document.body.className.replace(/device-\\w+/g, '');
        document.body.classList.add('device-' + newDeviceType);
        
        // Store current device type
        window.currentDeviceType = newDeviceType;
        
        return newDeviceType;
    }
    
    // Update on load and resize with debouncing
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(updateDeviceType, 100);
    });
    
    // Initial update
    updateDeviceType();
    </script>
    """
    
    st.markdown(device_detection_css, unsafe_allow_html=True)
    
    # Detect device type using screen width heuristics
    # Since this is server-side, we'll use responsive CSS primarily
    width_detection = """
    <div id="width-detector" style="display: none;">
        <div class="device-mobile">mobile</div>
        <div class="device-tablet">tablet</div>
        <div class="device-desktop">desktop</div>
    </div>
    """
    
    st.markdown(width_detection, unsafe_allow_html=True)
    
    # Return device type based on CSS media queries
    # The actual detection happens client-side via CSS
    return 'responsive'  # This signals to use CSS-based responsive design

# Page configuration
st.set_page_config(
    page_title="Global Sales Performance Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="auto"
)

# Responsive CSS for all devices
st.markdown("""
<style>
    /* Main container responsive styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
        transition: all 0.3s ease;
    }
    
    /* Header responsive with smooth transitions */
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        padding: 0.5rem;
        transition: all 0.4s ease;
    }
    
    .main-header:hover {
        transform: translateY(-2px);
        text-shadow: 0 2px 8px rgba(31, 119, 180, 0.3);
    }
    
    /* Metric cards responsive with enhanced transitions */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        text-align: center;
        min-height: 100px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-container:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    /* Responsive metrics with smooth animations */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 32px rgba(116, 185, 255, 0.3);
    }
    
    [data-testid="metric-container"] label {
        color: white !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: white !important;
        font-size: clamp(1.2rem, 3vw, 2rem);
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    /* Enhanced tabs with smooth transitions */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        flex-wrap: wrap;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        min-height: 50px;
        padding: 8px 16px;
        font-size: clamp(0.8rem, 2vw, 1rem);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    /* Sidebar responsive with enhanced transitions */
    .css-1d391kg {
        padding-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .css-1d391kg:hover {
        box-shadow: 2px 0 15px rgba(102, 126, 234, 0.1);
    }
    
    /* Charts responsive with smooth transitions */
    .js-plotly-plot, .plotly {
        width: 100% !important;
        height: auto !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .js-plotly-plot:hover, .plotly:hover {
        transform: translateY(-3px) scale(1.005);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15);
    }
    
    /* Mobile optimizations with smooth transitions */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            background: rgba(255, 255, 255, 1.0);
            border: 1px solid rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .main-header {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px;
            font-size: 0.8rem;
            color: #2d3748 !important;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-1px) scale(1.01);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
        }
        
        [data-testid="metric-container"] {
            min-height: 100px;
            padding: 0.5rem;
            margin: 0.25rem;
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-3px) scale(1.01);
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            font-size: 1.2rem;
            transition: all 0.3s ease;
        }
        
        /* Stack columns on mobile with smooth transitions */
        .element-container .stColumn {
            width: 100% !important;
            flex: 1 1 100% !important;
            transition: all 0.3s ease;
        }
        
        /* Mobile text improvements with transitions */
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3 {
            color: #2d3748 !important;
            text-align: center;
            transition: color 0.3s ease;
        }
        
        .main .block-container p,
        .main .block-container .stMarkdown {
            color: #4a5568 !important;
            transition: color 0.3s ease;
        }
        
        .stSelectbox label,
        .stRadio label,
        .stMultiSelect label {
            color: #2d3748 !important;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
    }
    
    /* Tablet optimizations with smooth transitions */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 2rem;
            transition: all 0.3s ease;
        }
        
        .main-header:hover {
            transform: translateY(-1px);
            text-shadow: 0 2px 6px rgba(31, 119, 180, 0.2);
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 14px;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 4px 10px rgba(102, 126, 234, 0.2);
        }
        
        [data-testid="metric-container"] {
            min-height: 110px;
            padding: 0.75rem;
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px) scale(1.02);
        }
    }
    
    /* Desktop optimizations with enhanced transitions */
    @media (min-width: 1025px) {
        .main-header {
            font-size: 2.5rem;
            transition: all 0.4s ease;
        }
        
        .main-header:hover {
            transform: translateY(-3px);
            text-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
        }
        
        [data-testid="metric-container"] {
            min-height: 120px;
            padding: 1rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-8px) scale(1.03);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.25);
        }
    }
    
    /* Data table responsive with smooth transitions */
    .dataframe {
        font-size: clamp(0.7rem, 1.5vw, 0.9rem);
        transition: all 0.3s ease;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.1);
    }
    
    /* Expander responsive with enhanced transitions */
    .streamlit-expanderHeader {
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    .streamlit-expanderHeader:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.15);
    }
    
    /* Text area responsive with smooth transitions */
    .stTextArea textarea {
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 8px;
    }
    
    .stTextArea textarea:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
    }
    
    .stTextArea textarea:focus {
        transform: translateY(-2px) scale(1.002);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
    }
    
    /* Button responsive with enhanced animations */
    .stButton button {
        width: 100%;
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
        padding: 0.5rem 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 8px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.25);
    }
    
    .stButton button:active {
        transform: translateY(-1px) scale(1.01);
        transition: all 0.1s ease;
    }
    
    /* Selectbox responsive with smooth transitions */
    .stSelectbox {
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
        transition: all 0.3s ease;
    }
    
    .stSelectbox:hover {
        transform: translateY(-1px);
    }
    
    /* Hide Streamlit menu and footer on mobile with smooth transitions */
    @media (max-width: 768px) {
        #MainMenu {visibility: hidden; opacity: 0; transition: opacity 0.3s ease;}
        footer {visibility: hidden; opacity: 0; transition: opacity 0.3s ease;}
        header {visibility: hidden; opacity: 0; transition: opacity 0.3s ease;}
    }
    
    /* Global page transitions */
    * {
        transition-property: transform, box-shadow, background, color, border, opacity;
        transition-duration: 0.3s;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Smooth scrolling for the entire page */
    html {
        scroll-behavior: smooth;
    }
    
    /* Page entrance animation */
    .main {
        animation: pageEntrance 0.8s ease-out;
    }
    
    @keyframes pageEntrance {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Enhanced focus states for accessibility */
    *:focus {
        outline: 2px solid rgba(102, 126, 234, 0.5);
        outline-offset: 2px;
        transition: outline 0.2s ease;
    }
    
    /* Loading state transitions */
    .stSpinner {
        border-radius: 50%;
        animation: spin 1s linear infinite, pulse 2s ease-in-out infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

def format_number(num):
    """Format large numbers with appropriate suffixes."""
    if num >= 1_000_000_000:
        return f"${num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"${num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"${num/1_000:.1f}K"
    else:
        return f"${num:,.0f}"

def load_data():
    """Load or create sample data."""
    processor = SalesDataProcessor()
    visualizer = SalesVisualizer()
    
    # Create sample data if it doesn't exist
    sample_data_path = "data/sample_sales_data.csv"
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists(sample_data_path):
        sample_df = create_sample_data()
        sample_df.to_csv(sample_data_path, index=False)
        print(f"Sample data created at: {sample_data_path}")
    
    return processor, visualizer, sample_data_path

def sidebar_content():
    """Sidebar content that can be used in both sidebar and expander."""
    # Data source selection
    st.subheader("📂 Data Source Options")
    
    # Data source radio buttons
    data_source = st.radio(
        "Choose your data source:",
        ["Use Sample Data", "Upload File", "Paste CSV Data"],
        index=0
    )
    
    # File upload option
    uploaded_file = None
    csv_text = None
    
    if data_source == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload your sales data (CSV/Excel)",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a file with columns: Country, Region, Sales, and optionally Profit, Year, Product_Category"
        )
    
    elif data_source == "Paste CSV Data":
        st.markdown("**📋 Paste CSV Data:**")
        
        # Add help section for CSV format
        with st.expander("💡 CSV Format Help & Auto-Transform"):
            st.markdown("""
            **🔄 Auto-Transform Features:**
            - **Column Mapping**: Automatically detects columns like 'revenue' → 'Sales', 'nation' → 'Country'
            - **Currency Conversion**: Removes $, €, £ symbols and converts K/M/B notation
            - **Region Generation**: Auto-generates regions from country names
            - **Data Validation**: Fills missing required fields intelligently
            
            **📝 Supported Formats:**
            ```
            Country,Sales,Region
            USA,50000,North America
            UK,30000,Europe
            ```
            
            **Or paste ANY raw data - the system will auto-transform it!**
            ```
            nation,revenue,continent
            United States,$75K,NA
            Britain,€45M,EU
            ```
            """)
        
        csv_text = st.text_area(
            "Paste your CSV data here:",
            height=200,
            placeholder="Country,Sales,Region\nUSA,50000,North America\nUK,30000,Europe\n...",
            help="Paste CSV data or any raw format - the system will auto-transform it to the required format"
        )
        
        # Initialize session state for CSV submission
        if 'csv_submitted' not in st.session_state:
            st.session_state.csv_submitted = False
        if 'submitted_csv_text' not in st.session_state:
            st.session_state.submitted_csv_text = ""
            
        # Submit button for CSV data
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("📊 Process CSV Data", disabled=not csv_text or csv_text.strip() == ""):
                st.session_state.csv_submitted = True
                st.session_state.submitted_csv_text = csv_text
                st.success("✅ CSV data submitted for processing!")
        
        with col2:
            if st.button("🗑️ Clear") and st.session_state.csv_submitted:
                st.session_state.csv_submitted = False
                st.session_state.submitted_csv_text = ""
                st.info("📋 Ready for new CSV data")
                st.rerun()
        
        # Return the submitted CSV text if it was submitted
        if st.session_state.csv_submitted and st.session_state.submitted_csv_text:
            csv_text = st.session_state.submitted_csv_text
            st.info("🔄 Using submitted CSV data")
        else:
            csv_text = None
    
    return data_source, uploaded_file, csv_text

def display_dashboard_content(processor, visualizer, sample_data_path, data_source, uploaded_file, csv_text, device_type):
    """Display the main dashboard content with automatic responsive design."""
    
    # Data processing
    if data_source == "Upload File" and uploaded_file is not None:
        # Process uploaded file
        temp_file = f"temp_{uploaded_file.name}"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            data_dict = processor.process_full_pipeline(temp_file)
            st.success("✅ Data uploaded and processed successfully!")
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            data_dict = processor.process_full_pipeline(sample_data_path)
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    elif data_source == "Paste CSV Data" and csv_text:
        # Process pasted CSV data with auto-transformation
        try:
            import pandas as pd
            import io
            
            # Create DataFrame from pasted CSV text
            csv_data = pd.read_csv(io.StringIO(csv_text))
            
            # Show original data preview
            st.info(f"📋 {len(csv_data)} rows loaded with columns: {', '.join(csv_data.columns)}")
            
            # Auto-transform the data to required format
            transformed_data = processor.auto_transform_data(csv_data)
            
            # Clean and process the transformed data
            cleaned_data = processor.clean_data(transformed_data)
            
            # Create aggregations
            continent_data = processor.aggregate_by_continent(cleaned_data)
            country_data = processor.aggregate_by_country(cleaned_data)
            growth_trends = processor.calculate_growth_trends(cleaned_data)
            
            # Get top performers
            top_countries = processor.get_top_performers(country_data, 'Total_Sales', 15)
            top_regions = processor.get_top_performers(continent_data, 'Total_Sales', 10)
            
            data_dict = {
                'raw_data': csv_data,
                'transformed_data': transformed_data,
                'cleaned_data': cleaned_data,
                'continent_data': continent_data,
                'country_data': country_data,
                'growth_trends': growth_trends,
                'top_countries': top_countries,
                'top_regions': top_regions
            }
            
            st.success(f"✅ CSV data auto-transformed and processed! {len(cleaned_data)} records ready for analysis.")
                
        except Exception as e:
            st.error(f"❌ Error processing CSV data: {str(e)}")
            st.info("💡 The system will auto-transform column names and data formats. Any raw data format should work!")
            data_dict = processor.process_full_pipeline(sample_data_path)
    
    else:
        # Use sample data
        data_dict = processor.process_full_pipeline(sample_data_path)
        if data_source == "Use Sample Data":
            st.info("📋 Using sample data. Upload your own file or paste CSV data to analyze real data.")
    
    # Auto-responsive filters using CSS media queries
    st.markdown("""
    <div class="responsive-filters">
        <style>
        .responsive-filters .stExpander {
            display: none;
        }
        
        @media (max-width: 768px) {
            .responsive-filters .stExpander {
                display: block !important;
            }
            .responsive-filters .filter-columns {
                display: none !important;
            }
        }
        
        @media (min-width: 769px) {
            .responsive-filters .filter-columns {
                display: flex !important;
            }
        }
        </style>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters that automatically adapt to screen size
    with st.expander("🔍 Filter Data", expanded=False):
        # Mobile: vertical layout, Desktop: horizontal layout
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            # Region filter
            available_regions = sorted(data_dict['cleaned_data']['Region'].unique())
            selected_regions = st.multiselect(
                "Select Regions",
                available_regions,
                default=available_regions
            )
        
        with col2:
            # Year filter (if available)
            if 'Year' in data_dict['cleaned_data'].columns:
                available_years = sorted(data_dict['cleaned_data']['Year'].unique())
                selected_years = st.multiselect(
                    "Select Years",
                    available_years,
                    default=available_years
                )
            else:
                selected_years = []
        
        with col3:
            # Product filter (if available)
            if 'Product_Category' in data_dict['cleaned_data'].columns:
                available_products = sorted(data_dict['cleaned_data']['Product_Category'].unique())
                selected_products = st.multiselect(
                    "Select Product Categories",
                    available_products,
                    default=available_products
                )
            else:
                selected_products = []
    
    # Apply filters
    filtered_data = data_dict['cleaned_data'][data_dict['cleaned_data']['Region'].isin(selected_regions)]
    
    if 'Year' in data_dict['cleaned_data'].columns and selected_years:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]
    
    if 'Product_Category' in data_dict['cleaned_data'].columns and selected_products:
        filtered_data = filtered_data[filtered_data['Product_Category'].isin(selected_products)]
    
    # Recalculate aggregations with filtered data
    filtered_continent_data = processor.aggregate_by_continent(filtered_data)
    filtered_country_data = processor.aggregate_by_country(filtered_data)
    filtered_growth_data = processor.calculate_growth_trends(filtered_data)
    
    filtered_data_dict = {
        'cleaned_data': filtered_data,
        'continent_data': filtered_continent_data,
        'country_data': filtered_country_data,
        'growth_trends': filtered_growth_data
    }
    
    # Generate KPIs
    kpis = visualizer.create_kpi_cards(filtered_data_dict)
    
    # Auto-responsive KPI Cards - CSS handles the layout
    st.subheader("📈 Key Performance Indicators")
    
    # Use CSS Grid for automatic responsive layout
    st.markdown("""
    <style>
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    @media (max-width: 768px) {
        .kpi-grid {
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Stunning KPI cards with gradient backgrounds
    st.markdown("""
    <div class="slide-in" style="margin: 2rem 0;">
        <h3 style="
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
            margin-bottom: 1.5rem;
        ">📊 Key Performance Indicators</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="metric-container glow-effect" style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        " onmouseover="
            this.style.transform='translateY(-5px) scale(1.02)';
            this.style.boxShadow='0 20px 50px rgba(79, 172, 254, 0.4)';
            this.style.background='linear-gradient(45deg, #4facfe, #00f2fe, #5fbcff, #1affff, #4facfe, #00f2fe)';
            this.style.backgroundSize='300% 300%';
            this.style.animation='gradientShift 2s ease infinite';
        " onmouseout="
            this.style.transform='translateY(0) scale(1)';
            this.style.boxShadow='0 10px 30px rgba(79, 172, 254, 0.3)';
            this.style.background='linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
            this.style.backgroundSize='100% 100%';
            this.style.animation='none';
        " onmousedown="
            this.style.transform='scale(0.98)';
            this.style.boxShadow='0 5px 15px rgba(79, 172, 254, 0.5)';
        " onmouseup="
            this.style.transform='translateY(-5px) scale(1.02)';
            this.style.boxShadow='0 20px 50px rgba(79, 172, 254, 0.4)';
        ">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">Total Sales</div>
            <div style="font-size: 2rem; font-weight: 700;">{}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">{}% YoY Growth</div>
        </div>
        
        <style>
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        </style>
        """.format(
            format_number(kpis.get('total_sales', 0)),
            f"{kpis.get('growth_rate', 0):.1f}"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container glow-effect" style="
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(67, 233, 123, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        " onmouseover="
            this.style.transform='translateY(-5px) scale(1.02)';
            this.style.boxShadow='0 20px 50px rgba(67, 233, 123, 0.4)';
            this.style.background='linear-gradient(45deg, #43e97b, #38f9d7, #56ff91, #4cffed, #43e97b, #38f9d7)';
            this.style.backgroundSize='300% 300%';
            this.style.animation='gradientShift 2s ease infinite';
        " onmouseout="
            this.style.transform='translateY(0) scale(1)';
            this.style.boxShadow='0 10px 30px rgba(67, 233, 123, 0.3)';
            this.style.background='linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)';
            this.style.backgroundSize='100% 100%';
            this.style.animation='none';
        " onmousedown="
            this.style.transform='scale(0.98)';
            this.style.boxShadow='0 5px 15px rgba(67, 233, 123, 0.5)';
        " onmouseup="
            this.style.transform='translateY(-5px) scale(1.02)';
            this.style.boxShadow='0 20px 50px rgba(67, 233, 123, 0.4)';
        ">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">Total Profit</div>
            <div style="font-size: 2rem; font-weight: 700;">{}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">{}% Margin</div>
        </div>
        """.format(
            format_number(kpis.get('total_profit', 0)),
            f"{kpis.get('profit_margin', 0):.1f}"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container glow-effect" style="
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(250, 112, 154, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        " onmouseover="
            this.style.transform='translateY(-5px) scale(1.02)';
            this.style.boxShadow='0 20px 50px rgba(250, 112, 154, 0.4)';
            this.style.background='linear-gradient(45deg, #fa709a, #fee140, #ff8bb0, #ffed56, #fa709a, #fee140)';
            this.style.backgroundSize='300% 300%';
            this.style.animation='gradientShift 2s ease infinite';
        " onmouseout="
            this.style.transform='translateY(0) scale(1)';
            this.style.boxShadow='0 10px 30px rgba(250, 112, 154, 0.3)';
            this.style.background='linear-gradient(135deg, #fa709a 0%, #fee140 100%)';
            this.style.backgroundSize='100% 100%';
            this.style.animation='none';
        " onmousedown="
            this.style.transform='scale(0.98)';
            this.style.boxShadow='0 5px 15px rgba(250, 112, 154, 0.5)';
        " onmouseup="
            this.style.transform='translateY(-5px) scale(1.02)';
            this.style.boxShadow='0 20px 50px rgba(250, 112, 154, 0.4)';
        ">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">Countries</div>
            <div style="font-size: 2rem; font-weight: 700;">{:,}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">Global Reach</div>
        </div>
        """.format(kpis.get('total_countries', 0)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container glow-effect" style="
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #2d3748;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(168, 237, 234, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        " onmouseover="
            this.style.transform='translateY(-5px) scale(1.02)';
            this.style.boxShadow='0 20px 50px rgba(168, 237, 234, 0.4)';
            this.style.background='linear-gradient(45deg, #a8edea, #fed6e3, #bef7fe, #ffe8f9, #a8edea, #fed6e3)';
            this.style.backgroundSize='300% 300%';
            this.style.animation='gradientShift 2s ease infinite';
        " onmouseout="
            this.style.transform='translateY(0) scale(1)';
            this.style.boxShadow='0 10px 30px rgba(168, 237, 234, 0.3)';
            this.style.background='linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)';
            this.style.backgroundSize='100% 100%';
            this.style.animation='none';
        " onmousedown="
            this.style.transform='scale(0.98)';
            this.style.boxShadow='0 5px 15px rgba(168, 237, 234, 0.5)';
        " onmouseup="
            this.style.transform='translateY(-5px) scale(1.02)';
            this.style.boxShadow='0 20px 50px rgba(168, 237, 234, 0.4)';
        ">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 0.5rem;">Regions</div>
            <div style="font-size: 2rem; font-weight: 700;">{:,}</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Coverage Areas</div>
        </div>
        """.format(kpis.get('total_regions', 0)), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show data transformation info if available
    if data_source == "Paste CSV Data" and 'transformed_data' in data_dict:
        with st.expander("🔄 Data Transformation Summary", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Original Data:**")
                st.write(data_dict['raw_data'].head())
                st.write(f"Original columns: {', '.join(data_dict['raw_data'].columns)}")
            
            with col2:
                st.markdown("**✅ Transformed Data:**")
                st.write(data_dict['transformed_data'].head())
                st.write(f"Mapped columns: {', '.join(data_dict['transformed_data'].columns)}")
        
        st.markdown("---")
    
    # Auto-responsive visualization container
    st.markdown("""
    <div class="viz-container">
        <style>
        .viz-container .stTabs {
            display: block;
        }
        
        .viz-container .stSelectbox {
            display: none;
        }
        
        @media (max-width: 768px) {
            .viz-container .stTabs {
                display: none !important;
            }
            .viz-container .stSelectbox {
                display: block !important;
            }
        }
        </style>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile-only: selectbox for chart selection
    st.markdown('<div class="device-mobile">', unsafe_allow_html=True)
    chart_option = st.selectbox(
        "📊 Choose Visualization:",
        ["🌍 World Map", "📊 Regional Analysis", "📈 Growth Trends", "🏆 Performance Analysis"],
        key="mobile_chart_selector"
    )
    
    # Handle mobile selectbox navigation
    if chart_option == "🌍 World Map":
        st.subheader("🌍 Global Sales Distribution")
        world_map = visualizer.create_world_map(filtered_country_data, device_type='responsive')
        st.plotly_chart(world_map, use_container_width=True, key="chart_selection_world_map")
    
    elif chart_option == "📊 Regional Analysis":
        st.subheader("📊 Sales by Region")
        
        # Auto-responsive layout for charts
        col1, col2 = st.columns([1, 1])
        
        with col1:
            bar_chart = visualizer.create_continent_bar_chart(filtered_continent_data, device_type='responsive')
            st.plotly_chart(bar_chart, use_container_width=True, key="chart_selection_bar")
        
        with col2:
            pie_chart = visualizer.create_sales_distribution_pie(filtered_continent_data, device_type='responsive')
            st.plotly_chart(pie_chart, use_container_width=True, key="chart_selection_pie")
    
    elif chart_option == "📈 Growth Trends":
        if len(filtered_growth_data) > 0:
            st.subheader("📈 Growth Trends")
            growth_chart = visualizer.create_growth_trend_chart(filtered_growth_data, device_type='responsive')
            st.plotly_chart(growth_chart, use_container_width=True, key="chart_selection_growth")
        else:
            st.info("📊 Growth trend data not available with current filters.")
    
    elif chart_option == "🏆 Performance Analysis":
        st.subheader("🏆 Performance Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            top_countries_chart = visualizer.create_top_performers_chart(
                filtered_country_data, 
                metric='Total_Sales', 
                title="Top 10 Countries by Sales",
                device_type='responsive'
            )
            st.plotly_chart(top_countries_chart, use_container_width=True, key="chart_selection_top_countries")
        
        with col2:
            profit_scatter = visualizer.create_profit_vs_sales_scatter(filtered_country_data, device_type='responsive')
            st.plotly_chart(profit_scatter, use_container_width=True, key="chart_selection_profit_scatter")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close mobile div
    
    # Desktop/Tablet-only: tabs for chart navigation
    st.markdown('<div class="device-desktop device-tablet">', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["🌍 World Map", "📊 Regional Analysis", "📈 Growth Trends", "🏆 Performance Analysis"])
    
    with tab1:
        st.subheader("🌍 Global Sales Distribution")
        world_map = visualizer.create_world_map(filtered_country_data, device_type='responsive')
        st.plotly_chart(world_map, use_container_width=True, key="tab_world_map")
    
    with tab2:
        st.subheader("📊 Sales by Region")
        
        col1, col2 = st.columns(2)
        
        with col1:
            bar_chart = visualizer.create_continent_bar_chart(filtered_continent_data, device_type='responsive')
            st.plotly_chart(bar_chart, use_container_width=True, key="tab_bar_chart")
        
        with col2:
            pie_chart = visualizer.create_sales_distribution_pie(filtered_continent_data, device_type='responsive')
            st.plotly_chart(pie_chart, use_container_width=True, key="tab_pie_chart")
    
    with tab3:
        if len(filtered_growth_data) > 0:
            st.subheader("📈 Growth Trends")
            growth_chart = visualizer.create_growth_trend_chart(filtered_growth_data, device_type='responsive')
            st.plotly_chart(growth_chart, use_container_width=True, key="tab_growth_chart")
        else:
            st.info("📊 Growth trend data not available with current filters.")
    
    with tab4:
        st.subheader("🏆 Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            top_countries_chart = visualizer.create_top_performers_chart(
                filtered_country_data, 
                metric='Total_Sales', 
                title="Top 10 Countries by Sales",
                device_type='responsive'
            )
            st.plotly_chart(top_countries_chart, use_container_width=True, key="tab_top_countries")
        
        with col2:
            profit_scatter = visualizer.create_profit_vs_sales_scatter(filtered_country_data, device_type='responsive')
            st.plotly_chart(profit_scatter, use_container_width=True, key="tab_profit_scatter")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close desktop div
    
    # Data table (visible on all devices)
    with st.expander("📋 View Data Table", expanded=False):
        st.dataframe(filtered_data, use_container_width=True)
    
    # Footer section with enhanced design
    st.markdown("---")
    
    # Create footer using Streamlit components for better compatibility
    st.markdown("""
    <div style="text-align: center; padding: 2rem; margin: 2rem 0; 
                background: linear-gradient(135deg, #232526 0%, #414345 100%); 
                border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);">
        <h3 style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            font-size: 1.4rem;
            font-weight: 600;
        ">🚀 Crafted with Cutting-Edge Technology</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Technology badges in columns for better layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <style>
        @keyframes streamlitGradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .streamlit-tech-badge {
            background: linear-gradient(-45deg, #ff6b6b, #ff8e8e, #ffa8a8, #ffb3b3, #ff6b6b, #ff4757);
            background-size: 300% 300%;
            animation: none;
        }
        .streamlit-tech-badge:hover {
            animation: streamlitGradientShift 2s ease infinite;
        }
        </style>
        <div style="text-align: center; margin: 1rem 0;">
            <a href="https://streamlit.io" target="_blank" 
               class="streamlit-tech-badge"
               style="color: #fff; text-decoration: none; font-weight: bold; 
                      padding: 12px 24px; 
                      border-radius: 15px; border: 1px solid rgba(255, 107, 107, 0.4);
                      display: inline-block; transition: all 0.3s ease;
                      box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
                      position: relative; overflow: hidden;
                      text-shadow: 0 2px 4px rgba(0,0,0,0.3);"
               onmouseover="
                   this.style.transform='translateY(-5px) scale(1.05)'; 
                   this.style.boxShadow='0 15px 40px rgba(255, 107, 107, 0.6)';
                   this.style.border='1px solid rgba(255, 107, 107, 0.8)';
               "
               onmouseout="
                   this.style.transform='translateY(0) scale(1)'; 
                   this.style.boxShadow='0 4px 15px rgba(255, 107, 107, 0.2)';
                   this.style.border='1px solid rgba(255, 107, 107, 0.4)';
               ">
                ⚡ Streamlit
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <style>
        @keyframes plotlyGradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .plotly-tech-badge {
            background: linear-gradient(-45deg, #00d4aa, #1dd1a1, #2ed3a3, #48dbab, #00d4aa, #38f9d7);
            background-size: 300% 300%;
            animation: none;
        }
        .plotly-tech-badge:hover {
            animation: plotlyGradientShift 2s ease infinite;
        }
        </style>
        <div style="text-align: center; margin: 1rem 0;">
            <a href="https://plotly.com/python/" target="_blank" 
               class="plotly-tech-badge"
               style="color: #fff; text-decoration: none; font-weight: bold; 
                      padding: 12px 24px; 
                      border-radius: 15px; border: 1px solid rgba(0, 212, 170, 0.4);
                      display: inline-block; transition: all 0.3s ease;
                      box-shadow: 0 4px 15px rgba(0, 212, 170, 0.2);
                      position: relative; overflow: hidden;
                      text-shadow: 0 2px 4px rgba(0,0,0,0.3);"
               onmouseover="
                   this.style.transform='translateY(-5px) scale(1.05)'; 
                   this.style.boxShadow='0 15px 40px rgba(0, 212, 170, 0.6)';
                   this.style.border='1px solid rgba(0, 212, 170, 0.8)';
               "
               onmouseout="
                   this.style.transform='translateY(0) scale(1)'; 
                   this.style.boxShadow='0 4px 15px rgba(0, 212, 170, 0.2)';
                   this.style.border='1px solid rgba(0, 212, 170, 0.4)';
               ">
                📊 Plotly
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <style>
        @keyframes pandasGradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .pandas-tech-badge {
            background: linear-gradient(-45deg, #9c88ff, #a555ff, #b566ff, #c777ff, #9c88ff, #764ba2);
            background-size: 300% 300%;
            animation: none;
        }
        .pandas-tech-badge:hover {
            animation: pandasGradientShift 2s ease infinite;
        }
        </style>
        <div style="text-align: center; margin: 1rem 0;">
            <a href="https://pandas.pydata.org/" target="_blank" 
               class="pandas-tech-badge"
               style="color: #fff; text-decoration: none; font-weight: bold; 
                      padding: 12px 24px; 
                      border-radius: 15px; border: 1px solid rgba(156, 136, 255, 0.4);
                      display: inline-block; transition: all 0.3s ease;
                      box-shadow: 0 4px 15px rgba(156, 136, 255, 0.2);
                      position: relative; overflow: hidden;
                      text-shadow: 0 2px 4px rgba(0,0,0,0.3);"
               onmouseover="
                   this.style.transform='translateY(-5px) scale(1.05)'; 
                   this.style.boxShadow='0 15px 40px rgba(156, 136, 255, 0.6)';
                   this.style.border='1px solid rgba(156, 136, 255, 0.8)';
               "
               onmouseout="
                   this.style.transform='translateY(0) scale(1)'; 
                   this.style.boxShadow='0 4px 15px rgba(156, 136, 255, 0.2)';
                   this.style.border='1px solid rgba(156, 136, 255, 0.4)';
               ">
                🐼 Pandas
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # Dashboard features
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0; padding: 1rem;
                background: rgba(102, 126, 234, 0.1); border-radius: 15px;
                backdrop-filter: blur(10px); border: 1px solid rgba(102, 126, 234, 0.2);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);">
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 18px; 
            font-weight: 600;
            margin-bottom: 0.5rem;
        ">
            📊 Global Sales Performance Dashboard with Auto-Responsive Design
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="text-align: center; color: #fff; background: rgba(102, 126, 234, 0.8); 
                    padding: 0.8rem; border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3);
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2); transition: all 0.3s ease;
                    cursor: pointer; position: relative; overflow: hidden;"
             onmouseover="
                 this.style.transform='translateY(-8px) scale(1.05)'; 
                 this.style.boxShadow='0 20px 40px rgba(102, 126, 234, 0.4)';
                 this.style.background='linear-gradient(135deg, rgba(102, 126, 234, 1) 0%, rgba(118, 75, 162, 1) 100%)';
             "
             onmouseout="
                 this.style.transform='translateY(0) scale(1)'; 
                 this.style.boxShadow='0 4px 15px rgba(102, 126, 234, 0.2)';
                 this.style.background='rgba(102, 126, 234, 0.8)';
             ">
            <strong>✨ Auto Device Detection</strong>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align: center; color: #fff; background: rgba(0, 212, 170, 0.8); 
                    padding: 0.8rem; border-radius: 10px; border: 1px solid rgba(0, 212, 170, 0.3);
                    box-shadow: 0 4px 15px rgba(0, 212, 170, 0.2); transition: all 0.3s ease;
                    cursor: pointer; position: relative; overflow: hidden;"
             onmouseover="
                 this.style.transform='translateY(-8px) scale(1.05)'; 
                 this.style.boxShadow='0 20px 40px rgba(0, 212, 170, 0.4)';
                 this.style.background='linear-gradient(135deg, rgba(0, 212, 170, 1) 0%, rgba(56, 249, 215, 1) 100%)';
             "
             onmouseout="
                 this.style.transform='translateY(0) scale(1)'; 
                 this.style.boxShadow='0 4px 15px rgba(0, 212, 170, 0.2)';
                 this.style.background='rgba(0, 212, 170, 0.8)';
             ">
            <strong>📁 CSV Upload</strong>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align: center; color: #fff; background: rgba(255, 107, 107, 0.8); 
                    padding: 0.8rem; border-radius: 10px; border: 1px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2); transition: all 0.3s ease;
                    cursor: pointer; position: relative; overflow: hidden;"
             onmouseover="
                 this.style.transform='translateY(-8px) scale(1.05)'; 
                 this.style.boxShadow='0 20px 40px rgba(255, 107, 107, 0.4)';
                 this.style.background='linear-gradient(135deg, rgba(255, 107, 107, 1) 0%, rgba(255, 140, 0, 1) 100%)';
             "
             onmouseout="
                 this.style.transform='translateY(0) scale(1)'; 
                 this.style.boxShadow='0 4px 15px rgba(255, 107, 107, 0.2)';
                 this.style.background='rgba(255, 107, 107, 0.8)';
             ">
            <strong>🔄 Data Transformation</strong>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="text-align: center; color: #fff; background: rgba(156, 136, 255, 0.8); 
                    padding: 0.8rem; border-radius: 10px; border: 1px solid rgba(156, 136, 255, 0.3);
                    box-shadow: 0 4px 15px rgba(156, 136, 255, 0.2); transition: all 0.3s ease;
                    cursor: pointer; position: relative; overflow: hidden;"
             onmouseover="
                 this.style.transform='translateY(-8px) scale(1.05)'; 
                 this.style.boxShadow='0 20px 40px rgba(156, 136, 255, 0.4)';
                 this.style.background='linear-gradient(135deg, rgba(156, 136, 255, 1) 0%, rgba(118, 75, 162, 1) 100%)';
             "
             onmouseout="
                 this.style.transform='translateY(0) scale(1)'; 
                 this.style.boxShadow='0 4px 15px rgba(156, 136, 255, 0.2)';
                 this.style.background='rgba(156, 136, 255, 0.8)';
             ">
            <strong>📈 Interactive Visualizations</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Final message
    st.markdown("""
    <div style="text-align: center; color: #4a5568; 
                font-size: 14px; margin-top: 2rem; padding: 1rem; 
                border-top: 1px solid rgba(102, 126, 234, 0.2);
                background: rgba(102, 126, 234, 0.05); border-radius: 10px;
                font-weight: 500;">
        Built with ❤️ for seamless data visualization experience
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main dashboard function with automatic device detection."""
    
    # Automatic device detection - no manual toggle needed
    device_type = update_device_detection()
    
    # Stunning gradient header with animations
    st.markdown("""
    <div class="fade-in" style="
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
    " onmouseover="
        this.style.transform='translateY(-5px) scale(1.02)';
        this.style.boxShadow='0 20px 50px rgba(102, 126, 234, 0.2)';
        this.style.background='linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%)';
        this.style.border='1px solid rgba(102, 126, 234, 0.3)';
    " onmouseout="
        this.style.transform='translateY(0) scale(1)';
        this.style.boxShadow='none';
        this.style.background='linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        this.style.border='1px solid rgba(102, 126, 234, 0.2)';
    ">
        <h1 style="
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            text-shadow: 0 4px 6px rgba(0,0,0,0.1);
            letter-spacing: -0.025em;
            transition: all 0.3s ease;
        " onmouseover="
            this.style.transform='scale(1.02)';
            this.style.filter='drop-shadow(0 2px 8px rgba(102, 126, 234, 0.3))';
        " onmouseout="
            this.style.transform='scale(1)';
            this.style.filter='none';
        ">
            🌍 Global Sales Performance Dashboard
        </h1>
        <p style="
            font-size: 1.2rem;
            color: rgba(102, 126, 234, 0.8);
            margin: 0;
            font-weight: 500;
            transition: all 0.3s ease;
        " onmouseover="
            this.style.transform='translateY(-2px)';
            this.style.color='rgba(102, 126, 234, 1)';
            this.style.textShadow='0 2px 4px rgba(102, 126, 234, 0.2)';
        " onmouseout="
            this.style.transform='translateY(0)';
            this.style.color='rgba(102, 126, 234, 0.8)';
            this.style.textShadow='none';
        ">
            ✨ AI-Powered Analytics with Real-time Responsive Design
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    processor, visualizer, sample_data_path = load_data()
    
    # Auto-responsive sidebar - shows based on screen size via CSS
    st.markdown("""
    <div class="sidebar-container">
        <div class="device-desktop device-tablet">
            <!-- Desktop/Tablet: Show full sidebar -->
        </div>
        <div class="device-mobile">
            <!-- Mobile: Show collapsible controls -->
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar content - automatically adapts
    with st.sidebar:
        st.header("📊 Dashboard Controls")
        data_source, uploaded_file, csv_text = sidebar_content()
    
    # Mobile-friendly expandable controls
    with st.container():
        st.markdown("""
        <style>
        @media (max-width: 768px) {
            .stSidebar { display: none !important; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Mobile controls in expander
        mobile_controls = st.container()
        with mobile_controls:
            st.markdown("""
            <div class="device-mobile">
            <style>
            .device-mobile { display: none; }
            @media (max-width: 768px) {
                .device-mobile { display: block !important; }
            }
            </style>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📊 Dashboard Controls", expanded=False):
                data_source_mobile, uploaded_file_mobile, csv_text_mobile = sidebar_content()
                # Use mobile values if on mobile
                data_source = data_source_mobile if 'data_source_mobile' in locals() else data_source
                uploaded_file = uploaded_file_mobile if 'uploaded_file_mobile' in locals() else uploaded_file
                csv_text = csv_text_mobile if 'csv_text_mobile' in locals() else csv_text
    
    # Continue with the rest of the dashboard - it will auto-adapt
    display_dashboard_content(processor, visualizer, sample_data_path, data_source, uploaded_file, csv_text, device_type)

if __name__ == "__main__":
    main()
