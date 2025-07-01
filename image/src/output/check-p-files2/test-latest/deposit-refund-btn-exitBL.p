
DEF TEMP-TABLE t-reservation    LIKE reservation.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resnr          AS INT.
DEF INPUT  PARAMETER artnr          AS INT.
DEF INPUT  PARAMETER payment        LIKE reservation.depositbez.
DEF INPUT  PARAMETER deposit-pay    AS DECIMAL.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER depoart        AS INT.
DEF INPUT  PARAMETER depobezeich    AS CHAR.
DEF OUTPUT PARAMETER balance        AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-reservation.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "deposit-refund". 

FIND FIRST artikel WHERE artikel.departement = 0 
    AND (artart = 6 OR artart = 7) 
    AND artikel.activeflag
    AND artikel.artnr = artnr.
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK. 
FIND CURRENT reservation EXCLUSIVE-LOCK. 
IF reservation.depositbez = 0 THEN RUN deposit-payment1. 
ELSE RUN deposit-payment2. 
FIND CURRENT reservation NO-LOCK.
CREATE t-reservation.
BUFFER-COPY reservation TO t-reservation.

PROCEDURE deposit-payment1: 
DEFINE VARIABLE bill-date AS DATE. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  bill-date = htparam.fdate. 
 
  ASSIGN 
    reservation.depositbez = reservation.depositbez - payment 
    reservation.zahldatum = ? 
    reservation.zahlkonto = 0. 
 
  /**
  balance = reservation.depositgef - reservation.depositbez. 
  DISP reservation.depositbez reservation.zahldatum 
       balance WITH FRAME frame1. 
  PROCESS EVENTS.
  **/
 
  FIND FIRST umsatz WHERE umsatz.departement = 0 
    AND umsatz.artnr = artikel.artnr 
    AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    CREATE umsatz. 
    umsatz.artnr = artikel.artnr. 
    umsatz.datum = bill-date. 
  END. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  umsatz.betrag = umsatz.betrag + deposit-pay. 
  RELEASE umsatz. 
 
  CREATE billjournal. 
  billjournal.artnr = artikel.artnr. 
  billjournal.anzahl = 1. 
  billjournal.betrag = deposit-pay. 
  billjournal.bezeich = artikel.bezeich 
    + "  " + STRING(reservation.resnr). 
  billjournal.epreis = 0. 
  billjournal.zeit = time. 
  billjournal.userinit = user-init. 
  billjournal.bill-datum = bill-date. 
  FIND CURRENT billjournal NO-LOCK. 
 
  FIND FIRST umsatz WHERE umsatz.artnr = depoart 
    AND umsatz.departement = 0 
    AND umsatz.datum = bill-date NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    create umsatz. 
    umsatz.artnr = depoart. 
    umsatz.datum = bill-date. 
  END. 
  umsatz.betrag = umsatz.betrag - deposit-pay. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  FIND CURRENT umsatz NO-LOCK. 
 
  create billjournal. 
  billjournal.artnr = depoart. 
  billjournal.anzahl = 1. 
/*  billjournal.fremdwaehrng = - foreign-payment. */ 
  billjournal.betrag = - deposit-pay. 
  billjournal.bezeich =  depobezeich 
    + "  " + STRING(reservation.resnr). 
  billjournal.epreis = 0. 
  billjournal.billjou-ref = artikel.artnr. 
  billjournal.zeit = time. 
  billjournal.userinit = user-init. 
  billjournal.bill-datum = bill-date. 
  FIND CURRENT billjournal NO-LOCK. 
 
  IF artikel.artart = 7 THEN 
  DO: 
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    create debitor. 
    ASSIGN 
      debitor.artnr        = artikel.artnr 
      debitor.gastnr       = reservation.gastnr 
      debitor.gastnrmember = reservation.gastnr 
      debitor.saldo        = - deposit-pay 
      debitor.transzeit    = TIME 
      debitor.rgdatum      = bill-date 
      debitor.bediener-nr  = bediener.nr 
      debitor.name         = reservation.name. 
    RELEASE debitor. 
  END. 
 
END. 
 
PROCEDURE deposit-payment2: 
DEFINE VARIABLE bill-date AS DATE. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  bill-date = htparam.fdate. 
 
  IF payment GT reservation.depositbez2 THEN 
  DO: 
    reservation.depositbez = reservation.depositbez - payment 
      + reservation.depositbez2. 
    reservation.depositbez2 = 0. 
  END. 
  ELSE reservation.depositbez2 = reservation.depositbez2 - payment. 
  reservation.zahldatum = ?. 
  reservation.zahldatum2 = ?. 
  reservation.zahlkonto2 = 0. 
 
  /**
  balance = reservation.depositgef - reservation.depositbez 
          - reservation.depositbez2. 
  DISP reservation.depositbez2 reservation.zahldatum2 
       balance WITH FRAME frame1. 
  PROCESS EVENTS. 
  **/

  FIND FIRST umsatz WHERE umsatz.departement = 0 
    AND umsatz.artnr = artikel.artnr 
    AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    CREATE umsatz. 
    umsatz.artnr = artikel.artnr. 
    umsatz.datum = bill-date. 
  END. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  umsatz.betrag = umsatz.betrag + deposit-pay. 
  RELEASE umsatz. 
 
  CREATE billjournal. 
  billjournal.artnr = artikel.artnr. 
  billjournal.anzahl = 1. 
  billjournal.betrag = deposit-pay. 
  billjournal.bezeich = artikel.bezeich 
    + " [" + translateExtended ("Refund",lvCAREA,"") + " #" 
    + STRING(reservation.resnr) + "]". 
  billjournal.epreis = 0. 
  billjournal.zeit = time. 
  billjournal.userinit = user-init. 
  billjournal.bill-datum = bill-date. 
  billjournal.billjou-ref = reservation.resnr. 
  FIND CURRENT billjournal NO-LOCK. 
 
  FIND FIRST umsatz WHERE umsatz.artnr = depoart 
    AND umsatz.departement = 0 
    AND umsatz.datum = bill-date NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    CREATE umsatz. 
    umsatz.artnr = depoart. 
    umsatz.datum = bill-date. 
  END. 
  umsatz.betrag = umsatz.betrag - deposit-pay. 
  umsatz.anzahl = umsatz.anzahl + 1. 
  FIND CURRENT umsatz NO-LOCK. 
 
  create billjournal. 
  billjournal.artnr = depoart. 
  billjournal.anzahl = 1. 
/*  billjournal.fremdwaehrng = - foreign-payment. */ 
  billjournal.betrag = - deposit-pay. 
  billjournal.bezeich =  depobezeich 
    + "  " + STRING(reservation.resnr). 
  billjournal.epreis = 0. 
  billjournal.zeit = time. 
  billjournal.userinit = user-init. 
  billjournal.bill-datum = bill-date. 
  FIND CURRENT billjournal NO-LOCK. 
 
  IF artikel.artart = 7 THEN 
  DO: 
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    create debitor. 
    ASSIGN 
      debitor.artnr        = artikel.artnr 
      debitor.gastnr       = reservation.gastnr 
      debitor.gastnrmember = reservation.gastnr 
      debitor.saldo        = - deposit-pay 
      debitor.transzeit    = TIME 
      debitor.rgdatum      = bill-date 
      debitor.bediener-nr  = bediener.nr 
      debitor.name         = reservation.NAME. 
    debitor.vesrcod        = translateExtended ("Deposit Refund - ResNo:",lvCAREA,"") 
                             + " " + STRING(resnr). 
    RELEASE debitor. 
  END. 
 
END. 


