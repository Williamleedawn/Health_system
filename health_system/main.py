# 文件路径: health_system/main.py

import sys
import os

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_manager import DataManager
from utils.health_analyzer import HealthAnalyzer
from models.patient import Patient
from utils.logger import logger

class HealthSystem:
    def __init__(self):
        """
        功能：初始化健康记录管理系统
        """
        try:
            self.data_manager = DataManager()
            self.health_analyzer = HealthAnalyzer()
            logger.info("健康记录管理系统初始化成功。")
        except Exception as e:
            logger.error(f"系统初始化失败: {e}")
            sys.exit(1)

    def display_menu(self):
        """
        功能：显示系统主菜单
        """
        print("\n=== 患者健康记录管理系统 ===")
        print("1. 查看患者信息")
        print("2. 添加新患者")
        print("3. 更新患者信息")
        print("4. 删除患者")
        print("5. 生成健康报告")
        print("6. 导入数据")
        print("7. 导出数据")
        print("8. 退出系统")

    def input_patient_data(self, existing_id=None):
        """
        功能：交互式输入患者数据
        返回：
            Patient: 新的患者对象
        异常：
            ValueError: 输入数据无效
        """
        try:
            if existing_id:
                patient_id = existing_id
            else:
                patient_id = input("请输入患者ID(以'P'开头): ").strip()
            name = input("请输入姓名: ").strip()
            age = int(input("请输入年龄(0-120): ").strip())
            gender = input("请输入性别(男/女): ").strip()
            height = float(input("请输入身高(cm): ").strip())
            weight = float(input("请输入体重(kg): ").strip())
            blood_pressure = input("请输入血压(收缩压/舒张压): ").strip()
            blood_sugar = float(input("请输入血糖值(mmol/L): ").strip())
            cholesterol = float(input("请输入胆固醇值(mmol/L): ").strip())
            check_date = input("请输入检查日期(YYYY-MM-DD): ").strip()

            patient = Patient(
                patient_id=patient_id,
                name=name,
                age=age,
                gender=gender,
                height=height,
                weight=weight,
                blood_pressure=blood_pressure,
                blood_sugar=blood_sugar,
                cholesterol=cholesterol,
                check_date=check_date
            )
            patient.validate()
            return patient
        except ValueError as ve:
            print(f"输入错误: {ve}")
            logger.error(f"输入错误: {ve}")
            return None
        except Exception as e:
            print(f"发生错误: {e}")
            logger.error(f"发生错误: {e}")
            return None

    def run(self):
        """
        功能：运行系统主循环
        """
        while True:
            self.display_menu()
            choice = input("请选择操作(1-8): ").strip()
            if choice == '1':
                # 查看患者信息
                patient_id = input("请输入患者ID: ").strip()
                patient = self.data_manager.get_patient(patient_id)
                if patient:
                    print(patient)
                else:
                    print("未找到该患者。")
            elif choice == '2':
                # 添加新患者
                patient = self.input_patient_data()
                if patient:
                    try:
                        self.data_manager.add_patient(patient)
                        print("患者添加成功。")
                    except ValueError as ve:
                        print(f"添加失败: {ve}")
                        logger.error(f"添加失败: {ve}")
            elif choice == '3':
                # 更新患者信息
                patient_id = input("请输入要更新的患者ID: ").strip()
                existing_patient = self.data_manager.get_patient(patient_id)
                if existing_patient:
                    print("请输入新的患者信息:")
                    patient = self.input_patient_data(existing_id=patient_id)
                    if patient:
                        try:
                            self.data_manager.update_patient(patient)
                            print("患者信息更新成功。")
                        except ValueError as ve:
                            print(f"更新失败: {ve}")
                            logger.error(f"更新失败: {ve}")
                else:
                    print("未找到该患者。")
            elif choice == '4':
                # 删除患者
                patient_id = input("请输入要删除的患者ID: ").strip()
                try:
                    self.data_manager.delete_patient(patient_id)
                    print("患者删除成功。")
                except ValueError as ve:
                    print(f"删除失败: {ve}")
                    logger.error(f"删除失败: {ve}")
            elif choice == '5':
                # 生成健康报告
                patient_id = input("请输入患者ID: ").strip()
                patient = self.data_manager.get_patient(patient_id)
                if patient:
                    # 询问是否输入额外的健康数据
                    extra_data = {}
                    add_extra = input("是否输入额外的健康数据（心率、体温）？(y/n): ").strip().lower()
                    if add_extra == 'y':
                        heart_rate = int(input("请输入心率(bpm): ").strip())
                        temperature = float(input("请输入体温(℃): ").strip())
                        extra_data['heart_rate'] = heart_rate
                        extra_data['temperature'] = temperature
                    try:
                        report = self.health_analyzer.generate_health_report(patient, extra_data)
                        print("健康报告生成成功。")
                        print(report)
                    except Exception as e:
                        print(f"生成报告失败: {e}")
                        logger.error(f"生成报告失败: {e}")
                else:
                    print("未找到该患者。")
            elif choice == '6':
                # 导入数据
                file_path = input("请输入要导入的文件路径: ").strip()
                file_type = input("请输入文件类型(csv/json): ").strip().lower()
                try:
                    self.data_manager.import_data(file_path, file_type)
                    print("数据导入成功。")
                except Exception as e:
                    print(f"数据导入失败: {e}")
                    logger.error(f"数据导入失败: {e}")
            elif choice == '7':
                # 导出数据
                file_path = input("请输入要导出的文件路径: ").strip()
                file_type = input("请输入文件类型(csv/json): ").strip().lower()
                try:
                    self.data_manager.export_data(file_path, file_type)
                    print("数据导出成功。")
                except Exception as e:
                    print(f"数据导出失败: {e}")
                    logger.error(f"数据导出失败: {e}")
            elif choice == '8':
                # 退出系统
                print("感谢使用，再见！")
                sys.exit()
            else:
                print("无效的选择，请重新输入。")

if __name__ == "__main__":
    print("启动健康记录管理系统...")
    system = HealthSystem()
    system.run()
