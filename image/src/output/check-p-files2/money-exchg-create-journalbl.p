

DEFINE TEMP-TABLE s-list 
    FIELD wahrnr    AS INTEGER 
    FIELD dept      AS INTEGER FORMAT ">9" LABEL "Dept" 
    FIELD artnr     AS INTEGER FORMAT ">>>9" LABEL "ArtNo" 
    FIELD bezeich   AS CHAR FORMAT "x(31)" LABEL "Description" 
    FIELD zinr      AS CHAR FORMAT "x(5)" LABEL "RmNo" 
    FIELD anzahl    AS INTEGER FORMAT ">,>>9" LABEL "Qty" 
    FIELD preis     AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "Foreign Amount" 
    FIELD we-buy    AS DECIMAL FORMAT ">>>>,>>>,>>9.99" LABEL "We &we-buy" 
    FIELD we-sell   AS DECIMAL FORMAT ">>>>,>>>,>>9.99" LABEL "We &we-sell" 
    FIELD betrag    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "Local Amount". 

DEF INPUT PARAMETER TABLE FOR s-list.
DEF INPUT PARAMETER room AS CHAR.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER print-flag AS LOGICAL.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER char-455 AS CHAR.

DEFINE VARIABLE i AS INTEGER INITIAL 0. 
DEFINE VARIABLE bill-date AS DATE. 

FIND FIRST htparam WHERE htparam.paramnr = 110 no-lock.   /* bill DATE */ 
bill-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 253 no-lock. /* N/A running */ 
IF htparam.flogical THEN bill-date = bill-date + 1. 
FOR EACH s-list: 
    create billjournal. 
    ASSIGN 
      billjournal.rechnr = 0 
      billjournal.artnr = s-list.artnr 
      billjournal.anzahl = 1 
      billjournal.fremdwaehrng = s-list.preis 
      billjournal.betrag = s-list.betrag 
      billjournal.bezeich = s-list.bezeich 
      billjournal.zinr = room 
      billjournal.departement = 0 
      billjournal.zeit = time + i 
      billjournal.userinit = user-init 
      billjournal.bill-datum = bill-date 
      billjournal.waehrungsnr = s-list.wahrnr. 
    FIND CURRENT billjournal NO-LOCK. 
    i = i + 1. 
 
    FIND FIRST umsatz WHERE umsatz.artnr = s-list.artnr AND umsatz.departement 
      = 0 AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE umsatz THEN 
    DO: 
      create umsatz. 
      ASSIGN 
        umsatz.artnr = s-list.artnr 
        umsatz.datum = bill-date 
        umsatz.departement = 0. 
    END. 
    ASSIGN 
      umsatz.betrag = umsatz.betrag + s-list.betrag 
      umsatz.anzahl = umsatz.anzahl + 1. 
    FIND CURRENT umsatz NO-LOCK. 
END. 


IF print-flag THEN 
DO:
  FIND FIRST htparam WHERE paramnr = 455 NO-LOCK NO-ERROR.
  IF AVAILABLE htparam AND htparam.fchar NE "" THEN
      ASSIGN
      fl-code = 1
      char-455 = htparam.fchar.
  ELSE  fl-code = 2.
END.
