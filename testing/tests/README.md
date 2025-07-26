# OCPI EMSP Backend Testing Framework

A comprehensive testing framework for the OCPI-compliant EMSP (E-Mobility
Service Provider) backend, designed to simulate and validate bidirectional
interactions with CPO (Charge Point Operator) systems.

## 🎯 Overview

This testing framework provides:

- **Mock CPO Server**: Complete CPO backend simulation using extrawest_ocpi library
- **Integration Tests**: End-to-end validation of EMSP-CPO interactions
- **Compliance Tests**: OCPI 2.2.1 specification adherence validation
- **Performance Tests**: Load testing and scalability validation
- **Unit Tests**: Individual component testing
- **Automated CI/CD**: Ready for continuous integration pipelines

## 📁 Project Structure

```text
tests/
├── __init__.py                 # Package initialization
├── conftest.py                 # Pytest configuration and fixtures
├── mock_cpo_server.py         # Mock CPO implementation
├── test_data_factory.py       # Test data generators
├── integration/               # End-to-end integration tests
│   ├── __init__.py
│   ├── test_authentication.py
│   ├── test_data_synchronization.py
│   └── test_command_flows.py
├── unit/                      # Unit tests for components
│   ├── __init__.py
│   └── test_authentication.py
├── compliance/                # OCPI specification compliance tests
│   ├── __init__.py
│   └── test_ocpi_compliance.py
├── performance/               # Load and performance tests
│   ├── __init__.py
│   └── test_load_performance.py
└── reports/                   # Generated test reports
    ├── coverage/              # Coverage reports
    ├── report.html           # HTML test report
    ├── junit.xml             # JUnit XML for CI/CD
    └── coverage.xml          # Coverage XML for CI/CD
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install test dependencies
pip install -r requirements.txt

# Or use the test runner
python run_tests.py --install-deps
```

### 2. Run Tests

```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py unit
python run_tests.py integration
python run_tests.py compliance
python run_tests.py performance

# Run quick tests (unit + integration)
python run_tests.py quick

# Run with options
python run_tests.py all --parallel --verbose
```

### 3. View Reports

After running tests, reports are generated in `tests/reports/`:

- **HTML Report**: `tests/reports/report.html` - Detailed test results
- **Coverage Report**: `tests/reports/coverage/index.html` - Code coverage analysis
- **JUnit XML**: `tests/reports/junit.xml` - CI/CD integration format

## 🧪 Test Categories

### Integration Tests

End-to-end tests that validate complete OCPI workflows:

```bash
# Run integration tests
pytest -m integration

# Specific integration test files
pytest tests/integration/test_authentication.py
pytest tests/integration/test_data_synchronization.py
pytest tests/integration/test_command_flows.py
```

**Coverage:**

- Authentication and token exchange flows
- Location discovery and synchronization
- Session reporting and management
- CDR submission and processing
- Command execution (START_SESSION, STOP_SESSION, etc.)
- Real-time communication and callbacks

### Unit Tests

Individual component testing:

```bash
# Run unit tests
pytest -m unit

# Test specific components
pytest tests/unit/test_authentication.py
```

**Coverage:**

- Authentication module validation
- CRUD operations testing
- Configuration management
- Data model validation
- Error handling

### Compliance Tests

OCPI 2.2.1 specification adherence validation:

```bash
# Run compliance tests
pytest -m compliance

# Generate compliance report
pytest tests/compliance/ --html=compliance_report.html
```

**Coverage:**

- Response format compliance
- Required field validation
- Data type compliance
- HTTP status code validation
- Error response format
- Pagination compliance

### Performance Tests

Load testing and performance validation:

```bash
# Run performance tests
pytest -m performance

# Run with benchmarking
pytest -m benchmark
```

**Coverage:**

- Concurrent request handling
- Load testing with multiple clients
- Response time benchmarking
- Resource usage validation
- Scalability testing

## 🔧 Configuration

### Pytest Configuration

The framework uses `pytest.ini` for configuration:

```ini
[tool:pytest]
testpaths = tests
addopts = --strict-markers --verbose --cov=. --html=tests/reports/report.html
markers =
    unit: Unit tests
    integration: Integration tests
    compliance: Compliance tests
    performance: Performance tests
```

### Test Fixtures

Key fixtures available in `conftest.py`:

- `emsp_app`: EMSP FastAPI application
- `mock_cpo_app`: Mock CPO FastAPI application
- `emsp_client`: Synchronous test client for EMSP
- `mock_cpo_client`: Synchronous test client for Mock CPO
- `async_emsp_client`: Async test client for EMSP
- `async_mock_cpo_client`: Async test client for Mock CPO
- `test_data_factory`: Test data generator
- `emsp_auth_headers`: EMSP authentication headers
- `cpo_auth_headers`: CPO authentication headers

## 📊 Mock CPO Server

The Mock CPO server (`mock_cpo_server.py`) provides:

### Features

- **Complete CPO Implementation**: All OCPI 2.2.1 CPO role endpoints
- **Realistic Data**: Pre-populated with test locations, tariffs, and sessions
- **Configurable Responses**: Support for error scenarios and edge cases
- **Separate Port**: Runs on port 8001 to avoid conflicts

### Usage

```python
# In tests, use the mock_cpo_client fixture
async def test_cpo_interaction(async_mock_cpo_client, cpo_auth_headers):
    response = await async_mock_cpo_client.get(
        "/ocpi/cpo/2.2.1/locations",
        headers=cpo_auth_headers
    )
    assert response.status_code == 200
```

### Supported Endpoints

- **Locations**: GET, PUT, PATCH location data
- **Sessions**: GET, PUT, PATCH session data
- **CDRs**: GET, POST charge detail records
- **Tariffs**: GET, PUT, DELETE tariff information
- **Commands**: POST command execution
- **Tokens**: GET, PUT token authorization
- **Credentials**: GET, POST, PUT credentials exchange

## 🏭 Test Data Factory

The `TestDataFactory` class generates realistic OCPI test data:

```python
# Create test data
factory = TestDataFactory()

# Generate OCPI objects
location = factory.create_location(name="Test Station")
session = factory.create_session(location_id="LOC001")
cdr = factory.create_cdr(session_id="SES001")
command = factory.create_command(command_type="START_SESSION")
```

### Available Generators

- `create_location()`: Location objects with EVSEs and connectors
- `create_session()`: Charging session objects
- `create_cdr()`: Charge Detail Records
- `create_tariff()`: Tariff and pricing information
- `create_token()`: Authentication tokens
- `create_command()`: Command objects for all types

## 🔍 Running Specific Tests

### By Test Type

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Compliance tests only
pytest -m compliance

# Performance tests only
pytest -m performance

# Slow tests (performance + long-running)
pytest -m slow
```

### By Test File

```bash
# Specific test file
pytest tests/integration/test_authentication.py

# Specific test class
pytest tests/integration/test_authentication.py::TestOCPIAuthentication

# Specific test method
pytest tests/integration/test_authentication.py::TestOCPIAuthentication::test_emsp_token_validation
```

### With Options

```bash
# Parallel execution
pytest -n auto

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Coverage report
pytest --cov=. --cov-report=html

# HTML report
pytest --html=report.html --self-contained-html
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: OCPI EMSP Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python run_tests.py all --parallel
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: tests/reports/coverage.xml
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python run_tests.py all --parallel'
            }
        }
        stage('Publish Results') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'tests/reports',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
                publishCoverage adapters: [
                    coberturaAdapter('tests/reports/coverage.xml')
                ]
            }
        }
    }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**

   ```bash
   # Make sure you're in the project root
   cd /path/to/evcharger

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Port Conflicts**

   ```bash
   # Check if ports 8000/8001 are in use
   lsof -i :8000
   lsof -i :8001

   # Kill processes if needed
   kill -9 <PID>
   ```

3. **Test Failures**

   ```bash
   # Run with verbose output
   pytest -v --tb=long

   # Run specific failing test
   pytest tests/path/to/test.py::test_name -v
   ```

4. **Performance Test Timeouts**

   ```bash
   # Increase timeout
   pytest --timeout=600 -m performance

   # Skip slow tests
   pytest -m "not slow"
   ```

### Debug Mode

```bash
# Run with debug output
pytest --log-cli-level=DEBUG

# Run single test with debugging
pytest tests/integration/test_authentication.py::test_emsp_token_validation -v -s
```

## 📚 Additional Resources

- [OCPI 2.2.1 Specification](https://evroaming.org/app/uploads/2021/11/OCPI-2.2.1.pdf)
- [extrawest_ocpi Documentation](https://github.com/extrawest/extrawest_ocpi)
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

## 🤝 Contributing

1. Add new tests following the existing patterns
2. Update test data factory for new OCPI objects
3. Ensure compliance tests cover new features
4. Add performance tests for critical paths
5. Update documentation for new test categories

## 📄 License

This testing framework follows the same license as the main EMSP backend project.
