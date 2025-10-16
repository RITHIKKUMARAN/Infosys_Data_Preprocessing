import streamlit as st
from mvp.mvp_pipeline import SummarizationPipeline
import os
from dotenv import load_dotenv

# -------------------------
# Load env & page settings
# -------------------------
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="NeoGlass — Colorful Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Enhanced Modern CSS
# -------------------------
CUSTOM_STYLE = r"""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --tertiary-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  --glass-bg: rgba(255,255,255,0.05);
  --glass-border: rgba(255,255,255,0.1);
  --text-primary: #ffffff;
  --text-secondary: rgba(255,255,255,0.7);
  --text-muted: rgba(255,255,255,0.5);
  --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  --glow-purple: rgba(102, 126, 234, 0.4);
  --glow-pink: rgba(245, 87, 108, 0.4);
  --glow-cyan: rgba(0, 242, 254, 0.4);
}

/* Global Styles */
html, body, [class*="css"], .stApp {
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #0a0e27;
  color: var(--text-primary);
}

/* Dynamic Background */
.stApp::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(255, 107, 107, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 159, 64, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 60% 80%, rgba(72, 219, 251, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 30% 70%, rgba(162, 155, 254, 0.1) 0%, transparent 50%),
    linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
  z-index: -1;
  animation: backgroundPulse 15s ease-in-out infinite;
}

@keyframes backgroundPulse {
  0%, 100% { opacity: 1; filter: hue-rotate(0deg); }
  50% { opacity: 0.85; filter: hue-rotate(10deg); }
}

/* Floating Particles */
.particle {
  position: fixed;
  border-radius: 50%;
  pointer-events: none;
  z-index: 0;
  animation: floatParticle 20s infinite;
  opacity: 0;
}

.particle:nth-child(1) {
  width: 4px;
  height: 4px;
  background: rgba(255, 107, 107, 0.8);
  left: 10%;
  animation-delay: 0s;
  box-shadow: 0 0 10px rgba(255, 107, 107, 0.8);
}

.particle:nth-child(2) {
  width: 3px;
  height: 3px;
  background: rgba(255, 159, 64, 0.8);
  left: 30%;
  animation-delay: 5s;
  box-shadow: 0 0 10px rgba(255, 159, 64, 0.8);
}

.particle:nth-child(3) {
  width: 5px;
  height: 5px;
  background: rgba(72, 219, 251, 0.8);
  left: 50%;
  animation-delay: 10s;
  box-shadow: 0 0 10px rgba(72, 219, 251, 0.8);
}

.particle:nth-child(4) {
  width: 3px;
  height: 3px;
  background: rgba(162, 155, 254, 0.8);
  left: 70%;
  animation-delay: 15s;
  box-shadow: 0 0 10px rgba(162, 155, 254, 0.8);
}

.particle:nth-child(5) {
  width: 4px;
  height: 4px;
  background: rgba(255, 234, 167, 0.8);
  left: 85%;
  animation-delay: 8s;
  box-shadow: 0 0 10px rgba(255, 234, 167, 0.8);
}

@keyframes floatParticle {
  0% { transform: translateY(100vh) translateX(0) scale(0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-100vh) translateX(100px) scale(1.5); opacity: 0; }
}

/* Header Enhancement */
.modern-header {
  background: linear-gradient(135deg, 
    rgba(255, 107, 107, 0.15) 0%, 
    rgba(255, 159, 64, 0.12) 25%,
    rgba(255, 234, 167, 0.1) 50%,
    rgba(72, 219, 251, 0.12) 75%,
    rgba(162, 155, 254, 0.15) 100%);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  padding: 32px;
  margin-bottom: 24px;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 
              0 0 60px rgba(255, 159, 64, 0.2),
              inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  animation: headerFloat 6s ease-in-out infinite;
}

@keyframes headerFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.modern-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: 
    radial-gradient(circle at 30% 50%, rgba(255, 107, 107, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 70% 50%, rgba(72, 219, 251, 0.2) 0%, transparent 50%);
  animation: headerGlow 10s ease-in-out infinite;
}

.modern-header::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.1) 50%, 
    transparent 100%);
  animation: shimmer 8s ease-in-out infinite;
}

@keyframes headerGlow {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(15%, 10%) rotate(5deg); }
  66% { transform: translate(-10%, 15%) rotate(-5deg); }
}

@keyframes shimmer {
  0% { left: -100%; }
  50%, 100% { left: 200%; }
}

.header-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 20px;
}

.app-icon {
  font-size: 48px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 50%, #48dbfb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 30px rgba(255, 159, 64, 0.6));
  animation: iconPulse 3s ease-in-out infinite, iconRotate 20s linear infinite;
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 30px rgba(255, 159, 64, 0.6)); }
  50% { transform: scale(1.15); filter: drop-shadow(0 0 40px rgba(255, 107, 107, 0.8)); }
}

@keyframes iconRotate {
  0% { filter: drop-shadow(0 0 30px rgba(255, 159, 64, 0.6)); }
  33% { filter: drop-shadow(0 0 30px rgba(72, 219, 251, 0.6)); }
  66% { filter: drop-shadow(0 0 30px rgba(162, 155, 254, 0.6)); }
  100% { filter: drop-shadow(0 0 30px rgba(255, 159, 64, 0.6)); }
}

.header-text h1 {
  margin: 0;
  font-size: 36px;
  font-weight: 700;
  background: linear-gradient(135deg, 
    #ff6b6b 0%, 
    #ffa500 25%, 
    #ffe66d 50%, 
    #48dbfb 75%, 
    #a29bfe 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  animation: gradientShift 8s ease-in-out infinite;
  text-shadow: 0 0 40px rgba(255, 159, 64, 0.3);
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.header-text p {
  margin: 8px 0 0 0;
  color: rgba(255, 255, 255, 0.85);
  font-size: 16px;
  font-weight: 400;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* Modern Cards */
.neo-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 28px;
  backdrop-filter: blur(20px) saturate(180%);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.neo-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    #ff6b6b 0%, 
    #ffa500 25%, 
    #ffe66d 50%, 
    #48dbfb 75%, 
    #a29bfe 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.neo-card::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 159, 64, 0.1) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.neo-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4), 
              0 0 40px rgba(255, 159, 64, 0.2);
  border-color: rgba(255, 159, 64, 0.3);
}

.neo-card:hover::before {
  opacity: 1;
  animation: borderFlow 3s linear infinite;
}

.neo-card:hover::after {
  width: 300px;
  height: 300px;
}

@keyframes borderFlow {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

/* Section Titles */
.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-primary);
  animation: titleGlow 4s ease-in-out infinite;
}

.section-title::before {
  content: '';
  width: 4px;
  height: 24px;
  background: linear-gradient(180deg, #ff6b6b 0%, #ffa500 50%, #48dbfb 100%);
  border-radius: 2px;
  box-shadow: 0 0 10px rgba(255, 159, 64, 0.5);
  animation: barPulse 2s ease-in-out infinite;
}

@keyframes titleGlow {
  0%, 100% { text-shadow: 0 0 10px rgba(255, 159, 64, 0.3); }
  50% { text-shadow: 0 0 20px rgba(255, 159, 64, 0.5); }
}

@keyframes barPulse {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(1.2); }
}

/* Streamlit Component Overrides */
.stTextArea textarea {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 16px !important;
  padding: 16px !important;
  color: var(--text-primary) !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 15px !important;
  line-height: 1.6 !important;
  transition: all 0.3s !important;
}

.stTextArea textarea:focus {
  border-color: rgba(102, 126, 234, 0.5) !important;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
  background: rgba(255, 255, 255, 0.08) !important;
}

.stTextArea textarea::placeholder {
  color: var(--text-muted) !important;
}

/* Modern Buttons */
.stButton button {
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 50%, #48dbfb 100%) !important;
  background-size: 200% auto !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 14px 28px !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  letter-spacing: 0.3px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 4px 16px rgba(255, 159, 64, 0.4) !important;
  position: relative !important;
  overflow: hidden !important;
  animation: buttonGradient 3s ease infinite !important;
}

.stButton button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.stButton button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(255, 159, 64, 0.6) !important;
  background-position: right center !important;
}

.stButton button:hover::before {
  width: 300px;
  height: 300px;
}

.stButton button:active {
  transform: translateY(0) !important;
}

@keyframes buttonGradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Radio Buttons */
.stRadio > div {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid var(--glass-border);
}

.stRadio label {
  color: var(--text-primary) !important;
  font-weight: 500 !important;
}

/* Select Slider */
.stSlider {
  padding: 12px 0;
}

/* Sidebar Enhancements */
.css-1d391kg, [data-testid="stSidebar"] {
  background: rgba(10, 14, 39, 0.8) !important;
  backdrop-filter: blur(20px) !important;
}

[data-testid="stSidebar"] .neo-card {
  background: rgba(255, 255, 255, 0.05);
  margin-bottom: 16px;
}

/* Status Badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  margin-top: 12px;
}

.status-success {
  background: linear-gradient(135deg, rgba(67, 233, 123, 0.15) 0%, rgba(56, 249, 215, 0.15) 100%);
  border: 1px solid rgba(67, 233, 123, 0.3);
  color: #43e97b;
}

.status-error {
  background: linear-gradient(135deg, rgba(245, 87, 108, 0.15) 0%, rgba(240, 147, 251, 0.15) 100%);
  border: 1px solid rgba(245, 87, 108, 0.3);
  color: #f5576c;
}

/* Info Messages */
.stInfo, .stSuccess, .stError {
  border-radius: 12px !important;
  border: none !important;
  backdrop-filter: blur(10px) !important;
}

/* Download Button */
.stDownloadButton button {
  background: var(--tertiary-gradient) !important;
  box-shadow: 0 4px 16px rgba(79, 172, 254, 0.3) !important;
}

.stDownloadButton button:hover {
  box-shadow: 0 8px 24px rgba(79, 172, 254, 0.4) !important;
}

/* Spinner */
.stSpinner > div {
  border-color: rgba(102, 126, 234, 0.3) !important;
  border-top-color: #667eea !important;
}

/* Markdown Enhancements */
.stMarkdown code {
  background: rgba(255, 255, 255, 0.1) !important;
  padding: 2px 8px !important;
  border-radius: 6px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 13px !important;
  color: #4facfe !important;
}

/* Footer */
.footer {
  text-align: center;
  padding: 32px 0;
  color: var(--text-muted);
  font-size: 14px;
  font-weight: 400;
}

.footer-highlight {
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 600;
}

.header-row {
  display: flex;
  align-items: center;
  gap: 14px;
}
.app-title {
  font-weight: 800;
  font-size: 24px;
  margin: 0;
}
.app-sub {
  color: var(--muted);
  margin: 0;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .header-text h1 {
    font-size: 28px;
  }
  
  .modern-header {
    padding: 24px;
  }
  
  .neo-card {
    padding: 20px;
  }
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

::-webkit-scrollbar-thumb {
  background: var(--primary-gradient);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #7c8eef 0%, #8d5cb5 100%);
}
</style>

"""

st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)

# -------------------------
# Helper: pipeline loader
# -------------------------
@st.cache_resource
def get_pipeline():
    return SummarizationPipeline()

# If API key missing -> stop with an explanation (clean)
if not HF_API_KEY:
    st.markdown(
        "<div class='neo-card'><h3 style='margin:0'>⚠️ Missing Hugging Face API Key</h3>"
        "<p style='color: var(--text-secondary); margin-top: 12px;'>Add <code>HF_API_KEY</code> to your .env and restart. The UI is ready; the backend needs the key.</p></div>",
        unsafe_allow_html=True
    )
    st.stop()

# Try to initialize the pipeline, but don't crash the page if it fails
try:
    pipeline = get_pipeline()
    pipeline_ready = True
except Exception as e:
    pipeline = None
    pipeline_ready = False
    st.error(f"Failed to initialize SummarizationPipeline: {str(e)}")

# -------------------------
# Modern Header
# -------------------------
st.markdown(
    "<div class='neo-card' style='margin-bottom:16px;'>"
    "<div class='header-row'>"
    "<div style='display:flex;flex-direction:column;'>"
    "<div style='display:flex;align-items:center;gap:12px;'>"
    "<div style='font-size:30px'>📝</div>"
    "<div><div class='app-title'>NeoGlass — Chromatic Summarizer</div>"
    "<div class='muted'>Colorful background • glass UI • Hugging Face inference</div></div>"
    "</div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

# -------------------------
# Sidebar with Modern Design
# -------------------------
with st.sidebar:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚙️ Configuration</div>", unsafe_allow_html=True)
    
    method = st.radio(
        "Summarization Method",
        ["Extractive", "Abstractive"],
        index=1,
        help="Choose how the summary is generated"
    )
    
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    
    length = st.select_slider(
        "Summary Length",
        ["Short", "Medium", "Long"],
        value="Medium",
        help="Control the output length"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Status Card
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔐 System Status</div>", unsafe_allow_html=True)
    
    if pipeline_ready:
        st.markdown(
            "<div class='status-badge status-success'>✓ Pipeline Active</div>",
            unsafe_allow_html=True
        )
        st.caption(f"🔑 API Key: `{HF_API_KEY[:8]}...{HF_API_KEY[-4:]}`")
    else:
        st.markdown(
            "<div class='status-badge status-error'>✗ Pipeline Error</div>",
            unsafe_allow_html=True
        )
        st.caption("Check logs for details")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Info Card
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💡 About</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='color: var(--text-secondary); font-size: 14px; line-height: 1.6;'>
        Powered by <strong>Hugging Face</strong> models with a modern, 
        glass-morphic interface featuring dynamic gradients and smooth animations.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Main Content Area
# -------------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📄 Input Text</div>", unsafe_allow_html=True)
    
    input_text = st.text_area(
        "text_input",
        height=320,
        placeholder="Paste your article, notes, or any text you want to process...\n\nTry pasting:\n• Meeting transcripts\n• Research papers\n• Blog posts\n• News articles",
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        summarize_btn = st.button("✨ Summarize", use_container_width=True)
    with c2:
        paraphrase_btn = st.button("🔄 Paraphrase", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Output</div>", unsafe_allow_html=True)

    if 'last_action' not in st.session_state:
        st.session_state.last_action = None

    if summarize_btn:
        st.session_state.last_action = 'summarize'
    if paraphrase_btn:
        st.session_state.last_action = 'paraphrase'

    if not input_text:
        st.info("👈 Enter text in the input panel and select an action")
        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='color: var(--text-secondary); font-size: 14px; line-height: 1.8;'>
            <strong>Quick tips:</strong><br>
            • Paste 5-15 paragraphs for best results<br>
            • Works great with meeting notes & articles<br>
            • Try both extractive & abstractive methods
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        if st.session_state.last_action == 'summarize':
            if not pipeline_ready:
                st.error("Summarization backend not available. Check API key and pipeline logs.")
            else:
                with st.spinner("🔮 Generating your summary..."):
                    try:
                        summary = pipeline.summarize(input_text, method=method.lower(), length=length.lower())
                        if isinstance(summary, str) and (summary.startswith("Error") or summary.startswith("API Error")):
                            st.error(summary)
                        else:
                            st.success("✅ Summary generated successfully!")
                            st.text_area("output", value=summary, height=280, label_visibility="collapsed")
                            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
                            st.download_button(
                                "⬇️ Download Summary",
                                data=summary,
                                file_name="summary.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
                        
        elif st.session_state.last_action == 'paraphrase':
            if not pipeline_ready:
                st.error("Paraphrase backend not available. Check API key and pipeline logs.")
            else:
                with st.spinner("🔮 Paraphrasing your text..."):
                    try:
                        paraphrased = pipeline.paraphrase(input_text)
                        if isinstance(paraphrased, str) and (paraphrased.startswith("Error") or paraphrased.startswith("API Error")):
                            st.error(paraphrased)
                        else:
                            st.success("✅ Paraphrase completed successfully!")
                            st.text_area("output", value=paraphrased, height=280, label_visibility="collapsed")
                            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
                            st.download_button(
                                "⬇️ Download Paraphrase",
                                data=paraphrased,
                                file_name="paraphrase.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Error paraphrasing: {str(e)}")
        else:
            st.info("Press Summarize or Paraphrase to process your text")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Modern Footer
# -------------------------
st.markdown(
    """
    <div class='footer'>
        Built with <span class='footer-highlight'>♥</span> using Streamlit & Hugging Face
        <br>
        <span style='font-size: 12px; color: var(--text-muted);'>NeoGlass UI • 2025</span>
    </div>
    """,
    unsafe_allow_html=True,
)
