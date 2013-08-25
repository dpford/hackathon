from base import *

# Production storage using s3.
DEFAULT_FILE_STORAGE = 's3storages.MediaStorage'
STATICFILES_STORAGE = 's3storages.StaticStorage'
STATIC_URL = 'https://s3.amazonaws.com/excello2/static/'
ADMIN_MEDIA_PREFIX = 'https://s3.amazonaws.com/excello2/static/admin/'
MEDIA_URL = 'https://s3.amazonaws.com/excello2/media/'

AWS_S3_CUSTOM_DOMAIN = 'https://s3.amazonaws.com/excello2/static' #important: no "http://"