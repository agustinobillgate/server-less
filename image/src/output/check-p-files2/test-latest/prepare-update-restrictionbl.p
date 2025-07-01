DEFINE TEMP-TABLE room-list
    FIELD bezeich AS CHAR.

DEFINE TEMP-TABLE ota-list
    FIELD bezeich AS CHAR.

DEFINE TEMP-TABLE rcode-list
    FIELD bezeich AS CHAR.

DEFINE OUTPUT PARAMETER ci-date AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.
DEFINE OUTPUT PARAMETER TABLE FOR ota-list.
DEFINE OUTPUT PARAMETER TABLE FOR rcode-list.

/*DEFINE VAR ci-date AS DATE.*/

DEFINE VARIABLE cat-flag AS LOGICAL INIT NO NO-UNDO.
DEFINE BUFFER qsy FOR queasy.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ci-date = htparam.fdate.

FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN cat-flag = YES.

IF cat-flag THEN
DO:
    FOR EACH queasy WHERE queasy.KEY = 152 NO-LOCK:
        FIND FIRST room-list WHERE room-list.bezeich = queasy.char1 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE room-list THEN
        DO:
            CREATE room-list.
            ASSIGN
                room-list.bezeich = queasy.char1.
        END.
    END.
END.
ELSE 
DO:
    FOR EACH zimkateg NO-LOCK:
        FIND FIRST room-list WHERE room-list.bezeich = zimkateg.kurzbez NO-LOCK NO-ERROR.
        IF NOT AVAILABLE room-list THEN
        DO:
            CREATE room-list.
            ASSIGN
                room-list.bezeich = zimkateg.kurzbez.
        END.
    END.
END.

FOR EACH queasy WHERE queasy.KEY = 159 NO-LOCK:
    FOR EACH guest-pr WHERE guest-pr.gastnr = queasy.number2 NO-LOCK:
        FIND FIRST qsy WHERE qsy.KEY = 2 AND qsy.char1 = guest-pr.CODE NO-LOCK NO-ERROR.
        IF AVAILABLE qsy THEN
        DO:
            FIND FIRST rcode-list WHERE rcode-list.bezeich = qsy.char1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rcode-list THEN
            DO:
                CREATE rcode-list.
                ASSIGN
                    rcode-list.bezeich = qsy.char1 .
            END.  
        END.
    END.
END.

FOR EACH guest WHERE guest.karteityp = 2 AND guest.steuernr NE "" NO-LOCK:
    FIND FIRST ota-list WHERE ota-list.bezeich = TRIM(ENTRY(1,guest.steuernr,"|")) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE ota-list THEN
    DO:
        CREATE ota-list.
        ASSIGN
            ota-list.bezeich = TRIM(ENTRY(1,guest.steuernr,"|")) .
    END. 
END.
