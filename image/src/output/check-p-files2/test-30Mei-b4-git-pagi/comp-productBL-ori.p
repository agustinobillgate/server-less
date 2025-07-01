DEFINE TEMP-TABLE compproduct-list 
    FIELD num       AS INTEGER 
    FIELD nr        AS INTEGER      FORMAT ">>>>" LABEL "No" 
    FIELD bezeich   AS CHARACTER    FORMAT "x(32)" LABEL "COMPANY" 
    FIELD room      AS INTEGER      EXTENT 12 FORMAT "->>,>>9" INITIAL [0,0,0,0,0,0,0,0,0,0,0,0] 
    FIELD ytd       AS INTEGER      FORMAT "->>>,>>9"  LABEL "Total YTD" 
    FIELD lytd      AS INTEGER      FORMAT "->>>,>>9" LABEL "Tot LYTD"
    . 

DEFINE TEMP-TABLE c-list LIKE compproduct-list
    FIELD gastnr    AS INTEGER.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER curr-date        AS CHARACTER            NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR compproduct-list.

DEFINE VARIABLE mm              AS INTEGER      NO-UNDO.
DEFINE VARIABLE yy              AS INTEGER      NO-UNDO.
DEFINE VARIABLE i               AS INTEGER      NO-UNDO. 
DEFINE VARIABLE from-date       AS DATE         NO-UNDO.
DEFINE VARIABLE to-date         AS DATE         NO-UNDO.
DEFINE VARIABLE datum           AS DATE         NO-UNDO.
DEFINE VARIABLE jml           AS INT         NO-UNDO. /* Malik Serverless */

DEFINE BUFFER r-list FOR compproduct-list. 
DEFINE STREAM s1. 

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "comp-product". 

/***************MAIN LOGIC********/
DEFINE VARIABLE curr-guest AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-name AS CHAR NO-UNDO.
DEFINE VARIABLE do-it AS LOGICAL NO-UNDO.
DEFINE VARIABLE created AS LOGICAL NO-UNDO.
DEFINE VARIABLE counter AS INTEGER NO-UNDO.
DEFINE VARIABLE troom   AS INTEGER EXTENT 12 NO-UNDO.
DEFINE VARIABLE tytd    AS INTEGER NO-UNDO.
DEFINE VARIABLE tlytd   AS INTEGER NO-UNDO.
DEFINE VARIABLE lfdate  AS DATE NO-UNDO.
DEFINE VARIABLE ltdate  AS DATE NO-UNDO.

mm = INTEGER(SUBSTR(curr-date,1,2)). 
yy = INTEGER(SUBSTR(curr-date,3,4)). 
jml = yy - 1.


FOR EACH r-list: 
    DELETE r-list. 
END. 

from-date = DATE(1,1,yy).
IF mm = 12 THEN
    to-date = DATE(1,1,yy + 1) - 1.
ELSE to-date = DATE(mm + 1, 1, yy) - 1.

lfdate = DATE(1,1,jml).
IF mm = 12 THEN
    ltdate = DATE(1,1,yy) - 1.
ELSE ltdate = DATE(mm + 1, 1, jml) - 1.

FOR EACH guest WHERE guest.karteityp = 1 NO-LOCK USE-INDEX typenam_ix: 

    CREATE compproduct-list. 
    compproduct-list.bezeich = guest.NAME. 

    DO i = 1 TO mm: 
        from-date = DATE(i, 1, yy).
        IF i EQ 12 THEN
            to-date = DATE(1, 1, yy + 1) - 1.
        ELSE
            to-date = DATE(i + 1, 1, yy) - 1.

        /* Oscar - modify looping to use looping by FOR EACH */
        /* DO datum = from-date TO to-date:
            FIND FIRST guestat1 WHERE guestat1.gastnr = guest.gastnr 
                AND guestat1.datum = datum NO-LOCK NO-ERROR. 
            IF AVAILABLE guestat1 THEN 
            DO: 
                compproduct-list.room[i] = compproduct-list.room[i] + guestat1.zimmeranz. 
                compproduct-list.ytd = compproduct-list.ytd + guestat1.zimmeranz. 
            END.
        END. */

        FOR EACH guestat1 WHERE guestat1.gastnr EQ guest.gastnr
            AND guestat1.datum GE from-date
            AND guestat1.datum LE to-date NO-LOCK:
                compproduct-list.room[i] = compproduct-list.room[i] + guestat1.zimmeranz. 
                compproduct-list.ytd = compproduct-list.ytd + guestat1.zimmeranz.
        END.
    END.    

    
    DO i = 1 TO mm: 
        from-date = DATE(i, 1, jml).
        IF i EQ 12 THEN
            to-date = DATE(1, 1, jml + 1) - 1.
        ELSE
            to-date = DATE(i + 1, 1, jml) - 1.

        /* Oscar - modify looping to use looping by FOR EACH*/
        /* DO datum = from-date TO to-date:
            FIND FIRST guestat1 WHERE guestat1.gastnr = guest.gastnr 
                AND guestat1.datum = datum NO-LOCK NO-ERROR. 
            IF AVAILABLE guestat1 THEN 
            DO: 
                compproduct-list.lytd = compproduct-list.lytd + guestat1.zimmeranz. 
            END.
        END. */

        FOR EACH guestat1 WHERE guestat1.gastnr EQ guest.gastnr
            AND guestat1.datum GE from-date
            AND guestat1.datum LE to-date NO-LOCK:
                compproduct-list.lytd = compproduct-list.lytd + guestat1.zimmeranz. 
        END.
    END.    

END.   

i = 0. 
/* Oscar - add condition to check if lytd not 0 */
FOR EACH compproduct-list WHERE compproduct-list.ytd NE 0
    OR compproduct-list.lytd NE 0
    BY compproduct-list.ytd DESCENDING 
    BY compproduct-list.bezeich: 
        i = i + 1. 
        compproduct-list.nr = i. 
        compproduct-list.num = i. 
END. 

FOR EACH compproduct-list WHERE (compproduct-list.nr = 0): 
    DELETE compproduct-list. 
END. 


    
       . 

FOR EACH r-list WHERE r-list.num LT 9999: 
    DO i = 1 TO 12: 
        compproduct-list.room[i] = compproduct-list.room[i] + r-list.room[i]. 
    END.

    compproduct-list.ytd  = compproduct-list.ytd + r-list.ytd.
    compproduct-list.lytd = compproduct-list.lytd + r-list.lytd.
END. 

