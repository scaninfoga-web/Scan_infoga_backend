from dotenv import load_dotenv
import os
import boto3

load_dotenv()

class LeakEmailPasswords:
    def __init__(self) -> None:
        self._aws_access_key_id = os.getenv('AWS_DYNAMODB_ACCESS_TOKEN')
        self._aws_secret_access_key = os.getenv('AWS_DYNAMODB_SECURITY_ACCESS_TOKEN')
        self._region_name = os.getenv('AWS_DYNAMODB_REGION_NAME')
        self._table_name = os.getenv('AWS_DYNAMODB_LEAKED_TABLE_NAME')
        self._dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            region_name=self._region_name
        )
        self._table = self._dynamodb.Table(self._table_name)

    def _get_passwords(self, email: str):
        response = self._table.get_item(Key={'email': email})
        return response.get('Item', {'email':email,'password':['No password found']})

    def fetch_passwords(self, email: str):
        return self._get_passwords(email=email)
