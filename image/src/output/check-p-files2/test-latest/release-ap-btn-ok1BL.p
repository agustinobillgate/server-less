
DEFINE TEMP-TABLE pay-list 
  FIELD datum   LIKE l-kredit.rgdatum COLUMN-LABEL "Pay-Date" 
  FIELD saldo   LIKE l-kredit.saldo   COLUMN-LABEL "Paid Amount" 
  FIELD bezeich LIKE artikel.bezeich 
  FIELD s-recid AS INTEGER. 

DEF INPUT  PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER bill-no     AS CHAR.
DEF INPUT  PARAMETER datum       AS DATE.
DEF INPUT  PARAMETER saldo       AS DECIMAL.
DEF OUTPUT PARAMETER msg-str     AS CHAR.
DEF OUTPUT PARAMETER msg-str2    AS CHAR.
DEF OUTPUT PARAMETER rec-id      AS INT.
DEF OUTPUT PARAMETER TABLE FOR pay-list.
  
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-gcPI".

DEFINE VARIABLE tot-anz AS INTEGER INITIAL 0. 
DEFINE buffer debt FOR l-kredit. 

  FIND FIRST l-kredit WHERE l-kredit.lscheinnr = bill-no 
    AND l-kredit.rgdatum = datum 
    AND l-kredit.saldo = saldo 
    AND l-kredit.zahlkonto = 0 
    AND l-kredit.counter NE 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-kredit THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("No such A/P record found!",lvCAREA,"").
    /*MTAPPLY "entry" TO bill-no. */
    RETURN NO-APPLY. 
  END. 
  IF l-kredit.counter = 0 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("This A/P has no payment record!",lvCAREA,"").
    /*MTAPPLY "entry" TO bill-no. */
    RETURN NO-APPLY. 
  END. 
 
  FOR EACH pay-list: 
    delete pay-list. 
  END. 
  FOR EACH debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto GT 0 
    NO-LOCK BY debt.rgdatum: 
    FIND FIRST artikel WHERE artikel.artnr = debt.zahlkonto NO-LOCK. 
    create pay-list. 
    pay-list.datum = debt.rgdatum. 
    pay-list.saldo = debt.saldo. 
    pay-list.bezeich = artikel.bezeich. 
    pay-list.s-recid = RECID(debt). 
    tot-anz = tot-anz + 1. 
  END. 
  OPEN QUERY q1 FOR EACH pay-list. 
 
  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK. 
  IF tot-anz GT 1 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Double click the payment record to cancel the payment.",lvCAREA,"")
            + CHR(10)
            + translateExtended ("Supplier Name :",lvCAREA,"") + " " + l-lieferant.firma.
    /*MTAPPLY "entry" TO bill-no . */
    RETURN NO-APPLY. 
  END. 

  FIND FIRST htparam WHERE paramnr = 1118 NO-LOCK.  /* LAST A/P Transfer DATE */ 
  FIND FIRST debt WHERE debt.counter = l-kredit.counter AND debt.opart GE 1 
    AND debt.zahlkonto NE 0 AND debt.rgdatum LE htparam.fdate
    NO-LOCK NO-ERROR.
  IF AVAILABLE debt THEN
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("A/P Payment transferred to G/L - Cancel no longer possible.",lvCAREA,"").
    /*MTAPPLY "entry" TO bill-no. */
    RETURN NO-APPLY. 
  END.


  msg-str2 = msg-str2 + CHR(2) + "&Q"
           + translateExtended ("Do you really want to release ALL A/P payment record(s).",lvCAREA,"")
           + CHR(10)
           + translateExtended ("Supplier Name :",lvCAREA,"") + " " + l-lieferant.firma + "?".
  rec-id = RECID(l-kredit).
    
