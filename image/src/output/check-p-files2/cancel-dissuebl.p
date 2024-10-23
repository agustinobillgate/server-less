
DEF INPUT PARAMETER lief-nr AS INT.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF INPUT PARAMETER user-init AS CHAR.

DEFINE VARIABLE wert      AS DECIMAL. 
DEFINE VARIABLE billdate  AS DATE. 
DEFINE VARIABLE closedate AS DATE. 
DEFINE VARIABLE anzahl    AS DECIMAL. 
DEFINE VARIABLE t-amount  AS DECIMAL. 
DEFINE VARIABLE tot-anz   AS DECIMAL. 
DEFINE VARIABLE tot-wert  AS DECIMAL. 

DEFINE VARIABLE lscheinnr AS CHAR. 
 
FIND FIRST bediener WHERE bediener.userinit = user-init.
lscheinnr = docu-nr. 

FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
  AND l-ophdr.op-typ = "STT" NO-LOCK NO-ERROR. 
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
closedate = htparam.fdate. 
 
FOR EACH l-op WHERE l-op.lief-nr = lief-nr 
  AND l-op.lscheinnr = docu-nr 
  AND (l-op.op-art = 1 OR l-op.op-art = 3) 
  AND l-op.flag = YES 
  AND l-op.loeschflag = 0 AND l-op.pos GT 0:

  l-op.loeschflag = 2. 
  billdate = l-op.datum. 
  wert = - l-op.warenwert. 
 
  IF l-op.op-art = 1 THEN 
  DO: 
    t-amount = t-amount + wert. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = l-op.lager-nr AND 
      l-bestand.artnr = l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO: 
      l-bestand.anz-eingang = l-bestand.anz-eingang - l-op.anzahl. 
      l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert. 
      l-bestand.anz-ausgang = l-bestand.anz-ausgang - l-op.anzahl. 
      l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op.warenwert. 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO: 
      l-bestand.anz-eingang = l-bestand.anz-eingang - l-op.anzahl. 
      l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert. 
      l-bestand.anz-ausgang = l-bestand.anz-ausgang - l-op.anzahl. 
      l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op.warenwert. 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
  END. 
  ELSE IF l-op.op-art = 3 AND l-ophdr.betriebsnr NE 0 THEN 
  DO: 
    RUN create-lartjob.p(RECID(l-ophdr), l-op.artnr, - l-op.anzahl, 
      - l-op.warenwert, l-op.datum, NO). 
  END. 
END. 
RUN update-ap. 



PROCEDURE update-ap: 
DEFINE VARIABLE ap-license AS LOGICAL INITIAL NO. 
DEFINE VARIABLE ap-acct AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL INITIAL YES. 
 
  FIND FIRST htparam WHERE paramnr = 1016 no-lock. /* ap license */ 
  IF NOT flogical THEN RETURN. 
 
  FIND FIRST htparam WHERE paramnr = 986 NO-LOCK. 
  ap-acct = htparam.fchar. 
  /*FIND FIRST gl-acct WHERE gl-acct.fibukonto = ap-acct NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-acct THEN 
  DO: 
    IF l-lieferant.z-code NE "" THEN 
    DO: 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-lieferant.z-code 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct AND (l-lieferant.z-code NE ap-acct) THEN do-it = NO. 
    END. 
  END.*/

  FIND FIRST gl-acct WHERE gl-acct.fibukonto = ap-acct NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE gl-acct THEN ASSIGN do-it = NO.
  IF NOT do-it THEN RETURN. 
 
  FIND FIRST l-kredit WHERE l-kredit.name = docu-nr 
    AND l-kredit.saldo = - t-amount 
    AND l-kredit.lief-nr = lief-nr 
    AND l-kredit.rgdatum = billdate NO-LOCK NO-ERROR. 
  IF AVAILABLE l-kredit THEN 
  DO: 
    FIND CURRENT l-kredit EXCLUSIVE-LOCK. 
    delete l-kredit. 
  END. 
  ELSE 
  DO: 
    create l-kredit. 
    l-kredit.name = docu-nr. 
    l-kredit.lief-nr = lief-nr. 
    l-kredit.lscheinnr = lscheinnr. 
    l-kredit.rgdatum = billdate. 
    l-kredit.saldo = t-amount. 
    l-kredit.ziel = 0. 
    l-kredit.netto = t-amount. 
    l-kredit.bediener-nr = bediener.nr. 
  END. 
 
  create ap-journal. 
  ap-journal.lief-nr = lief-nr. 
  ap-journal.docu-nr = docu-nr. 
  ap-journal.lscheinnr = docu-nr. 
  ap-journal.rgdatum = billdate. 
  ap-journal.saldo = t-amount. 
  ap-journal.netto = t-amount. 
  ap-journal.userinit = bediener.userinit. 
  ap-journal.zeit = time. 
  ap-journal.bemerk = "Cancel Direct Issueing". 
END. 
