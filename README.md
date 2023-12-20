
# Welcome to your CDK Python project!

This program was developed from AWS CDK with Python. An AWS Lambda function runs that uses AWS services such as S3, DynamoDB, and SES (Simple Email Service).
The program processes some data, then saves it to DynamoDB and then sends an email with the results. The email includes information such as total, credit, debit, etc.

Here is a breakdown of the code:
*In the file email_challenge_stack.py
S3 Bucket: Create an S3 bucket using aws_s3.Bucket.

Lambda Function: Defines a Lambda function using aws_lambda.Function. The Lambda function is associated with a Python 3.9 runtime and a specified handler function (lambda_function.lambda_handler).
The function code is loaded from the local ./lambda directory.
Sets an environment variable (MY_BUCKET) with the name of the S3 bucket.

IAM Permissions for Lambda: Adds a policy statement to the Lambda function role, granting permission to read objects from the S3 bucket.

DynamoDB Table: Create a DynamoDB table using aws_dynamodb.Table. The table has a partition key called "id" of type string.

IAM permissions for DynamoDB: Gives the Lambda function full access to the DynamoDB table.
IAM Permissions for SES: Adds a policy statement to the Lambda function role, allowing it to send emails using SES.

Basically, this script sets up a simple infrastructure to handle email challenges, where the Lambda function has access to an S3 bucket, a DynamoDB table, and SES to send emails.

*In the lambda_function.py file
Setup: Import required libraries, configure AWS services (S3, DynamoDB, SES) and define some constants like bucket name, file key, table name, sender and recipient email addresses .

send_email function: Defines a function to send an email using the SES client.

Lambda_handler function: The main handler for Lambda functions. Processes the data and returns some calculated values.
Prints the item to be saved to DynamoDB and is saved using put_item.

Builds an email subject and body based on the results of transaction analysis. Send an email with the results using the send_email function.
Returns a successful response with HTTP status code 200 and the element saved.

To upload the .csv file to s3 use the following command:
aws s3 cp C:\Users\alexi\OneDrive\Desktop\Tests\txns.csv s3://emailchallengestack-bucket83908e77-gplgwtvzbtez

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
