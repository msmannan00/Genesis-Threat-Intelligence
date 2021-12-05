import enum


class ERROR_MESSAGES(enum.Enum):
    S_SINGLETON_EXCEPTION = "This class is a singleton"
    S_DATABASE_FETCH_ERROR = "Database Load Error : Database Empty"


class INFO_MESSAGES(enum.Enum):
    S_LOADING_BACKUP_URL = "[1] Loading Backup URL"
    S_BACKUP_QUEUE_EMPTY = "Backup Queue Empty"
    S_THREAD_CREATED = "THREAD CREATED : "