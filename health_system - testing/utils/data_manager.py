# 文件路径: health_system/utils/data_manager.py

import os
import re
from models.patient import Patient


class DataManager:
    def __init__(self, file_path):
        """
        功能：初始化数据管理器
        参数：
            file_path (str): 数据文件路径
        """
        self.file_path = file_path
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

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    # 使用正则表达式拆分，支持制表符和空格作为分隔符
                    fields = re.split(r'[\t\s]+', line)
                    if len(fields) != 10:
                        print(f"警告：数据格式不正确，已跳过此行：{line}")
                        continue  # 跳过格式不正确的行

                    # 处理性别字段，支持 '男'、'女'、'M'、'F'
                    gender = fields[3]
                    if gender in ['M', '男']:
                        gender = '男'
                    elif gender in ['F', '女']:
                        gender = '女'
                    else:
                        print(f"警告：性别字段无效，已跳过此行：{line}")
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
                        print(f"警告：{ve}，已跳过此行：{line}")
                    except Exception as e:
                        print(f"警告：处理数据时发生错误，已跳过此行：{line}\n错误信息：{e}")
        except Exception as e:
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
        except Exception as e:
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

    def get_all_patients(self):
        """
        功能：获取所有患者列表
        返回：
            list[Patient]: 患者对象列表
        """
        return list(self.patients.values())
