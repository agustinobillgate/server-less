DEF TEMP-TABLE t-argt-line LIKE argt-line.

DEF INPUT PARAMETER TABLE FOR t-argt-line.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

FIND FIRST t-argt-line NO-ERROR.
IF AVAILABLE t-argt-line THEN
DO:
  success-flag = YES.
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
END.
