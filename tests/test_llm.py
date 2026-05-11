from src.llm.inference import run_llm


def test_llm_inference():
    result = run_llm(
        query="What is CUDA?",
        context="CUDA is a GPU computing platform."
    )

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0