# Project Repository

This is the initial README file for the project.# RDS Connectivity API

A FastAPI-based service providing API endpoints with Amazon RDS connectivity.

## Project Overview

This project implements a RESTful API service that connects to Amazon RDS (MySQL) database. It provides a robust foundation for building scalable backend services with proper database integration, error handling, and API documentation.

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: MySQL on Amazon RDS
- **ORM**: SQLAlchemy
- **Testing**: pytest
- **API Documentation**: Swagger UI (via FastAPI)
- **Environment Management**: python-dotenv
- **HTTP Server**: uvicorn

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL client libraries
- Access to an Amazon RDS instance

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd -Backend-RDS-connectivity-L.0.2
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Configuration

1. Create a `.env` file in the project root with the following variables:
   ```
   DB_HOST=your-rds-endpoint
   DB_PORT=3306
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_NAME=your-database-name
   DEBUG=False
   ```

2. Ensure your RDS security group allows connections from your application's IP address.

## API Documentation

### Base URL
- Development: `http://localhost:8000`
- Production: Your deployed API endpoint

### Endpoints

#### Health Check
- **GET /** - Root endpoint to verify API is running
  - Response: `{"message": "RDS Connectivity API is running"}`

- **GET /health** - Health check endpoint
  - Response: `{"status": "healthy"}`

### API Documentation UI
- Access the interactive API documentation at `/docs` (Swagger UI)
- Alternative documentation at `/redoc` (ReDoc)

## Testing

### Running Tests

1. Set up a test database and update test environment variables if needed.

2. Run the test suite:
   ```bash
   pytest
   ```

3. Run tests with coverage:
   ```bash
   pytest --cov=app tests/
   ```

### Test Structure
- `tests/conftest.py` - Test configurations and fixtures
- `tests/test_api_integration.py` - API integration tests
- `tests/test_base_crud_service.py` - CRUD service tests
- `tests/test_base_model.py` - Base model tests
- `tests/test_base_schema.py` - Schema validation tests

## Development Guidelines

### Code Structure
```
.
├── app/
│   ├── api/         # API routes and endpoints
│   ├── models/      # SQLAlchemy models
│   ├── schemas/     # Pydantic schemas
│   └── services/    # Business logic
├── tests/           # Test files
├── config.py        # Configuration management
├── main.py         # Application entry point
└── requirements.txt # Project dependencies
```

### Best Practices
1. Follow PEP 8 style guidelines
2. Write docstrings for all public functions and classes
3. Maintain test coverage for new features
4. Use type hints for better code maintainability
5. Handle database operations within service classes
6. Implement proper error handling and validation

### Error Handling
- Database errors are automatically caught and return a 500 response
- Use appropriate HTTP status codes for different error scenarios
- Implement input validation using Pydantic schemas

### Security Considerations
- Store sensitive information in environment variables
- Use proper authentication and authorization (to be implemented)
- Configure CORS settings appropriately for production
- Follow security best practices for database connections

## Deployment

### Production Configuration
1. Set appropriate environment variables
2. Configure CORS with specific allowed origins
3. Enable proper logging
4. Set DEBUG=False in production

### Monitoring
- Implement health checks
- Monitor database connection pool
- Track API response times
- Set up error alerting

## Contributing
1. Create a feature branch
2. Write tests for new features
3. Follow the coding style guidelines
4. Submit a pull request with a clear description

## License
[Add your license information here]
