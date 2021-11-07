# Local Imports
import time

from CrawlerInstance.crawlController.crawlEnums import CRAWLER_STATUS
from CrawlerInstance.helperServices.helperMethod import helperMethod
from CrawlerInstance.iCrawlController.iCrawlEnums import ICRAWL_CONTROLLER_COMMANDS
from CrawlerInstance.sharedModel.requestHandler import requestHandler
from GenesisCrawlerServices.crawlerServices.mongoDB.mongoEnums import MONGODB_COMMANDS
from GenesisCrawlerServices.helperServices.duplicationHandler import duplicationHandler
from CrawlerInstance.iCrawlController.parseManager import parseManager
from CrawlerInstance.classModels.indexModel import indexModel
from CrawlerInstance.iCrawlController.webRequestManager import webRequestManager
from GenesisCrawlerServices.crawlerServices.mongoDB.mongoController import mongo_controller


class iCrawlController(requestHandler):

    __m_web_request_handler = None
    __m_duplication_handler = None
    __m_request_model = None
    __m_html_parser = None

    __m_parsed_model = None
    __m_thread_status = CRAWLER_STATUS.S_RUNNING

    def __init__(self):
        self.m_html_parser = parseManager()
        self.__m_duplication_handler = duplicationHandler()
        self.__m_web_request_handler = webRequestManager()

    def __trigger_url_request(self, p_request_model):
        # Initialize
        m_redirected_url, response, html = self.__m_web_request_handler.load_url(p_request_model.get_url())

        # Normalize Slashes
        m_redirected_requested_url = helperMethod.normalize_slashes(p_request_model.get_url())
        m_redirected_url = helperMethod.normalize_slashes(m_redirected_url)

        # Parse HTML
        if response is True:
            m_parsed_model = self.m_html_parser.on_parse_html(html, m_redirected_requested_url)

            # Filter Non Interesting URL
            if m_redirected_url == m_redirected_requested_url or m_redirected_url != m_redirected_requested_url and self.__m_duplication_handler.validate_duplicate_url(m_redirected_url) is False:
                self.__m_duplication_handler.insert_url(m_redirected_url)

                if m_parsed_model.get_validity_score() == 1:
                    mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_SAVE_PARSE_URL,m_parsed_model)
        else:
            m_parsed_model = indexModel(p_url=p_request_model.get_url())

        return m_parsed_model

    # Wait For Crawl Manager To Provide URL From Queue
    def __start_crawler_instance(self, p_request_model):
        self.__invoke_thread(True, p_request_model)
        while self.__m_thread_status in [CRAWLER_STATUS.S_RUNNING, CRAWLER_STATUS.S_PAUSE]:
            if self.__m_thread_status == CRAWLER_STATUS.S_RUNNING:
                self.__m_parsed_model = self.__trigger_url_request(self.__m_request_model)
                self.__m_thread_status = CRAWLER_STATUS.S_PAUSE
            time.sleep(2)

    # Crawl Manager Awakes Crawler Instance From Sleep
    def __invoke_thread(self, p_status, p_request_model):
        if p_status is True:
            self.__m_request_model = p_request_model
            self.__m_thread_status = CRAWLER_STATUS.S_RUNNING
        else:
            self.__m_thread_status = CRAWLER_STATUS.S_STOP

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE:
            self.__start_crawler_instance(p_data[0])
        if p_command == ICRAWL_CONTROLLER_COMMANDS.S_GET_CRAWLED_DATA:
            return self.__m_parsed_model, self.__m_thread_status
        if p_command == ICRAWL_CONTROLLER_COMMANDS.S_INVOKE_THREAD:
            return self.__invoke_thread(p_data[0], p_data[1])
