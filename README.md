# Banking Loan Document Review Assistant

An AI-powered banking document review assistant using RAG, FAISS, BM25 hybrid search, and Qwen3 through Ollama.

## Features

- PDF document upload
- PDF text extraction
- OCR support for scanned documents
- Intelligent document chunking
- Semantic search using embeddings
- FAISS vector database
- BM25 keyword search
- Hybrid intelligent search
- Retrieval-Augmented Generation (RAG)
- Local Qwen3 LLM using Ollama
- Evidence-based answers with document and page references

## Architecture

PDF
→ Text Extraction / OCR
→ Chunking
→ Embeddings
→ FAISS
→ BM25
→ Hybrid Search
→ RAG
→ Qwen3 / Ollama
→ Answer + Evidence

## Technologies

- Python
- Streamlit
- PyMuPDF
- Sentence Transformers
- FAISS
- BM25
- Ollama
- Qwen3
- NumPy
- Pytesseract

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv