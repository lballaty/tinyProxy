# Pthon Proxy Server Documentation

## Overview

This project implements a Python-based proxy server designed to forward API requests from a web application to a HomeAssistant server, resolving CORS issues. The proxy is built using Flask, with configurable settings for the target server, port, and authentication token via a `config.json` file. Logging and error handling are implemented for better observability and robustness.

---

## Features

- **CORS Resolution**: Enables seamless communication between web applications and the HomeAssistant API.
- **Configurable Settings**: Configure the target server, port, and authentication token via `config.json`.
- **Logging**: Provides detailed logs for requests and errors.
- **Error Handling**: Gracefully handles exceptions and returns meaningful error messages.

---

## Prerequisites

- Python 3.9 or later
- Required Python libraries (listed in `requirements.txt`):
  - Flask
  - Requests
  - Certifi

---

## File Structure

```plaintext
python-proxy-app/
├── proxy_server/
│   ├── __init__.py
│   ├── main.py       # Main application logic
│   ├── utils.py      # Utility functions (future use)
├── tests/
│   ├── __init__.py
│   ├── test_proxy.py # Unit tests
├── .devcontainer/
│   ├── devcontainer.json # Dev container configuration
├── config.json       # Proxy configuration file
├── requirements.txt  # Project dependencies
├── setup.py          # Py2App packaging configuration
├── README.md         # Project documentation
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/python-proxy-app.git
cd python-proxy-app
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `config.json` file in the root directory with the following structure:

```json
{
    "target_server": "http://192.168.2.2:8123",
    "port": 8888,
    "auth_token": "YOUR_LONG_LIVED_ACCESS_TOKEN"
}
```

- **target\_server**: URL of the HomeAssistant server.
- **port**: Port number for the proxy server.
- **auth\_token**: Long-lived access token for authenticating with the HomeAssistant API.

---

## Usage

### Start the Proxy Server

Run the following command to start the server:

```bash
python proxy_server/main.py
```

The server listens on the port specified in `config.json` (default: `8888`).

### Send Requests Through the Proxy

Using `curl`, you can test the proxy server:

```bash
curl -X GET "http://localhost:8888/api/states" -H "Content-Type: application/json"
```

- This command forwards the request to the HomeAssistant server and returns the response.

### Logs and Debugging

Logs are printed to the terminal and include:

- Request details
- Response status codes
- Error messages in case of failure

---

## Testing

### Run Unit Tests

Unit tests are located in the `tests/` directory. To run the tests:

```bash
python -m unittest discover tests
```

---

## Deployment

To deploy the proxy server as a standalone macOS application, follow these steps:

### 1. Install `py2app`

```bash
pip install py2app
```

### 2. Configure `setup.py`

Ensure `setup.py` is correctly configured:

```python
from setuptools import setup

APP = ['proxy_server/main.py']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'Python Proxy Server',
        'CFBundleVersion': '0.1.0'
    }
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

### 3. Build the Application

```bash
python setup.py py2app
```

The packaged application will be available in the `dist/` directory.

---

## Troubleshooting

### Common Issues

1. **Configuration File Not Found**

   - Ensure `config.json` exists in the project root and is properly formatted.

2. **Server Not Responding**

   - Verify the HomeAssistant server URL and that it is reachable from the proxy server.

3. **Authentication Errors**

   - Check the validity of the long-lived access token in `config.json`.

### Debugging

- Check the logs printed to the terminal for detailed error messages.
- Enable debug mode in Flask for more information:
  ```python
  app.run(host='0.0.0.0', port=PROXY_PORT, debug=True)
  ```

---

## Future Enhancements

- Add support for additional HTTP methods (e.g., PUT, DELETE).
- Implement rate limiting for security.
- Add unit tests for edge cases.
- Create a Dockerfile for containerized deployment.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- Flask: A micro web framework for Python
- Requests: A simple HTTP library for Python
- HomeAssistant: Open-source home automation platform

---

