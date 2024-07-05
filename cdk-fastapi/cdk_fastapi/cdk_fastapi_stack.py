import aws_cdk as core
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_ecr as ecr
)
from constructs import Construct

class CdkFastapiStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, "vpc-0262bede1e4144f66", max_azs=2)

        cluster = ecs.Cluster(self, "fastapi-cluster", vpc=vpc)

        table = dynamodb.Table(
            self, "MessagesTable",
            partition_key={"name": "id", "type": dynamodb.AttributeType.STRING}
        )

        repository = ecr.Repository.from_repository_name(
            self, "ECRRepo", "fastapi-service"
        )

        task_role = iam.Role.from_role_arn(
            self, "TaskRole", "arn:aws:iam::305572817819:user/another_cdk_user"
        )

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "FargateService",
            cluster=cluster,
            task_image_options={
                "image": ecs.ContainerImage.from_ecr_repository(repository),
                "environment": {
                    "DYNAMODB_TABLE": table.table_name,
                    "AWS_REGION": "eu-central-1"
                },
                "task_role": task_role
            },
            public_load_balancer=False  # Ensure the load balancer is internal
        )

        table.grant_read_write_data(fargate_service.task_definition.task_role)
