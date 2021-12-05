import eventlet

from crawler_instance.constants import constants
from crawler_instance.helper_method.helper_method import helper_method
from crawler_instance.i_crawl_controller.i_crawl_enums import RESPONSE_CODE
from crawler_instance.log_manager.log_manager import log
from genesis_crawler_services.constants import strings


class web_request_manager:

    # Load URL - used to request url for parsing to actually crawl the hidden web
    def load_url(self, p_url):

        m_request_handler = helper_method.on_create_session()
        try:
            with eventlet.Timeout(1):
                page = m_request_handler.get(p_url, timeout=constants.S_URL_TIMEOUT, allow_redirects=True, )
                m_html = page.content.decode(strings.S_ISO)

            if page.status_code != RESPONSE_CODE.S_SUCCESS.value or page.content == strings.S_EMPTY:
                return p_url, False, None
            else:
                return page.url, True, m_html

        except Exception as e:
            log.g().i(strings.S_URL_PROCESSING_ERROR + " : " + p_url + " : " + str(e))
            return p_url, False, None

