
DEFINE TEMP-TABLE sduration
    FIELD Duration-nr  AS INTEGER
    FIELD time-str AS CHAR FORMAT "X(100)".

DEFINE TEMP-TABLE t-eg-Duration LIKE eg-Duration
    FIELD rec-id AS INT.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER TABLE FOR sduration.
DEF OUTPUT PARAMETER TABLE FOR t-eg-Duration.

RUN create-duration.

RUN define-group.
RUN define-engineering.

FOR EACH eg-Duration:
    CREATE t-eg-Duration.
    BUFFER-COPY eg-Duration TO t-eg-Duration.
    ASSIGN t-eg-Duration.rec-id = RECID(eg-Duration).
END.

PROCEDURE create-duration:
    DEF BUFFER qbuff FOR eg-Duration.
    DEF VAR str AS CHAR NO-UNDO.

    FOR EACH sduration:
        DELETE sduration.
    END.

    FOR EACH qbuff NO-LOCK BY qbuff.Duration-nr:
        IF qbuff.days = 0 THEN
        DO:
            str = "".
        END.
        ELSE 
        DO:
            str = string(qbuff.days).
            IF qbuff.days > 1 THEN str = str + " days ".
            ELSE str = str + " day ".
        END.

        IF qbuff.hour = 0 THEN
        DO:
            str = str.
        END.
        ELSE 
        DO:
            str = str + string(qbuff.hour).
            IF qbuff.hour > 1 THEN str = str + " hrs ".
            ELSE str = str + " hr ".
        END.

        IF qbuff.minute = 0 THEN
        DO:
            str = str .
        END.
        ELSE 
        DO:
            str = str + string(qbuff.minute) + " min ".
        END.

        CREATE sduration.
        ASSIGN sduration.duration-nr  = qbuff.duration-nr
               sduration.time-str = str.
    END.
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
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Group No for Engineering Modul not yet defined.", lvCAREA, "":U) 
            SKIP 
            translateExtended( "Please contact your next VHP Support for further Information.", lvCAREA, "":U) 
            VIEW-AS ALERT-BOX INFORMATION. */
    END.
END.
