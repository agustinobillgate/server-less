DEFINE TEMP-TABLE pay-list 
  FIELD artnr LIKE artikel.artnr 
  FIELD paynr LIKE Artikel.artnr 
  FIELD datum LIKE debitor.rgdatum 
  FIELD saldo LIKE debitor.saldo FORMAT "->,>>>,>>>,>>9.99" 
  FIELD bezeich LIKE artikel.bezeich 
  FIELD s-recid AS INTEGER. 


DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER artnr          AS INTEGER.
DEF INPUT  PARAMETER bill-no        AS INTEGER.
DEF INPUT  PARAMETER datum          AS DATE.
DEF INPUT  PARAMETER saldo          AS DECIMAL.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER msg-str2       AS CHAR.
DEF OUTPUT PARAMETER rec-id-debitor AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR pay-list.


{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "release-ar". 

DEFINE buffer debt FOR debitor.
DEFINE BUFFER art1 FOR artikel.
DEFINE VARIABLE tot-anz AS INTEGER INITIAL 0.
  
  FIND FIRST debitor WHERE debitor.artnr = artnr 
    AND debitor.rechnr = bill-no 
    AND debitor.rgdatum = datum 
    AND debitor.saldo = saldo 
    AND debitor.opart = 2 
    AND debitor.zahlkonto = 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE debitor THEN 
  DO: 
    FIND FIRST debt WHERE debt.artnr = artnr 
      AND debt.rechnr = bill-no AND debt.opart = 1 
      AND debt.zahlkonto GT 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE debt THEN FIND FIRST debitor WHERE debitor.artnr = artnr 
      AND debitor.rechnr = bill-no AND debitor.rgdatum = datum 
      AND debitor.saldo = saldo AND debitor.opart = 0 
      AND debitor.zahlkonto = 0 NO-LOCK NO-ERROR. 
  END. 
  IF NOT AVAILABLE debitor THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("No such A/R record found!",lvCAREA,"").
    /*MTAPPLY "entry" TO artnr. */
    RETURN NO-APPLY. 
  END. 
 
  FOR EACH pay-list: 
    delete pay-list. 
  END. 
  FOR EACH debt WHERE debt.counter = debitor.counter AND debt.zahlkonto GT 0 
    NO-LOCK BY debt.rgdatum: 
    FIND FIRST artikel WHERE artikel.artnr = debt.zahlkonto
        AND artikel.departement EQ 0 NO-LOCK. /*FDL Sept 10, 2023 => Ticket 365EB1 - Dept 0*/
    create pay-list. 
    pay-list.datum = debt.rgdatum. 
    pay-list.artnr = debt.artnr. 
    pay-list.paynr = artikel.artnr. 
    pay-list.saldo = debt.saldo. 
    pay-list.bezeich = artikel.bezeich. 
    pay-list.s-recid = RECID(debt). 
    tot-anz = tot-anz + 1. 
  END. 
  /*MTOPEN QUERY q1 FOR EACH pay-list. */
 
  FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
  IF tot-anz GT 1 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Double click the payment record to cancel the payment",lvCAREA,"")
            + CHR(10)
            + translateExtended ("Bill Receiver : ",lvCAREA,"") + guest.name + ", " + guest.vorname1 + " "
            + guest.anrede1 + guest.anredefirma.
    /*MTAPPLY "entry" TO artnr. */
    RETURN NO-APPLY. 
  END. 
 
  FIND FIRST art1 WHERE art1.artnr = pay-list.paynr AND art1.departement = 0 
      NO-LOCK. 
  IF art1.artart = 2 OR art1.artart = 7 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Cancel payment not possible for this type of payment article.",lvCAREA,"").
    /*MTAPPLY "entry" TO artnr. */
    RETURN NO-APPLY. 
  END. 

  FIND FIRST htparam WHERE paramnr = 1014 NO-LOCK.  /* LAST A/R Transfer DATE */ 
  FIND FIRST debt WHERE debt.counter = debitor.counter AND debt.opart GE 1 
    AND debt.zahlkonto NE 0 AND debt.rgdatum LE htparam.fdate
    NO-LOCK NO-ERROR.
  IF AVAILABLE debt THEN
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("A/R Payment transferred to G/L - Cancel no longer possible.",lvCAREA,"").
    /*MTAPPLY "entry" TO artnr. */
    RETURN NO-APPLY. 
  END.


  msg-str2 = msg-str2 + CHR(2) + "&Q"
           + translateExtended ("Do you really want to release the A/R payment record",lvCAREA,"")
           + CHR(10)
           + translateExtended ("Bill Receiver : ",lvCAREA,"") + guest.name + ", " + guest.vorname1 + " "
           + guest.anrede1 + guest.anredefirma + "?".

  rec-id-debitor = RECID(debitor).
