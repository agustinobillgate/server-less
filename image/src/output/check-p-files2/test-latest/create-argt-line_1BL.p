DEF TEMP-TABLE t-argt-line LIKE argt-line.

DEF INPUT PARAMETER user-init AS CHARACTER.
DEF INPUT PARAMETER TABLE FOR t-argt-line.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEF VARIABLE proz AS DECIMAL.
DEF VARIABLE betrag AS DECIMAL.
DEF VARIABLE force-qty-stats AS LOGICAL. /* Naufal Afthar - 8C22F6*/
DEF BUFFER temp-bediener FOR bediener.

FIND FIRST t-argt-line NO-ERROR.
IF AVAILABLE t-argt-line THEN
DO:
  success-flag = YES.
  betrag = t-argt-line.betrag.
  FIND FIRST argt-line WHERE
    argt-line.argtnr       = t-argt-line.argtnr      AND
    argt-line.argt-artnr   = t-argt-line.argt-artnr  AND
    argt-line.departement  = t-argt-line.departement AND
    argt-line.fakt-modus   = t-argt-line.fakt-modus  AND
    argt-line.intervall    = t-argt-line.intervall   AND
    argt-line.kind1        = t-argt-line.kind1       AND
    argt-line.kind2        = t-argt-line.kind2       AND
    argt-line.betrag       = t-argt-line.betrag      AND
    argt-line.betriebsnr   = t-argt-line.betriebsnr  AND
    argt-line.vt-percnt    = t-argt-line.vt-percnt 
    NO-LOCK NO-ERROR.
  IF NOT AVAILABLE argt-line THEN
  DO:
      CREATE argt-line.
      BUFFER-COPY t-argt-line TO argt-line.
      RELEASE argt-line.     
  END.
  
  /*FD Jan 18, 2022 => create system log file*/
  FIND FIRST temp-bediener WHERE temp-bediener.userinit EQ user-init NO-LOCK.

  IF t-argt-line.betrag LE 0 THEN
  DO:
      proz = t-argt-line.betrag.
      betrag = 0.
  END. 

  /* Naufal Afthar - 8C22F6*/
  IF t-argt-line.betriebsnr EQ 1 THEN force-qty-stats = YES.
  ELSE force-qty-stats = NO.
      
  CREATE res-history.
  ASSIGN
      res-history.nr          = temp-bediener.nr
      res-history.datum       = TODAY
      res-history.zeit        = TIME
      res-history.action      = "Arrangement Lines Setup"
      res-history.aenderung   = "Create => " + "No: " + STRING(t-argt-line.argtnr) + " | " +
                                "Dept: " + STRING(t-argt-line.departement) + " | " +
                                "ArtNo: " + STRING(t-argt-line.argt-artnr) + " | " +
                                "Amt: " + STRING(betrag) + " | " +
                                "In %: " + STRING(proz) + " | " +
                                "Type: " + STRING(t-argt-line.fakt-modus) + " | " +
                                "Incl: " + STRING(t-argt-line.kind1) + " | " +
                                "Fixt: " + STRING(t-argt-line.kind2) + " | " +
                                "Force One Qty: " + STRING(force-qty-stats) /* Naufal Afthar - 8C22F6*/
                                .      
END.
