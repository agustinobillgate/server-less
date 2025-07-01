
DEF INPUT PARAMETER res-no       AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER resline-no   AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER guest-number AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER sign-data    AS LONGCHAR NO-UNDO.
DEF OUTPUT PARAMETER mess-result AS CHAR NO-UNDO.

IF res-no EQ ? THEN res-no = 0.
IF resline-no EQ ? THEN resline-no = 0.
IF guest-number EQ ? THEN guest-number = 0.
IF sign-data EQ ? THEN sign-data = "".

IF res-no EQ 0 THEN
DO:
    mess-result = "2-Reservation Number Can't be Null!".
    RETURN.
END.
IF resline-no EQ 0 THEN
DO:
    mess-result = "3-Reservation Line Number Can't be Null!".
    RETURN.
END.
IF guest-number EQ 0 THEN
DO:
    mess-result = "4-Guest Number Can't be Null!".
    RETURN.
END.
IF sign-data EQ "" THEN
DO:
    mess-result = "5-Signature Data Can't be Null!".
    RETURN.
END.

DEF VARIABLE sys-date   AS CHAR NO-UNDO.
DEF VARIABLE image-data AS CHAR NO-UNDO.
DEF VARIABLE bb         AS MEMPTR.


FIND FIRST archieve WHERE archieve.KEY EQ "send-sign-rc" 
    AND archieve.num1 EQ res-no 
    AND archieve.num2 EQ resline-no 
    AND archieve.num3 EQ guest-number NO-ERROR.
IF AVAILABLE archieve THEN
DO:
   DELETE archieve. 
END.

FIND FIRST res-line WHERE res-line.resnr EQ res-no AND res-line.reslinnr EQ resline-no EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    IF NOT res-line.zimmer-wunsch MATCHES "*mobile-sign-rc*" THEN
    DO:
        res-line.zimmer-wunsch = res-line.zimmer-wunsch + "mobile-sign-rc;".
    END.
    FIND CURRENT res-line NO-LOCK.
    
    sys-date = STRING(MONTH(TODAY), "99") + "/" + STRING(DAY(TODAY), "99") 
        + "/" + STRING(YEAR(TODAY), "9999") + ";" + STRING(TIME) + ";".
    
    bb = BASE64-DECODE(sign-data).
    image-data = GET-STRING(bb,1,GET-SIZE(bb)).
    
    
    CREATE archieve.
    ASSIGN  
        archieve.KEY     = "send-sign-rc"
        archieve.num1    = res-no
        archieve.num2    = resline-no
        archieve.num3    = guest-number
        archieve.CHAR[1] = ""
        archieve.CHAR[2] = image-data
        archieve.CHAR[4] = ""
        archieve.CHAR[3] = sys-date
        archieve.datum   = res-line.ankunft
    .
    FIND CURRENT archieve NO-LOCK.
    RELEASE archieve.
    mess-result = "0-Save Signature Success".
END.
ELSE
DO:
    mess-result = "1-No REservation found!".
    RETURN.
END.

