# Local Imports
import re

from native_services.constants.constant import CRAWL_SETTINGS_CONSTANTS
from native_services.constants.strings import GENERIC_STRINGS


class index_model:

    # Local Variables
    m_title = GENERIC_STRINGS.S_EMPTY
    m_description = GENERIC_STRINGS.S_EMPTY
    m_url = GENERIC_STRINGS.S_EMPTY
    m_content_type = CRAWL_SETTINGS_CONSTANTS.S_THREAD_CATEGORY_GENERAL
    m_validity_score = 0
    m_keyword = []

    # Initializations
    def __init__(self, p_title=None, p_description=GENERIC_STRINGS.S_EMPTY, p_url=None, p_content_type=None, p_keyword=[], p_validity_score=None):
        self.m_title = p_title
        self.m_description = re.sub(' +', GENERIC_STRINGS.S_SPACE, p_description)
        self.m_url = p_url
        self.m_keyword = p_keyword
        self.m_content_type = p_content_type
        self.m_validity_score = p_validity_score
