from src.ollama_client import generate_answer


def build_context(results):

    context_parts = []

    for i, result in enumerate(
        results,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {i}

Document: {result['source']}
Page: {result['page']}

Content:
{result['text']}
"""
        )

    return "\n".join(context_parts)


def create_prompt(question, context):

    prompt = f"""
You are a Banking Loan Document Review Assistant.

Your job is to answer questions using ONLY the provided
document context.

IMPORTANT RULES:

1. Do not invent information.
2. Do not use outside knowledge to fill missing information.
3. If the answer is not present in the documents, say:
   "The requested information was not found in the provided documents."
4. Always mention the supporting document and page.
5. If documents contain conflicting information, clearly
   identify the conflict.
6. Keep the answer concise and professional.
7. Do not make the final decision about whether a loan
   should be approved or rejected.

USER QUESTION:

{question}

DOCUMENT CONTEXT:

{context}

Now answer the question.
"""

    return prompt


def answer_question(
    question,
    search_engine
):

    results = search_engine.search(
        question
    )

    if not results:

        return (
            "No relevant information was found.",
            []
        )

    context = build_context(
        results
    )

    prompt = create_prompt(
        question,
        context
    )

    answer = generate_answer(
        prompt
    )

    return answer, results