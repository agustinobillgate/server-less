.
DEF INPUT PARAMETER pvILanguage     AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER resnr           AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER artnr           AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER depositgef      AS DECIMAL          NO-UNDO.
DEF INPUT PARAMETER payment         AS DECIMAL          NO-UNDO.
DEF INPUT PARAMETER deposit-exrate  AS DECIMAL          NO-UNDO.
DEF INPUT PARAMETER voucher-str     AS CHAR             NO-UNDO.
DEF INPUT PARAMETER user-init       AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER error-flag     AS LOGICAL INIT NO  NO-UNDO.
DEF OUTPUT PARAMETER deposit-pay    AS DECIMAL          NO-UNDO.

DEFINE VARIABLE exchg-rate          AS DECIMAL NO-UNDO INIT 1. 
DEFINE VARIABLE foreign-payment     AS DECIMAL NO-UNDO.
DEFINE VARIABLE local-payment       AS DECIMAL NO-UNDO.
DEFINE VARIABLE price-decimal       AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart             AS INTEGER NO-UNDO. 
DEFINE VARIABLE deposit-balance     AS DECIMAL.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "deposit-pay". 

FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
  AND artikel.departement = 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE artikel OR artikel.artart NE 5 THEN
DO:
  ASSIGN
    error-flag = YES
    msg-str = translateExtended ("Deposit article not defined.",lvCAREA,"")
  .
  RETURN. 
END.
ASSIGN depoart = artikel.artnr.

FIND FIRST artikel WHERE artikel.departement = 0 AND 
  (artart = 6 OR artart = 7) AND artikel.artnr = artnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel THEN 
DO: 
  ASSIGN
    error-flag = YES
    msg-str = translateExtended ("Payment article not defined.",lvCAREA,"")
  .
  RETURN. 
END. 

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 

RUN calculate-amount(INPUT-OUTPUT payment). 
/*DODY 090124 change query pentest
FIND FIRST reservation WHERE reservation.resnr = resnr EXCLUSIVE-LOCK. 
IF reservation.depositbez = 0 THEN RUN deposit-payment1. 
ELSE RUN deposit-payment2. 
FIND CURRENT reservation NO-LOCK. 
*/

FIND FIRST reservation WHERE reservation.resnr = resnr EXCLUSIVE-LOCK.
IF AVAILABLE reservation THEN
DO:
    IF depositbez NE 0 THEN     /*FDL Feb 19, 2024 => Ticket 2EDE58*/
    DO:
        IF reservation.depositbez2 NE 0 THEN 
        DO:
            deposit-balance = depositgef - reservation.depositbez - reservation.depositbez2.
        END.
        ELSE deposit-balance = depositgef - reservation.depositbez.
        IF deposit-balance EQ 0 THEN RETURN.
    END.

    IF reservation.depositbez = 0 THEN RUN deposit-payment1. 
    ELSE RUN deposit-payment2. 
    FIND CURRENT reservation NO-LOCK. 
END.
/*end dody*/

PROCEDURE calculate-amount: 
DEFINE INPUT-OUTPUT PARAMETER amount AS DECIMAL. 
DEFINE VARIABLE avrg-kurs       AS DECIMAL INIT 1 NO-UNDO. 
DEFINE VARIABLE pay-exrate      AS DECIMAL INIT 1 NO-UNDO.
  
  IF artikel.pricetab THEN
  DO:
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
      NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN 
      ASSIGN pay-exrate = waehrung.ankauf / waehrung.einheit.
  END.

  deposit-pay = - ROUND(amount * pay-exrate / deposit-exrate, 2).

  IF artikel.pricetab THEN  /* foreign currency */ 
  ASSIGN 
    foreign-payment = amount
    amount          = amount * exchg-rate 
    amount          = ROUND(amount, price-decimal)
  . 
  ELSE foreign-payment = amount / exchg-rate. 
  local-payment = amount.
END. 

PROCEDURE deposit-payment1: 
DEFINE VARIABLE bill-date   AS DATE    NO-UNDO. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  bill-date = htparam.fdate. 

  ASSIGN 
    reservation.depositgef = depositgef
    reservation.depositbez = deposit-pay
    reservation.zahldatum = bill-date 
    reservation.zahlkonto = artikel.artnr
  . 
  RUN create-journal(bill-date). 
END. 
 
PROCEDURE deposit-payment2: 
DEFINE VARIABLE bill-date AS DATE NO-UNDO. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  bill-date = htparam.fdate. 
 
  ASSIGN 
    reservation.depositgef = depositgef
    reservation.depositbez2 = reservation.depositbez2 + deposit-pay
    reservation.zahldatum2 = bill-date 
    reservation.zahlkonto2 = artikel.artnr
  . 
  RUN create-journal(bill-date). 
END. 

PROCEDURE create-journal: 
  DEFINE INPUT PARAMETER bill-date AS DATE. 
  IF artikel.artart = 2 OR artikel.artart = 7 THEN 
  DO: 
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    CREATE debitor. 
    ASSIGN 
      debitor.artnr        = artikel.artnr 
      debitor.gastnr       = reservation.gastnr 
      debitor.gastnrmember = reservation.gastnr 
      debitor.saldo        = - local-payment 
      debitor.vesrdep      = - foreign-payment 
      debitor.transzeit    = TIME 
      debitor.rgdatum      = bill-date 
      debitor.bediener-nr  = bediener.nr 
      debitor.name         = reservation.name. 
    debitor.vesrcod        = translateExtended ("Deposit Payment - ResNo:",lvCAREA,"") 
                             + " " + STRING(resnr). 
    IF voucher-str NE "" THEN debitor.vesrcod = debitor.vesrcod
        + "; " + voucher-str. 
    RELEASE debitor. 
  END. 
 
/* payment article */
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
    umsatz.betrag = umsatz.betrag + local-payment. 
  RELEASE umsatz. 
 
  CREATE billjournal. 
  ASSIGN 
    billjournal.artnr = artikel.artnr 
    billjournal.anzahl = 1 
    billjournal.fremdwaehrng = foreign-payment 
    billjournal.epreis = 0 
    billjournal.zeit = TIME 
    billjournal.userinit = user-init 
    billjournal.bill-datum = bill-date 
    billjournal.billjou-ref = reservation.resnr 
  . 
  billjournal.bezeich = artikel.bezeich + "[" 
    + translateExtended("Deposit",lvCAREA,"") + " #" + STRING(reservation.resnr) 
    + "]" + voucher-str. 
  /*IF artikel.pricetab THEN billjournal.betrag = foreign-payment. 
  ELSE billjournal.betrag = local-payment. */
  /*by LN May 27 08*/
  billjournal.betrag = local-payment.
  FIND CURRENT billjournal NO-LOCK. 
 
  FIND FIRST umsatz WHERE umsatz.artnr = depoart
    AND umsatz.departement = 0 
    AND umsatz.datum = bill-date NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    CREATE umsatz. 
    ASSIGN
      umsatz.artnr = depoart
      umsatz.datum = bill-date
    . 
  END. 
  ASSIGN
    umsatz.betrag = umsatz.betrag - local-payment
    umsatz.anzahl = umsatz.anzahl + 1
  . 
 
  CREATE billjournal. 
  ASSIGN 
    billjournal.artnr = depoart 
    billjournal.anzahl = 1 
    billjournal.fremdwaehrng = - foreign-payment 
    billjournal.betrag = - local-payment 
    billjournal.bezeich =  artikel.bezeich 
      + " [#" + STRING(reservation.resnr) + " " + artikel.bezeich + "]" + voucher-str /*ITA 010713*/ . . 
    billjournal.epreis = 0. 
    billjournal.zeit = TIME. 
    billjournal.billjou-ref = artikel.artnr. /* payment ArtNo */ 
    billjournal.userinit = user-init. 
    billjournal.bill-datum = bill-date. 
  FIND CURRENT billjournal NO-LOCK. 
 
END. 
 
