# 文件路径: health_system/config.py

import os

# 数据文件路径
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'patient_records.txt')

# 日志文件路径
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'system.log')
