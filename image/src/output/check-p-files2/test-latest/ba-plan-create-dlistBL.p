
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
DEF INPUT  PARAMETER from-date      AS DATE.

DEFINE BUFFER rmBuff  FOR bk-raum.
DEFINE BUFFER childRM FOR bk-raum.
DEFINE BUFFER gast    FOR guest. 

DEFINE VARIABLE i      AS INTEGER. 
DEFINE VARIABLE maxpar AS INTEGER. 

FOR EACH bk-reser WHERE (bk-reser.datum = from-date
    OR (bk-reser.datum LE from-date AND bk-reser.bis-datum GE from-date)) 
    AND bk-reser.resstatus LE 3 USE-INDEX zeit_ix NO-LOCK, 
    FIRST bk-veran WHERE bk-veran.veran-nr = bk-reser.veran-nr NO-LOCK :

    FIND FIRST gast WHERE gast.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR.
    
    RUN create-dlist1(bk-reser.raum, bk-reser.raum).
    
    FIND FIRST childRM WHERE childRM.raum = bk-reser.raum NO-LOCK NO-ERROR.
    IF childRM.lu-raum MATCHES "*;*" THEN
    DO:
        maxpar = NUM-ENTRIES(childRM.lu-raum, ";").
        DO i = 1 TO maxpar:
            FIND FIRST rmBuff WHERE rmBuff.raum = ENTRY(i, childRM.lu-raum, ";") NO-LOCK NO-ERROR.
            RUN create-dlist2 (bk-reser.raum, rmBuff.raum).
        END.
    END.
    ELSE
    DO:
        FOR EACH rmBuff WHERE rmBuff.raum = childRM.lu-raum NO-LOCK:
            RUN create-dlist2 (bk-reser.raum, rmBuff.raum).
        END.
    END.
END.

PROCEDURE create-dlist1:
DEFINE INPUT PARAMETER parent-rm        AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER curr-rm          AS CHAR NO-UNDO.

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

    FIND FIRST rml WHERE rml.raum = curr-rm AND rml.nr = bk-reser.resstatus NO-ERROR.
    IF AVAILABLE rml THEN  DO:
        /*ITA 020415*/
        IF AVAILABLE gast THEN ASSIGN gastname = gast.NAME.
        ELSE ASSIGN gastname = "Please re-attach guest.".
        
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
            rml.gstatus[i] = bk-reser.resstatus.
            IF bk-reser.resstatus = 2 THEN
            DO:
                /*FIND FIRST bk-buff WHERE (bk-buff.datum = from-date
                    OR (bk-buff.datum LE from-date AND bk-buff.bis-datum GE from-date) )
                    AND bk-buff.resstatus = 3 AND bk-buff.raum = bk-reser.raum
                    AND i LE bk-buff.bis-i AND i GE bk-buff.von-i
                     USE-INDEX zeit_ix NO-LOCK NO-ERROR.
                IF AVAILABLE bk-buff /*AND i LE bk-buff.bis-i AND i GE bk-buff.von-i*/THEN
                DO:
                    rml.gstatus[i] = -1.  /*new 24 feb : tentative with waiting list exist*/
                END.
                ELSE*/ rml.gstatus[i] = bk-reser.resstatus. 
            END. 
            IF bk-reser.resstatus = 3 THEN rml.gstatus[i] = -1.
            ASSIGN
              rml.room[i]       = SUBSTR(gastname, j, 1)
              rml.resnr[i]      = bk-reser.veran-nr
              rml.reslinnr[i]   = bk-reser.veran-resnr 
              j                 = j + 1
            . 
            IF parent-rm NE curr-rm THEN rml.blocked[i] = 1.
        END. 
        
        FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum 
          USE-INDEX raum-ix NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-raum THEN 
        DO: 
            IF bk-raum.vorbereit NE 0 THEN 
            DO: 
                k = bk-raum.vorbereit / 30. 
                IF bk-raum.vorbereit GT k * 30 THEN k = k + 1.
                l = start. 
                IF l - 1 GT 0 THEN 
                DO: 
                  DO m = l - k TO l - 1: 
                    IF m GT 0 THEN 
                    DO: 
                      IF rml.gstatus[m] = 0 THEN 
                      DO: 
                        rml.gstatus[m] = 3. 
                        rml.resnr[m] = bk-reser.veran-nr. 
                        rml.reslinnr[m] = bk-reser.veran-resnr. 
                      END. 
                    END. 
                  END.                  
                END. 
            END. 
        END.
    END.
    
    FOR EACH rmBuff WHERE ENTRY(1 ,rmBuff.lu-raum , ";") = curr-rm NO-LOCK:
        RUN create-dlist1 (bk-reser.raum, rmBuff.raum).
    END.
END.

PROCEDURE create-dlist2:
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

    FIND FIRST rml WHERE rml.raum = curr-rm AND rml.nr = bk-reser.resstatus NO-ERROR.
    IF AVAILABLE rml THEN DO:
        /*ITA 020415*/
        IF AVAILABLE gast THEN ASSIGN gastname = gast.NAME.
        ELSE ASSIGN gastname = "Please re-attach guest.".
        
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
    
        /*ITa 280316*/
        IF START = 0 THEN ASSIGN START = 1.
        IF finish = 49 THEN ASSIGN finish = 48.
    
        DO i = start TO finish: 
            rml.gstatus[i] = bk-reser.resstatus.
            IF bk-reser.resstatus = 2 THEN
            DO:
                /*FIND FIRST bk-buff WHERE (bk-buff.datum = from-date
                    OR (bk-buff.datum LE from-date AND bk-buff.bis-datum GE from-date) )
                    AND bk-buff.resstatus = 3 AND bk-buff.raum = bk-reser.raum
                    AND i LE bk-buff.bis-i AND i GE bk-buff.von-i
                     USE-INDEX zeit_ix NO-LOCK NO-ERROR.
                IF AVAILABLE bk-buff /*AND i LE bk-buff.bis-i AND i GE bk-buff.von-i*/THEN
                DO:
                    rml.gstatus[i] = -1.  /*new 24 feb : tentative with waiting list exist*/
                END.
                ELSE*/ rml.gstatus[i] = bk-reser.resstatus. 
            END. 
            IF bk-reser.resstatus = 3 THEN rml.gstatus[i] = -1.
            
            ASSIGN
              rml.room[i]       = SUBSTR(gastname, j, 1)
              rml.resnr[i]      = bk-reser.veran-nr
              rml.reslinnr[i]   = bk-reser.veran-resnr 
              j                 = j + 1
            . 
            IF parent-rm NE curr-rm THEN rml.blocked[i] = 2.
        END.
    
        FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum 
            USE-INDEX raum-ix NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-raum THEN 
        DO: 
            IF bk-raum.vorbereit NE 0 THEN 
            DO: 
                k = bk-raum.vorbereit / 30. 
                IF bk-raum.vorbereit GT k * 30 THEN k = k + 1. 
                l = start. 
                IF l - 1 GT 0 THEN 
                DO: 
                  DO m = l - k TO l - 1: 
                    IF m GT 0 THEN 
                    DO: 
                      IF rml.gstatus[m] = 0 THEN 
                      DO: 
                        rml.gstatus[m] = 3. 
                        rml.resnr[m] = bk-reser.veran-nr. 
                        rml.reslinnr[m] = bk-reser.veran-resnr. 
                      END. 
                    END. 
                  END. 
                END. 
            END. 
        END.
    END.
    
    FIND FIRST childRM WHERE childRM.raum = curr-rm NO-LOCK.
    FOR EACH rmBuff WHERE rmBuff.raum = childRM.lu-raum NO-LOCK:
        RUN create-dlist2 (bk-reser.raum, rmBuff.raum).
    END.
END.
