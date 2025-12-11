### 1. Building the Python Package

1) Install Build Tools: Ensure you have setuptools and wheel installed.
   ```
   pip install setuptools wheel build
   ```

2) Build Distribution Archives.
   ```
   python -m build
   ```

3) create a virtual environment.
    ```
    python -m venv .venv
    source venv/bin/activate
    On Windows: venv\Scripts\activate
    ```

4) Install your package.
     ```
     pip install -e .  # Install in editable mode for development
     (or)
     pip install dist/ria-0.1.0-py3-none-any.whl   # to install from the built wheel:
     ```

6) Run the module.
     ```
     python -m ria.ria
     ```

7) Run the script.
     ```
     python <project_root>/ria/ria.py
     ```


######################################


### 2. Python Package Index (PyPI) servers

1) Private Python Packages Server With devpi
```
pip install devpi devpi-server devpi-client
initialize: devpi-init
start server  : devpi-server --host 0.0.0.0 --port 3141
devpi use http://0.0.0.0:3141/
login         : devpi login root --password ''
add index     : devpi index -c dev bases=root/pypi
use index     : devpi use root/dev
upload package: devpi upload dist/*
Uploading to a specific index (if not using devpi use):
                devpi upload --index <user>/<index_name>
e.g.,           devpi upload --index root/dev
```
(or)
```
twine upload --repository-url http://0.0.0.0:3141/root/dev dist/* -u root -p ''
```
(or)
```
twine upload -r devpi dist/* --verbose
vi ~/.pypirc:
[distutils]
index-servers = devpi

[devpi]
repository = http://localhost:3141/root/dev
username = root
```

2) Install package from Index:
```
uvx --index http://0.0.0.0:3141/root/dev/+simple/ ria@latest
uvx --index http://0.0.0.0:3141/root/dev/ ria
uv tool run --index http://0.0.0.0:3141/root/dev/ ria
(or)
export PIP_INDEX_URL=http://localhost:3141/root/dev/
uvx ria
(or)
pip install -i http://localhost:3141/root/pypi/+simple/ your-package-name
e.g., pip install -i http://localhost:3141/root/dev/+simple/ ria --verbose
```
