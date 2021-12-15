# Local Imports
import re
from abc import ABC
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from native_services.constants.constant import CRAWL_SETTINGS_CONSTANTS
from native_services.constants.strings import GENERIC_STRINGS
from native_services.i_crawl_manager.i_crawl_enums import PARSE_TAGS, PARSE_TAGS_STRINGS
from crawler_services.helper_services.spell_checker_handler import spell_checker_handler
from gensim.parsing.preprocessing import remove_stopwords


# class to parse html raw duplicationHandlerService
class html_parser(HTMLParser, ABC):

    def __init__(self, m_base_url, m_html):
        super().__init__()

        self.m_title = GENERIC_STRINGS.S_EMPTY
        self.m_description = GENERIC_STRINGS.S_EMPTY
        self.m_keywords = GENERIC_STRINGS.S_EMPTY
        self.m_content_type = CRAWL_SETTINGS_CONSTANTS.S_THREAD_CATEGORY_GENERAL

        self.m_base_url = m_base_url
        self.m_html = m_html
        self.m_paragraph_count = 0
        self.rec = PARSE_TAGS.S_NONE
        self.m_total_url = 0

    # --------------- Tag Manager --------------- #

    def handle_starttag(self, p_tag, p_attrs):
        self.rec = PARSE_TAGS.S_NONE

        if p_tag == PARSE_TAGS_STRINGS.S_HREFS_A:
            for name, value in p_attrs:
                if name == PARSE_TAGS_STRINGS.S_HREFS:
                    self.m_total_url += 1

        if p_tag == PARSE_TAGS_STRINGS.S_TITLE:
            self.rec = PARSE_TAGS.S_TITLE

        elif p_tag == PARSE_TAGS_STRINGS.S_HEADER:
            self.rec = PARSE_TAGS.S_HEADER

        elif p_tag == PARSE_TAGS_STRINGS.S_PARAGRAPH:
            self.rec = PARSE_TAGS.S_PARAGRAPH

        elif p_tag == PARSE_TAGS_STRINGS.S_META:
            try:
                if p_attrs[0][1] == PARSE_TAGS_STRINGS.S_META_DESCRIPTION.value:
                    if len(p_attrs) > 1 and len(p_attrs[1]) > 0 and p_attrs[1][0] == PARSE_TAGS_STRINGS.S_META_CONTENT.value and p_attrs[1][1] is not None:
                        self.m_description = p_attrs[1][1]
                elif p_attrs[0][1] == PARSE_TAGS_STRINGS.S_META_KEYWORD.value:
                    if len(p_attrs) > 1 and len(p_attrs[1]) > 0 and p_attrs[1][0] == PARSE_TAGS_STRINGS.S_META_CONTENT.value and p_attrs[1][1] is not None:
                        self.m_keywords = p_attrs[1][1].replace(",", GENERIC_STRINGS.S_SPACE)
            except Exception:
                pass

    def handle_data(self, p_data):
        if self.rec == PARSE_TAGS.S_HEADER:
            self.rec = PARSE_TAGS.S_NONE
            self.m_description = self.m_description + p_data
        if self.rec == PARSE_TAGS.S_TITLE:
            self.rec = PARSE_TAGS.S_NONE
            self.m_title = p_data
        elif self.rec == PARSE_TAGS.S_META and len(self.m_title)>0:
            self.rec = PARSE_TAGS.S_NONE
            self.m_title = p_data
        elif self.rec == PARSE_TAGS.S_PARAGRAPH:
            self.rec = PARSE_TAGS.S_NONE
            self.m_description = self.m_description + p_data
        self.rec = PARSE_TAGS.S_NONE

    # --------------- Text Extraction --------------- #

    def __get_html_text(self):
        m_soup = BeautifulSoup(self.m_html, "html.parser")
        m_text = m_soup.get_text(separator=u' ')

        return m_text

    # --------------- Text Preprocessing --------------- #

    def __strip_special_character(self, p_desc):
        p_desc = re.sub('[^A-Za-z0-9 .@#_+-]+', '', p_desc)
        p_desc = re.sub(' +', ' ', p_desc)
        return p_desc

    def __clean_html(self, p_html):
        m_html = re.sub('\W+', ' ', p_html)
        m_html = m_html.replace('\n', ' ')
        m_html = m_html.replace('\t', ' ')
        m_html = m_html.replace('\r', ' ')
        m_html = re.sub(' +', ' ', m_html)

        return remove_stopwords(m_html)

    # ----------------- Data Recievers -----------------

    # duplicationHandlerService Getters
    def __get_title(self):
        return self.__strip_special_character(self.m_title).strip()

    # extract relavent keywords from html for its representation
    def __get_keyword(self, p_text):

        # New Line and Tab Remover
        p_text = p_text.replace('\\n', ' ')
        p_text = p_text.replace('\\t', ' ')
        p_text = p_text.replace('\\r', ' ')

        # Tokenizer
        word_list = p_text.split()

        # Lower Case
        word_list = [x.lower() for x in word_list]

        # Word Checking
        incorrect_word, correct_word = spell_checker_handler.get_instance().validation_handler(word_list)

        # Cleaning Incorrect Words
        incorrect_word_cleaned = []
        for m_word in incorrect_word:
            incorrect_word_filter, correct_word_filter = spell_checker_handler.get_instance().invalid_validation_handler(m_word)
            if len(correct_word_filter) > 0 and len(correct_word_filter) + 1 >= len(incorrect_word_filter):
                correct_word = correct_word + correct_word_filter
            elif spell_checker_handler.get_instance().incorrect_word_validator(m_word) is True and len(incorrect_word_filter) <= 1:
                incorrect_word_cleaned.append(m_word)

        # Remove Special Character
        word_list = [re.sub('[^a-zA-Z0-9]+', '', _) for _ in incorrect_word_cleaned]
        incorrect_word_cleaned = list(filter(None, word_list))

        correct_word = list(set(correct_word))
        return correct_word, incorrect_word_cleaned

    # extract website description from raw duplicationHandlerService
    def __get_description(self):
        clean_description = self.__strip_special_character(self.m_description)
        return clean_description

    def __get_content_type(self):
        return  self.m_content_type

    def __get_validity_score(self, p_title, p_description, p_keyword):
        if len(p_keyword)>10 and (len(p_title) + len(p_description) > 0) and p_title.lower().__contains__("domain") is False and p_description.lower().__contains__("buy domain") is False and self.m_total_url>10:
            return 1
        else:
            return 0

    def get_parsed_html(self):
        m_cleaned_text = self.__clean_html(self.__get_html_text())

        m_title = self.m_title

        m_description = self.__get_description()
        correct_word, incorrect_word = self.__get_keyword(m_cleaned_text)
        m_validity_score = self.__get_validity_score(m_title, m_description, correct_word)

        return m_title, m_description, correct_word, incorrect_word, m_validity_score
