
DEF INPUT  PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER pay-list-paynr AS INT.
DEF INPUT  PARAMETER pay-list-s-recid AS INT.
DEF INPUT  PARAMETER bediener-nr AS INT.
DEF INPUT  PARAMETER bediener-userinit AS CHAR.

DEF INPUT  PARAMETER artnr          AS INTEGER.
DEF INPUT  PARAMETER bill-no        AS INTEGER.
DEF INPUT  PARAMETER datum          AS DATE.
DEF INPUT  PARAMETER saldo          AS DECIMAL.


DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "release-ar".

DEFINE VARIABLE i-counter AS INTEGER. 
DEFINE BUFFER debt  FOR debitor. 
DEFINE BUFFER art1  FOR artikel.
DEFINE VARIABLE pay-amount AS DECIMAL.
DEFINE VARIABLE debt-no AS INT.

FIND FIRST htparam WHERE paramnr = 1014 NO-LOCK.  /* LAST A/R Transfer DATE */ 
FIND FIRST debt WHERE RECID(debt) = pay-list-s-recid NO-LOCK NO-ERROR.
IF AVAILABLE debt AND debt.rgdatum LE htparam.fdate THEN
DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("A/R Payment transferred to G/L - Cancel no longer possible.",lvCAREA,"").
    /*MTAPPLY "entry" TO artnr.*/
    RETURN NO-APPLY. 
END.

FIND FIRST art1 WHERE art1.artnr = pay-list-paynr AND art1.departement = 0 NO-LOCK. 
IF art1.artart = 2 OR art1.artart = 7 THEN 
DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Cancel payment not possible for this type of payment article.",lvCAREA,"").
    /*MTAPPLY "entry" TO artnr.*/
    RETURN NO-APPLY.
END. 
 
FIND FIRST debitor WHERE debitor.artnr = debt.artnr 
    AND debitor.counter = debt.counter 
    AND debitor.zahlkonto = 0 NO-LOCK NO-ERROR.

IF AVAILABLE debitor THEN
DO TRANSACTION: 
    ASSIGN i-counter = debitor.counter. 
    pay-amount = debt.saldo.
    debt-no = debt.zahlkonto.
    FIND CURRENT debt EXCLUSIVE-LOCK. 
    FIND FIRST umsatz WHERE umsatz.departement = 0 AND 
      umsatz.artnr = debt.zahlkonto AND umsatz.datum = debt.rgdatum 
      EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE umsatz THEN 
    DO: 
      umsatz.anzahl = umsatz.anzahl - 1. 
      umsatz.betrag = umsatz.betrag - debt.saldo. 
      release umsatz. 
    END. 
    DELETE debt. 

    IF AVAILABLE debitor THEN
    DO:
      FIND CURRENT debitor EXCLUSIVE-LOCK. 
      debitor.opart = 0. 
      FIND CURRENT debitor NO-LOCK. 
    END.

    FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
    create billjournal. 
    billjournal.rechnr = bill-no. 
    billjournal.bill-datum = fdate. 
    billjournal.artnr = artnr. 
    billjournal.bezeich = translateExtended ("Release A/R Payment",lvCAREA,"") 
      + " " + STRING(saldo) + ";" + STRING(pay-amount) + ";" + STRING(debt-no).  /* Rulita C4D1F8 14/07/2022| add debt.saldo for pay amount cancelation A/R*/
    billjournal.zinr = debitor.zinr. 
    billjournal.anzahl = 1. 
    billjournal.zeit = time. 
    billjournal.bediener-nr = bediener-nr.
    billjournal.userinit = bediener-userinit.
 
    FOR EACH debt WHERE debt.counter = i-counter 
      AND debt.zahlkonto GT 0 AND debt.opart = 2: 
      debt.opart = 1. 
    END. 

    /*Agung A97715*/
    FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
    CREATE res-history.
    ASSIGN
       res-history.nr          = bediener-nr                                                                                       
       res-history.datum       = TODAY                                                                                               
       res-history.zeit        = TIME                                                                                                
       res-history.aenderung   = "Cancel A/R Payment With Bill No: " + STRING(bill-no) 
                                 + " | Art No: " + STRING(artnr) 
                                 + " | Balance: " + STRING(saldo) 
                                 + " | Pay Amount: " + STRING(pay-amount)               /* Rulita C4D1F8 14/07/2022| add debt.saldo for pay amount cancelation A/R */
                                 + " | Deb N0 : " + STRING(debt-no)                     /* Rulita */
                                 + " | Bill Receiver : "+ guest.NAME 
                                 + "," + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma + "?". 
       res-history.action      = "Cancel A/R Payment".
    
     /*End Agung*/
 
END. 
