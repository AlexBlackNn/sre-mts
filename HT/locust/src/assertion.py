import http


def check_http_response(transaction, response):
    if response.status_code != 200:
        response.failure(f'failed with status code {response.status_code}')