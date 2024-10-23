DEFINE TEMP-TABLE compproduct-list 
    FIELD num       AS INTEGER 
    FIELD nr        AS INTEGER      FORMAT ">>>>" LABEL "No" 
    FIELD bezeich   AS CHARACTER    FORMAT "x(32)" LABEL "COMPANY" 
    FIELD room      AS INTEGER      EXTENT 12 FORMAT "->>,>>9" INITIAL [0,0,0,0,0,0,0,0,0,0,0,0] 
    FIELD ytd       AS INTEGER      FORMAT "->>>,>>9"  LABEL "Total YTD" 
    FIELD lytd      AS INTEGER      FORMAT "->>>,>>9" LABEL "Tot LYTD"
    . 

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER curr-date        AS CHARACTER            NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR compproduct-list.

DEFINE VARIABLE mm              AS INTEGER      NO-UNDO.
DEFINE VARIABLE yy              AS INTEGER      NO-UNDO.
DEFINE VARIABLE i               AS INTEGER      NO-UNDO. 
DEFINE VARIABLE from-date       AS DATE         NO-UNDO.
DEFINE VARIABLE to-date         AS DATE         NO-UNDO.
DEFINE VARIABLE datum           AS DATE         NO-UNDO.
DEFINE BUFFER r-list FOR compproduct-list. 
DEFINE STREAM s1. 

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "comp-product". 

/***************MAIN LOGIC********/
mm = INTEGER(SUBSTR(curr-date,1,2)). 
yy = INTEGER(SUBSTR(curr-date,3,4)). 


FOR EACH r-list: 
    DELETE r-list. 
END. 

FOR EACH guest WHERE guest.karteityp = 1 AND NAME GT "" 
    AND guest.logiernachte > 0 NO-LOCK USE-INDEX typenam_ix, 
    FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
    AND guestseg.reihenfolge = 1 NO-LOCK, 
    FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
    AND segment.betriebsnr = 0 NO-LOCK: 

    CREATE compproduct-list. 
    compproduct-list.bezeich = guest.NAME. 

    DO i = 1 TO mm: 
        from-date = DATE(i, 1, yy).
        to-date = from-date + 32.
        to-date = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1.
        DO datum = from-date TO to-date:
            FIND FIRST guestat1 WHERE guestat1.gastnr = guest.gastnr 
                AND guestat1.datum = datum NO-LOCK NO-ERROR. 
            IF AVAILABLE guestat1 THEN 
            DO: 
                compproduct-list.room[i] = compproduct-list.room[i] + guestat1.zimmeranz. 
                compproduct-list.ytd = compproduct-list.ytd + guestat1.zimmeranz. 
            END.
        END.
    END. 
    
    DO i = 1 TO mm: 
        from-date = DATE(i, 1, (yy - 1)).
        to-date = from-date + 32.
        to-date = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1.
        DO datum = from-date TO to-date:
            FIND FIRST guestat1 WHERE guestat1.gastnr = guest.gastnr 
                AND guestat1.datum = datum NO-LOCK NO-ERROR. 
            IF AVAILABLE guestat1 THEN 
            DO: 
                compproduct-list.lytd = compproduct-list.lytd + guestat1.zimmeranz. 
            END.
        END.
    END. 

END.   

i = 0. 
FOR EACH compproduct-list WHERE compproduct-list.ytd NE 0 
    BY compproduct-list.ytd DESCENDING BY compproduct-list.bezeich: 
    i = i + 1. 
    compproduct-list.nr = i. 
    compproduct-list.num = i. 
END. 

FOR EACH compproduct-list WHERE (compproduct-list.nr = 0): 
    DELETE compproduct-list. 
END. 

CREATE compproduct-list. 
ASSIGN  compproduct-list.num = 9999 
        compproduct-list.bezeich = translateExtended ("T O T A L",lvCAREA,""). 

FOR EACH r-list WHERE r-list.num LT 9999: 
    DO i = 1 TO 12: 
        compproduct-list.room[i] = compproduct-list.room[i] + r-list.room[i]. 
    END.

    compproduct-list.ytd  = compproduct-list.ytd + r-list.ytd.
    compproduct-list.lytd = compproduct-list.lytd + r-list.lytd.
END. 

