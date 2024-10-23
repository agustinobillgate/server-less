
DEF INPUT  PARAMETER op-list-artnr      AS INT.
DEF INPUT  PARAMETER op-list-fuellflag  AS INT.
DEF INPUT  PARAMETER op-list-stornogrund AS CHAR.
DEF INPUT  PARAMETER curr-lager         AS INT.
DEF OUTPUT PARAMETER s-bezeich          AS CHAR.
DEF OUTPUT PARAMETER s-bez2             AS CHAR.
DEF OUTPUT PARAMETER s-username         AS CHAR.
DEF OUTPUT PARAMETER s-onhand           AS DECIMAL.

DEF BUFFER l-art FOR l-artikel.
DEF BUFFER sys-user FOR bediener.

FIND FIRST l-art WHERE l-art.artnr = op-list-artnr NO-LOCK. 
FIND FIRST sys-user WHERE sys-user.nr = op-list-fuellflag NO-LOCK.
FIND FIRST l-bestand WHERE l-bestand.artnr = op-list-artnr
    AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR.
ASSIGN
    s-bezeich  = l-art.bezeich
    s-username = sys-user.username
  .
IF AVAILABLE l-bestand THEN s-onhand = l-bestand.anz-anf-best
    + l-bestand.anz-eingang - l-bestand.anz-ausgang.


FIND FIRST gl-acct WHERE gl-acct.fibukonto = op-list-stornogrund NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN 
  s-bez2 = gl-acct.bezeich.
