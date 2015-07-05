# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/5 18:52.
__author__ = 'mcxiaoke'

import logging

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
logger = logging.getLogger('tcpserver')
logger.setLevel(logging.DEBUG)
logger.debug('Protocol problem: %s', 'connection reset', extra=d)
logger.info('Protocol problem: %s', 'connection reset', extra=d)
logger.warning('Protocol problem: %s', 'connection reset', extra=d)
logger.error('Protocol problem: %s', 'connection reset', extra=d)
logger.critical('Protocol problem: %s', 'connection reset', extra=d)
