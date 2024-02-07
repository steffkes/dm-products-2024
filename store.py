import re


def match_from_url(url):
    m = re.search("/store/(de)-(\\d+)/", url)
    return (m.group(1).upper(), int(m.group(2))) if m else None
