
DEF INPUT PARAMETER str-list-op-recid AS INT.
DEF INPUT PARAMETER bediener-nr AS INT.

RUN del-op.

PROCEDURE del-op:
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE val AS DECIMAL. 
/* DEFINE buffer l-oph FOR l-ophdr. */      /* Rulita 240225 | fixing comment unused code issue git 661 */
 
  FIND FIRST l-op WHERE RECID(l-op) = str-list-op-recid NO-LOCK NO-ERROR. 
  /* Rulita 240225 | Fixing from if avail serveless issue git 661 */
  IF AVAILABLE l-op THEN
  DO:
      FIND CURRENT l-op EXCLUSIVE-LOCK.
      l-op.loeschflag = 2. 
      l-op.fuellflag = bediener-nr. 
      FIND CURRENT l-op NO-LOCK. 
      RELEASE l-op.

    /* FIND FIRST l-oph WHERE l-oph.lscheinnr = l-op.lscheinnr 
      AND l-oph.op-typ = "STT" NO-LOCK NO-ERROR.  */                      /* Rulita 240225 | fixing comment unused code issue git 661 */
    /*IF AVAILABLE l-oph AND l-oph.betriebsnr NE 0 THEN 
      RUN create-lartjob.p(RECID(l-oph), l-op.artnr, - l-op.anzahl, - l-op.warenwert, l-op.datum, NO). */   /* Dody 051224 | bl unused issue git 79 */
  
    FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr 
      AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN
    DO:
      FIND CURRENT l-bestand EXCLUSIVE-LOCK.                                  /* Rulita 240225 | fixing excusive lock issue git 661 */
      l-bestand.anz-ausgang = l-bestand.anz-ausgang - l-op.anzahl. 
      l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op.warenwert. 
      FIND CURRENT l-bestand NO-LOCK. 
      
      qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
      val = l-bestand.val-anf-best + l-bestand.wert-eingang - l-bestand.wert-ausgang. 
      RELEASE l-bestand.
    END.

    /*geral no record l-bestand 27B864*/
    /*qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
    val = l-bestand.val-anf-best + l-bestand.wert-eingang - l-bestand.wert-ausgang.*/ 
    IF qty NE 0 THEN 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR. 
      FIND CURRENT l-artikel EXCLUSIVE-LOCK.                                    /* Rulita 240225 | fixing excusive lock issue git 661 */
      l-artikel.vk-preis = val / qty. 
      FIND CURRENT l-artikel NO-LOCK. 
      RELEASE l-artikel. 
    END. 
  
    FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr 
      AND l-bestand.lager-nr = l-op.lager-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN
    DO:
      FIND CURRENT l-bestand EXCLUSIVE-LOCK.                                    /* Rulita 240225 | fixing excusive lock issue git 661 */
      l-bestand.anz-ausgang = l-bestand.anz-ausgang - l-op.anzahl. 
      l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op.warenwert. 
      FIND CURRENT l-bestand NO-LOCK. 
      RELEASE l-bestand.
    END.

    FIND FIRST l-verbrauch WHERE l-verbrauch.artnr = l-op.artnr 
      AND l-verbrauch.datum = l-op.datum NO-LOCK NO-ERROR. 
    IF AVAILABLE l-verbrauch THEN 
    DO: 
      FIND CURRENT l-verbrauch EXCLUSIVE-LOCK.                                    /* Rulita 240225 | fixing excusive lock issue git 661 */
      l-verbrauch.anz-verbrau = l-verbrauch.anz-verbrau - l-op.anzahl. 
      l-verbrauch.wert-verbrau = l-verbrauch.wert-verbrau + l-op.warenwert. 
      FIND CURRENT l-verbrauch NO-LOCK. 
      RELEASE l-verbrauch.
    END. 

  END.
  /* End if avail l-op */
END. 
/* End procedure */
