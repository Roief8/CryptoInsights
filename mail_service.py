import boto3
from config import BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, ARN_SNS

sns = boto3.client('sns', region_name= 'us-east-1', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
s3 = boto3.client('s3',  region_name= 'us-east-1', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY  )

def upload_to_s3(image_buffer, file_name):

    # Upload image to S3
    bucket_name = BUCKET_NAME
    file_name = f'{file_name}.pdf'
    image_buffer.seek(0)
    
    try:
        s3.upload_fileobj(image_buffer, bucket_name, file_name, ExtraArgs =  
                                                {"ContentDisposition" : 'inline',
                                                "ContentType": 'application/pdf'})
        print(f"Successfully uploaded {file_name} to {bucket_name}")

             # Generate a pre-signed URL for the S3 object

        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': bucket_name,
                                                'Key': file_name},
                                        ExpiresIn=10800)  # URL expires in 1 hour
        return url
        
    except Exception as e:
        print(f"An error occurred while uploading to S3: {str(e)}")
    

def send_sns_mail(message):

    subject = "Cryptocurrency Daily Update"
    message = message
  
    topic_arn = ARN_SNS
    # response = sns.list_subscriptions_by_topic(TopicArn=topic_arn)  @TODO get the list of subscribers to send each email.
    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )

    print("Notification sent successfully")

def check_email_subscription(email):

    try:
        # List all subscriptions for the topic
        paginator = sns.get_paginator('list_subscriptions_by_topic')
        page_iterator = paginator.paginate(TopicArn=ARN_SNS)
        
        # Check each subscription
        for page in page_iterator:
            for subscription in page['Subscriptions']:
                if subscription['Protocol'] == 'email' and subscription['Endpoint'] == email:
                    print(f"Email {email} is already subscribed to the topic.")
                    return True
        
        print(f"Email {email} is not subscribed to the topic.")
        return False
    
    except Exception as e:
        print(f"Error checking subscription: {str(e)}")
        return False

def create_sns_subscription(endpoint):
    
    protocol = 'email'
    TopicArn = ARN_SNS

    
    try:
        # Subscribe to the topic
        response = sns.subscribe(
            TopicArn=TopicArn,
            Protocol=protocol,
            Endpoint=endpoint
        )
        
        # Get the subscription ARN
        subscription_arn = response['SubscriptionArn']
        
        print(f"Subscription created: {subscription_arn}")
        return subscription_arn
    
    except Exception as e:
        print(f"Error creating subscription: {str(e)}")
        return None

