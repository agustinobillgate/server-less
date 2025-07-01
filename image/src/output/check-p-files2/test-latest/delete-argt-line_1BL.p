DEF TEMP-TABLE t-argt-line LIKE argt-line.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER user-init AS CHARACTER.
DEF INPUT PARAMETER TABLE FOR t-argt-line.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEF VARIABLE proz AS DECIMAL.
DEF VARIABLE betrag AS DECIMAL.
DEF BUFFER temp-bediener FOR bediener.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST t-argt-line NO-ERROR.
        IF NOT AVAILABLE t-argt-line THEN RETURN NO-APPLY.
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
          EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE argt-line THEN
        DO:
          DELETE argt-line.
          RELEASE argt-line.
          success-flag = YES.


          /*FD Jan 18, 2022 => create system log file*/
          betrag = t-argt-line.betrag.
          FIND FIRST temp-bediener WHERE temp-bediener.userinit EQ user-init NO-LOCK.
        
          IF t-argt-line.betrag LE 0 THEN
          DO:
              proz = t-argt-line.betrag.
              betrag = 0.
          END.  
              
          CREATE res-history.
          ASSIGN
              res-history.nr          = temp-bediener.nr
              res-history.datum       = TODAY
              res-history.zeit        = TIME
              res-history.action      = "Arrangement Lines Setup"
              res-history.aenderung   = "Delete => " + "No: " + STRING(t-argt-line.argtnr) + " | " +
                                        "Dept: " + STRING(t-argt-line.departement) + " | " +
                                        "ArtNo: " + STRING(t-argt-line.argt-artnr) + " | " +
                                        "Amt: " + STRING(betrag) + " | " +
                                        "In %: " + STRING(proz) + " | " +
                                        "Type: " + STRING(t-argt-line.fakt-modus) + " | " +
                                        "Incl: " + STRING(t-argt-line.kind1) + " | " +
                                        "Fix: " + STRING(t-argt-line.kind2)
                                        .
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST argt-line WHERE RECID(argt-line) = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE argt-line THEN
        DO:
          DELETE argt-line.
          RELEASE argt-line.
          success-flag = YES.
        END.
    END.
END CASE.

