"""
gunicorn驱动Django实现多进程+多协程

"""
from multiprocessing import cpu_count

bind = ['0.0.0.0:9000']  # 线上环境不会开启在公网IP下，一般使用内网IP
daemon = True  # 是否开启守护进程模式
pidfile = 'gunicorn.pid'

workers = cpu_count() * 2
worker_class = 'gevent'  # 指定一个异步处理的库
worker_connections = 65535  # 单个进程能接的数量

keepalive = 60  # TCP下的HTTP访问断开后服务器保留时间，避免频繁的三次握手过程
timeout = 30
graceful_timeout = 10
forwarder_allow_ips = '*'

# 日志处理
capture_output = True
loglevel = 'info'
errorlog = 'logs/error.log'
