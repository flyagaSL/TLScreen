'''
:copyright: (c) 2020 by lavrovsergei97
:license: Apache2, see LICENSE for more details.
'''
import logging
import sys

log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
log.addHandler(handler)

handler = logging.FileHandler('info.log', 'w')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
log.addHandler(handler)
