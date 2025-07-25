# 🚗⚡ OCPI EMSP-CPO Educational Demo Environment

A comprehensive educational platform for learning OCPI (Open Charge Point Interface) 2.2.1 through practical demonstrations and interactive testing.

## 🎯 What is OCPI?

OCPI (Open Charge Point Interface) is a protocol that enables communication between different actors in the EV charging ecosystem:

- **EMSP** (E-Mobility Service Provider): Charging apps and services that EV drivers use
- **CPO** (Charge Point Operator): Companies that own and operate charging stations
- **MSP** (Mobility Service Provider): Roaming services that connect EMSPs and CPOs

This project demonstrates how these systems communicate to provide seamless charging experiences.

## 🏗️ Architecture

```
📱 EMSP Backend (Port 8000)     🔌 Mock CPO Server (Port 8001)
├─ Authentication & Tokens      ├─ Location Management
├─ Session Management           ├─ Token Authorization  
├─ CDR Processing              ├─ Session Monitoring
├─ Command Handling            ├─ Command Execution
└─ Location Discovery          └─ Billing Integration
            │                           │
            └─── OCPI 2.2.1 Protocol ───┘
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Using pipenv (recommended)
pipenv install

# Or using pip
pip install -r requirements.txt
```

### 2. Start the Educational Demo
```bash
# Interactive menu system
python ocpi_menu.py

# Or start services directly
python start_ocpi_demo.py
```

### 3. Explore OCPI Concepts
```bash
# Interactive educational demos
python ocpi_educational_demo.py interactive

# Specific concept demos
python ocpi_educational_demo.py authentication
python ocpi_educational_demo.py locations
python ocpi_educational_demo.py sessions
```

### 4. Run Tests
```bash
# All tests
python run_tests.py

# Specific test types
python run_tests.py unit
python run_tests.py integration
python run_tests.py compliance
```

## 🎓 Educational Features

### Interactive Learning
- **Step-by-step demos** with detailed explanations
- **Real OCPI message flows** with educational commentary
- **Interactive menu system** for guided exploration
- **Troubleshooting guides** for common issues

### Key OCPI Concepts Covered
1. **Authentication & Credential Exchange** - How systems establish trust
2. **Location Discovery** - How EMSPs find charging stations
3. **Token Authorization** - How users get validated for charging
4. **Session Management** - How charging sessions are controlled
5. **CDR Processing** - How billing information is exchanged

### Testing Framework
- **Unit Tests** - Individual component validation
- **Integration Tests** - End-to-end EMSP-CPO interactions
- **Compliance Tests** - OCPI 2.2.1 specification adherence
- **Performance Tests** - Load testing and scalability validation

## 📚 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `ocpi_menu.py` | Interactive menu system | `python ocpi_menu.py` |
| `start_ocpi_demo.py` | Start EMSP/CPO services | `python start_ocpi_demo.py` |
| `ocpi_educational_demo.py` | Educational demonstrations | `python ocpi_educational_demo.py interactive` |
| `run_tests.py` | Test execution | `python run_tests.py [test_type]` |
| `test_framework_validation.py` | Framework validation | `python test_framework_validation.py` |

## 🌐 API Documentation

Once services are running:

- **EMSP Backend**: http://localhost:8000/docs
- **Mock CPO Server**: http://localhost:8001/docs
- **OCPI Endpoints**: 
  - EMSP: http://localhost:8000/ocpi/emsp/2.2.1/versions
  - CPO: http://localhost:8001/ocpi/cpo/2.2.1/versions

## 🧪 Testing

### Test Categories

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

### Test Reports

After running tests, reports are generated in `tests/reports/`:
- **HTML Report**: `tests/reports/report.html`
- **Coverage Report**: `tests/reports/coverage/index.html`
- **JUnit XML**: `tests/reports/junit.xml` (for CI/CD)

## 🔧 Configuration

### Authentication Tokens
- **EMSP Token A**: `emsp_token_a_12345`
- **CPO Token C**: `cpo_token_c_abcdef`

### Service Ports
- **EMSP Backend**: 8000
- **Mock CPO Server**: 8001

### Environment Variables
```bash
PROJECT_NAME="OCPI EMSP Backend"
OCPI_HOST="http://localhost:8000"
COUNTRY_CODE="US"
PARTY_ID="EMS"
```

## 🔍 Troubleshooting

### Common Issues

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

### Getting Help

- **Check logs**: `tail -f ocpi_demo.log`
- **Validate setup**: `python test_framework_validation.py`
- **View reports**: Open `tests/reports/report.html`
- **Interactive help**: `python ocpi_menu.py`

## 📖 Learning Resources

### Official OCPI Resources
- [OCPI 2.2.1 Specification](https://evroaming.org/)
- [OCPI GitHub](https://github.com/ocpi/ocpi)
- [EVRoaming Foundation](https://evroaming.org/)

### Key OCPI Concepts
- **EMSP**: E-Mobility Service Provider (charging apps/services)
- **CPO**: Charge Point Operator (charging station operators)
- **Token**: User authentication credential (RFID, app)
- **CDR**: Charge Detail Record (billing information)
- **Location**: Charging station with EVSEs and connectors

### OCPI Message Flow
1. **Credential Exchange** (establish trust)
2. **Location Discovery** (find charging stations)
3. **Token Authorization** (validate users)
4. **Session Management** (control charging)
5. **CDR Exchange** (billing information)

## 🎉 Success Criteria

After completing the educational demos, you should understand:

✅ **OCPI Protocol Fundamentals**
- How EMSP and CPO systems communicate
- Token-based authentication mechanisms
- OCPI 2.2.1 message structures

✅ **EV Charging Ecosystem**
- Roles of different actors (EMSP, CPO, MSP)
- Real-world charging workflows
- Business relationships and data flows

✅ **Technical Implementation**
- REST API design patterns
- Authentication and authorization
- Real-time communication patterns

✅ **Testing and Validation**
- How to test OCPI implementations
- Compliance validation techniques
- Performance testing approaches

## 🤝 Contributing

This educational platform is designed to help newcomers understand OCPI. Contributions that improve the learning experience are welcome:

1. **Educational Content**: Add more demos or explanations
2. **Test Coverage**: Expand test scenarios
3. **Documentation**: Improve guides and troubleshooting
4. **Bug Fixes**: Fix issues that hinder learning

## 📄 License

This educational project is provided under the MIT License to encourage learning and experimentation in the EV charging ecosystem.

---

**Happy Learning! 🚗⚡**

Start your OCPI journey with: `python ocpi_menu.py`
