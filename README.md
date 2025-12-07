### Building the Python Package

**1. Install Build Tools: Ensure you have setuptools and wheel installed.**
   ```
   pip install setuptools wheel build
   ```

**2. Build Distribution Archives.**
   ```
   python -m build
   ```

**3. create a virtual environment.**
    ```
    python -m venv .venv
    source venv/bin/activate
    On Windows: venv\Scripts\activate
    ```

**4. Install your package.**
     ```
     pip install -e .  # Install in editable mode for development
     Or, to install from the built wheel:
     pip install dist/ria-0.1.0-py3-none-any.whl
     ```

**5. Run the module.**
     ```
     python -m ria.ria
     ```

**6. Run the script.**
     ```
     python <project_root>/ria/ria.py
     ```