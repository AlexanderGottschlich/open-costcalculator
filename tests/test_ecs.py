# tests/test_ecs.py

from resources.ecs import ecs_meta


def test_extract_ecs_task_definition():
    plan = {
        "resource_changes": [
            {
                "type": "aws_ecs_task_definition",
                "change": {
                    "actions": ["create"],
                    "after": {"cpu": "256", "memory": "512"},
                },
            }
        ]
    }
    result = ecs_meta.extract_ecs_task_definition(plan)
    assert result == {"cpu": "256", "memory": "512"}


def test_extract_ecs_task_definition_no_ecs():
    plan = {"resource_changes": [{"type": "aws_eks_cluster"}]}
    result = ecs_meta.extract_ecs_task_definition(plan)
    assert result is None


def test_extract_ecs_service():
    plan = {
        "resource_changes": [
            {
                "type": "aws_ecs_service",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "launch_type": "FARGATE",
                        "desired_count": 2,
                        "task_definition": "task:1",
                    },
                },
            }
        ]
    }
    result = ecs_meta.extract_ecs_service(plan)
    assert result == {
        "launch_type": "FARGATE",
        "desired_count": 2,
        "task_definition": "task:1",
    }


def test_extract_ecs_service_no_desired_count():
    after = {"launch_type": "FARGATE"}
    plan = {"resource_changes": [{"type": "aws_ecs_service", "change": {"actions": ["create"], "after": after}}]}
    result = ecs_meta.extract_ecs_service(plan)
    assert result["desired_count"] == 1


def test_detect_ecs_usage_no_ecs():
    plan = {"resource_changes": [{"type": "aws_s3_bucket"}]}
    assert ecs_meta.detect_ecs_usage(plan) is False


def test_detect_ecs_usage_with_ecs():
    task_change = {"actions": ["create"], "after": {"cpu": "256"}}
    svc_change = {"actions": ["create"], "after": {"launch_type": "FARGATE"}}
    plan = {
        "resource_changes": [
            {"type": "aws_ecs_task_definition", "change": task_change},
            {"type": "aws_ecs_service", "change": svc_change},
        ]
    }
    assert ecs_meta.detect_ecs_usage(plan) is True


def test_extract_ecs_complete():
    task_after = {"cpu": "512", "memory": "1024"}
    svc_after = {
        "launch_type": "FARGATE",
        "desired_count": 3,
        "task_definition": "task:1",
    }
    plan = {
        "resource_changes": [
            {"type": "aws_ecs_task_definition", "change": {"actions": ["create"], "after": task_after}},
            {"type": "aws_ecs_service", "change": {"actions": ["create"], "after": svc_after}},
        ]
    }
    result = ecs_meta.extract(plan)
    assert result == {
        "cpu": "512",
        "memory": "1024",
        "launch_type": "FARGATE",
        "desired_count": 3,
    }


def test_extract_ecs_no_task_definition():
    plan = {"resource_changes": [{"type": "aws_ecs_service", "change": {"actions": ["create"], "after": {}}}]}
    result = ecs_meta.extract(plan)
    assert result is None


def test_extract_ecs_no_service():
    plan = {"resource_changes": [{"type": "aws_ecs_task_definition", "change": {"actions": ["create"], "after": {}}}]}
    result = ecs_meta.extract(plan)
    assert result is None
