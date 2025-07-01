
DEF TEMP-TABLE t-eg-vendor LIKE eg-vendor
    FIELD rec-id AS INT.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-eg-vendor.

RUN define-group.
RUN define-engineering.

FOR EACH eg-vendor:
    CREATE t-eg-vendor.
    BUFFER-COPY eg-vendor TO t-eg-vendor.
    ASSIGN t-eg-vendor.rec-id = RECID(eg-vendor).
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


