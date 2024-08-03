import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf.example'))


REDDIT_SECRET = parser.get('api_key', 'reddit_secret')
REDDIT_CLIENT_ID = parser.get('api_key', 'reddit_client')


AWS_ACCESS_KEY_ID = parser.get('aws_secret_key', 'aws_access_key_id')
AWS_ACCESS_KEY = parser.get('aws_secret_key', 'aws_secret_access_key')
AWS_BUCKET_NAME = parser.get('aws_secret_key', 'aws_bucket_name')
AWS_REGION_NAME = parser.get('aws_secret_key', 'aws_region_name')




