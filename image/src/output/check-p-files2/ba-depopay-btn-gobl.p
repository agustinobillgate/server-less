DEFINE INPUT PARAMETER curr-i           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER veran-nr         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER payment          AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER artnr            AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER foreign-payment  AS DECIMAL NO-UNDO. 
DEFINE INPUT PARAMETER depoart          AS INTEGER NO-UNDO. 
DEFINE INPUT PARAMETER depobezeich      AS CHAR    NO-UNDO. 
DEFINE OUTPUT PARAMETER deposit-payment AS DECIMAL NO-UNDO.
DEFINE OUTPUT PARAMETER payment-date    AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER balance         AS DECIMAL NO-UNDO.

DEFINE VARIABLE bill-date AS DATE    NO-UNDO.

RUN deposit-payment(curr-i).

PROCEDURE deposit-payment: 
DEFINE INPUT PARAMETER curr-counter AS INTEGER. 
DEFINE VARIABLE bill-date AS DATE. 
DEFINE VARIABLE i AS INTEGER.
  FIND FIRST htparam WHERE paramnr = 110 USE-INDEX paramnr_ix NO-LOCK. 
  bill-date = htparam.fdate. 

  FIND FIRST bk-veran WHERE bk-veran.veran-nr = veran-nr NO-LOCK NO-ERROR.
  FIND CURRENT bk-veran EXCLUSIVE-LOCK. 
  ASSIGN
    bk-veran.deposit-payment[curr-counter]  = - payment
    bk-veran.payment-date[curr-counter]     = bill-date
    bk-veran.payment-userinit[curr-counter] = user-init
    bk-veran.total-paid                     = 0. 

  DO i = 1 TO 9:
    bk-veran.total-paid = bk-veran.total-paid + bk-veran.deposit-payment[i]. 
  END.

  FIND CURRENT bk-veran NO-LOCK. 
  ASSIGN 
      balance           = bk-veran.deposit - bk-veran.total-paid
      deposit-payment   = bk-veran.deposit-payment[curr-counter]
      payment-date      = bk-veran.payment-date[curr-counter].

 
  RUN create-journal(bill-date). 
END. 
 
PROCEDURE create-journal: 
  DEFINE INPUT PARAMETER bill-date AS DATE. 
  FIND FIRST artikel WHERE artikel.artnr = artnr NO-LOCK NO-ERROR.

  IF artikel.artart = 2 OR artikel.artart = 7 THEN RUN inv-ar(bill-date). 
 
  FIND FIRST umsatz WHERE umsatz.departement = 0 
    AND umsatz.artnr = artikel.artnr 
    AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    CREATE umsatz. 
    ASSIGN 
        umsatz.artnr = artikel.artnr
        umsatz.datum = bill-date. 
  END. 
  ASSIGN 
      umsatz.anzahl = umsatz.anzahl + 1
      umsatz.betrag = umsatz.betrag + payment. 
  RELEASE umsatz.  

  CREATE billjournal. 
  ASSIGN
    billjournal.artnr           = artikel.artnr
    billjournal.anzahl          = 1
    billjournal.fremdwaehrng    = foreign-payment 
    billjournal.bezeich         = artikel.bezeich  + " *BQT" + STRING(bk-veran.veran-nr)
    billjournal.epreis          = 0
    billjournal.zeit            = TIME 
    billjournal.userinit        = user-init 
    billjournal.bill-datum      = bill-date.

  IF artikel.pricetab THEN billjournal.betrag = foreign-payment. 
  ELSE billjournal.betrag = payment. 
  FIND CURRENT billjournal NO-LOCK. 
 
  FIND FIRST umsatz WHERE umsatz.artnr = depoart /*artikel.artnr */
    AND umsatz.departement = 0 
    AND umsatz.datum = bill-date NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    create umsatz. 
    ASSIGN 
      umsatz.departement = 0
      umsatz.artnr       = depoart 
      umsatz.datum       = bill-date. 
  END. 
  ASSIGN 
      umsatz.betrag = umsatz.betrag - payment
      umsatz.anzahl = umsatz.anzahl + 1. 
 
  CREATE billjournal. 
  ASSIGN
    billjournal.artnr = depoart
    billjournal.departement = artikel.departement
    billjournal.billjou-ref = artikel.artnr
    billjournal.anzahl = 1 
    billjournal.fremdwaehrng = - foreign-payment
    billjournal.betrag = - payment
    billjournal.bezeich =  depobezeich + " *BQT" + STRING(bk-veran.veran-nr) 
    billjournal.epreis = 0 
    billjournal.zeit = TIME 
    billjournal.userinit = user-init 
    billjournal.bill-datum = bill-date.
  FIND CURRENT billjournal NO-LOCK.
END. 


PROCEDURE inv-ar: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
  FIND FIRST htparam WHERE paramnr = 997 NO-LOCK. 
  IF NOT htparam.flogical THEN RETURN. 
  DO: 
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR. 
    FIND FIRST artikel WHERE artikel.artnr = artnr NO-LOCK NO-ERROR.
    CREATE debitor. 
    ASSIGN 
        debitor.artnr        = artikel.artnr. 
        debitor.gastnr       = bk-veran.gastnr. 
        debitor.gastnrmember = bk-veran.gastnr. 
        debitor.saldo        = - payment. 
        debitor.transzeit    = time. 
        debitor.rgdatum      = bill-date. 
        debitor.bediener-nr  = bediener.nr. 
        debitor.vesrcod      = "Banquet Deposit Payment". 
        debitor.name         = guest.name + ", " +  guest.vorname1 
                               + " " + guest.anrede1 + guest.anredefirma. 
    RELEASE debitor. 
  END. 
END. 
