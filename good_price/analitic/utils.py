from good_price.analitic.exceptions import ParserFindTagException


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        raise ParserFindTagException(error_msg)
    return searched_tag


def clock_to_float(clock):
    clock = float(clock.split(' ')[0])
    if clock > 100:
        clock /= 1000
    return clock


def cores_to_int(cores):
    if cores is not None:
        return int(cores)
    return None


def validate_graphics_core(core):
    if core.startswith('да'):
        return 'да'
    return 'нет'
