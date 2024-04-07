import logging.config

'''
日志配置与记录
'''

# 日志配置字典
LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # 日志格式
    'formatters': {
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'filters': {},
    # 日志处理器
    'handlers': {
        'get_file_hander': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': 'Log/get.log',
            'maxBytes': 1024 * 1024 * 10,  # 日志大小 10M
            'backupCount': 10,  # 日志文件保存数量限制
            'encoding': 'utf-8',
            'formatter': 'simple',
        },
        'without_file_handler': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',  # 保存到文件
            'filename': 'Log/without.log',  # 日志存放的路径
            'encoding': 'utf-8',  # 日志文件的编码
            'formatter': 'simple',
        },
        'upload_file_handler': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',  # 保存到文件
            'filename': 'Log/upload.log',  # 日志存放的路径
            'encoding': 'utf-8',  # 日志文件的编码
            'formatter': 'simple',
        },
    },
    # 日志记录器
    'loggers': {
        'logger1': {  # 导入 logging.getLogger 时使用的 app_name
            'handlers': ['get_file_hander'],  # 日志分配到哪个handlers中
            'level': 'INFO',  # 日志记录的级别限制
            'propagate': False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
        },
        'logger2': {
            'handlers': ['without_file_handler'],
            'level': 'WARNING',
            'propagate': False,
        },
        'logger3': {
            'handlers': ['upload_file_handler'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(LOGGING_DIC)
get_file_logger = logging.getLogger('logger1')
without_file_logger = logging.getLogger('logger2')
upload_file_logger = logging.getLogger('logger3')
