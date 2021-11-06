import enum


class ICRAWL_CONTROLLER_COMMANDS(enum.Enum):
    S_START_CRAWLER_INSTANCE = 1
    S_GET_CRAWLED_DATA = 2
    S_INVOKE_THREAD = 3

class PARSE_TAGS(enum.Enum):
    S_TITLE = 1
    S_META = 2
    S_KEYWORD = 3
    S_HEADER = 4
    S_PARAGRAPH = 5
    S_NONE = -1

class RESPONSE_CODE(enum.Enum):
    S_SUCCESS = 200

class PARSE_TAGS_STRINGS(enum.Enum):
    S_HREFS_A = "a"
    S_HREFS = "href"
    S_TITLE = "title"
    S_HEADER = "h1"
    S_PARAGRAPH = "p"
    S_META = "meta"
    S_META_DESCRIPTION = "description"
    S_META_KEYWORD = "keywords"
    S_META_CONTENT = "content"
