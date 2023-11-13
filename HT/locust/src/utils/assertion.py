import http


def check_http_response(transaction, response):
    if response.status_code != 200:
        response.failure(f'failed with status code {response.status_code}')
    elif response.json()[0]["name"] != "Moscow":
        response.failure(
            f"Get unexpected value in 'name' -> {response.json()[0]['name']}"
        )
    elif response.elapsed.total_seconds() > 0.5:
        response.failure(
            f"Request took too long -> {response.elapsed.total_seconds()}"
        )


def check_http_response_post(transaction, response):
    if response.status_code != 200:
        response.failure(f'failed with status code {response.status_code}')
    elif response.elapsed.total_seconds() > 0.5:
        response.failure(
            f"Request took too long -> {response.elapsed.total_seconds()}"
        )


