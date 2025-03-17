import os
import requests


class CloudSetup:
    def __init__(self):
        self.colab_script_url = "https://raw.githubusercontent.com/your-repo/apollo-colab/main/colab_script.py"
        self.aws_instance_url = "https://your-aws-server.com/start_apollo"
        self.azure_instance_url = "https://your-azure-server.com/start_apollo"

    def start_colab_instance(self):
        """Запускает Аполлона в Google Colab."""
        try:
            response = requests.get(self.colab_script_url)
            if response.status_code == 200:
                print("✅ Google Colab запущен!")
                return f"Google Colab: {self.colab_script_url}"
            else:
                return f"❌ Ошибка запуска Colab: {response.status_code}"
        except Exception as e:
            return f"❌ Ошибка Google Colab: {str(e)}"

    def start_aws_instance(self):
        """Запускает Аполлона на AWS."""
        try:
            response = requests.get(self.aws_instance_url)
            if response.status_code == 200:
                print("✅ AWS-инстанс запущен!")
                return "AWS-инстанс успешно запущен!"
            else:
                return f"❌ Ошибка запуска AWS: {response.status_code}"
        except Exception as e:
            return f"❌ Ошибка AWS: {str(e)}"

    def start_azure_instance(self):
        """Запускает Аполлона на Azure."""
        try:
            response = requests.get(self.azure_instance_url)
            if response.status_code == 200:
                print("✅ Azure-инстанс запущен!")
                return "Azure-инстанс успешно запущен!"
            else:
                return f"❌ Ошибка запуска Azure: {response.status_code}"
        except Exception as e:
            return f"❌ Ошибка Azure: {str(e)}"


# Тестирование запуска
if __name__ == "__main__":
    cloud = CloudSetup()
    print(cloud.start_colab_instance())  # Запускаем Google Colab
    print(cloud.start_aws_instance())    # Запускаем AWS
    print(cloud.start_azure_instance())  # Запускаем Azure
