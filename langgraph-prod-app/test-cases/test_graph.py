from nodes import classify_message

def test_classify_message_billing():
    state = {
        "user_id": "u_1",
        "message": "I was charged twice"
    }

    result = classify_message(state)

    # if result["category"] == "billing":
    #     "Valid"
    # else:
    #     "Test case fail"

    assert result["category"] == "billing"
    assert result["risk"] == "high"

def test_classify_technical_message():
    state = {
        "user_id": "u_2",
        "message": "The app crashes"
    }

    result = classify_message(state)

    assert result["category"] == "technical"
    assert result["risk"] == "medium"

