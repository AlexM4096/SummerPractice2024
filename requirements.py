import os
import subprocess
import zipfile

from data import main_directory, kaggle_dataset_directory


install_requirements_command = 'pip install -U -r requirements.txt'
kaggle_api_command = 'kaggle datasets download -d gpiosenka/cats-in-the-wild-image-classification'
kaggle_dataset_zip_name = 'cats-in-the-wild-image-classification.zip'
kaggle_dataset_zip_path = os.path.join(main_directory, kaggle_dataset_zip_name)


def install_requirements_if_needed():
    subprocess.run(install_requirements_command)

    if not os.path.isfile(kaggle_dataset_zip_path):
        subprocess.run(kaggle_api_command)

    with zipfile.ZipFile(kaggle_dataset_zip_path) as dataset_zip:
        dataset_zip.extractall(kaggle_dataset_directory)
