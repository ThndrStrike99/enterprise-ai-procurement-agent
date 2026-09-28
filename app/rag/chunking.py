from dataclasses import dataclass
from typing import List


@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: dict


def fixed_size_chunk(text: str, size: int = 500, overlap: int = 50) -> List[str]:
    if size <= overlap:
        raise ValueError("size must be greater than overlap")

    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap

    return chunks


def contract_to_chunks(contract_id: str, supplier_id: str, text: str) -> List[Chunk]:
    pieces = fixed_size_chunk(text, size=350, overlap=50)

    return [
        Chunk(
            chunk_id=f"{contract_id}-{i+1}",
            text=piece,
            metadata={
                "contract_id": contract_id,
                "supplier_id": supplier_id,
                "document_type": "contract",
            },
        )
        for i, piece in enumerate(pieces)
    ]
