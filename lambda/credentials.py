import logging
import json

from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MalformedSecretException(Exception):
    """Exception raised when the Secret is malformed."""

    def __init__(self):
        sample_secret = json.dumps({
            "key": "secret_key",
            "passphrase": "phrase",
            "b64secret": "sdfffweew==",
            "sandbox": "False"
        })

        super().__init__(f"The Secret is malformed. Please ensure the secret is formed as follows: {sample_secret}")


class Credentials:
    def __init__(self, creds_secret_id, secrets_manager):
        secret_string = self.get_secret_string(creds_secret_id, secrets_manager)
        try:
            secret_json = json.loads(secret_string)
            self.key = secret_json['key']
            self.passphrase = secret_json['passphrase']
            self.b64secret = secret_json['b64secret']
            self.sandbox = secret_json.get('sandbox').upper()

            if self.sandbox == "TRUE":
                self.sandbox = True
                self.api_url = "https://api-public.sandbox.pro.coinbase.com"
            else:
                self.sandbox = False
                self.api_url = "https://api.pro.coinbase.com"
        except Exception as e:
            raise MalformedSecretException()

    def get_secret_string(self, creds_secret_id, secrets_manager):
        """
        Gets the secret string from AWS Secrets Manager
        """
        try:
            get_secret_value_response = secrets_manager.get_secret_value(
                SecretId=creds_secret_id
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                return get_secret_value_response['SecretString']
            else:
                raise MalformedSecretException()
