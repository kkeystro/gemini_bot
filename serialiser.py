import json as j


def serialise(input_text, role):
    return j.dumps({
        "parts": [
            {
                "text": input_text
            }
        ],
        "role": role
    },)


def deserialise(list_of_parts):
    list_of_parts = [j.loads(item) for item in list_of_parts]
    return list_of_parts
