from src.rag.retriever import retrieve_context
from src.llm.inference import run_llm


def test_rag_llm_pipeline():
    query = "What is CUDA?"

    context = retrieve_context(query)
    result = run_llm(query, context)

    assert context is not None
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0