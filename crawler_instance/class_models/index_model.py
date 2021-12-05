# Local Imports
import re
from crawler_instance.constants import strings, constants


class index_model:

    # Local Variables
    m_title = strings.S_EMPTY
    m_description = strings.S_EMPTY
    m_url = strings.S_EMPTY
    m_content_type = constants.S_THREAD_CATEGORY_GENERAL
    m_validity_score = 0

    m_keyword = []
    m_sub_url = []

    # Initializations
    def __init__(self, p_title=None, p_description=strings.S_EMPTY, p_url=None, p_content_type=None, p_keyword=[], p_validity_score=None):
        self.m_title = p_title
        self.m_description = re.sub(' +', strings.S_SPACE, p_description)
        self.m_url = p_url
        self.m_keyword = p_keyword
        self.m_content_type = p_content_type
        self.m_validity_score = p_validity_score

