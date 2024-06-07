import app
import data
import requirements
import trainer
import setup


def main():
    data.create_directories_if_needed()
    if setup.clear_setup:
        data.clear_directories()

    if setup.check_for_requirements:
        requirements.install_requirements_if_needed()

    if setup.need_to_train:
        trainer.train()

    if setup.start_app:
        app.start()


if __name__ == "__main__":
    main()
