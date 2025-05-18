# Asynchronous Task Processing System

A robust task processing system built with Flask, Celery, RabbitMQ, and Redis. This system supports multiple task types, priorities, and provides comprehensive task management capabilities.

## Features

- **Multiple Task Types Support**
  - Data Processing
  - Email Sending
  - File Processing
  - Custom task types can be added

- **Priority-based Task Processing**
  - High Priority Queue
  - Normal Priority Queue
  - Low Priority Queue

- **Comprehensive Task Management**
  - Task submission with priority
  - Real-time task status monitoring
  - Task filtering by state and type
  - Task history management
  - Queue management

- **Robust Error Handling**
  - Automatic retries for failed tasks
  - Detailed error logging
  - Task failure notifications


![System Architecture](images/Architectural%20Diagram.png)


## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- RabbitMQ
- Redis

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task_system
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

4. Create a `.env` file in the project root:
```env
FLASK_APP=app.py
FLASK_ENV=development
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//
REDIS_URL=redis://redis:6379/0
```

## Monitoring

### RabbitMQ Management UI
- Access at: http://localhost:15672
- Default credentials: guest/guest
- Monitor queues, exchanges, and connections

### Redis Monitoring
- Monitor task results and states
- View task history and statistics


## Running the System

1. Start all services using Docker Compose:
```bash
docker-compose up --build
```

This will start:
- Flask application (port 5000)
- Celery worker
- RabbitMQ (port 5672, management UI port 15672)
- Redis (port 6379)

## API Documentation

Open Postman application. Then, follow the following commands:
```
POST http://localhost:5000/api/tasks
```
In header section:
```
Content-Type: application/json
```
### 1. Submit a Task
In body section:
```http


{
    "task_type": "data_processing",
    "priority": "high",
    "parameters": {
        "data": "example data"
    }
}
```

Response:
```json
{
    "task_id": "task-uuid",
    "status": "submitted",
    "message": "Task has been submitted successfully",
    "queue": "high_priority"
}
```

### 2. Get Task Status
```http
GET /api/tasks/{task_id}
```

Response:
```json
{
    "state": "SUCCESS",
    "status": {
        "priority": "high",
        "result": {
            "data": {
                "data": "example data"
            },
            "processed": true
        },
        "status": "completed",
        "task_type": "data_processing"
    }
}
```

### 3. List Tasks
```http
GET /api/tasks?state=SUCCESS&type=active
```

Query Parameters:
- `state`: Filter by task state (PENDING, STARTED, SUCCESS, FAILURE, RETRY)
- `type`: Filter by task type (active, reserved, scheduled, completed)

Response:
```json
{
    "tasks": [...],
    "total": 10,
    "filters": {
        "state": "SUCCESS",
        "type": "active"
    },
    "available_filters": {
        "states": ["PENDING", "STARTED", "SUCCESS", "FAILURE", "RETRY"],
        "types": ["active", "reserved", "scheduled", "completed"]
    }
}
```

### 4. Purge Task History
```http
POST /api/tasks/purge
```

Response:
```json
{
    "status": "success",
    "message": "All task history has been purged",
    "details": {
        "active_tasks_revoked": 2,
        "reserved_tasks_revoked": 1,
        "scheduled_tasks_revoked": 0,
        "redis_keys_cleared": 15
    }
}
```

## Task Types

### 1. Data Processing
- Processes data with configurable parameters
- Supports high-priority processing

### 2. Email Sending
- Sends emails with customizable templates
- Handles email queue management

### 3. File Processing
- Processes files with configurable options
- Supports different file formats


## Error Handling

The system includes comprehensive error handling:
- Automatic retries for failed tasks
- Detailed error logging
- Task failure notifications
- Queue-level error handling

## Development

### Running Tests
```bash
python test_filtering.py
```

### Adding New Task Types
1. Add new task type to `tasks.py`
2. Update task routing in `celeryconfig.py`
3. Add task-specific error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 