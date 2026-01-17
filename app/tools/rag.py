from typing import List, Tuple, Dict, Iterable
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import hashlib
from functools import lru_cache
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from pathlib import Path
import os

HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]
INDEX_DIR = "app/data/rag_index_house"
DOC_PATHS = ["app/docs/index.md"]

os.makedirs(INDEX_DIR, exist_ok=True)

# 分割 md 文本
def split_markdown_with_headers(md_text:str, chunk_size:int, chunk_overlap:int) -> List[Tuple[str, Dict]]:
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS)
    header_docs = header_splitter.split_text(md_text)
    recursive_character_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n### ", "\n## ", "\n# ", "\n\n", "\n", " ", ""])
    chunks: List[Tuple[str, Dict]] = []
    for d in header_docs:
        meta = dict(d.metadata) if d.metadata else {}
        heading_path = " > ".join([meta[k] for k in ("h1", "h2", "h3") if k in meta])
        for c in recursive_character_splitter.split_text(d.page_content):
            chunks.append((c, {"source_heading_path": heading_path}))
    return chunks

# 每个文本块生成一个唯一 ID
def _hash_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# 加载embedding实例，仅初始化一次
@lru_cache(maxsize=1)
def _embedding() -> OllamaEmbeddings:
    return OllamaEmbeddings(model="nomic-embed-text")

# 构建一个新的 RAG 向量库实例
def _new_chroma() -> Chroma:
    return Chroma(
        collection_name="owd",
        embedding_function=_embedding(),
        persist_directory=INDEX_DIR,
    )

# 构造向量库
def build_update_index(doc_paths:Iterable[str] = DOC_PATHS, chunk_size:int = 500, chunk_overlap:int = 100) -> None:
    chroma = _new_chroma()
    texts: List[str] = []
    metadatas: List[dict] = []
    ids:List[str] = []
    for p in doc_paths:
        path = Path(p)
        if not path.exists():
            continue
        md = path.read_text(encoding="utf-8")
        for content, meta in split_markdown_with_headers(md, chunk_size, chunk_overlap):
            m = {"path": str(path), **meta}
            texts.append(content)
            metadatas.append(m)
            ids.append(_hash_id(f"{path}::{content}"))
    if texts:
        chroma.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        
# 检索相关上下文
def retrieve_context(question:str, k:int, max_chars:int) ->str:
    chroma = _new_chroma()
    docs = chroma.similarity_search(question, k=k)
    ctx = "\n\n---\n\n".join(d.page_content for d in docs)
    return ctx[:max_chars]
