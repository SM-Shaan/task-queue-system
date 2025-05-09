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

BASE_URL = 'http://localhost:5000/api'

def submit_task(task_type, priority='normal', parameters=None):
    url = f"{BASE_URL}/tasks"
    data = {
        'task_type': task_type,
        'priority': priority,
        'parameters': parameters or {}
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

def test_normal_task():
    logger.info("Testing normal priority task...")
    task_id = submit_task('data_processing', 'normal', {'data': 'test data'})
    if task_id:
        status = wait_for_task_completion(task_id)
        logger.info(f"Normal task result: {json.dumps(status, indent=2)}")
    return task_id

def test_high_priority_task():
    logger.info("Testing high priority task...")
    task_id = submit_task('email_sending', 'high', {'to': 'test@example.com'})
    if task_id:
        status = wait_for_task_completion(task_id)
        logger.info(f"High priority task result: {json.dumps(status, indent=2)}")
    return task_id

def test_low_priority_task():
    logger.info("Testing low priority task...")
    task_id = submit_task('file_processing', 'low', {'filename': 'test.txt'})
    if task_id:
        status = wait_for_task_completion(task_id)
        logger.info(f"Low priority task result: {json.dumps(status, indent=2)}")
    return task_id

def test_invalid_task_type():
    logger.info("Testing invalid task type...")
    task_id = submit_task('invalid_type', 'normal', {'data': 'test'})
    if task_id:
        status = wait_for_task_completion(task_id)
        logger.info(f"Invalid task type result: {json.dumps(status, indent=2)}")
    return task_id

def test_invalid_parameters():
    logger.info("Testing invalid parameters...")
    task_id = submit_task('data_processing', 'normal', 'invalid_parameters')
    if task_id:
        status = wait_for_task_completion(task_id)
        logger.info(f"Invalid parameters result: {json.dumps(status, indent=2)}")
    return task_id

def test_concurrent_tasks():
    logger.info("Testing concurrent task submission...")
    tasks = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(10):
            task_type = random.choice(['data_processing', 'email_sending', 'file_processing'])
            priority = random.choice(['high', 'normal', 'low'])
            parameters = {'data': f'test_data_{random.randint(1, 100)}'}
            tasks.append(executor.submit(submit_task, task_type, priority, parameters))
    
    for future in tasks:
        task_id = future.result()
        if task_id:
            status = wait_for_task_completion(task_id)
            logger.info(f"Concurrent task result: {json.dumps(status, indent=2)}")

def run_all_tests():
    logger.info("Starting system tests...")
    
    test_normal_task()
    test_high_priority_task()
    test_low_priority_task()
    
    test_invalid_task_type()
    test_invalid_parameters()
    
    test_concurrent_tasks()
    
    logger.info("All tests completed!")

if __name__ == '__main__':
    run_all_tests() 