DEF TEMP-TABLE t-argt-line   LIKE argt-line.
DEF TEMP-TABLE argtlineBuff  LIKE argt-line.

DEF INPUT PARAMETER TABLE FOR argtlineBuff.
DEF INPUT PARAMETER TABLE FOR t-argt-line.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

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
      BUFFER-COPY t-argt-line TO argt-line.
      RELEASE argt-line.
      success-flag = YES.
  END.

END.
