import boto3
import json

def lambda_handler(event, context):
    print("Lambda function triggered!")  # ✅ LOG 1

    # Log the incoming event for debugging
    print("Received event:", json.dumps(event))  # ✅ LOG 2

    try:
        body = json.loads(event['body'])
    except Exception as e:
        print("Error parsing body:", str(e))  # ✅ LOG 3
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }

    subject = body.get('subject', 'Default Subject')
    message = body.get('message', 'Default Message')

    # Log extracted data
    print(f"Subject: {subject}, Message: {message}")  # ✅ LOG 4

    # Set SES client
    ses = boto3.client('ses', region_name='ap-south-1')

    # Replace with verified SES emails
    SENDER = "itskashishverma@gmail.com"
    RECEIVER = "itskashishverma@gmail.com"

    try:
        response = ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': [RECEIVER]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': message}}
            }
        )

        # Log SES response
        print("SES Response:", response)  # ✅ LOG 5

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent!', 'response': response})
        }

    except Exception as e:
        print("Error sending email:", str(e))  # ✅ LOG 6
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


#aftr this u have to make event fo this in which body will be there as test case.
# Test case for the Lambda function
