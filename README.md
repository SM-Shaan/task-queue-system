# Asynchronous Task Processing System

This project is divided into various chapter, Each chapter show various implementation with techonology tools. 

# Introduction

A robust distributed task processing system built with Flask, Celery, and Docker. This system provides priority-based task routing, automatic retries with exponential backoff, and real-time task monitoring.

## Table of Contents

- [Project Overview](#-project-overview)
- [System Architecture](#-system-architecture)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [Monitoring & Management](#-monitoring--management)
- [Deployment](#-deployment)
- [Error Handling](#-error-handling)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Project Overview

This project is divided into various chapters, each demonstrating different implementation approaches and deployment strategies:

- **Chapter 1**: Local machine and Poridhi lab implementation ([Read more](README.md))
- **Chapter 2**: AWS deployment steps ([Read more](DOC/Lab-02/aws-deployment.md))
- **Chapter 3**: Multi-EC2 instance deployment using Pulumi ([Read more](DOC\Lab-03\pulumi.md))

## 🏗️ System Architecture

### 1. High-Level System Architecture
![Priority Queue System diagram](DOC/Lab-01/images/archi.drawio.svg)

### 2. Client Interaction Flow
![Process Dataflow Sequence diagram](DOC/Lab-01/images/Dataflow.drawio.svg)
The sequence diagram shows the complete lifecycle of a task from submission to status check:
1. Client submits a task via POST request to Flask API
2. Flask receives the request and queues the task in RabbitMQ
3. RabbitMQ delivers the task to an appropriate worker
4. Worker processes the task and stores the result in Redis
5. Client can check task status via GET request
6. Flask queries Redis for the task status
7. Status is returned to the client

###  3. Priority Queue System
![Priority Queue System diagram](DOC/Lab-01/images/priorityqueue.drawio.svg)

The priority queue system routes tasks based on their priority:
- **High Priority Queue**: For urgent tasks that need immediate processing
- **Normal Priority Queue**: For standard tasks
- **Low Priority Queue**: For background tasks that can be processed when resources are available


###  4. Worker Processing Flow
![Priority Queue System diagram](DOC/Lab-01/images/taskflow.svg)

Task lifecycle within a worker:
- **Initial State**: Task arrives in the "Received" state
- **Processing State**: Worker begins processing the task
- **Success Path**: If processing completes successfully, result is stored
- **Error Path**: If an error occurs, task enters "Failed" state
- **Retry Logic**: Failed tasks enter "Retrying" state with exponential backoff
- **Final States**: Task either completes successfully or fails after max retries

### 5. Task Types and Workers
![Priority Queue System diagram](DOC/Lab-01/images/task_worker.drawio.svg)

Specialized workers for different task types:
- **Data Processing Tasks**: Handled by Data Worker
- **Email Tasks**: Handled by Email Worker
- **File Processing Tasks**: Handled by File Worker

### 6. Monitoring System
![Priority Queue System diagram](DOC/Lab-01/images/workerTask.drawio.svg)
Real-time monitoring capabilities:
- Task Metrics: Performance and processing statistics
- Worker Status: Health and availability of workers
- System health checks
- Performance monitoring
- Resource utilization tracking
- Problem detection and resolution

### 7. Error Handling Flow
![Priority Queue System diagram](DOC/Lab-01/images/taskflow.drawio.svg)
This diagram details the error handling process:
When an error occurs, it triggers the retry logic
Retry Logic implements exponential backoff strategy
Backoff calculation determines wait time between retries
Max Retries Check ensures system doesn't get stuck in retry loops
Error Logging captures all error information for debugging
This flow ensures:
Graceful handling of failures
Systematic retry attempts
Proper error documentation
System stability under error conditions

Error handling process:
- Retry logic with exponential backoff
- Max retries check
- Comprehensive error logging
- Graceful failure handling

## 🚀 Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+

### Installation

1. Clone the repository:
```bash
git clone git@github.com:poridhioss/asynchronous_task_processing_system_using_Flask_Celery_RabbitMQ.git
cd task_system
```

2. Set up Python environment:
```bash
# For Poridhi lab
apt-get update
apt-get install -y python3-venv

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Start the services:
```bash
docker-compose up -d
```

### Poridhi Lab Setup

1. Access the application through load balancer:

![Load Balancer Setup](DOC/Lab-01/images/poridhilab.png)

2. Configure IP and port:
- Get IP using `ifconfig`
- Use application port from Dockerfile

3. Create load balancer in Poridhi lab:

![Load Balancer Configuration](DOC/Lab-01/images/poridhilab2.png)

4. Configure with your application's IP and port:

![Load Balancer Details](DOC/Lab-01/images/poridhilab3.png)

![Load Balancer Final Setup](DOC/Lab-01/images/poridhilab4.png)

## Usage

### API Endpoints
1. **Submit a Task**
Open Postman application. Then, follow the following commands:
```
POST http://localhost:5000/api/tasks
```
#### For Poridhi lab 
Adjust the address according to yours:
```
POST https://67ac2c9d1fcfb0b6f0fdcee7-lb-800.bm-southeast.lab.poridhi.io/api/tasks/1a985c56-503f-4ad9-82ae-8b51897d6f3e 
```
You can see:
![alt text](DOC/Lab-01/images/poridhilab5.png)
**Headers:**
```
Content-Type: application/json
```

**Request Body:**
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
**Using curl:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "data_processing",
    "priority": "high",
    "parameters": {
      "data": "test data"
    },
    "delay": 0
  }'
```

#### 2. Check Task Status

**Local Environment:**
```bash
GET http://localhost:5000/api/tasks/<task_id>
```
**Poridhi Lab:**

Adjust the address according to yours:
```
GET https://67ac2c9d1fcfb0b6f0fdcee7-lb-800.bm-southeast.lab.poridhi.io/api/tasks/<task_id>
```
You can see:
![alt text](DOC/Lab-01/images/poridhilab6.png)
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

![alt text](DOC/Lab-01/images/poridhilab7.png)

## RabbitMQ Management UI
- Access at: `http://localhost:15672`
- Default credentials: guest/guest
- Monitor queues, exchanges, and connections
 
![alt text](DOC/Lab-01/images/poridhilab8.png)

For poridhi lab, click on the respective load balancer link for FLower & RaabitMq Management UI. Look at the images for examples.

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

## ⚙️ Configuration

### Core Components Setup

1. **Flask Application (app.py)**
```python
from flask import Flask, request, jsonify
from celery import Celery
from redis import Redis

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@rabbitmq:5672//'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)
```

2. **Celery Configuration (celery_config.py)**
```python
from kombu import Exchange, Queue

# Define exchanges
default_exchange = Exchange('default', type='direct')
high_priority_exchange = Exchange('high_priority', type='direct')

# Define queues
task_queues = (
    Queue('high_priority', high_priority_exchange, routing_key='high'),
    Queue('normal_priority', default_exchange, routing_key='normal'),
    Queue('low_priority', default_exchange, routing_key='low'),
)

# Celery configuration
broker_url = 'amqp://guest:guest@rabbitmq:5672//'
result_backend = 'redis://redis:6379/0'
task_queues = task_queues
task_routes = {
    'tasks.high_priority': {'queue': 'high_priority'},
    'tasks.normal_priority': {'queue': 'normal_priority'},
    'tasks.low_priority': {'queue': 'low_priority'},
}
```

3. **Task Definitions (tasks.py)**

```python
from celery import Task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

class BaseTask(Task):
    abstract = True
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f'Task {task_id} failed: {exc}')
        # Implement retry logic here

@celery.task(base=BaseTask, bind=True, max_retries=3)
def process_task(self, task_type, parameters):
    try:
        # Task processing logic
        result = process_task_logic(task_type, parameters)
        return result
    except Exception as exc:
        self.retry(exc=exc, countdown=2 ** self.request.retries)
```

4. **Docker Compose (docker-compose.yml)**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - rabbitmq
      - redis
    environment:
      - CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

  worker:
    build: .
    command: celery -A tasks worker --loglevel=info
    depends_on:
      - rabbitmq
      - redis
    environment:
      - CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```

### Environment Variables

Create a `.env` file in your project root:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

# Celery Configuration
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# RabbitMQ Configuration
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

### Error Handling Configuration

```python
# Error handling configuration in tasks.py
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 60  # seconds

def get_retry_delay(retry_count):
    return min(INITIAL_RETRY_DELAY * (2 ** retry_count), MAX_RETRY_DELAY)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Look on the next chapter --> Link to readme file of the chapter 2

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
