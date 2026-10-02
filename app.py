import os
import streamlit as st

from agent import ask_tutor


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
    .stApp {
        background: #f6f8fc;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.5px;
    }

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.7rem;
    }

    [data-testid="stChatInput"] {
        border-radius: 16px;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 12px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px;
    }

    .stButton > button {
        border-radius: 10px;
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

if "study_material_name" not in st.session_state:
    st.session_state.study_material_name = ""


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_message(role, content):
    st.session_state.memory.append(
        {
            "role": role,
            "content": content,
        }
    )


def get_memory_text():
    if not st.session_state.memory:
        return ""

    conversation = []

    for message in st.session_state.memory:
        role = message["role"].capitalize()
        content = message["content"]

        conversation.append(
            f"{role}: {content}"
        )

    return "\n".join(conversation)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎓 Study Tutor AI")
    st.caption("Your intelligent study companion")

    st.divider()

    # --------------------------------------------------------
    # STUDY MATERIAL
    # --------------------------------------------------------

    st.subheader("📚 Study Material")

    uploaded_file = st.file_uploader(
        "Upload study material",
        type=["txt", "md"],
        help="Upload TXT or Markdown study material.",
    )

    if uploaded_file is not None:

        try:
            text = uploaded_file.read().decode("utf-8")

            st.session_state.study_material = text
            st.session_state.study_material_name = uploaded_file.name

            st.success("Study material loaded.")

        except Exception as e:
            st.error("Could not read the uploaded file.")

            with st.expander("Technical details"):
                st.code(str(e))

    if st.session_state.study_material:

        st.caption(
            f"📄 {st.session_state.study_material_name}"
        )

        st.metric(
            "Characters",
            len(st.session_state.study_material),
        )

    else:

        st.info(
            "No study material loaded yet."
        )

    st.divider()

    # --------------------------------------------------------
    # TUTOR SETTINGS
    # --------------------------------------------------------

    st.subheader("⚙️ Tutor Settings")

    difficulty = st.selectbox(
        "Learning level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
        index=0,
    )

    response_style = st.selectbox(
        "Teaching style",
        [
            "Simple and clear",
            "Detailed explanation",
            "Step-by-step",
            "Example-based",
        ],
        index=0,
    )

    st.divider()

    # --------------------------------------------------------
    # SESSION MEMORY
    # --------------------------------------------------------

    st.subheader("🧠 Session Memory")

    message_count = len(st.session_state.memory)

    if message_count > 0:

        st.success(
            f"{message_count} messages remembered"
        )

        material_status = (
            "Loaded"
            if st.session_state.study_material
            else "Not loaded"
        )

        st.caption(
            f"📄 Study material: {material_status}"
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
# HERO SECTION
# ============================================================

with st.container(border=True):

    st.caption("✦ AI-POWERED LEARNING")

    st.title("Study smarter. Understand deeper.")

    st.write(
        "Your personal AI tutor for explanations, practice, "
        "questions, and learning — powered by CrewAI and Groq."
    )


st.write("")


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.markdown("### 💡 Understand Concepts")

        st.caption(
            "Get difficult topics explained in simple, "
            "student-friendly language."
        )


with col2:

    with st.container(border=True):

        st.markdown("### 🧮 Solve Problems")

        st.caption(
            "Work through calculations and academic "
            "problems step by step."
        )


with col3:

    with st.container(border=True):

        st.markdown("### 📚 Study Material")

        st.caption(
            "Ask questions about your uploaded study "
            "material."
        )


st.write("")
st.divider()


# ============================================================
# CHAT SECTION
# ============================================================

st.subheader("💬 Ask Your Tutor")

st.caption(
    "Ask questions, explore concepts, and learn step by step."
)


with st.container(border=True):

    if not st.session_state.memory:

        st.markdown("### 🎓 Ready when you are")

        st.caption(
            "Ask your first question below. "
            "Your tutor can explain concepts, work through "
            "problems, and use your uploaded study material."
        )

    else:

        for message in st.session_state.memory:

            with st.chat_message(message["role"]):

                st.markdown(
                    message["content"]
                )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask anything about your studies..."
)


# ============================================================
# TUTOR AGENT
# ============================================================

if question:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)

    add_message(
        "user",
        question,
    )

    # --------------------------------------------------------
    # CONVERSATION MEMORY
    # --------------------------------------------------------

    conversation = get_memory_text()

    # --------------------------------------------------------
    # TUTOR CONTEXT
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
    # ASSISTANT RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 Your tutor is thinking..."
        ):

            try:

                answer = ask_tutor(
                    question=enhanced_question,
                    study_material=st.session_state.study_material,
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

                    st.code(
                        str(e)
                    )

    # --------------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # --------------------------------------------------------

    add_message(
        "assistant",
        answer,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎓 Study Tutor AI • Powered by CrewAI + Groq"
)
