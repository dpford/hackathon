from base import *

# Production storage using s3.
DEFAULT_FILE_STORAGE = 's3storages.MediaStorage'
STATICFILES_STORAGE = 's3storages.StaticStorage'
STATIC_URL = 'http://excello.s3-website-us-east-1.amazonaws.com/static/'
ADMIN_MEDIA_PREFIX = 'http://excello.s3-website-us-east-1.amazonaws.com/static/admin/'
MEDIA_URL = 'http://excello.s3-website-us-east-1.amazonaws.com/media/'

AWS_S3_CUSTOM_DOMAIN = 'http://excello.s3-website-us-east-1.amazonaws.com/static' #important: no "http://"