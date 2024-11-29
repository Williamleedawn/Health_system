# 文件路径: health_system/models/patient.py

import re
import datetime

class Patient:
    def __init__(self, patient_id, name, age, gender, height, weight, blood_pressure, blood_sugar, cholesterol, check_date):
        """
        功能：初始化患者对象
        参数：
            所有患者基本信息字段
        异常：
            无
        """
        self.patient_id = patient_id.strip()
        self.name = name.strip()
        self.age = age
        self.gender = gender.strip()
        self.height = height
        self.weight = weight
        self.blood_pressure = blood_pressure.strip()
        self.blood_sugar = blood_sugar
        self.cholesterol = cholesterol
        self.check_date = check_date.strip()

    def validate(self):
        """
        功能：验证患者数据的有效性
        返回：
            bool - 验证是否通过
        异常：
            ValueError - 数据验证失败时抛出，包含具体错误信息
        """
        errors = []
        # 验证patient_id
        if not re.match(r'^P\d+$', self.patient_id):
            errors.append("患者ID必须以'P'开头，后跟数字。")
        # 验证name
        if not self.name:
            errors.append("姓名不能为空。")
        # 验证age
        if not (0 <= self.age <= 120):
            errors.append("年龄必须在0到120之间。")
        # 验证gender
        if self.gender in ['男', '女', 'M', 'F']:
            if self.gender == 'M':
                self.gender = '男'
            elif self.gender == 'F':
                self.gender = '女'
        else:
            errors.append("性别必须是'男'或'女'。")
        # 验证height
        if not (50 <= self.height <= 250):
            errors.append("身高必须在50到250厘米之间。")
        # 验证weight
        if not (20 <= self.weight <= 200):
            errors.append("体重必须在20到200公斤之间。")
        # 验证blood_pressure
        if not self._validate_blood_pressure():
            errors.append("血压格式错误，应为'收缩压/舒张压'，且数值在合理范围内。")
        # 验证blood_sugar
        if self.blood_sugar <= 0:
            errors.append("血糖值必须为正数。")
        # 验证cholesterol
        if self.cholesterol <= 0:
            errors.append("胆固醇值必须为正数。")
        # 验证check_date
        if not self._validate_date():
            errors.append("检查日期格式错误，应为'YYYY-MM-DD'。")

        if errors:
            raise ValueError("数据验证失败: " + "; ".join(errors))
        return True

    def _validate_blood_pressure(self):
        try:
            systolic, diastolic = self.blood_pressure.split('/')
            systolic = int(systolic)
            diastolic = int(diastolic)
            if 0 < systolic < 300 and 0 < diastolic < 200:
                return True
            else:
                return False
        except:
            return False

    def _validate_date(self):
        try:
            datetime.datetime.strptime(self.check_date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def to_string(self):
        """
        功能：将患者信息转换为制表符分隔的字符串
        返回：
            str - 格式化的字符串
        """
        fields = [
            self.patient_id, self.name, str(self.age), self.gender,
            f"{self.height:.2f}", f"{self.weight:.2f}", self.blood_pressure,
            f"{self.blood_sugar:.2f}", f"{self.cholesterol:.2f}", self.check_date
        ]
        return '\t'.join(fields)

    def __str__(self):
        """
        功能：返回患者信息的可读字符串表示
        返回：
            str - 格式化的字符串
        """
        return (
            f"患者ID: {self.patient_id}\n"
            f"姓名: {self.name}\n"
            f"年龄: {self.age}\n"
            f"性别: {self.gender}\n"
            f"身高: {self.height} cm\n"
            f"体重: {self.weight} kg\n"
            f"血压: {self.blood_pressure}\n"
            f"血糖: {self.blood_sugar} mmol/L\n"
            f"胆固醇: {self.cholesterol} mmol/L\n"
            f"检查日期: {self.check_date}"
        )
