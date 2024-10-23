DEFINE TEMP-TABLE t-list NO-UNDO
    FIELD progavail      AS CHARACTER
    FIELD hotelcode      AS CHARACTER
    FIELD pushrate-flag  AS LOGICAL
    FIELD pushavail-flag AS LOGICAL
    FIELD period        AS INTEGER.

DEF TEMP-TABLE t-push-list NO-UNDO
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0
    FIELD license       AS INTEGER.

DEFINE TEMP-TABLE rmtype-list
    FIELD bezeich AS CHAR.

DEFINE INPUT PARAMETER beCode       AS INTEGER.
DEFINE OUTPUT PARAMETER from-date   AS DATE.
DEFINE OUTPUT PARAMETER to-date     AS DATE.
DEFINE OUTPUT PARAMETER maxdate     AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-push-list.
DEFINE OUTPUT PARAMETER TABLE FOR rmtype-list.


DEFINE VARIABLE i   AS INTEGER NO-UNDO.
DEFINE VARIABLE str AS CHARACTER NO-UNDO.

FIND FIRST queasy WHERE KEY = 160 AND number1 = beCode NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO :
    CREATE t-list.
    DO i = 1 TO NUM-ENTRIES(queasy.char1, ";").
        str = ENTRY(i, queasy.char1, ";").
        IF SUBSTR(str,1,10)      = "$progname$"  THEN t-list.progavail        = SUBSTR(str, 11).
        ELSE IF SUBSTR(str,1,9)  = "$htlcode$"   THEN t-list.hotelcode        = SUBSTR(str,10).
        ELSE IF SUBSTR(str,1,10) = "$pushrate$"  THEN t-list.pushrate-flag    = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,11) = "$pushavail$" THEN t-list.pushavail-flag   = LOGICAL(SUBSTR(str,12)).
		ELSE IF SUBSTR(str,1,8)  = "$period$"    THEN t-list.period         = INT(SUBSTR(str,9)).
    END.
END.

FOR EACH queasy WHERE queasy.KEY = 161 AND queasy.number1 = beCode NO-LOCK:

    CREATE t-push-list.
    ASSIGN
        t-push-list.rcodeVHP    = ENTRY(1, queasy.char1, ";")
        t-push-list.rcodeBE     = ENTRY(2, queasy.char1, ";")
        t-push-list.rmtypeVHP   = ENTRY(3, queasy.char1, ";")
        t-push-list.rmtypeBE    = ENTRY(4, queasy.char1, ";")
        t-push-list.argtVHP     = ENTRY(5, queasy.char1, ";").
END.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
ASSIGN from-date = htparam.fdate.

FIND FIRST t-push-list NO-LOCK NO-ERROR.
IF AVAILABLE t-push-list THEN
DO:
    CREATE rmtype-list.
    rmtype-list.bezeich = "*".

    FOR EACH t-push-list:
        FIND FIRST rmtype-list WHERE rmtype-list.bezeich EQ t-push-list.rmtypeVHP NO-LOCK NO-ERROR.
        IF NOT AVAILABLE rmtype-list THEN
        DO:
            CREATE rmtype-list.
            rmtype-list.bezeich = t-push-list.rmtypeVHP.
        END.
    END.
END.

FIND FIRST t-list NO-ERROR.
IF AVAILABLE t-list THEN
DO:
    IF t-list.period LT 90 THEN t-list.period = 90.
    ASSIGN
        to-date = from-date + t-list.period
        maxdate = to-date.    
END.
