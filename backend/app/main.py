from fastapi import FastAPI
from pydantic import BaseModel

from groq import RateLimitError, APIError

from backend.app.graph.workflow import app_graph

from backend.app.memory.chat_history import (
    create_conversation,
    save_message,
    get_recent_conversations,
    get_conversation_messages,
    delete_conversation,
    update_conversation_title,
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="AI Student Career & Research Assistant API",
    description=(
        "FastAPI backend for the AI-powered "
        "Student Career & Research Assistant."
    ),
    version="1.0.0",
)


# =========================================================
# REQUEST / RESPONSE SCHEMAS
# =========================================================

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    thread_id: str = "default_thread"


class ChatResponse(BaseModel):
    response: str


# =========================================================
# CHAT TITLE GENERATOR
# =========================================================

def generate_chat_title(message: str) -> str:
    """
    Generate a short readable title from
    the user's message without using an LLM.
    """

    text = message.strip()

    # Ignore PDF path added by frontend
    text = text.split(
        "\n\nPDF file path:"
    )[0].strip()

    lower_text = text.lower()

    # -----------------------------------------------------
    # Data Scientist
    # -----------------------------------------------------

    if "data scientist" in lower_text:

        if "roadmap" in lower_text:
            return "Data Scientist Roadmap"

        if "skill" in lower_text:
            return "Data Scientist Skills"

        if "salary" in lower_text:
            return "Data Scientist Salary"

        if "job" in lower_text:
            return "Data Scientist Jobs"

        return "Data Scientist Career"


    # -----------------------------------------------------
    # AI Engineer
    # -----------------------------------------------------

    if "ai engineer" in lower_text:

        if "roadmap" in lower_text:
            return "AI Engineer Roadmap"

        if "skill" in lower_text:
            return "AI Engineer Skills"

        if "salary" in lower_text:
            return "AI Engineer Salary"

        if "job" in lower_text:
            return "AI Engineer Jobs"

        return "AI Engineer Career"


    # -----------------------------------------------------
    # Machine Learning Engineer
    # -----------------------------------------------------

    if (
        "machine learning engineer" in lower_text
        or "ml engineer" in lower_text
    ):

        if "roadmap" in lower_text:
            return "ML Engineer Roadmap"

        if "skill" in lower_text:
            return "ML Engineer Skills"

        if "salary" in lower_text:
            return "ML Engineer Salary"

        if "job" in lower_text:
            return "ML Engineer Jobs"

        return "ML Engineer Career"


    # -----------------------------------------------------
    # Resume / Documents
    # -----------------------------------------------------

    if (
        "resume" in lower_text
        or "cv" in lower_text
    ):
        return "Resume Analysis"

    if (
        "pdf" in lower_text
        or "document" in lower_text
        or "summarize" in lower_text
        or "summary" in lower_text
    ):
        return "Document Analysis"


    # -----------------------------------------------------
    # Finance
    # -----------------------------------------------------

    if (
        "stock" in lower_text
        or "share price" in lower_text
    ):
        return "Stock Analysis"

    if (
        "currency" in lower_text
        or "convert" in lower_text
        or "exchange rate" in lower_text
    ):
        return "Currency Conversion"


    # -----------------------------------------------------
    # Weather
    # -----------------------------------------------------

    if "weather" in lower_text:
        return "Weather Search"


    # -----------------------------------------------------
    # Job / Company
    # -----------------------------------------------------

    if (
        "company" in lower_text
        or "companies" in lower_text
    ):
        return "Company Research"

    if (
        "job" in lower_text
        or "vacancy" in lower_text
        or "hiring" in lower_text
    ):
        return "Job Search"


    # -----------------------------------------------------
    # Salary
    # -----------------------------------------------------

    if "salary" in lower_text:
        return "Salary Research"


    # -----------------------------------------------------
    # General Fallback
    # -----------------------------------------------------

    title = text.split("\n")[0].strip()

    if len(title) > 40:
        title = (
            title[:40].rstrip()
            + "..."
        )

    if not title:
        title = "New Conversation"

    return title


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def root():

    return {
        "status": "running",
        "message": (
            "AI Student Career & Research Assistant API"
        )
    }


# =========================================================
# CHAT ENDPOINT
# =========================================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    # -----------------------------------------------------
    # Generate Conversation Title
    # -----------------------------------------------------

    title = generate_chat_title(
        request.message
    )

    # -----------------------------------------------------
    # Create / Update Conversation
    # -----------------------------------------------------

    create_conversation(
        thread_id=request.thread_id,
        user_id=request.user_id,
        title=title
    )

    update_conversation_title(
        thread_id=request.thread_id,
        title=title
    )

    # -----------------------------------------------------
    # Save User Message
    # -----------------------------------------------------

    save_message(
        thread_id=request.thread_id,
        role="user",
        content=request.message
    )

    # -----------------------------------------------------
    # LangGraph Configuration
    # -----------------------------------------------------

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    # -----------------------------------------------------
    # Initial Graph State
    # -----------------------------------------------------

    initial_state = {
        "query": request.message,
        "tasks": [],
        "results": [],
        "summary": "",
        "chat_history": [],
        "user_id": request.user_id,
    }

    # -----------------------------------------------------
    # Run LangGraph with Error Handling
    # -----------------------------------------------------

    try:

        result = app_graph.invoke(
            initial_state,
            config=config
        )

        assistant_response = (
            result["summary"]
        )

    except RateLimitError as e:

        print(
            f"Groq Rate Limit Error: {e}"
        )

        assistant_response = (
            "⚠️ The AI service has temporarily reached "
            "its usage limit. Please wait a few minutes "
            "and try again."
        )

    except APIError as e:

        print(
            f"Groq API Error: {e}"
        )

        assistant_response = (
            "⚠️ The AI service is temporarily unavailable. "
            "Please try again later."
        )

    except Exception as e:

        print(
            f"Application Error: {e}"
        )

        assistant_response = (
            "⚠️ Something went wrong while processing "
            "your request. Please try again."
        )

    # -----------------------------------------------------
    # Save Assistant Response
    # -----------------------------------------------------

    save_message(
        thread_id=request.thread_id,
        role="assistant",
        content=assistant_response
    )

    # -----------------------------------------------------
    # Return Response
    # -----------------------------------------------------

    return ChatResponse(
        response=assistant_response
    )


# =========================================================
# GET RECENT CONVERSATIONS
# =========================================================

@app.get(
    "/conversations/{user_id}"
)
def conversations(
    user_id: str
):

    return get_recent_conversations(
        user_id=user_id,
        limit=10
    )


# =========================================================
# LOAD ONE CONVERSATION
# =========================================================

@app.get(
    "/conversations/thread/{thread_id}"
)
def conversation_messages(
    thread_id: str
):

    return get_conversation_messages(
        thread_id=thread_id
    )


# =========================================================
# DELETE CONVERSATION
# =========================================================

@app.delete(
    "/conversations/{thread_id}"
)
def remove_conversation(
    thread_id: str
):

    delete_conversation(
        thread_id=thread_id
    )

    return {
        "status": "deleted",
        "thread_id": thread_id
    }