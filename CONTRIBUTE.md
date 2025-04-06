# CONTRIBUTE

Thank you for considering contributing to the Stores API project! Follow the guidelines below to get started.

## Start App Using Flask in Debug Mode

```bash
flask --app=app.py run --debug
```

## Start App Using Gunicorn

```bash
gunicorn -b '0.0.0.0:5000' 'app:create_app()'
```

## Setting Up the Development Environment

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd restapi
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run the test suite to ensure everything is working as expected:

```bash
pytest
```

## Submitting Changes

1. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with a descriptive message:

   ```bash
   git commit -m "Add feature: your feature description"
   ```

3. Push your branch to the repository:

   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a pull request on GitHub and describe your changes.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Use meaningful variable and function names.
- Write clear and concise comments where necessary.

## Reporting Issues

If you encounter any issues, please open an issue on the repository with a detailed description of the problem.

---

Thank you for contributing!
