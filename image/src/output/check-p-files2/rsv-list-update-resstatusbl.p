
DEF INPUT-OUTPUT PARAMETER output-list-resnr        AS INT.
DEF INPUT-OUTPUT PARAMETER output-list-reslinnr     AS INT.
DEF INPUT        PARAMETER r-status                 AS INTEGER. 
DEF INPUT        PARAMETER c-status                 AS CHAR. 
DEF OUTPUT       PARAMETER output-list-str          AS CHAR.
DEF OUTPUT       PARAMETER output-list-resstatus    AS INT.
DEF OUTPUT       PARAMETER output-list-sob          AS CHAR.
DEF OUTPUT       PARAMETER gastnr                   AS INT.
DEF OUTPUT       PARAMETER output-list-gastnr       AS INT.

RUN update-resstatus.

PROCEDURE update-resstatus: 
  DO TRANSACTION: 
    FIND FIRST bk-func WHERE bk-func.veran-nr = output-list-resnr 
      AND bk-func.veran-seite = output-list-reslinnr EXCLUSIVE-LOCK. 
    ASSIGN 
      bk-func.resstatus = r-status 
      bk-func.r-resstatus[1] = r-status 
      bk-func.c-resstatus[1] = c-status. 
    FIND CURRENT bk-func NO-LOCK. 
 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = output-list-resnr 
      AND bk-reser.veran-seite = output-list-reslinnr EXCLUSIVE-LOCK. 
    ASSIGN 
      bk-reser.resstatus = r-status. 
    FIND CURRENT bk-reser NO-LOCK. 
 
    FIND FIRST bk-veran WHERE bk-veran.veran-nr = output-list-resnr EXCLUSIVE-LOCK. 
    ASSIGN bk-veran.resstatus = r-status. 
    FIND CURRENT bk-veran NO-LOCK. 
 
 
    ASSIGN 
      output-list-str = STRING(bk-func.bis-datum,"99/99/99") + 
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
        output-list-resnr = bk-func.veran-nr 
        output-list-reslinnr = bk-func.veran-seite 
        output-list-resstatus = bk-func.resstatus.
        output-list-sob   = bk-func.technik[2].
    gastnr = bk-veran.gastnr.
    output-list-gastnr = bk-veran.gastnr.
  END. 
END. 
