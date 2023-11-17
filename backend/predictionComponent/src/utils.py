def validate_predict_request(request, expected_fields):
    """
    Checks that the request is a valid JSON containing all the required request fields.
    :param request: client request
    :param expected_fields: fields that are expected to be in the request JSON
    :return: error message if the request is not valid, None otherwise
    """
    if not request:
        return {"error": "Request can't be empty"}

    if not request.is_json:
        return {"error": "Request body must be JSON"}

    for field in expected_fields:
        if field not in request.json:
            return {"error": f"{field} is required"}
    return None


def validate_predict_response(response, expected_fields):
    """
    Validate that the returned response from the server for the prediction request is valid.
    :param response: server prediction response
    :param expected_fields: expected fields in response JSON
    """
    try:
        data = response.json()
    except ValueError:
        raise ValueError("Response from server must be a JSON")

    for field in expected_fields:
        if field not in data:
            raise ValueError(f"{field} is missing from response JSON")