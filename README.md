# Task Processing System

A robust distributed task processing system built with Flask, Celery, and Docker. This system provides priority-based task routing, automatic retries with exponential backoff, and real-time task monitoring.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Monitoring](#monitoring)
- [RabbitMQ Management UI](#rabbitmq-management-ui)
- [Testing](#testing)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Priority-based Task Routing**
  - High priority tasks
  - Normal priority tasks
  - Low priority tasks
  - Each priority level has its own dedicated queue

- **Task Type-specific Processing**
  - Data processing tasks
  - Email sending tasks
  - File processing tasks
  - Dedicated workers for each task type

- **Robust Error Handling**
  - Automatic retry mechanism
  - Exponential backoff strategy
  - Maximum retry attempts configuration
  - Detailed error logging and tracking

- **Real-time Monitoring**
  - Flower dashboard for task monitoring
  - Task status tracking
  - Queue statistics
  - Worker status monitoring

## Architecture

The system consists of the following components:

![System Architecture](images/task.svg)

1. **Web Application (Flask)**
   - RESTful API endpoints
   - Task submission and status checking
   - CORS support
   - Error handling middleware

2. **Task Queue (RabbitMQ)**
   - Message broker
   - Queue management
   - Priority queues
   - Task routing

3. **Result Backend (Redis)**
   - Task result storage
   - Status tracking
   - Result caching

4. **Workers (Celery)**
   - Priority worker (handles high/normal/low priority tasks)
   - Data processing worker
   - Email worker
   - File processing worker

5. **Monitoring (Flower)**
   - Web-based monitoring interface
   - Real-time task tracking
   - Worker status monitoring
   - Queue statistics

## Prerequisites

- Docker
- Docker Compose
- Python 3.8+

## Installation

1. Clone the repository:
```bash
git clone <git@github.com:SM-Shaan/task-queue-system.git>
cd task_system
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Start the services:
```bash
docker-compose up -d
```

## Usage

### API Endpoints
Open Postman application. Then, follow the following commands:
```
POST http://localhost:5000/api/tasks
```
In header section:
```
Content-Type: application/json
```

1. **Submit a Task**
In body section:
```bash
{
    "task_type": "data_processing",
    "priority": "high",
    "parameters": {
        "data": "test data"
    },
    "delay": 0
}
```

2. **Check Task Status**
```bash
GET http://localhost:5000/api/tasks/<task_id>
```

### Task Types

1. **Data Processing**
```json
{
    "task_type": "data_processing",
    "parameters": {
        "data": "your data"
    }
}
```

2. **Email Sending**
```json
{
    "task_type": "email_sending",
    "parameters": {
        "to": "recipient@example.com"
    }
}
```

3. **File Processing**
```json
{
    "task_type": "file_processing",
    "parameters": {
        "filename": "your_file.txt"
    }
}
```

### Priorities

- `high`: Tasks processed immediately
- `normal`: Standard priority tasks
- `low`: Background tasks

## Monitoring

Access the Flower dashboard at `http://localhost:5555` to:
- Monitor task execution
- View queue statistics
- Check worker status
- Track task history

## RabbitMQ Management UI
- Access at: `http://localhost:15672`
- Default credentials: guest/guest
- Monitor queues, exchanges, and connections

## Testing

Run the test suite:
```bash
python test_tasks.py
```

The test suite verifies:
- Priority-based routing
- Task type processing
- Retry functionality
- Error handling

## Configuration

### Celery Configuration (celeryconfig.py)
- Queue definitions
- Task routing
- Retry policies
- Worker settings

### Docker Configuration (docker-compose.yml)
- Service definitions
- Network setup
- Volume mappings
- Environment variables

## Error Handling

The system implements several error handling mechanisms:

![Error Handling diagram](images/error.svg)

1. **Task Retries**
   - Exponential backoff
   - Maximum retry attempts
   - Jitter to prevent thundering herd

2. **Error Logging**
   - Detailed error messages
   - Stack traces
   - Task context information

3. **Status Tracking**
   - Task state monitoring
   - Result storage
   - Error details preservation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
