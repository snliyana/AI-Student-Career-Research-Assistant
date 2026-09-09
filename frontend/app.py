import streamlit as st
import requests
import uuid
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Student Career & Research Assistant",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# API CONFIGURATION
# =========================================================

BASE_API_URL = "https://ai-student-career-research-assistant.onrender.com"
CHAT_API_URL = f"{BASE_API_URL}/chat"


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "user_id" not in st.session_state:
    st.session_state.user_id = "student_001"

if "uploaded_pdf_path" not in st.session_state:
    st.session_state.uploaded_pdf_path = None


# =========================================================
# FUNCTIONS
# =========================================================

def start_new_conversation():
    """
    Start a fresh conversation.

    This clears the current UI conversation
    but does not delete long-term memory.
    """

    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.uploaded_pdf_path = None


def get_recent_chats():
    """
    Get recent conversations from FastAPI.
    """

    try:

        response = requests.get(
            f"{BASE_API_URL}/conversations/"
            f"{st.session_state.user_id}",
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return []

    except requests.exceptions.RequestException:
        return []


def load_conversation(thread_id):
    """
    Load an old conversation from FastAPI.
    """

    try:

        response = requests.get(
            f"{BASE_API_URL}/conversations/thread/"
            f"{thread_id}",
            timeout=10
        )

        if response.status_code == 200:

            stored_messages = response.json()

            st.session_state.messages = [
                {
                    "role": message["role"],
                    "content": message["content"]
                }
                for message in stored_messages
            ]

            st.session_state.thread_id = thread_id

            # Do not carry PDF from another chat
            st.session_state.uploaded_pdf_path = None

            return True

        return False

    except requests.exceptions.RequestException:
        return False


def delete_chat(thread_id):
    """
    Delete a conversation through FastAPI.
    """

    try:

        response = requests.delete(
            f"{BASE_API_URL}/conversations/{thread_id}",
            timeout=10
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 Career Assistant")

    st.write(
        "AI-powered career and research assistant "
        "using LangGraph Orchestrator–Worker architecture."
    )

    st.divider()

    # -----------------------------------------------------
    # New Conversation
    # -----------------------------------------------------

    if st.button(
        "＋ New Conversation",
        use_container_width=True,
        type="primary"
    ):

        start_new_conversation()
        st.rerun()


    # -----------------------------------------------------
    # Recent Chats
    # -----------------------------------------------------

    st.subheader("💬 Recent Chats")

    recent_chats = get_recent_chats()

    if recent_chats:

        for chat in recent_chats:

            thread = chat["thread_id"]
            title = chat["title"]

            # Shorten long titles
            display_title = title

            if len(display_title) > 26:
                display_title = (
                    display_title[:26] + "..."
                )

            # Conversation + delete button
            col_chat, col_delete = st.columns(
                [5, 1]
            )

            with col_chat:

                if st.button(
                    display_title,
                    key=f"chat_{thread}",
                    use_container_width=True,
                    help=title
                ):

                    loaded = load_conversation(
                        thread
                    )

                    if loaded:
                        st.rerun()

                    else:
                        st.error(
                            "Could not load conversation."
                        )

            with col_delete:

                if st.button(
                    "🗑️",
                    key=f"delete_{thread}",
                    help="Delete conversation"
                ):

                    deleted = delete_chat(
                        thread
                    )

                    if deleted:

                        # If user deleted currently opened chat,
                        # automatically create a new conversation.
                        if (
                            st.session_state.thread_id
                            == thread
                        ):

                            start_new_conversation()

                        st.rerun()

                    else:

                        st.error(
                            "Could not delete conversation."
                        )

    else:

        st.caption(
            "No recent conversations yet."
        )


    # -----------------------------------------------------
    # Session Information
    # -----------------------------------------------------

    st.divider()

    with st.expander(
        "⚙️ Session"
    ):

        st.text_input(
            "User ID",
            key="user_id"
        )

        st.caption(
            f"Thread ID: "
            f"{st.session_state.thread_id[:8]}..."
        )


    # -----------------------------------------------------
    # PDF Upload
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "📄 Document"
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:

        os.makedirs(
            "data/uploads",
            exist_ok=True
        )

        upload_path = os.path.join(
            "data",
            "uploads",
            uploaded_file.name
        )

        with open(
            upload_path,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        st.session_state.uploaded_pdf_path = (
            upload_path
        )


    # -----------------------------------------------------
    # Current PDF
    # -----------------------------------------------------

    if st.session_state.uploaded_pdf_path:

        file_name = os.path.basename(
            st.session_state.uploaded_pdf_path
        )

        st.caption(
            f"📎 {file_name}"
        )

        if st.button(
            "Remove Document",
            use_container_width=True
        ):

            st.session_state.uploaded_pdf_path = None

            st.rerun()


    # -----------------------------------------------------
    # Available Tools
    # -----------------------------------------------------

    st.divider()

    with st.expander(
        "🛠️ Available Tools"
    ):

        st.markdown(
            """
- 🔎 Web Search
- 📚 Wikipedia
- 📰 News Search
- 💰 Finance / Stock
- 🌤️ Weather
- 🧮 Calculator
- 💱 Currency Converter
- 🐍 Python / Data Analysis
- 💼 Career Analysis
- 🔍 Job / Company Search
- 📄 PDF Reader
- 🧠 Short-Term Memory
- 🗃️ Long-Term Memory
"""
        )


# =========================================================
# MAIN HEADER
# =========================================================

st.title(
    "🎓 AI Student Career & Research Assistant"
)

st.caption(
    "Research careers, explore jobs, compare salaries, "
    "analyze companies, use tools, and build "
    "personalized learning roadmaps."
)


# =========================================================
# SUGGESTED QUESTIONS
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        "##### Try asking:"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "• What skills do I need to become "
            "a Data Scientist in Malaysia?"
        )

        st.markdown(
            "• Find current AI Engineer jobs "
            "in Malaysia."
        )

    with col2:

        st.markdown(
            "• Convert 5000 SGD to MYR."
        )

        st.markdown(
            "• What is the weather "
            "in Kuala Lumpur?"
        )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_message = st.chat_input(
    "Ask about careers, jobs, companies, salary, "
    "skills, finance, weather, documents..."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_message:

    # -----------------------------------------------------
    # Save User Message in UI
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # -----------------------------------------------------
    # Display User Message
    # -----------------------------------------------------

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_message
        )


    # -----------------------------------------------------
    # Prepare Backend Message
    # -----------------------------------------------------

    message_to_send = user_message

    if st.session_state.uploaded_pdf_path:

        message_to_send += (
            "\n\nPDF file path: "
            f"{st.session_state.uploaded_pdf_path}"
        )


    # -----------------------------------------------------
    # Assistant Response
    # -----------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Thinking, planning and using tools..."
        ):

            try:

                payload = {
                    "message": message_to_send,
                    "user_id": (
                        st.session_state.user_id
                    ),
                    "thread_id": (
                        st.session_state.thread_id
                    )
                }

                response = requests.post(
                    CHAT_API_URL,
                    json=payload,
                    timeout=180
                )

                if response.status_code == 200:

                    data = response.json()

                    assistant_message = (
                        data["response"]
                    )

                else:

                    assistant_message = (
                        "Backend error: "
                        f"{response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                assistant_message = (
                    "Could not connect to the "
                    "FastAPI backend. Please make "
                    "sure the backend is running."
                )

            except requests.exceptions.Timeout:

                assistant_message = (
                    "The request took too long. "
                    "Please try again."
                )

            except Exception as e:

                assistant_message = (
                    f"Unexpected error: {str(e)}"
                )


        # -------------------------------------------------
        # Display Assistant Response
        # -------------------------------------------------

        st.markdown(
            assistant_message
        )


    # -----------------------------------------------------
    # Save Assistant Message in UI
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )


    # -----------------------------------------------------
    # Refresh Recent Chats
    # -----------------------------------------------------

    st.rerun()