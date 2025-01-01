from setuptools import setup

APP = ['proxy_server/main.py']
DATA_FILES = ['resources/app_icon.icns']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/app_icon.icns',
    'plist': {
        'CFBundleName': 'Python Proxy Server',
        'CFBundleDisplayName': 'Python Proxy Server',
        'CFBundleIdentifier': 'com.example.pythonproxy',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
