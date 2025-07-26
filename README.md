# OCPI EMSP-CPO Educational Demo & Backend

A comprehensive **E-Mobility Service Provider (EMSP)** backend
implementation using the [extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi)
library and FastAPI, combined with an educational platform for learning OCPI
(Open Charge Point Interface) 2.2.1. This project provides full OCPI 2.2.1
compliance, supports all required EMSP modules, and offers interactive
demonstrations and a robust testing framework.

---

### ⚠️ Disclaimer: Work in Progress ⚠️

This repository is primarily an **educational and development project** designed to demonstrate OCPI (Open Charge Point Interface) concepts and provide a functional EMSP backend for learning and testing purposes.

**Please be aware of the following:**

*   **Development Status**: This project is actively under development. You may encounter bugs, incomplete features, or unexpected behavior when starting services or running components.
*   **Primary Purpose**: Its main goal is to serve as a practical example and a robust testing ground for OCPI 2.2.1, not as a production-ready solution out-of-the-box.
*   **Stability & Completeness**: While efforts are made to ensure stability, certain features might be experimental or subject to change. It is not intended for critical production environments without significant further development and hardening.
*   **Reporting Issues**: If you encounter any issues or have suggestions, please open an issue on the GitHub repository. Your feedback is valuable!
*   **Educational vs. Production**: This demo is structured to be easily understandable and modifiable for educational purposes. Production-grade implementations would require more robust error handling, security measures, scalability considerations, and persistent data storage.

---

## 🚀 Main Project Features

- **OCPI 2.2.1 Compliant**: Full implementation of OCPI protocol version 2.2.1
- **EMSP Role**: Complete EMSP functionality for managing EV charging services
- **All EMSP Modules**: Locations, Sessions, CDRs, Tariffs, Commands, Tokens,
  Hub Client Info, Charging Profiles
- **Token Authentication**: OCPI-compliant token-based authentication
  (Token A & Token C)
- **Mock Data**: Built-in mock data for development and testing
- **Production Ready**: Configurable for production deployment
- **Real-time Updates**: HTTP push notifications support
- **Comprehensive API**: RESTful API with OpenAPI documentation

### 📋 Supported OCPI Modules (EMSP Backend)

#### Receiver Modules (EMSP receives data from CPO)

- **Locations** - Charging station location information
- **Sessions** - Charging session data
- **CDRs** - Charge Detail Records
- **Tariffs** - Pricing and tariff information
- **Hub Client Info** - Hub client information
- **Credentials** - Registration and credentials management

#### Sender Modules (EMSP sends data to CPO)

- **Commands** - Commands to charging stations (Start/Stop/Reserve/etc.)
- **Tokens** - Token authorization requests
- **Charging Profiles** - Smart charging profile management

### 🛠️ Installation (Main Project)

#### Prerequisites

- Python 3.10 or higher
- pip or poetry for package management

#### Quick Start

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd evcharger
   ```

2. **Install dependencies**:

   ```bash
   # Using pip
   pip install -r requirements.txt

   # Or using the extrawest_ocpi library directly
   cd extrawest_ocpi
   pip install -e .
   cd ..
   ```

3. **Set up environment variables** (optional):

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**:

   ```bash
   python core/main.py
   ```

The EMSP backend will be available at `http://localhost:8000`

### ⚙️ Configuration (Main Project)

#### Environment Variables

Create a `.env` file in the root directory:

```env
# Application Settings
PROJECT_NAME=OCPI EMSP Backend
ENVIRONMENT=development
DEBUG=true

# OCPI Settings
OCPI_HOST=localhost:8000
COUNTRY_CODE=US
PARTY_ID=EMS
PROTOCOL=http

# Authentication
NO_AUTH=false
SECRET_KEY=your-secret-key-change-in-production

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost/emsp_db

# CORS Origins
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

#### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `OCPI_HOST` | Host and port for OCPI endpoints | `localhost:8000` |
| `COUNTRY_CODE` | 2-letter country code | `US` |
| `PARTY_ID` | 3-letter EMSP identifier | `EMS` |
| `PROTOCOL` | Protocol (http/https) | `http` |
| `NO_AUTH` | Disable authentication (dev only) | `false` |
| `DEBUG` | Enable debug mode | `true` |

### 🔗 API Endpoints (Main Project)

#### Base URLs

- **Application Root**: `http://localhost:8000/`
- **OCPI Base**: `http://localhost:8000/ocpi/emsp/2.2.1/`
- **API Documentation**: `http://localhost:8000/ocpi/emsp/2.2.1/docs`
- **Health Check**: `http://localhost:8000/health`

#### OCPI Endpoints

##### Version Information

- `GET /ocpi/versions` - Get supported OCPI versions
- `GET /ocpi/emsp/2.2.1/` - Get version details and endpoints

##### Locations Module

- `GET /ocpi/emsp/2.2.1/locations` - List all locations
- `GET /ocpi/emsp/2.2.1/locations/{country_code}/{party_id}/{location_id}` - Get specific location
- `PUT /ocpi/emsp/2.2.1/locations/{country_code}/{party_id}/{location_id}` - Create/update location

##### Sessions Module

- `GET /ocpi/emsp/2.2.1/sessions` - List all sessions
- `GET /ocpi/emsp/2.2.1/sessions/{country_code}/{party_id}/{session_id}` - Get specific session
- `PUT /ocpi/emsp/2.2.1/sessions/{country_code}/{party_id}/{session_id}` - Create/update session

##### CDRs Module

- `GET /ocpi/emsp/2.2.1/cdrs` - List all CDRs
- `GET /ocpi/emsp/2.2.1/cdrs/{cdr_id}` - Get specific CDR
- `POST /ocpi/emsp/2.2.1/cdrs` - Create new CDR

##### Commands Module

- `POST /ocpi/emsp/2.2.1/commands/START_SESSION` - Start charging session
- `POST /ocpi/emsp/2.2.1/commands/STOP_SESSION` - Stop charging session
- `POST /ocpi/emsp/2.2.1/commands/RESERVE_NOW` - Reserve charging point
- `POST /ocpi/emsp/2.2.1/commands/CANCEL_RESERVATION` - Cancel reservation

##### Tokens Module

- `GET /ocpi/emsp/2.2.1/tokens/{country_code}/{party_id}/{token_uid}` - Get token authorization
- `POST /ocpi/emsp/2.2.1/tokens/{country_code}/{party_id}/{token_uid}/authorize` - Authorize token

### 🔐 Authentication (Main Project)

The EMSP backend uses OCPI-compliant token-based authentication:

#### Token Types

- **Token A**: Used by EMSP to authenticate with CPO systems
- **Token C**: Used by CPO systems to authenticate with EMSP

#### Authentication Header

Include the authentication token in the `Authorization` header:

```text
Authorization: Token your_token_here
```

#### Default Development Tokens

For development and testing, the following tokens are pre-configured:

**Token A (EMSP tokens)**:
- `emsp_token_a_12345`
- `emsp_development_token_a`

**Token C (CPO tokens)**:
- `cpo_token_c_abcdef`
- `cpo_development_token_c`
- `test_token_c_123`

### 🧪 Testing (Main Project)

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Get OCPI Versions

```bash
curl -H "Authorization: Token test_token_c_123" \
     http://localhost:8000/ocpi/versions
```

#### List Locations

```bash
curl -H "Authorization: Token test_token_c_123" \
     http://localhost:8000/ocpi/emsp/2.2.1/locations
```

#### Start Charging Session

```bash
curl -X POST \
     -H "Authorization: Token test_token_c_123" \
     -H "Content-Type: application/json" \
     -d '{
       "response_url": "https://cpo.example.com/commands/callback",
       "token": {
         "uid": "TOKEN123",
         "type": "RFID"
       },
       "location_id": "LOC001",
       "evse_uid": "EVSE001",
       "connector_id": "CONN001"
     }' \
     http://localhost:8000/ocpi/emsp/2.2.1/commands/START_SESSION
```

### 🏗️ Architecture (Main Project)

#### Project Structure

```text
evcharger/
├── core/                # Core application logic
│   ├── main.py          # Application entry point
│   ├── crud.py          # CRUD operations implementation
│   ├── auth.py          # Authentication implementation
│   ├── config.py        # Configuration management
│   └── models.py        # Data models and mock data
├── educational/         # Educational demos and scripts
├── testing/             # Testing framework and mock CPO
├── utilities/           # Utility scripts and logs
├── README.md            # This documentation
├── .env                 # Environment variables (create from .env.example)
├── requirements.txt     # Python dependencies
└── extrawest_ocpi/      # OCPI library
    └── py_ocpi/         # Core OCPI implementation
```

#### Key Components

1. **Main Application** (`core/main.py`): FastAPI application setup with
   OCPI configuration
2. **CRUD Operations** (`core/crud.py`): Database operations for all
   EMSP modules
3. **Authentication** (`core/auth.py`): OCPI token-based authentication
4. **Configuration** (`core/config.py`): Environment-based configuration
   management
5. **Data Models** (`core/models.py`): Mock data and data structures

### 🔧 Development (Main Project)

#### Adding New Features

1. **Extend CRUD Operations**: Add new methods to `EMSPCrud` class in
   `core/crud.py`
2. **Update Authentication**: Modify token management in `core/auth.py`
3. **Add Configuration**: Update settings in `core/config.py`
4. **Mock Data**: Add test data in `core/models.py`

#### Database Integration

Replace the mock storage in `core/crud.py` with actual database operations:

```python
# Example with SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession

class EMSPCrud(Crud):
    @classmethod
    async def get(cls, module: ModuleID, role: RoleEnum, id: str, **kwargs):
        async with get_db_session() as session:
            # Implement actual database query
            pass
```

## 🚀 Production Deployment (Main Project)

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t emsp-backend .
docker run -p 8000:8000 -e ENVIRONMENT=production emsp-backend
```

### Environment Setup

For production deployment:

1. **Set secure environment variables**:

   ```env
   ENVIRONMENT=production
   DEBUG=false
   PROTOCOL=https
   OCPI_HOST=your-domain.com
   SECRET_KEY=your-secure-secret-key
   NO_AUTH=false
   DATABASE_URL=postgresql://user:password@db-host/emsp_db
   ```

2. **Configure HTTPS**: Use a reverse proxy (nginx) or load balancer
3. **Database**: Set up PostgreSQL or your preferred database
4. **Monitoring**: Implement logging and monitoring solutions

## 🔍 Troubleshooting (Main Project)

### Common Issues

#### 1. Import Errors

```text
ImportError: No module named 'py_ocpi'
```

**Solution**: Install the extrawest_ocpi library:

```bash
cd extrawest_ocpi
pip install -e .
```

#### 2. Authentication Failures

```text
{"status_code": 2001, "status_message": "Invalid or missing token"}
```

**Solution**: Check your authorization header and token validity:

```bash
# Verify token format
curl -H "Authorization: Token your_token_here" ...
```

#### 3. CORS Issues

```text
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution**: Add your frontend URL to `BACKEND_CORS_ORIGINS` in config.

#### 4. Port Already in Use

```text
OSError: [Errno 48] Address already in use
```

**Solution**: Change the port or kill the existing process:

```bash
# Change port
python core/main.py --port 8001

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

### Debug Mode

Enable debug logging by setting:

```env
DEBUG=true
LOG_LEVEL=DEBUG
```

### Health Checks

Monitor the service health:

```bash
# Basic health check
curl http://localhost:8000/health

# OCPI version check
curl -H "Authorization: Token test_token_c_123" \
     http://localhost:8000/ocpi/versions
```

## 📚 OCPI Compliance (Main Project)

This implementation follows the [OCPI 2.2.1 specification](https://github.com/ocpi/ocpi/tree/2.2.1)
and includes:

- ✅ **Version Information Endpoint**: `/ocpi/versions`
- ✅ **Credentials Module**: Registration and token management
- ✅ **Locations Module**: Charging station information
- ✅ **Sessions Module**: Charging session management
- ✅ **CDRs Module**: Charge Detail Records
- ✅ **Tariffs Module**: Pricing information
- ✅ **Tokens Module**: Token authorization
- ✅ **Commands Module**: Charging station commands
- ✅ **Charging Profiles Module**: Smart charging
- ✅ **Hub Client Info Module**: Hub information

### OCPI Flow Examples

#### 1. CPO Registration Flow

1. CPO calls `POST /ocpi/emsp/2.2.1/credentials` with Token A
2. EMSP validates and stores CPO credentials
3. EMSP returns Token C for future authentication
4. CPO uses Token C for subsequent requests

#### 2. Token Authorization Flow

1. CPO sends `POST /ocpi/emsp/2.2.1/tokens/{token_uid}/authorize`
2. EMSP validates token and returns authorization status
3. CPO uses authorization result to allow/deny charging

#### 3. Session Management Flow

1. CPO sends session start: `PUT /ocpi/emsp/2.2.1/sessions/{session_id}`
2. EMSP stores session information
3. CPO sends session updates during charging
4. CPO sends final session data when complete
5. CPO sends CDR: `POST /ocpi/emsp/2.2.1/cdrs`

## 🤝 Contributing (Main Project)

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature/new-feature`
6. Submit a pull request

## 📄 License (Main Project)

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support (Main Project)

For support and questions:

- Create an issue in the repository
- Check the [OCPI specification](https://github.com/ocpi/ocpi/tree/2.2.1)
- Review the [extrawest_ocpi documentation](https://github.com/extrawest/extrawest_ocpi)

## 🔗 Related Links (Main Project)

- [OCPI Protocol Specification](https://github.com/ocpi/ocpi)
- [extrawest_ocpi Library](https://github.com/extrawest/extrawest_ocpi)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OCPI Community](https://www.ocpi-protocol.org/)

---

## 🚗⚡ OCPI EMSP-CPO Educational Demo Environment

A comprehensive educational platform for learning OCPI (Open Charge Point
Interface) 2.2.1 through practical demonstrations and interactive testing.

### 🎯 What is OCPI?

OCPI (Open Charge Point Interface) is a protocol that enables communication
between different actors in the EV charging ecosystem:

- **EMSP** (E-Mobility Service Provider): Charging apps and services that EV
  drivers use
- **CPO** (Charge Point Operator): Companies that own and operate charging
  stations
- **MSP** (Mobility Service Provider): Roaming services that connect EMSPs and
  CPOs

This project demonstrates how these systems communicate to provide seamless
charging experiences.

### 🏗️ Architecture (Educational Demo)

```text
📱 EMSP Backend (Port 8000)     🔌 Mock CPO Server (Port 8001)
├─ Authentication & Tokens      ├─ Location Management
├─ Session Management           ├─ Token Authorization
├─ CDR Processing              ├─ Session Monitoring
├─ Command Handling            ├─ Command Execution
└─ Location Discovery          └─ Billing Integration
            │                           │
            └─── OCPI 2.2.1 Protocol ───┘
```

### 🚀 Quick Start (Educational Demo)

#### 1. Install Dependencies

```bash
# Using pipenv (recommended)
pipenv install

# Or using pip
pip install -r requirements.txt
```

#### 2. Start the Educational Demo

```bash
# Interactive menu system
python educational/ocpi_menu.py

# Or start services directly
python educational/start_ocpi_demo.py
```

#### 3. Explore OCPI Concepts

```bash
# Interactive educational demos
python educational/ocpi_educational_demo.py interactive

# Specific concept demos
python educational/ocpi_educational_demo.py authentication
python educational/ocpi_educational_demo.py locations
python educational/ocpi_educational_demo.py sessions
```

#### 4. Run Tests

```bash
# All tests
python testing/run_tests.py

# Specific test types
python testing/run_tests.py unit
python testing/run_tests.py integration
python testing/run_tests.py compliance
```

### 🎓 Educational Features

#### Interactive Learning

- **Step-by-step demos** with detailed explanations
- **Real OCPI message flows** with educational commentary
- **Interactive menu system** for guided exploration
- **Troubleshooting guides** for common issues

#### Key OCPI Concepts Covered

1. **Authentication & Credential Exchange** - How systems establish trust
2. **Location Discovery** - How EMSPs find charging stations
3. **Token Authorization** - How users get validated for charging
4. **Session Management** - How charging sessions are controlled
5. **CDR Processing** - How billing information is exchanged

#### Testing Framework (Educational Demo)

- **Unit Tests** - Individual component validation
- **Integration Tests** - End-to-end EMSP-CPO interactions
- **Compliance Tests** - OCPI 2.2.1 specification adherence
- **Performance Tests** - Load testing and scalability validation

### 📚 Available Scripts (Educational Demo)

| Script | Purpose | Usage |
|--------|---------|-------|
| `ocpi_menu.py` | Interactive menu system | `python ocpi_menu.py` |
| `start_ocpi_demo.py` | Start EMSP/CPO services | `python start_ocpi_demo.py` |
| `ocpi_educational_demo.py` | Educational demonstrations | `python ocpi_educational_demo.py interactive` |
| `run_tests.py` | Test execution | `python run_tests.py [test_type]` |
| `test_framework_validation.py` | Framework validation | `python test_framework_validation.py` |

### 🌐 API Documentation (Educational Demo)

Once services are running:

- **EMSP Backend**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Mock CPO Server**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **OCPI Endpoints**:
  - EMSP: [http://localhost:8000/ocpi/emsp/2.2.1/versions](http://localhost:8000/ocpi/emsp/2.2.1/versions)
  - CPO: [http://localhost:8001/ocpi/cpo/2.2.1/versions](http://localhost:8001/ocpi/cpo/2.2.1/versions)

### 🧪 Testing (Educational Demo)

#### Test Categories

```bash
# Unit tests (individual components)
python run_tests.py unit

# Integration tests (EMSP-CPO interactions)
python run_tests.py integration

# Compliance tests (OCPI 2.2.1 specification)
python run_tests.py compliance

# Performance tests (load and scalability)
python run_tests.py performance

# Quick test suite (unit + integration)
python run_tests.py quick
```

#### Test Reports

After running tests, reports are generated in `testing/tests/reports/`:
- **HTML Report**: `testing/tests/reports/report.html`
- **Coverage Report**: `testing/tests/reports/coverage/index.html`
- **JUnit XML**: `testing/tests/reports/junit.xml` (for CI/CD)

### 🔧 Configuration (Educational Demo)

#### Authentication Tokens

- **EMSP Token A**: `emsp_token_a_12345`
- **CPO Token C**: `cpo_token_c_abcdef`

#### Service Ports

- **EMSP Backend**: 8000
- **Mock CPO Server**: 8001

#### Environment Variables

```bash
PROJECT_NAME="OCPI EMSP Backend"
OCPI_HOST="http://localhost:8000"
COUNTRY_CODE="US"
PARTY_ID="EMS"
```

### 🔍 Troubleshooting (Educational Demo)

#### Common Issues

1. **Services won't start**:

   ```bash
   # Check if ports are in use
   lsof -i :8000
   lsof -i :8001

   # Kill existing processes
   kill -9 <PID>
   ```

2. **Import errors**:

   ```bash
   # Install dependencies
   pipenv install

   # Validate framework
   python test_framework_validation.py
   ```

3. **Test failures**:

   ```bash
   # Check service status
   python ocpi_menu.py

   # Run specific tests
   python run_tests.py unit -v
   ```

#### Getting Help

- **Check logs**: `tail -f ocpi_demo.log`
- **Validate setup**: `python test_framework_validation.py`
- **View reports**: Open `testing/tests/reports/report.html`
- **Interactive help**: `python ocpi_menu.py`

### 📖 Learning Resources (Educational Demo)

#### Official OCPI Resources

- [OCPI 2.2.1 Specification](https://evroaming.org/)
- [OCPI GitHub](https://github.com/ocpi/ocpi)
- [EVRoaming Foundation](https://evroaming.org/)

#### Key OCPI Concepts

- **EMSP**: E-Mobility Service Provider (charging apps/services)
- **CPO**: Charge Point Operator (charging station operators)
- **Token**: User authentication credential (RFID, app)
- **CDR**: Charge Detail Record (billing information)
- **Location**: Charging station with EVSEs and connectors

#### OCPI Message Flow

1. **Credential Exchange** (establish trust)
2. **Location Discovery** (find charging stations)
3. **Token Authorization** (validate users)
4. **Session Management** (control charging)
5. **CDR Exchange** (billing information)

## 🎉 Success Criteria (Educational Demo)

After completing the educational demos, you should understand:

### OCPI Protocol Fundamentals

- How EMSP and CPO systems communicate
- Token-based authentication mechanisms
- OCPI 2.2.1 message structures

### EV Charging Ecosystem

- Roles of different actors (EMSP, CPO, MSP)
- Real-world charging workflows
- Business relationships and data flows

### Technical Implementation

- REST API design patterns
- Authentication and authorization
- Real-time communication patterns

### Testing and Validation

- How to test OCPI implementations
- Compliance validation techniques
- Performance testing approaches

## 🤝 Contributing (Educational Demo)

This educational platform is designed to help newcomers understand OCPI.
Contributions that improve the learning experience are welcome:

1. **Educational Content**: Add more demos or explanations
2. **Test Coverage**: Expand test scenarios
3. **Documentation**: Improve guides and troubleshooting
4. **Bug Fixes**: Fix issues that hinder learning

## 📄 License (Educational Demo)

This educational project is provided under the MIT License to encourage learning and
experimentation in the EV charging ecosystem.

---

# OCPI EMSP Backend Testing Framework

A comprehensive testing framework for the OCPI-compliant EMSP (E-Mobility Service Provider) backend, designed to simulate and validate bidirectional interactions with CPO (Charge Point Operator) systems.

## 🎯 Overview (Testing Framework)

This testing framework provides:

- **Mock CPO Server**: Complete CPO backend simulation using extrawest_ocpi library
- **Integration Tests**: End-to-end validation of EMSP-CPO interactions
- **Compliance Tests**: OCPI 2.2.1 specification adherence validation
- **Performance Tests**: Load testing and scalability validation
- **Unit Tests**: Individual component testing
- **Automated CI/CD**: Ready for continuous integration pipelines

## 📁 Project Structure (Testing Framework)

```
testing/
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

## 🚀 Quick Start (Testing Framework)

### 1. Install Dependencies

```bash
# Install test dependencies
pip install -r requirements.txt

# Or use the test runner
python testing/run_tests.py --install-deps
```

### 2. Run Tests

```bash
# Run all tests
python testing/run_tests.py

# Run specific test types
python testing/run_tests.py unit
python testing/run_tests.py integration
python testing/run_tests.py compliance
python testing/run_tests.py performance

# Run quick tests (unit + integration)
python testing/run_tests.py quick

# Run with options
python testing/run_tests.py all --parallel --verbose
```

### 3. View Reports

After running tests, reports are generated in `testing/tests/reports/`:

- **HTML Report**: `testing/tests/reports/report.html` - Detailed test results
- **Coverage Report**: `testing/tests/reports/coverage/index.html` - Code coverage analysis
- **JUnit XML**: `testing/tests/reports/junit.xml` - CI/CD integration format

## 🧪 Test Categories (Testing Framework)

### Integration Tests

End-to-end tests that validate complete OCPI workflows:

```bash
# Run integration tests
pytest -m integration

# Specific integration test files
pytest testing/tests/integration/test_authentication.py
pytest testing/tests/integration/test_data_synchronization.py
pytest testing/tests/integration/test_command_flows.py
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
pytest testing/tests/unit/test_authentication.py
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
pytest testing/tests/compliance/ --html=compliance_report.html
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

## 🔧 Configuration (Testing Framework)

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

Key fixtures available in `testing/tests/conftest.py`:

- `emsp_app`: EMSP FastAPI application
- `mock_cpo_app`: Mock CPO FastAPI application
- `emsp_client`: Synchronous test client for EMSP
- `mock_cpo_client`: Synchronous test client for Mock CPO
- `async_emsp_client`: Async test client for EMSP
- `async_mock_cpo_client`: Async test client for Mock CPO
- `test_data_factory`: Test data generator
- `emsp_auth_headers`: EMSP authentication headers
- `cpo_auth_headers`: CPO authentication headers

## 📊 Mock CPO Server (Testing Framework)

The Mock CPO server (`testing/tests/mock_cpo_server.py`) provides:

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

## 🏭 Test Data Factory (Testing Framework)

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

## 🔍 Running Specific Tests (Testing Framework)

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
pytest testing/tests/integration/test_authentication.py

# Specific test class
pytest testing/tests/integration/test_authentication.py::TestOCPIAuthentication

# Specific test method
pytest testing/tests/integration/test_authentication.py::TestOCPIAuthentication::test_emsp_token_validation
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

## 📈 CI/CD Integration (Testing Framework)

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
      run: python testing/run_tests.py all --parallel
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: testing/tests/reports/coverage.xml
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
                sh 'python testing/run_tests.py all --parallel'
            }
        }
        stage('Publish Results') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'testing/tests/reports',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
                publishCoverage adapters: [
                    coberturaAdapter('testing/tests/reports/coverage.xml')
                ]
            }
        }
    }
}
```

## 🐛 Troubleshooting (Testing Framework)

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
   pytest testing/tests/path/to/test.py::test_name -v
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
pytest testing/tests/integration/test_authentication.py::test_emsp_token_validation -v -s
```

## 📚 Additional Resources (Testing Framework)

- [OCPI 2.2.1 Specification](https://evroaming.org/app/uploads/2021/11/OCPI-2.2.1.pdf)
- [extrawest_ocpi Documentation](https://github.com/extrawest/extrawest_ocpi)
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

## 🤝 Contributing (Testing Framework)

1. Add new tests following the existing patterns
2. Update test data factory for new OCPI objects
3. Ensure compliance tests cover new features
4. Add performance tests for critical paths
5. Update documentation for new test categories

## 📄 License (Testing Framework)

This testing framework follows the same license as the main EMSP backend project.
