# ------- Allowed Files --------- #

S_DOC_TYPES = [".pdf", ".msword", ".document", ".docx", "doc"]

# ------- Local Paths --------- #

# OS Directory
S_PROJECT_PATH = "C:\\Workspace\\Genesis Website Classifier"
S_DATASET_PATH = "\\GenesisCrawlerServices\\raw\\crawled_classifier_websites.csv"

# Local Directory
S_RAW_PATH = S_PROJECT_PATH + "\\"
S_QUEUE_STATE_PATH = S_PROJECT_PATH + "\\CrawlerInstance\\stateManager\\queues_state"
S_DICTIONARY_PATH = S_PROJECT_PATH + "\\GenesisCrawlerServices\\raw\\dictionary"
S_DICTIONARY_MINI_PATH = S_PROJECT_PATH + "\\GenesisCrawlerServices\\raw\\dictionary_small"

# Local URL
S_START_URL = "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address/"

# ------- Crawler Settings --------- #

# Total Thread Instances Allowed
S_MAX_THREAD_COUNT_PER_INSTANCE = 30

# Time Delay to Invoke New Url Requests
S_ICRAWL_INVOKE_DELAY = 2
S_CRAWLER_INVOKE_DELAY = 2

# Max Allowed Depth
S_MAX_ALLOWED_DEPTH = 1
S_DEFAULT_DEPTH = 0

# Max Allowed Images
S_MAX_ALLOWED_SUB_FILE = 10

# Max Allowed Redirects
S_MAX_ALLOWED_REDIRECT = 5

# Max URL Timeout
S_URL_TIMEOUT = 70
S_HEADER_TIMEOUT = 30

# Max Host Queue Size
S_MAX_HOST_QUEUE_SIZE = 100
S_MAX_SUBHOST_QUEUE_SIZE = 100

# Max URL Size
S_MAX_URL_SIZE = 480

# Backup Time
S_BACKUP_TIME_DELAY = 86400
S_BACKUP_FETCH_LIMIT = 50

# mongoDB Database
S_DATABASE_NAME = 'web_classifier'
S_DATABASE_PORT = 27017
S_DATABASE_IP = 'localhost'

# Min Image Content Size
S_MIN_CONTENT_LENGTH = 50000

# Static Parser
S_STATIC_PARSER_LIST_MAX_SIZE = 5

# User Agent
S_SOCKS_HTTPS_PROXY = "socks5h://127.0.0.1:"
S_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'

# Crawl Catagory
S_THREAD_CATEGORY_GENERAL = "General"
