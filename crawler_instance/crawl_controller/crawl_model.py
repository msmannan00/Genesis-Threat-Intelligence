# Local Libraries
from crawler_instance.class_models.backup_model import backup_model
from crawler_instance.constants import constants, application_status
from crawler_instance.crawl_controller.crawl_enums import CRAWL_MODEL_COMMANDS, DOCUMENT_INDEX
from crawler_instance.helper_method.helper_method import helper_method
from crawler_instance.log_manager.log_enums import ERROR_MESSAGES, INFO_MESSAGES
from crawler_instance.request_handler.request_handler import request_handler
from genesis_crawler_services.constants import strings, keys
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
            self.__m_duplication_handler.insert_url(m_document[DOCUMENT_INDEX.S_HOST.value])

    def __calculate_depth(self, p_url, p_base_url_model):
        depth = 1
        new_url_host = helper_method.get_host_url(p_url)
        parent_host = helper_method.get_host_url(p_base_url_model.m_redirected_url)

        if new_url_host == parent_host:
            try:
                depth = p_base_url_model.m_redirected_url.__m_depth + 1
            except Exception as e:
                log.g().e(str(e))
        else:
            depth = constants.S_MAX_ALLOWED_DEPTH - 1

        return depth

    # Insert To Database - Insert URL to database after parsing them
    def __insert_url(self, p_url, p_base_url_model):
        m_url = helper_method.on_clean_url(helper_method.normalize_slashes(p_url + "////"))
        m_url_depth = self.__calculate_depth(m_url, p_base_url_model)

        m_url_host = helper_method.get_host_url(p_url)
        if m_url_host not in self.__m_url_queue.keys():
            if len(self.__m_url_queue) < constants.S_MAX_HOST_QUEUE_SIZE:
                m_fresh_url_model = queue_url_model(p_url, m_url_depth, p_base_url_model.m_content_type)
                if self.__m_duplication_handler.validate_duplicate_url(m_url_host) is False:
                    self.__m_duplication_handler.insert_url(m_url_host)
                    self.__m_url_queue[m_url_host] = [m_fresh_url_model]
                    self.__m_inactive_queue_keys.append(m_url_host)
            else:
                self.__save_backup_url_to_drive(p_url, m_url_depth)
                application_status.S_QUEUE_BACKUP_STATUS = True
        else:
            if "?" not in p_url:
                self.__m_url_queue[m_url_host].insert(0, queue_url_model(p_url, m_url_depth, p_base_url_model.m_content_type))

    def __save_backup_url_to_drive(self, p_url, p_url_depth, p_category = None):
        if self.__m_duplication_handler.validate_duplicate_url(p_url) is False:
            application_status.S_QUEUE_BACKUP_STATUS = True
            m_host = helper_method.get_host_url(p_url)
            m_subhost = p_url.replace(m_host, strings.S_EMPTY)
            if p_category is not None:
                m_data = backup_model(m_host, m_subhost, p_url_depth, p_category)
            else:
                m_data = backup_model(m_host, m_subhost, p_url_depth, constants.S_THREAD_CATEGORY_GENERAL)
            mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_SAVE_BACKUP, m_data)
        else:
            self.__m_duplication_handler.insert_url(p_url)

    # Extract Fresh Host URL
    def __get_host_url(self):
        if len(self.__m_inactive_queue_keys) <= 0:
            if application_status.S_QUEUE_BACKUP_STATUS is True:
                self.__load_backup_url()

        if len(self.__m_inactive_queue_keys) > 0:
            m_url_key = self.__m_inactive_queue_keys.pop(0)
            m_url_model = self.__m_url_queue.get(m_url_key).pop(0)
            self.__m_active_queue_keys.append(m_url_key)

            return True, m_url_model
        else:
            return False, None

    # Extract Sub URL - Extract url in relation to host extracted in above ^ function
    def __get_sub_url(self, p_host_url):
        m_url_host = helper_method.get_host_url(p_host_url)
        if m_url_host in self.__m_url_queue and len(self.__m_url_queue[m_url_host]) > 0:
            m_url_model = self.__m_url_queue.get(m_url_host).pop(0)
            return True, m_url_model
        else:
            self.__m_active_queue_keys.remove(m_url_host)
            self.__m_url_queue.pop(m_url_host, None)
            mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_ADD_UNIQUE_HOST, m_url_host)
            mongo_controller.get_instance().invoke_trigger(m_url_host, None)
            return False, None

    def __load_backup_url(self):
        m_data = backup_model(strings.S_EMPTY, strings.S_EMPTY, strings.S_EMPTY, constants.S_THREAD_CATEGORY_GENERAL)
        response, data = mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_BACKUP_URL, m_data)
        if response is True:
            for data_item in data:
                for m_url_model in data_item[keys.K_URL_DATA]:
                    p_url = data_item[keys.K_HOST] + m_url_model[keys.K_SUB_HOST]
                    p_depth = int(m_url_model[keys.K_DEPTH])
                    p_type = data_item['m_catagory'].lower()
                    m_url_host = helper_method.get_host_url(p_url)
                    if m_url_host not in self.__m_url_queue.keys():
                        m_fresh_url_model = queue_url_model(p_url, p_depth, p_type)
                        self.__m_url_queue[m_url_host] = [m_fresh_url_model]
                        self.__m_inactive_queue_keys.append(m_url_host)
                    else:
                        self.__m_url_queue[m_url_host].append(queue_url_model(p_url, p_depth, p_type))

            log.g().i(INFO_MESSAGES.S_LOADING_BACKUP_URL.value)
            if len(data) < constants.S_BACKUP_FETCH_LIMIT:
                log.g().e(INFO_MESSAGES.S_BACKUP_QUEUE_EMPTY.value)
                application_status.S_QUEUE_BACKUP_STATUS = False
        else:
            log.g().e(ERROR_MESSAGES.S_DATABASE_FETCH_ERROR.value)
            application_status.S_QUEUE_BACKUP_STATUS = False

    def __m_crawl_finished_status(self):
        return len(self.__m_url_queue)==0 and len(self.__m_inactive_queue_keys)==0 and len(self.__m_active_queue_keys)==0

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == CRAWL_MODEL_COMMANDS.S_SAVE_BACKUP_URL:
           return self.__save_backup_url_to_drive(p_data[0],p_data[1],p_data[2])
        if p_command == CRAWL_MODEL_COMMANDS.S_GET_HOST_URL:
           return self.__get_host_url()
        if p_command == CRAWL_MODEL_COMMANDS.S_INSERT_URL:
           return self.__insert_url(p_data[0], p_data[1])
        if p_command == CRAWL_MODEL_COMMANDS.S_GET_SUB_URL:
           return self.__get_sub_url(p_data[0])
        if p_command == CRAWL_MODEL_COMMANDS.S_CRAWL_FINISHED_STATUS:
           return self.__m_crawl_finished_status()

