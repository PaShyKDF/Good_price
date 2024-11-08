class ParserFindTagException(Exception):
    '''Вызывается, когда парсер не может найти тег.'''
    pass


class IncomingDataIsMissingException(Exception):
    '''Вызывается, когда отсутствуют входящие данные'''
    pass
