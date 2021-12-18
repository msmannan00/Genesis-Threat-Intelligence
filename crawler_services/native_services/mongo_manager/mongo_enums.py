import enum

class MONGO_CRUD(enum.Enum):
    S_CREATE = '1'
    S_READ = '2'
    S_UPDATE = '3'
    S_DELETE = '4'

class MONGODB_COMMANDS(enum.Enum):
    S_CLEAR_DATA = '-1'
    S_CLEAR_DATA_INVOKE = '0'
    S_SAVE_BACKUP = '1'
    S_SAVE_PARSE_URL = '2'
    S_SET_BACKUP_URL = '3'
    S_GET_PARSE_URL = '4'
    S_RESET_BACKUP_URL = '5'
    S_CLEAR_INDEX = '8'
    S_CLEAR_BACKUP = '9'
    S_CLEAR_TFIDF = '10'
    S_GET_UNPARSED_URL = '13'


class MONGODB_COLLECTIONS:
    S_INDEX_MODEL = 'index_model'
    S_BACKUP_MODEL = 'backup_model'
    S_TFIDF_MODEL = 'tfidf_model'

class MONGODB_KEYS:
    S_DOCUMENT = 'm_document'
    S_FILTER = 'm_filter'
    S_VALUE = 'm_value'

class MANAGE_USER_MESSAGES:
    S_INSERT_FAILURE = "[1] Something unexpected happened while inserting"
    S_INSERT_SUCCESS = "[2] Document Created Successfully"
    S_UPDATE_FAILURE = "[3] Something unexpected happened while updating"
    S_UPDATE_SUCCESS = "[4] Data Updated Successfully"
    S_DELETE_FAILURE = "[5] Something unexpected happened while deleting"
    S_DELETE_SUCCESS = "[6] Data Deleted Successfully"
    S_READ_FAILURE = "[5] Something unexpected happened while reading"
    S_READ_SUCCESS = "[6] Data Read Successfully"
