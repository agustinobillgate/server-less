DEFINE TEMP-TABLE s-list 
  FIELD zeit        AS INTEGER 
  FIELD dept        AS INTEGER  FORMAT ">9"                 LABEL "Dept" 
  FIELD artnr       AS INTEGER  FORMAT ">>>9"               LABEL "ArtNo" 
  FIELD bezeich     AS CHAR     FORMAT "x(31)"              LABEL "Description" 
  FIELD zinr        AS CHAR     FORMAT "x(5)"               LABEL "RmNo" 
  FIELD anzahl      AS INTEGER  FORMAT ">,>>9"              LABEL "Qty" 
  FIELD preis       AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99"   LABEL "Price" 
  FIELD betrag      AS DECIMAL  FORMAT ">>,>>>,>>>,>>9.99"  LABEL "Amount" 
  FIELD l-betrag    AS DECIMAL 
  FIELD f-betrag    AS DECIMAL 
  FIELD resnr       AS INTEGER 
  FIELD reslinnr    AS INTEGER. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR s-list.
DEF INPUT  PARAMETER pvILanguage     AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER billart         AS INTEGER.
DEF INPUT  PARAMETER curr-dept       AS INTEGER.
DEF INPUT  PARAMETER amount          AS DECIMAL.
DEF INPUT  PARAMETER double-currency AS LOGICAL. 
DEF INPUT  PARAMETER foreign-rate    AS LOGICAL. 
DEF INPUT  PARAMETER user-init       AS CHAR.
DEF INPUT  PARAMETER voucher-nr      AS CHAR.
DEF OUTPUT PARAMETER msg-str         AS CHAR.
DEF OUTPUT PARAMETER msg-str2        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "quick-post".

RUN create-bill.

PROCEDURE create-bill: 
  FOR EACH s-list: 
    FIND FIRST res-line WHERE res-line.resnr = s-list.resnr 
      AND res-line.reslinnr = s-list.reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN                                        /* Rulita 181124 | Fixing for serverless */
    DO:
      FIND FIRST bill WHERE bill.resnr = res-line.resnr 
        AND bill.reslinnr = res-line.reslinnr 
        AND bill.zinr = res-line.zinr NO-LOCK NO-ERROR. 
      IF AVAILABLE bill THEN                                          /* Rulita 091224 | Fixing for serverless issue git 156 */
      DO:
        IF bill.flag = 1 THEN 
        DO: 
          msg-str = msg-str + CHR(2) + "&W"
                  + translateExtended ("Bill Number",lvCAREA,"") + " " + STRING(bill.rechnr) + " " + translateExtended ("RmNo",lvCAREA,"") + " " + s-list.zinr
                  + " : " + translateExtended ("Status closed, Posting not possible.",lvCAREA,"").
        END. 
        ELSE 
        DO: 
          IF res-line.l-zuordnung[2] NE 1 THEN RUN check-mbill(s-list.dept, s-list.artnr).                     /* Rulita 220425 | Fixing for serverless penambahan find first artikel utk get data artart & umsatzart git issue 716 */
                  /* l-zuordnung[2] = 1 -> disconnect from the master bill */ 
          RUN update-bill. 
        END.
      END.
    END. 
    DELETE s-list. 
  END.
END. 


PROCEDURE update-bill: 
DEFINE VARIABLE bil-flag AS INTEGER INITIAL 0. 
DEFINE VARIABLE master-flag AS LOGICAL. 
DEFINE VARIABLE bill-date AS DATE. 
DEFINE VARIABLE na-running AS LOGICAL. 
  DO: 
    FIND CURRENT bill EXCLUSIVE-LOCK. 
    FIND FIRST artikel WHERE artikel.artnr = billart 
        AND artikel.departement = curr-dept NO-LOCK NO-ERROR. 
    /* Rulita 101224 | Fixing for serverless git issue 156 */
    IF AVAILABLE artikel THEN 
    DO:
      IF artikel.umsatzart = 1 
        THEN bill.logisumsatz = bill.logisumsatz + amount. 
      ELSE IF artikel.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + amount. 
      ELSE IF (artikel.umsatzart = 3 OR artikel.umsatzart = 5 
        OR artikel.umsatzart = 6) 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + amount. 
      ELSE IF artikel.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + amount. 
      IF artikel.umsatzart GE 1 AND artikel.umsatzart LE 4 THEN 
        bill.gesamtumsatz = bill.gesamtumsatz + amount.
    END.
    /* End Rulita */
 
    bill.rgdruck = 0. 
    bill.saldo = bill.saldo + s-list.l-betrag. 
    IF double-currency OR foreign-rate THEN 
        bill.mwst[99] = bill.mwst[99] + s-list.f-betrag. 
    IF bill.rechnr = 0 THEN 
    DO: 
      FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
      counters.counter = counters.counter + 1. 
      bill.rechnr = counters.counter. 
      FIND CURRENT counter NO-LOCK. 
    END. 
    FIND FIRST htparam WHERE paramnr = 253 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN na-running = htparam.flogical.                           /* Rulita 250325 | Fixing if avail htparam serverless issue git 716 */
    FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.   /* bill DATE */ 
    IF AVAILABLE htparam THEN                                                          /* Rulita 250325 | Fixing if avail htparam serverless issue git 716 */
    DO:
      bill-date = htparam.fdate.

      /*  IF Night Audit is running THEN increase the billing DATE BY 1.   */ 
      IF na-running AND bill-date = htparam.fdate THEN bill-date = bill-date + 1.      /* Rulita 250325 | Fixing from fdate to fdate serverless issue git 716 */
    END.

    IF bill.datum LT bill-date OR bill.datum = ? THEN bill.datum = bill-date. 
    FIND CURRENT bill NO-LOCK. 
 
    create bill-line. 
    ASSIGN 
      bill-line.rechnr = bill.rechnr 
      bill-line.artnr = s-list.artnr 
      bill-line.bezeich = s-list.bezeich 
      bill-line.anzahl = s-list.anzahl 
      bill-line.betrag = s-list.l-betrag 
      bill-line.fremdwbetrag = s-list.f-betrag 
      bill-line.zinr = s-list.zinr 
      bill-line.departement = s-list.dept 
      bill-line.epreis = s-list.preis 
      bill-line.zeit = s-list.zeit 
      bill-line.userinit = user-init 
      bill-line.bill-datum = bill-date. 
    FIND CURRENT bill-line NO-LOCK. 
 
    FIND FIRST umsatz WHERE umsatz.artnr = s-list.artnr 
      AND umsatz.departement = s-list.dept 
      AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE umsatz THEN 
    DO: 
      create umsatz. 
      umsatz.artnr = s-list.artnr. 
      umsatz.datum = bill-date. 
      umsatz.departement = s-list.dept. 
    END. 
    umsatz.betrag = umsatz.betrag + s-list.l-betrag. 
    umsatz.anzahl = umsatz.anzahl + s-list.anzahl. 
    FIND CURRENT umsatz NO-LOCK. 
 
    CREATE billjournal. 
    ASSIGN 
      billjournal.rechnr = bill.rechnr 
      billjournal.artnr = s-list.artnr 
      billjournal.anzahl = s-list.anzahl 
      billjournal.fremdwaehrng = s-list.f-betrag 
      billjournal.betrag = s-list.l-betrag 
      billjournal.bezeich = s-list.bezeich 
      billjournal.zinr = s-list.zinr 
      billjournal.departement = s-list.dept 
      billjournal.epreis = s-list.preis 
      billjournal.zeit = s-list.zeit 
      billjournal.userinit = user-init 
      billjournal.bill-datum = bill-date. 
    FIND CURRENT billjournal NO-LOCK. 

    IF artikel.artart = 2 OR artikel.artart = 7 THEN
      RUN inv-ar(artikel.artnr, res-line.zinr, bill.gastnr, 
        res-line.gastnrmember, bill.rechnr, 
        s-list.betrag, s-list.f-betrag, bill-date, 
        bill.name, user-init, voucher-nr). 

  END. 
END. 

{ inv-ar.i } 

PROCEDURE check-mbill: 
DEFINE INPUT  PARAMETER slist-dept  AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER slist-artnr AS INTEGER NO-UNDO.

DEFINE VARIABLE master-flag AS LOGICAL INITIAL NO. 
DEFINE buffer resline FOR res-line. 
  FIND FIRST artikel WHERE artikel.departement EQ slist-dept                    /* Rulita 220425 | Fixing for serverless penambahan find first artikel utk get data artart & umsatzart git issue 716 */
    AND artikel.artnr EQ slist-artnr NO-LOCK NO-ERROR.  
  FIND FIRST master WHERE master.resnr = bill.resnr 
    AND master.active = YES AND master.flag = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE master THEN 
  DO: 
    IF (master.umsatzart[1] = YES AND artikel.artart = 8) 
        OR (master.umsatzart[2] = YES AND artikel.artart = 9 
            AND artikel.artgrp = 0) 
        OR (master.umsatzart[3] = YES AND artikel.umsatzart = 3) 
        OR (master.umsatzart[4] = YES AND artikel.umsatzart = 4) THEN 
      master-flag = YES. 
    IF NOT master-flag THEN 
    DO: 
      FIND FIRST mast-art WHERE mast-art.resnr = master.resnr 
        AND mast-art.departement = artikel.departement 
        AND mast-art.artnr = artikel.artnr NO-LOCK NO-ERROR. 
      IF AVAILABLE mast-art THEN master-flag = YES. 
    END. 
  END. 
  
  IF master-flag THEN 
  DO: 
    FIND FIRST bill WHERE bill.resnr = res-line.resnr 
      AND bill.reslinnr = 0 NO-LOCK.
    msg-str2 = translateExtended ("RmNo",lvCAREA,"") + " " + res-line.zinr + " "
          + translateExtended ("transfered to Master Bill No.",lvCAREA,"") 
          + " " + STRING(bill.rechnr).
    RETURN. 
  END. 
  IF res-line.memozinr NE "" AND res-line.memozinr NE res-line.zinr THEN 
  DO: 
    FIND FIRST resline WHERE resline.zinr = res-line.memozinr 
        AND resline.resstatus = 6 NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN FIND FIRST bill WHERE bill.resnr = resline.resnr 
      AND bill.reslinnr = resline.reslinnr NO-LOCK.
    msg-str2 = translateExtended ("RmNo",lvCAREA,"") + " " + res-line.zinr + " "
             + translateExtended ("transfered to Bill No.",lvCAREA,"") + " " 
             + STRING(bill.rechnr).
  END. 
END. 
