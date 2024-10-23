
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER split-qty AS INT.
DEF INPUT PARAMETER rest AS DECIMAL.
DEF INPUT PARAMETER foreign-rest AS DECIMAL.
DEF INPUT PARAMETER curr-qty AS INT.
DEF INPUT PARAMETER price-decimal AS INT.

DEF INPUT-OUTPUT PARAMETER amount AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER foreign-amt AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER qty-sign AS INT.
DEF VAR i AS INT.

DEFINE BUFFER h-bline FOR vhp.h-bill-line. 

FIND FIRST h-bill-line WHERE RECID(h-bill-line) = rec-id.

DO i = 1 TO split-qty: 
  IF i = split-qty THEN 
  DO TRANSACTION: 
    FIND CURRENT vhp.h-bill-line EXCLUSIVE-LOCK. 
    ASSIGN
      amount = rest
      foreign-amt = foreign-rest 
      vhp.h-bill-line.anzahl = qty-sign
      vhp.h-bill-line.fremdwbetrag = foreign-amt 
      vhp.h-bill-line.betrag = amount
      vhp.h-bill-line.epreis = vhp.h-bill-line.epreis * curr-qty 
                             * qty-sign / split-qty 
      vhp.h-bill-line.epreis = ROUND(vhp.h-bill-line.epreis, price-decimal) 
      vhp.h-bill-line.nettobetrag = vhp.h-bill-line.epreis * vhp.h-bill-line.anzahl /*FD For Web Based*/
      vhp.h-bill-line.zeit = TIME + i
    .
    IF split-qty NE curr-qty THEN 
      vhp.h-bill-line.bezeich = vhp.h-bill-line.bezeich + "*". 
    FIND CURRENT vhp.h-bill-line NO-LOCK. 
    RELEASE vhp.h-bill-line. /*Stack Trace Bali Dynasty*/
  END. 
  ELSE 
  DO TRANSACTION: 
    CREATE h-bline. 
    ASSIGN
      rest = rest - amount
      foreign-rest = foreign-rest - foreign-amt
      h-bline.steuercode = 9999
      h-bline.rechnr = vhp.h-bill-line.rechnr 
      h-bline.artnr = vhp.h-bill-line.artnr
      h-bline.anzahl = qty-sign
      h-bline.fremdwbetrag = foreign-amt 
      h-bline.betrag = amount
      h-bline.tischnr =  vhp.h-bill-line.tisch
      h-bline.departement = vhp.h-bill-line.departement 
      h-bline.epreis = vhp.h-bill-line.epreis * curr-qty 
                     * qty-sign / split-qty 
      h-bline.epreis = ROUND(h-bline.epreis, price-decimal) 
      h-bline.nettobetrag = h-bline.epreis * h-bline.anzahl /*FD For Web Based*/
      h-bline.zeit = TIME + i
      h-bline.bill-datum = vhp.h-bill-line.bill-datum
      h-bline.sysdate = vhp.h-bill-line.sysdate
    . 
    IF split-qty = curr-qty THEN 
      h-bline.bezeich = vhp.h-bill-line.bezeich. 
    ELSE h-bline.bezeich = vhp.h-bill-line.bezeich + "*". 
    IF price-decimal = 0 THEN h-bline.epreis = 
      ROUND(h-bline.epreis, 0). 
    FIND CURRENT h-bline NO-LOCK. 
  END. 
END.
