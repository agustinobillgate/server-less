
DEF INPUT PARAMETER inv-type AS INT.
DEF INPUT PARAMETER m-endkum AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER closedate AS DATE.
DEF INPUT PARAMETER todate AS DATE.

/********** UPDATE l-op receiving beyond the current closing date ************/
/*MTi = 0. 
n = 0. 
curr-anz = 0.*/
FOR EACH l-op WHERE l-op.op-art LE 4 AND l-op.loeschflag LT 2 
  AND l-op.datum GT closedate AND l-op.datum LE todate NO-LOCK: 
  IF l-op.op-art = 1 OR (l-op.op-art = 2 AND l-op.herkunftflag = 3) 
    OR l-op.op-art = 3 OR l-op.op-art = 4 THEN 
  DO: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-artikel AND ((inv-type = 1 AND endkum LT m-endkum) OR 
      (inv-type = 2 AND endkum GE m-endkum) OR inv-type = 3) THEN 
    DO: 
      RUN update-onhand. 
    END. 
  END. 
END. 
 
/**********  Deleting l-bestand w/ qty = 0 ************/ 
/*MTcurr-anz = 0.*/
FOR EACH l-lager NO-LOCK: 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr 
    AND (l-bestand.anf-best-dat LE closedate OR l-bestand.anf-best-dat = ?) 
    NO-LOCK NO-ERROR. 
  DO TRANSACTION WHILE AVAILABLE l-bestand: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
        NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-artikel THEN
    DO:
      FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
      DELETE l-bestand. 
    END.
    ELSE IF AVAILABLE l-artikel AND ((inv-type = 1 AND endkum LT m-endkum) OR 
      (inv-type = 2 AND endkum GE m-endkum) OR inv-type = 3) THEN 
    DO: 
      IF (l-bestand.anz-anf-best + l-bestand.anz-eingang 
          - l-bestand.anz-ausgang) = 0 THEN 
      DO: 
        FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
        DELETE l-bestand. 
      END. 
    END. 
    FIND NEXT l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr 
      AND (l-bestand.anf-best-dat LE closedate OR l-bestand.anf-best-dat = ?) 
      NO-LOCK NO-ERROR. 
  END. 
END. 
 
DO: 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 
    AND (l-bestand.anf-best-dat LE closedate OR l-bestand.anf-best-dat = ?) 
    NO-LOCK NO-ERROR. 
  DO TRANSACTION WHILE AVAILABLE l-bestand: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
        NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-artikel THEN
    DO:
      FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
      DELETE l-bestand. 
    END.
    ELSE IF AVAILABLE l-artikel AND ((inv-type = 1 AND endkum LT m-endkum) OR 
      (inv-type = 2 AND endkum GE m-endkum) OR inv-type = 3) THEN 
    DO: 
      IF l-bestand.anz-anf-best = 0 AND l-bestand.anz-eingang = 0 
        AND l-bestand.anz-ausgang = 0 THEN 
      DO: 
        FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
        DELETE l-bestand. 
      END. 
    END. 
    FIND NEXT l-bestand WHERE l-bestand.lager-nr = 0 
      AND (l-bestand.anf-best-dat LE closedate OR l-bestand.anf-best-dat = ?) 
      NO-LOCK NO-ERROR.
  END. 
END. 


FOR EACH l-lager NO-LOCK: 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr 
    AND (l-bestand.anf-best-dat LE closedate OR l-bestand.anf-best-dat = ?) 
    NO-LOCK NO-ERROR. 
  DO TRANSACTION WHILE AVAILABLE l-bestand: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
        NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-artikel THEN
    DO:
      FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
      DELETE l-bestand. 
    END.
    ELSE IF AVAILABLE l-artikel AND ((inv-type = 1 AND endkum LT m-endkum) OR 
      (inv-type = 2 AND endkum GE m-endkum) OR inv-type = 3) THEN 
    DO: 
      IF l-bestand.anz-anf-best = 0 AND l-bestand.anz-eingang = 0 
        AND l-bestand.anz-ausgang = 0 THEN 
      DO: 
        FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
        DELETE l-bestand. 
      END. 
    END. 
    FIND NEXT l-bestand WHERE l-bestand.lager-nr = l-lager.lager-nr 
      AND (l-bestand.anf-best-dat LE closedate OR l-bestand.anf-best-dat = ?) 
      NO-LOCK NO-ERROR. 
  END. 
END. 


IF inv-type = 1 THEN 
DO TRANSACTION: 
  FIND FIRST htparam WHERE paramnr = 224 EXCLUSIVE-LOCK. 
  htparam.fdate = todate. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 
END. 
ELSE IF inv-type = 2 THEN 
DO TRANSACTION: 
  FIND FIRST htparam WHERE paramnr = 221 EXCLUSIVE-LOCK. 
  htparam.fdate = todate. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 
END. 
ELSE IF inv-type = 3 THEN 
DO TRANSACTION: 
  FIND FIRST htparam WHERE paramnr = 221 EXCLUSIVE-LOCK. 
  htparam.fdate = todate. 
  FIND CURRENT htparam NO-LOCK. 
  FIND FIRST htparam WHERE paramnr = 224 EXCLUSIVE-LOCK. 
  htparam.fdate = todate. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 
END. 

DO TRANSACTION: 
  FIND FIRST htparam WHERE paramnr = 232 EXCLUSIVE-LOCK. 
  htparam.flogical = NO. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 
END. 


/*****************************************************************************/
PROCEDURE update-onhand: 
DEFINE VARIABLE s-artnr AS INTEGER. 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE transdate AS DATE. 
DEFINE VARIABLE curr-lager AS INTEGER. 
DEFINE VARIABLE tot-anz AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE avrg-price AS DECIMAL FORMAT "->>>,>>>,>>9.999999" INITIAL 0. 
 
  s-artnr    = l-op.artnr. 
  anzahl     = l-op.anzahl. 
  wert       = l-op.warenwert. 
  transdate  = l-op.datum. 
  curr-lager = l-op.lager-nr. 
 
/* UPDATE stock onhand  */ 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
    l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    CREATE l-bestand. 
    l-bestand.artnr = s-artnr. 
    l-bestand.anf-best-dat = transdate. 
  END. 
 
  IF l-op.op-art LE 2 THEN 
  DO: 
    l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
    l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
  END. 
  ELSE 
  DO: 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
  END. 
  FIND CURRENT l-bestand NO-LOCK. 
 
  IF l-op.herkunftflag NE 2 THEN 
  DO: 
    tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
      - l-bestand.anz-ausgang. 
    tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
      - l-bestand.wert-ausgang. 
 
    IF tot-anz NE 0 THEN 
    DO: 
      avrg-price = tot-wert / tot-anz. 
      FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
      l-artikel.vk-preis = avrg-price. 
      FIND CURRENT l-artikel NO-LOCK. 
    END. 
  END. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
    l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    CREATE l-bestand. 
    l-bestand.lager-nr = curr-lager. 
    l-bestand.artnr = s-artnr. 
    l-bestand.anf-best-dat = transdate. 
  END. 
 
  IF l-op.op-art LE 2 THEN 
  DO: 
    l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
    l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
  END. 
  ELSE 
  DO: 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
  END. 
  FIND CURRENT l-bestand NO-LOCK. 
 
END. 

