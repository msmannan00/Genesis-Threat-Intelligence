# Local Imports
import pymongo

from pymongo import WriteConcern
from crawler_instance.constants.constants import CRAWL_SETTINGS_CONSTANTS
from crawler_instance.log_manager.log_manager import log
from genesis_crawler_services.constants.strings import MESSAGE_STRINGS
from genesis_crawler_services.crawler_services.mongo.mongo_enums import MONGODB_COMMANDS, MONGODB_COLLECTIONS
from genesis_crawler_services.shared_model.request_handler import request_handler


class mongo_controller(request_handler):
    __instance = None
    __m_connection = None

    # Initializations
    @staticmethod
    def get_instance():
        if mongo_controller.__instance is None:
            mongo_controller()
        return mongo_controller.__instance

    def __init__(self):
        mongo_controller.__instance = self
        self.__link_connection()

    def __link_connection(self):
        self.__m_connection = pymongo.MongoClient(CRAWL_SETTINGS_CONSTANTS.S_DATABASE_IP, CRAWL_SETTINGS_CONSTANTS.S_DATABASE_PORT)[CRAWL_SETTINGS_CONSTANTS.S_DATABASE_NAME]

    def __clear_data(self):
        m_collection_index = self.__m_connection[MONGODB_COLLECTIONS.S_INDEX_MODEL]
        m_collection_backup = self.__m_connection[MONGODB_COLLECTIONS.S_BACKUP_MODEL]
        m_collection_tfidf = self.__m_connection[MONGODB_COLLECTIONS.S_TFIDF_MODEL]
        m_collection_m_unique_host = self.__m_connection[MONGODB_COLLECTIONS.S_UNIQUE_HOST_MODEL]
        m_collection_index.delete_many({})
        m_collection_backup.delete_many({})
        m_collection_tfidf.delete_many({})
        m_collection_m_unique_host.delete_many({})

    def __get_parsed_url(self):
        m_collection = self.__m_connection[MONGODB_COLLECTIONS.S_INDEX_MODEL]
        m_collection_result = m_collection.find()

        return m_collection_result

    def __set_backup_url(self, p_data):
        try:
            m_collection = self.__m_connection[MONGODB_COLLECTIONS.S_BACKUP_MODEL]
            myquery = {'m_host': p_data.m_host,
                       'm_parsing': False,
                       'm_catagory': p_data.m_catagory}
            m_collection.insert_one(myquery)
            log.g().i(MESSAGE_STRINGS.S_BACKUP_PARSED + " : " + p_data.m_host)
        except Exception:
            pass

    def __set_parse_url(self, p_data):
        m_collection = self.__m_connection[MONGODB_COLLECTIONS.S_INDEX_MODEL]
        myquery = {'m_url': {'$eq': p_data.m_url}}
        newvalues = {"$set": {'m_title': p_data.m_title,
                              'm_description': p_data.m_description,
                              'm_keyword' : p_data.m_keyword,
                              'm_content_type' : p_data.m_content_type
                              }}
        m_collection.update_one(myquery, newvalues, upsert=True)

        log.g().i(MESSAGE_STRINGS.S_URL_PARSED + " : " + p_data.m_url)

    def __get_backup_url(self, p_data):
        m_collection = self.__m_connection[MONGODB_COLLECTIONS.S_BACKUP_MODEL]
        m_document_list = []
        m_document_list_id = []
        if p_data.m_catagory == "default":
            m_collection_result = m_collection.find({'m_parsing': {'$eq': False}}).limit(CRAWL_SETTINGS_CONSTANTS.S_BACKUP_FETCH_LIMIT)
        else:
            m_collection_result = m_collection.find({'m_parsing': {'$eq': False}}).limit(CRAWL_SETTINGS_CONSTANTS.S_BACKUP_FETCH_LIMIT)

        for m_document in m_collection_result:
            m_document_list.append(m_document)
            m_document_list_id.append(m_document["_id"])

        m_collection.update_many({"_id": {"$in": m_document_list_id}},{"$set":{"m_parsing":True}})
        return len(m_document_list) > 0, m_document_list

    def __reset_backup_url(self):
        m_collection = self.__m_connection[MONGODB_COLLECTIONS.S_BACKUP_MODEL]
        m_collection.update_many({},{"$set":{"m_parsing":False}})

    def __add_unique_host(self, p_data):
        m_collection = self.__m_connection[MONGODB_COLLECTIONS.S_UNIQUE_HOST_MODEL]
        m_collection.with_options(write_concern=WriteConcern(w=0)).insert({'m_host': p_data})

        m_collection = self.__m_connection[MONGODB_COLLECTIONS.S_BACKUP_MODEL]
        m_collection.delete_one({'m_host': p_data})

    def __fetch_unique_host(self):
        m_collection = self.__m_connection[MONGODB_COLLECTIONS.S_UNIQUE_HOST_MODEL]
        m_collection_result = m_collection.find()
        return m_collection_result

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == MONGODB_COMMANDS.S_CLEAR_DATA:
            return self.__clear_data()
        elif p_commands == MONGODB_COMMANDS.S_SAVE_BACKUP:
            return self.__set_backup_url(p_data)
        elif p_commands == MONGODB_COMMANDS.S_SAVE_PARSE_URL:
            return self.__set_parse_url(p_data)
        elif p_commands == MONGODB_COMMANDS.S_BACKUP_URL:
            return self.__get_backup_url(p_data)
        elif p_commands == MONGODB_COMMANDS.S_GET_PARSE_URL:
            return self.__get_parsed_url()
        elif p_commands == MONGODB_COMMANDS.S_RESET_BACKUP_URL:
            return self.__reset_backup_url()
        elif p_commands == MONGODB_COMMANDS.S_ADD_UNIQUE_HOST:
            return self.__add_unique_host(p_data)
        elif p_commands == MONGODB_COMMANDS.S_FETCH_UNIQUE_HOST:
            return self.__fetch_unique_host()
