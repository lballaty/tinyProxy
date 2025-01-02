from flask import request, Response, current_app
import requests

@current_app.route('/api/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(subpath):
    url = f"{current_app.config['TARGET_SERVER']}/api/{subpath}"
    current_app.logger.info(f"Proxying {request.method} request to: {url}")
    try:
        # Prepare the request parameters
        data = request.get_data() if request.method in ['POST', 'PUT', 'PATCH'] else None
        params = request.args if request.method == 'GET' else None
        headers = {**current_app.config['HEADERS'], **request.headers}

        # Forward the request
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
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
        current_app.logger.error(f"Error forwarding request: {e}")
        return Response("Failed to forward request.", status=500)

