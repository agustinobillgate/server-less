DEFINE TEMP-TABLE t-h-bill  LIKE h-bill
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE vat-list
  FIELD vatProz AS DECIMAL INITIAL 0
  FIELD vatAmt  AS DECIMAL INITIAL 0
  FIELD netto   AS DECIMAL INITIAL 0
  FIELD betrag  AS DECIMAL INITIAL 0
  FIELD fBetrag AS DECIMAL INITIAL 0.

DEF INPUT-OUTPUT PARAMETER amount LIKE vhp.bill-line.betrag.
DEF INPUT-OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.

DEF INPUT PARAMETER rec-kellner     AS INT.
DEF INPUT PARAMETER rec-h-bill      AS INT.
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER exchg-rate      AS DECIMAL.
DEF INPUT PARAMETER bilrecid        AS INT.
DEF INPUT PARAMETER value-sign      AS INTEGER.
DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER bill-date       AS DATE.
DEF INPUT PARAMETER curr-select     AS INT.
DEF INPUT PARAMETER price-decimal   AS INT.

DEF OUTPUT PARAMETER billart        AS INT.
DEF OUTPUT PARAMETER qty            AS INT.
DEF OUTPUT PARAMETER description    AS CHAR.
DEF OUTPUT PARAMETER cancel-str     AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

DEF VAR multi-vat  AS LOGICAL INITIAL NO NO-UNDO.
DEF VAR vat-amount AS DECIMAL INITIAL 0. 

FIND FIRST kellner WHERE RECID(kellner) = rec-kellner.
FIND FIRST h-bill WHERE RECID(h-bill) = rec-h-bill.
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 271 NO-LOCK. 
  IF vhp.htparam.feldtyp = 4 THEN multi-vat = vhp.htparam.flogical.

  ASSIGN
    billart        = 0
    qty            = 1 
    amount         = - amount 
    amount-foreign = - amount-foreign
  . 
  IF NOT double-currency THEN amount-foreign = amount / exchg-rate. 

/** 12/31/2007 since it is not logic to make it 0
  IF NOT double-currency THEN amount-foreign = 0. /* WHY ??? */
**/

  IF amount NE 0 THEN 
  DO TRANSACTION: 
    FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.kellner.kcredit-nr 
      AND vhp.artikel.departement = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.artikel THEN 
    DO: 
      billart = vhp.artikel.artnr. 
      description = TRIM(vhp.artikel.bezeich) 
          + " *" + STRING(vhp.h-bill.rechnr). 
    END. 
    ELSE description = "*" + STRING(vhp.h-bill.rechnr). 

    FIND FIRST vhp.bill WHERE RECID(bill) = bilrecid EXCLUSIVE-LOCK. 
    IF vhp.bill.rechnr = 0 THEN 
    DO: 
      FIND FIRST vhp.counters WHERE vhp.counters.counter-no = 3 EXCLUSIVE-LOCK. 
      vhp.counters.counter = vhp.counters.counter + 1. 
      vhp.bill.rechnr = vhp.counters.counter. 
      FIND CURRENT counter NO-LOCK. 
    END. 

    RUN update-bill-umsatz(value-sign).

    IF double-currency THEN 
      vhp.bill.mwst[99] = vhp.bill.mwst[99] + amount-foreign.  
    vhp.bill.rgdruck = 0. 

    RUN cal-vat-amount(OUTPUT vat-amount). 
    IF multi-vat THEN RUN create-vat-list(value-sign).
 
    IF multi-vat THEN
    FOR EACH vat-list:
      
      IF AVAILABLE vhp.artikel THEN 
      DO: 
        billart = vhp.artikel.artnr. 
        description = TRIM(vhp.artikel.bezeich) 
            + "[" + STRING(vat-list.vatProz) + "]"
            + " *" + STRING(vhp.h-bill.rechnr). 
      END. 
      ELSE description = "[" + STRING(vat-list.vatProz) + "]"
          + " *" + STRING(vhp.h-bill.rechnr). 

      CREATE vhp.bill-line. 
      ASSIGN 
        vhp.bill-line.rechnr       = vhp.bill.rechnr 
        vhp.bill-line.zinr         = vhp.bill.zinr 
        vhp.bill-line.artnr        = billart 
        vhp.bill-line.bezeich      = description  
        vhp.bill-line.anzahl       = 1 
        vhp.bill-line.fremdwbetrag = vat-list.fbetrag
        vhp.bill-line.betrag       = vat-list.betrag 
        vhp.bill-line.nettobetrag  = vat-list.netto
        vhp.bill-line.departement  = vhp.h-bill.departement 
        vhp.bill-line.epreis       = 0 
        vhp.bill-line.zeit         = TIME 
        vhp.bill-line.userinit     = user-init 
        vhp.bill-line.bill-datum   = bill-date 
        vhp.bill-line.orts-tax     = vat-list.vatamt 
        vhp.bill-line.origin-id = "VAT%," + STRING(vat-list.vatProz * 100) + ";"
          + "VAT," + STRING(vat-list.vatAmt * 100) + ";"
          + "NET," + STRING(vat-list.netto * 100) + ";"
      . 
      FIND CURRENT vhp.bill-line NO-LOCK. 
    
      CREATE vhp.billjournal. 
      ASSIGN
        vhp.billjournal.rechnr       = vhp.bill.rechnr 
        vhp.billjournal.zinr         = vhp.bill.zinr
        vhp.billjournal.artnr        = billart
        vhp.billjournal.anzahl       = 1 
        vhp.billjournal.fremdwaehrng = vat-list.fbetrag
        vhp.billjournal.betrag       = vat-list.betrag
        vhp.billjournal.bezeich      = description 
        vhp.billjournal.epreis       = 0
        vhp.billjournal.zeit         = TIME 
        vhp.billjournal.stornogrund  = "" 
        vhp.billjournal.userinit     = user-init 
        vhp.billjournal.bill-datum   = bill-date
      . 
      IF AVAILABLE vhp.artikel THEN 
        vhp.billjournal.departement = vhp.artikel.departement. 
      FIND CURRENT vhp.billjournal NO-LOCK. 
    END. 
    ELSE DO:
      /*
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
        vhp.bill-line.rechnr       = vhp.bill.rechnr 
        vhp.bill-line.zinr         = vhp.bill.zinr 
        vhp.bill-line.artnr        = billart 
        vhp.bill-line.bezeich      = description  
        vhp.bill-line.anzahl       = 1 
        vhp.bill-line.fremdwbetrag = amount-foreign
        vhp.bill-line.betrag       = amount 
        vhp.bill-line.departement  = vhp.h-bill.departement 
        vhp.bill-line.epreis       = 0 
        vhp.bill-line.zeit         = TIME 
        vhp.bill-line.userinit     = user-init 
        vhp.bill-line.bill-datum   = bill-date 
        vhp.bill-line.orts-tax     = vat-amount
      . 
      FIND CURRENT vhp.bill-line NO-LOCK. 
    
      CREATE vhp.billjournal. 
      ASSIGN
        vhp.billjournal.rechnr       = vhp.bill.rechnr 
        vhp.billjournal.zinr         = vhp.bill.zinr
        vhp.billjournal.artnr        = billart
        vhp.billjournal.anzahl       = 1 
        vhp.billjournal.fremdwaehrng = amount-foreign
        vhp.billjournal.betrag       = amount
        vhp.billjournal.bezeich      = description 
        vhp.billjournal.epreis       = 0
        vhp.billjournal.zeit         = TIME 
        vhp.billjournal.stornogrund  = "" 
        vhp.billjournal.userinit     = user-init 
        vhp.billjournal.bill-datum   = bill-date
      . 
      IF AVAILABLE vhp.artikel THEN 
        vhp.billjournal.departement = vhp.artikel.departement. 
      FIND CURRENT vhp.billjournal NO-LOCK. 
    END. 
    
    cancel-str = "".
  END.

  DO TRANSACTION:
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
    vhp.h-bill.flag = 1. 
    FIND CURRENT vhp.h-bill NO-LOCK. 
    FIND CURRENT vhp.bill NO-LOCK. 
  END. 

FIND CURRENT vhp.h-bill.
CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).

PROCEDURE update-bill-umsatz:
DEF INPUT PARAMETER value-sign AS INTEGER.
DEF VARIABLE do-it AS LOGICAL NO-UNDO.
DEF BUFFER hbline FOR vhp.h-bill-line.
DEF BUFFER hart   FOR vhp.h-artikel.
DEF BUFFER foart  FOR vhp.artikel.

  FOR EACH hbline WHERE hbline.departement = vhp.h-bill.departement
      AND hbline.rechnr = vhp.h-bill.rechnr 
      AND hbline.artnr NE 0 NO-LOCK,
    FIRST hart WHERE hart.artnr = hbline.artnr 
      AND hart.departement = hbline.departement
      AND hart.artart = 0 NO-LOCK,
    FIRST foart WHERE foart.artnr = hart.artnrfront 
      AND foart.departement = hart.departement
      AND foart.artart = 0 NO-LOCK:

    IF curr-select = 0 THEN do-it = YES.
    ELSE do-it = (hbline.waehrungsnr = curr-select).

    IF do-it THEN
    DO:
      IF foart.umsatzart = 3 OR foart.umsatzart = 5 
        OR foart.umsatzart = 6 THEN
      ASSIGN vhp.bill.f-b-umsatz = vhp.bill.f-b-umsatz 
        + value-sign * hbline.betrag.
      ELSE ASSIGN vhp.bill.sonst-umsatz = vhp.bill.sonst-umsatz 
        + value-sign * hbline.betrag.
      vhp.bill.gesamtumsatz = vhp.bill.gesamtumsatz 
        + value-sign * hbline.betrag.
    END.
  END.
  ASSIGN vhp.bill.saldo = vhp.bill.saldo + amount. 
END.


PROCEDURE cal-vat-amount:
DEF OUTPUT PARAMETER mwst       AS DECIMAL INITIAL 0. 
DEF VARIABLE h-service          AS DECIMAL. 
DEF VARIABLE h-mwst             AS DECIMAL. 
DEF VARIABLE vat2               AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE fact               AS DECIMAL. 
DEF VARIABLE fact1              AS DECIMAL. 
DEF VARIABLE unit-price         AS DECIMAL. 
DEF VARIABLE amount             AS DECIMAL. 
DEF VARIABLE incl-mwst          AS LOGICAL. 
DEF VARIABLE multi-vat          AS LOGICAL INITIAL NO. 
DEF VARIABLE curr-vat           AS DECIMAL INITIAL 0. 
 
DEF BUFFER hbline FOR vhp.h-bill-line. 
DEF BUFFER hart   FOR vhp.h-artikel. 

  FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
  incl-mwst = vhp.htparam.flogical. 
 
  FOR EACH hbline WHERE hbline.rechnr = vhp.h-bill.rechnr 
    AND hbline.departement = vhp.h-bill.departement 
    AND hbline.waehrungsnr = curr-select NO-LOCK, 
    FIRST hart WHERE hart.artnr = hbline.artnr 
    AND hart.departement = hbline.departement 
    AND hart.artart = 0 NO-LOCK: 
 
    ASSIGN
        h-service = 0 
        h-mwst    = 0 
        fact      = 1
    .  
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
 
    amount = hbline.epreis * hbline.anzahl. 
    unit-price = hbline.epreis / fact. 
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
      IF h-service = 0 THEN h-mwst = hbline.betrag - amount. 
    END. 
 
    IF hbline.betrag GT 0 AND h-mwst LT 0 THEN h-mwst = - h-mwst.
      ELSE IF hbline.betrag LT 0 AND h-mwst GT 0 THEN h-mwst = - h-mwst.
    mwst = mwst + h-mwst.  
  END. 
END. 


PROCEDURE create-vat-list:
DEF INPUT PARAMETER value-sign AS INTEGER.
DEF VARIABLE do-it             AS LOGICAL NO-UNDO.
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

    IF curr-select = 0 THEN do-it = YES.
    ELSE do-it = (hbline.waehrungsnr = curr-select).
    
    IF do-it THEN
    DO:
       FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = hart.mwst-code
          NO-LOCK NO-ERROR.
       IF NOT AVAILABLE vhp.htparam THEN
       DO:
           FIND FIRST vat-list WHERE vat-list.vatProz = 0 NO-ERROR.
           IF NOT AVAILABLE vat-list THEN CREATE vat-list.
           ASSIGN vat-list.netto = vat-list.netto + hbline.betrag.
       END.
       ELSE
       DO:
           FIND FIRST vat-list WHERE 
              vat-list.vatProz = vhp.htparam.fdecimal NO-ERROR.
           IF NOT AVAILABLE vat-list THEN
           DO:
              CREATE vat-list.
              ASSIGN vat-list.vatProz = vhp.htparam.fdecimal.
           END.
       END.
    END.
  END.
  FOR EACH vat-list WHERE vat-list.vatProz NE 0:
     RUN cal-vatamt(value-sign, vat-list.vatProz, OUTPUT vat-list.vatAmt, 
         OUTPUT vat-list.netto, OUTPUT vat-list.betrag,
         OUTPUT vat-list.fbetrag).
  END.
END.


PROCEDURE cal-vatamt:
DEF INPUT  PARAMETER value-sign AS INTEGER.
DEF INPUT  PARAMETER vatProz    AS DECIMAL.
DEF OUTPUT PARAMETER mwst       AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER netto      AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER betrag     AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER fbetrag    AS DECIMAL INITIAL 0.
DEF VARIABLE h-service    AS DECIMAL.
DEF VARIABLE h-mwst       AS DECIMAL.
DEF VARIABLE vat2         AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE fact         AS DECIMAL.
DEF VARIABLE fact1        AS DECIMAL.
DEF VARIABLE qty          AS DECIMAL.   
DEF VARIABLE unit-price   AS DECIMAL.
DEF VARIABLE amount       AS DECIMAL.
DEF VARIABLE incl-mwst    AS LOGICAL.
DEF VARIABLE do-it        AS LOGICAL NO-UNDO.
DEF VARIABLE disc-art1    AS INTEGER NO-UNDO. 
DEF VARIABLE vatInd       AS INTEGER NO-UNDO.
DEF VARIABLE vatStr       AS CHAR.
DEF VARIABLE locStr       AS CHAR.

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
   
    IF curr-select = 0 THEN do-it = YES.
    ELSE do-it = (hbline.waehrungsnr = curr-select).
    IF do-it THEN
    DO:
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
            vatInd = INDEX(vhp.h-journal.aendertext, vatStr).
            IF vhp.htparam.fdecimal = vatProz AND vhp.h-journal.aendertext = "" THEN
              ASSIGN netto   = netto   + value-sign * hbline.nettobetrag
                   betrag  = betrag  + value-sign * hbline.betrag
                   fbetrag = fbetrag + value-sign * hbline.fremdwbetrag
                   mwst    = mwst    + value-sign * vhp.h-journal.steuercode / 100
              . 
            ELSE IF vatInd GT 0 THEN
            DO:
              locStr = SUBSTR(vhp.h-journal.aendertext, vatInd + LENGTH(vatStr)).
              RUN get-vat(value-sign, locStr, INPUT-OUTPUT mwst, INPUT-OUTPUT netto,
                        INPUT-OUTPUT betrag, INPUT-OUTPUT fbetrag).
            END.
          END. /* available h-journal */
        END.   /* artnr = disc-art1   */
        ELSE IF vhp.htparam.fdecimal = vatProz THEN
        DO:
          ASSIGN netto   = netto   + value-sign * hbline.nettobetrag
               betrag  = betrag  + value-sign * hbline.betrag
               fbetrag = fbetrag + value-sign * hbline.fremdwbetrag
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
          mwst = mwst + value-sign * h-mwst.  
        END.   /* htparam.fdecimal = vatProz */
      END.     /* available htparam */
    END.       /* if do-it */
  END.
END.


PROCEDURE get-vat:
DEF INPUT PARAMETER value-sign     AS INTEGER.
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
        WHEN "VAT"  THEN mwst    = mwst    + value-sign * DECIMAL(mesValue) / 100.
        WHEN "NET"  THEN netto   = netto   + value-sign * DECIMAL(mesValue) / 100.
        WHEN "AMT"  THEN betrag  = betrag  + value-sign * DECIMAL(mesValue) / 100.
        WHEN "FAMT" THEN fbetrag = fbetrag + value-sign * DECIMAL(mesValue) / 100.
    END CASE.
  END.
END.
