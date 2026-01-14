def safe_chat_invoke(chat_chain, question, session_id):
    """
    Safely invoke a LangChain Runnable with session memory.
    Always returns a predictable dict:
    {
        "answer": str | None,
        "error": str | None
    }
    """
    try:
        response = chat_chain.invoke(
            {"question": question},
            config={"configurable": {"session_id": session_id}}
        )

        # Normalize response (AIMessage -> string)
        answer = response.content if hasattr(response, "content") else str(response)

        return {
            "answer": answer,
            "error": None
        }

    except Exception as e:
        error_msg = str(e).lower()

        if "rate limit" in error_msg:
            return {
                "answer": None,
                "error": "I'm temporarily busy due to high usage. Please try again shortly."
            }

        if "api key" in error_msg or "authentication" in error_msg:
            return {
                "answer": None,
                "error": "There is a configuration issue. Please try again later."
            }

        return {
            "answer": None,
            "error": "Something went wrong. Please try again."
        }
