
DEFINE TEMP-TABLE l-list LIKE fa-kateg.

DEF INPUT PARAMETER TABLE FOR l-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST l-list.
IF case-type = 1 THEN   /* add */
DO:
    create fa-kateg. 
    RUN fill-new-fa-kateg. 
END.
ELSE    /* chg */
DO:
    FIND FIRST fa-kateg WHERE RECID(fa-kateg) = rec-id.
    FIND CURRENT fa-kateg EXCLUSIVE-LOCK.
    fa-kateg.bezeich = l-list.bezeich.
    fa-kateg.nutzjahr = l-list.nutzjahr.
    fa-kateg.rate = l-list.rate.
    FIND CURRENT fa-kateg NO-LOCK. 
END.

PROCEDURE fill-new-fa-kateg:
    fa-kateg.katnr = l-list.katnr. 
    fa-kateg.bezeich = l-list.bezeich. 
    fa-kateg.nutzjahr = l-list.nutzjahr. 
    fa-kateg.rate = l-list.rate. 
END. 

