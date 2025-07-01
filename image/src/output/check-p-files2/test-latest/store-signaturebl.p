
DEF INPUT PARAMETER res-no       AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER resline-no   AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER gast-no      AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER ct           AS CHAR     NO-UNDO.
DEF INPUT PARAMETER update-flag  AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER mobile-no    AS CHAR NO-UNDO.
DEF INPUT PARAMETER email        AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER result-flag AS INTEGER  NO-UNDO INIT 0.

DEF VARIABLE sys-date   AS CHAR     NO-UNDO.
DEF VARIABLE image-data AS CHAR     NO-UNDO.
DEF VARIABLE bb         AS MEMPTR.

IF ct EQ ? OR ct EQ "" THEN
DO:
    result-flag = 1.
    RETURN.
END.

FIND FIRST guest WHERE guest.gastnr = gast-no EXCLUSIVE-LOCK.
IF AVAILABLE guest THEN
DO:
    IF mobile-no NE ? THEN 
    DO: 
      guest.mobil-telefon = mobile-no.
    END.
    ELSE
    DO:
      guest.mobil-telefon = "".
    END.
    IF email NE ? THEN 
    DO: 
      guest.email-adr = email.    
    END.
    ELSE
    DO:
      guest.email-adr = "".
    END.
END.
ELSE
DO:
    result-flag = 1.
    RETURN.
END.
RELEASE guest.

FIND FIRST res-line WHERE res-line.resnr EQ res-no AND res-line.reslinnr = resline-no NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    IF NOT res-line.zimmer-wunsch MATCHES "*mobile-sign-rc*" THEN
    DO:
        res-line.zimmer-wunsch = res-line.zimmer-wunsch + "mobile-sign-rc;".
    END.
    FIND CURRENT res-line NO-LOCK.

    FIND FIRST archieve WHERE archieve.KEY EQ "send-sign-rc" 
        AND archieve.num1 EQ res-no 
        AND archieve.num2 EQ resline-no NO-ERROR. 
    IF AVAILABLE archieve THEN DELETE archieve.

    FIND FIRST archieve WHERE archieve.KEY EQ "send-sign-rc" 
        AND archieve.num1 EQ res-no 
        AND archieve.num2 EQ resline-no 
        AND archieve.num3 EQ gast-no NO-ERROR.
    IF NOT AVAILABLE archieve THEN
    DO:
        sys-date = STRING(MONTH(TODAY), "99") + "/" + STRING(DAY(TODAY), "99") + "/" + STRING(YEAR(TODAY), "9999") + ";" + STRING(TIME) + ";".
        
        /* Oscar (04/03/25) - 457378 - fix loss information when saving signature */
        /* bb = BASE64-DECODE(ct).
        image-data = GET-STRING(bb,1,GET-SIZE(bb)). */
        
        CREATE archieve.
        ASSIGN  
            archieve.KEY     = "send-sign-rc"
            archieve.num1    = res-no
            archieve.num2    = resline-no
            archieve.num3    = gast-no
            archieve.CHAR[1] = ""
            archieve.CHAR[2] = ct
            archieve.CHAR[3] = sys-date
            archieve.CHAR[4] = ""
            archieve.CHAR[5] = ""
            archieve.datum   = res-line.ankunft.
    END.
    ELSE
    DO:
        sys-date = STRING(MONTH(TODAY), "99") + "/" + STRING(DAY(TODAY), "99") + "/" + STRING(YEAR(TODAY), "9999") + ";" + STRING(TIME) + ";".
        
        /* Oscar (04/03/25) - 457378 - fix loss information when saving signature */
        /* bb = BASE64-DECODE(ct).
        image-data = GET-STRING(bb,1,GET-SIZE(bb)). */
    
        ASSIGN  
            archieve.CHAR[1] = ""
            archieve.CHAR[2] = ct
            archieve.CHAR[3] = sys-date
            archieve.CHAR[4] = ""
            archieve.CHAR[5] = ""
            archieve.datum   = res-line.ankunft.
    END.
    FIND CURRENT archieve NO-LOCK.
    RELEASE archieve.
END.


/*masdod ubah konsep
FIND FIRST archieve WHERE archieve.KEY = "send-sign-rc" AND
    archieve.num1 = res-no AND archieve.num2 = resline-no AND
    archieve.num3 = gast-no NO-ERROR.

IF AVAILABLE archieve AND update-flag THEN
DO:
   DELETE archieve. /*IT 210313*/
END.
ELSE IF AVAILABLE archieve AND NOT update-flag THEN
DO:
    result-flag = 1.
    RETURN.
END.
ELSE IF NOT update-flag THEN
DO:
    result-flag = 1.
    RETURN.
END.


FIND FIRST res-line WHERE res-line.resnr = res-no AND
    res-line.reslinnr = resline-no NO-ERROR.

IF NOT res-line.zimmer-wunsch MATCHES "*mobile-sign-rc*" THEN
DO:
    res-line.zimmer-wunsch = res-line.zimmer-wunsch + "mobile-sign-rc;".
END.

FIND CURRENT res-line NO-LOCK.

sys-date = STRING(MONTH(TODAY), "99") + "/" + STRING(DAY(TODAY), "99") 
    + "/" + STRING(YEAR(TODAY), "9999") + ";" + STRING(TIME) + ";".

bb = BASE64-DECODE(ct).
image-data = GET-STRING(bb,1,GET-SIZE(bb)).


CREATE archieve.
ASSIGN  
    archieve.KEY     = "send-sign-rc"
    archieve.num1    = res-no
    archieve.num2    = resline-no
    archieve.num3    = gast-no
    archieve.CHAR[1] = ""
    archieve.CHAR[2] = image-data
    archieve.CHAR[4] = ""
    archieve.CHAR[3] = sys-date
    archieve.datum   = res-line.ankunft
.
FIND CURRENT archieve NO-LOCK.
RELEASE archieve.
*/
