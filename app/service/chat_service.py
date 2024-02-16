import re
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain_core.documents import Document
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate


def load_doc(doc_dir: str):

    loader = DirectoryLoader(doc_dir, loader_cls=UnstructuredMarkdownLoader)
    docs = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=256, chunk_overlap=50)
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
    n_ctx = 2048
    max_token = 0
    # model_path = r'weight/llama-2-7b-chat.Q5_0.gguf'
    model_path = r'weight/chinese-alpaca-2-7b.Q5_0.gguf'
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(
        model_path=model_path,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        n_ctx=n_ctx,
        f16_kv=
        True,  # MUST set to True, otherwise you will run into problem after a couple of calls
        callback_manager=callback_manager,
        max_token=max_token,
        temperature=0.2,
        verbose=False,
    )

    return llm


def build_conversation(llm: LlamaCpp,
                       retriever) -> ConversationalRetrievalChain:

    # 1. 定義 Prompt
    system_template = r"""
    你現在是一個擁有10年經驗的創意料理家, 請根據下面的資訊給出一個簡短的答案, 並使用中文回答, 如果不知道的話就回答「窩不知道 peko」
    --------------
    {context}
    --------------
    """
    human_template = r"""
    問題: {question}
    回答:"""

    # 2. 設定聊天模板
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=ConversationBufferMemory(memory_key='chat_history'),
        combine_docs_chain_kwargs={'prompt': qa_prompt},
        chain_type="stuff",
        get_chat_history=lambda h: h,
        return_source_documents=False)

    return qa


def build_chatbot(llm: LlamaCpp) -> ConversationalRetrievalChain:

    # NOTE: 2024-02-06 暫時拿掉文本搜尋
    # 1. 載入資料（知識文本）
    doc_dir = r'data/recipe'
    docs = load_doc(doc_dir)

    # 2. 建立 Embedding Model
    embedding_model_path = r'shibing624/text2vec-base-chinese'
    embedding_model = build_embedding(embedding_model_path)

    # 3. 建立向量資料庫
    qdrant_url = r'http://localhost:6333'
    collection_name = 'recipe'
    doc_store = build_docstore(qdrant_url, docs, collection_name,
                               embedding_model)

    # 4. 建立有記憶的對話式問答
    conversation = build_conversation(llm, doc_store.as_retriever())

    return conversation


def extract_answer(output: str) -> str:

    # 1. 比對輸出的文字
    # NOTE: Chinese-Alpana-2 是依據 llama2-prompt 模板訓練的，輸出的角色 prefix 目前已知有可能是 Answer, ChatGPT, Output, System
    matches = [
        _ for _ in re.finditer(r'(Answer|ChatGPT|Output|System): ', output)
    ]

    # 2. 擷取 AI 角色回覆的文字
    if matches:
        start = matches[-1].end() if len(matches) == 1 else matches[-2].end()
        end = len(output) if len(matches) == 1 else matches[-1].start()
        output = output[start:end]

    # 3. 處理換行符號
    output = output.replace('\\n', '\n')
    output = output.replace('\n\n', '\n')
    if output.startswith('\n\n'):
        output = output[2:]

    return output
