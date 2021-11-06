import eventlet

from CrawlerInstance.constants import constants
from CrawlerInstance.helperServices.helperMethod import helperMethod
from CrawlerInstance.iCrawlController.iCrawlEnums import RESPONSE_CODE
from CrawlerInstance.logManager.logManager import log
from GenesisCrawlerServices.constants import strings


class webRequestManager:

    # Load URL - used to request url for parsing to actually crawl the hidden web
    def load_url(self, p_url):

        m_request_handler = helperMethod.on_create_session()
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

