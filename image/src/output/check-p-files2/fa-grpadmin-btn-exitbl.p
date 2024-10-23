
DEFINE TEMP-TABLE l-list LIKE fa-grup.

DEF INPUT PARAMETER TABLE FOR l-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-list.
IF case-type = 1 THEN   /* create */
DO:
    create fa-grup.
    RUN fill-new-fa-grup.
END.
ELSE    /* change */
DO:
    FIND FIRST fa-grup WHERE RECID(fa-grup) = rec-id.
    FIND CURRENT fa-grup EXCLUSIVE-LOCK.
    fa-grup.bezeich = l-list.bezeich.
    FIND CURRENT fa-grup NO-LOCK.
END.

PROCEDURE fill-new-fa-grup: 
    fa-grup.gnr = l-list.gnr. 
    fa-grup.bezeich = l-list.bezeich. 
    fa-grup.flag = 0. 
END.

