DEFINE TEMP-TABLE t-list
    FIELD datum AS DATE
    FIELD stat AS CHAR
.

DEFINE INPUT PARAMETER rcode  AS CHAR.
DEFINE INPUT PARAMETER rmtype AS CHAR.
DEFINE INPUT PARAMETER ota    AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.
/*

DEFINE VAR rcode  AS CHAR INIT "dyna".
DEFINE VAR rmtype AS CHAR INIT "hf".
DEFINE VAR ota    AS CHAR INIT "*".*/

DEFINE VARIABLE roomnr     AS INT NO-UNDO.
DEFINE VARIABLE i          AS INT NO-UNDO.
DEFINE VARIABLE end-month  AS INT NO-UNDO.
DEFINE VARIABLE cat-flag   AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE datum      AS DATE.
DEFINE VARIABLE ci-date    AS DATE.
DEFINE VARIABLE to-date AS DATE.
DEFINE VARIABLE prev-day   AS INT.
DEFINE VARIABLE curr-anz   AS INT.
DEFINE VARIABLE otanr      AS INT INIT 0.
DEFINE VARIABLE mm         AS INT.
DEFINE VARIABLE yy         AS INT.

DEFINE BUFFER qbuff FOR queasy.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.

FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN cat-flag = YES.

IF cat-flag THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.char1 = rmtype NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
        roomnr = queasy.number1.
END.
ELSE 
DO:
    FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmtype NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN
        roomnr = zimkateg.zikatnr.
END.

IF ota NE "" AND ota NE "*" THEN
DO:
    FIND FIRST guest WHERE guest.karteityp = 2 AND guest.steuernr NE "" 
        AND TRIM(ENTRY(1,guest.steuernr,"|")) = ota NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN otanr = guest.gastnr.
END.

FIND FIRST queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode
    AND queasy.number1 = roomnr AND queasy.number3 = otanr 
    AND queasy.date1 = ? NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy:
    yy = queasy.number2.
    datum = DATE(01,01,yy) - 1.
    DO i = 1 TO NUM-ENTRIES(queasy.char2,";") - 1:
        datum = datum + 1.
        IF INT(ENTRY(i,queasy.char2,";")) NE 0 THEN
        DO:
            CREATE qbuff.
            ASSIGN
                qbuff.KEY = 174
                qbuff.date1 = datum
                qbuff.number1 = roomnr                
                qbuff.number3 = otanr
                qbuff.char1 = rcode
            .
            IF INT(ENTRY(i,queasy.char2,";")) = 1 THEN
                qbuff.char2 = "1;0;0".
            ELSE IF INT(ENTRY(i,queasy.char2,";")) = 2 THEN
                qbuff.char2 = "0;1;0".
            ELSE IF INT(ENTRY(i,queasy.char2,";")) = 3 THEN
                qbuff.char2 = "0;0;1".
            ELSE IF INT(ENTRY(i,queasy.char2,";")) = 4 THEN
                qbuff.char2 = "0;1;1".
        END.
    END.    
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    DELETE queasy.
    RELEASE queasy. /**/

    FIND NEXT queasy WHERE queasy.KEY = 174 AND queasy.char1 = rcode
        AND queasy.number1 = roomnr AND queasy.number3 = otanr 
        AND queasy.date1 = ? NO-LOCK NO-ERROR.
END.

FOR EACH queasy WHERE queasy.KEY = 174 AND queasy.date1 LT ci-date - 30:
    DELETE queasy.
    RELEASE queasy.
END.


to-date = ci-date + 365.

FOR EACH queasy WHERE queasy.KEY = 174 AND queasy.date1 GE ci-date
    AND queasy.date1 LE to-date AND queasy.char1 = rcode
    AND queasy.number1 = roomnr AND queasy.number3 = otanr NO-LOCK:
    CREATE t-list.
    ASSIGN
        t-list.datum = queasy.date1
        t-list.stat  = queasy.char2.
END.
 






