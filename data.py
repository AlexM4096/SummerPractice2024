import os
import shutil

main_directory = os.getcwd()

kaggle_dataset_directory_name = 'kaggle-dataset'
kaggle_dataset_directory = os.path.join(main_directory, kaggle_dataset_directory_name)

kaggle_dataset_cvs_name = 'WILDCATS.CSV'
kaggle_dataset_cvs_path = os.path.join(kaggle_dataset_directory, kaggle_dataset_cvs_name)


def create_directories_if_needed():
    os.makedirs(kaggle_dataset_directory, exist_ok=True)


def clear_directories():
    clear_directory(kaggle_dataset_directory)


def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
