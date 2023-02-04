from parsers.constants.cli import (
    CLI,
    PARSE,
    VERBOSE,
)
from parsers.constants.files import (
    PROJECT_DIR,
    PARSERS,
    USER_PARSERS,
    PARSED_DATA,
    USER_AGENTS,
    SAMPLE,
    NOTES,
    LOG,
    DEBUG_OUT,
    DEBUG_ERR,
    DEBUG_ALL,
    Dir,
    File,
)
from parsers.constants.numbers import (
    DEFAULT_CONNECTION_TIMEOUT,
    DEFAULT_READ_TIMEOUT,
    MagicNumber,
)
from parsers.constants.prompt import (
    ENTER_BS4_PARSER,
    ENTER_URL_OR_FALSE,
    Prompt,
)
from parsers.constants.scrap import (
    BUILTIN,
    FASTEST,
    HTML_PARSER,
    HTML5LIB,
    LXML,
    MarkupParser,
    Scrap
)
from parsers.constants.urls import (
    HTTPBIN_ORG,
    CHECK_PROXY_URL,
    CHECK_PROXY_URL_PARAMS,
    URL,
)


class ConstStorage:
    from parsers.datatypes import classproperty

    @classproperty
    def CLI(cls): return CLI()  # noqa: E704

    @classproperty
    def DIR(cls): return Dir()  # noqa: E704

    @classproperty
    def FILE(cls): return File()  # noqa: E704

    @classproperty
    def URL(cls): return URL()  # noqa: E704

    @classproperty
    def PARSE(cls): return Scrap()  # noqa: E704,F811

    @classproperty
    def PROMPT(cls): return Prompt()  # noqa: E704

    @classproperty
    def MAGIC_NUMBERS(cls): return MagicNumber()  # noqa: E704

    @classproperty
    def TIMEOUTS(cls) -> tuple[float, float]:
        default_connection, default_read = ConstStorage.MAGIC_NUMBERS
        return default_connection, default_read


class Constant(ConstStorage):

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'({", ".join(ns for ns in dir(Constant) if ns.isupper())})'
        )
