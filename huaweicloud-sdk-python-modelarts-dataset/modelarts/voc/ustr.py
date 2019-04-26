import sys

from numpy import unicode

from modelarts.voc.constants import DEFAULT_ENCODING


def ustr(x):
  '''py2/py3 unicode helper'''

  if sys.version_info < (3, 0, 0):
    from PyQt4.QtCore import QString
    if type(x) == str:
      return x.decode(DEFAULT_ENCODING)
    if type(x) == QString:
      return unicode(x.toUtf8(), DEFAULT_ENCODING, 'ignore')
    return x
  else:
    return x
