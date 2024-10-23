
DEF INPUT PARAMETER datum AS DATE.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER pax AS INT.
DEF INPUT PARAMETER fpax AS INT.
DEF INPUT PARAMETER bpax AS INT.

FIND FIRST h-umsatz WHERE h-umsatz.datum = datum
    AND h-umsatz.departement = dept
    AND h-umsatz.betriebsnr = dept NO-LOCK NO-ERROR.
IF AVAILABLE h-umsatz THEN
DO TRANSACTION:
   FIND CURRENT h-umsatz EXCLUSIVE-LOCK.
   ASSIGN
       h-umsatz.anzahl      = pax
       h-umsatz.betrag      = fpax
       h-umsatz.nettobetrag = bpax
   .
   FIND CURRENT h-umsatz NO-LOCK.
END.
