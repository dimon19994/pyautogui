import os

from environs import Env

env = Env()

_override_env = os.environ.get("APP_OVERRIDE_ENV", "true")

if _override_env == "true":
    _override_env = True
elif _override_env == "false":
    _override_env = False
else:
    _override_env = True


env.read_env(override=_override_env)


with env.prefixed("APP_"):
    CONFIG = dict(
        find_url=env.str("FIND_URL"),
        important_site_scrolling_from=env.int("IMPORTANT_SITES_SCROLLING_FROM") or 300,
        important_site_scrolling_to=env.int("IMPORTANT_SITES_SCROLLING_TO") or 600,
        key_words=env.str("KEY_WORDS"),
        search_limit=env.int("SEARCH_LIMIT") or 50,
        unimportant_site_count_from=env.int("UNIMPORTANT_SITES_COUNT_FROM") or 4,
        unimportant_site_count_to=env.int("UNIMPORTANT_SITES_COUNT_TO") or 6,
        unimportant_site_scrolling_from=env.int("UNIMPORTANT_SITES_SCROLLING_FROM") or 5,
        unimportant_site_scrolling_to=env.int("UNIMPORTANT_SITES_SCROLLING_TO") or 15,
    )

