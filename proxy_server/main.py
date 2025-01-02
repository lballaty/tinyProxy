from flask import Flask, request, Response
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration variables (replace with your actual configuration)
HOMEASSISTANT_BASE_URL = "http://192.168.2.2:8123"
PROXY_PORT = 8888
HEADERS = {
    "Authorization": "Bearer YOUR_LONG_LIVED_ACCESS_TOKEN",
    "Content-Type": "application/json"
}

@app.route('/api/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(subpath):
    url = f"{HOMEASSISTANT_BASE_URL}/api/{subpath}"
    logger.info(f"Proxying {request.method} request to: {url}")
    try:
        # Prepare the request parameters
        data = request.get_data() if request.method in ['POST', 'PUT', 'PATCH'] else None
        params = request.args if request.method == 'GET' else None
        headers = {key: value for key, value in request.headers if key.lower() not in ['host', 'content-length']}

        # Forward the request based on the method
        response = requests.request(
            method=request.method,
            url=url,
            headers={**HEADERS, **headers},
            params=params,
            data=data,
            allow_redirects=False
        )

        # Exclude hop-by-hop headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for name, value in response.raw.headers.items()
                            if name.lower() not in excluded_headers]

        # Create the Flask response object
        flask_response = Response(response.content, response.status_code, response_headers)
        return flask_response

    except requests.exceptions.RequestException as e:
        logger.error(f"Error forwarding request: {e}")
        return Response("Failed to forward request.", status=500)

if __name__ == '__main__':
    logger.info(f"Starting proxy server on port {PROXY_PORT}...")
    app.run(host='0.0.0.0', port=PROXY_PORT)
