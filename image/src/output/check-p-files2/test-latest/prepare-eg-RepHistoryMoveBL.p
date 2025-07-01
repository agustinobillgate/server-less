
DEF TEMP-TABLE t-queasy133 LIKE queasy.

DEF INPUT PARAMETER user-init AS CHAR.

DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-queasy133.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
RUN define-group.
RUN define-engineering.

FOR EACH queasy WHERE KEY = 133:
    CREATE t-queasy133.
    BUFFER-COPY queasy TO t-queasy133.
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

