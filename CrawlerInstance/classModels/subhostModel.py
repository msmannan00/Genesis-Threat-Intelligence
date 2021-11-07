# Local Imports
class subHostModel:

    # Local Variables
    __m_sub_host = False
    __m_depth = None

    # Initializations
    def __init__(self, p_sub_host, p_depth):
        self.__m_sub_host = p_sub_host
        self.__m_depth = p_depth

    def get_sub_host(self):
        return self.__m_sub_host

    def m_depth(self):
        return self.__m_depth