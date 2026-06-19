from app.core.optimizer import optimize


def test_optimizer_exists():

    assert callable(
        optimize
    )