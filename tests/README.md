# Tests

Basic validation tests for the ML Pipeline DAG.

## Purpose

These tests ensure:
- ✅ DAG can be loaded without syntax/import errors
- ✅ DAG has the correct structure and task count
- ✅ DAG has appropriate tags

## Running Tests

### Using Docker (Recommended)

```bash
# Run tests inside Airflow container
docker-compose exec airflow-webserver pytest tests/
```

### Locally

```bash
# Install test dependencies
pip install -r tests/requirements-test.txt

# Run tests
pytest tests/

# Run with verbose output
pytest tests/ -v
```

## What's Tested

- **DAG Loading**: Verifies the DAG file has no Python syntax errors
- **Import Validation**: Ensures all imports work correctly
- **Task Count**: Confirms all expected tasks are present
- **DAG Tags**: Validates metadata is correctly set

## Adding More Tests

If you want to expand testing:
- Add integration tests for individual task functions
- Add data validation tests
- Add performance tests
- Add end-to-end pipeline tests

For now, this basic validation is sufficient for a portfolio project.
