DEF TEMP-TABLE t-eg-action LIKE eg-action
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE maintask
    FIELD main-nr  AS INTEGER 
    FIELD main-nm AS CHAR FORMAT "x(36)" COLUMN-LABEL "Object".

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER TABLE FOR maintask.
DEF OUTPUT PARAMETER TABLE FOR t-eg-action.

RUN define-group.
RUN define-engineering.

RUN create-main-nr.

FOR EACH eg-action:
    CREATE t-eg-action.
    BUFFER-COPY eg-action TO t-eg-action.
    ASSIGN t-eg-action.rec-id = RECID(eg-action).
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
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Group No for Engineering Modul not yet defined.", lvCAREA, "":U) 
            SKIP 
            translateExtended( "Please contact your next VHP Support for further Information.", lvCAREA, "":U) 
            VIEW-AS ALERT-BOX INFORMATION.*/
    END.
END.

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE create-main-nr:
    DEF BUFFER qbuff FOR queasy.

    FOR EACH maintask:
        DELETE maintask.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 133 NO-LOCK:
        CREATE maintask.
        ASSIGN maintask.main-nr = qbuff.number1
            maintask.main-nm = qbuff.char1.
    END.                                    
END.
  
