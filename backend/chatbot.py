import gradio as gr
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq


# import the .env file
from dotenv import load_dotenv
load_dotenv()

# configuration
DATA_PATH = "C:\\Users\\jojoo\\Downloads\\ksu-experience-project\\backend\\data1"
CHROMA_PATH = r"chroma_db"

# initiate the embeddings model
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# connect to the chromadb
vector_store = Chroma(
    collection_name="ksu_collection",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH, 
)

# Set up the vectorstore to be the retriever
num_results = 5
retriever = vector_store.as_retriever(search_kwargs={'k': num_results})

# call this function for every message added to the chatbot
def stream_response(message, history):
    #print(f"Input: {message}. History: {history}\n")

    # retrieve the relevant chunks based on the question asked
    docs = retriever.invoke(message)

    # add all the chunks to 'knowledge'
    knowledge = ""

    for doc in docs:
        knowledge += doc.page_content+"\n\n"


    # make the call to the LLM (including prompt)
    if message is not None:

        partial_message = ""

        rag_prompt = f"""
        You are an assistant which ONLY ANSWERS QUESTIONS based on knowledge which is provided to you.
        While answering, you don't use your internal knowledge, 
        You only use the information in the "The knowledge" section to answer the question.
        You don't mention anything to the user about the provided knowledge.
        Additionally, you are to only answer questions, not make suggestions nor provide any additional information.
        If the question is not really a question such as, "Hello", be polite and specify that you should only be asked questions.
        Lastly, if you are unsure about the answer, you should say so rather than guessing.

        The question: {message}

        Conversation history: {history}

        The knowledge: {knowledge}

        """

        #print(rag_prompt)

        # stream the response to the Gradio App
        for response in llm.stream(rag_prompt):
            partial_message += response.content
            yield partial_message


demo = gr.ChatInterface(
    fn=stream_response,
    title="Python Chatbot Backend"
)

demo.launch()