from src.rag.retriever import retrieve_context


def test_rag_retrieve_context():
    context = retrieve_context("What is CUDA?")

    assert context is not None
    assert isinstance(context, str)
    assert len(context) > 0