"""
Answer generation layer for the Twenty CRM support chatbot.
Retrieves relevant documentation chunks and generates a grounded response.
"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import anthropic

sys.path.insert(0, str(Path(__file__).parent))
from retrieve import retrieve

MODEL = "claude-haiku-4-5-20251001"
_RATIONALE_TAG = "RATIONALE:"
_ANSWER_TAG = "ANSWER:"

_SYSTEM_PROMPT = """\
You are a support specialist for Twenty CRM, a modern open-source CRM platform.

Answer user questions using ONLY the documentation excerpts provided in each message. \
Do not draw on outside knowledge, even if you are confident about it.

When the excerpts fully answer the question, give a clear, practical answer.

When the excerpts partially answer the question, say explicitly what the documentation \
covers and name what it does not cover. Do not fill the gap with general knowledge or guesses.

When the excerpts do not address the question at all, say clearly that you could not find \
relevant documentation on this topic.

Keep answers concise and direct.\
"""

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def _format_chunks(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[{i}] {chunk['heading']}  ({chunk['source']})\n{chunk['text']}")
    return "\n\n".join(parts)


def _build_user_message(query: str, chunks: list[dict]) -> str:
    return (
        f"Documentation excerpts:\n\n"
        f"{_format_chunks(chunks)}\n\n"
        f"---\n"
        f"Question: {query}\n\n"
        f"Respond using exactly this format:\n"
        f"{_RATIONALE_TAG} <one or two sentences: what you understood the question to be "
        f"asking, and what the above excerpts do or do not cover>\n"
        f"{_ANSWER_TAG} <your response grounded in the excerpts above>"
    )


def _parse_response(text: str) -> tuple[str, str]:
    if _RATIONALE_TAG in text and _ANSWER_TAG in text:
        rationale_start = text.index(_RATIONALE_TAG) + len(_RATIONALE_TAG)
        answer_start = text.index(_ANSWER_TAG)
        rationale = text[rationale_start:answer_start].strip()
        answer = text[answer_start + len(_ANSWER_TAG):].strip()
        return rationale, answer
    return "Could not parse structured rationale.", text.strip()


def answer(query: str, k: int = 3, threshold: float = 0.40) -> dict:
    """
    Retrieve relevant chunks and generate a grounded answer.

    Returns a dict with keys:
      answer     — text to show the user
      rationale  — what the model understood and what it found
      escalated  — True if below threshold (API was not called)
      sources    — list of {source, heading} for chunks used in generation
    """
    chunks = retrieve(query, k=k)
    best_score = chunks[0]["score"] if chunks else 0.0

    if best_score < threshold:
        return {
            "answer": (
                "I wasn't able to find documentation that covers this question. "
                "For help with this topic, please reach out to the Twenty CRM support team "
                "or check the official documentation at docs.twenty.com."
            ),
            "rationale": (
                f"The best matching documentation chunk scored {best_score:.2f}, "
                f"which is below the confidence threshold of {threshold:.2f}. "
                "No retrieved content was sufficiently relevant to provide a reliable answer."
            ),
            "escalated": True,
            "sources": [],
        }

    user_message = _build_user_message(query, chunks)
    response = _get_client().messages.create(
        model=MODEL,
        max_tokens=1024,
        temperature=0,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    rationale, answer_text = _parse_response(response.content[0].text)

    return {
        "answer": answer_text,
        "rationale": rationale,
        "escalated": False,
        "sources": [{"source": c["source"], "heading": c["heading"]} for c in chunks],
    }


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    query = " ".join(sys.argv[1:]) or "How do I create a custom field in Twenty?"
    result = answer(query)
    print(json.dumps(result, indent=2, ensure_ascii=False))
