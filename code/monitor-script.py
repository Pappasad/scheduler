from mitmproxy import http
from backend import WEB_ADDR as REPLACEMENT_URL

def request(flow: http.HTTPFlow) -> None:
    """
    Intercept all outgoing HTTP(S) requests and redirect them to a specific URL.
    """
    original_url = flow.request.url  # Save the original URL for logging
    if original_url == REPLACEMENT_URL:
        return

    # Extract the path and query string from the original URL
    path = flow.request.path
    query = flow.request.query

    # Construct the new URL with the replacement domain and the original path/query
    flow.request.host = "127.0.0.1"
    flow.request.port = 5000
    flow.request.scheme = "http"
    flow.request.path = path
    flow.request.query = query

    print(f"Redirecting: {original_url} --> {flow.request.url}")
