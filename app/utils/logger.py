from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format= '<level>{time:YYYY-MM-DD}</level> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <cyan>{message}</cyan>',
    level= 'DEBUG',
    colorize= True
)

logger.add(
    'logs/app.logs',
    format= '{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} | {message}',
    level= 'INFO',
    rotation='1 day',
    retention='7 days',
    encoding='utf-8'
)

__all__=['logger']