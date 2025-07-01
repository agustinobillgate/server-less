
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
  DEFINE VARIABLE deposit AS DECIMAL NO-UNDO.
  DEFINE VARIABLE total-paid AS DECIMAL NO-UNDO.

  DO TRANSACTION: 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = output-list-resnr 
      AND bk-reser.veran-seite = output-list-reslinnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE bk-reser THEN /*FT serverless*/
    DO:
      ASSIGN 
        bk-reser.resstatus = r-status. 
      FIND CURRENT bk-reser NO-LOCK. 
    END.

    FIND FIRST bk-veran WHERE bk-veran.veran-nr = output-list-resnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE bk-veran THEN
    DO:
      ASSIGN 
        bk-veran.resstatus = r-status
        gastnr = bk-veran.gastnr
        output-list-gastnr = bk-veran.gastnr
        deposit = bk-veran.deposit
        total-paid = bk-veran.total-paid.
      FIND CURRENT bk-veran NO-LOCK. 
    END.

    FIND FIRST bk-func WHERE bk-func.veran-nr = output-list-resnr 
      AND bk-func.veran-seite = output-list-reslinnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE bk-func THEN /*FT serverless*/
    DO:
      ASSIGN 
        bk-func.resstatus = r-status 
        bk-func.r-resstatus[1] = r-status 
        bk-func.c-resstatus[1] = c-status
        output-list-resnr = bk-func.veran-nr 
        output-list-reslinnr = bk-func.veran-seite 
        output-list-resstatus = bk-func.resstatus
        output-list-sob   = bk-func.technik[2]
        output-list-str = STRING(bk-func.bis-datum,"99/99/99") + 
              STRING(bk-func.bestellt_durch,"x(32)") + 
              STRING(bk-func.v-kontaktperson[1],"x(32)") + 
              STRING(bk-func.zweck[1],"x(18)") + 
              STRING(bk-func.raeume[1],"x(12)") + 
              STRING(bk-func.uhrzeit,"x(13)") + 
              STRING(bk-func.personen,">,>>>")
        output-list-str = output-list-str + 
              STRING(deposit,">>>,>>>,>>9") + 
              STRING(total-paid,">>>,>>>,>>9")
        output-list-str = output-list-str + 
              STRING(bk-func.vgeschrieben,"x(2)") + 
              STRING(bk-func.veran-nr,">>>,>>>") + 
              STRING(bk-func.veran-seite,">>>") + 
              STRING(bk-func.c-resstatus[1],"x(1)").
      FIND CURRENT bk-func NO-LOCK. 
    END.
 
    /*IF AVAILABLE bk-func THEN
    DO:
      ASSIGN 
        output-list-str = STRING(bk-func.bis-datum,"99/99/99") + 
              STRING(bk-func.bestellt_durch,"x(32)") + 
              STRING(bk-func.v-kontaktperson[1],"x(32)") + 
              STRING(bk-func.zweck[1],"x(18)") + 
              STRING(bk-func.raeume[1],"x(12)") + 
              STRING(bk-func.uhrzeit,"x(13)") + 
              STRING(bk-func.personen,">,>>>").
      IF AVAILABLE bk-veran THEN
        output-list-str = output-list-str + 
              STRING(bk-veran.deposit,">>>,>>>,>>9") + 
              STRING(bk-veran.total-paid,">>>,>>>,>>9").
      ELSE
        output-list-str = output-list-str + 
              STRING("","x(11)") +
              STRING("","x(11)").

      output-list-str = output-list-str + 
              STRING(bk-func.vgeschrieben,"x(2)") + 
              STRING(bk-func.veran-nr,">>>,>>>") + 
              STRING(bk-func.veran-seite,">>>") + 
              STRING(bk-func.c-resstatus[1],"x(1)").
    END.
      
    IF AVAILABLE bk-func THEN
    DO:
      ASSIGN
        output-list-resnr = bk-func.veran-nr 
        output-list-reslinnr = bk-func.veran-seite 
        output-list-resstatus = bk-func.resstatus.
        output-list-sob   = bk-func.technik[2].
    END.
      
    IF AVAILABLE bk-veran THEN
      ASSIGN
        gastnr = bk-veran.gastnr
        output-list-gastnr = bk-veran.gastnr.*/
  END. 
END. 
