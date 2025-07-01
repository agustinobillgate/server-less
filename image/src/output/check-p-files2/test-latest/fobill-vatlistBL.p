DEF TEMP-TABLE bline-vatlist
    FIELD seqnr   AS INTEGER
    FIELD vatnr   AS INTEGER INIT 0
    FIELD bezeich AS CHAR    FORMAT "x(24)"
    FIELD betrag  AS DECIMAL FORMAT "->>>,>>>,>>9.99"
.


DEF INPUT PARAMETER  pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER billNo       AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR bline-vatlist.

/*
DEF VAR  pvILanguage AS INTEGER NO-UNDO.
DEF VAR billno       AS INTEGER NO-UNDO INIT 1.
DEF VAR counter      AS INTEGER NO-UNDO.*/


DEF VARIABLE exchg-rate    AS DECIMAL NO-UNDO.
DEF VARIABLE price-decimal AS INTEGER NO-UNDO. 
DEF VARIABLE curr-billdate AS DATE    NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fo-invoice". 


FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

RUN htpdate.p(110, OUTPUT curr-billdate).

FOR EACH bill-line WHERE bill-line.rechnr = billNo 
    AND bill-line.betrag NE 0 NO-LOCK:
    FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr
        AND artikel.departement = bill-line.departement NO-LOCK.
    IF artikel.artart = 0 OR
       artikel.artart = 1 OR
       artikel.artart = 8 THEN RUN rev-bdown1.
    ELSE IF artikel.artart = 9 THEN 
    DO:
        IF artikel.artgrp = 0 THEN RUN rev-bdown2. 
        ELSE RUN rev-bdown3. 
    END.
END.

/*
FOR EACH bline-vatlist BY bline-vatlist.seqnr
    BY bline-vatlist.vatnr:
    DISP bline-vatlist.
END.*/

PROCEDURE calc-servtaxes:
DEF INPUT PARAMETER artNo    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER deptNo   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER betrag   AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER billdate AS DATE    NO-UNDO.

DEF VARIABLE serv AS DECIMAL    NO-UNDO.
DEF VARIABLE vat  AS DECIMAL    NO-UNDO.
DEF VARIABLE tax  AS DECIMAL    NO-UNDO.
DEF VARIABLE fact AS DECIMAL    NO-UNDO.
DEF VARIABLE vat-bez AS CHAR    NO-UNDO INIT "".
DEF VARIABLE tax-bez AS CHAR    NO-UNDO INIT "".
DEF VARIABLE sc-bez  AS CHAR    NO-UNDO INIT "".
DEF VARIABLE netto   AS DECIMAL NO-UNDO.
DEF VARIABLE vat-amt AS DECIMAL NO-UNDO.
DEF VARIABLE tax-amt AS DECIMAL NO-UNDO.
DEF VARIABLE sc-amt  AS DECIMAL NO-UNDO.

DEF BUFFER artbuff FOR artikel.

    FIND FIRST artbuff WHERE artbuff.artnr = artNo
        AND artbuff.departement = deptNo NO-LOCK NO-ERROR.
    IF artbuff.mwst-code NE 0 THEN 
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = artbuff.mwst-code
        NO-LOCK NO-ERROR.
        IF AVAILABLE htparam AND htparam.paramnr NE 0 THEN
            ASSIGN vat-bez = htparam.bezeich.
    END.
    IF artbuff.service-code NE 0 THEN 
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = artbuff.service-code
        NO-LOCK NO-ERROR.
        IF AVAILABLE htparam AND htparam.paramnr NE 0 THEN
            ASSIGN sc-bez = htparam.bezeich.
    END.
    IF artbuff.prov-code NE 0 THEN 
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = artbuff.prov-code
        NO-LOCK NO-ERROR.
        IF AVAILABLE htparam AND htparam.paramnr NE 0 THEN
            ASSIGN tax-bez = htparam.bezeich.
    END.
    RUN calc-servtaxesbl.p (1, artNo, deptNo, billdate, 
        OUTPUT serv, OUTPUT vat, OUTPUT tax, OUTPUT fact).

    ASSIGN 
        netto   = ROUND(betrag / fact, price-decimal)
        vat-amt = ROUND(netto * vat, price-decimal)
        tax-amt = ROUND(netto * tax, price-decimal)
        /*sc-amt  = bill-line.betrag - netto - vat-amt - tax-amt*/
        sc-amt  = betrag - netto - vat-amt - tax-amt.
    
    IF vat NE 0 THEN
    DO:
        FIND FIRST bline-vatlist WHERE 
            bline-vatlist.vatnr = artbuff.mwst-code NO-ERROR.
        IF NOT AVAILABLE bline-vatlist THEN
        DO:
            CREATE bline-vatlist.
            ASSIGN
                bline-vatlist.seqnr   = 9
                bline-vatlist.vatnr   = artbuff.mwst-code
                bline-vatlist.bezeich = vat-bez
            .
        END.
        bline-vatlist.betrag = bline-vatlist.betrag + vat-amt.

    END.

    IF tax NE 0 THEN
    DO:
        FIND FIRST bline-vatlist WHERE 
            bline-vatlist.vatnr = artbuff.prov-code NO-ERROR.
        IF NOT AVAILABLE bline-vatlist THEN
        DO:
            CREATE bline-vatlist.
            ASSIGN
                bline-vatlist.seqnr   = 4
                bline-vatlist.vatnr   = artbuff.prov-code
                bline-vatlist.bezeich = tax-bez
            .
        END.
        /*bline-vatlist.betrag = bline-vatlist.betrag + netto.        */
        bline-vatlist.betrag = bline-vatlist.betrag + tax-amt.   

    END.

    IF serv NE 0 THEN
    DO:
        FIND FIRST bline-vatlist WHERE bline-vatlist.vatnr = artbuff.service-code NO-ERROR.
        IF NOT AVAILABLE bline-vatlist THEN
        DO:
            CREATE bline-vatlist.
            ASSIGN
                bline-vatlist.seqnr   = 3
                bline-vatlist.vatnr   = artbuff.service-code
                bline-vatlist.bezeich = sc-bez
            .
        END.
        bline-vatlist.betrag = bline-vatlist.betrag + sc-amt.
    END.

    FIND FIRST bline-vatlist WHERE bline-vatlist.seqnr = 1 NO-ERROR.
    IF NOT AVAILABLE bline-vatlist THEN
    DO:
        CREATE bline-vatlist.
        ASSIGN
            bline-vatlist.seqnr   = 1
            bline-vatlist.vatnr   = -1
            bline-vatlist.bezeich = 
            translateExtended("Total Incl. VAT",lvCAREA,"").
    END.
    /*bline-vatlist.betrag = bline-vatlist.betrag + bill-line.betrag.*/
    bline-vatlist.betrag = bline-vatlist.betrag + betrag.

    FIND FIRST bline-vatlist WHERE 
        bline-vatlist.seqnr = 2 NO-ERROR.
    IF NOT AVAILABLE bline-vatlist THEN
    DO:
        CREATE bline-vatlist.
        ASSIGN
            bline-vatlist.seqnr   = 2
            bline-vatlist.vatnr   = -2
            bline-vatlist.bezeich =
            translateExtended("Net Amount",lvCAREA,"")
        .
    END.
    bline-vatlist.betrag = bline-vatlist.betrag + netto.
END.

PROCEDURE rev-bdown1:
    FIND CURRENT bill-line NO-LOCK.
    FIND CURRENT artikel NO-LOCK.
    RUN calc-servtaxes (artikel.artnr, artikel.departement,
        bill-line.betrag, bill-line.bill-datum).
END.

PROCEDURE rev-bdown2:
DEFINE VARIABLE rest-betrag     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE argt-betrag     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE ex-rate         AS DECIMAL NO-UNDO.
DEFINE VARIABLE p-sign          AS INTEGER NO-UNDO INIT 1. 

DEFINE BUFFER artikel1 FOR artikel. 
DEFINE BUFFER billbuff FOR bill.
DEFINE BUFFER mbill    FOR bill.

  FIND CURRENT artikel NO-LOCK.
  FIND CURRENT bill-line NO-LOCK.
  IF bill-line.betrag LT 0 THEN p-sign = -1.
   
  FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
      AND res-line.reslinnr = bill-line.billin-nr NO-LOCK NO-ERROR.
  IF NOT AVAILABLE res-line THEN RETURN.

  FIND FIRST arrangement WHERE arrangement.arrangement 
      = res-line.arrangement NO-LOCK.

  FIND FIRST billbuff WHERE billbuff.resnr = res-line.resnr
      AND billbuff.reslinnr = res-line.reslinnr NO-LOCK.
  FIND FIRST mbill WHERE mbill.resnr = res-line.resnr
      AND mbill.reslinnr = 0 NO-LOCK NO-ERROR.

  rest-betrag = bill-line.betrag. 

  FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
    AND NOT argt-line.kind2 NO-LOCK:  /* kind2 = YES => fix cost e.g extrabed */ 
    
    FIND FIRST billjournal WHERE billjournal.artnr = argt-line.argt-artnr
        AND billjournal.departement = argt-line.departement
        AND billjournal.bill-datum = bill-line.bill-datum
        AND billjournal.zeit = bill-line.zeit
        AND billjournal.userinit = bill-line.userinit
        AND billjournal.rechnr = billbuff.rechnr
        AND billjournal.anzahl NE 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE billjournal AND AVAILABLE mbill THEN
    FIND FIRST billjournal WHERE billjournal.artnr = argt-line.argt-artnr
        AND billjournal.departement = argt-line.departement
        AND billjournal.bill-datum = bill-line.bill-datum
        AND billjournal.zeit = bill-line.zeit
        AND billjournal.userinit = bill-line.userinit
        AND billjournal.rechnr = mbill.rechnr
        AND billjournal.anzahl NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE billjournal THEN argt-betrag = billjournal.betrag.
    ELSE
    DO:
        RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
          OUTPUT argt-betrag, OUTPUT ex-rate). 
        ASSIGN
            argt-betrag = ROUND(argt-betrag * ex-rate, price-decimal)
            argt-betrag = argt-betrag * p-sign
        . 
    END.
    rest-betrag = rest-betrag - argt-betrag. 

    IF argt-betrag NE 0 THEN 
        RUN calc-servtaxes (argt-line.argt-artnr, argt-line.departement,
                            argt-betrag, bill-line.bill-datum).
  END. 
 
  
  FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
    AND artikel1.departement = 0 NO-LOCK. 

  RUN calc-servtaxes (artikel1.artnr, artikel1.departement,
                      rest-betrag, bill-line.bill-datum).
 
END. 

PROCEDURE rev-bdown3:
DEFINE VARIABLE rest-betrag     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE argt-betrag     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE ex-rate         AS DECIMAL NO-UNDO.
DEFINE VARIABLE p-sign          AS INTEGER NO-UNDO INIT 1. 

DEFINE BUFFER artikel1 FOR artikel. 

  FIND CURRENT artikel NO-LOCK.
  FIND CURRENT bill-line NO-LOCK.
  IF bill-line.betrag LT 0 THEN p-sign = -1.
   
  FIND FIRST arrangement WHERE arrangement.argtnr 
      = artikel.artgrp NO-LOCK.

  rest-betrag = bill-line.betrag. 

  FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
      NO-LOCK:
    
    FIND FIRST billjournal WHERE billjournal.artnr = argt-line.argt-artnr
        AND billjournal.departement = argt-line.departement
        AND billjournal.bill-datum = bill-line.bill-datum
        AND billjournal.zeit = bill-line.zeit
        AND billjournal.userinit = bill-line.userinit
        AND billjournal.anzahl NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE billjournal THEN argt-betrag = billjournal.betrag.
    ELSE
    DO:
      IF argt-line.betrag NE 0 THEN 
      DO: 
        argt-betrag = argt-line.betrag * bill-line.anzahl. 
        IF artikel.pricetab THEN 
        DO:
          exchg-rate = 1.
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
              NO-LOCK NO-ERROR.
          IF bill-line.bill-datum = curr-billdate 
              AND AVAILABLE waehrung THEN
              exchg-rate = waehrung.ankauf / waehrung.einheit.
          ELSE
          DO:
              FIND FIRST exrate WHERE exrate.datum = bill-line.bill-datum
                  AND exrate.artnr = artikel.betriebsnr NO-LOCK NO-ERROR.
              IF AVAILABLE exrate THEN exchg-rate = exrate.betrag.
              ELSE IF AVAILABLE waehrung THEN 
                  exchg-rate = waehrung.ankauf / waehrung.einheit.
          END.
          argt-betrag = ROUND(argt-betrag * exchg-rate, price-decimal). 
        END.
      END.
      ELSE 
      ASSIGN 
          argt-betrag = bill-line.betrag * argt-line.vt-percnt / 100 
          argt-betrag = ROUND(argt-betrag, price-decimal)
      . 
      rest-betrag = rest-betrag - argt-betrag. 
      IF argt-betrag NE 0 THEN 
      RUN calc-servtaxes (argt-line.argt-artnr, argt-line.departement,
          argt-betrag, bill-line.bill-datum).
    END. 
  END.
    
  FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
      AND artikel1.departement = 0 NO-LOCK. 

  RUN calc-servtaxes (artikel1.artnr, artikel1.departement,
        rest-betrag, bill-line.bill-datum).

END. 
