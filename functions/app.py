import boto3
import json

def send_to_ecs(ecs_config: dict, payload: dict) -> dict:
    """
    ecs_config: dict = {
        'cluster': 'cluster-name',
        'task_definition': 'task-name:task-version',
        'container_name': 'container-name'
        }
    payload: dict = # result from scraper
    """
    ecs = boto3.client('ecs')
    response = ecs.run_task(
        cluster=ecs_config['cluster'],
        launchType = 'FARGATE',
        taskDefinition=ecs_config['task_definition'],
        count = 1,
        platformVersion='1.3.0',
        networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': ['', ''],
                    'assignPublicIp': 'ENABLED'
                }
            },
        overrides={
            'containerOverrides': [
                {
                    'name': ecs_config['container_name'],
                    'environment': [{'name': 'REQ', 'value': json.dumps(payload)}],
                    },
                ]
            }
        )
    

def lambda_handler(event, context):
    container_name = "docker-prueba-container"
    ecs_cluster_name = "prueba-cluster"
    task_definition = "prueba-cluster-task"
    print(f"task_definition {task_definition}")
    ecs_config = {
        'cluster': ecs_cluster_name,
        'task_definition': task_definition,
        'container_name': container_name
        }
    ts = send_to_ecs(ecs_config, event)
    print(f"task started {ts}")