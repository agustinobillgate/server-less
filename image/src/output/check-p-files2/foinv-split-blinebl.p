
DEF INPUT PARAMETER split-amount  AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER user-init     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER price-decimal AS INTEGER NO-UNDO.
DEF INPUT PARAMETER rec-id        AS INTEGER NO-UNDO.

FIND FIRST bill-line WHERE RECID(bill-line) = rec-id.
RUN split-bill-line.

PROCEDURE split-bill-line: 
DEFINE VARIABLE fact AS DECIMAL    NO-UNDO. 
DEFINE VARIABLE epreis AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE amount AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE famount AS DECIMAL NO-UNDO. 
DEFINE BUFFER bline FOR bill-line. 
 
  ASSIGN
    fact    = split-amount / bill-line.betrag
    epreis  = bill-line.epreis
    amount  = bill-line.betrag 
    famount = bill-line.fremdwbetrag
  . 
 
  CREATE billjournal. 
  ASSIGN 
    billjournal.rechnr = bill-line.rechnr 
    billjournal.artnr = bill-line.artnr 
    billjournal.anzahl = - bill-line.anzahl 
    billjournal.fremdwaehrng = - bill-line.fremdwbetrag 
    billjournal.betrag = - bill-line.betrag 
    billjournal.bezeich = bill-line.bezeich 
    billjournal.zinr = bill-line.zinr 
    billjournal.departement = bill-line.departement 
    billjournal.epreis = bill-line.epreis 
    billjournal.zeit = TIME 
    billjournal.userinit = user-init 
    billjournal.bill-datum = bill-line.bill-datum. 
 
  FIND CURRENT bill-line EXCLUSIVE-LOCK. 
  ASSIGN 
    bill-line.sysdate   = TODAY 
    bill-line.zeit      = TIME 
    bill-line.userinit  = user-init 
    bill-line.epreis    = ROUND(bill-line.epreis * (1 - fact), price-decimal) 
    bill-line.betrag    = bill-line.betrag - split-amount 
    bill-line.fremdwbetrag = ROUND(bill-line.fremdwbetrag * (1 - fact), 6). 
  
  IF SUBSTR(bill-line.bezeich, LENGTH(bill-line.bezeich), 1) NE "&" THEN 
    bill-line.bezeich = bill-line.bezeich + "&". 
  FIND CURRENT bill-line NO-LOCK. 
 
  CREATE bline. 
  BUFFER-copy bill-line TO bline. 
  ASSIGN 
    bline.epreis = ROUND(epreis * fact, price-decimal) 
    bline.betrag = split-amount 
    bline.fremdwbetrag = ROUND(famount * fact, 6). 
  FIND CURRENT bline NO-LOCK. 
 
  CREATE billjournal. 
  ASSIGN 
    billjournal.rechnr      = bill-line.rechnr 
    billjournal.artnr       = bill-line.artnr 
    billjournal.anzahl      = bill-line.anzahl 
    billjournal.fremdwaehrng = bill-line.fremdwbetrag 
    billjournal.betrag      = bill-line.betrag 
    billjournal.bezeich     = bill-line.bezeich 
    billjournal.zinr        = bill-line.zinr 
    billjournal.departement = bill-line.departement 
    billjournal.zeit        = TIME 
    billjournal.userinit    = user-init 
    billjournal.bill-datum  = bill-line.bill-datum. 
 
  CREATE billjournal. 
  ASSIGN 
    billjournal.rechnr       = bline.rechnr 
    billjournal.artnr        = bline.artnr 
    billjournal.anzahl       = bline.anzahl 
    billjournal.fremdwaehrng = bline.fremdwbetrag 
    billjournal.betrag       = bline.betrag 
    billjournal.bezeich      = bline.bezeich 
    billjournal.zinr         = bline.zinr 
    billjournal.departement  = bline.departement 
    billjournal.zeit         = TIME 
    billjournal.userinit     = user-init 
    billjournal.bill-datum   = bline.bill-datum. 
 
END. 
 
