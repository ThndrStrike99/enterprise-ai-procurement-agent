from app.rag.chunking import fixed_size_chunk


def test_chunking_returns_multiple_chunks():
    text = "A" * 1000
    chunks = fixed_size_chunk(text, size=300, overlap=50)

    assert len(chunks) > 1
    assert all(len(chunk) <= 300 for chunk in chunks)
