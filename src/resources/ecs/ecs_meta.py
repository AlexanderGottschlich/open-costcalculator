# resources/ecs/ecs_meta.py

from core import logger


def extract_ecs_task_definition(plan):
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_ecs_task_definition":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after", {})
                if after:
                    cpu = after.get("cpu")
                    memory = after.get("memory")
                    return {"cpu": cpu, "memory": memory}
    return None


def extract_ecs_service(plan):
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_ecs_service":
            change = res.get("change", {})
            actions = change.get("actions", [])
            if "create" in actions or "update" in actions:
                after = change.get("after", {})
                if after:
                    launch_type = after.get("launch_type", "FARGATE")
                    desired_count = after.get("desired_count", 1)
                    task_definition = after.get("task_definition")
                    return {
                        "launch_type": launch_type,
                        "desired_count": desired_count,
                        "task_definition": task_definition,
                    }
    return None


def detect_ecs_usage(plan):
    task_def = extract_ecs_task_definition(plan)
    service = extract_ecs_service(plan)
    if task_def and service:
        return True
    return False


def extract(plan):
    task_def = extract_ecs_task_definition(plan)
    service = extract_ecs_service(plan)

    if not task_def or not service:
        return None

    cpu = task_def.get("cpu")
    memory = task_def.get("memory")
    launch_type = service.get("launch_type", "FARGATE")
    desired_count = service.get("desired_count", 1)

    if not desired_count:
        desired_count = 1
        logger.info("ECS desired_count nicht gefunden, fallback auf 1")

    return {
        "cpu": cpu,
        "memory": memory,
        "launch_type": launch_type,
        "desired_count": desired_count,
    }
