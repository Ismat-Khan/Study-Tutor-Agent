import streamlit as st
from pypdf import PdfReader

from agent import ask_tutor
from memory import add_message, get_memory_text


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
    ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 229, 255, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(124, 58, 237, 0.10),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #050816 0%,
                #081127 50%,
                #050816 100%
            );

        color: #f5f7ff;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }


    /* ========================================================
       TEXT
    ======================================================== */

    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
    }

    p, label {
        color: #cbd5e1;
    }

    [data-testid="stCaptionContainer"] {
        color: #94a3b8;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #060b1b 0%,
                #081127 100%
            );

        border-right: 1px solid rgba(0, 229, 255, 0.12);
    }

    [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        margin-top: 8px;
    }

    .sidebar-brand {
        text-align: center;
        padding: 8px 0 18px 0;
    }

    .sidebar-brand-icon {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .sidebar-brand-title {
        font-size: 21px;
        font-weight: 800;
        color: #67e8f9;
    }

    .sidebar-brand-subtitle {
        font-size: 12px;
        color: #7f8daa;
        margin-top: 3px;
    }


    /* ========================================================
       SIDEBAR STATUS
    ======================================================== */

    .status-box {
        padding: 14px;
        border-radius: 15px;

        background:
            linear-gradient(
                135deg,
                rgba(0, 229, 255, 0.07),
                rgba(99, 102, 241, 0.07)
            );

        border: 1px solid rgba(103, 232, 249, 0.15);

        margin: 10px 0 14px 0;
    }

    .status-line {
        font-size: 13px;
        color: #b8c4dc;
        padding: 4px 0;
    }


    /* ========================================================
       HERO CONTAINER
    ======================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(103, 232, 249, 0.15) !important;
        border-radius: 22px !important;
        background:
            linear-gradient(
                135deg,
                rgba(10, 25, 60, 0.78),
                rgba(10, 15, 35, 0.65)
            ) !important;

        box-shadow:
            0 12px 45px rgba(0, 0, 0, 0.20),
            inset 0 1px 0 rgba(255, 255, 255, 0.03);
    }


    /* ========================================================
       HERO
    ======================================================== */

    .hero-badge-text {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;

        background: rgba(0, 229, 255, 0.08);
        border: 1px solid rgba(0, 229, 255, 0.22);

        color: #67e8f9;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.8px;
    }

    .hero-description {
        color: #9eacc7;
        font-size: 16px;
        line-height: 1.7;
        max-width: 700px;
    }

    .hero-title-text {
        font-size: clamp(32px, 5vw, 54px);
        font-weight: 850;
        line-height: 1.05;
        margin: 10px 0 8px 0;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #67e8f9,
                #38bdf8,
                #a78bfa
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    /* ========================================================
       FEATURE CARDS
    ======================================================== */

    .feature-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }

    .feature-title {
        font-size: 17px;
        font-weight: 750;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .feature-text {
        font-size: 13px;
        line-height: 1.55;
        color: #8fa0bd;
    }


    /* ========================================================
       SECTION HEADER
    ======================================================== */

    .section-header {
        margin-top: 30px;
        margin-bottom: 5px;
    }

    .section-header-title {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
    }

    .section-header-subtitle {
        font-size: 13px;
        color: #8190ad;
        margin-top: 3px;
    }


    /* ========================================================
       CHAT AREA
    ======================================================== */

    [data-testid="stChatMessage"] {
        border-radius: 18px !important;

        border: 1px solid rgba(120, 160, 255, 0.10) !important;

        background:
            linear-gradient(
                135deg,
                rgba(12, 25, 52, 0.72),
                rgba(8, 18, 40, 0.60)
            ) !important;

        margin-bottom: 12px !important;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.12);
    }

    [data-testid="stChatMessage"] p {
        color: #dbe5f5;
        line-height: 1.7;
    }

    [data-testid="stChatMessage"] code {
        border-radius: 8px;
    }


    /* ========================================================
       EMPTY CHAT STATE
    ======================================================== */

    .empty-chat {
        text-align: center;
        padding: 35px 20px;
    }

    .empty-chat-icon {
        font-size: 45px;
        margin-bottom: 10px;
    }

    .empty-chat-title {
        font-size: 20px;
        font-weight: 750;
        color: #ffffff;
    }

    .empty-chat-text {
        color: #8494b2;
        font-size: 14px;
        max-width: 500px;
        margin: 6px auto 0 auto;
        line-height: 1.6;
    }


    /* ========================================================
       BUTTONS
    ======================================================== */

    .stButton > button {
        width: 100%;
        min-height: 42px;

        border-radius: 12px;

        border: 1px solid rgba(103, 232, 249, 0.20);

        background:
            linear-gradient(
                135deg,
                rgba(0, 170, 255, 0.10),
                rgba(88, 80, 255, 0.10)
            );

        color: #dffaff;

        font-weight: 650;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #67e8f9;

        box-shadow:
            0 0 18px rgba(0, 229, 255, 0.16);

        color: #ffffff;
    }


    /* ========================================================
       FILE UPLOADER
    ======================================================== */

    [data-testid="stFileUploader"] {
        background: rgba(8, 20, 43, 0.45);
        border-radius: 14px;
    }


    /* ========================================================
       SELECT BOX
    ======================================================== */

    div[data-baseweb="select"] > div {
        background: rgba(8, 20, 43, 0.72) !important;

        border-color: rgba(120, 160, 255, 0.18) !important;

        border-radius: 12px !important;
    }


    /* ========================================================
       CHAT INPUT
    ======================================================== */

    [data-testid="stChatInput"] {
        border-color: rgba(103, 232, 249, 0.22);
    }


    /* ========================================================
       EXPANDER
    ======================================================== */

    [data-testid="stExpander"] {
        border-radius: 12px;
        border-color: rgba(120, 160, 255, 0.14);
        background: rgba(8, 18, 40, 0.45);
    }


    /* ========================================================
       DIVIDER
    ======================================================== */

    hr {
        border-color: rgba(120, 160, 255, 0.10);
    }


    /* ========================================================
       MOBILE
    ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding: 1rem;
        }

        .hero-title-text {
            font-size: 34px;
        }

        .hero-description {
            font-size: 14px;
        }

        .section-header-title {
            font-size: 21px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "memory" not in st.session_state:
    st.session_state.memory = []

if "study_material" not in st.session_state:
    st.session_state.study_material = ""

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🎓</div>
            <div class="sidebar-brand-title">Study Tutor AI</div>
            <div class="sidebar-brand-subtitle">
                Your intelligent study companion
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # --------------------------------------------------------
    # STUDY MATERIAL
    # --------------------------------------------------------

    st.markdown("### 📚 Study Material")

    uploaded_file = st.file_uploader(
        "Upload your study PDF",
        type=["pdf"],
        help="Upload lecture notes, textbook chapters, or study material.",
    )

    if uploaded_file:

        if uploaded_file.name != st.session_state.pdf_name:

            try:

                reader = PdfReader(uploaded_file)

                text = ""

                for page in reader.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

                st.session_state.study_material = text
                st.session_state.pdf_name = uploaded_file.name

                st.success(
                    f"✓ {len(reader.pages)} pages loaded"
                )

            except Exception as e:

                st.error(
                    f"Could not read PDF: {e}"
                )

    elif not st.session_state.study_material:

        st.caption(
            "Upload lecture notes or a textbook PDF "
            "to let your tutor study with you."
        )

    st.divider()

    # --------------------------------------------------------
    # TUTOR SETTINGS
    # --------------------------------------------------------

    st.markdown("### ⚙️ Tutor Settings")

    difficulty = st.selectbox(
        "Learning Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    response_style = st.selectbox(
        "Teaching Style",
        [
            "Simple & Clear",
            "Detailed",
            "Step-by-Step",
            "Exam Focused",
        ],
    )

    st.divider()

    # --------------------------------------------------------
    # SESSION MEMORY
    # --------------------------------------------------------

    st.markdown("### 🧠 Session Memory")

    message_count = len(
        st.session_state.memory
    )

    if message_count:

        material_status = (
            "Loaded"
            if st.session_state.study_material
            else "Not loaded"
        )

        st.markdown(
            f"""
            <div class="status-box">
                <div class="status-line">
                    🟢 {message_count} messages remembered
                </div>
                <div class="status-line">
                    📄 Study material: {material_status}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.caption(
            "Your conversation will be remembered "
            "during this study session."
        )

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.memory = []

        st.rerun()


# ============================================================
# HERO
# ============================================================

with st.container(border=True):

    st.markdown(
        '<div class="hero-badge-text">✦ AI-POWERED LEARNING</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-title-text">
            Study smarter.<br>
            Understand deeper.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-description">
            Your personal AI tutor for explanations, practice,
            questions, and learning — powered by CrewAI and Groq.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FEATURE CARDS
# ============================================================

st.write("")

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="feature-icon">💡</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-title">Understand Concepts</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="feature-text">
                Get difficult topics explained in simple,
                student-friendly language.
            </div>
            """,
            unsafe_allow_html=True,
        )


with col2:

    with st.container(border=True):

        st.markdown(
            '<div class="feature-icon">📚</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-title">Learn From Your Notes</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="feature-text">
                Upload your study material and ask questions
                about what you're learning.
            </div>
            """,
            unsafe_allow_html=True,
        )


with col3:

    with st.container(border=True):

        st.markdown(
            '<div class="feature-icon">🧠</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-title">Personalized Tutoring</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="feature-text">
                Your tutor remembers the current conversation
                and adapts to your learning level.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# CHAT SECTION HEADER
# ============================================================

st.markdown(
    """
    <div class="section-header">
        <div class="section-header-title">
            💬 Ask Your Tutor
        </div>
        <div class="section-header-subtitle">
            Ask questions, explore concepts, and learn step by step.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# QUESTION & ANSWER BLOCK
# ============================================================

with st.container(border=True):

    if not st.session_state.memory:

        st.markdown(
            """
            <div class="empty-chat">
                <div class="empty-chat-icon">🎓</div>

                <div class="empty-chat-title">
                    Ready when you are
                </div>

                <div class="empty-chat-text">
                    Ask your first question below.
                    Your tutor can explain concepts, work through
                    problems, and use your uploaded study material.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        for message in st.session_state.memory:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask anything about your studies..."
)


if question:

    # --------------------------------------------------------
    # User message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    add_message(
        st.session_state.memory,
        "user",
        question,
    )


    # --------------------------------------------------------
    # Memory
    # --------------------------------------------------------

    conversation = get_memory_text(
        st.session_state.memory
    )


    # --------------------------------------------------------
    # Tutor context
    # --------------------------------------------------------

    tutor_context = f"""
Student learning level:
{difficulty}

Preferred teaching style:
{response_style}

"""

    enhanced_question = (
        tutor_context
        + "\nStudent question:\n"
        + question
    )


    # --------------------------------------------------------
    # Agent
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 Your tutor is thinking..."
        ):

            try:

                answer = ask_tutor(

                    question=enhanced_question,

                    study_material=(
                        st.session_state.study_material
                    ),

                    conversation_memory=conversation,

                )

                st.markdown(answer)

            except Exception as e:

                answer = (
                    "I encountered an error while "
                    "processing your question."
                )

                st.error(answer)

                with st.expander(
                    "Technical details"
                ):

                    st.code(str(e))


    # --------------------------------------------------------
    # Save response
    # --------------------------------------------------------

    add_message(
        st.session_state.memory,
        "assistant",
        answer,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎓 Study Tutor AI  •  Powered by CrewAI + Groq"
)
