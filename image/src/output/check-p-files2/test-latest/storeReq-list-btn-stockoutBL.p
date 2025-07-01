
DEF INPUT PARAMETER t-list-s-recid AS INT.
DEF OUTPUT PARAMETER herkunftflag AS INT.

FIND FIRST l-op WHERE RECID(l-op) = t-list-s-recid NO-LOCK.
herkunftflag = l-op.herkunftflag.
