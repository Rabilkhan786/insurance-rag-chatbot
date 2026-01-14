from .Vectorstore import VectorStoreManager
from .prompt import get_prompt
from src.llm.groq_llm import groq_model
from src.memory.session_memory import get_session_history


def build_rag_chain():
    try:
        from langchain_core.output_parsers import StrOutputParser # Converts output to string
    except Exception as e:
        raise ImportError(
            "langchain_core is required. Please install langchain-core."
        ) from e

    vectorstore = VectorStoreManager.load_vectorstore(
    "faiss_insurance_index/faiss_index"
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 3,
            "fetch_k": 10,
            "lambda_mult": 0.7
        }
    )

    prompt = get_prompt()
    llm = groq_model()

    return (
        {
            "context": lambda x: "\n\n".join(
                doc.page_content for doc in retriever.invoke(x["question"])
            ),
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("chat_history", [])
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def build_chat_chain():
    rag_chain = build_rag_chain()

    try:
        from langchain_core.runnables import RunnableWithMessageHistory
    except Exception as e:
        raise ImportError(
            "RunnableWithMessageHistory requires langchain-core."
        ) from e

    return RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
