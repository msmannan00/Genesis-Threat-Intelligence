# Local Libraries
from crawler_instance.class_models.backup_model import backup_model
from crawler_instance.constants.application_status import CRAWL_STATUS
from crawler_instance.constants.constant import CRAWL_SETTINGS_CONSTANTS
from crawler_instance.constants.keys import classifier_constants
from crawler_instance.constants.strings import GENERIC_STRINGS
from crawler_instance.crawl_controller.crawl_enums import CRAWL_MODEL_COMMANDS, DOCUMENT_INDEX
from crawler_instance.helper_method.helper_method import helper_method
from crawler_instance.log_manager.log_enums import ERROR_MESSAGES, INFO_MESSAGES
from crawler_instance.request_handler.request_handler import request_handler
from genesis_crawler_services.crawler_services.mongo.mongo_enums import MONGODB_COMMANDS
from genesis_crawler_services.helper_services.duplication_handler import duplication_handler
from crawler_instance.class_models.queue_url_model import queue_url_model
from crawler_instance.log_manager.log_manager import log
from genesis_crawler_services.crawler_services.mongo.mongo_controller import mongo_controller


# URL Queue Manager
class crawl_model(request_handler):

    # Local Queues
    __m_url_queue = {}
    __m_active_queue_keys = []
    __m_inactive_queue_keys = []

    # Local Variables
    __m_duplication_handler = None

    # Helper Methods
    def __init__(self):
        self.__m_url_queue = dict()
        self.__m_duplication_handler = duplication_handler()
        self.__init_duplication_handler()

    def __init_duplication_handler(self):
        m_parsed_hosts = mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_FETCH_UNIQUE_HOST, None)

        for m_document in m_parsed_hosts:
            self.__m_duplication_handler.insert_url(m_document[DOCUMENT_INDEX.S_HOST])

    # Insert To Database - Insert URL to database after parsing them
    def __insert_url(self, p_url, p_base_url_model):
        m_url = helper_method.on_clean_url(helper_method.normalize_slashes(p_url + "////"))
        m_url_host = helper_method.get_host_url(m_url)
        if m_url_host not in self.__m_url_queue.keys():
            if len(self.__m_url_queue) < CRAWL_SETTINGS_CONSTANTS.S_MAX_HOST_QUEUE_SIZE:
                m_fresh_url_model = queue_url_model(p_url, p_base_url_model.m_content_type)
                if self.__m_duplication_handler.validate_duplicate_url(m_url_host) is False:
                    self.__m_duplication_handler.insert_url(m_url_host)
                    self.__m_url_queue[m_url_host] = [m_fresh_url_model]
                    self.__m_inactive_queue_keys.append(m_url_host)
            else:
                self.__save_backup_url_to_drive(p_url)
                CRAWL_STATUS.S_QUEUE_BACKUP_STATUS = True

    def __save_backup_url_to_drive(self, p_url, p_category = None):
        if self.__m_duplication_handler.validate_duplicate_url(p_url) is False:
            self.__m_duplication_handler.insert_url(p_url)
            CRAWL_STATUS.S_QUEUE_BACKUP_STATUS = True
            m_host = helper_method.get_host_url(p_url)
            if p_category is not None:
                m_data = backup_model(m_host, p_category)
            else:
                m_data = backup_model(m_host, CRAWL_SETTINGS_CONSTANTS.S_THREAD_CATEGORY_GENERAL)
            mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_SAVE_BACKUP, m_data)

    # Extract Fresh Host URL
    def __get_host_url(self):
        if len(self.__m_inactive_queue_keys) <= 0:
            if CRAWL_STATUS.S_QUEUE_BACKUP_STATUS is True:
                self.__load_backup_url()

        if len(self.__m_inactive_queue_keys) > 0:
            m_url_key = self.__m_inactive_queue_keys.pop(0)
            m_url_model = self.__m_url_queue.get(m_url_key).pop(0)
            self.__m_active_queue_keys.append(m_url_key)

            return True, m_url_model
        else:
            return False, None

    # Extract Sub URL - Extract url in relation to host extracted in above ^ function
    def __load_backup_url(self):
        m_data = backup_model(GENERIC_STRINGS.S_EMPTY, CRAWL_SETTINGS_CONSTANTS.S_THREAD_CATEGORY_GENERAL)
        response, data = mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_BACKUP_URL, m_data)
        if response is True:
            for data_item in data:
                p_url = data_item[classifier_constants.S_MONGO_HOST]
                p_type = data_item['m_catagory'].lower()
                m_url_host = helper_method.get_host_url(p_url)
                if m_url_host not in self.__m_url_queue.keys():
                    m_fresh_url_model = queue_url_model(p_url, p_type)
                    self.__m_url_queue[m_url_host] = [m_fresh_url_model]
                    self.__m_inactive_queue_keys.append(m_url_host)
                else:
                    self.__m_url_queue[m_url_host].append(queue_url_model(p_url, p_type))

            log.g().i(INFO_MESSAGES.S_LOADING_BACKUP_URL)
            if len(data) < CRAWL_SETTINGS_CONSTANTS.S_BACKUP_FETCH_LIMIT:
                log.g().e(INFO_MESSAGES.S_BACKUP_QUEUE_EMPTY)
                CRAWL_STATUS.S_QUEUE_BACKUP_STATUS = False
        else:
            log.g().e(ERROR_MESSAGES.S_DATABASE_FETCH_ERROR)
            CRAWL_STATUS.S_QUEUE_BACKUP_STATUS = False

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == CRAWL_MODEL_COMMANDS.S_SAVE_BACKUP_URL:
           return self.__save_backup_url_to_drive(p_data[0],p_data[1])
        if p_command == CRAWL_MODEL_COMMANDS.S_GET_HOST_URL:
           return self.__get_host_url()
        if p_command == CRAWL_MODEL_COMMANDS.S_INSERT_URL:
           return self.__insert_url(p_data[0], p_data[1])


