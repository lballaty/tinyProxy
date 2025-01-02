# Flask-Based Proxy Server

## Overview

This project implements a lightweight, Flask-based proxy server designed for testing and development purposes. The proxy server forwards HTTP requests from a client to a specified target server and relays the responses back to the client. It supports multiple HTTP methods, including GET, POST, PUT, DELETE, and PATCH. This project is not intended for production use without significant enhancements to security and performance.

## Features

- **Request Forwarding**: Dynamically routes requests to the target server.
- **Response Handling**: Relays responses with status codes and headers.
- **Authorization**: Adds predefined authorization headers to requests.
- **Dynamic Routing**: Routes requests based on configurable endpoints.
- **Multi-Method Support**: Supports GET, POST, PUT, DELETE, and PATCH requests.

## Requirements

- Python 3.x
- Flask
- requests

## Project Structure

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

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd tinyProxy
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   - Create a `config.json` file in the `instance/` directory:
     ```json
     {
       "target_server": "http://192.168.2.2:8123",
       "port": 8888,
       "auth_token": "YOUR_LONG_LIVED_ACCESS_TOKEN"
     }
     ```

## Usage

1. **Start the proxy server**:
   ```bash
   python run.py
   ```

2. **Send requests to the proxy server**:
   - Example GET request:
     ```bash
     curl http://localhost:8888/api/resource
     ```
   - Example POST request:
     ```bash
     curl -X POST http://localhost:8888/api/resource \
          -H "Content-Type: application/json" \
          -d '{"key": "value"}'
     ```

## Testing

1. **Run the test suite**:
   ```bash
   python -m unittest discover tests
   ```

## Limitations

- Does not validate incoming request payloads or headers.
- Does not support HTTPS (not suitable for production).
- Single-threaded when run with Flask's development server.

## Future Enhancements

1. **Security**:
   - Add HTTPS support.
   - Implement input validation and sanitization.
   - Restrict access by IP allowlists.

2. **Performance**:
   - Introduce caching mechanisms for repeated requests.
   - Use asynchronous frameworks like FastAPI for better concurrency.

3. **Scalability**:
   - Deploy with production-grade servers like Gunicorn or uWSGI.
   - Containerize the application using Docker.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Flask documentation: https://flask.palletsprojects.com
- requests library documentation: https://docs.python-requests.org/en/latest/

