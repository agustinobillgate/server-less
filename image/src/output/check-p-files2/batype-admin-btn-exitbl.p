
DEF TEMP-TABLE ba-list LIKE ba-typ. 

DEF INPUT PARAMETER iCase  AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER TABLE FOR ba-list.

FIND FIRST ba-list.

IF iCase = 1 THEN
DO:
    create ba-typ. 
    RUN fill-new-ba-typ.
END.
ELSE
DO:
    FIND FIRST ba-typ WHERE RECID(ba-typ) = rec-id EXCLUSIVE-LOCK.
    ba-typ.bezeich = ba-list.bezeich.
    FIND CURRENT ba-typ NO-LOCK. 
END.

PROCEDURE fill-new-ba-typ: 
    ba-typ.typ-id = ba-list.typ-id. 
    ba-typ.bezeich = ba-list.bezeich. 
END. 
