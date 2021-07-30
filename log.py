"""
日志配置
"""
from loguru import logger
logger.add('runtime.log', retention='10 days',format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}")