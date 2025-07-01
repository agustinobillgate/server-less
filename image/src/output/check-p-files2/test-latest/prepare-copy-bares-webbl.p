DEFINE TEMP-TABLE room-list
    FIELD room-id   AS CHAR
    FIELD room-name AS CHAR
    FIELD prep-time AS INTEGER.

DEFINE INPUT  PARAMETER resnr       AS INTEGER. 
DEFINE INPUT  PARAMETER reslinnr    AS INTEGER. 
DEFINE OUTPUT PARAMETER datum       AS DATE.
DEFINE OUTPUT PARAMETER ftime       LIKE bk-reser.von-zeit.
DEFINE OUTPUT PARAMETER ttime       LIKE bk-reser.bis-zeit.
 
DEFINE OUTPUT PARAMETER from-date   AS DATE.
DEFINE OUTPUT PARAMETER to-date     AS DATE.
DEFINE OUTPUT PARAMETER gname       AS CHAR.
DEFINE OUTPUT PARAMETER raum        AS CHAR.
DEFINE OUTPUT PARAMETER raum1       AS CHAR.
DEFINE OUTPUT PARAMETER statsort    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.

/* FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK. */              /* Rulita 200225 | bk-veran unused  */
FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr 
    AND bk-reser.veran-resnr = reslinnr NO-LOCK NO-ERROR. 
/* Rulita 200225 | Fixing serverless if avail issue git 618 */ 
IF AVAILABLE bk-reser THEN
DO:
    FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
        AND bk-func.veran-seite = reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-func THEN statsort = bk-reser.resstatus.                    /* Rulita 200225 | Fixing serverless if avail issue git 618 */ 

    FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum NO-LOCK NO-ERROR.     
    /* Rulita 200225 | Fixing serverless if avail issue git 618 */ 
    IF AVAILABLE bk-raum THEN
    DO:
        datum = bk-reser.datum. 
        ftime = bk-reser.von-zeit. 
        ttime = bk-reser.bis-zeit. 
        raum  = bk-raum.bezeich. 
        raum1 = bk-raum.raum.
        
        from-date = datum + 1. 
        to-date   = from-date. 
        gname     = bk-func.bestellt_durch. 

        FOR EACH bk-raum NO-LOCK:
            CREATE room-list.
            ASSIGN 
                room-list.room-id   = bk-raum.raum   
                room-list.room-name = bk-raum.bezeich
                room-list.prep-time = bk-raum.vorbereit.
        END.
    END.
    /* End Rulita */
END.
/* End Rulita */