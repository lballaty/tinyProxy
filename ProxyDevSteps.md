**Implementation Document: Flask-Based Proxy Server**

---

**Introduction:**

This document outlines the implementation of a non-production-ready proxy server developed using Flask. Designed for testing purposes only, this proxy server forwards client requests to a specified target server and relays the responses back to the client. It supports various HTTP methods and is intended for local development and experimentation.

---

**Implementation Process:**

1. **Set Up the Development Environment:**
   - Ensure Python 3.x is installed.
   - Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install required packages:
     ```bash
     pip install Flask requests
     ```
   - Freeze the installed packages into `requirements.txt`:
     ```bash
     pip freeze > requirements.txt
     ```

2. **Organize the Project Structure:**
   - Create the necessary directories and files as outlined in the file structure below.

3. **Develop the Application Components:**
   - Configure the application settings.
   - Implement the proxy logic to handle incoming requests and forward them to the target server.
   - Set up logging for monitoring purposes.

4. **Test the Application:**
   - Develop test cases to ensure the proxy server functions as expected.
   - Run the application locally and verify its behavior with various HTTP methods.

---

**File Structure:**

```
tinyProxy/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── config.py
│   └── utils.py
├── instance/
│   └── config.json
├── tests/
│   ├── test_routes.py
│   └── test_utils.py
├── requirements.txt
└── run.py
```

---

**Function Explanations and Code Details:**

1. **`app/__init__.py`:**
   - Initializes the Flask application and loads configurations.
   
   **Code:**
   ```python
   from flask import Flask
   from .config import configure_app

   def create_app():
       app = Flask(__name__, instance_relative_config=True)
       configure_app(app)

       with app.app_context():
           from . import routes
           return app
   ```

   **Explanation:**
   - Imports the `Flask` class and the `configure_app` function.
   - Defines `create_app()` to initialize the Flask application.
   - Sets `instance_relative_config=True` to allow instance-specific configurations.
   - Calls `configure_app(app)` to load configurations.
   - Registers routes within the application context.
   - Returns the configured Flask application instance.

2. **`app/config.py`:**
   - Manages configuration settings and logging setup.

   **Code:**
   ```python
   import json
   import logging
   from flask import current_app

   def configure_app(app):
       # Load configuration
       try:
           with open('instance/config.json', 'r') as file:
               config = json.load(file)
               app.config['TARGET_SERVER'] = config["target_server"]
               app.config['PROXY_PORT'] = config["port"]
               app.config['AUTH_TOKEN'] = config["auth_token"]
               app.config['HEADERS'] = {
                   "Authorization": f"Bearer {config['auth_token']}",
                   "Content-Type": "application/json"
               }
               app.logger.info("Configuration loaded successfully.")
       except FileNotFoundError:
           app.logger.error("Configuration file 'config.json' not found.")
           raise
       except KeyError as e:
           app.logger.error(f"Missing required configuration key: {e}")
           raise

       # Configure logging
       logging.basicConfig(level=logging.INFO,
                           format="%(asctime)s [%(levelname)s] %(message)s")
       app.logger = logging.getLogger(__name__)
   ```

   **Explanation:**
   - Imports necessary modules: `json` for parsing configuration files, `logging` for setting up logging, and `current_app` from Flask.
   - Defines `configure_app(app)` to load configurations and set up logging.
   - Attempts to open and read `config.json` from the `instance` directory.
   - Loads the JSON data and assigns configuration values to the Flask app's `config` dictionary.
   - Sets up default headers, including authorization, for forwarding requests.
   - Logs a success message if configurations are loaded successfully.
   - Handles exceptions for missing configuration files or keys, logging appropriate error messages.
   - Configures logging with a specified format and assigns a logger to the app.

3. **`instance/config.json`:**
   - Stores instance-specific configuration parameters such as the target server URL, port, and authorization token.

   **Code:**
   ```json
   {
     "target_server": "http://192.168.2.2:8123",
     "port": 8888,
     "auth_token": "YOUR_LONG_LIVED_ACCESS_TOKEN"
   }
   ```

   **Explanation:**
   - **`target_server`**: Specifies the base URL of the server to which the proxy forwards requests.
   - **`port`**: Defines the port number on which the proxy server listens for incoming requests.
   - **`auth_token`**: Provides an authorization token for secure communication with the target server.

4. **`app/routes.py`:**
   - Defines the proxy route and request handling logic.

   **Code:**
   ```python
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
   ```

   **Explanation:**
   - Defines a route `/api/<path:subpath>` to handle incoming API requests.
   - Constructs the target URL by appending `subpath` to the base URL.
   - Logs the details of the incoming request.
   - Prepares request data, parameters, and headers.
   - Forwards the request using the `requests` library.
   - Excludes hop-by-hop headers before forwarding the response.
   - Returns the response content and headers to the client.
   - Logs and handles errors in forwarding requests.

5. **`tests/test_routes.py`:**
   - Contains test cases for the `routes.py` module.

   **Code:**
   ```python
   import unittest
   from app import create_app

   class TestRoutes(unittest.TestCase):
       def setUp(self):
           self.app = create_app()
           self.client = self.app.test_client()

       def test_proxy_get(self):
           response = self.client.get('/api/test')
           self.assertEqual(response.status_code, 200)

       def test_proxy_post(self):
           response = self.client.post('/api/test', json={"key": "value"})
           self.assertEqual(response.status_code, 200)

   if __name__ == '__main__':
       unittest.main()
   ```

   **Explanation:**
   - Sets up a test client for the Flask application.
   - Tests the `GET` and `POST` proxy functionality by sending requests to the `/api/test` endpoint.
   - Verifies that the response status code is as expected.

6. **`tests/test_utils.py`:**
   - Placeholder for utility function tests.

   **Code:**
   ```python
   import unittest

   class TestUtils(unittest.TestCase):
       def test_sample_utility(self):
           self.assertTrue(True)  # Replace with actual utility tests

   if __name__ == '__main__':
       unittest.main()
   ```

   **Explanation:**
   - Provides a structure to test utility functions.
   - Includes a sample test case to be replaced with actual logic.

7. **`run.py`:**
   - Entry point to start the Flask application.

   **Code:**
   ```python
   from app import create_app

   app = create_app()

   if __name__ == '__main__':
       app.logger.info(f"Starting proxy server on port {app.config['PROXY_PORT']}...")
       app.run(host='0.0.0.0', port=app.config['PROXY_PORT'], threaded=True)
   ```

   **Explanation:**
   - Imports the `create_app` function from the `app` package.
   - Creates an instance of the Flask application.
   - Starts the Flask development server on the configured port and listens on all interfaces (`0.0.0.0`).
   - Uses multithreading (`threaded=True`) to handle multiple requests concurrently.

---

**How to Build the App for macOS, Windows, and Linux:**

1. **Prerequisites:**
   - Ensure Python 3.x is installed.
   - Install Git if cloning the repository from a version control system.

2. **Steps for All Platforms:**
   - Clone the repository:
     ```bash
     git clone <repository_url>
     cd tinyProxy
     ```
   - Create and activate a virtual environment:
     - **macOS/Linux:**
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       ```
     - **Windows:**
       ```cmd
       python -m venv venv
       venv\Scripts\activate
       ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the application:
     ```bash
     python run.py
     ```

3. **macOS/Linux-Specific Notes:**
   - Ensure that the Python executable is correctly linked, especially if using system Python.
   - Adjust permissions if needed using `chmod`.

4. **Windows-Specific Notes:**
   - Use `python` instead of `python3`.
   - Ensure environment variables are correctly set up


---

**Future Enhancement possibilities :**

1. **Security Improvements:**
   - Implement input validation and sanitization.
   - Restrict access to authorized users or IPs.
   - Use HTTPS for secure communication.
   - Store the Long Lived Token in a secure way.
   - Provide Login and Password functionality

2. **Performance Enhancements:**
   - Introduce caching for frequently accessed endpoints.
   - Use asynchronous request handling for better concurrency.
   - Optimize logging to minimize performance impact.

3. **Scaling Considerations:**
   - Deploy with a production-ready server like Gunicorn or uWSGI.
   - Use containerization (e.g., Docker) for easier deployment.
   - Implement load balancing to handle increased traffic.

4. **Cross-Platform Support:**
   - Ensure the application works seamlessly across different operating systems.
   - Test compatibility with various Python environments and versions.

---


