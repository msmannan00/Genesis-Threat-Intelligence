# Non Parsed URL Model
# Model representing information of url to be put in backup queue
from CrawlerInstance.constants import constants
from GenesisCrawlerServices.constants import strings


class queueURLModel:

    # Local Variables
    m_url = strings.S_EMPTY
    m_type = strings.S_EMPTY
    m_depth = constants.S_DEFAULT_DEPTH

    # Initializations
    def __init__(self, p_url, p_depth, p_type):
        self.m_url = p_url
        self.m_depth = p_depth
        self.m_type = p_type

    # Getter Setters
    def getURL(self):
        return self.m_url
