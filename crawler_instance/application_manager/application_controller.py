# Libraries
from crawler_instance.application_manager.application_enums import APPICATION_COMMANDS
from crawler_instance.constants.strings import ERROR_MESSAGES
from crawler_instance.crawl_manager.crawl_enums import CRAWL_CONTROLLER_COMMANDS
from crawler_services.native_services.topic_classifier_manager.topic_classifier_enums import TOPIC_CLASSFIER_COMMANDS
from crawler_shared_directory.request_model.request_handler import request_handler
from crawler_services.native_services.topic_classifier_manager.topic_classifier import topic_classifier
from crawler_instance.crawl_manager.crawl_controller import crawl_controller


class application_controller(request_handler):
    __instance = None
    __m_crawl_controller = None

    # Initializations
    @staticmethod
    def get_instance():
        if application_controller.__instance is None:
            application_controller()
        return application_controller.__instance

    def __init__(self):
        if application_controller.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            self.__m_crawl_controller = crawl_controller()
            application_controller.__instance = self


    # External Reuqest Callbacks
    def __on_start(self):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_RUN_GENERAL_CRAWLER)

    def __on_start_classifier_crawl(self):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_RUN_TOPIC_CLASSIFIER_CRAWLER)

    def __on_load_classifier_dataset(self):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_LOAD_TOPIC_CLASSIFIER_DATASET)

    # External Reuqest Manager
    def invoke_trigger(self, p_command, p_data=None):
        if p_command == APPICATION_COMMANDS.S_LOAD_TOPIC_CLASSIFIER_DATASET:
            return self.__on_load_classifier_dataset()
        if p_command == APPICATION_COMMANDS.S_CRAWL_TOPIC_CLASSIFIER_DATASET:
            return self.__on_start_classifier_crawl()
        if p_command == APPICATION_COMMANDS.S_INSTALL_TOPIC_CLASSIFIER:
            topic_classifier.get_instance().invoke_trigger(TOPIC_CLASSFIER_COMMANDS.S_GENERATE_CLASSIFIER)
