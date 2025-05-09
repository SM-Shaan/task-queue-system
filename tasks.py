from celery import Celery
from celery.signals import task_failure, task_success
import os
from dotenv import load_dotenv
import time
import logging
import traceback
import json
from celery.utils.log import get_task_logger

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

@celery_app.task(name='tasks.process_task')
def process_task(task_type, priority='normal', parameters=None):
    task_logger.info(f"Starting task processing: type={task_type}, priority={priority}, parameters={parameters}")
    
    try:
        if not isinstance(task_type, str):
            raise TaskError("task_type must be a string")
        
        if not isinstance(priority, str):
            raise TaskError("priority must be a string")
            
        if parameters is not None and not isinstance(parameters, dict):
            raise TaskError("parameters must be a dictionary or None")
        
        if task_type == 'data_processing':
            result = process_data_task(parameters or {})
        elif task_type == 'email_sending':
            result = send_email_task(parameters or {})
        elif task_type == 'file_processing':
            result = process_file_task(parameters or {})
        else:
            raise TaskError(f"Unknown task type: {task_type}")
        
        task_logger.info(f"Task completed successfully: {result}")
        return {
            'status': 'completed',
            'result': result,
            'task_type': task_type,
            'priority': priority
        }
    
    except TaskError as exc:
        task_logger.error(f"Task failed: {str(exc)}")
        return exc.to_dict()
    except Exception as exc:
        task_logger.error(f"Task failed: {str(exc)}\n{traceback.format_exc()}")
        return {
            'error': str(exc),
            'details': {
                'traceback': traceback.format_exc()
            }
        }

def get_task_status(task_id):
    try:
        task = celery_app.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Task is waiting for execution or unknown'
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
                'status': task.info
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