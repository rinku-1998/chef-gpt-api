from app.db.message_entity import MessageEntity
from app.enum.role import Role
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain, ConversationChain, LLMChain
from langchain.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain_core.documents import Document


def load_doc(doc_dir: str):

    loader = DirectoryLoader(doc_dir, loader_cls=UnstructuredMarkdownLoader)
    docs = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(docs)

    return docs


def build_embedding(model_path: str) -> HuggingFaceEmbeddings:

    model_kwargs = {'device': 'mps'}
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceEmbeddings(model_name=model_path,
                                       model_kwargs=model_kwargs,
                                       encode_kwargs=encode_kwargs)

    return embeddings


def build_docstore(url: str, docs: list[Document], collection_name: str,
                   embeddings: HuggingFaceEmbeddings) -> list[Document]:

    doc_store = Qdrant.from_documents(docs,
                                      embeddings,
                                      url=url,
                                      collection_name=collection_name,
                                      force_recreate=True)

    return doc_store


def build_llm() -> LlamaCpp:

    n_gpu_layers = 32
    n_batch = 512
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    model_path = r'weight/Taiwan-LLM-7B-v2.0-chat-Q5_1.gguf'
    # model_path = r'mistralai/Mistral-7B-v0.1'

    llm = LlamaCpp(
        model_path=model_path,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        n_ctx=4096,
        f16_kv=
        True,  # MUST set to True, otherwise you will run into problem after a couple of calls
        callback_manager=callback_manager,
        max_token=3000,
        verbose=False,
    )

    return llm


def build_conversation(llm: LlamaCpp) -> ConversationalRetrievalChain:

    conversation = ConversationChain(
        llm=llm, memory=ConversationBufferMemory(return_messages=True))

    return conversation


def build_chatbot(llm: LlamaCpp) -> ConversationalRetrievalChain:

    # NOTE: 2024-02-06 暫時拿掉文本搜尋
    # 1. 載入資料（知識文本）
    # doc_dir = r'data/recipe'
    # docs = load_doc(doc_dir)

    # # 2. 建立 Embedding Model
    # # embedding_model_path = r'sentence-transformers/all-MiniLM-L6-v2'
    # embedding_model_path = r'shibing624/text2vec-base-chinese'
    # embedding_model = build_embedding(embedding_model_path)

    # # 3. 建立向量資料庫
    # qdrant_url = r'http://localhost:6333'
    # collection_name = 'recipe'
    # doc_store = build_docstore(qdrant_url, docs, collection_name,
    #                            embedding_model)

    # 4. 建立有記憶的對話式問答
    conversation = build_conversation(llm)

    return conversation
