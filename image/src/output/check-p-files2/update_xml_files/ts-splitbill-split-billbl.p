DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line
    FIELD rec-id AS INT.

DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.

DEFINE WORKFILE art-list LIKE vhp.h-bill-line. 

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
RUN split-bill.

FOR EACH h-bill-line WHERE h-bill-line.departement EQ dept
    AND h-bill-line.rechnr EQ h-bill.rechnr
    AND h-bill-line.waehrungsnr EQ 0 NO-LOCK BY h-bill-line.bezeich:
    CREATE t-h-bill-line.
    BUFFER-COPY h-bill-line TO t-h-bill-line.
    ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).
END.

PROCEDURE split-bill: 
DEFINE VARIABLE h-artart    AS INTEGER. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE amount      AS DECIMAL. 
DEFINE VARIABLE splitamount AS DECIMAL.
DEFINE VARIABLE pos-anz     AS INTEGER. 
 
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
    AND vhp.h-bill-line.departement = dept NO-LOCK: 

    IF vhp.h-bill-line.artnr NE 0 THEN 
    DO: 
      FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
        AND vhp.h-artikel.departement = vhp.h-bill-line.departement NO-LOCK. 
      h-artart = vhp.h-artikel.artart. 
    END. 
    ELSE h-artart = 2. 
 
    FIND FIRST art-list WHERE art-list.artnr = vhp.h-bill-line.artnr 
      AND art-list.departement = vhp.h-bill-line.departement 
      AND art-list.bezeich = vhp.h-bill-line.bezeich 
      AND art-list.waehrungsnr = vhp.h-bill-line.waehrungsnr 
      AND art-list.betriebsnr = vhp.h-bill-line.betriebsnr
      NO-LOCK NO-ERROR. 

    IF NOT AVAILABLE art-list 
      OR (AVAILABLE art-list AND h-artart NE 0) 
/*      
      OR (AVAILABLE art-list AND art-list.waehrungsnr NE 0) 
      OR (AVAILABLE art-list AND art-list.betriebsnr NE 0) 
*/
    THEN 
    DO:      
      CREATE art-list. 
      ASSIGN
        art-list.artnr = vhp.h-bill-line.artnr
        art-list.departement = vhp.h-bill-line.departement
        art-list.bezeich = vhp.h-bill-line.bezeich
        art-list.epreis = vhp.h-bill-line.epreis
        art-list.rechnr = vhp.h-bill-line.rechnr 
        art-list.tischnr = vhp.h-bill-line.tischnr 
        art-list.zeit = vhp.h-bill-line.zeit
        art-list.kellner-nr = vhp.h-bill-line.kellner-nr 
        art-list.bill-datum = vhp.h-bill-line.bill-datum 
        art-list.sysdate = vhp.h-bill-line.sysdate
        art-list.waehrungsnr = vhp.h-bill-line.waehrungsnr
        art-list.betriebsnr = vhp.h-bill-line.betriebsnr
      . 
    END.
    ASSIGN
      art-list.anzahl = art-list.anzahl + vhp.h-bill-line.anzahl 
      art-list.betrag = art-list.betrag + vhp.h-bill-line.betrag 
      art-list.nettobetrag = art-list.nettobetrag + vhp.h-bill-line.nettobetrag
    . 
  END. 
 
  FOR EACH art-list: 
    IF art-list.anzahl = 0 AND ROUND(art-list.betrag, 0) = 0 
      THEN DELETE art-list. 
  END. 
 
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
    AND vhp.h-bill-line.departement = dept EXCLUSIVE-LOCK: 
    DELETE vhp.h-bill-line. 
  END. 
  RELEASE vhp.h-bill-line.
 
  FOR EACH art-list: 
    ASSIGN
        amount     = 0
        pos-anz    = art-list.anzahl
    .
    IF pos-anz LT 0 THEN pos-anz = - pos-anz.
    splitamount = ROUND(art-list.betrag / pos-anz, price-decimal).

    DO i = 1 TO pos-anz: 
      IF i LT pos-anz THEN amount = splitamount.
      ELSE amount = ROUND(art-list.betrag - amount * (pos-anz - 1), price-decimal).
      CREATE vhp.h-bill-line. 
      ASSIGN
        vhp.h-bill-line.steuercode = 9999
        vhp.h-bill-line.artnr = art-list.artnr
        vhp.h-bill-line.departement = art-list.departement
        vhp.h-bill-line.bezeich = art-list.bezeich
        vhp.h-bill-line.rechnr = art-list.rechnr
        vhp.h-bill-line.tischnr = art-list.tischnr 
        vhp.h-bill-line.zeit = art-list.zeit
        vhp.h-bill-line.kellner-nr = art-list.kellner-nr 
        vhp.h-bill-line.epreis = art-list.epreis
        vhp.h-bill-line.betrag = amount
        vhp.h-bill-line.nettobetrag = ROUND(art-list.nettobetrag / art-list.anzahl, price-decimal) 
        vhp.h-bill-line.bill-datum = art-list.bill-datum 
        vhp.h-bill-line.sysdate = art-list.sysdate
        vhp.h-bill-line.waehrungsnr = art-list.waehrungsnr
        vhp.h-bill-line.betriebsnr  = art-list.betriebsnr
      .
      IF art-list.anzahl GT 0 THEN vhp.h-bill-line.anzahl = 1. 
      ELSE vhp.h-bill-line.anzahl = - 1. 
      FIND CURRENT vhp.h-bill-line NO-LOCK. 
    END. 
  END. 
 
  FOR EACH art-list: 
    DELETE art-list. 
  END. 
END. 

