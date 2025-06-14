import boto3
from core import settings
from botocore.exceptions import NoCredentialsError, ClientError

dynamodb_resource = None
dynamodb_client = None

def initialize_dynamodb_clients():
    global dynamodb_resource, dynamodb_client
    if dynamodb_resource is not None and dynamodb_client is not None:
        return
    try:
        if not settings.AWS_ACCESS_TOKEN or not settings.AWS_SECURITY_ACCESS_TOKEN:
            print("WARNING: AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY not found. "
                  "Boto3 will attempt to use IAM roles or default credentials chain.")

        dynamodb_resource = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_TOKEN,
            aws_secret_access_key=settings.AWS_SECURITY_ACCESS_TOKEN,
            region_name=settings.AWS_DYNAMO_REGION_NAME
        )
        dynamodb_client = boto3.client(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_TOKEN,
            aws_secret_access_key=settings.AWS_SECURITY_ACCESS_TOKEN,
            region_name=settings.AWS_DYNAMO_REGION_NAME
        )
        print("DynamoDB clients initialized successfully.")
    except NoCredentialsError:
        print("ERROR: AWS credentials not found. Please configure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or IAM roles.")
        dynamodb_resource = None
        dynamodb_client = None
    except Exception as e:
        print(f"ERROR: Failed to initialize DynamoDB clients: {e}")
        dynamodb_resource = None
        dynamodb_client = None

def get_leaked_credentials_dynamodb_table(table_name=None):
    if dynamodb_resource is None:
        initialize_dynamodb_clients()
        if dynamodb_resource is None:
            raise Exception("DynamoDB resource is not initialized. Check AWS configuration.")

    if table_name is None:
        table_name = settings.DYNAMODB_LEAKED_TABLE_NAME

    return dynamodb_resource.Table(table_name)

def get_jobseeker_dynamodb_table(table_name=None):
    if dynamodb_resource is None:
        initialize_dynamodb_clients()
        if dynamodb_resource is None:
            raise Exception("DynamoDB resource is not initialized. Check AWS configuration.")

    if table_name is None:
        table_name = settings.DYNAMODB_JOBSEEKER_TABLE_NAME

    return dynamodb_resource.Table(table_name)

def get_dynamodb_client():
    """Returns the low-level DynamoDB client."""
    if dynamodb_client is None:
        initialize_dynamodb_clients()
        if dynamodb_client is None:
            raise Exception("DynamoDB client is not initialized. Check AWS configuration.")
    return dynamodb_client