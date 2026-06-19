from app.planner.planner import plan_context


def test_plan_context_returns_dict():

    result = plan_context(
        "Explain authentication",
        []
    )

    assert isinstance(
        result,
        dict
    )