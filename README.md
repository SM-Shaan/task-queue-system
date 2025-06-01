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
- **Chapter 2**: AWS deployment steps (single EC2 instance) ([Read more](DOC/Lab-02/aws-deployment.md))
- **Chapter 3**: Multi-EC2 instance deployment using Pulumi ([Read more](DOC\Lab-03\pulumi.md))

## 🏗️ System Architecture

### 1. High-Level System Architecture
![Priority Queue System diagram](./DOC/Lab-01/images/archi.drawio.svg)

### 2. Client Interaction Flow
![Process Dataflow Sequence diagram](./DOC/Lab-01/images/Dataflow.drawio.svg)
The sequence diagram shows the complete lifecycle of a task from submission to status check:
1. Client submits a task via POST request to Flask API
2. Flask receives the request and queues the task in RabbitMQ
3. RabbitMQ delivers the task to an appropriate worker
4. Worker processes the task and stores the result in Redis
5. Client can check task status via GET request
6. Flask queries Redis for the task status
7. Status is returned to the client

###  3. Priority Queue System
![Priority Queue System diagram](./DOC/Lab-01/images/priorityqueue.drawio.svg)

The priority queue system routes tasks based on their priority:
- **High Priority Queue**: For urgent tasks that need immediate processing
- **Normal Priority Queue**: For standard tasks
- **Low Priority Queue**: For background tasks that can be processed when resources are available


###  4. Worker Processing Flow
![Priority Queue System diagram](./DOC/Lab-01/images/taskflow.svg)

Task lifecycle within a worker:
- **Initial State**: Task arrives in the "Received" state
- **Processing State**: Worker begins processing the task
- **Success Path**: If processing completes successfully, result is stored
- **Error Path**: If an error occurs, task enters "Failed" state
- **Retry Logic**: Failed tasks enter "Retrying" state with exponential backoff
- **Final States**: Task either completes successfully or fails after max retries

### 5. Task Types and Workers
![Priority Queue System diagram](./DOC/Lab-01/images/task_worker.drawio.svg)

Specialized workers for different task types:
- **Data Processing Tasks**: Handled by Data Worker
- **Email Tasks**: Handled by Email Worker
- **File Processing Tasks**: Handled by File Worker

### 6. Monitoring System
![Priority Queue System diagram](./DOC/Lab-01/images/workerTask.drawio.svg)
Real-time monitoring capabilities:
- Task Metrics: Performance and processing statistics
- Worker Status: Health and availability of workers
- System health checks
- Performance monitoring
- Resource utilization tracking
- Problem detection and resolution

### 7. Error Handling Flow
![Priority Queue System diagram](./DOC/Lab-01/images/taskflow.drawio.svg)
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

![Load Balancer Setup](./DOC/Lab-01/images/poridhilab.png)

2. Configure IP and port:
- Get IP from eth0 using `ifconfig`
- Use application port from Dockerfile

3. Create load balancer in Poridhi lab:

![Load Balancer Configuration](./DOC/Lab-01/images/poridhilab2.png)


4. Configure with your application's IP and port:

    Enter the taken IP with each port (FastApi, RabbitMq UI, Flower). 

![Load Balancer Details](./DOC/Lab-01/images/poridhilab3.png)

![Load Balancer Final Setup](./DOC/Lab-01/images/poridhilab4.png)

## Usage

### API Endpoints
1. **Submit a Task**
Open Postman application. Then, follow the following commands:
```
POST http://localhost:5000/api/tasks
```
#### For Poridhi lab 
Adjust the address according to yours:

Domain name for a load balancer in the Poridhi lab environment (For 5000 port): 67ac2c9d1fcfb0b6f0fdcee7-lb-800.bm-southeast.lab.poridhi.io 
```
POST https://67ac2c9d1fcfb0b6f0fdcee7-lb-800.bm-southeast.lab.poridhi.io/api/tasks
```
You can see:
![alt text](./DOC/Lab-01/images/poridhilab5.png)
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
![alt text](./DOC/Lab-01/images/poridhilab6.png)
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

**Poridhi Lab:**

![alt text](./DOC/Lab-01/images/poridhilab7.png)

## RabbitMQ Management UI
- Access at: `http://localhost:15672`
- Default credentials: guest/guest
- Monitor queues, exchanges, and connections
 
 **Poridhi Lab:**

![alt text](./DOC/Lab-01/images/poridhilab8.png)

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
from flask_cors import CORS
from tasks import process_task, get_task_status, celery_app, submit_task_with_priority
import os
from dotenv import load_dotenv
import logging
import traceback
from celery.result import AsyncResult

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure Flask to handle trailing slashes
app.url_map.strict_slashes = False

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Task Processing System API',
        'endpoints': {
            'submit_task': '/api/tasks (POST)',
            'get_task': '/api/tasks/<task_id> (GET)'
        }
    })

@app.route('/api/tasks', methods=['POST', 'OPTIONS'])
def submit_task():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        task_type = data.get('task_type')
        priority = data.get('priority', 'normal')
        parameters = data.get('parameters', {})
        delay = data.get('delay', 0)
        
        if not task_type:
            return jsonify({'error': 'task_type is required'}), 400
            
        if not isinstance(delay, (int, float)) or delay < 0:
            return jsonify({'error': 'delay must be a non-negative number'}), 400
            
        app.logger.info(f"Submitting task: type={task_type}, priority={priority}, parameters={parameters}, delay={delay}")
        
        # Submit task with priority-based routing
        task = submit_task_with_priority(
            task_type=task_type,
            priority=priority,
            parameters=parameters,
            delay=delay
        )
        
        app.logger.info(f"Task submitted successfully: {task.id}")
        return jsonify({
            'task_id': task.id,
            'status': 'pending',
            'message': f'Task submitted successfully. Will start in {delay} seconds.'
        }), 202
        
    except Exception as e:
        app.logger.error(f"Error submitting task: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['GET', 'OPTIONS'])
def get_task(task_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        status = get_task_status(task_id)
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'details': {
                'traceback': traceback.format_exc()
            }
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested URL was not found on the server',
        'path': request.path
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(error),
        'details': {
            'traceback': traceback.format_exc()
        }
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

2. **Celery Configuration (celery_config.py)**
```python
from kombu import Exchange, Queue
import os

broker_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
result_backend = os.getenv('REDIS_URL', 'redis://redis:6379/0')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

worker_prefetch_multiplier = 1 # Number of tasks to prefetch
worker_max_tasks_per_child = 1000 # Number of tasks a worker can process before being replaced
worker_max_memory_per_child = 200000 # Maximum memory a worker can use before being replaced
worker_pool = 'solo' # Use solo pool for debugging
worker_concurrency = 1 # Number of concurrent tasks a worker can process
worker_send_task_events = True # Send task events to the broker
task_send_sent_event = True # Send task sent events to the broker

task_queues = (
    Queue('default', Exchange('default', type='direct'), routing_key='default'),
    Queue('high_priority', Exchange('high_priority', type='direct'), routing_key='high_priority'),
    Queue('low_priority', Exchange('low_priority', type='direct'), routing_key='low_priority'),
    Queue('data_processing', Exchange('data_processing', type='direct'), routing_key='data_processing'),
    Queue('email_sending', Exchange('email_sending', type='direct'), routing_key='email_sending'),
    Queue('file_processing', Exchange('file_processing', type='direct'), routing_key='file_processing'),
)

task_queues = tuple(
    Queue(
        queue.name,
        Exchange(queue.exchange.name, type=queue.exchange.type, durable=True),
        routing_key=queue.routing_key,
        durable=True
    )
    for queue in task_queues
)

task_routes = {
    'tasks.process_task': {
        'queue': 'default',
        'routing_key': 'default'
    }
}

# Add task-specific routing
task_routes.update({
    'tasks.process_data_task': {'queue': 'data_processing', 'routing_key': 'data_processing'},
    'tasks.send_email_task': {'queue': 'email_sending', 'routing_key': 'email_sending'},
    'tasks.process_file_task': {'queue': 'file_processing', 'routing_key': 'file_processing'},
})

# Configure task retry policy
task_annotations = {
    'tasks.process_task': {
        'rate_limit': '10/s',
        'retry_backoff': True,
        'retry_backoff_max': 600,  # Maximum retry delay in seconds
        'max_retries': 3,  # Maximum number of retries
        'retry_jitter': True  # Add jitter to prevent thundering herd
    }
}

task_acks_late = True
task_reject_on_worker_lost = True
task_track_started = True
task_time_limit = 3600
task_soft_time_limit = 3300
task_create_missing_queues = True

broker_connection_retry = True
broker_connection_retry_on_startup = True
broker_connection_max_retries = 5
broker_heartbeat = 10
broker_connection_timeout = 30

task_track_started = True
task_ignore_result = False
task_store_errors_even_if_ignored = True s
```

3. **Task Definitions (tasks.py)**

```python
from celery import Celery
from celery.signals import task_failure, task_success
import os
from dotenv import load_dotenv
import time
import logging
import traceback
import json
from celery.utils.log import get_task_logger
import random

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

celery_app = Celery('tasks')
celery_app.config_from_object('celeryconfig')

task_logger = get_task_logger(__name__)

class TaskError(Exception):
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details or {}

    def to_dict(self):
        return {
            'error': str(self),
            'details': self.details
        }

def process_data_task(parameters):
    task_logger.debug(f"Processing data task with parameters: {parameters}")
    time.sleep(2)  # Simulate work
    return {'processed': True, 'data': parameters}

def send_email_task(parameters):
    task_logger.debug(f"Processing email task with parameters: {parameters}")
    time.sleep(1)  # Simulate work
    return {'sent': True, 'to': parameters.get('to')}

def process_file_task(parameters):
    task_logger.debug(f"Processing file task with parameters: {parameters}")
    time.sleep(3)  # Simulate work
    return {'processed': True, 'filename': parameters.get('filename')}

@celery_app.task(name='tasks.process_task', bind=True)
def process_task(self, task_type, priority='normal', parameters=None, delay=0):
    task_logger.info(f"Starting task processing: type={task_type}, priority={priority}, parameters={parameters}, delay={delay}")
    
    try:
        if not isinstance(task_type, str):
            raise TaskError("task_type must be a string")
        
        if not isinstance(priority, str):
            raise TaskError("priority must be a string")
            
        if parameters is not None and not isinstance(parameters, dict):
            raise TaskError("parameters must be a dictionary or None")
            
        if not isinstance(delay, (int, float)) or delay < 0:
            raise TaskError("delay must be a non-negative number")
        
        # Update task state to STARTED
        self.update_state(state='STARTED', meta={'status': 'Task processing started'})
        
        # Simulate random failure (10% chance)
        if random.random() < 0.1:
            raise TaskError("Random task failure simulation")
        
        try:
            # Route to specific task handler based on task_type
            if task_type == 'data_processing':
                result = process_data_task(parameters or {})
            elif task_type == 'email_sending':
                result = send_email_task(parameters or {})
            elif task_type == 'file_processing':
                result = process_file_task(parameters or {})
            else:
                raise TaskError(f"Unknown task type: {task_type}")
        except Exception as exc:
            # Calculate retry delay with exponential backoff
            retry_delay = min(2 ** self.request.retries * 60, 600)  # Max 10 minutes
            task_logger.warning(f"Task failed, retrying in {retry_delay} seconds. Error: {str(exc)}")
            raise self.retry(exc=exc, countdown=retry_delay)
        
        task_logger.info(f"Task completed successfully: {result}")
        return {
            'status': 'completed',
            'result': result,
            'task_type': task_type,
            'priority': priority,
            'delay': delay
        }
    
    except TaskError as exc:
        task_logger.error(f"Task failed: {str(exc)}")
        # Raise the exception to properly mark the task as failed
        raise exc
    except Exception as exc:
        task_logger.error(f"Task failed: {str(exc)}\n{traceback.format_exc()}")
        # Raise the exception to properly mark the task as failed
        raise TaskError(str(exc), {'traceback': traceback.format_exc()})

def submit_task_with_priority(task_type, priority='normal', parameters=None, delay=0):
    """Submit a task with priority-based routing."""
    queue = {
        'high': 'high_priority',
        'low': 'low_priority',
        'normal': 'default'
    }.get(priority, 'default')
    
    return process_task.apply_async(
        args=[task_type, priority, parameters, delay],
        queue=queue,
        routing_key=queue
    )

def get_task_status(task_id):
    try:
        task = celery_app.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Task is waiting for execution or unknown',
                'info': task.info if task.info else None
            }
        elif task.state == 'STARTED':
            response = {
                'state': task.state,
                'status': 'Task has been started',
                'info': task.info if task.info else None
            }
        elif task.state == 'RETRY':
            response = {
                'state': task.state,
                'status': 'Task is being retried',
                'info': task.info if task.info else None
            }
        elif task.state == 'FAILURE':
            error_info = task.info
            if isinstance(error_info, dict):
                response = {
                    'state': task.state,
                    'status': error_info.get('error', 'Task failed'),
                    'details': error_info.get('details', {})
                }
            else:
                response = {
                    'state': task.state,
                    'status': str(error_info),
                    'details': {}
                }
        else:
            response = {
                'state': task.state,
                'status': task.info if task.info else 'Task completed',
                'result': task.info if task.info else None
            }
        task_logger.debug(f"Task status for {task_id}: {response}")
        return response
    except Exception as e:
        task_logger.error(f"Error getting task status: {str(e)}")
        return {
            'state': 'ERROR',
            'status': str(e),
            'details': {
                'traceback': traceback.format_exc()
            }
        }

@task_failure.connect
def handle_task_failure(task_id, exception, args, kwargs, traceback, einfo, **kw):
    task_logger.error(f"Task {task_id} failed with error: {exception}")
    task_logger.error(f"Task args: {args}")
    task_logger.error(f"Task kwargs: {kwargs}")
    task_logger.error(f"Traceback: {traceback}")

@task_success.connect
def handle_task_success(result, **kw):
    task_logger.info(f"Task completed successfully: {result}")
```

4. **Docker Compose (docker-compose.yml)**
```yaml
services:
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"   # AMQP protocol port
      - "15672:15672" # Management UI port (optional, restrict in production)
    environment:
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_USER:-guest}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASS:-guest}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_port_connectivity"]
      interval: 30s
      timeout: 10s
      retries: 5

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  web:
    build:
      context: .
      dockerfile: Dockerfile.web
    image: myapp-web:latest
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=development  # Use development for local testing
      - RABBITMQ_URL=amqp://${RABBITMQ_USER:-guest}:${RABBITMQ_PASS:-guest}@rabbitmq:5672/
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      rabbitmq:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - .:/app:ro  # Read-only for production, but can be writable locally
    entrypoint: ["sh", "-c", "python3 init_queues.py && flask run --host=0.0.0.0 --port=5000"]
    

    x-worker-template: &worker-template
        build:
          context: ..
          dockerfile: ../Dockerfile.worker
        # image: myapp-worker:latest
        #     command: celery -A tasks worker --loglevel=info -Q default,high_priority,low_priority
        environment:
          - CELERY_BROKER_URL=amqp://${RABBITMQ_USER:-guest}:${RABBITMQ_PASS:-guest}@rabbitmq:5672/
          - CELERY_RESULT_BACKEND=redis://redis:6379/0
        depends_on:
          - rabbitmq
          - redis
        volumes:
          - ./worker:/app:ro

    worker: 
    <<: *worker-template
    command: celery -A tasks worker --loglevel=info -Q default,high_priority,low_priority
    

  data_worker:
    <<: *worker-template
    command: celery -A tasks worker --loglevel=info -Q data_processing

  email_worker:
    <<: *worker-template
    command: celery -A tasks worker --loglevel=info -Q email_sending

  file_worker:
    <<: *worker-template
    command: celery -A tasks worker --loglevel=info -Q file_processing

  flower:
    build:
      context: .
      dockerfile: Dockerfile.flower
    image: myapp-flower:latest
    ports:
      - "5555:5555"
    environment:
      - RABBITMQ_URL=amqp://${RABBITMQ_USER:-guest}:${RABBITMQ_PASS:-guest}@rabbitmq:5672/
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      rabbitmq:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  rabbitmq_data:
  redis_data:
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

### Dockerfile.web
```python
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
```
### Dockerfile.worker
```python
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
CMD ["sh", "-c", "python3 init_queues.py && celery -A tasks worker --loglevel=info"]
```
### Dockerfile.flower
```python
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt flower

COPY . .

EXPOSE 5555

CMD ["celery", "-A", "tasks", "flower", "--port=5555"]
```

### init_queues

```python
import pika
import time
import os
from celeryconfig import task_queues

def init_queues():
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672//')
    
    parameters = pika.URLParameters(rabbitmq_url)
    
    # Try to connect to RabbitMQ
    max_retries = 5
    retry_interval = 5
    
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            for queue in task_queues:
                channel.exchange_declare(
                    exchange=queue.exchange.name,
                    exchange_type=queue.exchange.type,
                    durable=True
                )
                
                channel.queue_declare(
                    queue=queue.name,
                    durable=True
                )
                
                channel.queue_bind(
                    exchange=queue.exchange.name,
                    queue=queue.name,
                    routing_key=queue.routing_key
                )
                
                print(f"Created queue: {queue.name}")
            
            connection.close()
            print("Successfully initialized all queues")
            return True
            
        except pika.exceptions.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Failed to connect to RabbitMQ (attempt {attempt + 1}/{max_retries}). Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                print(f"Failed to connect to RabbitMQ after {max_retries} attempts")
                raise e

if __name__ == '__main__':
    init_queues() 
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

### Keep in mind
1. Remove Unnecessary Volumes in Production: 
- Mounting the entire project as a volume (- .:/app:ro) is only needed for local development.
- For production, build the image with only the required files and remove the volume mounts.

2. Scaling Celery Worker

3. 

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Look on the next chapter --> Link to readme file of the chapter 2

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
