
DEF INPUT  PARAMETER s-artnr        AS INT.
DEF INPUT  PARAMETER curr-lager     AS INT.
DEF INPUT  PARAMETER avail-out-list AS LOGICAL.
DEF INPUT  PARAMETER transdate      AS DATE.
DEF INPUT  PARAMETER mat-closedate  AS DATE.
DEF INPUT  PARAMETER closedate      AS DATE.
DEF INPUT  PARAMETER req-flag       AS LOGICAL.
DEF INPUT  PARAMETER lscheinnr      LIKE l-op.lscheinnr.

DEF OUTPUT PARAMETER l-artikel-artnr AS INT.
DEF OUTPUT PARAMETER stock-oh       AS DECIMAL.
DEF OUTPUT PARAMETER description    AS CHAR.
DEF OUTPUT PARAMETER price          AS DECIMAL.
DEF OUTPUT PARAMETER l-op-lscheinnr LIKE l-op.lscheinnr.
DEF OUTPUT PARAMETER err-flag       AS INT INIT 0.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-artikel THEN 
DO:
  err-flag = 1.
  RETURN NO-APPLY. 
END. 
l-artikel-artnr = l-artikel.artnr.
IF l-artikel.betriebsnr = 0 THEN 
DO: 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
    AND l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO:
    err-flag = 2.
    RETURN NO-APPLY. 
  END. 
  ELSE 
  DO: 
    IF avail-out-list THEN 
    DO:
      err-flag = 3.
      RETURN NO-APPLY. 
    END. 
    IF l-artikel.endkum LT 3 THEN 
    DO: 
      IF transdate GT closedate THEN 
      DO:
        err-flag = 4.
        RETURN NO-APPLY. 
      END. 
    END. 
    IF l-artikel.endkum EQ 3 THEN 
    DO: 
      IF transdate GT mat-closedate THEN 
      DO:
        err-flag = 5.
        RETURN NO-APPLY. 
      END. 
    END. 
    IF req-flag THEN 
    DO: 
      FIND FIRST l-op WHERE l-op.artnr = s-artnr AND 
        l-op.datum = transdate AND (l-op.op-art = 3 OR l-op.op-art = 4) 
        AND SUBSTR(l-op.lscheinnr,4, (length(l-op.lscheinnr) - 3)) = 
      SUBSTR(lscheinnr,4, (length(lscheinnr) - 3)) NO-LOCK NO-ERROR. 
      IF AVAILABLE l-op THEN 
      DO:
        err-flag = 6.
      END. 
    END. 
    stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
      - l-bestand.anz-ausgang. 
    description = l-artikel.bezeich + " - " + l-artikel.masseinheit. 
    price = l-artikel.vk-preis.
    err-flag = 7.
    RETURN NO-APPLY. 
  END. 
END. 
ELSE 
DO: 
  description = l-artikel.bezeich + " - " + l-artikel.masseinheit. 
  price = 0. 
  stock-oh = 0.
  err-flag = 8.
  RETURN NO-APPLY. 
END.
