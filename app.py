import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile
import os
import shutil
import ollama

# 1. System Setup & Cyber Theme UI Injection
st.set_page_config(page_title="MAGNET-INTEL Workspace", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: #E5E5E5; }
    .forensic-header {
        background-color: #111111; padding: 15px; border-bottom: 3px solid #00FF66;
        border-radius: 4px; font-family: 'Courier New', Courier, monospace; margin-bottom: 20px;
    }
    .glitch-title { color: #00FF66; font-size: 24px; font-weight: bold; text-shadow: 0 0 8px rgba(0, 255, 102, 0.4); }
    section[data-testid="stSidebar"] { background-color: #0F0F0F !important; border-right: 2px solid #1A1A1A; min-width: 320px !important; max-width: 320px !important; }
    .investigation-card {
        background-color: #121212; padding: 18px; border-radius: 8px;
        border: 1px solid #222; border-top: 3px solid #00FF66; margin-bottom: 15px;
    }
    .terminal-log { background-color: #030303; color: #00FF66; font-family: 'Consolas', monospace; padding: 12px; border-radius: 4px; white-space: pre-wrap; }
    .sidebar-desc { color: #888888; font-size: 11px; margin-top: -10px; margin-bottom: 10px; padding-left: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class='forensic-header'>
        <span class='glitch-title'>🛡️ MAGNET-WORKBENCH // ADVANCED DIGITAL EVIDENCE EXAMINER</span>
    </div>
    """, unsafe_allow_html=True)

# Session state configuration mapping
if 'processed' not in st.session_state:
    st.session_state.processed = False
    st.session_state.files_df = None
    st.session_state.media_summary = None
    st.session_state.file_size_str = "0 GB"
    st.session_state.raw_text_summary = ""

# --- 📁 LEFT SIDEBAR: DEFAULT FORENSIC EVIDENCE ARTIFACT TREE ---
with st.sidebar:
    st.markdown("<h2 style='color:#00FF66; font-size:18px; font-family:monospace; margin-bottom:0px;'>📁 FORENSIC EVIDENCE</h2>", unsafe_allow_html=True)
    
    if st.session_state.processed:
        st.success(f"Target Active: {st.session_state.file_size_str}")
    else:
        st.caption("Status: Awaiting Data Source Ingestion...")
    st.write("---")
    
    artifact_tab = st.radio("Go to Explorer Categories:", [
        "🌐 CASE ACQUISITION & OVERVIEW",
        "📞 1. Call & Contact Data",
        "💬 2. Messages & Chats",
        "📍 3. Location Data (GPS)",
        "📷 4. Photos & Videos",
        "🌐 5. Internet & Browser Data",
        "📱 6. Apps Data",
        "📂 7. Files & Documents",
        "🔐 8. SIM & Device Info",
        "☁️ 9. Cloud & Backup Data",
        "🧠 10. Advanced Analysis"
    ])
    
    st.write("---")
    if "1. Call" in artifact_tab:
        st.markdown("<div class='sidebar-desc'>Logs (In/Out/Missed)<br>Contact list data</div>", unsafe_allow_html=True)
    elif "2. Messages" in artifact_tab:
        st.markdown("<div class='sidebar-desc'>SMS/MMS payloads<br>WhatsApp & Telegram DBs</div>", unsafe_allow_html=True)
    elif "4. Photos" in artifact_tab:
        st.markdown("<div class='sidebar-desc'>Gallery structures<br>EXIF metadata index</div>", unsafe_allow_html=True)

# 2. EVIDENCE INGESTION CONTROLLER ON CENTER MAIN FRAME
st.markdown("### 📥 STEP 1: LOAD ACQUISITION SOURCE TARGET")
uploaded_file = st.file_uploader("Upload Target Mobile Data Package Archive (.zip)", type=["zip"])

# --- PROCESS REAL UPLOADED FILES ---
if uploaded_file is not None and not st.session_state.processed:
    with st.status("🕵️‍♂️ PARSING REAL ARTIFACT SHARDS...", expanded=True) as status:
        # Calculate dynamic size metrics
        bytes_size = uploaded_file.size
        st.session_state.file_size_str = f"{bytes_size / (1024 * 1024):.2f} MB"
            
        extract_dir = "extracted_evidence"
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir)
        
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        file_details = []
        img_count, vid_count, db_count, doc_count = 0, 0, 0, 0
        
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, extract_dir)
                size_kb = os.path.getsize(full_path) / 1024
                ext = os.path.splitext(file)[1].lower()
                
                file_details.append({'File Name': file, 'Path': rel_path, 'Size (KB)': round(size_kb, 2)})
                
                if ext in ['.jpg', '.jpeg', '.png']: img_count += 1
                elif ext in ['.mp4', '.avi', '.mov']: vid_count += 1
                elif ext in ['.db', '.sqlite']: db_count += 1
                elif ext in ['.txt', '.pdf', '.json', '.md']: doc_count += 1

        # Real Files DataFrame
        st.session_state.files_df = pd.DataFrame(file_details)
        
        st.session_state.media_summary = pd.DataFrame({
            'Forensic Object': ['Photos / Images', 'Video Sequences', 'Active Databases', 'Documents / Logs'],
            'Count Records': [img_count, vid_count, db_count, doc_count]
        })
        
        st.session_state.raw_text_summary = f"Zip package contains {len(file_details)} distinct files. Database structures count: {db_count}. Document logs text assets count: {doc_count}."
        st.session_state.processed = True
        status.update(label=f"📁 RECONSTRUCTION FINISHED", state="complete", expanded=False)

# 3. INTERFACE RENDER SPLITTING ENGINE
col_center, col_right = st.columns([2.2, 1.1])

if not st.session_state.processed:
    with col_center:
        st.info("📌 System Standby Parameters Active: Upload forensic zip dump above.")
        st.markdown("<div class='terminal-log'>[SYS_IDLE] Awaiting external stream mount loop...</div>", unsafe_allow_html=True)
    with col_right:
        st.markdown("### ...")
else:
    with col_center:
        st.markdown(f"### 📂 Evidence View: {uploaded_file.name} ({st.session_state.file_size_str})")
        
        # Dynamic Views according to the Sidebar selection
        if "CASE ACQUISITION" in artifact_tab or "📂 7. Files" in artifact_tab:
            st.markdown("<div class='investigation-card'><b>📁 Real Extracted Files Registry List</b>", unsafe_allow_html=True)
            st.dataframe(st.session_state.files_df, use_container_width=True, hide_index=True)
            
            # Interactive file size graph based on real items uploaded
            if not st.session_state.files_df.empty:
                fig = px.bar(st.session_state.files_df.head(10), x='File Name', y='Size (KB)',
                             template='plotly_dark', color_discrete_sequence=['#00FF66'], title="Size Matrix of top 10 files")
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        elif "📷 4. Photos" in artifact_tab or "🌐 CASE ACQUISITION" in artifact_tab:
            st.markdown("<div class='investigation-card'><b>🖼️ Real Media Shards Summary</b>", unsafe_allow_html=True)
            st.dataframe(st.session_state.media_summary, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='investigation-card'><b>ℹ️ Artifact Framework Registry</b><br>Select '7. Files & Documents' or '4. Photos & Videos' tab on the left sidebar tree to visualize the real database file matrix extracted from your zip archive.</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("### ...")
        
        run_ollama = st.button("🚀 Analyze Connection Matrix")
        
        if run_ollama:
            with st.spinner("Processing vectors inside Ollama Engine Layer..."):
                try:
                    context_payload = f"""
                    You are an automated digital forensics Llama 3 analysis core engine.
                    Here is the structural telemetry data extracted from the suspect archive:
                    {st.session_state.raw_text_summary}
                    
                    Based strictly on these structural parameters, outline target investigation vectors in short bullet points.
                    """
                    
                    ollama_response = ollama.chat(model='llama3', messages=[
                        {'role': 'user', 'content': context_payload}
                    ])
                    
                    st.markdown(f"""
                    <div class='terminal-log' style='border-left: 4px solid #FF3333;'>
                    <b>[LIVE OLLAMA SYSTEM LOG INTERCEPT]</b><br><br>
                    {ollama_response['message']['content']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as sys_err:
                    st.error(f"Ollama Execution Fault. Check if model is pulled using 'ollama pull llama3'. Details: {sys_err}")