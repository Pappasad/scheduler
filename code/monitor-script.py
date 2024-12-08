from mitmproxy import http
from urllib.parse import urlsplit, unquote

# Replacement URL and target redirect details
REPLACEMENT_HOST = "127.0.0.1"
REPLACEMENT_PORT = 5000

def request(flow: http.HTTPFlow) -> None:
    """
    Intercept and redirect all outgoing HTTP(S) requests.
    """
    original_url = flow.request.pretty_url  # Full URL
    original_host = flow.request.host

    # 1. Avoid infinite redirects to self
    if REPLACEMENT_HOST in original_url and str(REPLACEMENT_PORT) in original_url:
        return  # Don't redirect requests to itself

    # 2. Get the full path (including query params)
    url_parts = urlsplit(original_url)
    path_with_query = url_parts.path + ('?' + url_parts.query if url_parts.query else '')

    # 3. Decode percent-encoded characters (e.g., %20)
    decoded_path = unquote(path_with_query)
    
    # 4. Log the original and redirected URL
    print(f"[MONITOR] Redirecting: {original_url} --> http://{REPLACEMENT_HOST}:{REPLACEMENT_PORT}{decoded_path}")

    # 5. Change request host, port, scheme, and path
    flow.request.host = REPLACEMENT_HOST
    flow.request.port = REPLACEMENT_PORT
    flow.request.scheme = "http"  # Convert HTTPS to HTTP
    flow.request.path = decoded_path
