DEFINE TEMP-TABLE TypeRes
    FIELD TYPE  AS INTEGER 
    FIELD fldRes AS CHAR FORMAT "x(36)" COLUMN-LABEL "Resources Type".

DEF TEMP-TABLE t-eg-resources LIKE eg-resources
    FIELD rec-id AS INT.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-eg-resources.

RUN define-group.
RUN define-engineering.

RUN create-type.

FOR EACH eg-resources:
    CREATE t-eg-resources.
    BUFFER-COPY eg-resources TO t-eg-resources.
    ASSIGN t-eg-resources.rec-id = RECID(eg-resources).
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

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE create-type:
    DEF BUFFER qbuff FOR queasy.

    FOR EACH typeres:
        DELETE typeres.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 136 NO-LOCK:
        CREATE typeres.
        ASSIGN typeres.TYPE = qbuff.number1
            typeres.fldres = qbuff.char1.
    END.                                    
END.

