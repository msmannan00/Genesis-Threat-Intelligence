# Local Imports
import time

from crawler_services.constants.strings import MESSAGE_STRINGS
from native_services.crawl_manager.crawl_enums import CRAWLER_STATUS
from native_services.helper_method.helper_method import helper_method
from native_services.i_crawl_manager.i_crawl_enums import ICRAWL_CONTROLLER_COMMANDS
from native_services.log_manager.log_manager import log
from native_services.request_manager.request_handler import request_handler
from crawler_services.native_services.mongo_manager.mongo_enums import MONGODB_COMMANDS, mongo_crud
from crawler_services.helper_services.duplication_handler import duplication_handler
from native_services.i_crawl_manager.parse_manager import parse_manager
from native_services.shared_models.index_model import index_model
from native_services.i_crawl_manager.web_request_manager import web_request_manager
from crawler_services.native_services.mongo_manager.mongo_controller import mongo_controller


class i_crawl_controller(request_handler):

    __m_web_request_handler = None
    __m_duplication_handler = None
    __m_request_model = None
    __m_html_parser = None

    __m_parsed_model = None
    __m_thread_status = CRAWLER_STATUS.S_RUNNING

    def __init__(self):
        self.m_html_parser = parse_manager()
        self.__m_duplication_handler = duplication_handler()
        self.__m_web_request_handler = web_request_manager()

    def __trigger_url_request(self, p_request_model):
        # Initialize
        m_redirected_url, response, html = self.__m_web_request_handler.load_url(p_request_model.m_url)

        # Normalize Slashes
        m_redirected_requested_url = helper_method.normalize_slashes(p_request_model.m_url)
        m_redirected_url = helper_method.normalize_slashes(m_redirected_url)

        # Parse HTML
        if response is True:
            m_parsed_model = self.m_html_parser.on_parse_html(html, m_redirected_requested_url, p_request_model.m_type)

            # Filter Non Interesting URL
            if m_redirected_url == m_redirected_requested_url or m_redirected_url != m_redirected_requested_url and self.__m_duplication_handler.validate_duplicate_url(m_redirected_url) is False:
                self.__m_duplication_handler.insert_url(m_redirected_url)

                if m_parsed_model.m_validity_score == 1:
                    mongo_controller.get_instance().invoke_trigger(mongo_crud.S_UPDATE, [MONGODB_COMMANDS.S_SAVE_PARSE_URL, True, m_parsed_model])
                    log.g().s(MESSAGE_STRINGS.S_URL_PARSED + " : " + m_parsed_model.m_url)
        else:
            m_parsed_model = index_model(p_url=p_request_model.m_url)

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
