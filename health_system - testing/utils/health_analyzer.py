# 文件路径: health_system/utils/health_analyzer.py
import os

class HealthAnalyzer:
    @staticmethod
    def calculate_bmi(height, weight):
        """
        功能：计算BMI指数
        参数：
            height (float): 身高(cm)
            weight (float): 体重(kg)
        返回：
            tuple(float, str): (BMI值, BMI分类)
        """
        height_m = height / 100  # 转换为米
        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 2)
        if bmi < 18.5:
            category = "偏瘦"
        elif 18.5 <= bmi < 24:
            category = "正常"
        elif 24 <= bmi < 28:
            category = "过重"
        else:
            category = "肥胖"
        return bmi, category

    @staticmethod
    def analyze_blood_pressure(bp_str):
        """
        功能：分析血压状况
        参数：
            bp_str (str): 血压字符串(格式：收缩压/舒张压)
        返回：
            str: 血压状况描述
        """
        try:
            systolic, diastolic = map(int, bp_str.split('/'))
            if systolic < 90 or diastolic < 60:
                status = "低血压"
            elif 90 <= systolic < 120 and 60 <= diastolic < 80:
                status = "理想血压"
            elif 120 <= systolic < 140 or 80 <= diastolic < 90:
                status = "正常血压"
            elif 140 <= systolic < 160 or 90 <= diastolic < 100:
                status = "轻度高血压"
            elif 160 <= systolic < 180 or 100 <= diastolic < 110:
                status = "中度高血压"
            else:
                status = "重度高血压"
            return status
        except:
            return "血压数据错误"

    @staticmethod
    def analyze_blood_sugar(blood_sugar):
        """
        功能：分析血糖水平
        参数：
            blood_sugar (float): 血糖值
        返回：
            str: 血糖水平描述
        """
        if blood_sugar < 3.9:
            return "低血糖"
        elif 3.9 <= blood_sugar <= 6.1:
            return "正常血糖"
        elif 6.1 < blood_sugar <= 7.0:
            return "糖耐量受损"
        else:
            return "糖尿病"

    @staticmethod
    def analyze_cholesterol(cholesterol):
        """
        功能：分析胆固醇水平
        参数：
            cholesterol (float): 胆固醇值
        返回：
            str: 胆固醇水平描述
        """
        if cholesterol < 3.1:
            return "胆固醇偏低"
        elif 3.1 <= cholesterol <= 5.2:
            return "胆固醇正常"
        else:
            return "胆固醇偏高"

    def generate_health_report(self, patient):
        """
        功能：生成患者健康报告，并以"[patient_id]_report.txt"文件格式存储在"health_system/"主文件夹下
        参数：
            patient (Patient): 患者对象
        返回：
            str: 格式化的健康报告
        """
        bmi_value, bmi_category = self.calculate_bmi(patient.height, patient.weight)
        bp_status = self.analyze_blood_pressure(patient.blood_pressure)
        sugar_status = self.analyze_blood_sugar(patient.blood_sugar)
        cholesterol_status = self.analyze_cholesterol(patient.cholesterol)

        report = (
            f"健康报告 - {patient.name} ({patient.patient_id})\n"
            f"----------------------------------------\n"
            f"检查日期: {patient.check_date}\n\n"
            f"基本信息:\n"
            f"年龄: {patient.age} 岁\n"
            f"性别: {patient.gender}\n"
            f"身高: {patient.height} cm\n"
            f"体重: {patient.weight} kg\n\n"
            f"BMI指数: {bmi_value} ({bmi_category})\n"
            f"血压: {patient.blood_pressure} ({bp_status})\n"
            f"血糖: {patient.blood_sugar} mmol/L ({sugar_status})\n"
            f"胆固醇: {patient.cholesterol} mmol/L ({cholesterol_status})\n"
        )

        # 将报告保存到文件
        report_filename = f"{patient.patient_id}_report.txt"
        report_path = os.path.join(os.getcwd(), report_filename)
        try:
            with open(report_path, 'w', encoding='utf-8') as file:
                file.write(report)
        except Exception as e:
            raise Exception(f"保存健康报告时发生错误: {e}")

        return report
