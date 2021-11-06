import enum


class MONGODB_COMMANDS(enum.Enum):
    S_CLEAR_DATA = '-1'
    S_CLEAR_DATA_INVOKE = '0'
    S_SAVE_BACKUP = '1'
    S_SAVE_PARSE_URL = '2'
    S_BACKUP_URL = '3'
    S_GET_PARSE_URL = '4'
    S_RESET_BACKUP_URL = '5'
    S_FETCH_UNIQUE_HOST = '6'
    S_ADD_UNIQUE_HOST = '7'


class MONGODB_COLLECTIONS(enum.Enum):
    S_INDEX_MODEL = 'index_model'
    S_BACKUP_MODEL = 'backup_model'
    S_UNIQUE_HOST_MODEL = 'unique_host'
    S_TFIDF_MODEL = 'tfidf_model'
