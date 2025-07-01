
DEF BUFFER l-op1 FOR l-op.

DEF INPUT PARAMETER t-list-datum AS DATE.
DEF INPUT PARAMETER t-list-lscheinnr AS CHAR.
DEF OUTPUT PARAMETER successFlag AS LOGICAL.

DO TRANSACTION:
  FOR EACH l-op WHERE l-op.datum = t-list-datum
    AND (l-op.op-art = 2 OR l-op.op-art = 4)
    AND l-op.lscheinnr = t-list-lscheinnr 
    AND l-op.loeschflag LE 1 NO-LOCK:
    IF l-op.op-art = 2 THEN
    DO:
      FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
        AND l-bestand.lager-nr = l-op.lager-nr EXCLUSIVE-LOCK
        NO-ERROR.
      IF AVAILABLE l-bestand THEN
      DO:
        l-bestand.anz-eingang = l-bestand.anz-eingang - l-op.anzahl.
        l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert.
        FIND CURRENT l-bestand NO-LOCK.
      END.
      FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
        AND l-bestand.lager-nr = 0 EXCLUSIVE-LOCK
        NO-ERROR.
      IF AVAILABLE l-bestand THEN
      DO:
        l-bestand.anz-eingang = l-bestand.anz-eingang - l-op.anzahl.
        l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert.
        FIND CURRENT l-bestand NO-LOCK.
      END.
    END.
    ELSE IF l-op.op-art = 4 THEN
    DO:
      FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
        AND l-bestand.lager-nr = l-op.lager-nr EXCLUSIVE-LOCK
        NO-ERROR.
      IF AVAILABLE l-bestand THEN
      DO:
        l-bestand.anz-ausgang = l-bestand.anz-ausgang + l-op.anzahl.
        l-bestand.wert-ausgang = l-bestand.wert-ausgang + l-op.warenwert.
        FIND CURRENT l-bestand NO-LOCK.
      END.
      FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
        and l-bestand.lager-nr = 0 EXCLUSIVE-LOCK
        NO-ERROR.
      IF AVAILABLE l-bestand THEN
      DO:
        l-bestand.anz-ausgang = l-bestand.anz-ausgang + l-op.anzahl.
        l-bestand.wert-ausgang = l-bestand.wert-ausgang + l-op.warenwert.
        FIND CURRENT l-bestand NO-LOCK.
      END.
      FIND FIRST l-verbrauch WHERE l-verbrauch.artnr = l-op.artnr
        AND l-verbrauch.datum = l-op.datum EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE l-verbrauch THEN
      DO:
        l-verbrauch.anz-verbrau = l-verbrauch.anz-verbrau - l-op.anzahl.
        l-verbrauch.wert-verbrau = l-verbrauch.wert-verbrau - l-op.warenwert.
        FIND CURRENT l-verbrauch NO-LOCK.
      END.
    END.
    FIND FIRST l-op1 WHERE RECID(l-op1) = RECID(l-op) EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE l-op1 THEN
    DO:
        ASSIGN l-op1.loeschflag = 2.
        ASSIGN successFlag = YES.
        FIND CURRENT l-op1 NO-LOCK.
    END.
    ELSE ASSIGN successFlag = NO.
  END.
END.

