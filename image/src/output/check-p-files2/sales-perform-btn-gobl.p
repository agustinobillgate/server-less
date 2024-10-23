DEFINE TEMP-TABLE slist
    FIELD Yr            AS INTEGER
    FIELD mnth          AS INTEGER
    FIELD lodg          LIKE salestat.argtumsatz
    FIELD lbudget       LIKE salesbud.argtumsatz
    FIELD lproz         AS DECIMAL FORMAT ">>9.99"
    FIELD fbrev         LIKE salestat.f-b-umsatz
    FIELD fbbudget      LIKE salesbud.f-b-umsatz
    FIELD fbproz        AS DECIMAL FORMAT ">>9.99"
    FIELD otrev         LIKE salestat.sonst-umsatz
    FIELD otbudget      LIKE salesbud.sonst-umsatz
    FIELD otproz        AS DECIMAL FORMAT ">>9.99"
    FIELD rmnight       LIKE salestat.room-nights
    FIELD rbudget       LIKE salesbud.room-nights 
    FIELD rmproz        AS DECIMAL FORMAT ">>9.99"
    FIELD ytd-lodg      LIKE salestat.argtumsatz
    FIELD ytd-lbudget   LIKE salesbud.argtumsatz
    FIELD ytd-lproz     AS DECIMAL FORMAT ">>9.99"
    FIELD ytd-fbrev     LIKE salestat.sonst-umsatz
    FIELD ytd-fbbudget  LIKE salesbud.sonst-umsatz
    FIELD ytd-fbproz    AS DECIMAL FORMAT ">>9.99"
    FIELD ytd-rmnight   LIKE salestat.room-nights
    FIELD ytd-rbudget   LIKE salesbud.room-nights 
    FIELD ytd-rmproz    AS DECIMAL FORMAT ">>9.99"
    FIELD ytd-otrev     LIKE salestat.sonst-umsatz
    FIELD ytd-otbudget  LIKE salesbud.sonst-umsatz
    FIELD ytd-otproz    AS DECIMAL FORMAT ">>9.99"
    .

DEF INPUT  PARAMETER from-date AS CHAR.
DEF INPUT  PARAMETER to-date   AS CHAR.
DEF INPUT  PARAMETER usr-init  AS CHAR.
DEF OUTPUT PARAMETER its-ok    AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER TABLE FOR slist.

DEFINE VARIABLE m1 AS INTEGER. 
DEFINE VARIABLE m2 AS INTEGER. 
DEFINE VARIABLE y1 AS INTEGER. 
DEFINE VARIABLE y2 AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE monat AS INTEGER. 
DEFINE VARIABLE jahr AS INTEGER. 
  m1 = INTEGER(SUBSTR(from-date,1,2)). 
  y1 = INTEGER(SUBSTR(from-date,3,4)). 
  y2 = INTEGER(SUBSTR(to-date,3,4)). 
  m2 = INTEGER(SUBSTR(to-date,1,2)). 

FIND FIRST bediener WHERE bediener.userinit = usr-init NO-LOCK NO-ERROR. 
RUN check-budget.
IF its-ok THEN RUN create-list.

PROCEDURE check-budget: 
DEFINE VARIABLE m1 AS INTEGER. 
DEFINE VARIABLE m2 AS INTEGER. 
DEFINE VARIABLE y1 AS INTEGER. 
DEFINE VARIABLE y2 AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE monat AS INTEGER. 
DEFINE VARIABLE jahr AS INTEGER. 
  m1 = INTEGER(SUBSTR(from-date,1,2)). 
  y1 = INTEGER(SUBSTR(from-date,3,4)). 
  y2 = INTEGER(SUBSTR(to-date,3,4)). 
  m2 = INTEGER(SUBSTR(to-date,1,2)) + y2 - y1. 
 
  jahr = y1. 
  DO monat = m1 TO m2: 
    IF monat GT 12 THEN 
    DO: 
      monat = 1. 
      jahr = jahr + 1. 
    END. 
    FIND FIRST salesbud WHERE salesbud.bediener-nr = bediener.nr 
      AND salesbud.monat = monat AND salesbud.jahr = jahr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE salesbud THEN 
    DO:
      CREATE salesbud.
      ASSIGN
          salesbud.bediener-nr = bediener.nr
          salesbud.monat       = monat
          salesbud.jahr        = jahr
      .
      FIND CURRENT salesbud NO-LOCK.
/*
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("No Sales budget for period ",lvCAREA,"") + STRING(monat,"99") 
        "/" + STRING(jahr,"9999") 
        SKIP 
        translateExtended ("Calculation not possible",lvCAREA,"") 
      VIEW-AS ALERT-BOX INFORMATION. 
      its-ok = NO. 
*/      
      RETURN. 
    END. 

    /*gerald 300720*/
    FIND FIRST salestat WHERE salestat.bediener-nr = bediener.nr 
      AND salestat.monat = monat AND salestat.jahr = jahr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE salestat THEN 
    DO:
      CREATE salestat.
      ASSIGN
          salestat.bediener-nr = bediener.nr
          salestat.monat       = monat
          salestat.jahr        = jahr
      .
      FIND CURRENT salesbud NO-LOCK.
      RETURN. 
    END. 
  END. 
END. 

PROCEDURE create-list:
    DEF VARIABLE mm-room AS INTEGER NO-UNDO INIT 0.
    DEF VARIABLE c-room  AS INTEGER NO-UNDO.
    
    DEF VARIABLE do-it   AS LOGICAL NO-UNDO.
    DEF VARIABLE fdate   AS DATE    NO-UNDO.
    DEF VARIABLE mm      AS INTEGER NO-UNDO.
    DEF VARIABLE yy      AS INTEGER NO-UNDO.
    
    DEF VARIABLE loopi       AS DATE    NO-UNDO.
    DEF VARIABLE frdate      AS DATE    NO-UNDO.
    DEF VARIABLE tdate       AS DATE    NO-UNDO.
    DEF VARIABLE mdate       AS INTEGER NO-UNDO.
    DEF VARIABLE ytd-lodging AS DECIMAL NO-UNDO.
    DEF VARIABLE ytd-rmnight AS DECIMAL NO-UNDO.
    DEF VARIABLE mtd-lodging AS DECIMAL NO-UNDO.
    DEF VARIABLE mtd-rmnight AS DECIMAL NO-UNDO.
    

    DEF BUFFER stat-buff FOR salestat.
    DEF BUFFER bud-buff  FOR salesbud.
    DEF BUFFER bgenstat  FOR genstat.
   
    FOR EACH slist:
        DELETE slist.
    END.

    IF INT(SUBSTR(to-date, 1,2)) = 1 OR INT(SUBSTR(to-date, 1,2)) = 3
       OR INT(SUBSTR(to-date, 1,2)) = 5 OR INT(SUBSTR(to-date, 1,2)) = 7 
       OR INT(SUBSTR(to-date, 1,2)) = 8 OR INT(SUBSTR(to-date, 1,2)) = 10
       OR INT(SUBSTR(to-date, 1,2)) = 12 THEN ASSIGN mdate = 31.
    ELSE IF INT(SUBSTR(to-date, 1,2)) = 4 OR INT(SUBSTR(to-date, 1,2)) = 6
       OR INT(SUBSTR(to-date, 1,2)) = 9 OR INT(SUBSTR(to-date, 1,2)) = 11 
       THEN ASSIGN mdate = 30.
    ELSE DO:
        IF (INT(SUBSTR(to-date, 1,2)) MODULO 4) = 0 THEN ASSIGN mdate = 29.
        ELSE ASSIGN mdate = 28.
    END.
    
    ASSIGN 
        frdate = DATE(INT(SUBSTR(from-date, 1,2)), 1, INT(SUBSTR(from-date, 3,4)))
        tdate = DATE(INT(SUBSTR(to-date, 1,2)), mdate, INT(SUBSTR(to-date, 3,4))).

    DO loopi = frdate TO tdate:
        FIND FIRST slist WHERE slist.mnth = MONTH(loopi) AND slist.yr = YEAR(loopi) NO-LOCK NO-ERROR.  
        IF NOT AVAILABLE slist THEN DO:
            CREATE slist.
            ASSIGN
                slist.yr        = YEAR(loopi)
                slist.mnth      = MONTH(loopi).
        END.
    END.
   
    ASSIGN fdate = DATE(1,1, INT(SUBSTR(from-date, 3,4))).

    FOR EACH genstat WHERE genstat.datum GE fdate
           AND genstat.datum LE tdate
           AND genstat.zinr NE "" 
           AND genstat.res-logic[2] 
           USE-INDEX date_ix NO-LOCK,
           FIRST guest WHERE guest.gastnr = genstat.gastnr 
                 NO-LOCK BY genstat.datum BY guest.name BY guest.gastnr:

        ASSIGN do-it = YES.
        IF genstat.zipreis = 0 THEN DO:
            IF (genstat.gratis GT 0) THEN do-it = NO.
            IF (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis = 0)
               AND genstat.resstatus NE 13 THEN do-it = NO.
        END.

        IF do-it AND usr-init NE ? THEN DO:
            IF guest.phonetik3 = TRIM(usr-init) THEN DO:
                ASSIGN ytd-lodging = ytd-lodging + genstat.logis
                       ytd-rmnight = ytd-rmnight + 1.
                
                FIND FIRST slist WHERE slist.mnth = MONTH(genstat.datum) AND slist.yr = YEAR(genstat.datum) 
                    NO-LOCK NO-ERROR.            
                IF AVAILABLE slist THEN DO:
                    IF genstat.resstatus NE 13 THEN     
                        ASSIGN
                            mtd-lodging       = mtd-lodging + genstat.logis
                            mtd-rmnight       = mtd-rmnight + 1
                            slist.lodg        = mtd-lodging
                            slist.rmnight     = mtd-rmnight
                            slist.ytd-lodg    = ytd-lodging
                            slist.ytd-rmnight = ytd-rmnight.
                END.   
            END.
        END.
    END. 

   FOR EACH salestat WHERE salestat.bediener-nr = bediener.nr AND 
      ((salestat.jahr GT INTEGER(SUBSTR(from-date,3,4)) AND salestat.monat GE 1) OR 
       (salestat.jahr EQ INTEGER(SUBSTR(from-date,3,4)) AND 
        salestat.monat GE INTEGER(SUBSTR(from-date,1,2)))) AND 
      ((salestat.jahr LT INTEGER(SUBSTR(to-date,3,4)) AND salestat.monat GE 1) OR 
       (salestat.jahr EQ INTEGER(SUBSTR(to-date,3,4)) AND 
        salestat.monat LE INTEGER(SUBSTR(to-date,1,2)))) NO-LOCK,
       FIRST salesbud WHERE salesbud.bediener-nr = salestat.bediener-nr 
         AND salesbud.monat = salestat.monat AND salesbud.jahr = salestat.jahr 
        NO-LOCK BY salestat.jahr BY salestat.monat:

        FIND FIRST slist WHERE (slist.mnth = salestat.monat) AND slist.Yr = salestat.jahr NO-LOCK NO-ERROR.            
      
        IF AVAILABLE slist THEN
        DO:     
          ASSIGN      
              slist.lbudget   = salesbud.argtumsatz
              slist.otrev     = salestat.sonst-umsatz
              slist.otbudget  = salesbud.sonst-umsatz
              slist.otproz    = salestat.sonst-umsatz / salesbud.sonst-umsatz * 100
              slist.fbrev     = salestat.f-b-umsatz
              slist.fbbudget  = salesbud.f-b-umsatz
              slist.fbproz     = salestat.f-b-umsatz / salesbud.f-b-umsatz * 100           
              slist.rbudget   = salesbud.room-nights .

      
         FOR EACH stat-buff WHERE stat-buff.bediener-nr = bediener.nr AND
              stat-buff.jahr = salestat.jahr AND stat-buff.monat LE salestat.monat
              NO-LOCK, FIRST bud-buff WHERE bud-buff.bediener-nr = stat-buff.bediener-nr
              AND bud-buff.monat = stat-buff.monat AND bud-buff.jahr = stat-buff.jahr
              NO-LOCK BY stat-buff.jahr BY stat-buff.monat:
              ASSIGN 
                  slist.ytd-lbudget  = slist.ytd-lbudget + bud-buff.argtumsatz
                  slist.ytd-otrev    = slist.ytd-otrev + stat-buff.sonst-umsatz
                  slist.ytd-otbudget = slist.ytd-otbudget + bud-buff.sonst-umsatz
                  slist.ytd-fbrev    = slist.ytd-fbrev + stat-buff.f-b-umsatz
                  slist.ytd-fbbudget = slist.ytd-fbbudget + bud-buff.f-b-umsatz
                  slist.ytd-rbudget  = slist.ytd-rbudget + bud-buff.room-nights.
          END.
          ASSIGN
              slist.ytd-fbproz       = slist.ytd-fbrev / slist.ytd-fbbudget * 100
              slist.ytd-otproz       = slist.ytd-otrev / slist.ytd-otbudget * 100.
  
          
          IF slist.otproz = ? THEN slist.otproz = 0.00.
          IF slist.fbproz = ? THEN slist.fbproz = 0.00.
          IF slist.ytd-fbproz = ? THEN slist.ytd-fbproz = 0.00.
          IF slist.ytd-otproz = ? THEN slist.ytd-otproz = 0.00.
        END.
    END.

    FOR EACH slist NO-LOCK:
        ASSIGN 
            slist.lproz         = slist.lodg / mtd-lodging * 100
            slist.rmproz        = slist.rmnight / mtd-rmnight * 100
            slist.ytd-lproz     = slist.ytd-lodg / slist.ytd-lbudget * 100
            slist.ytd-rmproz    = slist.ytd-rmnight / slist.ytd-rbudget * 100.
    
            IF slist.lproz = ? THEN slist.lproz = 0.00.
            IF slist.rmproz = ? THEN slist.rmproz = 0.00.
            IF slist.ytd-lproz = ? THEN slist.ytd-lproz = 0.00.
            IF slist.ytd-rmproz = ? THEN slist.ytd-rmproz = 0.00.
    END.


END. 

