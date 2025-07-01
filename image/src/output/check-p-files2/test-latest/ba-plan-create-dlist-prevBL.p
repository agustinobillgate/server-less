
DEFINE TEMP-TABLE rml 
  FIELD nr          AS INTEGER 
  FIELD raum        AS CHAR 
  FIELD bezeich     AS CHAR FORMAT "x(32)" LABEL "Room" FONT 1 
  FIELD departement AS INTEGER
  FIELD resnr       AS INTEGER EXTENT 48 
  FIELD reslinnr    AS INTEGER EXTENT 48 
  FIELD gstatus     AS INTEGER EXTENT 48 
  FIELD room        AS CHAR    EXTENT 48 FORMAT "x(1)" FONT 1
  FIELD blocked     AS INTEGER EXTENT 48
. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR rml.
DEF INPUT PARAMETER from-date AS DATE.

DEFINE BUFFER gast    FOR guest. 

FOR EACH bk-reser WHERE (bk-reser.datum = from-date
    OR (bk-reser.datum LE from-date AND bk-reser.bis-datum GE from-date)) 
    AND bk-reser.resstatus LE 8 USE-INDEX zeit_ix NO-LOCK, 
    FIRST bk-veran WHERE bk-veran.veran-nr = bk-reser.veran-nr NO-LOCK, 
    FIRST gast WHERE gast.gastnr = bk-veran.gastnr NO-LOCK:
    RUN create-dlist1-prev (bk-reser.raum, bk-reser.raum).
END.

PROCEDURE create-dlist1-prev:
DEFINE INPUT PARAMETER parent-rm AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER curr-rm   AS CHAR NO-UNDO.

DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 
DEFINE VARIABLE k           AS INTEGER. 
DEFINE VARIABLE l           AS INTEGER. 
DEFINE VARIABLE m           AS INTEGER. 
DEFINE VARIABLE start       AS INTEGER. 
DEFINE VARIABLE finish      AS INTEGER. 
DEFINE VARIABLE gastname    AS CHAR.
DEFINE BUFFER bk-buff  FOR bk-reser.
DEFINE BUFFER rmBuff   FOR bk-raum.
DEFINE BUFFER childRm  FOR bk-raum.
                                 
    FIND FIRST rml WHERE rml.raum = curr-rm AND rml.nr = 1 NO-LOCK NO-ERROR.
    
    ASSIGN gastname = gast.NAME.
    IF bk-veran.bemerkung NE "" THEN gastname = "*" + gastname.
    j = 1. 
    IF bk-reser.datum = bk-reser.bis-datum THEN 
    DO: 
        start = bk-reser.von-i. 
        finish = bk-reser.bis-i. 
    END. 
    ELSE IF bk-reser.datum = from-date AND bk-reser.bis-datum GT from-date THEN 
    DO: 
        start = bk-reser.von-i. 
        finish = 48. 
    END. 
    ELSE IF bk-reser.datum LT from-date 
        AND bk-reser.bis-datum = from-date THEN 
    DO: 
        start = 1. 
        finish = bk-reser.bis-i. 
    END. 
    ELSE IF bk-reser.datum LT from-date AND bk-reser.bis-datum GT from-date THEN 
    DO: 
        start = 1. 
        finish = 48. 
    END. 

    /*ITA 280316*/
    IF START = 0 THEN ASSIGN START = 1.
    IF finish = 49 THEN ASSIGN finish = 48.

    DO i = start TO finish:
        IF i GT 0 AND i LT 49 THEN
        DO:
            rml.gstatus[i] = bk-reser.resstatus.
            IF bk-reser.resstatus = 8 THEN
            DO:
                FIND FIRST bk-buff WHERE (bk-buff.datum = from-date
                    OR (bk-buff.datum LE from-date AND bk-buff.bis-datum GE from-date) )
                    AND bk-buff.resstatus = 8 AND bk-buff.raum = bk-reser.raum
                    AND i LE bk-buff.bis-i AND i GE bk-buff.von-i
                    USE-INDEX zeit_ix NO-LOCK NO-ERROR.
                IF AVAILABLE bk-buff /*AND i LE bk-buff.bis-i AND i GE bk-buff.von-i*/THEN
                DO:
                    rml.gstatus[i] = 8.  
                END.
                ELSE rml.gstatus[i] = bk-reser.resstatus. 
                     
            END. 
            ASSIGN
              rml.room[i]       = SUBSTR(gastname, j, 1)
              rml.resnr[i]      = bk-reser.veran-nr
              rml.reslinnr[i]   = bk-reser.veran-resnr 
              j                 = j + 1
            . 
            IF parent-rm NE curr-rm THEN rml.blocked[i] = 1.
        END.      
    END. 
    FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum USE-INDEX raum-ix NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-raum THEN 
    DO: 
        IF bk-raum.vorbereit NE 0 THEN 
        DO: 
            k = bk-raum.vorbereit / 30. 
            IF bk-raum.vorbereit GT k * 30 THEN 
            DO:
                k = k + 1. 
            END. 
            l = start. 
            IF l - 1 GT 0 THEN 
            DO: 
              DO m = l - k TO l - 1: 
                  IF m GT 0 THEN 
                  DO: 
                      IF rml.gstatus[m] = 0 THEN 
                      DO: 
                          rml.gstatus[m] = 8. 
                          rml.resnr[m] = bk-reser.veran-nr. 
                          rml.reslinnr[m] = bk-reser.veran-resnr. 
                      END. 
                  END. 
              END. 
            END. 
        END. 
    END.
END.

