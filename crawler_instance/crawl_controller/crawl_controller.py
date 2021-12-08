# Local Imports
import threading
import pandas as pd

from crawler_instance.constants.constants import CRAWL_SETTINGS_CONSTANTS, RAW_PATH_CONSTANTS
from crawler_instance.crawl_controller.crawl_enums import CRAWLER_STATUS, CRAWL_MODEL_COMMANDS, CRAWL_CONTROLLER_COMMANDS, CLASSIFIER
from crawler_instance.i_crawl_controller.i_crawl_enums import ICRAWL_CONTROLLER_COMMANDS
from crawler_instance.log_manager.log_enums import INFO_MESSAGES
from crawler_instance.request_handler.request_handler import request_handler
from crawler_instance.crawl_controller.crawl_model import crawl_model
from crawler_instance.i_crawl_controller.i_crawl_controller import i_crawl_controller


class crawl_controller(request_handler):

    # Local Variables
    __m_crawl_model = None

    # Crawler Instances & Threads
    __m_main_thread = None
    __m_crawler_instance_list = []

    # Initializations
    def __init__(self):
        self.__m_crawl_model = crawl_model()

    # Start Crawler Manager
    def __load_classifier_from_database(self):
        data = pd.read_csv(RAW_PATH_CONSTANTS.S_PROJECT_PATH + RAW_PATH_CONSTANTS.S_DATASET_PATH)
        data = data.sample(frac=1).reset_index(drop=True)
        for index, row in data.iterrows():
            self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_SAVE_BACKUP_URL, [(row[CLASSIFIER.S_CLASSIFIER_URL]), row[CLASSIFIER.S_CLASSIFIER_LABEL]])

    def __on_run_topic_classifier(self):
        self.__m_main_thread = threading.Thread(target=self.__init_thread_manager)
        self.__m_main_thread.start()

    # ICrawler Manager
    def __init_thread_manager(self):
        while True:
            self.__crawler_instance_manager()
            while len(self.__m_crawler_instance_list) < CRAWL_SETTINGS_CONSTANTS.S_MAX_THREAD_COUNT_PER_INSTANCE:
                m_status, m_url_model = self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_GET_HOST_URL)
                if m_status is False:
                    break
                else:
                    m_icrawler_instance = i_crawl_controller()
                    self.__m_crawler_instance_list.insert(0, m_icrawler_instance)
                    thread_instance = threading.Thread(target=self.__create_crawler_instance, args=(m_url_model,m_icrawler_instance,))
                    thread_instance.start()


    # Awake Crawler From Sleep
    def __crawler_instance_manager(self):
        for m_crawl_instance in self.__m_crawler_instance_list:
            m_index_model, m_thread_status = m_crawl_instance.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_GET_CRAWLED_DATA)
            if m_thread_status == CRAWLER_STATUS.S_STOP:
                self.__m_crawler_instance_list.remove(m_crawl_instance)
            elif m_thread_status == CRAWLER_STATUS.S_PAUSE:
                m_crawl_instance.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_INVOKE_THREAD,[False, None])

    def __create_crawler_instance(self, p_url_model, p_crawler_instance):

        # Creating Thread Instace
        m_crawler_instance = p_crawler_instance

        # Saving Thread Instace
        print(INFO_MESSAGES.S_THREAD_CREATED + str(len(self.__m_crawler_instance_list)))

        # Start Thread Instace
        m_crawler_instance.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE, [p_url_model])

    # Try To Get Job For Crawler Instance
    def invoke_trigger(self, p_command, p_data=None):
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_RUN_TOPIC_CLASSIFIER_CRAWLER:
            self.__on_run_topic_classifier()
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_LOAD_TOPIC_CLASSIFIER_DATASET:
            self.__load_classifier_from_database()
