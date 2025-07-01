DEFINE TEMP-TABLE spbill-list
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER
. 

DEF INPUT PARAMETER pvILanguage  AS INTEGER         NO-UNDO.
DEF INPUT PARAMETER j            AS INTEGER         NO-UNDO.
DEF INPUT PARAMETER recid-curr   AS INTEGER         NO-UNDO.
DEF INPUT PARAMETER recid-j      AS INTEGER         NO-UNDO.
DEF INPUT PARAMETER user-init    AS CHAR            NO-UNDO.
DEF INPUT PARAMETER TABLE        FOR spbill-list.
DEF OUTPUT PARAMETER msg-str     AS CHAR     INIT "" NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "split-bill". 

DEFINE VARIABLE availBill AS LOGICAL INIT NO NO-UNDO.

RUN check-bill-line.
IF msg-str EQ "" AND availBill THEN RUN update-billine.

PROCEDURE check-bill-line:
    FIND FIRST bill WHERE RECID(bill) = recid-curr NO-LOCK. 
    IF NOT AVAILABLE bill THEN RETURN. /*FT serverless*/
    availBill = YES.
    FOR EACH spbill-list WHERE spbill-list.selected = YES: 
        FIND FIRST bill-line WHERE RECID(bill-line) = spbill-list.bl-recid 
            AND bill-line.rechnr = bill.rechnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bill-line THEN
        DO:
            msg-str = translateExtended ("Bill transfer not possible:",lvCAREA,"") + CHR(10)
                    + translateExtended ("One of the bill has been changed, please refresh the screen!",lvCAREA,"").
            LEAVE.
        END.
    END.
END.

PROCEDURE update-billine: 
  DEFINE VARIABLE rechnr        AS INTEGER. 
  DEFINE VARIABLE datum         AS DATE INITIAL ?. 
  DEFINE VARIABLE replace-it    AS LOGICAL INITIAL NO. 
  DEFINE VARIABLE do-it         AS LOGICAL NO-UNDO.
  DEFINE VARIABLE billine-datum AS DATE.
  DEFINE BUFFER billi FOR bill. 
  DEFINE BUFFER billj FOR bill. 
  DEFINE BUFFER art1  FOR artikel. 
  DEFINE BUFFER bline FOR bill-line. 
  DEFINE BUFFER gbuff FOR guest.

  FIND FIRST billi 
      WHERE RECID(billi) = recid-curr EXCLUSIVE-LOCK. 
  rechnr = billi.rechnr. 
  FIND FIRST billj 
      WHERE RECID(billj) = recid-j EXCLUSIVE-LOCK. 
  IF billj.rechnr EQ 0 THEN 
  DO: 
    FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
    counters.counter = counters.counter + 1. 
    billj.rechnr = counters.counter. 
    FIND CURRENT counters NO-LOCK. 
    replace-it = YES. 
  END. 
  ELSE 
  DO: 
    FIND FIRST bline WHERE bline.rechnr = billj.rechnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE bline THEN replace-it = YES. 
  END. 
 
  FIND FIRST gbuff WHERE gbuff.gastnr = billj.gastnr NO-LOCK.
  FOR EACH spbill-list WHERE spbill-list.selected = YES: 
    FIND FIRST bill-line WHERE RECID(bill-line) = spbill-list.bl-recid 
        AND bill-line.rechnr = rechnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE bill-line THEN
    DO:
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr
          AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR.
      IF AVAILABLE artikel AND artikel.artart = 2 AND gbuff.zahlungsart = 0 THEN
      DO:
        msg-str = translateExtended ("Bill transfer not possible:",lvCAREA,"") + CHR(10)
          + translateExtended ("Destination bill does not have C/L account",lvCAREA,"").
        RETURN.
      END.
    END.
  END.

  FOR EACH spbill-list WHERE spbill-list.selected = YES: 
    FIND FIRST bill-line WHERE RECID(bill-line) = spbill-list.bl-recid 
        AND bill-line.rechnr = rechnr EXCLUSIVE-LOCK NO-ERROR. 
    do-it = (AVAILABLE bill-line).
    IF do-it AND billj.resnr > 0 AND billj.reslinnr > 0 
      AND bill-line.typ GT 0 AND bill-line.typ NE billi.resnr 
      AND bill-line.typ NE billj.resnr AND (billi.gastnr NE billj.gastnr) THEN   
    DO:
      FIND FIRST res-line WHERE res-line.resnr = billj.resnr
          AND res-line.reslinnr = billj.parent-nr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line AND res-line.ankunft GT bill-line.bill-datum THEN 
          ASSIGN
            do-it = NO
            billine-datum = bill-line.bill-datum.

    END.
    IF NOT do-it THEN
    msg-str = msg-str + CHR(2) + translateExtended ("Bill transfer not possible:",lvCAREA,"") + CHR(10)
       + translateExtended ("Posting date:",lvCAREA,"") + " " 
       + STRING(billine-datum) + " "
       + translateExtended ("BUT Arrival Date of the transferred guest bill is",lvCAREA,"")
       + " " + STRING(res-line.ankunft) + CHR(10).
    ELSE  
    DO: 
      ASSIGN
        billi.rgdruck = 0
        billj.rgdruck = 0
        bill-line.rechnr = billj.rechnr
        billi.saldo = billi.saldo - bill-line.betrag 
        billj.saldo = billj.saldo + bill-line.betrag 
        billi.mwst[99] = billi.mwst[99] - bill-line.fremdwbetrag 
        billj.mwst[99] = billj.mwst[99] + bill-line.fremdwbetrag
      . 
      IF bill-line.typ = 0 THEN ASSIGN bill-line.typ = billi.resnr.
      
      IF datum = ? THEN datum = bill-line.bill-datum. 
      ELSE IF datum LT bill-line.bill-datum THEN 
      datum = bill-line.bill-datum. 
 
      FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
      
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr = billj.rechnr
        billjournal.artnr = bill-line.artnr 
        billjournal.anzahl = /*bill-line.anzahl*/ 0
        billjournal.betrag = bill-line.betrag
        billjournal.fremdwaehrng = bill-line.fremdwbetrag 
        billjournal.zinr = billj.zinr
        billjournal.departement = bill-line.departement
        billjournal.epreis = bill-line.epreis
        billjournal.zeit = TIME 
        billjournal.userinit = user-init 
        billjournal.bill-datum = bill-line.bill-datum
      . 
      billjournal.bezeich = "*" + STRING(billi.rechnr) 
        + "; " + STRING(htparam.fdate) 
        + " " + translateExtended ("RmNo",lvCAREA,"") 
        + " " + billi.zinr.
      FIND CURRENT bill-line NO-LOCK. 
      FIND CURRENT billjournal NO-LOCK. 
 
      FIND FIRST art1 WHERE art1.artnr = bill-line.artnr AND 
        art1.departement = bill-line.departement NO-LOCK NO-ERROR. 
      IF AVAILABLE art1 AND (art1.artart = 2 OR art1.artart = 7) THEN 
      DO: 
        FIND FIRST debitor WHERE debitor.artnr = art1.artnr 
          AND debitor.rechnr = billi.rechnr 
          AND debitor.rgdatum = bill-line.bill-datum 
          AND debitor.saldo = - bill-line.betrag 
          AND debitor.counter = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE debitor THEN 
        DO: 
          FIND FIRST gbuff WHERE gbuff.gastnr = billj.gastnr.
          FIND CURRENT debitor EXCLUSIVE-LOCK. 
          ASSIGN
            debitor.rechnr = billj.rechnr
            debitor.gastnr = billj.gastnr
            debitor.NAME   = gbuff.NAME
          . 
          FIND CURRENT debitor NO-LOCK. 
        END. 
      END. 

      /*FDL: E75526*/
      FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
      IF AVAILABLE bediener THEN
      DO:
        CREATE res-history. 
        ASSIGN 
          res-history.nr = bediener.nr
          res-history.datum = TODAY 
          res-history.zeit = TIME 
          res-history.aenderung = "OutletNo: " + STRING(bill-line.departement) 
            + "|" + "ArtNo:" + STRING(bill-line.artnr)
            + "|" + "Desc:" + bill-line.bezeich
            + "|" + "Amount:" + TRIM(STRING(bill-line.betrag, "->>>,>>>,>>>,>>9.99")).
            
            IF billi.resnr NE 0 AND billi.reslinnr NE 0 THEN
            DO:
                res-history.aenderung = res-history.aenderung + "|" + "From Room:" + STRING(billi.zinr).
            END.
            ELSE IF billi.resnr NE 0 AND billi.reslinnr EQ 0 THEN
            DO:
                res-history.aenderung = res-history.aenderung + "|" + "From Master Bill".
            END.
            ELSE IF billi.resnr EQ 0 AND billi.reslinnr NE 0 THEN
            DO:
                res-history.aenderung = res-history.aenderung + "|" + "From NonStay Bill".
            END.    
            
            IF billj.resnr NE 0 AND billj.reslinnr NE 0 THEN
            DO:
                res-history.aenderung = res-history.aenderung + "|" + "To Room:" + STRING(billj.zinr).
            END.
            ELSE IF billj.resnr NE 0 AND billj.reslinnr EQ 0 THEN
            DO:
                res-history.aenderung = res-history.aenderung + "|" + "To Master Bill".
            END.
            ELSE IF billj.resnr EQ 0 AND billj.reslinnr NE 0 THEN
            DO:
                res-history.aenderung = res-history.aenderung + "|" + "To NonStay Bill".
            END.

            res-history.aenderung = res-history.aenderung + "|" + "From Bill:" + STRING(billi.rechnr)
                + "|" + "To Bill:" + STRING(billj.rechnr)
                .
          res-history.action = "Transfer Bill F/O". 
         FIND CURRENT res-history NO-LOCK. 
         RELEASE res-history. 
      END.
    END. 
    DELETE spbill-list. 
  END. 
  IF datum NE ? AND replace-it THEN billj.datum = datum. 
  ELSE IF billj.datum LT datum AND datum NE ? THEN billj.datum = datum. 
  datum = ?. 
  FOR EACH bline WHERE bline.rechnr = billi.rechnr NO-LOCK: 
    IF datum = ? THEN datum = bline.bill-datum. 
    ELSE IF datum LT bline.bill-datum THEN datum = bline.bill-datum. 
  END. 
  IF datum NE billi.datum AND datum NE ? THEN billi.datum = datum. 
 
  FIND CURRENT billi NO-LOCK. 
  FIND CURRENT billj NO-LOCK. 
 
END. 
