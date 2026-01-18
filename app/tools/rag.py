from typing import List, Tuple, Dict, Iterable
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import hashlib
from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
import os
from app.core.settings import settings

HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]
INDEX_DIR = "app/data/rag_index_house"
DOC_PATHS = ["app/docs/index.md"]

os.makedirs(INDEX_DIR, exist_ok=True)

# chunk markdown text with headers preserved
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

# generate a unique ID for each text chunk
def _hash_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# load embedding instance
@lru_cache(maxsize=1)
def _embedding() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=settings.embedding_model)

# check if FAISS index exists
def _faiss_files_exist() -> bool:
    return (Path(INDEX_DIR) / "index.faiss").exists() and (Path(INDEX_DIR) / "index.pkl").exists()

# load FAISS vector store
def _load_faiss() -> FAISS:
    return FAISS.load_local(
        INDEX_DIR,
        embeddings=_embedding(),
        allow_dangerous_deserialization=True,
    )


def build_update_index(
    doc_paths: Iterable[str] = DOC_PATHS,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> None:
    texts: List[str] = []
    metadatas: List[dict] = []

    for p in doc_paths:
        path = Path(p)
        if not path.exists():
            continue
        md = path.read_text(encoding="utf-8")
        for content, meta in split_markdown_with_headers(md, chunk_size, chunk_overlap):
            m = {"path": str(path), **meta, "chunk_id": _hash_id(f"{path}::{content}")}
            texts.append(content)
            metadatas.append(m)
    if not texts:
        return
    vs = FAISS.from_texts(texts=texts, embedding=_embedding(), metadatas=metadatas)
    vs.save_local(INDEX_DIR)

# retrieve context
def retrieve_context(question: str, k: int, max_chars: int) -> str:
    if not _faiss_files_exist():
        build_update_index()
    vs = _load_faiss()
    docs = vs.similarity_search(question, k=k)
    ctx = "\n\n---\n\n".join(d.page_content for d in docs)
    return ctx[:max_chars]
