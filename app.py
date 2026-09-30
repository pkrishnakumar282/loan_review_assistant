import os
import shutil

import streamlit as st

from config import (
    UPLOAD_DIR,
    VECTOR_DIR
)

from src.document_loader import (
    extract_text_from_pdf
)

from src.chunker import (
    create_chunks
)

from src.vector_store import (
    VectorStore
)

from src.hybrid_search import (
    HybridSearch
)

from src.rag import (
    answer_question
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Banking Loan Document Review Assistant",
    page_icon="🏦",
    layout="wide"
)


# ============================================================
# DIRECTORIES
# ============================================================

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    VECTOR_DIR,
    exist_ok=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "vector_store" not in st.session_state:

    st.session_state.vector_store = None


if "search_engine" not in st.session_state:

    st.session_state.search_engine = None


if "chunks" not in st.session_state:

    st.session_state.chunks = []


if "documents" not in st.session_state:

    st.session_state.documents = []


# ============================================================
# HEADER
# ============================================================

st.title(
    "🏦 Banking Loan Document Review Assistant"
)

st.caption(
    "RAG + FAISS + Hybrid Search + Qwen3/Ollama"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📄 Document Upload")

    uploaded_files = st.file_uploader(
        "Upload loan documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    process_documents = st.button(
        "🔄 Process Documents",
        use_container_width=True
    )

    st.divider()

    st.info(
        """
        Supported pipeline:

        PDF → Text/OCR → Chunking
        → Embeddings → FAISS
        → BM25 → Hybrid Search
        → RAG → Qwen3
        """
    )


# ============================================================
# PROCESS DOCUMENTS
# ============================================================

if process_documents:

    if not uploaded_files:

        st.warning(
            "Please upload at least one PDF."
        )

    else:

        all_chunks = []
        document_names = []

        progress = st.progress(0)

        status = st.empty()

        for index, uploaded_file in enumerate(
            uploaded_files
        ):

            file_path = os.path.join(
                UPLOAD_DIR,
                uploaded_file.name
            )

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            document_names.append(
                uploaded_file.name
            )

            status.write(
                f"Processing: {uploaded_file.name}"
            )

            pages = extract_text_from_pdf(
                file_path
            )

            chunks = create_chunks(
                pages
            )

            all_chunks.extend(
                chunks
            )

            progress.progress(
                (index + 1) /
                len(uploaded_files)
            )

        status.write(
            "Building vector database..."
        )

        # --------------------------------
        # BUILD VECTOR STORE
        # --------------------------------

        vector_store = VectorStore()

        vector_store.build(
            all_chunks
        )

        vector_store.save(
            VECTOR_DIR
        )

        # --------------------------------
        # BUILD HYBRID SEARCH
        # --------------------------------

        search_engine = HybridSearch(
            vector_store
        )

        st.session_state.vector_store = (
            vector_store
        )

        st.session_state.search_engine = (
            search_engine
        )

        st.session_state.chunks = (
            all_chunks
        )

        st.session_state.documents = (
            document_names
        )

        status.success(
            "Documents processed successfully!"
        )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.chunks:

    st.subheader(
        "📊 Document Overview"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Documents",
            len(
                st.session_state.documents
            )
        )

    with col2:

        st.metric(
            "Chunks",
            len(
                st.session_state.chunks
            )
        )

    with col3:

        pages = len(
            set(
                (
                    chunk["source"],
                    chunk["page"]
                )
                for chunk in
                st.session_state.chunks
            )
        )

        st.metric(
            "Pages",
            pages
        )


# ============================================================
# DOCUMENT LIST
# ============================================================

if st.session_state.documents:

    with st.expander(
        "📚 Uploaded Documents"
    ):

        for document in (
            st.session_state.documents
        ):

            st.write(
                f"📄 {document}"
            )


# ============================================================
# CHAT SECTION
# ============================================================

st.divider()

st.subheader(
    "🔎 Ask Questions About Your Documents"
)


question = st.text_input(
    "Enter your question",
    placeholder=(
        "Example: What is the applicant's "
        "monthly salary?"
    )
)


ask_button = st.button(
    "🔍 Search & Ask",
    type="primary"
)


# ============================================================
# ANSWER
# ============================================================

if ask_button:

    if not st.session_state.search_engine:

        st.warning(
            "Please upload and process documents first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            answer, results = answer_question(
                question,
                st.session_state.search_engine
            )

        # --------------------------------
        # ANSWER
        # --------------------------------

        st.markdown(
            "### 🤖 Answer"
        )

        st.write(
            answer
        )

        # --------------------------------
        # SOURCES
        # --------------------------------

        st.markdown(
            "### 📚 Retrieved Evidence"
        )

        for index, result in enumerate(
            results,
            start=1
        ):

            with st.expander(
                f"{index}. {result['source']} — Page {result['page']}"
            ):

                st.write(
                    result["text"]
                )

                st.caption(
                    f"Hybrid Search Score: "
                    f"{result.get('hybrid_score', 0):.4f}"
                )