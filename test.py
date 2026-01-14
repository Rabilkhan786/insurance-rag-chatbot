# from src.rag.Pdf_extractor import PDFExtractor

# extractor = PDFExtractor()
# docs = extractor.extract_all("D:\Virtual_Insurnace_Ai_Agent\Data\insurance_documents")

# print(len(docs))
# print(docs[0].page_content[:200])
# print(docs[0].metadata)


# from src.rag.Vectorstore import VectorStoreManager

# # 1. Load the vector store (class method)
# vector_store = VectorStoreManager.load_vectorstore(
#     r"D:\Virtual_Insurnace_Ai_Agent\faiss_insurance_index\faiss_index"
# )

# print(" Vector store loaded")

# # 2. Run a similarity search
# query = "What does health insurance cover?"
# results = vector_store.similarity_search(query, k=3)

# print(f"\n Query: {query}\n")

# for i, doc in enumerate(results, start=1):
#     print(f"Result {i}:")
#     print(doc.page_content[:300])  # first 300 chars
#     print("Metadata:", doc.metadata)
#     print("-" * 50)



# 1. Get the model

# from src.llm.groq_llm import groq_model
# from src.rag.Vectorstore import VectorStoreManager
# llm = groq_model()

# response = llm.invoke("where is india?")
# print(response.content)

# from src.rag.chain import chain

# rag = chain()

# response = rag.invoke({
#     "question": "What does health insurance cover?",
#     "chat_history": []
# })

# print(response)

# from src.rag.chain import build_chat_chain
# from src.memory.session_memory import get_or_create_session_id

# chat = build_chat_chain()

# session_id = get_or_create_session_id(None)

# response = chat.invoke(
#     {"question": "What does health insurance cover?"},
#     config={"configurable": {"session_id": session_id}}
# )

# print(response)
# from src.audio.speech_to_text import record_audio, audio_to_text
# from src.rag.chain import build_chat_chain
# from src.memory.session_memory import get_or_create_session_id

# # 1. Record audio
# record_audio(duration=5)

# # 2. Convert to text
# question = audio_to_text()
# print("User said:", question)

# # 3. Ask RAG
# from src.rag.chain import build_chat_chain
# from src.memory.session_memory import get_or_create_session_id
# from src.audio.speech_to_text import  audio_to_text


# chat = build_chat_chain()
# session_id = get_or_create_session_id(None)


# question = audio_to_text()

# print("Asking:", question)

# response = chat.invoke(
#     {"question": question},
#     config={"configurable": {"session_id": session_id}}
# )

# print("Assistant response:")
# print(response)



# from src.audio.speech_to_text import record_audio

# record_audio(duration=5)

# from src.llm.groq_llm import groq_model
# model = groq_model()

# result = model.invoke("where is tamilnadu")
# print(result.content)