# Celery配置
broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 1000  # Borker连接池，默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']

task_serializer = 'pickle'

result_backend = 'redis://127.0.0.1:63790/0'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大的缓存量
result_expires = 3600  # 任务结果过期时间

worker_redirect_stdouts_level = 'INFO'
