# Non Parsed URL Model
# Model representing information of url to be put in backup queue
from crawler_instance.constants import constants
from genesis_crawler_services.constants import strings


class queue_url_model:

    # Local Variables
    m_url = strings.S_EMPTY
    m_type = strings.S_EMPTY
    m_depth = constants.S_DEFAULT_DEPTH

    # Initializations
    def __init__(self, p_url, p_depth, p_type):
        self.m_url = p_url
        self.m_depth = p_depth
        self.m_type = p_type
