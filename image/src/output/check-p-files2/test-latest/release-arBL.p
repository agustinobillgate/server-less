
DEF INPUT  PARAMETER rec-id-debitor AS INT.
DEF INPUT  PARAMETER saldo          AS DECIMAL.
DEF INPUT  PARAMETER bill-no        AS INTEGER.
DEF INPUT  PARAMETER artnr          AS INTEGER.
DEF INPUT  PARAMETER bediener-nr    AS INTEGER.
DEF INPUT  PARAMETER bediener-userinit AS CHAR.

DEFINE buffer debt FOR debitor. 
DEFINE VARIABLE counter AS INTEGER. 
DEFINE VARIABLE pay-amount AS DECIMAL.
DEFINE VARIABLE debt-no AS INT.

FIND FIRST debitor WHERE RECID(debitor) = rec-id-debitor.
  DO TRANSACTION: 
    counter = debitor.counter. 
    
    FOR EACH debt WHERE debt.counter = counter 
      AND debt.opart GE 1 AND debt.zahlkonto NE 0: 
      FIND FIRST umsatz WHERE umsatz.departement = 0 AND 
        umsatz.artnr = debt.zahlkonto AND umsatz.datum = debt.rgdatum 
        EXCLUSIVE-LOCK NO-ERROR. 
      pay-amount = debt.saldo.
      debt-no = debt.zahlkonto.
      IF AVAILABLE umsatz THEN 
      DO: 
        umsatz.anzahl = umsatz.anzahl - 1. 
        umsatz.betrag = umsatz.betrag - debt.saldo. 
        release umsatz. 
      END. 
      delete debt. 
    END. 
    FIND CURRENT debitor EXCLUSIVE-LOCK. 
    debitor.opart = 0. 
    debitor.counter = 0. 
    FIND CURRENT debitor NO-LOCK. 
 
    FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
    create billjournal. 
    billjournal.rechnr = bill-no. 
    billjournal.bill-datum = htparam.fdate. 
    billjournal.artnr = artnr. 
    billjournal.bezeich = "Release A/R Payment " + STRING(saldo) 
                        + ";" + STRING(pay-amount) + ";" + STRING(debt-no).  /* Rulita C4D1F8 14/07/2022| add debt.saldo for pay amount cancelation A/R*/
    billjournal.zinr = debitor.zinr. 
    billjournal.anzahl = 1. 
    billjournal.zeit = time. 
    billjournal.bediener-nr = bediener-nr. 
    billjournal.userinit = bediener-userinit. 

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
                                 + " | Pay Amount: " + STRING(pay-amount)               /* Rulita C4D1F8 14/07/2022| add debt.saldo for pay amount cancelation A/R*/ 
                                 + " | Debt No : " + STRING(debt-no)                    /* Rulita */
                                 + " | Bill Receiver : "+ guest.NAME 
                                 + "," + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma + "?". 
       res-history.action      = "Cancel A/R Payment".
    
     /*End Agung*/

  END. 
