# 文件路径: health_system/utils/logger.py

import logging
import os
from config import LOG_FILE_PATH

# 创建日志目录
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
