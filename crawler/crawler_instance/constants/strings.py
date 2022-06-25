from crawler.crawler_instance.constants.app_status import TOR_STATUS


class STRINGS:
    S_EMPTY = ""
    S_EMPTY_SPACE = " "
    S_SEPERATOR = " : "
    S_UTF8_ENCODING = "utf-8"
    S_ONION_EXTENTION = ".onion"
    S_ISO = "unicode-escape"

class TOR_STRINGS:
    S_SOCKS_HTTP_PROXY = "socks5h://127.0.0.1:"
    S_SOCKS_HTTPS_PROXY = "socks5h://127.0.0.1:"
    S_RELEASE_PORT = 'for /f "tokens=5" %a in (\'netstat -aon ^| find "' + str(TOR_STATUS.S_TOR_CONNECTION_PORT) + '"\') do taskkill /f /pid %a'

class PARSE_STRINGS:
    S_CONTENT_LENGTH_HEADER = 'content-length'

class MANAGE_CRAWLER_MESSAGES:
    S_APPLICATION_STARTING = "[0] ----------------------- APPLICATION STARTING -----------------------"
    S_WEB_REQUEST_PROCESSING_ERROR = "[1] Error Fetching response from server"
    S_FILE_PARSED = "[2] Successfully Parsed File"
    S_URL_PARSED = "[3] Successfully Parsed URL"
    S_PROCESS_FINISHED_FAILURE = "[5] Processing Finished Failure"
    S_PROCESSING_URL = "[6] Processing URL"
    S_PROCESS_FINISHED_SUCCESS = "[7] Processing Finished Success"
    S_LOW_YIELD_URL = "[8] Low Yield URL"
    S_ALREADY_CRAWL_URL = "[8] already crawl URL"
    S_REINITIALIZING_CRAWLABLE_URL = "[9] Re-initializing Crawlable URL"
    S_LOADING_BACKUP_URL = "[10] Loading Backup URL"
    S_BACKUP_QUEUE_EMPTY = "[11] Backup Queue Empty"
    S_BACKUP_PARSED = "[13] Successfully Saved Backup URL"
    S_INSTALLED_URL = "[14] Successfully Installed URL"
    S_UPDATE_URL_STATUS_URL = "[15] Successfully Updated URL status"
    S_RESET_CRAWLABLE_URL = "[16] Successfully Reset Crawlable URL"
    S_LOCAL_DUPLICATE_URL = "[17] Local Duplicate Content URL Error"
    S_INTERNET_ERROR = "[18] Internet not running"
    S_LOCAL_URL_PARSED = "[19] Successfully Parsed Local URL"
    S_LOCAL_URL_EMPTY = "[20] Local URL Document Empty"
    S_UNIQUE_URL_CACHE_LOAD_FAILURE = "[21] Unique URL Duplication Handler Failure"
    S_LIVE_URL_CACHE_LOAD_FAILURE = "[22] Live Feeder Load Failure"
    S_APPLICATION_MAIN_FAILURE = "[23] Main Thread Failure"
    S_FEEDER_DATA_LOADING = "[24] Live Feeder Data Loading"
    S_THREAD_CREATED = "[25] Thread Created"
    S_ELASTIC_ERROR = "[26] Elastic Commands Failed"
    S_SERVER_REQUEST_FAILURE = "[23] Main Thread Failure"

class SPELL_CHECKER_STRINGS:
    S_STOPWORD_LANGUAGE = "english"

class ERROR_MESSAGES:
    S_SINGLETON_EXCEPTION = "This class is a singleton"
    S_DATABASE_FETCH_ERROR = "Database Load Error : Database Empty"
