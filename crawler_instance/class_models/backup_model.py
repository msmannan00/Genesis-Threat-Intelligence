# Local Imports
from crawler_instance.constants.constant import CRAWL_SETTINGS_CONSTANTS
from crawler_instance.constants.strings import GENERIC_STRINGS


class backup_model:
    # Local Variables
    m_parsed = False
    m_host = GENERIC_STRINGS.S_SPACE
    m_catagory = CRAWL_SETTINGS_CONSTANTS.S_THREAD_CATEGORY_GENERAL

    # Initializations
    def __init__(self, p_host, p_catagory):
        self.m_parsed = False
        self.m_host = p_host
        self.m_catagory = p_catagory
