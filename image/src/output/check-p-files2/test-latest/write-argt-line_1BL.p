DEF TEMP-TABLE t-argt-line   LIKE argt-line.
DEF TEMP-TABLE argtlineBuff  LIKE argt-line.

DEF INPUT PARAMETER user-init AS CHARACTER.
DEF INPUT PARAMETER TABLE FOR argtlineBuff.
DEF INPUT PARAMETER TABLE FOR t-argt-line.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEF VARIABLE proz AS DECIMAL.
DEF VARIABLE betrag AS DECIMAL.
DEFINE VARIABLE bezeich AS CHARACTER.
DEF BUFFER temp-bediener FOR bediener.

FIND FIRST argtlineBuff  NO-ERROR.
FIND FIRST t-argt-line   NO-ERROR.
IF AVAILABLE argtlineBuff AND AVAILABLE t-argt-line THEN
DO:
  FIND FIRST argt-line WHERE
    argt-line.argtnr       = argtlineBuff.argtnr      AND
    argt-line.argt-artnr   = argtlineBuff.argt-artnr  AND
    argt-line.departement  = argtlineBuff.departement AND
    argt-line.fakt-modus   = argtlineBuff.fakt-modus  AND
    argt-line.intervall    = argtlineBuff.intervall   AND
    argt-line.kind1        = argtlineBuff.kind1       AND
    argt-line.kind2        = argtlineBuff.kind2       AND
    argt-line.betrag       = argtlineBuff.betrag      AND
    argt-line.betriebsnr   = argtlineBuff.betriebsnr  AND
    argt-line.vt-percnt    = argtlineBuff.vt-percnt
    EXCLUSIVE-LOCK NO-ERROR.

  IF AVAILABLE argt-line THEN
  DO:
      /*FD Jan 18, 2022 => create system log file*/
      betrag = t-argt-line.betrag.      
      IF t-argt-line.betrag LE 0 THEN
      DO:
          proz = t-argt-line.betrag.
          betrag = 0.          
      END.

      FIND FIRST temp-bediener WHERE temp-bediener.userinit EQ user-init NO-LOCK.      
          
      CREATE res-history.
      ASSIGN
          res-history.nr          = temp-bediener.nr
          res-history.datum       = TODAY
          res-history.zeit        = TIME
          res-history.action      = "Arrangement Lines Setup".

      bezeich = "Change => " + "No: " + STRING(t-argt-line.argtnr) + " | " + 
            "Dept: " + STRING(argt-line.departement) + " - " + "Art: " + STRING(argt-line.argt-artnr). /* Naufal Afthar - 8C22F6*/
      IF argt-line.departement NE t-argt-line.departement THEN
      DO:
          bezeich = bezeich + " | " + "DeptNo: " + STRING(argt-line.departement) + " to: " + STRING(t-argt-line.departement).
      END.
      IF argt-line.argt-artnr NE t-argt-line.argt-artnr THEN
      DO:
          bezeich = bezeich + " | " + "ArtNo: " + STRING(argt-line.argt-artnr) + " to: " + STRING(t-argt-line.argt-artnr).
      END.
      IF argt-line.betrag GT 0 AND argt-line.betrag NE betrag THEN
      DO:
          bezeich = bezeich + " | " + "Amt: " + STRING(argt-line.betrag) + " to: " + STRING(betrag).
          
          IF t-argt-line.betrag LE 0 THEN
              bezeich = bezeich + " | " + "In %: " + STRING(betrag) + " to: " + STRING(proz).
      END.
      IF argt-line.betrag LE 0 AND argt-line.betrag NE proz THEN
      DO:
          bezeich = bezeich + " | " + "In %: " + STRING(argt-line.betrag) + " to: " + STRING(proz).

          IF t-argt-line.betrag GT 0 THEN
              bezeich = bezeich + " | " + "Amt: " + STRING(proz) + " to: " + STRING(betrag).
      END.      
      IF argt-line.fakt-modus NE t-argt-line.fakt-modus THEN
      DO:
          bezeich = bezeich + " | " + "Type: " + STRING(argt-line.fakt-modus) + " to: " + STRING(t-argt-line.fakt-modus).
      END.
      IF argt-line.kind1 NE t-argt-line.kind1 THEN
      DO:
          bezeich = bezeich + " | " + "Incl: " + STRING(argt-line.kind1) + " to: " + STRING(t-argt-line.kind1).
      END.
      IF argt-line.kind2 NE t-argt-line.kind2 THEN
      DO:
          bezeich = bezeich + " | " + "Fix: " + STRING(argt-line.kind2) + " to: " + STRING(t-argt-line.kind2).
      END.

      res-history.aenderung   = bezeich.                                    

      BUFFER-COPY t-argt-line TO argt-line.
      RELEASE argt-line.
      success-flag = YES.      
  END.
END.
