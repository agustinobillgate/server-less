DEFINE TEMP-TABLE t-output-list 
  FIELD resnr     AS INTEGER 
  FIELD reslinnr  AS INTEGER 
  FIELD resstatus AS INTEGER 
  FIELD datum     AS DATE 
  FIELD crdate    AS DATE
  FIELD cutOff    AS DATE
  FIELD STR       AS CHAR. 

DEF INPUT  PARAMETER r-status       AS INTEGER. 
DEF INPUT  PARAMETER c-status       AS CHAR. 
DEF INPUT  PARAMETER o-resnr        AS INT.
DEF INPUT  PARAMETER o-reslinnr     AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-output-list.
RUN update-resstatus.

PROCEDURE update-resstatus: 
  DO TRANSACTION: 
    FIND FIRST bk-func WHERE bk-func.veran-nr = o-resnr
      AND bk-func.veran-seite = o-reslinnr EXCLUSIVE-LOCK. 
    ASSIGN 
      bk-func.resstatus = r-status 
      bk-func.r-resstatus[1] = r-status 
      bk-func.c-resstatus[1] = c-status. 
    FIND CURRENT bk-func NO-LOCK. 
 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = o-resnr 
      AND bk-reser.veran-seite = o-reslinnr EXCLUSIVE-LOCK. 
    ASSIGN 
      bk-reser.resstatus = r-status. 
    FIND CURRENT bk-reser NO-LOCK. 
 
    FIND FIRST bk-veran WHERE bk-veran.veran-nr = o-resnr EXCLUSIVE-LOCK. 
    ASSIGN bk-veran.resstatus = r-status. 
    FIND CURRENT bk-veran NO-LOCK. 
 
    CREATE t-output-list.
    ASSIGN 
      t-output-list.str = STRING(bk-func.bis-datum,"99/99/99") + 
              STRING(bk-func.bestellt_durch,"x(32)") + 
              STRING(bk-func.v-kontaktperson[1],"x(32)") + 
              STRING(bk-func.zweck[1],"x(18)") + 
              STRING(bk-func.raeume[1],"x(12)") + 
              STRING(bk-func.uhrzeit,"x(13)") + 
              STRING(bk-func.personen,">,>>>") + 
              STRING(bk-veran.deposit,">>>,>>>,>>9") + 
              STRING(bk-veran.total-paid,">>>,>>>,>>9") + 
              STRING(bk-func.vgeschrieben,"x(2)") + 
              STRING(bk-func.veran-nr,">>>,>>>") + 
              STRING(bk-func.veran-seite,">>>") + 
              STRING(bk-func.c-resstatus[1],"x(1)") 
        t-output-list.resnr = bk-func.veran-nr 
        t-output-list.reslinnr = bk-func.veran-seite 
        t-output-list.resstatus = bk-func.resstatus       
        . 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr NO-ERROR.
    IF AVAILABLE bk-reser THEN
      t-output-list.cutOff = bk-reser.limitdate
    .
  END. 
END. 
