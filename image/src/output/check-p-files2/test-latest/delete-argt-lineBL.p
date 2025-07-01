DEF TEMP-TABLE t-argt-line LIKE argt-line.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER TABLE FOR t-argt-line.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.


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

