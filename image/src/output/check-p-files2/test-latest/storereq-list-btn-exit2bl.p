
DEF INPUT PARAMETER t-list-s-recid AS INT.
DEF INPUT PARAMETER fLager AS INT.
DEF INPUT PARAMETER tLager AS INT.

FIND FIRST l-op WHERE RECID(l-op) = t-list-s-recid EXCLUSIVE-LOCK.
ASSIGN l-op.lager-nr = fLager
     l-op.pos      = tLager.
FIND CURRENT l-op NO-LOCK.
