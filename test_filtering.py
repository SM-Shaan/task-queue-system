import requests
import time
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = 'http://localhost:5000/api'

def submit_test_tasks():
    """Submit multiple test tasks with different priorities"""
    tasks = [
        {
            "task_type": "data_processing",
            "priority": "high",
            "parameters": {"data": "high priority test"}
        },
        {
            "task_type": "email_sending",
            "priority": "normal",
            "parameters": {"to": "test@example.com"}
        },
        {
            "task_type": "file_processing",
            "priority": "low",
            "parameters": {"filename": "test.txt"}
        }
    ]
    
    task_ids = []
    for task in tasks:
        try:
            response = requests.post(f"{BASE_URL}/tasks", json=task)
            response.raise_for_status()
            task_id = response.json()['task_id']
            task_ids.append(task_id)
            logger.info(f"Submitted task {task_id}: {task}")
        except Exception as e:
            logger.error(f"Error submitting task: {str(e)}")
    
    return task_ids

def test_filters():
    """Test different filter combinations"""
    filters = [
        {'state': 'SUCCESS'},
        {'state': 'PENDING'},
        {'state': 'FAILURE'},
        
        {'type': 'active'},
        {'type': 'reserved'},
        {'type': 'completed'},
        
        {'state': 'SUCCESS', 'type': 'active'},
        {'state': 'PENDING', 'type': 'reserved'}
    ]
    
    for filter_params in filters:
        try:
            response = requests.get(f"{BASE_URL}/tasks", params=filter_params)
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"\nTesting filters: {filter_params}")
            logger.info(f"Found {result['total']} tasks")
            logger.info(f"Tasks: {json.dumps(result['tasks'], indent=2)}")
            
        except Exception as e:
            logger.error(f"Error testing filters {filter_params}: {str(e)}")

def main():
    """Run the test sequence"""
    logger.info("Starting filter test...")
    
    logger.info("Submitting test tasks...")
    task_ids = submit_test_tasks()
    
    logger.info("Waiting for tasks to be processed...")
    time.sleep(5)
    
    logger.info("Testing filters...")
    test_filters()
    
    logger.info("Filter test completed!")

if __name__ == '__main__':
    main() 