
DEF INPUT PARAMETER docu-nr     AS CHAR.
DEF INPUT PARAMETER t-amount    AS DECIMAL.
DEF INPUT PARAMETER lief-nr     AS INT.
DEF INPUT PARAMETER billdate    AS DATE.
DEF INPUT PARAMETER lscheinnr   LIKE l-op.lscheinnr.
DEF INPUT PARAMETER bediener-nr AS INT.
DEF INPUT PARAMETER bediener-userinit AS CHAR.

RUN update-ap.

PROCEDURE update-ap:
 
  FIND FIRST l-kredit WHERE l-kredit.name = docu-nr
    AND l-kredit.saldo = - t-amount 
    AND l-kredit.lief-nr = lief-nr 
    AND l-kredit.rgdatum = billdate 
    AND l-kredit.zahlkonto = 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-kredit THEN 
  DO: 
    create l-kredit. 
    l-kredit.name = docu-nr. 
    l-kredit.lief-nr = lief-nr. 
    l-kredit.lscheinnr = lscheinnr. 
    l-kredit.rgdatum = billdate. 
    l-kredit.datum = ?. 
    l-kredit.saldo = t-amount. 
    l-kredit.ziel = 0. 
    l-kredit.netto = t-amount. 
    l-kredit.bediener-nr = bediener-nr. 
    create ap-journal. 
    ap-journal.lief-nr = lief-nr. 
    ap-journal.docu-nr = docu-nr. 
    ap-journal.lscheinnr = lscheinnr. 
    ap-journal.rgdatum = billdate. 
    ap-journal.saldo = t-amount. 
    ap-journal.netto = t-amount. 
    ap-journal.userinit = bediener-userinit. 
    ap-journal.zeit = time. 
    ap-journal.bemerk = "Return". 
    RETURN. 
  END. 
  IF l-kredit.counter = 0 THEN 
  DO: 
    FIND CURRENT l-kredit EXCLUSIVE-LOCK. 
    delete l-kredit. 
    RETURN. 
  END. 
  ELSE 
  DO: 
    create l-kredit. 
    l-kredit.name = docu-nr. 
    l-kredit.lief-nr = lief-nr. 
    l-kredit.lscheinnr = lscheinnr. 
    l-kredit.rgdatum = billdate. 
    l-kredit.datum = ?. 
    l-kredit.saldo = t-amount. 
    l-kredit.ziel = 0. 
    l-kredit.netto = t-amount. 
    l-kredit.bediener-nr = bediener-nr. 
  END. 
 
  create ap-journal. 
  ap-journal.lief-nr = lief-nr. 
  ap-journal.docu-nr = docu-nr. 
  ap-journal.lscheinnr = lscheinnr. 
  ap-journal.rgdatum = billdate. 
  ap-journal.saldo = t-amount. 
  ap-journal.netto = t-amount. 
  ap-journal.userinit = bediener-userinit. 
  ap-journal.zeit = time. 
  ap-journal.bemerk = "Return". 
END. 
