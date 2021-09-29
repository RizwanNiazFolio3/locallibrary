from datetime import timedelta

ACCESS_TOKEN_REFRESH_TIME = timedelta(minutes=5)
REFRESH_TOKEN_LIFETIME = timedelta(days=1)
SLIDING_TOKEN_LIFETIME = timedelta(minutes=5)
SLIDING_TOKEN_REFRESH_LIFETIME = timedelta(days=1)