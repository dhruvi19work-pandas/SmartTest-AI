
from intelligence.element_similarity import ElementSimilarity


def test_detect_similar_element():

    original_element = {
        "tag": "input",
        "id": "username",
        "name": "username",
        "type": "text",
        "placeholder": "Username",
        "aria_label": "Username",
        "text": "",
        "href": ""
    }

    updated_element = {
        "tag": "input",
        "id": "user_login",
        "name": "username",
        "type": "text",
        "placeholder": "Username",
        "aria_label": "Username",
        "text": "",
        "href": ""
    }

    unrelated_element = {
        "tag": "button",
        "id": "submit",
        "name": "",
        "type": "submit",
        "placeholder": "",
        "aria_label": "",
        "text": "Login",
        "href": ""
    }

    similarity = ElementSimilarity()

    score = similarity.calculate_similarity(
        original_element,
        updated_element
    )

    assert score >= 80

    candidates = [
        unrelated_element,
        updated_element
    ]

    results = similarity.find_similar_elements(
        original_element,
        candidates
    )

    # The updated username field should rank first
    assert results[0]["element"]["id"] == "user_login"

    print("\nSimilarity results:")

    for result in results:
        print(
            f"Element: {result['element']['id']} "
            f"| Similarity: {result['similarity']}%"
        )
