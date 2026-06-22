"""
Reads raw_docs/*.txt, splits each file into sections at detected headings,
filters chunks that are too short to be meaningful, and saves the result to
data/chunks.json.

Heading detection heuristic (two steps):

  Step 1 — candidate filter: a block (text between blank lines) is a heading
  candidate if it is a single line, 5–80 chars, does not start with whitespace
  (scraper continuation artifact), does not end with '.' or ',' (sentence
  fragment or list item with description), and has a capitalization ratio >= 0.5
  (fraction of content words whose first letter is uppercase, excluding stop
  words like "a", "the", "is").

  Step 2 — run filter: 3+ consecutive heading candidates in the block list are
  treated as a vertical list (e.g. "Workspace Members / Calendar Events /
  Messages") and removed from the heading set. Isolated candidates and pairs are
  kept as real headings.
"""

import json
import re
from pathlib import Path

RAW_DOCS_DIR = Path(__file__).parent.parent / "data" / "raw_docs"
CHUNKS_OUT = Path(__file__).parent.parent / "data" / "chunks.json"
MIN_CHUNK_CHARS = 100

_STOP_WORDS = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be",
    "in", "of", "to", "for", "and", "or", "on", "at",
    "by", "with", "from", "that", "this", "these", "those",
    "it", "its", "not", "if", "as", "but", "has", "have",
    "do", "does", "can", "will", "may", "should", "could",
})


def _cap_ratio(text: str) -> float:
    """Fraction of content words (non-stop-words) that start uppercase."""
    words = re.findall(r"[\w']+", text)
    content = [w for w in words if w.lower() not in _STOP_WORDS]
    if not content:
        return 0.0
    return sum(1 for w in content if w[0].isupper()) / len(content)


def _split_blocks(text: str) -> list[str]:
    """Split on blank lines; return non-empty stripped blocks."""
    return [b.strip() for b in re.split(r"\n\n+", text) if b.strip()]


def _find_heading_indices(blocks: list[str]) -> set[int]:
    # Step 1: collect candidates
    candidates: set[int] = set()
    for i, block in enumerate(blocks):
        if "\n" in block:
            continue
        if not (5 <= len(block) <= 80):
            continue
        if block[0] in (" ", "\t"):
            continue
        if block.endswith((".", ",", ":", ")")):
            continue
        if _cap_ratio(block) < 0.6:
            continue
        candidates.add(i)

    # Step 2: remove runs of 3+ consecutive candidates (vertical lists)
    sorted_cands = sorted(candidates)
    list_items: set[int] = set()
    i = 0
    while i < len(sorted_cands):
        j = i
        while (
            j + 1 < len(sorted_cands)
            and sorted_cands[j + 1] == sorted_cands[j] + 1
        ):
            j += 1
        if j - i + 1 >= 3:
            list_items.update(sorted_cands[i : j + 1])
        i = j + 1

    return candidates - list_items


def chunk_file(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    blocks = _split_blocks(text)
    heading_indices = _find_heading_indices(blocks)

    chunks: list[dict] = []
    current_heading = path.stem
    current_parts: list[str] = []

    for i, block in enumerate(blocks):
        if i in heading_indices:
            if current_parts:
                chunk_text = "\n\n".join(current_parts)
                if len(chunk_text) >= MIN_CHUNK_CHARS:
                    chunks.append({
                        "text": chunk_text,
                        "source": path.name,
                        "heading": current_heading,
                    })
            current_heading = block
            current_parts = [block]
        else:
            current_parts.append(block)

    if current_parts:
        chunk_text = "\n\n".join(current_parts)
        if len(chunk_text) >= MIN_CHUNK_CHARS:
            chunks.append({
                "text": chunk_text,
                "source": path.name,
                "heading": current_heading,
            })

    return chunks


def main() -> None:
    all_chunks: list[dict] = []
    for path in sorted(RAW_DOCS_DIR.glob("*.txt")):
        file_chunks = chunk_file(path)
        print(f"{path.name}: {len(file_chunks)} chunks")
        all_chunks.extend(file_chunks)

    CHUNKS_OUT.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nTotal: {len(all_chunks)} chunks -> {CHUNKS_OUT}")


if __name__ == "__main__":
    main()
