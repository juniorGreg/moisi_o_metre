from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings



class PublicMediaStorage(S3Boto3Storage):
    location = 'images'
    default_acl = 'public-read'
    
