
DEF TEMP-TABLE q1-list
    FIELD netto     LIKE l-kredit.netto
    FIELD zahlkonto LIKE l-kredit.zahlkonto
    FIELD bezeich   LIKE artikel.bezeich
    FIELD rgdatum   LIKE l-kredit.rgdatum
    FIELD saldo     LIKE l-kredit.saldo
    FIELD username  LIKE bediener.username  .

DEF INPUT  PARAMETER ap-recid AS INT.
DEF OUTPUT PARAMETER counter  AS INT.
DEF OUTPUT PARAMETER invoice  AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FIND FIRST l-kredit WHERE RECID(l-kredit) = ap-recid NO-LOCK. 
counter = l-kredit.counter.
invoice = l-kredit.name.

IF counter NE 0 THEN
FOR EACH l-kredit WHERE l-kredit.counter = counter
    AND l-kredit.opart GE 0 AND l-kredit.zahlkonto GT 0 NO-LOCK
    USE-INDEX counter_ix,
    FIRST artikel WHERE artikel.artnr = l-kredit.zahlkonto
    AND artikel.departement = 0 NO-LOCK,
    FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr
    NO-LOCK BY l-kredit.rgdatum BY l-kredit.zahlkonto:
    CREATE q1-list.
    ASSIGN
      q1-list.netto     = l-kredit.netto
      q1-list.zahlkonto = l-kredit.zahlkonto
      q1-list.bezeich   = artikel.bezeich
      q1-list.rgdatum   = l-kredit.rgdatum
      q1-list.saldo     = l-kredit.saldo
      q1-list.username  = bediener.username.
END.
