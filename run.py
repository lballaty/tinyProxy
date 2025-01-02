from app import create_app

app = create_app()

if __name__ == '__main__':
    app.logger.info(f"Starting proxy server on port {app.config['PROXY_PORT']}...")
    app.run(host='0.0.0.0', port=app.config['PROXY_PORT'], threaded=True)
