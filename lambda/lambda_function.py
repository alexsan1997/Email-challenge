import boto3
import os
import csv
import uuid
from io import StringIO
from decimal import Decimal

bucket_name = os.environ["MY_BUCKET"]
file_key = 'txns.csv'
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = "EmailChallengeStack-emailtableE8154BC2-9KY1FIINLK3B"
table = dynamodb.Table(table_name)
ses = boto3.client('ses', region_name='us-east-1')
sender_email = "angel_may_s@hotmail.com"
recipient_email = "alexis_santos_1997@hotmail.com"


def send_email(subject, body):
    try:
        response = ses.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [recipient_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': body,
                    },
                },
            },
        )
        print(f"Email sent successfully: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


def lambda_handler(event, context):
    try:
        # Read file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')

        # Converts the content of the CSV to a StringIO object
        csv_data = StringIO(content)

        # Create a CSV reader
        csv_reader = csv.reader(csv_data)

        saldototal = 0
        credito = 0
        debito = 0
        transacciones = {}
        transcred = 0
        transdeb = 0

        next(csv_reader)

        # Loop through each row of the CSV
        for row in csv_reader:

            fecha = row[1]
            monto = float(row[2])
            fecha_split = fecha.split("/")

            if monto > 0:
                credito += monto
                transcred += 1
            elif monto < 0:
                debito += monto
                transdeb += 1

            saldototal += monto
            if fecha_split[0] in transacciones:
                transacciones[fecha_split[0]] += 1
            else:
                transacciones[fecha_split[0]] = 1

            print(row)

        # print(saldototal)
        # print(credito/transcred)
        # print(debito/transdeb)
        # print(transacciones)

        item = {
            "id": str(uuid.uuid4()),
            "total": Decimal(str(saldototal)),
            "credito": Decimal(str(credito / transcred)),
            "debito": Decimal(str(debito / transdeb))
        }

        for key, value in transacciones.items():
            item[key] = Decimal(str(value))

        print(f"Item to be saved to DynamoDB: {item}")

        response = table.put_item(Item=item)
        print(f"Item saved to DynamoDB: {response}")

        # Send email with the results
        email_subject = "Your bank statement"
        email_body = f"Total balance is: {saldototal}, Average credit amount: {credito / transcred}, Average debit amount: {debito / transdeb}, Number of transactions in July: {transcred}, Number of transactions in Augus: {transdeb}"
        send_email(email_subject, email_body)

        return {
            'statusCode': 200,
            'body': item
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }