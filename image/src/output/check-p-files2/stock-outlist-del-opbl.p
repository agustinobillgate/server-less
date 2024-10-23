
DEF INPUT PARAMETER str-list-op-recid AS INT.
DEF INPUT PARAMETER bediener-nr AS INT.

RUN del-op.

PROCEDURE del-op:
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
DEFINE buffer l-oph FOR l-ophdr. 
 
  FIND FIRST l-op WHERE RECID(l-op) = str-list-op-recid EXCLUSIVE-LOCK NO-ERROR. 
  l-op.loeschflag = 2. 
  l-op.fuellflag = bediener-nr. 
  FIND CURRENT l-op NO-LOCK. 
 
  FIND FIRST l-oph WHERE l-oph.lscheinnr = l-op.lscheinnr 
    AND l-oph.op-typ = "STT" NO-LOCK NO-ERROR. 
  IF AVAILABLE l-oph AND l-oph.betriebsnr NE 0 THEN 
    RUN create-lartjob.p(RECID(l-oph), l-op.artnr, - l-op.anzahl, 
      - l-op.warenwert, l-op.datum, NO). 
 
  FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr 
    AND l-bestand.lager-nr = 0 EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-bestand THEN
  DO:
    l-bestand.anz-ausgang = l-bestand.anz-ausgang - l-op.anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op.warenwert. 
    FIND CURRENT l-bestand NO-LOCK. 
    
    qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
    val = l-bestand.val-anf-best + l-bestand.wert-eingang - l-bestand.wert-ausgang. 
  END.

  /*geral no record l-bestand 27B864*/
  /*qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
  val = l-bestand.val-anf-best + l-bestand.wert-eingang - l-bestand.wert-ausgang.*/ 
  IF qty NE 0 THEN 
  DO: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
    l-artikel.vk-preis = val / qty. 
    FIND CURRENT l-artikel NO-LOCK. 
  END. 
 
  FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr 
    AND l-bestand.lager-nr = l-op.lager-nr EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-bestand THEN
  DO:
    l-bestand.anz-ausgang = l-bestand.anz-ausgang - l-op.anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op.warenwert. 
    FIND CURRENT l-bestand NO-LOCK. 
  END.

  FIND FIRST l-verbrauch WHERE l-verbrauch.artnr = l-op.artnr 
    AND l-verbrauch.datum = l-op.datum EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-verbrauch THEN 
  DO: 
    l-verbrauch.anz-verbrau = l-verbrauch.anz-verbrau - l-op.anzahl. 
    l-verbrauch.wert-verbrau = l-verbrauch.wert-verbrau + l-op.warenwert. 
    FIND CURRENT l-verbrauch NO-LOCK. 
  END. 
END. 
