from langchain_community.document_loaders import PyPDFDirectoryLoader, PyMuPDFLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
import os 
import glob


# import the .env file
from dotenv import load_dotenv
load_dotenv()

# configuration
DATA_PATH = "C:\\Users\\jojoo\\Downloads\\ksu-experience-project\\backend\\data1"
CHROMA_PATH = r"chroma_db"

# initiate the embeddings model
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# initiate the vector store
vector_store = Chroma(
    collection_name="ksu_collection",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

# loading the PDF document

# --- NEW LOADING LOGIC WITH OCR ---
raw_documents = []

# Find all PDF files in the target directory
pdf_files = glob.glob(os.path.join(DATA_PATH, "*.pdf"))

print(f"Found {len(pdf_files)} PDF(s) to parse...")

for pdf_path in pdf_files:
    print(f"Parsing {os.path.basename(pdf_path)} with OCR...")
    
    # PyMuPDF extracts regular text and feeds images through the RapidOCR parser
    loader = PyMuPDFLoader(
        file_path=pdf_path,
        mode="page",
        images_parser=RapidOCRBlobParser()
    )
    
    # Dynamically read and extend our raw documents list
    raw_documents.extend(loader.load())


###loader = PyPDFDirectoryLoader(DATA_PATH)
##raw_documents = loader.load()


# splitting the document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

# creating the chunks
chunks = text_splitter.split_documents(raw_documents)

# creating unique ID's
uuids = [str(uuid4()) for _ in range(len(chunks))]

# adding chunks to vector store
vector_store.add_documents(documents=chunks, ids=uuids)