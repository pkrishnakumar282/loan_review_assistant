from config import CHUNK_SIZE, CHUNK_OVERLAP


def clean_text(text):
    """
    Basic text cleaning.
    """

    text = text.replace("\x00", " ")
    text = " ".join(text.split())

    return text


def create_chunks(pages):

    chunks = []

    chunk_id = 0

    for page_data in pages:

        page_number = page_data["page"]
        source = page_data["source"]

        text = clean_text(page_data["text"])

        if not text:
            continue

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end]

            if chunk_text.strip():

                chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "source": source,
                    "page": page_number
                })

                chunk_id += 1

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks