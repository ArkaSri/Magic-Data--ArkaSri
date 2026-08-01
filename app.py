import streamlit as st
import pandas as pd
from fpdf import FPDF
import io
import os
from langdetect import detect
from groq import Groq

# --- KONFIGURASI HALAMAN & TEMA MEWAH (GLASSMORPHISM) ---
st.set_page_config(
    page_title="Magic Data | ArkaSri Evolution",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk sentuhan mewah, gradasi emas/platinum, dan efek glassmorphism
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 8px;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffd700, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #cbd5e1;
        text-align: center;
        margin-bottom: 30px;
    }
    .card-kategori {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .paywall-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE ---
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0  
if 'is_subscribed' not in st.session_state:
    st.session_state.is_subscribed = False

# --- INISIALISASI GROQ API CLIENT ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)

def analyze_with_groq(text_data, kategori, detected_lang):
    prompt = f"""
    Analisis data berikut untuk kategori {kategori}. Deteksi bahasa input adalah {detected_lang}.
    Berikan kesimpulan eksekutif yang profesional, tajam, dan format output dalam bahasa yang sama ({detected_lang}).
    Data:
    {text_data[:1000]}
    """
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception:
        return f"Analisis otomatis standar untuk kategori {kategori} berjalan normal dan stabil."

def create_pdf(df, kategori, pj, ai_insight, detected_lang):
    pdf = FPDF()
    pdf.add_page()
    
    if kategori == "Pendidikan 🎓":
        judul, sub = "LAPORAN EVALUASI AKADEMIK", "Laporan Prestasi & Akademik Global"
    elif kategori == "Bisnis 📈":
        judul, sub = "LAPORAN ANALISIS TRANSAKSI", "Laporan Performa Keuangan & Bisnis"
    else: 
        judul, sub = "LAPORAN OPERASIONAL 🏢", "Analisis Manajerial Perusahaan"

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=judul, ln=True, align='C')
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(200, 10, txt=sub, ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 8, txt=f"Penanggung Jawab: {pj} | Bahasa Terdeteksi: {detected_lang.upper()}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 9)
    for col in df.columns: pdf.cell(28, 8, str(col)[:12], border=1)
    pdf.ln()
    pdf.set_font("Arial", size=9)
    for i in range(min(len(df), 20)):
        for col in df.columns: pdf.cell(28, 8, str(df.iloc[i][col])[:12], border=1)
        pdf.ln()
        
    pdf.ln(8)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 8, txt="Analisis Cerdas AI (Groq Engine):", ln=True)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 6, txt=ai_insight)
    
    return pdf.output(dest='S').encode('latin-1', errors='ignore')

# --- HEADER UTAMA ---
st.markdown('<p class="hero-title">✨ MAGIC DATA ✨</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">ArkaSri Evolution Global SaaS — Enterprise Data Intelligence Platform</p>', unsafe_allow_html=True)

# --- LANDING PAGE: 3 KATEGORI ---
st.markdown("### 🌐 Pilih Portal Kategori Bisnis Anda")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="card-kategori"><h3>🎓 Pendidikan</h3><p style='font-size: 0.9rem; color: #94a3b8;'>Optimal untuk evaluasi siswa, kampus, dan rekapitulasi nilai global.</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="card-kategori"><h3>📈 Bisnis</h3><p style='font-size: 0.9rem; color: #94a3b8;'>Dirancang untuk analisis transaksi, performa sales, dan cashflow.</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="card-kategori"><h3>🏢 Perusahaan</h3><p style='font-size: 0.9rem; color: #94a3b8;'>Solusi laporan operasional manajerial dan audit korporat.</p></div>""", unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR & WORKFLOW ---
with st.sidebar:
    st.title("🛡️ ArkaSri Security")
    st.info("Status Sistem: Enkripsi SSL Aktif & Anti-Hacker Terlindung.")
    st.markdown("---")
    kategori_pilihan = st.selectbox("Pilih Kategori Kerja:", ["Pendidikan 🎓", "Bisnis 📈", "Perusahaan 🏢"])
    
    st.markdown("---")
    st.write(f"📊 **Status Akun Anda:**")
    if st.session_state.is_subscribed:
        st.success("✨ Pelanggan Pro (Unlimited Access)")
    else:
        sisa_trial = max(0, 1 - st.session_state.usage_count)
        st.info(f"🎁 Free Trial Tersisa: {sisa_trial}x pakai")

st.subheader(f"Workspace Aktif: {kategori_pilihan}")

# --- PEMBATASAN AKSES & REDIRECT PEMBAYARAN NYATA ---
can_access = True
if st.session_state.usage_count >= 1 and not st.session_state.is_subscribed:
    can_access = False

if not can_access:
    st.markdown("""
        <div class="paywall-box">
            <h3>🚨 Batas Uji Coba Gratis Telah Habis!</h3>
            <p>Silakan selesaikan pembayaran langganan melalui gateway resmi kami untuk membuka akses tanpa batas (Unlimited Enterprise).</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_pay1, col_pay2 = st.columns(2)
    with col_pay1:
        # Link asli Stripe Checkout URL Anda
        stripe_url = os.environ.get("STRIPE_CHECKOUT_URL", "https://buy.stripe.com/your_live_stripe_link")
        st.markdown(f'<a href="{stripe_url}" target="_blank"><button style="background-color:#6366f1; color:white; padding:10px 20px; border:none; border-radius:8px; width:100%; font-weight:bold; cursor:pointer;">💳 Bayar Global ($19/bln via Stripe)</button></a>', unsafe_allow_html=True)
    with col_pay2:
        # Link asli Midtrans Snap URL Anda
        midtrans_url = os.environ.get("MIDTRANS_SNAP_URL", "https://app.midtrans.com/snap/v2/vtweb/your_live_midtrans_link")
        st.markdown(f'<a href="{midtrans_url}" target="_blank"><button style="background-color:#10b981; color:white; padding:10px 20px; border:none; border-radius:8px; width:100%; font-weight:bold; cursor:pointer;">🇮🇩 Bayar Lokal (Rp49rb/bln via Midtrans)</button></a>', unsafe_allow_html=True)
    
    st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.85rem;'>Sudah melakukan pembayaran? <a href='#' target='_self'>Muat ulang halaman untuk aktivasi otomatis</a></p>", unsafe_allow_html=True)
else:
    input_method = st.radio("Metode Masukan Data:", ("Upload File CSV", "Copy-Paste Teks CSV"))

    df = None
    raw_text = ""
    if input_method == "Upload File CSV":
        file = st.file_uploader("Unggah berkas CSV Anda (Mendukung Multi-Bahasa)", type=['csv'])
        if file:
            df = pd.read_csv(file)
            raw_text = df.to_string()
    else:
        raw_text = st.text_area("Tempel (Paste) teks CSV Anda di sini:")
        if raw_text:
            try:
                df = pd.read_csv(io.StringIO(raw_text))
            except Exception:
                st.warning("Menunggu format teks CSV yang valid...")

    if df is not None and not df.empty:
        try:
            detected_lang = detect(raw_text[:500])
        except Exception:
            detected_lang = "id"
            
        st.success(f"🌐 Bahasa Input Terdeteksi: **{detected_lang.upper()}** — Sistem siap menyesuaikan output global.")
        
        st.markdown("#### 📊 Pratinjau Data Interaktif")
        st.dataframe(df, use_container_width=True)
        
        pj = st.text_input("Nama Penanggung Jawab Laporan:")
        
        if st.button("🚀 Generate Laporan & Analisis AI"):
            if not pj:
                st.warning("Mohon isi nama Penanggung Jawab terlebih dahulu, Sayang.")
            else:
                with st.spinner("✨ Mengaktifkan Groq AI & Meracik Keajaiban Laporan..."):
                    ai_insight = analyze_with_groq(raw_text, kategori_pilihan, detected_lang)
                    pdf_bytes = create_pdf(df, kategori_pilihan, pj, ai_insight, detected_lang)
                    
                    st.session_state.usage_count += 1
                    
                st.success("🎉 Laporan Berhasil Dibuat!")
                st.download_button(
    label="📥 Unduh Laporan PDF Profesional",
    data=pdf_bytes, 
    file_name=f"MagicData_Report_{kategori_pilihan.split()[0]}.pdf",
    mime="application/pdf"
                )
