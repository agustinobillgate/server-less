
DEFINE TEMP-TABLE top50-list 
    FIELD num       AS INTEGER 
    FIELD nr        AS INTEGER FORMAT ">>>"         LABEL "No" 
    FIELD bezeich   AS CHAR FORMAT "x(32)"          LABEL "AGENTS" 
    FIELD room      AS INTEGER EXTENT 12 FORMAT "->>,>>9" 
                        INITIAL [0,0,0,0,0,0,0,0,0,0,0,0] 
    FIELD ytd       AS INTEGER  FORMAT "->>>,>>9"   LABEL "Total YTD" 
    FIELD lytd      AS INTEGER  FORMAT "->>>,>>9"   LABEL "Tot LYTD"
    FIELD mtd       AS INTEGER
    FIELD gastnr    AS INTEGER. 

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER curr-date    AS CHARACTER.
DEFINE INPUT PARAMETER curr-month   AS INTEGER.
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE INPUT PARAMETER disptype     AS INTEGER.   /*william add input disptype*/
DEFINE OUTPUT PARAMETER TABLE FOR top50-list.


DEFINE VARIABLE mm                      AS INTEGER      NO-UNDO.
DEFINE VARIABLE yy                      AS INTEGER      NO-UNDO.
DEFINE VARIABLE i                       AS INTEGER      NO-UNDO. 
DEFINE VARIABLE from-date               AS DATE         NO-UNDO.
DEFINE VARIABLE to-date                 AS DATE         NO-UNDO.
DEFINE VARIABLE curr-date-loop          AS DATE         NO-UNDO. /* Oscar (11/03/25) - AAFA3A - adjusting query so result same as Room Production Report with filter Travel Agent */
DEFINE VARIABLE datum                   AS DATE         NO-UNDO.
DEFINE VARIABLE jml                     AS INTEGER      NO-UNDO.
DEFINE BUFFER r-list FOR top50-list. 

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "comp-product". 
     
/*****************************************************************************/
FOR EACH top50-list:
    DELETE top50-list.
END.

FOR EACH r-list: 
  DELETE r-list. 
END. 

mm = INTEGER(SUBSTR(curr-date,1,2)). 
yy = INTEGER(SUBSTR(curr-date,3,4)). 
jml = yy - 1.


/* Oscar (11/03/25) - AAFA3A - adjusting query so result same as Room Production Report with filter Travel Agent */
/* 
FOR EACH genstat WHERE YEAR(genstat.datum) = yy AND MONTH(genstat.datum) LE mm
    AND genstat.zinr NE "" AND genstat.karteityp = 2 
    AND genstat.res-logic[2] EQ YES USE-INDEX DATE_ix NO-LOCK
    /*, FIRST guest WHERE guest.gastnr = genstat.gastnr USE-INDEX gastnr_index NO-LOCK*/ :    
    IF disptype EQ 0 THEN         /*william add display type all*/
        FIND FIRST guest WHERE guest.gastnr = genstat.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
    ELSE IF disptype EQ 1 THEN    /*william add display type company*/
        FIND FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.karteityp EQ 1 USE-INDEX gastnr_index NO-LOCK NO-ERROR.
    ELSE IF disptype EQ 2 THEN    /*william add display type all travel agent*/
        FIND FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.karteityp EQ 2 USE-INDEX gastnr_index NO-LOCK NO-ERROR.
    ELSE IF disptype EQ 3 THEN    /*william add display type offline travel agent*/
        FIND FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.karteityp EQ 2 AND guest.steuernr EQ "" USE-INDEX gastnr_index NO-LOCK NO-ERROR.
    ELSE IF disptype EQ 4 THEN    /*william add display type online travel agent*/
        FIND FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.karteityp EQ 2 AND guest.steuernr NE "" USE-INDEX gastnr_index NO-LOCK NO-ERROR.

    FIND FIRST top50-list WHERE top50-list.gastnr = genstat.gastnr NO-ERROR.
    IF NOT AVAILABLE top50-list THEN
    DO:
        CREATE top50-list.
        top50-list.gastnr    = genstat.gastnr.
        IF AVAILABLE guest THEN /*FT serverless*/
            top50-list.bezeich   = guest.NAME.
    END.
    IF genstat.resstatus NE 13 THEN
        ASSIGN  top50-list.room[MONTH(genstat.datum)] = top50-list.room[MONTH(genstat.datum)] + 1
                top50-list.ytd = top50-list.ytd + 1.
END.
    
FOR EACH top50-list:
    FOR EACH genstat WHERE genstat.gastnr = top50-list.gastnr
        AND YEAR(genstat.datum) = yy - 1 AND MONTH(genstat.datum) LE mm
        AND genstat.zinr NE "" 
        AND genstat.res-logic[2] EQ YES USE-INDEX DATE_ix NO-LOCK:
        IF genstat.resstatus NE 13 THEN
            top50-list.lytd = top50-list.lytd + 1.
    END.
END. 
*/

/* Start - Oscar (11/03/25) - AAFA3A - adjusting query so result same as Room Production Report with filter Travel Agent */
from-date = DATE(1, 1, yy).
IF mm EQ 12 THEN
    to-date = DATE(1, 1, yy + 1) - 1.
ELSE
    to-date = DATE(mm + 1, 1, yy) - 1.

DO curr-date-loop = from-date TO to-date:
    FOR EACH genstat WHERE genstat.datum EQ curr-date-loop
        AND genstat.resstatus NE 13
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] NO-LOCK,
        FIRST res-line WHERE res-line.resnr EQ genstat.resnr
        AND res-line.reslinnr EQ genstat.res-int[1] NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.karteityp = 2 NO-LOCK
        BY guest.gastnr:

        IF disptype EQ 2 THEN
        DO:
            RUN create-top-50.
        END.
        ELSE IF disptype EQ 3 AND guest.steuernr EQ "" THEN 
        DO:
            RUN create-top-50.
        END.
        ELSE IF disptype EQ 4 AND guest.steuernr NE "" THEN 
        DO:
            RUN create-top-50.
        END.
    END.
END.


from-date = DATE(1, 1, jml).
IF mm EQ 12 THEN
    to-date = DATE(1, 1, jml + 1) - 1.
ELSE
    to-date = DATE(mm + 1, 1, jml) - 1.

DO curr-date-loop = from-date TO to-date:
    FOR EACH genstat WHERE genstat.datum EQ curr-date-loop
        AND genstat.resstatus NE 13
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] NO-LOCK,
        FIRST res-line WHERE res-line.resnr EQ genstat.resnr
        AND res-line.reslinnr EQ genstat.res-int[1] NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.karteityp = 2 NO-LOCK
        BY guest.gastnr:

        FIND FIRST top50-list WHERE top50-list.gastnr EQ genstat.gastnr NO-ERROR.
        IF AVAILABLE top50-list THEN
        DO:
            top50-list.lytd = top50-list.lytd + 1.
        END.
    END.
END.
/* End - Oscar (11/03/25) - AAFA3A - adjusting query so result same as Room Production Report with filter Travel Agent */

IF curr-month NE 0 THEN
    FOR EACH top50-list:
        top50-list.mtd = top50-list.room[curr-month].
    END.                   

/* Oscar (11/03/25) - AAFA3A - adjusting lytd counter */
i = 0. 
IF sorttype = 0 THEN
    FOR EACH top50-list WHERE top50-list.ytd NE 0 
        OR top50-list.lytd NE 0 
        BY top50-list.ytd DESCENDING BY top50-list.bezeich: 

        i = i + 1. 
        top50-list.nr = i. 
        top50-list.num = i. 
    END. 
ELSE
    FOR EACH top50-list WHERE top50-list.mtd NE 0 
        OR top50-list.lytd NE 0 
        BY top50-list.mtd DESCENDING BY top50-list.bezeich: 

        i = i + 1. 
        top50-list.nr = i. 
        top50-list.num = i. 
    END. 

FOR EACH top50-list WHERE (top50-list.nr = 0) OR (top50-list.nr GT 50): 
    DELETE top50-list. 
END. 

CREATE top50-list. 
ASSIGN  top50-list.num = 999
        top50-list.bezeich = translateExtended ("T O T A L",lvCAREA,""). 

FOR EACH r-list WHERE r-list.num GE 1 AND r-list.num LE 50: 
    DO i = 1 TO 12: 
        top50-list.room[i] = top50-list.room[i] + r-list.room[i]. 
    END. 

    ASSIGN  
        top50-list.ytd   = top50-list.ytd + r-list.ytd
        top50-list.lytd  = top50-list.lytd + r-list.lytd
        top50-list.mtd   = top50-list.mtd + r-list.room[curr-month]
    .
END.

PROCEDURE create-top-50:
    FIND FIRST top50-list WHERE top50-list.gastnr EQ genstat.gastnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE top50-list THEN
    DO:
        CREATE top50-list.
        top50-list.gastnr                     = genstat.gastnr.
        top50-list.bezeich                    = guest.NAME.
    END.

    top50-list.room[MONTH(genstat.datum)] = top50-list.room[MONTH(genstat.datum)] + 1.
    top50-list.ytd                        = top50-list.ytd + 1.
END.
