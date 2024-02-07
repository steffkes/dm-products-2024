import re


def match_from_url(url):
    m = re.search("-p(\\d+).", url)
    return ("DE", int(m.group(1))) if m else None
