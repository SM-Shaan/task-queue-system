from flask import Flask, request, jsonify
from flask_cors import CORS
from tasks import process_task, get_task_status, celery_app
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
CORS(app)

@app.route('/api/tasks', methods=['POST'])
def submit_task():
    try:
        data = request.get_json()
        logger.debug(f"Received task submission request: {data}")
        
        if not data or not isinstance(data, dict):
            return jsonify({
                'error': 'Invalid request body',
                'details': {'message': 'Request body must be a JSON object'}
            }), 400
            
        if 'task_type' not in data or not isinstance(data['task_type'], str):
            return jsonify({
                'error': 'Missing or invalid task_type',
                'details': {'required_fields': ['task_type (string)']}
            }), 400
        
        task_type = data['task_type']
        priority = data.get('priority', 'normal')
        parameters = data.get('parameters', {})
        
        if not isinstance(priority, str):
            return jsonify({
                'error': 'Invalid priority',
                'details': {'message': 'Priority must be a string'}
            }), 400
            
        if parameters is not None and not isinstance(parameters, dict):
            return jsonify({
                'error': 'Invalid parameters',
                'details': {'message': 'Parameters must be a dictionary or null'}
            }), 400
        
        logger.info(f"Submitting task: type={task_type}, priority={priority}, parameters={parameters}")
        
        try:
            queue_name = 'default'
            if priority == 'high':
                queue_name = 'high_priority'
            elif priority == 'low':
                queue_name = 'low_priority'
            
            # Submit task to Celery
            task = process_task.apply_async(
                args=[task_type],
                kwargs={
                    'priority': priority,
                    'parameters': parameters
                },
                queue=queue_name
            )
            
            logger.info(f"Task submitted successfully with ID: {task.id}")
            return jsonify({
                'task_id': task.id,
                'status': 'submitted',
                'message': 'Task has been submitted successfully',
                'queue': queue_name
            }), 202
            
        except Exception as task_error:
            logger.error(f"Failed to submit task: {str(task_error)}")
            return jsonify({
                'error': 'Failed to submit task',
                'details': {
                    'message': str(task_error),
                    'traceback': traceback.format_exc()
                }
            }), 500
        
    except Exception as e:
        logger.error(f"Error submitting task: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'details': {
                'traceback': traceback.format_exc()
            }
        }), 500

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
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

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    try:
        state_filter = request.args.get('state')
        type_filter = request.args.get('type')
        
        logger.info(f"Listing tasks with filters - State: {state_filter}, Type: {type_filter}")
        
        # Get all task IDs from Celery
        i = celery_app.control.inspect()
        
        # Get different task states
        active = i.active() or {}
        reserved = i.reserved() or {}
        scheduled = i.scheduled() or {}
        
        logger.info(f"Found active tasks: {active}")
        logger.info(f"Found reserved tasks: {reserved}")
        logger.info(f"Found scheduled tasks: {scheduled}")
        
        tasks = []
        
        def should_include_task(task_info, task_type):
            if state_filter and task_info.state != state_filter:
                logger.debug(f"Task {task_info.id} filtered out by state: {task_info.state} != {state_filter}")
                return False
            if type_filter and task_type != type_filter:
                logger.debug(f"Task {task_info.id} filtered out by type: {task_type} != {type_filter}")
                return False
            return True
        
        for worker, worker_tasks in active.items():
            for task in worker_tasks:
                task_id = task['id']
                task_info = AsyncResult(task_id, app=celery_app)
                if should_include_task(task_info, 'active'):
                    tasks.append({
                        'task_id': task_id,
                        'state': task_info.state,
                        'status': task_info.info,
                        'worker': worker,
                        'type': 'active',
                        'name': task.get('name', 'unknown'),
                        'args': task.get('args', []),
                        'kwargs': task.get('kwargs', {})
                    })
        
        for worker, worker_tasks in reserved.items():
            for task in worker_tasks:
                task_id = task['id']
                task_info = AsyncResult(task_id, app=celery_app)
                if should_include_task(task_info, 'reserved'):
                    tasks.append({
                        'task_id': task_id,
                        'state': task_info.state,
                        'status': task_info.info,
                        'worker': worker,
                        'type': 'reserved',
                        'name': task.get('name', 'unknown'),
                        'args': task.get('args', []),
                        'kwargs': task.get('kwargs', {})
                    })
        
        for worker, worker_tasks in scheduled.items():
            for task in worker_tasks:
                task_id = task['id']
                task_info = AsyncResult(task_id, app=celery_app)
                if should_include_task(task_info, 'scheduled'):
                    tasks.append({
                        'task_id': task_id,
                        'state': task_info.state,
                        'status': task_info.info,
                        'worker': worker,
                        'type': 'scheduled',
                        'name': task.get('name', 'unknown'),
                        'args': task.get('args', []),
                        'kwargs': task.get('kwargs', {})
                    })
        
        try:
            redis_client = celery_app.backend.client
            all_keys = redis_client.keys('celery-task-meta-*')
            logger.info(f"Found {len(all_keys)} completed tasks in Redis")
            
            for key in all_keys:
                task_id = key.decode('utf-8').replace('celery-task-meta-', '')
                task_info = AsyncResult(task_id, app=celery_app)
                if should_include_task(task_info, 'completed'):
                    tasks.append({
                        'task_id': task_id,
                        'state': task_info.state,
                        'status': task_info.info,
                        'worker': 'unknown',
                        'type': 'completed',
                        'name': 'unknown'
                    })
        except Exception as redis_error:
            logger.error(f"Error getting task results from Redis: {str(redis_error)}")
        
        logger.info(f"Total tasks found after filtering: {len(tasks)}")
        
        tasks_by_state = {}
        tasks_by_type = {}
        for task in tasks:
            state = task['state']
            task_type = task['type']
            
            if state not in tasks_by_state:
                tasks_by_state[state] = []
            tasks_by_state[state].append(task['task_id'])
            
            if task_type not in tasks_by_type:
                tasks_by_type[task_type] = []
            tasks_by_type[task_type].append(task['task_id'])
        
        logger.info(f"Tasks by state: {tasks_by_state}")
        logger.info(f"Tasks by type: {tasks_by_type}")
        
        return jsonify({
            'tasks': tasks,
            'total': len(tasks),
            'filters': {
                'state': state_filter,
                'type': type_filter
            },
            'available_filters': {
                'states': ['PENDING', 'STARTED', 'SUCCESS', 'FAILURE', 'RETRY'],
                'types': ['active', 'reserved', 'scheduled', 'completed']
            },
            'debug_info': {
                'tasks_by_state': tasks_by_state,
                'tasks_by_type': tasks_by_type
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'details': {
                'traceback': traceback.format_exc()
            }
        }), 500

if __name__ == '__main__':
    app.run(debug=True)