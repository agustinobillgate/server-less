
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
DEFINE OUTPUT PARAMETER TABLE FOR top50-list.


DEFINE VARIABLE mm                      AS INTEGER      NO-UNDO.
DEFINE VARIABLE yy                      AS INTEGER      NO-UNDO.
DEFINE VARIABLE i                       AS INTEGER      NO-UNDO. 
DEFINE VARIABLE from-date               AS DATE         NO-UNDO.
DEFINE VARIABLE to-date                 AS DATE         NO-UNDO.
DEFINE VARIABLE datum                   AS DATE         NO-UNDO.
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

FOR EACH genstat WHERE YEAR(genstat.datum) = yy AND MONTH(genstat.datum) LE mm
    AND genstat.zinr NE "" AND genstat.karteityp = 2 
    AND genstat.res-logic[2] EQ YES USE-INDEX DATE_ix NO-LOCK,
    FIRST guest WHERE guest.gastnr = genstat.gastnr USE-INDEX gastnr_index NO-LOCK:

    FIND FIRST top50-list WHERE top50-list.gastnr = genstat.gastnr NO-ERROR.
    IF NOT AVAILABLE top50-list THEN
    DO:
        CREATE top50-list.
        ASSIGN  top50-list.gastnr    = genstat.gastnr
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

IF curr-month NE 0 THEN
    FOR EACH top50-list:
        top50-list.mtd = top50-list.room[curr-month].
    END.                   

i = 0. 
IF sorttype = 0 THEN
    FOR EACH top50-list WHERE top50-list.ytd NE 0 
        BY top50-list.ytd DESCENDING BY top50-list.bezeich: 
        i = i + 1. 
        top50-list.nr = i. 
        top50-list.num = i. 
    END. 
ELSE
    FOR EACH top50-list WHERE top50-list.mtd NE 0 
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

FOR EACH r-list WHERE r-list.num LE 50: 
    DO i = 1 TO 12: 
        top50-list.room[i] = top50-list.room[i] + r-list.room[i]. 
    END. 

    ASSIGN  top50-list.ytd   = top50-list.ytd + r-list.ytd
            top50-list.lytd  = top50-list.lytd + r-list.lytd.
END.
