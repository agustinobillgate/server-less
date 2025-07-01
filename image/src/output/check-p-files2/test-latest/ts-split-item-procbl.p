
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
DEFINE BUFFER buff-h-journal FOR vhp.h-journal. 

FIND FIRST h-bill-line WHERE RECID(h-bill-line) = rec-id NO-LOCK NO-ERROR.
FIND FIRST h-journal WHERE h-journal.schankbuch = rec-id NO-LOCK NO-ERROR. /*bernatd*/
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

    /*add by bernatd ECB1CA*/
    IF AVAILABLE h-journal THEN 
    DO:
      FIND CURRENT vhp.h-journal EXCLUSIVE-LOCK.
      ASSIGN
      vhp.h-journal.anzahl = vhp.h-bill-line.anzahl
      vhp.h-journal.fremdwaehrng = vhp.h-bill-line.fremdwbetrag 
      vhp.h-journal.betrag = vhp.h-bill-line.betrag
      vhp.h-journal.epreis = vhp.h-bill-line.epreis 
      vhp.h-journal.zeit = vhp.h-bill-line.zeit.
    END.

    FIND CURRENT vhp.h-journal NO-LOCK.
    RELEASE vhp.h-journal.
    RELEASE vhp.h-bill-line.
    /*end bernatd ECB1CA*/
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


    /*add bernatd*/
    IF AVAILABLE h-journal THEN 
    DO:
        CREATE buff-h-journal.
        ASSIGN
        buff-h-journal.schankbuch = RECID(h-bline)
        buff-h-journal.rechnr = h-bline.rechnr
        buff-h-journal.artnr = h-bline.artnr 
        buff-h-journal.anzahl = h-bline.anzahl
        buff-h-journal.fremdwaehrng = h-bline.fremdwbetrag
        buff-h-journal.betrag = h-bline.betrag
        buff-h-journal.tischnr = h-bline.tischnr
        buff-h-journal.departement = h-bline.departement
        buff-h-journal.epreis = h-bline.epreis
        buff-h-journal.zeit = h-bline.zeit 
        buff-h-journal.bill-datum = h-bline.bill-datum
        buff-h-journal.sysdate = h-bline.sysdate
        buff-h-journal.bezeich = h-journal.bezeich
        buff-h-journal.kellner-nr = h-journal.kellner-nr
        buff-h-journal.artnr = h-journal.artnr
        buff-h-journal.stornogrund = h-journal.stornogrund
        buff-h-journal.aendertext = h-journal.aendertext
        buff-h-journal.wabkurz = h-journal.wabkurz
        buff-h-journal.segmentcode = h-journal.segmentcode
        buff-h-journal.artnrfront = h-journal.artnrfront
        buff-h-journal.bon-nr = h-journal.bon-nr
        buff-h-journal.zinr = h-journal.zinr
        buff-h-journal.gang = h-journal.gang.

        IF price-decimal = 0 THEN buff-h-journal.epreis = 
        ROUND(h-bline.epreis, 0).   
    END.
    FIND CURRENT buff-h-journal NO-LOCK. 
    /*end bernatd*/
  END. 
END.



