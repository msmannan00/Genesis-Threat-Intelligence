# Local Imports
import threading
import pandas as pd

from CrawlerInstance.constants import constants
from CrawlerInstance.constants.applicationStatus import S_QUEUE_BACKUP_STATUS
from CrawlerInstance.crawlController.crawlEnums import CRAWLER_STATUS, CRAWL_MODEL_COMMANDS, CRAWL_CONTROLLER_COMMANDS, \
    CLASSIFIER
from CrawlerInstance.iCrawlController.iCrawlEnums import ICRAWL_CONTROLLER_COMMANDS
from CrawlerInstance.logManager.logEnums import INFO_MESSAGES
from CrawlerInstance.sharedModel.requestHandler import requestHandler
from CrawlerInstance.crawlController.crawlModel import crawlModel
from CrawlerInstance.iCrawlController.iCrawlController import iCrawlController


class crawlController(requestHandler):

    # Local Variables
    __m_crawl_model = None

    # Crawler Instances & Threads
    __m_main_thread = None
    __m_crawler_instance_list = []

    # Initializations
    def __init__(self):
        self.__m_crawl_model = crawlModel()

    # Start Crawler Manager
    def __load_classifier_from_database(self):
        data = pd.read_csv(constants.S_PROJECT_PATH + constants.S_DATASET_PATH)
        data = data.sample(frac=1).reset_index(drop=True)
        for index, row in data.iterrows():
            try:
                if row[CLASSIFIER.S_CLASSIFIER_LABEL.value] == CLASSIFIER.S_CLASSIFIER_NEWS.value or row[CLASSIFIER.S_CLASSIFIER_LABEL.value] == CLASSIFIER.S_CLASSIFIER_BUSINESS.value or row[CLASSIFIER.S_CLASSIFIER_LABEL.value] == CLASSIFIER.S_CLASSIFIER_ADULT.value:
                    self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_SAVE_BACKUP_URL, [(row[CLASSIFIER.S_CLASSIFIER_URL.value]), 0, row[CLASSIFIER.S_CLASSIFIER_LABEL.value]])
            except Exception as e:
                pass

    def __on_run_topic_classifier(self):
        self.__m_main_thread = threading.Thread(target=self.__init_thread_manager)
        self.__m_main_thread.start()

    def __on_run_general(self):
        self.__m_main_thread = threading.Thread(target=self.__init_thread_manager)
        self.__m_main_thread.start()

    # ICrawler Manager
    def __init_thread_manager(self):
        self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_SAVE_BACKUP_URL, [constants.S_START_URL,constants.S_MAX_ALLOWED_DEPTH-1, constants.S_THREAD_CATEGORY_GENERAL])
        while True:
            self.__crawler_instance_manager()
            while len(self.__m_crawler_instance_list) < constants.S_MAX_THREAD_COUNT_PER_INSTANCE:
                m_status, m_url_model = self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_GET_HOST_URL)
                if m_status is False:
                    break
                else:
                    m_icrawler_instance = iCrawlController()
                    self.__m_crawler_instance_list.insert(0, m_icrawler_instance)
                    thread_instance = threading.Thread(target=self.__create_crawler_instance, args=(m_url_model,m_icrawler_instance,))
                    thread_instance.start()

            threading.Event().wait(constants.S_CRAWLER_INVOKE_DELAY)
            if S_QUEUE_BACKUP_STATUS is False and len(self.__m_crawler_instance_list)<0:
                m_status = self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_CRAWL_FINISHED_STATUS)
                if m_status:
                    self.__m_crawl_model = crawlModel()
                    self.__m_crawl_model.invoke_trigger(constants.S_START_URL, [0, None])

    # Awake Crawler From Sleep
    def __crawler_instance_manager(self):
        for m_crawl_instance in self.__m_crawler_instance_list:
            m_index_model, m_thread_status = m_crawl_instance.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_GET_CRAWLED_DATA)
            if m_thread_status == CRAWLER_STATUS.S_STOP:
                self.__m_crawler_instance_list.remove(m_crawl_instance)
            elif m_thread_status == CRAWLER_STATUS.S_PAUSE:
                m_status, m_url_model = self.__crawler_instance_job_fetcher(m_index_model)
                m_crawl_instance.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_INVOKE_THREAD,[m_status, m_url_model])

    def __create_crawler_instance(self, p_url_model, p_crawler_instance):

        # Creating Thread Instace
        m_crawler_instance = p_crawler_instance

        # Saving Thread Instace
        print(INFO_MESSAGES.S_THREAD_CREATED.value + str(len(self.__m_crawler_instance_list)))

        # Start Thread Instace
        m_crawler_instance.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE, [p_url_model])

    def __on_save_url(self, p_base_url_model):
        if p_base_url_model.m_sub_url is not None:
            for m_url in p_base_url_model.m_sub_url:
                self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_INSERT_URL, [m_url, p_base_url_model])

    # Try To Get Job For Crawler Instance
    def __crawler_instance_job_fetcher(self, p_index_model):
        self.__on_save_url(p_index_model)
        m_status, m_url_model = self.__m_crawl_model.invoke_trigger(CRAWL_MODEL_COMMANDS.S_GET_SUB_URL, [p_index_model.m_url])

        if m_status:
            return m_status, m_url_model
        else:
            return False, None

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_RUN_GENERAL_CRAWLER:
            self.__on_run_general()
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_RUN_TOPIC_CLASSIFIER_CRAWLER:
            self.__on_run_topic_classifier()
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_LOAD_TOPIC_CLASSIFIER_DATASET:
            self.__load_classifier_from_database()
