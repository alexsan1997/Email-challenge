import aws_cdk as core
import aws_cdk.assertions as assertions

from email_challenge.email_challenge_stack import EmailChallengeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in email_challenge/email_challenge_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EmailChallengeStack(app, "email-challenge")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
