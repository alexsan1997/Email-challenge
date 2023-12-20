from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_dynamodb as dynamo
)
from constructs import Construct


class EmailChallengeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "Bucket")

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'EmailHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('./lambda'),
            handler="lambda_function.lambda_handler",
        )
        my_lambda.add_environment("MY_BUCKET", bucket.bucket_name)

        # Permissions to read s3
        s3_read_permission = iam.PolicyStatement(
            actions=["s3:*"],
            resources=[f"{bucket.bucket_arn}/*"]
        )
        my_lambda.add_to_role_policy(s3_read_permission)

        # create dynamo table
        email_table = dynamo.Table(
            self, "email_table",
            partition_key=dynamo.Attribute(
                name="id",
                type=dynamo.AttributeType.STRING
            )
        )
        email_table.grant_full_access(my_lambda)

        # Permissions to send emails with SES
        ses_policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ses:SendEmail", "ses:SendRawEmail", "ses:SendTemplatedEmail"],
            resources=["*"]
        )
        my_lambda.add_to_role_policy(ses_policy_statement)