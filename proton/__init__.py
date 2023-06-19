from . import _pysrp, _ctsrp

_mod = None

try:
    _mod = _ctsrp
except (ImportError, OSError):
    pass

if not _mod:
    _mod = _pysrp

User = _mod.User
