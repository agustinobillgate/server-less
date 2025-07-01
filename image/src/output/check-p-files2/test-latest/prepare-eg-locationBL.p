DEFINE TEMP-TABLE building
    FIELD build-nr  AS INTEGER 
    FIELD char1 AS CHAR FORMAT "x(36)" COLUMN-LABEL "Building".

DEF TEMP-TABLE t-eg-location LIKE eg-location
    FIELD rec-id AS INT.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-eg-location.
DEF OUTPUT PARAMETER TABLE FOR building.

RUN define-group.
RUN define-engineering.

RUN create-build-nr.
FOR EACH eg-location:
    CREATE t-eg-location.
    BUFFER-COPY eg-location TO t-eg-location.
    ASSIGN t-eg-location.rec-id = RECID(eg-location).
END.

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE Define-engineering:
/*
    FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.CHAR3 = "Engineering" NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN EngID = queasy.number1.
    END.
*/
    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    ELSE
    DO:
        ASSIGN EngID = 0.
    END.
END.

PROCEDURE create-build-nr:
    DEF BUFFER qbuff FOR queasy.

    FOR EACH building:
        DELETE building.
    END.
    
    CREATE building.
    ASSIGN building.build-nr = 0
        building.char1 = "".

    FOR EACH qbuff WHERE qbuff.KEY = 135 NO-LOCK:
        CREATE building.
        ASSIGN building.build-nr = qbuff.number1
            building.char1 = qbuff.char1.
    END.                                    
END.
