
DEF INPUT PARAMETER recid-bk-setup AS INT.

FIND FIRST bk-setup WHERE RECID(bk-setup) = recid-bk-setup EXCLUSIVE-LOCK.
DELETE bk-setup.
RELEASE bk-setup.
