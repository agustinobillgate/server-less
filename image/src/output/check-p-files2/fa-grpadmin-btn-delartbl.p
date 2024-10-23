
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER do-it AS LOGICAL INIT YES.

FIND FIRST fa-grup WHERE RECID(fa-grup) = rec-id NO-LOCK.
FIND FIRST fa-artikel WHERE fa-artikel.subgrp = fa-grup.gnr NO-LOCK NO-ERROR. 
IF AVAILABLE fa-artikel THEN 
DO: 
  do-it = NO.
END.
ELSE
DO:
    FIND CURRENT fa-grup EXCLUSIVE-LOCK.
    delete fa-grup.
    RELEASE fa-grup.
END.
