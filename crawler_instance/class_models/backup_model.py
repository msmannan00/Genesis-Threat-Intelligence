# Local Imports
from crawler_instance.constants import constants, strings


class backup_model:
    # Local Variables
    m_parsed = False
    m_host = strings.S_SPACE
    m_catagory = constants.S_THREAD_CATEGORY_GENERAL

    # Initializations
    def __init__(self, p_host, p_catagory):
        self.m_parsed = False
        self.m_host = p_host
        self.m_catagory = p_catagory
