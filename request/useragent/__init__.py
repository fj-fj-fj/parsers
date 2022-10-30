"""This package contains user-agent tools"""

__all__ = 'gen_user_agents',

from typing import Generator

from request.useragent.constants import const


def gen_user_agents(file=const.USER_AGENTS_FILE) -> Generator[str, None, None]:
    with open(file) as user_agent_file:
        return (ua for ua in user_agent_file.readlines())
