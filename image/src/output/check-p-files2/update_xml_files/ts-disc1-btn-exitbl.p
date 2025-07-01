
DEFINE TEMP-TABLE MENU 
    FIELD artnr         AS INTEGER 
    FIELD anzahl        AS INTEGER 
    FIELD departement   AS INTEGER 
    FIELD prtflag       AS INTEGER 
    FIELD pos           AS INTEGER 
    FIELD bcolor        AS INTEGER INITIAL 1
    FIELD epreis        AS DECIMAL 
    FIELD betrag        AS DECIMAL 
    FIELD fremdwbetrag  AS DECIMAL 
    FIELD bezeich       AS CHAR 
    FIELD bez0          AS CHAR
. 
DEFINE TEMP-TABLE disc-list
    FIELD h-artnr       AS INTEGER
    FIELD bezeich       AS CHAR
    FIELD artnr         AS INTEGER
    FIELD mwst          AS INTEGER
    FIELD service       AS INTEGER
    FIELD umsatzart     AS INTEGER INITIAL 0 
    FIELD defaultFlag   AS LOGICAL INITIAL NO
    FIELD amount        AS DECIMAL INITIAL 0
    FIELD netto-amt     AS DECIMAL INITIAL 0
    FIELD service-amt   AS DECIMAL INITIAL 0
    FIELD mwst-amt      AS DECIMAL INITIAL 0
.
DEFINE TEMP-TABLE vat-list
    FIELD ArtNo   AS INTEGER INITIAL 0
    FIELD vatProz AS DECIMAL INITIAL 0
    FIELD vatAmt  AS DECIMAL INITIAL 0
    FIELD netto   AS DECIMAL INITIAL 0
    FIELD betrag  AS DECIMAL INITIAL 0
    FIELD fbetrag AS DECIMAL INITIAL 0
.


DEF INPUT PARAMETER rec-id          AS INT.
DEF INPUT PARAMETER billart         AS INT.
DEF INPUT PARAMETER dept            AS INT.
DEF INPUT PARAMETER transdate       AS DATE.
DEF INPUT PARAMETER amount          AS DECIMAL.
DEF INPUT PARAMETER DESCRIPTION     AS CHAR.
DEF INPUT PARAMETER netto-betrag    AS DECIMAL.
DEF INPUT PARAMETER exchg-rate      AS DECIMAL.
DEF INPUT PARAMETER tischnr         AS INT.
DEF INPUT PARAMETER curr-select     AS INT.
DEF INPUT PARAMETER disc-value      AS DECIMAL.
DEF INPUT PARAMETER qty             AS INT.
DEF INPUT PARAMETER cancel-str      AS CHAR.
DEF INPUT PARAMETER curr-waiter     AS INT.
DEF INPUT PARAMETER procent         AS DECIMAL.
DEF INPUT PARAMETER b-artnrfront    AS INT.
DEF INPUT PARAMETER o-artnrfront    AS INT.
DEF INPUT PARAMETER price-decimal   AS INT.
DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER TABLE FOR disc-list.
DEF INPUT PARAMETER TABLE FOR vat-list.
DEF INPUT PARAMETER TABLE FOR MENU.

/*Debug
MESSAGE 
    "rec-id        = " rec-id        SKIP 
    "billart       = " billart       SKIP
    "dept          = " dept          SKIP
    "transdate     = " transdate     SKIP
    "amount        = " amount        SKIP
    "DESCRIPTION   = " DESCRIPTION   SKIP
    "netto-betrag  = " netto-betrag  SKIP
    "exchg-rate    = " exchg-rate    SKIP
    "tischnr       = " tischnr       SKIP
    "curr-select   = " curr-select   SKIP
    "disc-value    = " disc-value    SKIP
    "qty           = " qty           SKIP
    "cancel-str    = " cancel-str    SKIP
    "curr-waiter   = " curr-waiter   SKIP
    "procent       = " procent       SKIP
    "b-artnrfront  = " b-artnrfront  SKIP
    "o-artnrfront  = " o-artnrfront  SKIP
    "price-decimal = " price-decimal SKIP
    "user-init     = " user-init     SKIP
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = billart 
    AND vhp.h-artikel.departement = dept NO-LOCK.

RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront). 
RUN update-rev-argtArt(vhp.h-artikel.artnrfront).

PROCEDURE update-bill: 
  DEFINE INPUT PARAMETER h-artart       AS INTEGER              NO-UNDO. 
  DEFINE INPUT PARAMETER h-artnrfront   AS INTEGER              NO-UNDO. 
  DEFINE VARIABLE bill-date             AS DATE                 NO-UNDO. 
  DEFINE VARIABLE curr-time             AS INTEGER              NO-UNDO.
  DEFINE VARIABLE vat-amount            AS DECIMAL              NO-UNDO.
  DEFINE VARIABLE separate-disc-flag    AS LOGICAL INITIAL NO   NO-UNDO.
  DEFINE VARIABLE amount-list           AS DECIMAL.

  amount-list = - amount.

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 281 NO-LOCK.
  IF vhp.htparam.paramgr = 19 THEN separate-disc-flag = vhp.htparam.flogical.

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 no-lock.   /* bill DATE */ 
  bill-date = vhp.htparam.fdate. 
  IF transdate NE ? THEN bill-date = transdate. 
  ELSE 
  DO: 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
    IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
  END. 

  DO TRANSACTION: 
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK NO-ERROR. 
/* 
    FIND FIRST kellner1 WHERE kellner1.kellner-nr = vhp.h-bill.kellner-nr 
      AND kellner1.departement = vhp.h-bill.departement NO-LOCK. 
*/ 
    vhp.h-bill.saldo = vhp.h-bill.saldo + amount. 
    vhp.h-bill.rgdruck = 0. 
  
    RUN cal-vat-amount(OUTPUT vat-amount).
    curr-time = TIME.
    IF NOT separate-disc-flag THEN
    DO:
      CREATE vhp.h-bill-line. 
      ASSIGN
        vhp.h-bill-line.rechnr = vhp.h-bill.rechnr
        vhp.h-bill-line.artnr = billart
        vhp.h-bill-line.bezeich = DESCRIPTION 
        vhp.h-bill-line.anzahl = 1
        vhp.h-bill-line.nettobetrag = netto-betrag        
        vhp.h-bill-line.betrag = ROUND(amount, price-decimal)
        vhp.h-bill-line.fremdwbetrag = ROUND(amount / exchg-rate, 2)        
        vhp.h-bill-line.tischnr = tischnr
        vhp.h-bill-line.departement = vhp.h-bill.departement 
        vhp.h-bill-line.zeit = curr-time
        vhp.h-bill-line.bill-datum = bill-date 
        vhp.h-bill-line.waehrungsnr = curr-select
      . 
      
      IF disc-value = 0 THEN vhp.h-bill-line.epreis = netto-betrag.
      FIND CURRENT vhp.h-bill-line NO-LOCK. 
    END.

    FOR EACH disc-list WHERE (disc-list.h-artnr = billart) OR 
        (disc-list.netto-amt NE 0):

        /*Debug
        MESSAGE 
            "h-artnr     = " disc-list.h-artnr     SKIP 
            "bezeich     = " disc-list.bezeich     SKIP
            "artnr       = " disc-list.artnr       SKIP
            "mwst        = " disc-list.mwst        SKIP
            "service     = " disc-list.service     SKIP
            "umsatzart   = " disc-list.umsatzart   SKIP
            "defaultFlag = " disc-list.defaultFlag SKIP
            "amount      = " disc-list.amount      SKIP
            "netto-amt   = " disc-list.netto-amt   SKIP
            "service-amt = " disc-list.service-amt SKIP
            "mwst-amt    = " disc-list.mwst-amt    SKIP
            VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
      IF disc-list.amount NE 0 THEN
      DO:              
        IF procent GT 0 THEN /*FDL Jan 02, 2023 => Ticket 2DA1E7*/
        DO:
            /*FDL June 23, 2023 - 2C1F34*/ 
            amount-list = amount-list + disc-list.amount.
            IF amount-list LT 0 THEN disc-list.amount = disc-list.amount - amount-list.
        END.

        IF separate-disc-flag THEN
        DO:
          CREATE vhp.h-bill-line. 
          ASSIGN
            vhp.h-bill-line.rechnr       = vhp.h-bill.rechnr
            vhp.h-bill-line.artnr        = disc-list.h-artnr
            vhp.h-bill-line.bezeich      = disc-list.bezeich 
            vhp.h-bill-line.anzahl       = 1
            vhp.h-bill-line.nettobetrag  = disc-list.netto-amt
            vhp.h-bill-line.betrag       = disc-list.amount
            vhp.h-bill-line.fremdwbetrag = ROUND(disc-list.amount / exchg-rate, price-decimal)
            vhp.h-bill-line.tischnr      = tischnr
            vhp.h-bill-line.departement  = vhp.h-bill.departement 
            vhp.h-bill-line.zeit         = curr-time
            vhp.h-bill-line.bill-datum   = bill-date 
            vhp.h-bill-line.waehrungsnr  = curr-select
          . 
          FIND CURRENT vhp.h-bill-line NO-LOCK. 
        END.

        FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = disc-list.h-artnr 
          AND vhp.h-umsatz.departement = dept 
          AND vhp.h-umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE vhp.h-umsatz THEN 
        DO: 
          CREATE vhp.h-umsatz. 
          ASSIGN
            vhp.h-umsatz.artnr = disc-list.h-artnr
            vhp.h-umsatz.datum = bill-date 
             vhp.h-umsatz.departement = dept
          . 
        END.
        ASSIGN
          vhp.h-umsatz.betrag = vhp.h-umsatz.betrag + ROUND(disc-list.amount, price-decimal) 
          vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl + qty
        . 
        FIND CURRENT vhp.h-umsatz NO-LOCK. 
        FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = disc-list.artnr 
          AND vhp.umsatz.departement = dept 
          AND vhp.umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE vhp.umsatz THEN 
        DO: 
          CREATE vhp.umsatz. 
          ASSIGN
            vhp.umsatz.artnr       = disc-list.artnr
            vhp.umsatz.datum       = bill-date
            vhp.umsatz.departement = dept 
          .
        END. 
        ASSIGN
          vhp.umsatz.betrag = vhp.umsatz.betrag + ROUND(disc-list.amount, price-decimal)
          vhp.umsatz.anzahl = vhp.umsatz.anzahl + qty
        . 
        FIND CURRENT vhp.umsatz NO-LOCK. 
      END.      
      
      CREATE vhp.h-journal. 
      ASSIGN
        vhp.h-journal.rechnr = vhp.h-bill.rechnr 
        vhp.h-journal.artnr = disc-list.h-artnr
        vhp.h-journal.anzahl = qty
        vhp.h-journal.betrag = ROUND(disc-list.amount, price-decimal)
        /*vhp.h-journal.betrag = disc-list.amount*/
        vhp.h-journal.steuercode = vat-amount
        vhp.h-journal.bezeich = disc-list.bezeich
        vhp.h-journal.tischnr = tischnr
        vhp.h-journal.departement = vhp.h-bill.departement 
        vhp.h-journal.zeit = curr-time 
        vhp.h-journal.stornogrund = cancel-str
        vhp.h-journal.kellner-nr = curr-waiter 
        vhp.h-journal.bill-datum = bill-date
        vhp.h-journal.artnrfront = h-artnrfront 
        vhp.h-journal.aendertext = ""
        vhp.h-journal.artart = h-artart
      . 

      /*Debug
      MESSAGE 
          "h-journal.rechnr  = " h-journal.rechnr  SKIP
          "h-journal.artnr   = " h-journal.artnr   SKIP
          "h-journal.anzahl  = " h-journal.anzahl  SKIP
          "h-journal.betrag  = " h-journal.betrag  SKIP
          "h-journal.bezeich = " h-journal.bezeich SKIP    
          VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
      IF disc-list.h-artnr = billart THEN
      DO:        
        ASSIGN vhp.h-journal.epreis = netto-betrag.                 
        FOR EACH vat-list:
          ASSIGN vhp.h-journal.aendertext = vhp.h-journal.aendertext
            + "VAT%," + STRING(vat-list.vatProz * 100) + ";"
            + "VAT,"  + STRING(vat-list.vatAmt  * 100) + ";"
            + "NET,"  + STRING(vat-list.netto   * 100) + ";"      
            + "AMT,"  + STRING(vat-list.betrag  * 100) + ";"      
            + "FAMT," + STRING(vat-list.fbetrag * 100) + ";".
        END.
      END.
      FIND CURRENT vhp.h-journal NO-LOCK. 

    END.       
  END. 
  cancel-str = "". 
END. 



PROCEDURE update-rev-argtArt:
DEF INPUT PARAMETER h-artnrfront AS INTEGER.
DEF VAR amount                   AS DECIMAL NO-UNDO.

  FOR EACH MENU WHERE MENU.prtflag = 1,
    FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = MENU.artnr
    AND vhp.h-artikel.departement = vhp.h-bill.departement NO-LOCK,
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront
    AND vhp.artikel.departement = vhp.h-artikel.departement
    AND vhp.artikel.artart = 9 AND vhp.artikel.artgrp NE 0 NO-LOCK:
    amount = - procent / 100 * MENU.betrag.
    RUN rev-bdown(h-artnrfront, menu.anzahl, amount).
  END.
END.


PROCEDURE rev-bdown: 
DEFINE INPUT PARAMETER h-artnrfront AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER qty          AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER amount       AS DECIMAL NO-UNDO.
DEFINE VARIABLE discArt             AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-date           AS DATE    NO-UNDO.
DEFINE VARIABLE rest-betrag         AS DECIMAL NO-UNDO. 
DEFINE VARIABLE argt-betrag         AS DECIMAL NO-UNDO. 
DEFINE BUFFER   artikel1            FOR vhp.artikel.

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
  ASSIGN rest-betrag = amount 
     bill-date       = vhp.htparam.fdate
  . 
  IF transdate NE ? THEN bill-date = transdate. 
  ELSE 
  DO: 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
    IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
  END. 

  IF vhp.artikel.umsatzart = 3 OR vhp.artikel.umsatzart = 5 THEN
      discArt = h-artnrfront.
  ELSE IF vhp.artikel.umsatzart = 6 THEN 
  DO:    
      IF b-artnrfront NE 0 THEN discArt = b-artnrfront.
      ELSE discArt = h-artnrfront.
  END.
  ELSE 
  DO:    
      IF o-artnrfront NE 0 THEN discArt = o-artnrfront.
      ELSE discArt = h-artnrfront.
  END.

  FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = discArt
    AND vhp.umsatz.departement = vhp.artikel.departement 
    AND vhp.umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.umsatz THEN 
  DO: 
    CREATE vhp.umsatz. 
    ASSIGN
      vhp.umsatz.artnr       = discArt
      vhp.umsatz.datum       = bill-date
      vhp.umsatz.departement = vhp.artikel.departement
    . 
  END.
  ASSIGN vhp.umsatz.betrag = vhp.umsatz.betrag - amount.
  FIND CURRENT vhp.umsatz NO-LOCK.

  ASSIGN rest-betrag = amount.
  FIND FIRST vhp.arrangement WHERE vhp.arrangement.argtnr 
    = vhp.artikel.artgrp NO-LOCK. 
  FOR EACH vhp.argt-line WHERE vhp.argt-line.argtnr 
    = vhp.arrangement.argtnr NO-LOCK: 
    IF vhp.argt-line.betrag NE 0 THEN 
    ASSIGN
      argt-betrag = - procent / 100 * vhp.argt-line.betrag * qty
      argt-betrag = ROUND(argt-betrag, price-decimal)
      rest-betrag = rest-betrag - argt-betrag
    .
    ELSE 
    ASSIGN 
      argt-betrag = amount * vhp.argt-line.vt-percnt / 100
      argt-betrag = ROUND(argt-betrag, price-decimal) 
      rest-betrag = rest-betrag - argt-betrag
    . 

    
    FIND FIRST artikel1 WHERE artikel1.artnr = vhp.argt-line.argt-artnr 
      AND artikel1.departement = vhp.argt-line.departement NO-LOCK. 
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.argt-line.argt-artnr
      AND vhp.umsatz.departement = vhp.argt-line.departement 
      AND vhp.umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.umsatz THEN 
    DO: 
      CREATE vhp.umsatz. 
      ASSIGN
        vhp.umsatz.artnr       = vhp.argt-line.argt-artnr
        vhp.umsatz.datum       = bill-date
        vhp.umsatz.departement = vhp.argt-line.departement
      . 
    END.
    ASSIGN vhp.umsatz.betrag = vhp.umsatz.betrag + argt-betrag.
    FIND CURRENT vhp.umsatz NO-LOCK.

    CREATE vhp.billjournal. 
    ASSIGN
      vhp.billjournal.rechnr        = vhp.h-bill.rechnr
      vhp.billjournal.artnr         = artikel1.artnr
      vhp.billjournal.anzahl        = 1
      vhp.billjournal.fremdwaehrng  = vhp.argt-line.betrag
      vhp.billjournal.betrag        = argt-betrag
      vhp.billjournal.bezeich       = artikel1.bezeich 
        + "<" + STRING(vhp.h-bill.departement,"99") + ">"
      vhp.billjournal.departement   = artikel1.departement 
      vhp.billjournal.epreis        = 0
      vhp.billjournal.zeit          = TIME 
      vhp.billjournal.userinit      = user-init
      vhp.billjournal.bill-datum    = bill-date
    . 
    FIND CURRENT vhp.billjournal NO-LOCK. 
  END. 
 
  FIND FIRST artikel1 WHERE artikel1.artnr = vhp.arrangement.artnr-logis 
    AND artikel1.departement = vhp.arrangement.intervall NO-LOCK. 
  FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = artikel1.artnr 
    AND vhp.umsatz.departement = artikel1.departement 
    AND vhp.umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.umsatz THEN 
  DO: 
    CREATE vhp.umsatz. 
    ASSIGN
      vhp.umsatz.artnr       = artikel1.artnr
      vhp.umsatz.datum       = bill-date
      vhp.umsatz.departement = artikel1.departement
    . 
  END.
  ASSIGN vhp.umsatz.betrag = vhp.umsatz.betrag + rest-betrag. 
  FIND CURRENT vhp.umsatz NO-LOCK. 
    
  CREATE vhp.billjournal. 
  ASSIGN
    vhp.billjournal.rechnr      = vhp.h-bill.rechnr
    vhp.billjournal.artnr       = artikel1.artnr
    vhp.billjournal.anzahl      = 1
    vhp.billjournal.betrag      = rest-betrag 
    vhp.billjournal.bezeich     = artikel1.bezeich
      + "<" + STRING(vhp.h-bill.departement,"99") + ">"
    vhp.billjournal.departement = artikel1.departement 
    vhp.billjournal.epreis      = 0
    vhp.billjournal.zeit        = TIME 
    vhp.billjournal.userinit    = user-init
    vhp.billjournal.bill-datum  = bill-date
  . 
  FIND CURRENT vhp.billjournal NO-LOCK. 
END. 


PROCEDURE cal-vat-amount:
DEF OUTPUT PARAMETER mwst AS DECIMAL INITIAL 0.
DEF VARIABLE h-service    AS DECIMAL.
DEF VARIABLE h-mwst       AS DECIMAL.
DEF VARIABLE vat2         AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE fact         AS DECIMAL.
DEF VARIABLE fact1        AS DECIMAL.
DEF VARIABLE qty          AS DECIMAL.   
DEF VARIABLE unit-price   AS DECIMAL.
DEF VARIABLE menu-amt     AS DECIMAL.
DEF VARIABLE famount      AS DECIMAL.
DEF VARIABLE incl-mwst    AS LOGICAL.
DEF VARIABLE anz-vat      AS INTEGER INITIAL 0.

DEF BUFFER hart     FOR vhp.h-artikel.
DEF BUFFER foart    FOR vhp.artikel.
DEF BUFFER vathtp   FOR vhp.htparam.

  FOR EACH vat-list:
      DELETE vat-list.
  END.

  FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
  incl-mwst = vhp.htparam.flogical.

  ASSIGN famount = ROUND(amount / exchg-rate, 2).

  FOR EACH MENU WHERE MENU.prtflag = 1 NO-LOCK:
    FIND FIRST hart WHERE hart.artnr = MENU.artnr 
      AND hart.departement = MENU.departement 
      AND hart.artart = 0 NO-LOCK.
   
    FIND FIRST foart WHERE foart.artnr = hart.artnrfront
        AND foart.departement = hart.departement NO-LOCK.

    ASSIGN
        h-service   = 0 
        h-mwst      = 0 
        fact        = 1
        qty         = MENU.anzahl
    .
    IF qty LT 0 THEN qty = - qty.

    RELEASE vathtp.

    IF incl-mwst THEN 
    DO: 
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
        FIND FIRST vathtp WHERE vathtp.paramnr = hart.mwst-code NO-LOCK. 
        IF vathtp.fdecimal NE 0 THEN 
        DO:
          fact1 = vathtp.fdecimal. 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
          IF vhp.htparam.flogical  /* service taxable */ THEN 
            fact = fact + (1 + fact) * fact1 / 100. 
          ELSE fact = fact + fact1 / 100.  
        END. 
      END.
      fact = 1 + fact. 
*/      
/* SY AUG 13 2017 */
      RUN calc-servtaxesbl.p(1, foart.artnr, foart.departement,
        ?, OUTPUT h-service, OUTPUT h-mwst, OUTPUT vat2, OUTPUT fact).
      ASSIGN h-mwst = h-mwst + vat2.
    END. 
 
    menu-amt = MENU.epreis * qty.  
    IF MENU.betrag GT 0 AND menu-amt LT 0 THEN menu-amt = - menu-amt.
    ELSE IF MENU.betrag LT 0 AND menu-amt GT 0 THEN menu-amt = - menu-amt.

    unit-price = MENU.epreis.
    IF incl-mwst THEN
    DO:
      IF qty NE 0 THEN unit-price = (MENU.betrag / qty) / fact. 
      ELSE unit-price = MENU.epreis / fact.
      unit-price = ROUND(unit-price, price-decimal).
    END.
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
 
    IF foart.mwst-code NE 0 THEN 
    DO: 
      FIND FIRST vathtp WHERE vathtp.paramnr = foart.mwst-code NO-LOCK. 
      IF vathtp.fdecimal NE 0 THEN 
      DO: 
        h-mwst = vathtp.fdecimal. 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
        IF vhp.htparam.flogical  /* service taxable */ 
          THEN h-mwst = h-mwst * (unit-price + h-service) / 100. 
        ELSE h-mwst = h-mwst * unit-price / 100.  
        h-mwst = ROUND(h-mwst * qty, price-decimal). 
      END. 
    END. 
    h-service = ROUND(h-service, price-decimal).
*/
/* SY AUG 13 2017 */
    ASSIGN
        h-service = ROUND(h-service * unit-price, price-decimal)
        h-mwst    = ROUND (h-mwst * unit-price, price-decimal)
    .
    
    IF h-service = 0 AND h-mwst = 0 THEN . 
    ELSE IF NOT incl-mwst THEN 
    DO: 
      IF h-service = 0 THEN h-mwst = MENU.betrag - menu-amt.  
    END. 
 
    IF MENU.betrag GT 0 AND h-mwst LT 0 THEN h-mwst = - h-mwst.
    ELSE IF MENU.betrag LT 0 AND h-mwst GT 0 THEN h-mwst = - h-mwst.
    mwst = mwst - h-mwst.  
  
    IF h-mwst NE 0 AND AVAILABLE vathtp THEN
    DO:
        FIND FIRST vat-list WHERE vat-list.artNo = foart.artnr NO-ERROR.
        IF NOT AVAILABLE vat-list THEN
        DO:
            CREATE vat-list.
            ASSIGN vat-list.artNo = foart.artnr.
            IF AVAILABLE vathtp THEN vat-list.vatProz = vathtp.fdecimal.
        END.
        ASSIGN 
            vat-list.vatamt = vat-list.vatamt - h-mwst * procent / 100
            vat-list.betrag = vat-list.betrag - MENU.betrag * procent / 100
        .
    END.
  END.   
  ASSIGN
    mwst = mwst * procent / 100.
  FOR EACH vat-list:
    ASSIGN 
        vat-list.vatAmt  = ROUND(vat-list.vatAmt, price-decimal)
        vat-list.netto   = vat-list.betrag - vat-list.vatAmt
        vat-list.fbetrag = ROUND(vat-list.betrag / exchg-rate, 2)
    .
  END.
END.
