from crawler_services.native_services.mongo_manager.mongo_enums import MONGODB_COLLECTIONS, MONGODB_KEYS, \
    MONGODB_COMMANDS
from crawler_services.shared_model.request_handler import request_handler


class mongo_request_generator(request_handler):

    def __init__(self):
        pass

    def __on_reset_backup_url(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_BACKUP_MODEL, MONGODB_KEYS.S_FILTER:{}, MONGODB_KEYS.S_VALUE:{"$set":{"m_parsing":False}}}

    def __on_set_parse_url(self, p_data):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_INDEX_MODEL, MONGODB_KEYS.S_FILTER:{"m_url": {"$eq": p_data.m_url}}, MONGODB_KEYS.S_VALUE:{"$set": {"m_title": p_data.m_title, "m_description": p_data.m_description, "m_keyword" : p_data.m_keyword, "m_content_type" : p_data.m_content_type }}}

    def __on_set_backup_url(self, p_data):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_BACKUP_MODEL, MONGODB_KEYS.S_VALUE:{"m_host": p_data.m_host, "m_parsing": False, "m_catagory": p_data.m_catagory}}

    def __on_get_parsed_url(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_INDEX_MODEL, MONGODB_KEYS.S_FILTER:{}}

    def __on_clear_index(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_INDEX_MODEL, MONGODB_KEYS.S_FILTER:{}}

    def __on_clear_backup(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_BACKUP_MODEL, MONGODB_KEYS.S_FILTER:{}}

    def __on_clear_tfidf(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_TFIDF_MODEL, MONGODB_KEYS.S_FILTER:{}}

    def __on_get_unparsed_url(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_BACKUP_MODEL, MONGODB_KEYS.S_FILTER: {"m_parsing": {"$eq": False}}}

    def __on_get_backup_url(self, p_doc_id):
        m_document_list_id = p_doc_id
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_BACKUP_MODEL, MONGODB_KEYS.S_FILTER:{"_id": {"$in": m_document_list_id}}, MONGODB_KEYS.S_VALUE:{"$set":{"m_parsing":True}}}

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == MONGODB_COMMANDS.S_GET_PARSE_URL:
            return self.__on_get_parsed_url()
        if p_commands == MONGODB_COMMANDS.S_RESET_BACKUP_URL:
            return self.__on_reset_backup_url()
        if p_commands == MONGODB_COMMANDS.S_SAVE_PARSE_URL:
            return self.__on_set_parse_url(p_data[0])
        if p_commands == MONGODB_COMMANDS.S_SAVE_BACKUP:
            return self.__on_set_backup_url(p_data[0])
        if p_commands == MONGODB_COMMANDS.S_CLEAR_INDEX:
            return self.__on_clear_index()
        if p_commands == MONGODB_COMMANDS.S_CLEAR_BACKUP:
            return self.__on_clear_backup()
        if p_commands == MONGODB_COMMANDS.S_CLEAR_TFIDF:
            return self.__on_clear_tfidf()
        elif p_commands == MONGODB_COMMANDS.S_GET_UNPARSED_URL:
            return self.__on_get_unparsed_url()
        elif p_commands == MONGODB_COMMANDS.S_SET_BACKUP_URL:
            return self.__on_get_backup_url(p_data[0])
