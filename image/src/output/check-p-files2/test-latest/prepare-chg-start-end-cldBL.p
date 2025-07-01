
DEF TEMP-TABLE t-rsv-table LIKE bk-reser
    FIELD rec-id AS INT
    FIELD t-vorbereit LIKE bk-raum.vorbereit.
DEF TEMP-TABLE t-bk-reser  LIKE bk-reser
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER resnr          AS INT.
DEF INPUT  PARAMETER reslinnr       AS INT.
DEF INPUT  PARAMETER curr-date      AS DATE.
DEF OUTPUT PARAMETER chg-date       AS DATE.
DEF OUTPUT PARAMETER ci-date        AS DATE.
DEF OUTPUT PARAMETER update-ok      AS LOGICAL.
DEF OUTPUT PARAMETER begin-i2       LIKE bk-reser.von-i.
DEF OUTPUT PARAMETER ending-i2      LIKE bk-reser.bis-i.
DEF OUTPUT PARAMETER begin-time     LIKE bk-reser.von-zeit. 
DEF OUTPUT PARAMETER begin-i        LIKE bk-reser.von-i. 
DEF OUTPUT PARAMETER ending-time    LIKE bk-reser.bis-zeit. 
DEF OUTPUT PARAMETER ending-i       LIKE bk-reser.bis-i. 
DEF OUTPUT PARAMETER msg            AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-rsv-table.
DEF OUTPUT PARAMETER TABLE FOR t-bk-reser.

DEFINE VARIABLE i               LIKE bk-reser.von-i.
DEFINE VARIABLE s               LIKE bk-reser.bis-i.

DEF BUFFER rsv-table FOR bk-reser.
chg-date = curr-date.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

update-ok = NO. 
FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr 
  AND bk-reser.veran-resnr = reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE bk-reser THEN 
DO: 
    FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum NO-LOCK.
    IF bk-reser.datum = chg-date AND bk-reser.bis-datum = chg-date THEN 
    DO: 
      i = (((bk-raum.vorbereit + 0.1) * 2 ) + 1) / 60.
      begin-i2 =  bk-reser.von-i - i.
      begin-time = bk-reser.von-zeit. 
      begin-i = bk-reser.von-i. 
      ending-time = bk-reser.bis-zeit. 
      ending-i = bk-reser.bis-i. 
      s = (((bk-raum.vorbereit + 0.1) * 2 ) + 1) / 60.
      ending-i2 = bk-reser.bis-i + s.

      msg = 1.
    END. 
    ELSE IF bk-reser.datum = chg-date AND bk-reser.bis-datum GT chg-date THEN 
    DO: 
      begin-time = bk-reser.von-zeit. 
      i = (((bk-raum.vorbereit + 0.1) * 2 ) + 1) / 60.
      begin-i = bk-reser.von-i. 
      begin-i2 =  bk-reser.von-i - i.
      ending-time = "24:00". 
      ending-i = 48. 

      msg = 2.
    END. 
    ELSE IF bk-reser.datum LT chg-date AND bk-reser.bis-datum = chg-date THEN 
    DO: 
      begin-time = "00:00". 
      begin-i = 1. 
      ending-time = bk-reser.bis-zeit. 
      s = (((bk-raum.vorbereit + 0.1) * 2 ) + 1) / 60.
      ending-i2 = bk-reser.bis-i + s.
      ending-i = bk-reser.bis-i. 

      msg = 3.
    END. 
    ELSE IF bk-reser.datum LT chg-date AND bk-reser.bis-datum GT chg-date THEN 
    DO: 
      begin-time = "00:00". 
      begin-i = 1. 
      ending-time = "24:00". 
      ending-i = 48. 
    END. 
END. 
ELSE 
DO: 
    msg = 4.
END. 

IF AVAILABLE bk-reser THEN
DO:
    /* FDL July 18, 2024 - CHG to cldBL cause this is not use in vhpcloud & make not responding | Ticket A93F56
    FOR EACH rsv-table WHERE rsv-table.raum = bk-reser.raum 
        AND rsv-table.resstatus LE 2,
        FIRST bk-raum WHERE bk-raum.raum = rsv-table.raum NO-LOCK:
        CREATE t-rsv-table.
        BUFFER-COPY rsv-table TO t-rsv-table.
        ASSIGN t-rsv-table.rec-id = RECID(rsv-table)
               t-rsv-table.t-vorbereit = bk-raum.vorbereit.
    END.
    */
    CREATE t-bk-reser.
    BUFFER-COPY bk-reser TO t-bk-reser.
    ASSIGN t-bk-reser.rec-id = RECID(bk-reser).
END.
