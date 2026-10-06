
import os
import tempfile
import matplotlib.pyplot as plt
import streamlit as st

from signal_io import ReadSignalFile, SaveSignalFile
from operations import AddSignals, MultiplySignalByConst


# =====================================================
# CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="DSP Studio Pro",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# PROFESSIONAL DARK THEME
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #030817;
    --panel: #07152b;
    --cyan: #22d3ee;
    --blue: #168cff;
    --purple: #8b5cf6;
    --green: #10b981;
    --text: #eaf6ff;
    --muted: #91b4d5;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, #102f64 0%, transparent 32%),
        radial-gradient(ellipse at 10% 70%, #071d3c 0%, transparent 35%),
        linear-gradient(135deg, #030817, #061226 65%, #020713);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(3, 8, 23, 0.8);
}

.block-container {
    max-width: 100%;
    padding: 1.3rem 2rem 2rem;
}

h1, h2, h3, h4 {
    color: #eaf6ff !important;
    letter-spacing: -0.5px;
}

p, label, .stMarkdown {
    color: #c7def5;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #040b1b, #07162b);
    border-right: 1px solid #16436a;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.4rem;
}

[data-testid="stSidebar"] hr {
    border-color: #163b5e;
}

.stButton > button {
    background: linear-gradient(110deg, #087fe8, #06b6d4);
    color: white !important;
    border: 1px solid #27c9f3;
    border-radius: 11px;
    min-height: 43px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #a5f3fc;
    box-shadow: 0 0 22px #0891b255;
    transform: translateY(-1px);
}

.stDownloadButton > button {
    background: linear-gradient(110deg, #047857, #059669);
    color: white !important;
    border: 1px solid #10b981;
    border-radius: 11px;
    min-height: 43px;
    font-weight: 700;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0a1e38, #07162b);
    border: 1px solid #194b74;
    padding: 17px;
    border-radius: 15px;
}

[data-testid="stMetricLabel"] {
    color: #91bce0 !important;
}

[data-testid="stMetricValue"] {
    color: #67e8f9 !important;
}

div[data-testid="stFileUploader"] {
    background: #07152b;
    border: 1px dashed #17608c;
    border-radius: 15px;
    padding: 12px;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #091b32;
    border-color: #20517b;
    border-radius: 9px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #164267;
    border-radius: 10px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #07152b;
    border-radius: 12px;
    padding: 7px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #b6d2ec;
    padding: 9px 16px;
}

.stTabs [aria-selected="true"] {
    background: #0b4771 !important;
    color: #67e8f9 !important;
}

.hero {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(ellipse at 80% 45%, #07598566, transparent 45%),
        linear-gradient(115deg, #07152b, #061a35 70%, #09294a);
    border: 1px solid #176092;
    border-radius: 22px;
    padding: 38px;
    margin-bottom: 25px;
    box-shadow: 0 15px 50px #00000035;
}

.hero-tag {
    display: inline-block;
    color: #67e8f9;
    background: #083b5a;
    border: 1px solid #12618b;
    border-radius: 30px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 15px;
}

.hero-title {
    font-size: clamp(34px, 4vw, 55px);
    font-weight: 800;
    line-height: 1.12;
    color: #f0f9ff;
}

.hero-title span {
    color: #22d3ee;
}

.hero-description {
    max-width: 680px;
    font-size: 15px;
    line-height: 1.8;
    color: #b8d8f4;
    margin-top: 15px;
}

.hero-wave {
    font-size: 42px;
    letter-spacing: 7px;
    color: #22d3ee;
    text-shadow: 0 0 20px #168cff;
    margin-top: 20px;
}

.section-card {
    background: linear-gradient(145deg, #091b33, #061327);
    border: 1px solid #153e62;
    border-radius: 16px;
    padding: 21px;
    margin-bottom: 17px;
}

.section-heading {
    color: #67e8f9;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #91b4d5;
    font-size: 13px;
    line-height: 1.7;
}

.feature-card {
    background: linear-gradient(145deg, #0a203b, #07152a);
    border: 1px solid #17456b;
    border-radius: 16px;
    padding: 22px;
    min-height: 180px;
    transition: 0.2s ease;
}

.feature-card:hover {
    border-color: #22d3ee;
    box-shadow: 0 0 24px #0891b220;
}

.feature-icon {
    font-size: 29px;
    margin-bottom: 14px;
}

.feature-title {
    color: #e5f7ff;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 8px;
}

.feature-description {
    color: #91b4d5;
    font-size: 12px;
    line-height: 1.8;
}

.status-pill {
    display: inline-block;
    color: #6ee7b7;
    background: #064e3b55;
    border: 1px solid #047857;
    border-radius: 20px;
    padding: 5px 11px;
    font-size: 12px;
}

.sidebar-brand {
    padding: 8px 2px 20px;
}

.sidebar-icon {
    font-size: 39px;
    color: #22d3ee;
    text-shadow: 0 0 20px #168cff;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    color: #f0f9ff;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #91b4d5;
}

.footer {
    text-align: center;
    color: #7095b8;
    font-size: 12px;
    padding: 22px 0 5px;
    border-top: 1px solid #153653;
    margin-top: 30px;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# SIGNAL HELPERS
# =====================================================
def read_uploaded_signal(uploaded_file):
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".txt", delete=False
        ) as temp:
            temp.write(uploaded_file.getvalue())
            temp_path = temp.name

        return ReadSignalFile(temp_path)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def display_signal(signal, title="Signal"):
    if not signal:
        st.warning("This signal has no samples.")
        return

    x = [sample[0] for sample in signal]
    y = [sample[1] for sample in signal]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
    fig.patch.set_facecolor("#07152b")

    for ax in axes:
        ax.set_facecolor("#091b32")
        ax.tick_params(colors="#b7d7f2")

        for spine in ax.spines.values():
            spine.set_color("#19466b")

        ax.xaxis.label.set_color("#b7d7f2")
        ax.yaxis.label.set_color("#b7d7f2")
        ax.title.set_color("#67e8f9")
        ax.grid(True, color="#244566", alpha=0.5)

    axes[0].stem(
        x, y,
        linefmt="#22d3ee",
        markerfmt="o",
        basefmt="#47708d"
    )
    axes[0].set_title("Discrete Signal")
    axes[0].set_xlabel("Sample Index")
    axes[0].set_ylabel("Amplitude")

    axes[1].plot(
        x, y,
        color="#8b5cf6",
        marker="o",
        linewidth=2,
        markersize=5
    )
    axes[1].set_title("Connected Line Representation")
    axes[1].set_xlabel("Sample Index")
    axes[1].set_ylabel("Amplitude")

    fig.suptitle(title, color="#e6f4ff", fontsize=14)
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def show_signal_info(signal_type, periodic, samples):
    a, b, c = st.columns(3)
    a.metric("Signal Type", signal_type)
    b.metric("Periodicity", periodic)
    c.metric("Total Samples", len(samples))


def show_samples(samples):
    st.dataframe(
        [
            {
                "Index / Frequency": sample[0],
                "Amplitude": sample[1]
            }
            for sample in samples
        ],
        use_container_width=True,
        hide_index=True
    )


def download_result(samples, signal_type, periodic, filename):
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as temp:
            temp_path = temp.name

        SaveSignalFile(temp_path, signal_type, periodic, samples)

        with open(temp_path, "rb") as file:
            data = file.read()

        st.download_button(
            "⬇️ Download Result TXT",
            data=data,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-icon">∿</div>
        <div class="sidebar-title">DSP Studio</div>
        <div class="sidebar-subtitle">DIGITAL SIGNAL PROCESSING</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Home", "Load & Visualize", "Signal Operations"],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### ⚡ Quick Guide")
    st.caption("01 · Upload your signals")
    st.caption("02 · Visualize the data")
    st.caption("03 · Process and export")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <div style="color:#67e8f9;font-weight:700;">
            ● System Ready
        </div>
        <div style="font-size:12px;color:#91b4d5;margin-top:8px;">
            Python · Streamlit<br>
            Matplotlib
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# TOP HEADER
# =====================================================
left, right = st.columns([3, 1])

with left:
    st.markdown("""
    <div style="padding:4px 0 12px;">
        <div style="font-size:clamp(23px,3vw,31px);
                    font-weight:800;color:#67e8f9;">
            ∿ DSP Studio Pro
        </div>
        <div style="color:#91b4d5;font-size:13px;">
            Analyze · Process · Visualize · Export
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(
        '<div style="text-align:right;padding-top:12px;">'
        '<span class="status-pill">● READY TO WORK</span></div>',
        unsafe_allow_html=True
    )

st.divider()


# =====================================================
# HOME
# =====================================================
if page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">WELCOME TO YOUR WORKSPACE</div>
        <div class="hero-title">
            DSP <span>Studio Pro</span>
        </div>
        <div style="font-size:20px;font-weight:700;color:#67e8f9;">
            Digital Signal Processing
        </div>
        <div class="hero-description">
            Your all-in-one workspace for reading, visualizing,
            and processing digital signals through a clean,
            modern engineering interface.
        </div>
        <div class="hero-wave">∿ ∿ ∿ ∿ ∿ ∿ ∿</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Explore Your Tools")
    st.markdown(
        '<div class="section-subtitle">'
        'Everything you need to work with your signals, in one place.'
        '</div><br>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📂</div>
            <div class="feature-title">Load & Visualize</div>
            <div class="feature-description">
                Upload TXT files, inspect sample values,
                and view two signal representations.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Visualization →", key="home_visualize",
                     use_container_width=True):
            st.session_state["navigation"] = "Load & Visualize"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Signal Operations</div>
            <div class="feature-description">
                Add two compatible signals or multiply
                a signal by a constant value.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Operations →", key="home_operations",
                     use_container_width=True):
            st.session_state["navigation"] = "Signal Operations"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📤</div>
            <div class="feature-title">Export Results</div>
            <div class="feature-description">
                Review processed samples and download
                the resulting signal as a TXT file.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Go to Results →", key="home_results",
                     use_container_width=True):
            st.session_state["navigation"] = "Signal Operations"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <div class="section-heading">Your Signal Workflow</div>
        <div class="section-subtitle">
            <span style="color:#22d3ee;">01 LOAD</span>
            &nbsp; → &nbsp;
            <span style="color:#8b5cf6;">02 VISUALIZE</span>
            &nbsp; → &nbsp;
            <span style="color:#22d3ee;">03 PROCESS</span>
            &nbsp; → &nbsp;
            <span style="color:#10b981;">04 EXPORT</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# LOAD & VISUALIZE
# =====================================================
elif page == "Load & Visualize":

    st.markdown("## 📂 Load & Visualize")
    st.markdown(
        '<div class="section-subtitle">'
        'Upload your signals to explore metadata, sample values and plots.'
        '</div><br>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Choose signal TXT files",
        type=["txt"],
        accept_multiple_files=True,
        key="visualization_upload"
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) selected.")

        for uploaded_file in uploaded_files:
            with st.container(border=True):
                st.markdown(f"### 📄 {uploaded_file.name}")

                try:
                    signal_type, periodic, samples = read_uploaded_signal(
                        uploaded_file
                    )

                    show_signal_info(signal_type, periodic, samples)

                    tab1, tab2 = st.tabs(
                        ["📈 Visualization", "📋 Sample Data"]
                    )

                    with tab1:
                        display_signal(samples, uploaded_file.name)

                    with tab2:
                        show_samples(samples)

                except Exception as error:
                    st.error(f"Could not read signal: {error}")

    else:
        st.markdown("""
        <div class="section-card">
            <div class="feature-icon">☁️</div>
            <div class="section-heading">Ready for your signal files</div>
            <div class="section-subtitle">
                Upload one or more TXT files above to start analyzing.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# SIGNAL OPERATIONS
# =====================================================
elif page == "Signal Operations":

    st.markdown("## ⚙️ Signal Operations")
    st.markdown(
        '<div class="section-subtitle">'
        'Select your input signals, choose an operation, and inspect the result.'
        '</div><br>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload signal files for processing",
        type=["txt"],
        accept_multiple_files=True,
        key="operations_upload"
    )

    signals = {}

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                signal_type, periodic, samples = read_uploaded_signal(
                    uploaded_file
                )

                signals[uploaded_file.name] = {
                    "type": signal_type,
                    "periodic": periodic,
                    "samples": samples
                }

            except Exception as error:
                st.error(f"{uploaded_file.name}: {error}")

    if not signals:
        st.info("Upload at least one valid signal file to begin.")

    else:
        st.markdown(
            f'<span class="status-pill">✓ {len(signals)} signal(s) ready</span>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        operation = st.selectbox(
            "SELECT OPERATION",
            ["Addition", "Multiplication by Constant"]
        )

        names = list(signals.keys())

        if operation == "Addition":

            if len(names) < 2:
                st.warning("Upload at least two signals for addition.")

            else:
                col1, col2 = st.columns(2)

                with col1:
                    first_name = st.selectbox(
                        "First Signal",
                        names,
                        key="first_signal"
                    )

                with col2:
                    other_names = [
                        name for name in names if name != first_name
                    ]

                    second_name = st.selectbox(
                        "Second Signal",
                        other_names,
                        key="second_signal"
                    )

                if st.button("＋ Add Signals",
                             use_container_width=True):
                    try:
                        first = signals[first_name]
                        second = signals[second_name]

                        if first["type"] != 0 or second["type"] != 0:
                            raise ValueError(
                                "This addition function currently supports "
                                "time-domain signals only."
                            )

                        if first["type"] != second["type"]:
                            raise ValueError(
                                "Both signals must have the same signal type."
                            )

                        result = AddSignals(
                            first["samples"],
                            second["samples"]
                        )

                        st.session_state["dsp_result"] = result
                        st.session_state["dsp_result_name"] = "Addition_Result"
                        st.session_state["dsp_result_type"] = first["type"]
                        st.session_state["dsp_result_periodic"] = first["periodic"]

                        st.success("Addition completed successfully.")

                    except Exception as error:
                        st.error(f"Could not add signals: {error}")

        elif operation == "Multiplication by Constant":

            selected_name = st.selectbox(
                "Select Signal",
                names,
                key="constant_signal"
            )

            constant = st.number_input(
                "Multiplication Constant",
                value=2.0,
                step=1.0
            )

            if constant == -1:
                st.caption("The signal amplitude will be inverted.")

            if st.button("✕ Multiply Signal",
                         use_container_width=True):
                try:
                    selected = signals[selected_name]

                    if selected["type"] != 0:
                        raise ValueError(
                            "This multiplication function currently supports "
                            "time-domain signals only."
                        )

                    result = MultiplySignalByConst(
                        selected["samples"],
                        constant
                    )

                    st.session_state["dsp_result"] = result
                    st.session_state["dsp_result_name"] = "Multiplication_Result"
                    st.session_state["dsp_result_type"] = selected["type"]
                    st.session_state["dsp_result_periodic"] = selected["periodic"]

                    st.success("Multiplication completed successfully.")

                except Exception as error:
                    st.error(f"Could not multiply signal: {error}")

        # RESULT PANEL
        if "dsp_result" in st.session_state:

            st.divider()
            st.markdown("## 📊 Operation Result")

            result = st.session_state["dsp_result"]
            result_name = st.session_state["dsp_result_name"]

            st.markdown(f"""
            <div class="section-card">
                <div class="section-heading">{result_name}</div>
                <div class="section-subtitle">
                    Operation completed · {len(result)} output samples
                </div>
            </div>
            """, unsafe_allow_html=True)

            show_samples(result)
            display_signal(result, result_name)

            download_result(
                result,
                st.session_state["dsp_result_type"],
                st.session_state["dsp_result_periodic"],
                f"{result_name}.txt"
            )


# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div class="footer">
    <b style="color:#67e8f9;">DSP STUDIO PRO</b>
    &nbsp; · &nbsp; Digital Signal Processing
    <br><br>
    ENGINEERED WITH PYTHON · STREAMLIT · MATPLOTLIB
</div>
""", unsafe_allow_html=True)