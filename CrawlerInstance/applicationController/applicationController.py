# Libraries
import sys

from GenesisCrawlerServices.crawlerServices.mongoDB.mongoController import mongo_controller
from GenesisCrawlerServices.crawlerServices.mongoDB.mongoEnums import MONGODB_COMMANDS

sys.path.append('C:\Workspace\Genesis-Crawler')
from CrawlerInstance.applicationController.applicationEnums import APPICATION_COMMANDS
from CrawlerInstance.crawlController.crawlEnums import CRAWL_CONTROLLER_COMMANDS
from CrawlerInstance.logManager.logEnums import ERROR_MESSAGES
from GenesisCrawlerServices.crawlerServices.topicClassifier.topicClassifierEnums import TOPIC_CLASSFIER_COMMANDS
from CrawlerInstance.sharedModel.requestHandler import requestHandler
from GenesisCrawlerServices.crawlerServices.topicClassifier.topicClassifier import TopicClassifier
from CrawlerInstance.crawlController.crawlController import crawlController


class applicationController(requestHandler):
    __instance = None
    __m_crawl_controller = None

    # Initializations
    @staticmethod
    def get_instance():
        if applicationController.__instance is None:
            applicationController()
        return applicationController.__instance

    def __init__(self):
        if applicationController.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            self.__m_crawl_controller = crawlController()
            applicationController.__instance = self


    # External Reuqest Callbacks
    def __on_start(self):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_RUN_GENERAL_CRAWLER)

    def __on_start_classifier_crawl(self):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_RUN_TOPIC_CLASSIFIER_CRAWLER)

    def __on_load_classifier_dataset(self):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_LOAD_TOPIC_CLASSIFIER_DATASET)

    # External Reuqest Manager
    def invoke_trigger(self, p_command, p_data=None):
        if p_command == APPICATION_COMMANDS.S_START_APPLICATION:
            return self.__on_start()
        if p_command == APPICATION_COMMANDS.S_CRAWL_TOPIC_CLASSIFIER_DATASET:
            return self.__on_start_classifier_crawl()
        if p_command == APPICATION_COMMANDS.S_LOAD_TOPIC_CLASSIFIER_DATASET:
            return self.__on_load_classifier_dataset()
        if p_command == APPICATION_COMMANDS.S_INSTALL_TOPIC_CLASSIFIER:
            TopicClassifier.get_instance().invoke_trigger(TOPIC_CLASSFIER_COMMANDS.S_GENERATE_CLASSIFIER)

# mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_CLEAR_DATA, None)
mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_RESET_BACKUP_URL, None)
applicationController.get_instance().invoke_trigger(APPICATION_COMMANDS.S_CRAWL_TOPIC_CLASSIFIER_DATASET)
