#!/usr/bin/env python
import logging

from you_should_read import ysr


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - '
                           '%(message)s')

log = logging.getLogger('requests')
log.setLevel(logging.WARNING)

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)


if __name__ == '__main__':
    ysr.app.run(host='0.0.0.0', debug=True)
