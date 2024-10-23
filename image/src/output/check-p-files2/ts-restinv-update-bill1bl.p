DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE vat-list
    FIELD vatProz    AS DECIMAL INITIAL 0
    FIELD vatAmt     AS DECIMAL INITIAL 0
    FIELD netto      AS DECIMAL INITIAL 0
    FIELD betrag     AS DECIMAL INITIAL 0
    FIELD fBetrag    AS DECIMAL INITIAL 0.

DEF INPUT PARAMETER rec-id-h-bill       AS INT.
DEF INPUT PARAMETER transdate           AS DATE.
DEF INPUT PARAMETER double-currency     AS LOGICAL.
DEF INPUT PARAMETER exchg-rate          AS DECIMAL.
DEF INPUT PARAMETER kellner1-kcredit-nr AS INT.
DEF INPUT PARAMETER bilrecid            AS INT.
DEF INPUT PARAMETER foreign-rate        AS LOGICAL.
DEF INPUT PARAMETER user-init           AS CHAR.
DEF INPUT PARAMETER gname               AS CHAR.
DEF INPUT PARAMETER hoga-resnr          AS INT.
DEF INPUT PARAMETER hoga-reslinnr       AS INT.
DEF INPUT PARAMETER price-decimal       AS INT.

DEF INPUT-OUTPUT PARAMETER amount LIKE vhp.bill-line.betrag.
DEF INPUT-OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.

/*DEF OUTPUT PARAMETER multi-vat AS LOGICAL INIT NO.*/
DEF OUTPUT PARAMETER bill-date          AS DATE.
DEF OUTPUT PARAMETER billart            AS INT.
DEF OUTPUT PARAMETER qty                AS DECIMAL.
DEF OUTPUT PARAMETER description        AS CHAR.
DEF OUTPUT PARAMETER cancel-str         AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

DEF VAR vat-amount AS DECIMAL INITIAL 0  NO-UNDO. 
DEF VAR multi-vat  AS LOGICAL INIT NO.

DEF VARIABLE get-rechnr  AS INTEGER NO-UNDO.
DEF VARIABLE get-amount  AS DECIMAL NO-UNDO.
DEF VARIABLE curr-dept   AS INTEGER NO-UNDO.
DEF VARIABLE active-deposit AS LOGICAL.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id-h-bill.
FIND FIRST vhp.bill WHERE RECID(bill) = bilrecid NO-LOCK.

curr-dept = h-bill.departement.
IF gname EQ ? THEN gname = "".
IF user-init EQ ? THEN user-init = "".

  /*FD Nov 30, 2022 => Feature Deposit Resto*/
  FIND FIRST htparam WHERE htparam.paramnr EQ 588 NO-LOCK NO-ERROR. 
  IF AVAILABLE htparam THEN active-deposit = htparam.flogical.

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 271 NO-LOCK. 
  IF vhp.htparam.feldtyp = 4 THEN multi-vat = vhp.htparam.flogical.

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
  /* vhp.bill DATE */ 
  bill-date = vhp.htparam.fdate. 
  IF transdate NE ? THEN bill-date = transdate. 
  ELSE 
  DO: 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
    IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
  END. 

  ASSIGN
      billart        = 0
      qty            = 1 
      amount         = - amount
      amount-foreign = - amount-foreign
  . 
  IF NOT double-currency THEN amount-foreign = amount / exchg-rate. 
  
  IF amount NE 0 THEN 
  DO TRANSACTION:
    FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = kellner1-kcredit-nr 
      AND vhp.artikel.departement = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.artikel THEN /*FD - Move from below*/
    DO: 
      billart = vhp.artikel.artnr. 
      description = TRIM(vhp.artikel.bezeich) 
          + " *" + STRING(vhp.h-bill.rechnr). 
    END. 
    ELSE description = "*" + STRING(vhp.h-bill.rechnr).

    FIND CURRENT vhp.bill EXCLUSIVE-LOCK. 
    IF vhp.bill.rechnr = 0 THEN 
    DO: 
      FIND FIRST vhp.counters WHERE vhp.counters.counter-no = 3 EXCLUSIVE-LOCK. 
      vhp.counters.counter = vhp.counters.counter + 1. 
      FIND CURRENT counter NO-LOCK. 
      vhp.bill.rechnr = vhp.counters.counter. 
    END. 
    
    RUN update-bill-umsatz.
    IF vhp.bill.datum LT bill-date THEN vhp.bill.datum = bill-date.

    
    IF foreign-rate AND NOT double-currency THEN 
      vhp.bill.mwst[99] = vhp.bill.mwst[99] + amount / exchg-rate. 
    ELSE IF double-currency THEN 
      vhp.bill.mwst[99] = vhp.bill.mwst[99] + amount-foreign. 
    vhp.bill.rgdruck = 0. 
    FIND CURRENT vhp.bill NO-LOCK. 
  
    RUN cal-vat-amount(OUTPUT vat-amount). 
    /*IF multi-vat THEN RUN create-vat-list.
 
    IF multi-vat THEN
    FOR EACH vat-list:
      
      IF AVAILABLE vhp.artikel THEN 
      DO: 
        billart = vhp.artikel.artnr. 
        description = TRIM(vhp.artikel.bezeich) 
            + "[" + STRING(vat-list.vatProz) + "]"
            + " *" + STRING(vhp.h-bill.rechnr). 
      END. 
      ELSE 
      description = "[" + STRING(vat-list.vatProz) + "]"
          + " *" + STRING(vhp.h-bill.rechnr). 

      CREATE vhp.bill-line. 
      ASSIGN 
        vhp.bill-line.rechnr = vhp.bill.rechnr 
        vhp.bill-line.zinr = vhp.bill.zinr 
        vhp.bill-line.massnr = vhp.bill.resnr 
        vhp.bill-line.billin-nr = vhp.bill.reslinnr 
        vhp.bill-line.artnr = billart 
        vhp.bill-line.bezeich = DESCRIPTION 
        vhp.bill-line.anzahl = 1 
        vhp.bill-line.fremdwbetrag = vat-list.fbetrag
        vhp.bill-line.betrag = vat-list.betrag 
        vhp.bill-line.nettobetrag = vat-list.netto
        vhp.bill-line.departement = vhp.h-bill.departement 
        vhp.bill-line.epreis = 0 
        vhp.bill-line.zeit = TIME 
        vhp.bill-line.userinit = user-init 
        vhp.bill-line.bill-datum = bill-date 
        vhp.bill-line.orts-tax = vat-list.vatAmt
        vhp.bill-line.origin-id = "VAT%," + STRING(vat-list.vatProz * 100) + ";"
          + "VAT," + STRING(vat-list.vatAmt * 100) + ";"
          + "NET," + STRING(vat-list.netto * 100) + ";"
      . 
 
      FIND CURRENT vhp.bill-line NO-LOCK. 

      CREATE vhp.billjournal. 
      ASSIGN
        vhp.billjournal.rechnr = vhp.bill.rechnr
        vhp.billjournal.zinr = vhp.bill.zinr
        vhp.billjournal.departement = vhp.h-bill.departement 
        vhp.billjournal.artnr = billart
        vhp.billjournal.anzahl = 1
        vhp.billjournal.fremdwaehrng = vat-list.fbetrag
        vhp.billjournal.betrag = vat-list.betrag
        vhp.billjournal.bezeich = DESCRIPTION
        vhp.billjournal.epreis = 0
        vhp.billjournal.zeit = TIME 
        vhp.billjournal.stornogrund = "" 
        vhp.billjournal.userinit = user-init 
        vhp.billjournal.bill-datum = bill-date
      . 
      IF AVAILABLE vhp.artikel THEN 
        vhp.billjournal.departement = vhp.artikel.departement. 
      FIND CURRENT vhp.billjournal NO-LOCK. 
    END.
    ELSE*/ 
    DO:
      /* FD Comment - Move Above Cause Avail Artikel Get From Other Procedure
      IF AVAILABLE vhp.artikel THEN 
      DO: 
        billart = vhp.artikel.artnr. 
        description = TRIM(vhp.artikel.bezeich) 
            + " *" + STRING(vhp.h-bill.rechnr). 
      END. 
      ELSE description = "*" + STRING(vhp.h-bill.rechnr). 
      */

      CREATE vhp.bill-line. 
      ASSIGN 
        vhp.bill-line.rechnr = vhp.bill.rechnr 
        vhp.bill-line.zinr = vhp.bill.zinr 
        vhp.bill-line.massnr = vhp.bill.resnr 
        vhp.bill-line.billin-nr = vhp.bill.reslinnr 
        vhp.bill-line.artnr = billart 
        vhp.bill-line.bezeich = DESCRIPTION 
        vhp.bill-line.anzahl = 1 
        vhp.bill-line.fremdwbetrag = amount-foreign
        vhp.bill-line.betrag = amount 
        vhp.bill-line.departement = vhp.h-bill.departement 
        vhp.bill-line.epreis = 0 
        vhp.bill-line.zeit = TIME 
        vhp.bill-line.userinit = user-init 
        vhp.bill-line.bill-datum = bill-date 
        vhp.bill-line.orts-tax = vat-amount
      .  
      FIND CURRENT vhp.bill-line NO-LOCK. 

      CREATE vhp.billjournal. 
      ASSIGN
        vhp.billjournal.rechnr = vhp.bill.rechnr
        vhp.billjournal.zinr = vhp.bill.zinr
        vhp.billjournal.departement = vhp.h-bill.departement 
        vhp.billjournal.artnr = billart
        vhp.billjournal.anzahl = 1
        vhp.billjournal.fremdwaehrng = amount-foreign
        vhp.billjournal.betrag = amount
        vhp.billjournal.bezeich = description
        vhp.billjournal.epreis = 0
        vhp.billjournal.zeit = TIME 
        vhp.billjournal.stornogrund = "" 
        vhp.billjournal.userinit = user-init 
        vhp.billjournal.bill-datum = bill-date
      . 
      IF AVAILABLE vhp.artikel THEN 
        vhp.billjournal.departement = vhp.artikel.departement. 
      FIND CURRENT vhp.billjournal NO-LOCK. 
    END.
    cancel-str = "". 
    /*MT*/
  END.

  DO TRANSACTION: 
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
    ASSIGN
      vhp.h-bill.flag = 1 
      vhp.h-bill.bilname = gname
    . 
    IF hoga-resnr GT 0 AND vhp.h-bill.resnr = 0 THEN 
    DO: 
      ASSIGN 
        vhp.h-bill.resnr = hoga-resnr 
        vhp.h-bill.reslinnr = hoga-reslinnr. 
      /*MTIF hogatex-flag THEN 
      DO: 
        vhp.h-bill.service[2] = hoga-host. 
      END. */
    END.
    FIND CURRENT vhp.h-bill NO-LOCK. 

    /*FD March 14, 2022 => UPDATE ALL QUEASY RELATED ON SELF ORDER*/
    get-rechnr = vhp.h-bill.rechnr.
    FOR EACH h-bill-line WHERE h-bill-line.departement EQ h-bill.departement 
        AND h-bill-line.rechnr EQ h-bill.rechnr
        AND h-bill-line.betrag LT 0 NO-LOCK:
        FIND FIRST h-artikel WHERE h-artikel.departement EQ h-bill-line.departement
            AND h-artikel.artnr EQ h-bill-line.artnr
            AND h-artikel.artart NE 0 NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN get-amount = get-amount + h-bill-line.betrag.
    END.
    FIND FIRST queasy WHERE queasy.KEY EQ 230 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        RUN update-selforder.
    END.

    /*FD Nov 30, 2022 => Feature Deposit Resto*/
    IF active-deposit THEN
    DO:
        RUN remove-rsv-table.
    END.
  END. 
  CREATE t-h-bill.
  BUFFER-COPY h-bill TO t-h-bill.
  ASSIGN t-h-bill.rec-id = RECID(h-bill).


  amount = - amount. 
  amount-foreign = - amount-foreign. 
  
/*MTT
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 271 NO-LOCK. 
  IF vhp.htparam.feldtyp = 4 THEN multi-vat = vhp.htparam.flogical.

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
  /* vhp.bill DATE */ 
  bill-date = vhp.htparam.fdate. 
  IF transdate NE ? THEN bill-date = transdate. 
  ELSE 
  DO: 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
    IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
  END. 

  ASSIGN
      billart        = 0
      qty            = 1 
      amount         = - amount
      amount-foreign = - amount-foreign
  . 
  IF NOT double-currency THEN amount-foreign = amount / exchg-rate. 
  
  IF amount NE 0 THEN 
  DO TRANSACTION:
    
    FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = kellner1-kcredit-nr 
      AND vhp.artikel.departement = 0 NO-LOCK NO-ERROR. 

    FIND FIRST vhp.bill WHERE RECID(bill) = bilrecid EXCLUSIVE-LOCK. 
    IF vhp.bill.rechnr = 0 THEN 
    DO: 
      FIND FIRST vhp.counters WHERE vhp.counters.counter-no = 3 EXCLUSIVE-LOCK. 
      vhp.counters.counter = vhp.counters.counter + 1. 
      FIND CURRENT counter NO-LOCK. 
      vhp.bill.rechnr = vhp.counters.counter. 
    END. 
    
    RUN update-bill-umsatz.

    IF vhp.bill.datum LT bill-date THEN vhp.bill.datum = bill-date.

    IF foreign-rate AND NOT double-currency THEN 
      vhp.bill.mwst[99] = vhp.bill.mwst[99] + amount / exchg-rate. 
    ELSE IF double-currency THEN 
      vhp.bill.mwst[99] = vhp.bill.mwst[99] + amount-foreign. 
    vhp.bill.rgdruck = 0. 
    FIND CURRENT vhp.bill NO-LOCK. 
  
    RUN cal-vat-amount(OUTPUT vat-amount). 
    IF multi-vat THEN RUN create-vat-list.
    
    IF multi-vat THEN
    FOR EACH vat-list:
      
      IF AVAILABLE vhp.artikel THEN 
      DO: 
        billart = vhp.artikel.artnr. 
        description = TRIM(vhp.artikel.bezeich) 
            + "[" + STRING(vat-list.vatProz) + "]"
            + " *" + STRING(vhp.h-bill.rechnr). 
      END. 
      ELSE 
      description = "[" + STRING(vat-list.vatProz) + "]"
          + " *" + STRING(vhp.h-bill.rechnr). 
    
      CREATE vhp.bill-line. 
      ASSIGN 
        vhp.bill-line.rechnr = vhp.bill.rechnr 
        vhp.bill-line.zinr = vhp.bill.zinr 
        vhp.bill-line.massnr = vhp.bill.resnr 
        vhp.bill-line.billin-nr = vhp.bill.reslinnr 
        vhp.bill-line.artnr = billart 
        vhp.bill-line.bezeich = DESCRIPTION 
        vhp.bill-line.anzahl = 1 
        vhp.bill-line.fremdwbetrag = vat-list.fbetrag
        vhp.bill-line.betrag = vat-list.betrag 
        vhp.bill-line.nettobetrag = vat-list.netto
        vhp.bill-line.departement = vhp.h-bill.departement 
        vhp.bill-line.epreis = 0 
        vhp.bill-line.zeit = TIME 
        vhp.bill-line.userinit = user-init 
        vhp.bill-line.bill-datum = bill-date 
        vhp.bill-line.orts-tax = vat-list.vatAmt
        vhp.bill-line.origin-id = "VAT%," + STRING(vat-list.vatProz * 100) + ";"
          + "VAT," + STRING(vat-list.vatAmt * 100) + ";"
          + "NET," + STRING(vat-list.netto * 100) + ";"
      . 
 
      FIND CURRENT vhp.bill-line NO-LOCK. 

      CREATE vhp.billjournal. 
      ASSIGN
        vhp.billjournal.rechnr = vhp.bill.rechnr
        vhp.billjournal.zinr = vhp.bill.zinr
        vhp.billjournal.departement = vhp.h-bill.departement 
        vhp.billjournal.artnr = billart
        vhp.billjournal.anzahl = 1
        vhp.billjournal.fremdwaehrng = vat-list.fbetrag
        vhp.billjournal.betrag = vat-list.betrag
        vhp.billjournal.bezeich = DESCRIPTION
        vhp.billjournal.epreis = 0
        vhp.billjournal.zeit = TIME 
        vhp.billjournal.stornogrund = "" 
        vhp.billjournal.userinit = user-init 
        vhp.billjournal.bill-datum = bill-date
      . 
      IF AVAILABLE vhp.artikel THEN 
        vhp.billjournal.departement = vhp.artikel.departement. 
      FIND CURRENT vhp.billjournal NO-LOCK. 
    END.
    ELSE DO:
      IF AVAILABLE vhp.artikel THEN 
      DO: 
        billart = vhp.artikel.artnr. 
        description = TRIM(vhp.artikel.bezeich) 
            + " *" + STRING(vhp.h-bill.rechnr). 
      END. 
      ELSE description = "*" + STRING(vhp.h-bill.rechnr). 

      CREATE vhp.bill-line. 
      ASSIGN 
        vhp.bill-line.rechnr = vhp.bill.rechnr 
        vhp.bill-line.zinr = vhp.bill.zinr 
        vhp.bill-line.massnr = vhp.bill.resnr 
        vhp.bill-line.billin-nr = vhp.bill.reslinnr 
        vhp.bill-line.artnr = billart 
        vhp.bill-line.bezeich = DESCRIPTION 
        vhp.bill-line.anzahl = 1 
        vhp.bill-line.fremdwbetrag = amount-foreign
        vhp.bill-line.betrag = amount 
        vhp.bill-line.departement = vhp.h-bill.departement 
        vhp.bill-line.epreis = 0 
        vhp.bill-line.zeit = TIME 
        vhp.bill-line.userinit = user-init 
        vhp.bill-line.bill-datum = bill-date 
        vhp.bill-line.orts-tax = vat-amount
      .  
      FIND CURRENT vhp.bill-line NO-LOCK. 

      CREATE vhp.billjournal. 
      ASSIGN
        vhp.billjournal.rechnr = vhp.bill.rechnr
        vhp.billjournal.zinr = vhp.bill.zinr
        vhp.billjournal.departement = vhp.h-bill.departement 
        vhp.billjournal.artnr = billart
        vhp.billjournal.anzahl = 1
        vhp.billjournal.fremdwaehrng = amount-foreign
        vhp.billjournal.betrag = amount
        vhp.billjournal.bezeich = description
        vhp.billjournal.epreis = 0
        vhp.billjournal.zeit = TIME 
        vhp.billjournal.stornogrund = "" 
        vhp.billjournal.userinit = user-init 
        vhp.billjournal.bill-datum = bill-date
      . 
      IF AVAILABLE vhp.artikel THEN 
        vhp.billjournal.departement = vhp.artikel.departement. 
      FIND CURRENT vhp.billjournal NO-LOCK. 
    END.
    cancel-str = "". 
  END.

  DO TRANSACTION: 
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
    ASSIGN
      vhp.h-bill.flag = 1 
      vhp.h-bill.bilname = gname
    . 
    IF hoga-resnr GT 0 AND vhp.h-bill.resnr = 0 THEN 
    DO: 
      ASSIGN 
        vhp.h-bill.resnr = hoga-resnr 
        vhp.h-bill.reslinnr = hoga-reslinnr. 
      /*MT not supported
      IF hogatex-flag THEN 
      DO: 
        vhp.h-bill.service[2] = hoga-host. 
      END.*/
    END.
    FIND CURRENT vhp.h-bill NO-LOCK. 
  END. 
*/



PROCEDURE cal-vat-amount:
DEF OUTPUT PARAMETER mwst AS DECIMAL INITIAL 0.
DEF VARIABLE h-service    AS DECIMAL.
DEF VARIABLE h-mwst       AS DECIMAL.
DEF VARIABLE vat2         AS DECIMAL NO-UNDO.
DEF VARIABLE fact         AS DECIMAL.
DEF VARIABLE fact1        AS DECIMAL.
DEF VARIABLE qty          AS DECIMAL.   
DEF VARIABLE unit-price   AS DECIMAL.
DEF VARIABLE amount       AS DECIMAL.
DEF VARIABLE incl-mwst    AS LOGICAL.
DEF VARIABLE multi-vat    AS LOGICAL INITIAL NO.
DEF VARIABLE curr-vat     AS DECIMAL INITIAL 0.
DEF VARIABLE disc-art1    AS INTEGER NO-UNDO. 

DEF BUFFER hbline FOR vhp.h-bill-line.
DEF BUFFER hart   FOR vhp.h-artikel.

  FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
  incl-mwst = vhp.htparam.flogical.

  FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
  disc-art1 = vhp.htparam.finteger. 



  FOR EACH hbline WHERE hbline.rechnr = vhp.h-bill.rechnr  
    AND hbline.departement = vhp.h-bill.departement NO-LOCK,
    FIRST hart WHERE hart.artnr = hbline.artnr 
    AND hart.departement = hbline.departement 
    AND hart.artart = 0 NO-LOCK:

   
    IF hart.artnr = disc-art1 THEN
    DO:
      FIND FIRST vhp.h-journal 
      WHERE vhp.h-journal.departement = hbline.departement
        AND vhp.h-journal.bill-datum = hbline.bill-datum
        AND vhp.h-journal.rechnr = hbline.rechnr
        AND vhp.h-journal.artnr = hbline.artnr
        AND vhp.h-journal.zeit = hbline.zeit NO-LOCK NO-ERROR.
      IF AVAILABLE vhp.h-journal THEN 
        mwst = mwst + vhp.h-journal.steuercode / 100.
    END.
    ELSE
    DO:
      h-service = 0. 
      h-mwst = 0. 
      fact = 1.
      qty = hbline.anzahl.
      IF qty LT 0 THEN qty = - qty.

      IF incl-mwst THEN 
      DO: 
/* SY AUG 13 2017 */
        FIND FIRST artikel WHERE artikel.artnr = hart.artnrfront
          AND artikel.departement = hart.departement NO-LOCK.      
        RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
        ?, OUTPUT h-service, OUTPUT h-mwst, OUTPUT vat2, OUTPUT fact).
        ASSIGN h-mwst = h-mwst + vat2.
        IF curr-vat = 0 THEN curr-vat = h-mwst.
        ELSE IF curr-vat NE h-mwst THEN multi-vat = YES.
/*
        fact = 0. 
        IF hart.service-code NE 0 THEN 
        DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr  
            = hart.service-code NO-LOCK. 
          IF vhp.htparam.fdecimal NE 0 THEN fact = vhp.htparam.fdecimal / 100.  
        END. 
        IF hart.mwst-code NE 0 THEN 
        DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr  
            = hart.mwst-code NO-LOCK. 
          IF vhp.htparam.fdecimal NE 0 THEN 
          DO: 
            IF curr-vat = 0 THEN curr-vat = vhp.htparam.fdecimal.
            ELSE IF curr-vat NE vhp.htparam.fdecimal THEN multi-vat = YES.

            fact1 = vhp.htparam.fdecimal. 
            FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
            IF vhp.htparam.flogical  /* service taxable */ THEN 
              fact = fact + (1 + fact) * fact1 / 100. 
            ELSE fact = fact + fact1 / 100.  
          END. 
        END.
        fact = 1 + fact. 
*/
      END. 
 
      amount = hbline.epreis * qty.  
      IF hbline.betrag GT 0 AND amount LT 0 THEN amount = - amount.
      ELSE IF hbline.betrag LT 0 AND amount GT 0 THEN amount = - amount.

      IF qty NE 0 THEN 
        unit-price = (hbline.betrag / qty) / fact. 
      ELSE unit-price = hbline.epreis / fact.
      IF unit-price LT 0 THEN unit-price = - unit-price.
/*
      IF hart.service-code NE 0 THEN 
      DO: 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr  
          = hart.service-code NO-LOCK. 
        IF vhp.htparam.fdecimal NE 0 THEN 
        DO: 
          h-service = unit-price * vhp.htparam.fdecimal / 100.  
          h-service = ROUND(h-service, 2).  
        END. 
      END. 
      IF hart.mwst-code NE 0 THEN 
      DO: 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr  
          = hart.mwst-code NO-LOCK. 
        IF vhp.htparam.fdecimal NE 0 THEN 
        DO: 
          h-mwst = vhp.htparam.fdecimal. 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
          IF vhp.htparam.flogical  /* service taxable */ 
            THEN h-mwst = h-mwst * (unit-price + h-service) / 100. 
          ELSE h-mwst = h-mwst * unit-price / 100.  
          h-mwst = ROUND(h-mwst * qty, price-decimal). 
        END. 
      END. 
*/
/* SY AUG 13 2017 */

      ASSIGN
        h-service = ROUND(h-service * unit-price, price-decimal)
        h-mwst    = ROUND (h-mwst * unit-price, price-decimal)
      .

      IF h-service = 0 AND h-mwst = 0 THEN . 
      ELSE IF NOT incl-mwst THEN 
      DO: 
        if h-service = 0 THEN h-mwst = hbline.betrag - amount.  
      END. 
 
      IF hbline.betrag GT 0 AND h-mwst LT 0 THEN h-mwst = - h-mwst.
      ELSE IF hbline.betrag LT 0 AND h-mwst GT 0 THEN h-mwst = - h-mwst.
      mwst = mwst + h-mwst.  
    END.
  END.   
END.


PROCEDURE create-vat-list:
DEFINE VARIABLE service AS DECIMAL NO-UNDO. 
DEFINE VARIABLE vat     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE vat2    AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact    AS DECIMAL NO-UNDO.
DEF BUFFER hbline FOR vhp.h-bill-line.
DEF BUFFER hart   FOR vhp.h-artikel.
  FOR EACH vat-list:
      DELETE vat-list.
  END.
  FOR EACH hbline WHERE hbline.rechnr = vhp.h-bill.rechnr
      AND hbline.departement = vhp.h-bill.departement NO-LOCK,
      FIRST hart WHERE hart.artnr = hbline.artnr
      AND hart.departement = hbline.departement 
      AND hart.artart = 0 NO-LOCK:
      FIND FIRST artikel WHERE artikel.artnr = hart.artnrfront
          AND artikel.departement = hart.departement NO-LOCK.
      FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code
          NO-LOCK NO-ERROR.
      IF NOT AVAILABLE htparam THEN
      DO:
          FIND FIRST vat-list WHERE vat-list.vatProz = 0 NO-ERROR.
          IF NOT AVAILABLE vat-list THEN CREATE vat-list.
          ASSIGN vat-list.netto = vat-list.netto + hbline.betrag.
      END.
      ELSE
      DO:
/* SY AUG 13 2017 */
         RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            ?, OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
          ASSIGN vat = vat + vat2.
          FIND FIRST vat-list WHERE vat-list.vatProz = vat * 100 
              NO-ERROR.
          IF NOT AVAILABLE vat-list THEN
          DO:
              CREATE vat-list.
              ASSIGN vat-list.vatProz = vat * 100.               
          END.
      END.
  END.
  FOR EACH vat-list:
    RUN cal-vatamt(vat-list.vatProz, OUTPUT vat-list.vatAmt, 
         OUTPUT vat-list.netto, OUTPUT vat-list.betrag,
         OUTPUT vat-list.fbetrag).
  END.
  amount = 0.
  FOR EACH vat-list:
     IF vat-list.betrag = 0 THEN DELETE vat-list.
  END.
END.


PROCEDURE update-bill-umsatz:
DEF BUFFER hbline FOR vhp.h-bill-line.
DEF BUFFER hart   FOR vhp.h-artikel.
DEF BUFFER foart  FOR vhp.artikel.
        
  FOR EACH hbline WHERE hbline.departement = vhp.h-bill.departement
      AND hbline.rechnr = vhp.h-bill.rechnr AND hbline.artnr NE 0 NO-LOCK,
    FIRST hart WHERE hart.artnr = hbline.artnr 
      AND hart.departement = hbline.departement AND hart.artart = 0 NO-LOCK,
    FIRST foart WHERE foart.artnr = hart.artnrfront 
      AND foart.departement = hart.departement AND foart.artart = 0 NO-LOCK:
      
    IF foart.umsatzart = 3 OR foart.umsatzart = 5 OR foart.umsatzart = 6 THEN
    DO:
        ASSIGN vhp.bill.f-b-umsatz = vhp.bill.f-b-umsatz + hbline.betrag.
    END.
    ELSE ASSIGN vhp.bill.sonst-umsatz = vhp.bill.sonst-umsatz + hbline.betrag.
  END.
  ASSIGN
    vhp.bill.gesamtumsatz = vhp.bill.gesamtumsatz + vhp.h-bill.gesamtumsatz 
    vhp.bill.saldo = vhp.bill.saldo + amount
  .
END.


PROCEDURE cal-vatamt:
DEF INPUT  PARAMETER vatProz AS DECIMAL.
DEF OUTPUT PARAMETER mwst    AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER netto   AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER betrag  AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER fbetrag AS DECIMAL INITIAL 0.
DEF VARIABLE h-service    AS DECIMAL.
DEF VARIABLE h-mwst       AS DECIMAL.
DEF VARIABLE vat2         AS DECIMAL NO-UNDO.
DEF VARIABLE fact         AS DECIMAL.
DEF VARIABLE fact1        AS DECIMAL.
DEF VARIABLE qty          AS DECIMAL.   
DEF VARIABLE unit-price   AS DECIMAL.
DEF VARIABLE amount       AS DECIMAL.
DEF VARIABLE incl-mwst    AS LOGICAL.
DEF VARIABLE disc-art1    AS INTEGER NO-UNDO. 
DEF VARIABLE vatInd       AS INTEGER NO-UNDO.
DEF VARIABLE vatStr       AS CHAR.
DEF VARIABLE locStr       AS CHAR.
DEF VARIABLE sourceStr    AS CHAR.

DEF BUFFER hbline FOR vhp.h-bill-line.
DEF BUFFER hart   FOR vhp.h-artikel.

  FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
  incl-mwst = vhp.htparam.flogical.

  FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
  disc-art1 = vhp.htparam.finteger. 

  vatStr = "VAT%," + STRING(vatProz * 100) + ";".

  FOR EACH hbline WHERE hbline.rechnr = vhp.h-bill.rechnr  
    AND hbline.departement = vhp.h-bill.departement NO-LOCK,
    FIRST hart WHERE hart.artnr = hbline.artnr 
    AND hart.departement = hbline.departement 
    AND hart.artart = 0 NO-LOCK:


   
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = hart.mwst-code
        NO-LOCK NO-ERROR.

    IF AVAILABLE vhp.htparam THEN
    DO:
      IF hart.artnr = disc-art1 THEN
      DO:
        FIND FIRST vhp.h-journal 
        WHERE vhp.h-journal.departement = hbline.departement
          AND vhp.h-journal.bill-datum = hbline.bill-datum
          AND vhp.h-journal.rechnr = hbline.rechnr
          AND vhp.h-journal.artnr = hbline.artnr
          AND vhp.h-journal.zeit = hbline.zeit NO-LOCK NO-ERROR.
        IF AVAILABLE vhp.h-journal THEN 
        DO:
          ASSIGN
            sourceStr = vhp.h-journal.aendertext
            vatInd = INDEX(sourceStr, vatStr)
          .
          IF vhp.htparam.fdecimal = vatProz AND sourceStr = "" THEN
          ASSIGN netto   = netto   + hbline.nettobetrag
                 betrag  = betrag  + hbline.betrag
                 fbetrag = fbetrag + hbline.fremdwbetrag
                 mwst    = mwst    + vhp.h-journal.steuercode / 100
          . 
          ELSE DO WHILE vatInd GT 0:
            locStr = SUBSTR(sourceStr, vatInd + LENGTH(vatStr)).
            RUN get-vat(locStr, INPUT-OUTPUT mwst, INPUT-OUTPUT netto,
                        INPUT-OUTPUT betrag, INPUT-OUTPUT fbetrag).
            sourceStr = locStr.
            vatInd = INDEX(sourceStr, vatStr).
          END.
        END. /* available h-journal */
      END.   /* artnr = disc-art1   */
      ELSE IF vhp.htparam.fdecimal = vatProz THEN
      DO:
        ASSIGN netto   = netto   + hbline.nettobetrag
               betrag  = betrag  + hbline.betrag
               fbetrag = fbetrag + hbline.fremdwbetrag
        .
        ASSIGN
            h-service = 0
            h-mwst    = 0 
            fact      = 1
            qty       = hbline.anzahl
          .
        IF qty LT 0 THEN qty = - qty.

        IF incl-mwst THEN 
        DO: 
/* SY AUG 13 2017 */
          FIND FIRST artikel WHERE artikel.artnr = hart.artnrfront
              AND artikel.departement = hart.departement NO-LOCK.      
          RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
            ?, OUTPUT h-service, OUTPUT h-mwst, OUTPUT vat2, OUTPUT fact).
          ASSIGN h-mwst = h-mwst + vat2.
/*
            fact = 0. 
            IF hart.service-code NE 0 THEN 
            DO: 
              FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr  
                = hart.service-code NO-LOCK. 
              IF vhp.htparam.fdecimal NE 0 THEN fact = vhp.htparam.fdecimal / 100.  
            END. 
            IF hart.mwst-code NE 0 THEN 
            DO: 
              FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr  
                = hart.mwst-code NO-LOCK. 
              IF vhp.htparam.fdecimal NE 0 THEN 
              DO: 
                fact1 = vhp.htparam.fdecimal. 
                FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
                IF vhp.htparam.flogical  /* service taxable */ THEN 
                  fact = fact + (1 + fact) * fact1 / 100. 
                ELSE fact = fact + fact1 / 100.  
              END. 
            END.
            fact = 1 + fact. 
*/
          END. 
 
          amount = hbline.epreis * qty.  
          IF hbline.betrag GT 0 AND amount LT 0 THEN amount = - amount.
          ELSE IF hbline.betrag LT 0 AND amount GT 0 THEN amount = - amount.

          unit-price = hbline.epreis / fact.
          IF incl-mwst THEN 
          DO:
            IF qty NE 0 THEN unit-price = (hbline.betrag / qty) / fact. 
            ELSE unit-price = hbline.betrag / fact.
          END.
          IF unit-price LT 0 THEN unit-price = - unit-price.
/*
          IF hart.service-code NE 0 THEN 
          DO: 
            FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr  
              = hart.service-code NO-LOCK. 
            IF vhp.htparam.fdecimal NE 0 THEN 
            DO: 
              h-service = unit-price * vhp.htparam.fdecimal / 100.  
              h-service = ROUND(h-service, 2).  
            END. 
          END.  
          IF hart.mwst-code NE 0 THEN 
          DO: 
            FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr  
              = hart.mwst-code NO-LOCK. 
            IF vhp.htparam.fdecimal NE 0 THEN 
            DO: 
              h-mwst = vhp.htparam.fdecimal. 
              FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
              IF vhp.htparam.flogical  /* service taxable */ 
                THEN h-mwst = h-mwst * (unit-price + h-service) / 100. 
              ELSE h-mwst = h-mwst * unit-price / 100.  
              h-mwst = ROUND(h-mwst * qty, price-decimal). 
            END. 
          END. 
*/ 
/* SY AUG 13 2017 */
          ASSIGN
            h-service = ROUND(h-service * unit-price, price-decimal)
            h-mwst    = ROUND (h-mwst * unit-price, price-decimal)
          .

          IF h-service = 0 AND h-mwst = 0 THEN . 
          ELSE IF NOT incl-mwst THEN 
          DO: 
            if h-service = 0 THEN h-mwst = hbline.betrag - amount.  
          END. 
 
          IF hbline.betrag GT 0 AND h-mwst LT 0 THEN h-mwst = - h-mwst.
          ELSE IF hbline.betrag LT 0 AND h-mwst GT 0 THEN h-mwst = - h-mwst.
          mwst = mwst + h-mwst.  
      END.   /* htparam.fdecimal = vatProz */
    END.
  END.
END.


PROCEDURE get-vat:
DEF INPUT PARAMETER curr-str       AS CHAR.
DEF INPUT-OUTPUT PARAMETER mwst    AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER netto   AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER betrag  AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER fbetrag AS DECIMAL.
DEF VAR ind                        AS INTEGER NO-UNDO.
DEF VAR tokcounter                 AS INTEGER NO-UNDO.
DEF VAR mesStr                     AS CHAR    NO-UNDO.
DEF VAR mesToken                   AS CHAR    NO-UNDO.
DEF VAR mesValue                   AS CHAR    NO-UNDO.
  ind = INDEX(curr-str, "VAT%").
  IF ind GT 0 THEN curr-str = SUBSTR(curr-str, 1, ind - 1).
  DO tokcounter = 1 TO NUM-ENTRIES(curr-str, ";") - 1:
    ASSIGN
      mesStr   = ENTRY(tokcounter, curr-str, ";")
      mesToken = ENTRY(1, mesStr, ",")
      mesValue = ENTRY(2, mesStr, ",")
    .
    CASE mesToken:
        WHEN "VAT"  THEN mwst    = mwst    + DECIMAL(mesValue) / 100.
        WHEN "NET"  THEN netto   = netto   + DECIMAL(mesValue) / 100.
        WHEN "AMT"  THEN betrag  = betrag  + DECIMAL(mesValue) / 100.
        WHEN "FAMT" THEN fbetrag = fbetrag + DECIMAL(mesValue) / 100.
    END CASE.
  END.
END.

PROCEDURE update-selforder:
    DEFINE BUFFER paramqsy FOR queasy.
    DEFINE BUFFER searchbill FOR queasy.
    DEFINE BUFFER genparamso FOR queasy.
    DEFINE BUFFER orderbill FOR queasy.
    DEFINE BUFFER orderbilline FOR queasy.
    DEFINE BUFFER orderbill-close FOR queasy.
    DEFINE BUFFER pickup-table FOR queasy.
    DEFINE BUFFER qpayment-gateway FOR queasy.

    DEFINE VARIABLE found-bill AS INT.
    DEFINE VARIABLE session-parameter AS CHAR.
    
    DEFINE VARIABLE mess-str AS CHAR.
    DEFINE VARIABLE i-str AS INT.
    DEFINE VARIABLE mess-token AS CHAR.
    DEFINE VARIABLE mess-keyword AS CHAR.
    DEFINE VARIABLE mess-value AS CHAR.

    DEFINE VARIABLE dynamic-qr AS LOGICAL.
    DEFINE VARIABLE room-serviceflag AS LOGICAL.

    /*SEARCH EVERY VALUE IN GENPARAM FOR SELFORDER*/
    FOR EACH genparamso WHERE genparamso.KEY EQ 222 
        AND genparamso.number1 EQ 1 
        AND genparamso.betriebsnr EQ curr-dept NO-LOCK:
        IF genparamso.number2 EQ 14 THEN dynamic-qr = genparamso.logi1.
        IF genparamso.number2 EQ 21 THEN room-serviceflag = genparamso.logi1.
    END.
    
    /*SEARCH SESSION PARAMETER BASED ON BILL NUMBER*/
    FOR EACH searchbill WHERE searchbill.KEY EQ 225 
        AND searchbill.number1 EQ curr-dept 
        AND searchbill.char1 EQ "orderbill" NO-LOCK:

        mess-str = searchbill.char2.
        DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
            mess-token = ENTRY(i-str,mess-str,"|").
            mess-keyword = ENTRY(1,mess-token,"=").
            mess-value = ENTRY(2,mess-token,"=").
            IF mess-keyword EQ "BL" THEN
            DO: 
                found-bill = INT(mess-value).
                LEAVE.
            END.
        END.
        IF found-bill EQ get-rechnr THEN
        DO: 
            session-parameter = searchbill.char3.
            LEAVE.
        END.
    END.    
    
    /*UPDATE SESSION FROM ACTIVE TO EXPIRED*/
    DO TRANSACTION:
        FIND FIRST paramqsy WHERE paramqsy.KEY EQ 230 AND paramqsy.char1 EQ session-parameter EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE paramqsy THEN
        DO:            
            paramqsy.betriebsnr = get-rechnr.

            IF dynamic-qr THEN
            DO:
                /*SEARCH TAKEN TABLE QUEASY AND UPDATE THE FIELDS*/
                FIND FIRST pickup-table WHERE pickup-table.KEY = 225
                    AND pickup-table.char1 EQ "taken-table"
                    AND pickup-table.number1 EQ curr-dept
                    AND pickup-table.logi1 EQ YES
                    AND pickup-table.logi2 EQ YES
                    AND pickup-table.number2 EQ paramqsy.number2
                    AND ENTRY(1, pickup-table.char3, "|") EQ session-parameter EXCLUSIVE-LOCK NO-ERROR.
                IF AVAILABLE pickup-table THEN
                DO:
                    ASSIGN
                        ENTRY(1, pickup-table.char3, "|") = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").

                    FIND CURRENT pickup-table NO-LOCK.
                END.
            END.            

            /*SEARCH ORDERBILL QUEASY AND UPDATE THE FIELDS*/
            FIND FIRST orderbill WHERE orderbill.KEY EQ 225 AND orderbill.char1 EQ "orderbill" 
                AND orderbill.char3 EQ session-parameter
                AND orderbill.logi1 EQ YES
                AND orderbill.logi3 EQ YES EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE orderbill THEN 
            DO:                
                orderbill.deci1 = get-amount.
                orderbill.logi2 = NO.
                orderbill.char3 = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                orderbill.logi1 = NO.

                FOR EACH orderbill-close WHERE orderbill-close.KEY EQ 225
                    AND orderbill-close.char1 EQ "orderbill"
                    AND orderbill-close.char3 EQ session-parameter 
                    AND orderbill-close.logi1 EQ YES
                    AND orderbill-close.logi3 EQ YES EXCLUSIVE-LOCK:
                    orderbill-close.char3 = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                    ASSIGN orderbill-close.logi1 = NO.
                END.
            END.            

            IF dynamic-qr THEN paramqsy.logi1 = YES.
            ELSE
            DO:
                IF room-serviceflag THEN
                DO:
                    ASSIGN
                    paramqsy.char1      = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","")
                    paramqsy.char3      = paramqsy.char3 + "|BL=" + STRING(get-rechnr)
                    paramqsy.logi1      = YES.
                   
                END.
                ELSE
                DO:
                    CREATE queasy.
                    BUFFER-COPY paramqsy TO queasy.
                    ASSIGN 
                    queasy.char1      = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","")
                    queasy.betriebsnr = 1
                    queasy.logi1      = YES.
                END.

                /*SEARCH ORDERBILL-LINE QUEASY AND UPDATE THE FIELDS CHAR2*/
                FOR EACH orderbilline WHERE orderbilline.KEY EQ 225 
                    AND orderbilline.char1 EQ "orderbill-line"
                    AND ENTRY(4,orderbilline.char2,"|") EQ session-parameter EXCLUSIVE-LOCK:                    
                   
                    IF orderbilline.logi2 AND orderbilline.logi3 THEN /*Posting to Bill*/
                    DO:
                        orderbilline.char2 = ENTRY(1,orderbilline.char2,"|") + "|" + 
                            ENTRY(2,orderbilline.char2,"|") + "|" + 
                            ENTRY(3,orderbilline.char2,"|") + "|" + 
                            session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                    END.
                    ELSE /*Cancel from seflorder dashboard*/
                    DO:
                        IF NUM-ENTRIES(orderbilline.char3,"|") GT 8
                            AND ENTRY(9, orderbilline.char3, "|") NE "" THEN
                        DO:
                            orderbilline.char2 = ENTRY(1,orderbilline.char2,"|") + "|" + 
                                ENTRY(2,orderbilline.char2,"|") + "|" + 
                                ENTRY(3,orderbilline.char2,"|") + "|" + 
                                session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                        END.
                    END.
                END.
            END.

            /*FD June 21, 2022 => For issue payment gateway can't posting, release betriebsnr 223 to 0*/
            FIND FIRST qpayment-gateway WHERE qpayment-gateway.KEY EQ 223
                AND qpayment-gateway.char3 EQ session-parameter
                AND qpayment-gateway.betriebsnr EQ get-rechnr EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE qpayment-gateway THEN
            DO:
                qpayment-gateway.betriebsnr = 0.
                FIND CURRENT qpayment-gateway NO-LOCK.
            END.

            FIND CURRENT paramqsy NO-LOCK.
        END.        
    END.
END PROCEDURE.

PROCEDURE remove-rsv-table:
    DEFINE VARIABLE recid-q33 AS INTEGER.

    DEFINE BUFFER buffq33 FOR queasy.

    FIND FIRST queasy WHERE queasy.KEY EQ 251 AND queasy.number1 EQ rec-id-h-bill NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        recid-q33 = queasy.number2.

        FIND FIRST buffq33 WHERE RECID(buffq33) EQ recid-q33 NO-LOCK NO-ERROR.
        IF AVAILABLE buffq33 THEN
        DO:
            FIND CURRENT buffq33 EXCLUSIVE-LOCK.
            ASSIGN
                buffq33.betriebsnr = 1      /*FD Dec 13, 2022 => betriebsnr = 1 (Closed)*/
            .
            FIND CURRENT buffq33 NO-LOCK.
            RELEASE buffq33.
        END.
    END.
END PROCEDURE.
