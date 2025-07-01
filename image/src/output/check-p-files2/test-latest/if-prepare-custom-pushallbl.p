/*
    Program       : if-prepare-custom-pushallBL.p
    Author        : Fadly
    Created       : 05/09/19
    last update   :
    Purpose       : For push all method on interfacing
                    with parameter from date and to date.
*/

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

DEFINE INPUT PARAMETER beCode AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-push-list.
DEFINE OUTPUT PARAMETER date-110 AS DATE.

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
ASSIGN date-110 = htparam.fdate.