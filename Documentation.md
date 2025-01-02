**Functional Use of the Flask-Based Proxy Server**

---

**Introduction:**

This document provides an overview of the functional use of the Flask-based proxy server. The proxy server is designed to forward HTTP requests from a client to a specified target server and relay the responses back to the client. It supports multiple HTTP methods, including GET, POST, PUT, DELETE, and PATCH. This proxy server is suitable for testing and development purposes and is not intended for production environments.

---

**Core Functionality:**

1. **Request Forwarding:**
   - The proxy server listens for HTTP requests on a designated port.
   - Incoming requests are forwarded to the configured target server.
   - Supported HTTP methods include:
     - GET: For retrieving resources.
     - POST: For creating or updating resources with a payload.
     - PUT: For replacing resources.
     - DELETE: For removing resources.
     - PATCH: For partial updates to resources.

2. **Response Handling:**
   - The proxy server captures the target server’s response.
   - It relays the response status code, headers, and body back to the client.
   - Hop-by-hop headers, such as `content-length` and `connection`, are excluded to ensure proper forwarding.

3. **Authorization Support:**
   - The proxy server adds predefined authorization headers to outgoing requests.
   - These headers can include bearer tokens or other credentials defined in the configuration file.

4. **Dynamic Routing:**
   - Requests to the proxy server’s `/api/<path:subpath>` endpoint are dynamically routed to corresponding endpoints on the target server.
   - Example:
     - Incoming: `http://localhost:8888/api/resource`
     - Forwarded: `http://192.168.2.2:8123/api/resource`

5. **Error Handling:**
   - The proxy server logs any errors encountered during request forwarding.
   - It returns a 500 Internal Server Error to the client if the request to the target server fails.

---

**Configuration Requirements:**

1. **Configuration File (`config.json`):**
   - A JSON file located in the `instance/` directory.
   - Example:
     ```json
     {
       "target_server": "http://192.168.2.2:8123",
       "port": 8888,
       "auth_token": "YOUR_LONG_LIVED_ACCESS_TOKEN"
     }
     ```
   - **Fields:**
     - `target_server`: The base URL of the server to which requests are forwarded.
     - `port`: The port on which the proxy server listens for incoming requests.
     - `auth_token`: A token used for authentication with the target server.

2. **Environment Setup:**
   - Python 3.x must be installed.
   - A virtual environment should be created and activated for dependency management.
   - Dependencies are listed in `requirements.txt` and include:
     - Flask
     - requests

---

**Example Usage:**

1. **Start the Proxy Server:**
   ```bash
   python run.py
   ```

2. **Send a GET Request:**
   - Client Command:
     ```bash
     curl http://localhost:8888/api/resource
     ```
   - Forwarded Request:
     - URL: `http://192.168.2.2:8123/api/resource`
     - Method: GET
     - Headers:
       ```
       Authorization: Bearer YOUR_LONG_LIVED_ACCESS_TOKEN
       Content-Type: application/json
       ```
   - Response:
     - Status Code: 200 (or appropriate code from the target server)
     - Body: JSON or other data as returned by the target server.

3. **Send a POST Request:**
   - Client Command:
     ```bash
     curl -X POST http://localhost:8888/api/resource \
          -H "Content-Type: application/json" \
          -d '{"key": "value"}'
     ```
   - Forwarded Request:
     - URL: `http://192.168.2.2:8123/api/resource`
     - Method: POST
     - Headers:
       ```
       Authorization: Bearer YOUR_LONG_LIVED_ACCESS_TOKEN
       Content-Type: application/json
       ```
     - Body:
       ```json
       {
         "key": "value"
       }
       ```
   - Response:
     - Status Code: 201 (or appropriate code from the target server)
     - Body: JSON or other data as returned by the target server.

---

**Limitations:**

1. **Security:**
   - The proxy server does not validate incoming request payloads or headers.
   - It does not enforce HTTPS, making it unsuitable for production environments.

2. **Error Handling:**
   - Error messages returned to the client are generic and do not include detailed diagnostics.

3. **Performance:**
   - The proxy server is single-threaded when run using Flask’s development server.
   - It may not scale well under high traffic.

---

**Use Cases:**

1. **Development and Testing:**
   - Simulate interactions between clients and a target server without direct access to the latter.
   - Test API calls in a controlled local environment.

2. **Debugging:**
   - Monitor and log API requests and responses.
   - Debug authentication flows by inspecting headers and payloads.

3. **Educational Purposes:**
   - Learn how proxy servers function.
   - Experiment with Flask’s routing and request handling capabilities.

---

**Conclusion:**

The Flask-based proxy server is a lightweight and flexible tool for forwarding API requests. While it is ideal for testing and development, it should not be deployed in production environments without significant enhancements to security, performance, and scalability. Its dynamic routing and ease of configuration make it a valuable asset for developers working with APIs.

