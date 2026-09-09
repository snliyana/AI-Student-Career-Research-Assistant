from backend.app.graph.state import GraphState
from backend.app.llm.groq_llm import llm_groq
from backend.app.memory.long_term_memory import get_all_memories


def collector_node(state: GraphState) -> GraphState:

    # =====================================================
    # GET STATE DATA
    # =====================================================

    user_query = state["query"]

    results = state.get(
        "results",
        []
    )

    # =====================================================
    # SHORT-TERM MEMORY
    # =====================================================

    chat_history = state.get(
        "chat_history",
        []
    )

    # =====================================================
    # LONG-TERM MEMORY
    # =====================================================

    user_id = state.get(
        "user_id",
        "default_user"
    )

    long_term_memory = get_all_memories(
        user_id
    )

    # =====================================================
    # COMBINE WORKER RESULTS
    # =====================================================

    if results:

        combined_results = "\n\n".join(
            [
                f"Result {i + 1}:\n{result}"
                for i, result in enumerate(results)
            ]
        )

    else:

        combined_results = (
            "No worker/tool results were available."
        )

    # =====================================================
    # COLLECTOR PROMPT
    # =====================================================

    prompt = f"""
You are the final response collector for an
AI Student Career & Research Assistant.

Your job is to combine the worker/tool results into
one accurate, clear, useful final answer.

=====================================================
LONG-TERM USER MEMORY
=====================================================

{long_term_memory}

=====================================================
SHORT-TERM CONVERSATION HISTORY
=====================================================

{chat_history}

=====================================================
CURRENT USER QUERY
=====================================================

{user_query}

=====================================================
WORKER / TOOL RESULTS
=====================================================

{combined_results}

=====================================================
INSTRUCTIONS
=====================================================

Answer the CURRENT USER QUERY using the worker/tool
results provided above.

GENERAL RULES:

- Focus on the user's current request.
- Combine relevant worker results into one coherent answer.
- Do not repeat the same information unnecessarily.
- Keep the response clear and practical.
- Prefer concise explanations.
- Keep the final response under approximately 700 words.
- Use long-term memory only when it is relevant.
- Use short-term conversation history only when it is relevant.
- Personalize the response when relevant user information is available.

=====================================================
GROUNDING RULES
=====================================================

The worker/tool results are the factual source for
external or time-sensitive information.

For information about:

- current jobs
- job vacancies
- hiring companies
- salaries
- stock prices
- finance
- exchange rates
- weather
- news
- company information
- current market information
- current events

follow these rules strictly:

1. Use only facts explicitly supported by the
   worker/tool results.

2. Do NOT invent or assume:
   - company names
   - job titles
   - job vacancies
   - posting dates
   - locations
   - salaries
   - stock prices
   - statistics
   - exchange rates
   - weather values
   - URLs or links
   - source names
   - dates
   - certifications
   - technologies allegedly required by a specific employer

3. If a detail is not available in the worker/tool
   results, say that the detail was not available.

4. Do NOT claim information is:
   - "current"
   - "latest"
   - "live"
   - "real-time"
   - "posted today"
   - "posted this week"
   - "posted within the last X days"

   unless the worker/tool result explicitly supports
   that statement.

5. Never create fake links.

6. Never create a job listing that is not present
   in the worker/tool results.

7. If the search results are incomplete, clearly
   state that the available search results are limited.

8. When different worker results conflict, do not
   silently choose one. Mention the uncertainty.

=====================================================
CAREER & LEARNING ROADMAP RULES
=====================================================

For career guidance and learning roadmaps:

- You may organize supported information into
  practical steps.
- Clearly distinguish researched facts from
  recommendations.
- Do not claim that a specific company requires a
  skill unless the worker/tool result says so.
- General learning recommendations may be provided
  when they logically follow from the identified skills.
- Avoid unrealistic guarantees about employment,
  salary, or career outcomes.

=====================================================
FORMATTING RULES
=====================================================

- Use clean Markdown only.
- Do NOT use HTML.
- Never use:
  <br>
  <br/>
  <br />
  <div>
  <span>
  <p>

- Prefer clear headings and bullet points.
- Use numbered steps for roadmaps when appropriate.
- Use tables only when they genuinely improve readability.
- Keep tables small and simple.
- Keep table cells short.
- Avoid long bullet lists inside table cells.
- Avoid very wide tables.
- For detailed comparisons, prefer separate sections
  rather than a large table.
- Do not include unnecessary introductions.
- Do not include unnecessary conclusions.

=====================================================
FINAL CHECK
=====================================================

Before producing the answer, check:

- Did I answer the user's actual question?
- Are current factual claims supported by tool results?
- Did I accidentally invent a company, job, salary,
  date, link, statistic, or other factual detail?
- Did I clearly distinguish recommendations from
  researched facts?
- Is the response readable in Streamlit Markdown?

Now produce the final answer.
"""

    # =====================================================
    # CALL LLM
    # =====================================================

    response = llm_groq.invoke(
        prompt
    )

    # =====================================================
    # CLEAN FINAL RESPONSE
    # =====================================================

    final_response = response.content

    # Remove unwanted HTML line breaks
    final_response = final_response.replace(
        "<br>",
        " "
    )

    final_response = final_response.replace(
        "<br/>",
        " "
    )

    final_response = final_response.replace(
        "<br />",
        " "
    )

    # =====================================================
    # SAVE FINAL SUMMARY
    # =====================================================

    state["summary"] = final_response

    # =====================================================
    # UPDATE SHORT-TERM MEMORY
    # =====================================================

    state["chat_history"] = (
        chat_history
        + [
            {
                "role": "user",
                "content": user_query
            },
            {
                "role": "assistant",
                "content": final_response
            }
        ]
    )

    # =====================================================
    # RETURN UPDATED STATE
    # =====================================================

    return state