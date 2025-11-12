
DEF TEMP-TABLE t-pull-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0.

DEF TEMP-TABLE t-push-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0.

DEF TEMP-TABLE t-list
    FIELD autostart     AS LOGICAL
    FIELD period        AS INT
    FIELD delay         AS INT
    FIELD hotelcode     AS CHAR
    FIELD username      AS CHAR
    FIELD password      AS CHAR
    FIELD liveflag      AS LOGICAL
    FIELD defcurr       AS CHAR
    FIELD pushrateflag  AS LOGICAL
    FIELD pullbookflag  AS LOGICAL
    FIELD pushavailflag AS LOGICAL
    FIELD workpath      AS CHAR
    FIELD progavail     AS CHAR.

DEF INPUT  PARAMETER  bookengID AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-pull-list.
DEF OUTPUT PARAMETER TABLE FOR t-push-list.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE i AS INT NO-UNDO.
DEFINE VARIABLE str AS CHAR NO-UNDO.
/* NC 22/05/24 #465B4D */
DEFINE VARIABLE gastnrBE AS INT NO-UNDO INIT 0.
FIND FIRST queasy WHERE queasy.KEY = 159 AND 
    queasy.number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
    gastnrBE = queasy.number2.
/********************************/
FIND FIRST queasy WHERE KEY = 160 AND number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO: 
    CREATE t-list.
    DO i = 1 TO NUM-ENTRIES(queasy.char1,";"):
        str = ENTRY(i, queasy.char1, ";").
        IF SUBSTR(str,1,11)      = "$autostart$" THEN t-list.autostart      = LOGICAL(SUBSTR(str,12)).
        ELSE IF SUBSTR(str,1,8)  = "$period$"    THEN t-list.period         = INT(SUBSTR(str,9)).
        ELSE IF SUBSTR(str,1,7)  = "$delay$"     THEN t-list.delay          = INT(SUBSTR(str,8)).
        ELSE IF SUBSTR(str,1,10) = "$liveflag$"  THEN t-list.liveflag       = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,9)  = "$defcurr$"   THEN t-list.defcurr        = SUBSTR(str,10).
        ELSE IF SUBSTR(str,1,10) = "$workpath$"  THEN t-list.workpath       = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10) = "$progname$"  THEN t-list.progavail      = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,9)  = "$htlcode$"   THEN t-list.hotelcode      = SUBSTR(str,10).
        ELSE IF SUBSTR(str,1,10) = "$username$"  THEN t-list.username       = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10) = "$password$"  THEN t-list.password       = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10) = "$pushrate$"  THEN t-list.pushrateflag   = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,10) = "$pullbook$"  THEN t-list.pullbookflag   = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,11) = "$pushavail$" THEN t-list.pushavailflag  = LOGICAL(SUBSTR(str,12)).        
    END.
END.

/** mapping pull **/
FOR EACH queasy WHERE queasy.KEY = 163 AND queasy.number1 = bookengID NO-LOCK:

    CREATE t-pull-list.
    ASSIGN
        t-pull-list.rcodeVHP    = ENTRY(1, queasy.char1, ";")
        t-pull-list.rcodeBE     = ENTRY(2, queasy.char1, ";")
        t-pull-list.rmtypeVHP   = ENTRY(3, queasy.char1, ";")
        t-pull-list.rmtypeBE    = ENTRY(4, queasy.char1, ";")
        t-pull-list.argtVHP     = ENTRY(5, queasy.char1, ";").
END.

/** mapping push **/
/*NC 22/05/24 #465B4D */
FOR EACH queasy WHERE queasy.KEY = 161 AND queasy.number1 = bookengID NO-LOCK,
	FIRST guest-pr WHERE guest-pr.gastnr = gastnrBE AND guest-pr.CODE EQ ENTRY(1, queasy.char1, ";") NO-LOCK :

    CREATE t-push-list.
    ASSIGN
        t-push-list.rcodeVHP    = ENTRY(1, queasy.char1, ";")
        t-push-list.rcodeBE     = ENTRY(2, queasy.char1, ";")
        t-push-list.rmtypeVHP   = ENTRY(3, queasy.char1, ";")
        t-push-list.rmtypeBE    = ENTRY(4, queasy.char1, ";")
        t-push-list.argtVHP     = ENTRY(5, queasy.char1, ";").
END.

