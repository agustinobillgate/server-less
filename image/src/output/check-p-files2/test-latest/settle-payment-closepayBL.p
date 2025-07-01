

DEFINE INPUT PARAMETER   user-init   AS CHAR.
DEFINE INPUT PARAMETER   artnr       AS INT.
DEFINE INPUT PARAMETER   p-betrag    AS DECIMAL.
DEFINE INPUT PARAMETER   f-amt       AS DECIMAL.
DEFINE INPUT PARAMETER   bill-date   AS DATE.

RUN settle-payment.


PROCEDURE settle-payment: 
  DEFINE VARIABLE saldo-i  AS DECIMAL.
  DEFINE VARIABLE count    AS INTEGER.
  DEFINE VARIABLE anzahl   AS INTEGER.
  DEFINE VARIABLE supplier AS CHAR.
  DEFINE buffer debitor1 FOR debitor. 
  
  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
  create debitor1. 
  debitor1.gastnr = debitor.gastnr. 
  debitor1.opart = 2. 
  debitor1.name = debitor.name. 
  debitor1.rechnr = debitor.rechnr. 
  debitor1.gastnr = debitor.gastnr. 
  debitor1.zahlkonto = artnr. 
  debitor1.saldo = p-betrag. 
  debitor1.vesrdep = f-amt.
  debitor1.betrieb-gastmem = artikel.betriebsnr.
  debitor1.counter = debitor.counter. 
  debitor1.rgdatum = bill-date. 
  debitor1.bediener-nr = bediener.nr. 
 
  FIND FIRST umsatz WHERE umsatz.departement = 0 AND 
    umsatz.artnr = artnr AND umsatz.datum = bill-date 
    EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN create umsatz. 
  umsatz.datum = bill-date. 
  umsatz.artnr = artnr. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  umsatz.betrag = umsatz.betrag + debitor.saldo. 
  release umsatz. 
 
  create billjournal. 
  FIND FIRST artikel WHERE artikel.artnr = artnr AND artikel.departement = 0 NO-LOCK. 
  billjournal.rechnr = debitor.rechnr. 
  billjournal.bill-datum = bill-date. 
  billjournal.artnr = artnr. 
  billjournal.betrag = p-betrag. 
  billjournal.bezeich = artikel.bezeich. 
  billjournal.zeit = time. 
  billjournal.bediener-nr = bediener.nr. 
  billjournal.userinit = user-init. 
  release billjournal. 
 
END. 
