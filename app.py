
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
# CUSTOM CSS — UI ONLY
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 8% 5%,
            rgba(0, 229, 255, 0.12),
            transparent 28%
        ),
        radial-gradient(
            circle at 92% 10%,
            rgba(124, 58, 237, 0.13),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(14, 165, 233, 0.07),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #030712 0%,
            #071226 48%,
            #030712 100%
        );

    color: #f8fafc;
}


/* ============================================================
   MAIN CONTAINER
============================================================ */

.block-container {
    max-width: 1280px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ============================================================
   SIDEBAR
============================================================ */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #040817 0%,
            #071226 55%,
            #040817 100%
        );

    border-right: 1px solid rgba(56, 189, 248, 0.14);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.4rem;
}


/* Sidebar logo */

.sidebar-logo {
    text-align: center;
    padding: 8px 0 18px 0;
}

.sidebar-logo-icon {
    font-size: 44px;
    margin-bottom: 5px;
    filter: drop-shadow(0 0 14px rgba(34, 211, 238, 0.45));
}

.sidebar-logo-title {
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.5px;

    background:
        linear-gradient(
            90deg,
            #67e8f9,
            #60a5fa,
            #a78bfa
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-logo-subtitle {
    color: #71809d;
    font-size: 12px;
    margin-top: 4px;
}


/* Sidebar headings */

[data-testid="stSidebar"] h3 {
    color: #dbeafe;
    font-size: 15px;
    font-weight: 700;
}


/* ============================================================
   HERO
============================================================ */

.hero {
    position: relative;
    overflow: hidden;

    padding: 34px 38px;
    margin-bottom: 24px;

    border-radius: 28px;

    border: 1px solid rgba(103, 232, 249, 0.18);

    background:
        linear-gradient(
            135deg,
            rgba(8, 30, 62, 0.94),
            rgba(9, 18, 40, 0.88)
        );

    box-shadow:
        0 20px 70px rgba(0, 0, 0, 0.30),
        inset 0 1px 0 rgba(255,255,255,0.06);
}

.hero::before {
    content: "";
    position: absolute;

    width: 220px;
    height: 220px;

    right: -70px;
    top: -100px;

    border-radius: 50%;

    background: rgba(34, 211, 238, 0.10);

    filter: blur(5px);
}

.hero::after {
    content: "";
    position: absolute;

    width: 170px;
    height: 170px;

    left: -90px;
    bottom: -100px;

    border-radius: 50%;

    background: rgba(139, 92, 246, 0.10);
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;

    padding: 7px 13px;

    margin-bottom: 14px;

    border-radius: 999px;

    background: rgba(34, 211, 238, 0.08);

    border: 1px solid rgba(34, 211, 238, 0.25);

    color: #67e8f9;

    font-size: 12px;
    font-weight: 700;

    letter-spacing: 0.7px;
}

.hero-title {
    font-size: clamp(34px, 5vw, 58px);
    font-weight: 850;

    line-height: 1.02;

    letter-spacing: -2px;

    margin: 0;

    background:
        linear-gradient(
            90deg,
            #ffffff 5%,
            #bff7ff 35%,
            #67e8f9 65%,
            #a78bfa 100%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 720px;

    color: #9fb0ca;

    font-size: 15px;

    line-height: 1.7;

    margin-top: 15px;
    margin-bottom: 0;
}


/* ============================================================
   FEATURE CARDS
============================================================ */

.feature-card {
    position: relative;

    height: 100%;

    padding: 21px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(15, 35, 69, 0.72),
            rgba(8, 19, 40, 0.72)
        );

    border: 1px solid rgba(148, 163, 184, 0.12);

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.18);

    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-3px);

    border-color: rgba(103, 232, 249, 0.28);

    box-shadow:
        0 18px 40px rgba(0, 0, 0, 0.25),
        0 0 25px rgba(34, 211, 238, 0.06);
}

.feature-icon {
    width: 44px;
    height: 44px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 13px;

    background: rgba(34, 211, 238, 0.08);

    border: 1px solid rgba(34, 211, 238, 0.15);

    font-size: 23px;

    margin-bottom: 12px;
}

.feature-title {
    font-weight: 750;
    font-size: 15px;

    color: #f8fafc;

    margin-bottom: 5px;
}

.feature-description {
    color: #8293b2;

    font-size: 12.5px;

    line-height: 1.55;
}


/* ============================================================
   SECTION HEADER
============================================================ */

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-top: 30px;
    margin-bottom: 12px;
}

.section-title {
    font-size: 20px;
    font-weight: 750;

    color: #f8fafc;

    letter-spacing: -0.3px;
}

.section-caption {
    color: #64748b;
    font-size: 12px;
}


/* ============================================================
   CHAT PANEL
============================================================ */

.chat-panel {
    position: relative;

    min-height: 350px;

    padding: 18px;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(8, 21, 43, 0.78),
            rgba(5, 13, 29, 0.82)
        );

    border: 1px solid rgba(103, 232, 249, 0.10);

    box-shadow:
        0 20px 55px rgba(0, 0, 0, 0.22),
        inset 0 1px 0 rgba(255,255,255,0.025);
}


/* ============================================================
   CHAT MESSAGES
============================================================ */

[data-testid="stChatMessage"] {
    border-radius: 18px !important;

    margin-bottom: 12px !important;

    padding: 8px 12px !important;

    border: 1px solid rgba(148, 163, 184, 0.08) !important;

    background: rgba(15, 27, 49, 0.60) !important;

    box-shadow: none !important;
}


/* User message */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background:
        linear-gradient(
            135deg,
            rgba(8, 45, 67, 0.75),
            rgba(8, 29, 51, 0.75)
        ) !important;

    border-color: rgba(34, 211, 238, 0.15) !important;
}


/* Assistant message */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background:
        linear-gradient(
            135deg,
            rgba(27, 22, 56, 0.65),
            rgba(12, 25, 48, 0.72)
        ) !important;

    border-color: rgba(167, 139, 250, 0.12) !important;
}


/* Message text */

[data-testid="stChatMessage"] p {
    color: #e2e8f0;
    line-height: 1.7;
    font-size: 14px;
}


/* ============================================================
   CHAT AVATARS
============================================================ */

[data-testid="chatAvatarIcon-user"] {
    background: rgba(34, 211, 238, 0.14);
}

[data-testid="chatAvatarIcon-assistant"] {
    background: rgba(139, 92, 246, 0.15);
}


/* ============================================================
   CHAT INPUT
============================================================ */

[data-testid="stChatInput"] {
    margin-top: 12px;
}

[data-testid="stChatInput"] > div {
    border-radius: 18px !important;

    border: 1px solid rgba(103, 232, 249, 0.20) !important;

    background:
        rgba(6, 18, 37, 0.92) !important;

    box-shadow:
        0 0 0 1px rgba(0, 0, 0, 0.12),
        0 12px 35px rgba(0, 0, 0, 0.22) !important;
}

[data-testid="stChatInput"] textarea {
    color: #f8fafc !important;

    font-size: 14px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}


/* ============================================================
   SIDEBAR STATUS CARD
============================================================ */

.status-card {
    padding: 16px;

    border-radius: 17px;

    background:
        linear-gradient(
            145deg,
            rgba(9, 28, 53, 0.80),
            rgba(7, 18, 38, 0.80)
        );

    border: 1px solid rgba(34, 211, 238, 0.12);

    margin-top: 14px;
}

.status-row {
    display: flex;
    align-items: center;

    gap: 9px;

    color: #9fb0ca;

    font-size: 12px;

    margin: 9px 0;
}

.status-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 10px rgba(34, 197, 94, 0.75);
}


/* ============================================================
   SIDEBAR INPUTS
============================================================ */

div[data-baseweb="select"] > div {
    background: rgba(7, 20, 40, 0.75) !important;

    border-color: rgba(120, 160, 255, 0.14) !important;

    border-radius: 11px !important;
}

[data-testid="stFileUploader"] {
    background: rgba(7, 20, 40, 0.55);

    border-radius: 15px;

    border: 1px solid rgba(120, 160, 255, 0.08);
}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {
    width: 100%;

    min-height: 42px;

    border-radius: 12px;

    border: 1px solid rgba(103, 232, 249, 0.17);

    background:
        linear-gradient(
            135deg,
            rgba(14, 165, 233, 0.10),
            rgba(124, 58, 237, 0.10)
        );

    color: #dffaff;

    font-weight: 650;

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);

    border-color: rgba(103, 232, 249, 0.55);

    box-shadow:
        0 0 20px rgba(34, 211, 238, 0.12);

    color: #ffffff;
}


/* ============================================================
   DIVIDERS
============================================================ */

hr {
    border-color: rgba(148, 163, 184, 0.08) !important;
}


/* ============================================================
   SCROLLBAR
============================================================ */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #030712;
}

::-webkit-scrollbar-thumb {
    background: #1e3a5f;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #2563eb;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {
    text-align: center;

    color: #52627d;

    font-size: 11px;

    padding: 20px 0 5px 0;
}

.footer span {
    color: #67e8f9;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 768px) {

    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 25px 22px;
        border-radius: 21px;
    }

    .hero-title {
        font-size: 36px;
        letter-spacing: -1.5px;
    }

    .hero-subtitle {
        font-size: 13px;
    }

    .feature-card {
        margin-bottom: 10px;
    }

    .chat-panel {
        padding: 10px;
        border-radius: 19px;
    }

    [data-testid="stChatMessage"] {
        padding: 7px !important;
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

    st.markdown(
        """
        <div class="sidebar-logo">

            <div class="sidebar-logo-icon">🎓</div>

            <div class="sidebar-logo-title">
                Study Tutor AI
            </div>

            <div class="sidebar-logo-subtitle">
                Your intelligent study companion
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

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


    st.markdown("---")

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


    st.markdown("---")

    st.markdown("### 🧠 Session Memory")

    message_count = len(
        st.session_state.memory
    )

    if message_count:

        st.markdown(
            f"""
            <div class="status-card">

                <div class="status-row">
                    <span class="status-dot"></span>
                    {message_count} messages remembered
                </div>

                <div class="status-row">
                    📄 Study material:
                    {"Loaded" if st.session_state.study_material else "Not loaded"}
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


    st.markdown("")

    if st.button("🗑️ Clear Conversation"):

        st.session_state.memory = []

        st.rerun()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-content">

            <div class="hero-badge">
                ✦ AI-POWERED LEARNING
            </div>

            <h1 class="hero-title">
                Study smarter.<br>
                Understand deeper.
            </h1>

            <p class="hero-subtitle">
                Your personal AI tutor for explanations,
                practice, questions, and learning.
                Upload your notes, ask questions,
                and learn at your own pace.
            </p>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">💡</div>

            <div class="feature-title">
                Understand Concepts
            </div>

            <div class="feature-description">
                Get difficult topics explained
                in simple, student-friendly language.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">📚</div>

            <div class="feature-title">
                Learn From Your Notes
            </div>

            <div class="feature-description">
                Upload your study material and
                ask questions about what you're learning.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">🧠</div>

            <div class="feature-title">
                Personalized Tutoring
            </div>

            <div class="feature-description">
                Your tutor remembers the current
                conversation and adapts to your level.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT SECTION
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            💬 Ask Your Tutor
        </div>

        <div class="section-caption">
            AI-powered learning workspace
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CHAT PANEL
# ============================================================

st.markdown(
    '<div class="chat-panel">',
    unsafe_allow_html=True,
)


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.memory:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


st.markdown(
    "</div>",
    unsafe_allow_html=True,
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

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        Study Tutor AI
        <span>•</span>
        Powered by CrewAI + Groq
        <span>•</span>
        Learn. Practice. Understand.
    </div>
    """,
    unsafe_allow_html=True,
)
