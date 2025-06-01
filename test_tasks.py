import requests
import time
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = 'http://13.215.46.60:5000/api'

def submit_task(task_type, priority='normal', parameters=None, delay=0):
    url = f"{BASE_URL}/tasks"
    data = {
        'task_type': task_type,
        'priority': priority,
        'parameters': parameters or {},
        'delay': delay
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['task_id']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error submitting task: {str(e)}")
        return None

def get_task_status(task_id):
    url = f"{BASE_URL}/tasks/{task_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting task status: {str(e)}")
        return None

def wait_for_task_completion(task_id, timeout=30, check_interval=1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        status = get_task_status(task_id)
        if status and status['state'] in ['SUCCESS', 'FAILURE']:
            return status
        time.sleep(check_interval)
    return {'state': 'TIMEOUT', 'status': 'Task did not complete within timeout'}

def test_priority_tasks():
    logger.info("Testing tasks with different priorities...")
    
    # Test high priority task
    high_priority_id = submit_task('data_processing', 'high', {'data': 'high priority test'})
    if high_priority_id:
        status = wait_for_task_completion(high_priority_id)
        logger.info(f"High priority task result: {json.dumps(status, indent=2)}")
    
    # Test normal priority task
    normal_priority_id = submit_task('data_processing', 'normal', {'data': 'normal priority test'})
    if normal_priority_id:
        status = wait_for_task_completion(normal_priority_id)
        logger.info(f"Normal priority task result: {json.dumps(status, indent=2)}")
    
    # Test low priority task
    low_priority_id = submit_task('data_processing', 'low', {'data': 'low priority test'})
    if low_priority_id:
        status = wait_for_task_completion(low_priority_id)
        logger.info(f"Low priority task result: {json.dumps(status, indent=2)}")

def test_task_types():
    logger.info("Testing different task types...")
    
    # Test data processing task
    data_task_id = submit_task('data_processing', 'normal', {'data': 'test data'})
    if data_task_id:
        status = wait_for_task_completion(data_task_id)
        logger.info(f"Data processing task result: {json.dumps(status, indent=2)}")
    
    # Test email task
    email_task_id = submit_task('email_sending', 'normal', {'to': 'test@example.com'})
    if email_task_id:
        status = wait_for_task_completion(email_task_id)
        logger.info(f"Email task result: {json.dumps(status, indent=2)}")
    
    # Test file processing task
    file_task_id = submit_task('file_processing', 'normal', {'filename': 'test.txt'})
    if file_task_id:
        status = wait_for_task_completion(file_task_id)
        logger.info(f"File processing task result: {json.dumps(status, indent=2)}")

def test_retry_functionality():
    logger.info("Testing task retry functionality...")
    
    # Submit multiple tasks to increase chance of failure
    task_ids = []
    for i in range(5):
        task_id = submit_task('data_processing', 'normal', {'data': f'test data {i}'})
        if task_id:
            task_ids.append(task_id)
    
    # Monitor tasks for retries
    for task_id in task_ids:
        status = wait_for_task_completion(task_id, timeout=60)  # Longer timeout for retries
        logger.info(f"Task {task_id} final status: {json.dumps(status, indent=2)}")

if __name__ == '__main__':
    logger.info("Starting task system tests...")
    
    # Run tests sequentially
    test_priority_tasks()
    test_task_types()
    test_retry_functionality()
    
    logger.info("All tests completed!") 