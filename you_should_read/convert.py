# TODO: bidict
import logging


logger = logging.getLogger(__name__)


def length_from_display(display):
    if display == 'Short':
        return 1
    elif display == 'Medium':
        return 2
    elif display == 'Long':
        return 3
    elif display == 'Epic':
        return 4
    else:
        logger.error('length_from_display: received invalid display %s',
                     display)
        return -1


def length_to_display(length):
    if length == 1:
        return 'Short'
    elif length == 2:
        return 'Medium'
    elif length == 3:
        return 'Long'
    elif length == 4:
        return 'Epic'
    else:
        logger.error('length_to_display: received invalid length %s', length)
        return 'ERROR'


def status_from_display(display):
    if display == 'Unread':
        return 0
    elif display == 'Ongoing':
        return 1
    elif display == 'Complete':
        return 2
    elif display == 'Abandoned':
        return 3
    else:
        logger.error('status_from_display: received invalid display %s',
                     display)
        return -1


def status_to_display(status):
    if status == 0:
        return 'Unread'
    elif status == 1:
        return 'Ongoing'
    elif status == 2:
        return 'Complete'
    elif status == 3:
        return 'Abandoned'
    else:
        logger.error('status_to_display: received invalid status %s', status)
        return 'ERROR'
