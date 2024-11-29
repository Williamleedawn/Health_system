# 文件路径: health_system/utils/data_manager.py

import os
import re
import json
import csv
from models.patient import Patient
from utils.logger import logger
from config import DATA_FILE_PATH

class DataManager:
    def __init__(self):
        """
        功能：初始化数据管理器
        """
        self.file_path = DATA_FILE_PATH
        self.patients = {}
        self.load_data()

    def load_data(self):
        """
        功能：从文件加载患者数据
        异常：
            FileNotFoundError: 文件不存在
            Exception: 其他加载错误
        """
        if not os.path.exists(self.file_path):
            # 如果文件不存在，创建空文件夹和文件
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            open(self.file_path, 'w', encoding='utf-8').close()
            logger.info(f"数据文件不存在，已创建新的文件：{self.file_path}")

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    # 使用正则表达式拆分，支持制表符和空格作为分隔符
                    fields = re.split(r'[\t\s]+', line)
                    if len(fields) != 10:
                        logger.warning(f"数据格式不正确，已跳过此行：{line}")
                        continue  # 跳过格式不正确的行

                    # 处理性别字段，支持 '男'、'女'、'M'、'F'
                    gender = fields[3]
                    if gender in ['M', '男']:
                        gender = '男'
                    elif gender in ['F', '女']:
                        gender = '女'
                    else:
                        logger.warning(f"性别字段无效，已跳过此行：{line}")
                        continue  # 跳过性别字段无效的行

                    # 创建患者对象
                    try:
                        patient = Patient(
                            patient_id=fields[0],
                            name=fields[1],
                            age=int(fields[2]),
                            gender=gender,
                            height=float(fields[4]),
                            weight=float(fields[5]),
                            blood_pressure=fields[6],
                            blood_sugar=float(fields[7]),
                            cholesterol=float(fields[8]),
                            check_date=fields[9]
                        )
                        # 验证患者数据
                        patient.validate()
                        self.patients[patient.patient_id] = patient
                    except ValueError as ve:
                        logger.warning(f"{ve}，已跳过此行：{line}")
                    except Exception as e:
                        logger.warning(f"处理数据时发生错误，已跳过此行：{line}\n错误信息：{e}")
            logger.info(f"成功加载 {len(self.patients)} 条患者数据。")
        except Exception as e:
            logger.error(f"加载数据时发生错误: {e}")
            raise Exception(f"加载数据时发生错误: {e}")

    def save_data(self):
        """
        功能：保存患者数据到文件
        异常：
            Exception: 保存失败
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                for patient in self.patients.values():
                    file.write(patient.to_string() + '\n')
            logger.info("数据已成功保存。")
        except Exception as e:
            logger.error(f"保存数据时发生错误: {e}")
            raise Exception(f"保存数据时发生错误: {e}")

    def add_patient(self, patient):
        """
        功能：添加新患者
        参数：
            patient (Patient): 患者对象
        异常：
            ValueError: 患者ID已存在
            ValueError: 数据验证失败
        """
        if patient.patient_id in self.patients:
            raise ValueError("患者ID已存在。")
        patient.validate()
        self.patients[patient.patient_id] = patient
        self.save_data()
        logger.info(f"添加患者：{patient.patient_id}")

    def get_patient(self, patient_id):
        """
        功能：获取指定ID的患者信息
        参数：
            patient_id (str): 患者ID
        返回：
            Patient对象或None
        """
        return self.patients.get(patient_id)

    def update_patient(self, patient):
        """
        功能：更新患者信息
        参数：
            patient (Patient): 更新后的患者对象
        异常：
            ValueError: 患者不存在
            ValueError: 数据验证失败
        """
        if patient.patient_id not in self.patients:
            raise ValueError("患者不存在。")
        patient.validate()
        self.patients[patient.patient_id] = patient
        self.save_data()
        logger.info(f"更新患者信息：{patient.patient_id}")

    def delete_patient(self, patient_id):
        """
        功能：删除患者记录
        参数：
            patient_id (str): 患者ID
        异常：
            ValueError: 患者不存在
        """
        if patient_id not in self.patients:
            raise ValueError("患者不存在。")
        del self.patients[patient_id]
        self.save_data()
        logger.info(f"删除患者：{patient_id}")

    def get_all_patients(self):
        """
        功能：获取所有患者列表
        返回：
            list[Patient]: 患者对象列表
        """
        return list(self.patients.values())

    def import_data(self, file_path, file_type='csv'):
        """
        功能：从指定文件导入患者数据
        参数：
            file_path (str): 导入文件路径
            file_type (str): 文件类型，'csv'或'json'
        """
        count = 0
        try:
            if file_type == 'csv':
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) != 10:
                            continue
                        patient = Patient(
                            patient_id=row[0],
                            name=row[1],
                            age=int(row[2]),
                            gender=row[3],
                            height=float(row[4]),
                            weight=float(row[5]),
                            blood_pressure=row[6],
                            blood_sugar=float(row[7]),
                            cholesterol=float(row[8]),
                            check_date=row[9]
                        )
                        patient.validate()
                        self.patients[patient.patient_id] = patient
                        count += 1
            elif file_type == 'json':
                with open(file_path, 'r', encoding='utf-8') as jsonfile:
                    data = json.load(jsonfile)
                    for item in data:
                        patient = Patient(**item)
                        patient.validate()
                        self.patients[patient.patient_id] = patient
                        count += 1
            else:
                raise ValueError("不支持的文件类型。")
            self.save_data()
            logger.info(f"成功导入 {count} 条患者数据。")
        except Exception as e:
            logger.error(f"导入数据时发生错误: {e}")
            raise Exception(f"导入数据时发生错误: {e}")

    def export_data(self, file_path, file_type='csv'):
        """
        功能：导出患者数据到指定文件
        参数：
            file_path (str): 导出文件路径
            file_type (str): 文件类型，'csv'或'json'
        """
        try:
            if file_type == 'csv':
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for patient in self.patients.values():
                        writer.writerow([
                            patient.patient_id, patient.name, patient.age, patient.gender,
                            patient.height, patient.weight, patient.blood_pressure,
                            patient.blood_sugar, patient.cholesterol, patient.check_date
                        ])
            elif file_type == 'json':
                data = [patient.__dict__ for patient in self.patients.values()]
                with open(file_path, 'w', encoding='utf-8') as jsonfile:
                    json.dump(data, jsonfile, ensure_ascii=False, indent=4)
            else:
                raise ValueError("不支持的文件类型。")
            logger.info(f"成功导出患者数据到 {file_path}")
        except Exception as e:
            logger.error(f"导出数据时发生错误: {e}")
            raise Exception(f"导出数据时发生错误: {e}")
