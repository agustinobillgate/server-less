/*FD Dec 07, 2021 => Add validation for use tax service art fo or resto*/

DEF TEMP-TABLE t-kellner1   LIKE vhp.kellner.

DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE submenu-list 
  FIELD menurecid    AS INTEGER 
  FIELD zeit         AS INTEGER 
  FIELD nr           AS INTEGER 
  FIELD artnr        LIKE vhp.h-artikel.artnr 
  FIELD bezeich      LIKE vhp.h-artikel.bezeich 
  FIELD anzahl       AS INTEGER 
  FIELD zknr         AS INTEGER 
  FIELD request      AS CHAR. 

DEF INPUT PARAMETER pvILanguage             AS INTEGER NO-UNDO.
DEF INPUT PARAMETER rec-id                  AS INT.
DEF INPUT PARAMETER rec-id-h-artikel        AS INT.
DEF INPUT PARAMETER deptname                AS CHAR.
DEF INPUT PARAMETER transdate               AS DATE.
DEF INPUT PARAMETER h-artart                AS INT.
DEF INPUT PARAMETER cancel-order            AS LOGICAL.
DEF INPUT PARAMETER h-artikel-service-code  AS INT.
DEF INPUT PARAMETER amount                  LIKE vhp.bill-line.betrag.
DEF INPUT PARAMETER amount-foreign          LIKE vhp.bill-line.betrag.
DEF INPUT PARAMETER price                   AS DECIMAL.
DEF INPUT PARAMETER double-currency         AS LOGICAL.
DEF INPUT PARAMETER qty                     AS INT.
DEF INPUT PARAMETER exchg-rate              AS DECIMAL.
DEF INPUT PARAMETER price-decimal           AS INT.
DEF INPUT PARAMETER order-taker             AS INT.
DEF INPUT PARAMETER tischnr                 AS INT.
DEF INPUT PARAMETER curr-dept               AS INT.
DEF INPUT PARAMETER curr-waiter             AS INT.
DEF INPUT PARAMETER gname                   AS CHAR.
DEF INPUT PARAMETER pax                     AS INT.
DEF INPUT PARAMETER kreditlimit             AS DECIMAL.
DEF INPUT PARAMETER add-zeit                AS INT.
DEF INPUT PARAMETER billart                 AS INT.
DEF INPUT PARAMETER description             AS CHAR.
DEF INPUT PARAMETER change-str              AS CHAR.
DEF INPUT PARAMETER cc-comment              AS CHAR.
DEF INPUT PARAMETER cancel-str              AS CHAR.
DEF INPUT PARAMETER req-str                 AS CHAR.
DEF INPUT PARAMETER voucher-str             AS CHAR.
DEF INPUT PARAMETER hoga-card               AS CHAR.
DEF INPUT PARAMETER print-to-kitchen        AS LOGICAL.
DEF INPUT PARAMETER from-acct               AS LOGICAL.
DEF INPUT PARAMETER h-artnrfront            AS INT.
DEF INPUT PARAMETER pay-type                AS INT.
DEF INPUT PARAMETER guestnr                 AS INT.
DEF INPUT PARAMETER transfer-zinr           AS CHAR.
DEF INPUT PARAMETER curedept-flag           AS LOGICAL.
DEF INPUT PARAMETER foreign-rate            AS LOGICAL.
DEF INPUT PARAMETER curr-room               AS CHAR.
DEF INPUT PARAMETER user-init               AS CHAR.

DEF INPUT PARAMETER hoga-resnr              AS INTEGER.
DEF INPUT PARAMETER hoga-reslinnr           AS INTEGER.
DEF INPUT PARAMETER incl-vat                AS LOGICAL. /*tambah disini ITA*/
DEF INPUT PARAMETER get-price               AS INTEGER. /*tambah disini ITA*/
DEF INPUT PARAMETER mc-str                  AS CHAR. /*tambah disini ITA*/

DEF INPUT PARAMETER TABLE FOR submenu-list.

DEF OUTPUT PARAMETER bill-date              AS DATE.
DEF OUTPUT PARAMETER cancel-flag            AS LOGICAL.
DEF OUTPUT PARAMETER fl-code                AS INT INIT 0.
DEF OUTPUT PARAMETER mwst                   LIKE vhp.h-bill-line.betrag INIT 0.
DEF OUTPUT PARAMETER mwst-foreign           LIKE vhp.h-bill-line.betrag INIT 0.
DEF OUTPUT PARAMETER rechnr                 AS INT.
DEF OUTPUT PARAMETER balance                AS DECIMAL.
DEF OUTPUT PARAMETER bcol                   AS INT.
DEF OUTPUT PARAMETER balance-foreign        AS DECIMAL.
DEF OUTPUT PARAMETER fl-code1               AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code2               AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code3               AS INT INIT 0.
DEF OUTPUT PARAMETER p-88                   AS LOGICAL.
DEF OUTPUT PARAMETER closed AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.
DEF OUTPUT PARAMETER TABLE FOR t-kellner1.
/*Debug for web
MESSAGE 
    "rec-id                 = " rec-id                  SKIP        
    "rec-id-h-artikel       = " rec-id-h-artikel        SKIP
    "deptname               = " deptname                SKIP
    "transdate              = " transdate               SKIP
    "h-artart               = " h-artart                SKIP
    "cancel-order           = " cancel-order            SKIP
    "h-artikel-service-code = " h-artikel-service-code  SKIP
    "amount                 = " amount                  SKIP
    "amount-foreign         = " amount-foreign          SKIP
    "price                  = " price                   SKIP
    "double-currency        = " double-currency         SKIP
    "qty                    = " qty                     SKIP
    "exchg-rate             = " exchg-rate              SKIP
    "price-decimal          = " price-decimal           SKIP
    "order-taker            = " order-taker             SKIP
    "tischnr                = " tischnr                 SKIP
    "curr-dept              = " curr-dept               SKIP
    "curr-waiter            = " curr-waiter             SKIP
    "gname                  = " gname                   SKIP
    "pax                    = " pax                     SKIP
    "kreditlimit            = " kreditlimit             SKIP
    "add-zeit               = " add-zeit                SKIP
    "billart                = " billart                 SKIP
    "description            = " description             SKIP
    "change-str             = " change-str              SKIP
    "cc-comment             = " cc-comment              SKIP
    "cancel-str             = " cancel-str              SKIP
    "req-str                = " req-str                 SKIP
    "voucher-str            = " voucher-str             SKIP
    "hoga-card              = " hoga-card               SKIP
    "print-to-kitchen       = " print-to-kitchen        SKIP
    "from-acct              = " from-acct               SKIP
    "h-artnrfront           = " h-artnrfront            SKIP
    "pay-type               = " pay-type                SKIP
    "guestnr                = " guestnr                 SKIP
    "transfer-zinr          = " transfer-zinr           SKIP
    "curedept-flag          = " curedept-flag           SKIP
    "foreign-rate           = " foreign-rate            SKIP
    "curr-room              = " curr-room               SKIP
    "user-init              = " user-init               SKIP
    "hoga-resnr             = " hoga-resnr              SKIP
    "hoga-reslinnr          = " hoga-reslinnr           SKIP
    "incl-vat               = " incl-vat                SKIP
    "get-price              = " get-price               SKIP
    "mc-str                 = " mc-str       
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
 
{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

DEFINE VARIABLE tax       AS DECIMAL. 
DEFINE VARIABLE serv      AS DECIMAL. 
DEFINE VARIABLE h-service AS DECIMAL. 
DEFINE VARIABLE unit-price AS DECIMAL. 
DEFINE VARIABLE nett-amount-foreign LIKE vhp.h-bill-line.betrag. 

DEFINE VARIABLE h-mwst AS DECIMAL. 
DEFINE VARIABLE h-mwst-foreign AS DECIMAL. 
DEFINE VARIABLE h-service-foreign AS DECIMAL. 

DEFINE VARIABLE nett-amount LIKE vhp.h-bill-line.betrag. 
DEFINE VARIABLE subtotal LIKE vhp.h-bill.saldo. 
DEFINE VARIABLE subtotal-foreign LIKE vhp.h-bill.saldo. 
/* FD Comment => if the service value is 3 digits or more behind a comma, 
                it will be rounded to 2 digits behind 
DEFINE VARIABLE service LIKE vhp.h-bill-line.betrag INITIAL 0. 
DEFINE VARIABLE service-foreign LIKE vhp.h-bill-line.betrag INITIAL 0.
*/
DEFINE VARIABLE service AS DECIMAL NO-UNDO INIT 0.          /*FD July 27, 2021*/
DEFINE VARIABLE service-foreign AS DECIMAL NO-UNDO INIT 0.  /*FD July 27, 2021*/
DEFINE VARIABLE serv-code AS INTEGER. /*FD Dec 07, 2021*/
DEFINE VARIABLE vat-code AS INTEGER. /*FD Dec 07, 2021*/
DEFINE VARIABLE servtax-use-foart AS LOGICAL. /*FD Dec 07, 2021*/
DEFINE VARIABLE recid-h-bill-line AS INTEGER INITIAL 0. /*FD June 13, 2022*/
DEFINE VARIABLE recid-hbill AS INTEGER. /*FD*/
DEFINE VARIABLE disc-art1 AS INTEGER. /*FDL*/
DEFINE VARIABLE disc-art2 AS INTEGER. /*FDL*/
DEFINE VARIABLE disc-art3 AS INTEGER. /*FDL*/
DEFINE VARIABLE count-i   AS INTEGER. /*FDL*/

DEFINE VARIABLE sysdate   AS DATE. 
DEFINE VARIABLE zeit      AS INTEGER.
DEFINE VARIABLE condiment AS LOGICAL INITIAL NO.
DEFINE VARIABLE succed    AS LOGICAL. 
DEFINE VARIABLE active-deposit AS LOGICAL.

DEF VARIABLE serv-vat    AS LOGICAL NO-UNDO. 
DEF VARIABLE ct          AS CHAR    NO-UNDO.
DEF VARIABLE l-deci      AS INTEGER NO-UNDO INIT 2.
DEF VARIABLE vat         AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE vat2        AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE tax-vat     AS LOGICAL NO-UNDO. 
DEF VARIABLE fact-scvat  AS DECIMAL NO-UNDO INIT 1.

DEF VARIABLE get-rechnr  AS INTEGER NO-UNDO.
DEF VARIABLE get-amount  AS DECIMAL NO-UNDO.
DEF VARIABLE curr-time   AS INTEGER.

DEFINE buffer h-bline FOR vhp.h-bill-line.
DEFINE buffer kellner1 FOR kellner.
DEFINE BUFFER bbill FOR vhp.h-bill.

DEFINE buffer mjou FOR h-mjourn. 

IF gname            EQ ? THEN gname         = "".
IF description      EQ ? THEN description   = "".
IF change-str       EQ ? THEN change-str    = "".
IF cc-comment       EQ ? THEN cc-comment    = "".
IF cancel-str       EQ ? THEN cancel-str    = "".
IF req-str          EQ ? THEN req-str       = "".
IF voucher-str      EQ ? THEN voucher-str   = "".
IF hoga-card        EQ ? THEN hoga-card     = "".
IF transfer-zinr    EQ ? THEN transfer-zinr = "".
IF curr-room        EQ ? THEN curr-room     = "".
IF user-init        EQ ? THEN user-init     = "".
IF mc-str           EQ ? THEN mc-str        = "".

IF rec-id NE 0 THEN
    FIND FIRST vhp.h-bill WHERE RECID(vhp.h-bill) = rec-id NO-LOCK NO-ERROR.
FIND FIRST h-artikel WHERE RECID(h-artikel) = rec-id-h-artikel NO-ERROR.

/*FD Dec 07, 2021*/
FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN servtax-use-foart = hoteldpt.defult.

IF AVAILABLE h-artikel THEN
DO:
    IF servtax-use-foart THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
            AND artikel.departement EQ h-artikel.departement NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN
        DO:
            ASSIGN
                serv-code = artikel.service-code
                vat-code = artikel.mwst-code
            .
        END.
    END.  
    ELSE
    DO:
        ASSIGN
            serv-code = h-artikel-service-code
            vat-code = h-artikel.mwst-code
        .
    END.
END.
/*End FD*/
/*FD Nov 30, 2022 => Feature Deposit Resto*/
FIND FIRST htparam WHERE htparam.paramnr EQ 588 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN active-deposit = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr EQ 557 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art1 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 596 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art2 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 556 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art3 = htparam.finteger.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
 /* vhp.bill DATE */ 
bill-date = vhp.htparam.fdate. 
IF transdate NE ? THEN bill-date = transdate. 
ELSE 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
  IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
END. 

IF AVAILABLE vhp.h-bill AND h-artart = 0 THEN
DO:
  FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr
    AND vhp.h-bill-line.departement = vhp.h-bill.departement
    AND vhp.h-bill-line.bill-datum NE bill-date NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.h-bill-line THEN
  DO:
    fl-code = 1.
    RETURN NO-APPLY.
  END.
END.

IF cancel-order THEN FIND FIRST h-bline WHERE 
    RECID(h-bline) = RECID(vhp.h-bill-line) NO-LOCK.

ASSIGN
  nett-amount           = amount 
  nett-amount-foreign   = amount-foreign 
  h-service             = 0 
  h-mwst                = 0 
  h-service-foreign     = 0 
  h-mwst-foreign        = 0
. 

IF price = 0 THEN /* eg cash payment */ 
DO: 
  IF double-currency THEN unit-price = amount-foreign / qty. 
  ELSE unit-price = amount / qty. 
END. 
ELSE unit-price = price. 
IF h-artart = 0 THEN 
ASSIGN
  subtotal          = subtotal + nett-amount
  subtotal-foreign  = subtotal-foreign + nett-amount-foreign
.

/*
FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
IF NOT vhp.htparam.flogical /* service NOT included */ 
  AND h-artart = 0 AND AVAILABLE vhp.h-artikel 
  AND h-artikel-service-code NE 0 THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr 
    = vhp.h-artikel.service-code NO-LOCK. 
  IF vhp.htparam.fdecimal NE 0 THEN 
  DO:
    
    ASSIGN
      serv      = vhp.htparam.fdecimal / 100
      h-service  = unit-price * vhp.htparam.fdecimal / 100
    . 

    IF double-currency THEN 
    ASSIGN 
      h-service-foreign = ROUND(h-service, 5) 
      h-service         = ROUND(h-service * exchg-rate, 5)
      service-foreign   = service-foreign + h-service-foreign * qty /* EKO 28/7/2015 */
    . 
    ELSE 
    ASSIGN
      /*h-service-foreign = ROUND(h-service / exchg-rate, 2)*/ /* EKO 28/7/2015 */
      h-service         = ROUND(h-service, 5)
    . 
    ASSIGN
      service           = service + h-service * qty
      /*service-foreign   = service-foreign + h-service-foreign * qty*/ /* EKO 28/7/2015 */
    .
    
  END. 
END. 

FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
IF NOT vhp.htparam.flogical /* mwst NOT included */ 
  AND h-artart = 0 AND AVAILABLE vhp.h-artikel 
  AND vhp.h-artikel.mwst-code NE 0 THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr 
    = vhp.h-artikel.mwst-code NO-LOCK. 
  IF vhp.htparam.fdecimal NE 0 THEN 
  DO:
    ASSIGN
      tax       = vhp.htparam.fdecimal / 100
      h-mwst    = vhp.htparam.fdecimal
    . 
    
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
    IF vhp.htparam.flogical  /* service taxable */ THEN 
    ASSIGN 
      tax = tax * ( 1 + serv)
      h-mwst = unit-price * tax
    . 
    ELSE h-mwst = h-mwst * unit-price / 100. 
    
    IF double-currency THEN 
    ASSIGN
      h-mwst-foreign    = ROUND(h-mwst, price-decimal)
      h-mwst            = tax * unit-price * exchg-rate
      h-mwst            = ROUND(h-mwst, price-decimal)
    . 
    ELSE 
    ASSIGN
      h-mwst-foreign    = ROUND(h-mwst / exchg-rate, price-decimal)
      h-mwst            = ROUND(h-mwst, price-decimal)
    . 
    

    ASSIGN
      mwst          = mwst + h-mwst * qty
      mwst-foreign  = mwst-foreign + h-mwst-foreign * qty
    .
  END. 
END. */

FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
IF NOT vhp.htparam.flogical /* service NOT included */ 
  AND h-artart = 0 AND AVAILABLE vhp.h-artikel 
  AND /*h-artikel-service-code*/ serv-code NE 0 THEN 
DO: 
    FIND FIRST htparam WHERE htparam.paramnr = /*h-artikel-service-code*/ serv-code NO-LOCK
        NO-ERROR. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO:
        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
          ASSIGN service = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
        ELSE service = htparam.fdecimal.
    END.
END.

RUN htplogic.p(479, OUTPUT serv-vat).
RUN htplogic.p(483, OUTPUT tax-vat).
FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
IF NOT vhp.htparam.flogical /* mwst NOT included */ 
  AND h-artart = 0 AND /*AVAILABLE vhp.h-artikel 
  AND vhp.h-artikel.mwst-code*/ vat-code NE 0 THEN 
DO: 
    FIND FIRST htparam WHERE htparam.paramnr = /*vhp.h-artikel.mwst-code*/ vat-code NO-LOCK
        NO-ERROR. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
          ASSIGN vat = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
        ELSE vat = htparam.fdecimal.
        IF serv-vat AND NOT tax-vat THEN vat = vat + vat * service / 100.
        ELSE IF serv-vat AND tax-vat THEN vat = vat + vat * (service + vat2) / 100.
        ELSE IF NOT serv-vat AND tax-vat THEN vat = vat + vat * vat2 / 100.
        ASSIGN 
            ct     = REPLACE(STRING(vat), ".", ",")
            l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
        .
        
        IF l-deci LE 2     THEN vat = ROUND(vat, 2).
        ELSE IF l-deci = 3 THEN vat = ROUND(vat, 3).
        ELSE vat = ROUND(vat, 4).
    END. 
END.

IF h-artart = 0 THEN DO:
    
    ASSIGN
        service = service / 100
        vat     = vat / 100
        vat2    = vat2 / 100.

    ASSIGN fact-scvat = 1 + service + vat + vat2.      
    
    /*FDL Sept, 05 2024: Ticket 196BEE*/
    ASSIGN 
        ct     = REPLACE(STRING(fact-scvat), ".", ",")
        l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
    .
    
    IF l-deci LE 2 THEN fact-scvat = ROUND(fact-scvat, 2).
    ELSE IF l-deci EQ 3 THEN fact-scvat = ROUND(fact-scvat, 3).
    ELSE fact-scvat = ROUND(fact-scvat, 4).
         
    IF vat = 1 THEN 
    ASSIGN
        fact-scvat  = 1
        service     = 0
        vat2        = 0
    .
    ELSE IF vat2 = 1 THEN 
    ASSIGN
        fact-scvat = 1
        service    = 0
        vat        = 0
    .
    ELSE IF service = 1 THEN 
    ASSIGN
        fact-scvat = 1
        vat        = 0
        vat2       = 0
    .    

    tax = vat + vat2.

    FIND FIRST htparam WHERE htparam.paramnr = 135 NO-LOCK. 
    IF htparam.flogical /* service included */ THEN service = 0. 
    FIND FIRST htparam WHERE htparam.paramnr = 134 NO-LOCK. 
    IF htparam.flogical /* mwst included */ THEN tax = 0.
    ASSIGN h-service  = unit-price * service.
    IF double-currency THEN 
    ASSIGN 
      h-service-foreign = ROUND(h-service, 4) 
      h-service         = ROUND(h-service * exchg-rate, 4)
      service-foreign   = service-foreign + h-service-foreign * qty /* EKO 28/7/2015 */
    . 
    ASSIGN 
        h-service = ROUND(h-service, 4)
        service   = service + h-service * qty
    .
    ASSIGN h-mwst = unit-price * tax.
    IF double-currency THEN 
    ASSIGN
      h-mwst-foreign    = ROUND(h-mwst, 4)
      h-mwst            = tax * unit-price * exchg-rate
      h-mwst            = ROUND(h-mwst, 4)
    . 
    ELSE 
    ASSIGN
      h-mwst-foreign    = ROUND(h-mwst / exchg-rate, 4)
      h-mwst            = ROUND(h-mwst, 4)
    . 
    ASSIGN
      mwst          = mwst + h-mwst * qty
      mwst-foreign  = mwst-foreign + h-mwst-foreign * qty
    .
END.

/*FD July 01, 2021*/
IF NOT incl-vat THEN unit-price = unit-price * fact-scvat.
ELSE
DO:
    price = unit-price / fact-scvat.
    nett-amount = nett-amount / fact-scvat.
END.
    
ASSIGN  
  /* FD Comment July 01, 2021 
  unit-price        = unit-price * fact-scvat
  */
  /*
  unit-price        = ROUND(unit-price, price-decimal)*/
  amount            = unit-price * qty
  /*amount            = amount + (h-service + h-mwst) * qty*/
  amount            = ROUND(amount, price-decimal)
  /*amount            = ROUND(amount, 0)*/
  amount-foreign    = amount-foreign 
                    + (h-service-foreign + h-mwst-foreign ) * qty
.

DO TRANSACTION: 
  FIND CURRENT vhp.h-bill NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.h-bill THEN FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
  ELSE DO: 
    /*ITA 120619 -> validasi untuk check table sudah terisi atau blm*/
    FIND FIRST bbill WHERE bbill.tischnr = tischnr
         AND bbill.departement = curr-dept AND bbill.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bbill THEN DO:
        fl-code = 2.
        RETURN NO-APPLY.
    END.

    CREATE vhp.h-bill. 
    ASSIGN 
      vhp.h-bill.betriebsnr = order-taker 
      vhp.h-bill.rgdruck = 1 
      vhp.h-bill.tischnr =  tischnr 
      vhp.h-bill.departement = curr-dept 
      vhp.h-bill.kellner-nr = curr-waiter 
      vhp.h-bill.bilname = gname 
      vhp.h-bill.belegung = pax. 

    FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 31 
        AND vhp.queasy.number1 = curr-dept
        AND vhp.queasy.number2 = tischnr /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy THEN
    DO:
      FIND CURRENT vhp.queasy EXCLUSIVE-LOCK.
      ASSIGN vhp.queasy.number3 = TIME
             vhp.queasy.date1 = TODAY.
      FIND CURRENT vhp.queasy NO-LOCK.
      RELEASE vhp.queasy.
    END.
    
    IF hoga-resnr GT 0 THEN 
    DO: 
      ASSIGN 
        vhp.h-bill.resnr    = hoga-resnr 
        vhp.h-bill.reslinnr = hoga-reslinnr. 
      /*MT not supported
      IF hogatex-flag THEN 
      DO: 
        vhp.h-bill.service[2] = hoga-host. 
      END.*/
    END.

    IF hoga-reslinnr EQ 0 AND gname NE "" AND gname NE ?  THEN
    DO:
        FIND FIRST guest WHERE guest.NAME + "," + guest.vorname1 EQ gname NO-LOCK NO-ERROR.
        IF NOT AVAILABLE guest THEN
        DO:
            /*FDL March 27, 2024 => Ticket 0A9354 | D5A911*/
            FIND FIRST guest WHERE (guest.NAME + "," + guest.vorname1 + " " + guest.anrede1 EQ gname)
                OR (guest.NAME + "," + guest.vorname1 + "  " + guest.anrede1 EQ gname)
                OR (guest.NAME + "," + guest.vorname1 + "   " + guest.anrede1 EQ gname)
                OR (guest.NAME + "," + " " + guest.anrede1 EQ gname)
                OR (guest.NAME + "," + "  " + guest.anrede1 EQ gname)
                OR (guest.NAME + "," + "   " + guest.anrede1 EQ gname)
                OR (guest.NAME + "," + guest.vorname1 + " " + guest.anredefirma EQ gname)
                OR (guest.NAME + "," + guest.vorname1 + "  " + guest.anredefirma EQ gname)
                OR (guest.NAME + "," + guest.vorname1 + "   " + guest.anredefirma EQ gname)
                OR (guest.NAME + "," + " " + guest.anredefirma EQ gname)
                OR (guest.NAME + "," + "  " + guest.anredefirma EQ gname)
                OR (guest.NAME + "," + "   " + guest.anredefirma EQ gname) NO-LOCK NO-ERROR.            
        END.
            
        IF AVAILABLE guest THEN
        DO:
          ASSIGN 
             vhp.h-bill.resnr    = guest.gastnr
             vhp.h-bill.reslinnr = 0.
        END.
    END.

    FIND FIRST vhp.counters WHERE vhp.counters.counter-no = (100 + curr-dept) 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.counters THEN FIND CURRENT vhp.counters EXCLUSIVE-LOCK. 
    ELSE DO: 
      FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = curr-dept NO-LOCK. 
      create vhp.counters. 
      vhp.counters.counter-no = 100 + curr-dept. 
      vhp.counters.counter-bez = "Outlet Invoice: " + hoteldpt.depart. 
    END. 
    vhp.counters.counter = vhp.counters.counter + 1. 
    IF counters.counter GT 999999 THEN counters.counter = 1.
    FIND CURRENT counters NO-LOCK. 
    vhp.h-bill.rechnr = vhp.counters.counter. 
    rechnr = vhp.h-bill.rechnr.
    fl-code2 = 1.
    RELEASE vhp.counters.
  END. 

  /*
  IF vhp.h-bill.bilname = "" AND gname NE "" THEN 
  DO: 
    vhp.h-bill.bilname = gname. 
  END. */

  IF gname NE "" THEN DO:
        vhp.h-bill.bilname = gname. 
        IF hoga-resnr GT 0 THEN 
        DO: 
          ASSIGN 
            vhp.h-bill.resnr    = hoga-resnr 
            vhp.h-bill.reslinnr = hoga-reslinnr. 
        END.
    
        IF hoga-reslinnr = 0 AND gname NE "" THEN
        DO:
            FIND FIRST guest WHERE guest.NAME + "," + guest.vorname1 = gname NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
              ASSIGN 
                 vhp.h-bill.resnr    = guest.gastnr
                 vhp.h-bill.reslinnr = 0.
            END.
        END.
  END.
  
  FIND FIRST kellner1 WHERE kellner1.kellner-nr = vhp.h-bill.kellner-nr 
    AND kellner1.departement = curr-dept NO-LOCK NO-ERROR.
  IF AVAILABLE kellner1 THEN
  DO:
      CREATE t-kellner1.
      BUFFER-COPY kellner1 TO t-kellner1.
  END.
/* 
  FIND FIRST kellne1 WHERE kellne1.kellner-nr = vhp.h-bill.kellner-nr 
    AND kellne1.departement = curr-dept NO-LOCK NO-ERROR. 
*/ 
  IF h-artart EQ 0 THEN vhp.h-bill.gesamtumsatz 
    = vhp.h-bill.gesamtumsatz + amount. 
  balance = balance + amount. 
  IF balance LE kreditlimit THEN bcol = 2. 
/*    ELSE bcol = 12. */ 
  vhp.h-bill.saldo = vhp.h-bill.saldo + amount. 
  vhp.h-bill.mwst[99] = vhp.h-bill.mwst[99] + amount-foreign. 
  balance = vhp.h-bill.saldo. 
  balance-foreign = vhp.h-bill.mwst[99]. 
  IF balance NE 0 THEN vhp.h-bill.rgdruck = 0. 
  IF balance LE kreditlimit THEN bcol = 2. 
/*    ELSE bcol = 12. */   

  ASSIGN
    sysdate = TODAY 
    zeit    = TIME + add-zeit
  . 
  
  IF billart NE 0 THEN 
  DO: 
    FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = billart 
      AND vhp.h-umsatz.departement = curr-dept 
      AND vhp.h-umsatz.datum = bill-date NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.h-umsatz THEN FIND CURRENT vhp.h-umsatz EXCLUSIVE-LOCK. 
    ELSE DO: 
      create vhp.h-umsatz. 
      vhp.h-umsatz.artnr = billart. 
      vhp.h-umsatz.datum = bill-date. 
      vhp.h-umsatz.departement = curr-dept. 
    END. 
    vhp.h-umsatz.betrag = vhp.h-umsatz.betrag + amount. 
    vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl + qty. 
    FIND CURRENT vhp.h-umsatz NO-LOCK. 
    RELEASE vhp.h-umsatz. 
  END. 

  CREATE vhp.h-journal. 
  ASSIGN 
    vhp.h-journal.rechnr = vhp.h-bill.rechnr 
    vhp.h-journal.artnr = billart 
    vhp.h-journal.anzahl = qty 
    vhp.h-journal.fremdwaehrng = amount-foreign 
    vhp.h-journal.betrag = amount 
    vhp.h-journal.bezeich = description + change-str + cc-comment 
    vhp.h-journal.tischnr =  tischnr 
    vhp.h-journal.departement = curr-dept 
    vhp.h-journal.epreis = price 
    vhp.h-journal.zeit = zeit 
    vhp.h-journal.stornogrund = cancel-str 
    vhp.h-journal.aendertext = req-str 
    vhp.h-journal.kellner-nr = curr-waiter 
    vhp.h-journal.bill-datum = bill-date 
    vhp.h-journal.sysdate = sysdate 
    vhp.h-journal.wabkurz = voucher-str 
  . 
  IF h-artart = 11 THEN 
  DO: 
    vhp.h-journal.aendertext = gname. 
    vhp.h-journal.segmentcode = billart. 
    
    IF mc-str NE " " THEN DO:
        FIND FIRST queasy WHERE queasy.KEY = 197 AND queasy.char1 = mc-str
            AND queasy.date1 = bill-date AND queasy.number1 = billart NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN DO:
            CREATE queasy.
            ASSIGN queasy.KEY     = 197
                   queasy.char1   = mc-str
                   queasy.date1   = bill-date
                   queasy.deci1   = amount
                   queasy.number1 = billart.
        END.
        ELSE DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN queasy.deci1 = queasy.deci1 + amount.
            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
        END.    
    END.    
  END. 

  CREATE vhp.h-bill-line. 
  vhp.h-bill-line.rechnr = vhp.h-bill.rechnr. 
  vhp.h-bill-line.artnr = billart. 
  vhp.h-bill-line.bezeich = description + change-str + cc-comment. 
  vhp.h-bill-line.anzahl = qty. 
  vhp.h-bill-line.nettobetrag = nett-amount. 
  vhp.h-bill-line.fremdwbetrag = amount-foreign. 
  vhp.h-bill-line.betrag = amount. 
  vhp.h-bill-line.tischnr =  tischnr. 
  vhp.h-bill-line.departement = curr-dept. 
  vhp.h-bill-line.epreis = price. 
  vhp.h-bill-line.zeit = zeit. 
  vhp.h-bill-line.bill-datum = bill-date. 
  vhp.h-bill-line.sysdate = sysdate.   
  /*IF SUBSTR(description,1,5) = "RmNo " OR SUBSTR(description,1,5) = "Card " 
    THEN vhp.h-bill-line.segmentcode 
      = INTEGER(SUBSTR(TRIM(hoga-card),1,9)) NO-ERROR.*/ /*Eko 15/12/2015*/ 
  
  /*FD June 13, 2022 => Ticket 431485 If posting one by one with same artno and diff request,
        KP always get first request, so must add recid h-bill-line to h-journal.schankbuch as flag*/
  recid-h-bill-line = RECID(vhp.h-bill-line). 
  h-journal.schankbuch = recid-h-bill-line.

  IF AVAILABLE vhp.h-artikel AND vhp.h-artikel.artart = 0 
      AND (NOT print-to-kitchen OR from-acct) THEN
  ASSIGN vhp.h-bill-line.steuercode = 9999.

  IF AVAILABLE vhp.h-artikel AND vhp.h-artikel.artart = 0 
    AND vhp.h-artikel.betriebsnr NE 0 THEN 
  DO: 
    IF NOT cancel-order THEN 
    FOR EACH submenu-list WHERE submenu-list.nr = vhp.h-artikel.betriebsnr 
      AND submenu-list.menurecid = menurecid: 
      submenu-list.zeit = zeit. 
      CREATE vhp.h-mjourn. 
      vhp.h-mjourn.departement = curr-dept. 
      vhp.h-mjourn.rechnr = vhp.h-bill.rechnr. 
      vhp.h-mjourn.tischnr =  tischnr. 
      vhp.h-mjourn.nr = submenu-list.nr. 
      vhp.h-mjourn.artnr = submenu-list.artnr. 
      vhp.h-mjourn.h-artnr = vhp.h-artikel.artnr. 
      vhp.h-mjourn.anzahl = qty. 
      vhp.h-mjourn.zeit = zeit. 
      vhp.h-mjourn.request = submenu-list.request. 
      vhp.h-mjourn.kellner-nr = curr-waiter. 
      vhp.h-mjourn.bill-datum = bill-date. 
      vhp.h-mjourn.sysdate = sysdate. 
      FIND CURRENT vhp.h-mjourn NO-LOCK. 
      condiment = YES.
    END. 
    ELSE 
    DO: 
      FIND FIRST h-jou WHERE h-jou.artnr = h-bline.artnr 
        AND h-jou.departement = h-bline.departement 
        AND h-jou.rechnr = h-bline.rechnr 
        AND h-jou.bill-datum = h-bline.bill-datum 
        AND h-jou.zeit = h-bline.zeit 
        AND h-jou.sysdate = h-bline.sysdate NO-LOCK NO-ERROR. 
      IF AVAILABLE h-jou THEN 
      DO: 
        FOR EACH mjou WHERE mjou.departement = h-jou.departement 
          AND mjou.h-artnr = h-jou.artnr AND mjou.rechnr = h-jou.rechnr 
          AND mjou.bill-datum = h-jou.bill-datum 
          AND mjou.sysdate = h-jou.sysdate 
          AND mjou.zeit = h-jou.zeit NO-LOCK: 
          CREATE h-mjourn. 
          vhp.h-mjourn.departement = mjou.departement. 
          vhp.h-mjourn.rechnr = vhp.h-bill.rechnr. 
          vhp.h-mjourn.tischnr = tischnr. 
          vhp.h-mjourn.nr = mjou.nr. 
          vhp.h-mjourn.artnr = mjou.artnr. 
          vhp.h-mjourn.h-artnr = mjou.h-artnr. 
          vhp.h-mjourn.anzahl = qty. 
          vhp.h-mjourn.zeit = zeit. 
          vhp.h-mjourn.request = mjou.request. 
          vhp.h-mjourn.kellner-nr = curr-waiter. 
          vhp.h-mjourn.bill-datum = bill-date. 
          vhp.h-mjourn.sysdate = sysdate. 
          FIND CURRENT vhp.h-mjourn NO-LOCK. 
          condiment = YES.
        END. 
      END. 
    END. 
  END. 

  IF AVAILABLE vhp.h-artikel THEN vhp.h-journal.artart 
    = vhp.h-artikel.artart. 
  vhp.h-journal.artnrfront = h-artnrfront. 
  IF h-artart = 0 AND 
    AVAILABLE vhp.h-artikel THEN vhp.h-journal.gang = vhp.h-artikel.gang. 
  IF billart NE 0 THEN vhp.h-journal.artart = h-artart. 
  IF pay-type = 1 THEN 
  DO: 
    vhp.h-journal.segmentcode = guestnr. 
    vhp.h-journal.bon-nr = vhp.h-bill.belegung. 
  END. 
  ELSE IF pay-type = 2 THEN vhp.h-journal.zinr = transfer-zinr. 

  IF condiment THEN 
  DO: 
    ASSIGN 
      vhp.h-bill-line.betriebsnr = 1
      vhp.h-journal.betriebsnr   = 1
    .
  END.  

  FIND CURRENT vhp.h-bill-line NO-LOCK. 
  FIND CURRENT vhp.h-journal NO-LOCK. 

  IF h-artart = 0 THEN 
  DO:
    fl-code3 = 1.
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.h-artikel.artnrfront 
      AND vhp.umsatz.departement = curr-dept 
      AND vhp.umsatz.datum = bill-date NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.umsatz THEN FIND CURRENT vhp.umsatz EXCLUSIVE-LOCK. 
    ELSE DO: 
      create vhp.umsatz. 
      vhp.umsatz.artnr = vhp.h-artikel.artnrfront. 
      vhp.umsatz.datum = bill-date. 
      vhp.umsatz.departement = curr-dept. 
    END. 
    vhp.umsatz.betrag = vhp.umsatz.betrag + amount. 
    vhp.umsatz.anzahl = vhp.umsatz.anzahl + qty. 
    FIND CURRENT vhp.umsatz NO-LOCK. 
    RELEASE vhp.umsatz. 

    FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = h-artnrfront 
      AND vhp.artikel.departement = curr-dept NO-LOCK. 
    IF vhp.artikel.artart = 9 AND vhp.artikel.artgrp NE 0 THEN RUN rev-bdown.

  END. 

  ELSE IF h-artart = 11 OR h-artart = 12 THEN 
  DO: 
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.h-artikel.artnrfront 
      AND vhp.umsatz.departement = curr-dept 
      AND vhp.umsatz.datum = bill-date NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.umsatz THEN FIND CURRENT vhp.umsatz EXCLUSIVE-LOCK. 
    ELSE DO: 
      create vhp.umsatz. 
      vhp.umsatz.artnr = vhp.h-artikel.artnrfront. 
      vhp.umsatz.datum = bill-date. 
      vhp.umsatz.departement = curr-dept. 
    END. 
    vhp.umsatz.anzahl = vhp.umsatz.anzahl + vhp.h-bill.belegung. 
    FIND CURRENT vhp.umsatz NO-LOCK. 
    RELEASE vhp.umsatz. 
  END. 
  
  /*FDL Dec 2021 => Feature Resto Deposit*/
  ELSE IF h-artart = 5 THEN
  DO:
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.h-artikel.artnrfront 
      AND vhp.umsatz.departement = 0 
      AND vhp.umsatz.datum = bill-date NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.umsatz THEN FIND CURRENT vhp.umsatz EXCLUSIVE-LOCK. 
    ELSE DO: 
      create vhp.umsatz. 
      vhp.umsatz.artnr = vhp.h-artikel.artnrfront. 
      vhp.umsatz.datum = bill-date. 
      vhp.umsatz.departement = 0. 
    END. 
    vhp.umsatz.betrag = vhp.umsatz.betrag + amount. 
    vhp.umsatz.anzahl = vhp.umsatz.anzahl + 1. 
    FIND CURRENT vhp.umsatz NO-LOCK. 
    RELEASE vhp.umsatz.
  END.

  ELSE IF h-artart = 6 THEN 
  DO: 
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.h-artikel.artnrfront 
      AND vhp.umsatz.departement = 0 
      AND vhp.umsatz.datum = bill-date NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.umsatz THEN FIND CURRENT vhp.umsatz EXCLUSIVE-LOCK. 
    ELSE DO: 
      create vhp.umsatz. 
      vhp.umsatz.artnr = vhp.h-artikel.artnrfront. 
      vhp.umsatz.datum = bill-date. 
      vhp.umsatz.departement = 0. 
    END. 
    vhp.umsatz.betrag = vhp.umsatz.betrag + amount. 
    vhp.umsatz.anzahl = vhp.umsatz.anzahl + 1. 
    FIND CURRENT vhp.umsatz NO-LOCK. 
    RELEASE vhp.umsatz. 
  END. 
  FIND CURRENT vhp.h-bill NO-LOCK NO-ERROR. 

  closed = NO. 
  IF h-artart = 2 OR h-artart = 7 THEN 
  DO:
    DEFINE BUFFER bill-guest FOR vhp.guest. 
    IF guestnr = 0 THEN
    DO:
        FIND FIRST vhp.htparam WHERE htpara.paramnr = 867 NO-LOCK.
        guestnr = vhp.htparam.finteger.
    END.
    FIND FIRST bill-guest WHERE bill-guest.gastnr = /*MTvhp.htparam.finteger*/
        guestnr NO-LOCK NO-ERROR. 

    FIND FIRST vhp.artikel WHERE vhp.artikel.artnr 
      = vhp.h-artikel.artnrfront AND vhp.artikel.departement = 0 NO-LOCK. 
    IF foreign-rate AND amount-foreign = 0 THEN 
      amount-foreign = amount / exchg-rate. 
    RUN ts-restinv-rinv-arbl.p 
        (artikel.artnr, curr-dept, curr-room, bill-guest.gastnr, 
         bill-guest.gastnr, vhp.h-bill.rechnr, amount, amount-foreign, 
         bill-date, bill-guest.name, user-init, cc-comment, deptname).
  END. 
  IF h-artart = 2 OR h-artart = 7 OR h-artart = 11 
    OR h-artart = 12 THEN 
  DO:     
    IF balance = 0 THEN 
    DO: 
      closed = YES. 
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
      
      vhp.h-bill.flag = 1. 
      IF h-artart = 11 OR h-artart = 12 THEN
      DO:
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 739 NO-LOCK.
        IF vhp.htparam.flogical THEN 
        DO:
          fl-code1 = 1.
          /*MTRUN TS-voucherUI.p(OUTPUT str).
          IF str NE "" THEN ASSIGN vhp.h-bill.service[5] = DECIMAL(str).*/
        END.
      END.

      /************************online tax vanguard (pengiriman realtime)*****************/
      CREATE INTERFACE.
      ASSIGN
      INTERFACE.KEY         = 38
      INTERFACE.action      = YES
      INTERFACE.nebenstelle = ""
      INTERFACE.parameters = "close-bill"
      INTERFACE.intfield    = h-bill.rechnr
      INTERFACE.decfield    = h-bill.departement
      INTERFACE.int-time    = TIME
      INTERFACE.intdate     = TODAY
      INTERFACE.resnr       = h-bill.resnr
      INTERFACE.reslinnr    = h-bill.reslinnr
      .
      FIND CURRENT INTERFACE NO-LOCK.
      RELEASE INTERFACE.

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
      recid-hbill = RECID(h-bill).
      IF active-deposit THEN
      DO:
          RUN remove-rsv-table.
      END.
    END. 
  END.    
  succed = YES. 
END. 

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 88 NO-LOCK.
p-88 = vhp.htparam.flogical.

FIND CURRENT h-bill NO-LOCK.
CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).

PROCEDURE rev-bdown: 
DEFINE BUFFER artikel1 FOR vhp.artikel. 
DEFINE VARIABLE rest-betrag AS DECIMAL. 
DEFINE VARIABLE argt-betrag AS DECIMAL. 
  rest-betrag = amount. 
  FIND FIRST vhp.arrangement WHERE vhp.arrangement.argtnr 
    = vhp.artikel.artgrp NO-LOCK. 
  FOR EACH vhp.argt-line WHERE vhp.argt-line.argtnr 
    = vhp.arrangement.argtnr NO-LOCK: 
    IF vhp.argt-line.betrag NE 0 THEN 
    DO: 
      argt-betrag = vhp.argt-line.betrag * qty. 
      IF double-currency OR vhp.artikel.pricetab THEN 
        argt-betrag = ROUND(argt-betrag * exchg-rate, price-decimal). 
    END. 
    ELSE 
    DO: 
      argt-betrag = amount * vhp.argt-line.vt-percnt / 100. 
      argt-betrag = ROUND(argt-betrag, price-decimal). 
    END. 
    rest-betrag = rest-betrag - argt-betrag.
    
    FIND FIRST artikel1 WHERE artikel1.artnr = vhp.argt-line.argt-artnr 
      AND artikel1.departement = vhp.argt-line.departement NO-LOCK. 
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = artikel1.artnr 
      AND vhp.umsatz.departement = artikel1.departement 
      AND vhp.umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.umsatz THEN 
    DO: 
      CREATE vhp.umsatz. 
      vhp.umsatz.artnr = artikel1.artnr. 
      vhp.umsatz.datum = bill-date. 
      vhp.umsatz.departement = artikel1.departement. 
    END. 
    vhp.umsatz.betrag = vhp.umsatz.betrag + argt-betrag. 
    vhp.umsatz.anzahl = vhp.umsatz.anzahl + qty. 
    FIND CURRENT vhp.umsatz NO-LOCK.

    CREATE vhp.billjournal. 
    ASSIGN
      vhp.billjournal.rechnr = vhp.h-bill.rechnr
      vhp.billjournal.artnr = artikel1.artnr
      vhp.billjournal.anzahl = qty
      vhp.billjournal.fremdwaehrng = vhp.argt-line.betrag
      vhp.billjournal.betrag = argt-betrag
      vhp.billjournal.bezeich = artikel1.bezeich 
        + "<" + STRING(vhp.h-bill.departement,"99") + ">"
      vhp.billjournal.departement = artikel1.departement 
      vhp.billjournal.epreis = 0
      vhp.billjournal.zeit = TIME 
      vhp.billjournal.stornogrund = cancel-str
      vhp.billjournal.userinit = user-init
      vhp.billjournal.bill-datum = bill-date
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
    vhp.umsatz.artnr = artikel1.artnr. 
    vhp.umsatz.datum = bill-date. 
    vhp.umsatz.departement = artikel1.departement. 
  END. 
  vhp.umsatz.betrag = vhp.umsatz.betrag + rest-betrag. 
  vhp.umsatz.anzahl = vhp.umsatz.anzahl + qty. 
  FIND CURRENT vhp.umsatz NO-LOCK. 

  CREATE vhp.billjournal. 
  ASSIGN
    vhp.billjournal.rechnr = vhp.h-bill.rechnr
    vhp.billjournal.artnr = artikel1.artnr
    vhp.billjournal.anzahl = qty
    vhp.billjournal.betrag = rest-betrag 
    vhp.billjournal.bezeich = artikel1.bezeich
      + "<" + STRING(vhp.h-bill.departement,"99") + ">"
    vhp.billjournal.departement = artikel1.departement 
    vhp.billjournal.epreis = 0
    vhp.billjournal.zeit = TIME 
    vhp.billjournal.stornogrund = cancel-str
    vhp.billjournal.userinit = user-init
    vhp.billjournal.bill-datum = bill-date
  . 
  IF double-currency THEN 
    vhp.billjournal.fremdwaehrng = ROUND(rest-betrag / exchg-rate, 2). 
  FIND CURRENT vhp.billjournal NO-LOCK. 
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
        FIND FIRST paramqsy WHERE paramqsy.KEY EQ 230 AND paramqsy.char1 EQ session-parameter /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
        IF AVAILABLE paramqsy THEN
        DO:      
            FIND CURRENT paramqsy EXCLUSIVE-LOCK.
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
                    AND ENTRY(1, pickup-table.char3, "|") EQ session-parameter /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
                IF AVAILABLE pickup-table THEN
                DO:
                    FIND CURRENT pickup-table EXCLUSIVE-LOCK.
                    ASSIGN
                        ENTRY(1, pickup-table.char3, "|") = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").

                    FIND CURRENT pickup-table NO-LOCK.
                    RELEASE pickup-table.
                END.
            END.
            
            /*SEARCH ORDERBILL QUEASY AND UPDATE THE FIELDS*/
            FIND FIRST orderbill WHERE orderbill.KEY EQ 225 
                AND orderbill.char1 EQ "orderbill" 
                AND orderbill.char3 EQ session-parameter
                AND orderbill.logi1 EQ YES
                AND orderbill.logi3 EQ YES /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
            IF AVAILABLE orderbill THEN 
            DO:             
                FIND CURRENT orderbill EXCLUSIVE-LOCK.
                orderbill.deci1 = get-amount.
                orderbill.logi2 = NO.
                orderbill.char3 = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                orderbill.logi1 = NO.
                FIND CURRENT orderbill NO-LOCK.
                
                /* FDL Comment CHG to Find First Do while
                FOR EACH orderbill-close WHERE orderbill-close.KEY EQ 225
                    AND orderbill-close.char1 EQ "orderbill"
                    AND orderbill-close.char3 EQ session-parameter 
                    AND orderbill-close.logi1 EQ YES
                    AND orderbill-close.logi3 EQ YES EXCLUSIVE-LOCK:
                    orderbill-close.char3 = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                    ASSIGN orderbill-close.logi1 = NO.
                END.
                */
                /*FDL Ticket 3B7602*/
                FIND FIRST orderbill-close WHERE orderbill-close.KEY EQ 225
                    AND orderbill-close.char1 EQ "orderbill"
                    AND orderbill-close.char3 EQ session-parameter 
                    AND orderbill-close.logi1 EQ YES
                    AND orderbill-close.logi3 EQ YES NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE orderbill-close:

                    FIND CURRENT orderbill-close EXCLUSIVE.
                    orderbill-close.char3 = session-parameter + "T" + REPLACE(STRING(TODAY),"/","") + REPLACE(STRING(TIME,"HH:MM"),":","").
                    ASSIGN orderbill-close.logi1 = NO.
                    FIND CURRENT orderbill-close NO-LOCK.
                    RELEASE orderbill-close.

                    FIND NEXT orderbill-close WHERE orderbill-close.KEY EQ 225
                        AND orderbill-close.char1 EQ "orderbill"
                        AND orderbill-close.char3 EQ session-parameter 
                        AND orderbill-close.logi1 EQ YES
                        AND orderbill-close.logi3 EQ YES EXCLUSIVE-LOCK NO-ERROR.
                END.

                RELEASE orderbill.
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
                FIND FIRST orderbilline WHERE orderbilline.KEY EQ 225 
                    AND orderbilline.char1 EQ "orderbill-line"
                    AND ENTRY(4,orderbilline.char2,"|") EQ session-parameter NO-LOCK NO-ERROR. 
                DO WHILE AVAILABLE orderbilline:
                   
                    FIND CURRENT orderbilline EXCLUSIVE-LOCK.
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
                    FIND CURRENT orderbilline NO-LOCK.
                    RELEASE orderbilline.

                    FIND NEXT orderbilline WHERE orderbilline.KEY EQ 225 
                        AND orderbilline.char1 EQ "orderbill-line"
                        AND ENTRY(4,orderbilline.char2,"|") EQ session-parameter NO-LOCK NO-ERROR.
                END.                
            END.

            /*FD June 21, 2022 => For issue payment gateway can't posting, release betriebsnr 223 to 0*/
            FIND FIRST qpayment-gateway WHERE qpayment-gateway.KEY EQ 223
                AND qpayment-gateway.char3 EQ session-parameter
                AND qpayment-gateway.betriebsnr EQ get-rechnr /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
            IF AVAILABLE qpayment-gateway THEN
            DO:
                FIND CURRENT qpayment-gateway EXCLUSIVE-LOCK.
                qpayment-gateway.betriebsnr = 0.
                FIND CURRENT qpayment-gateway NO-LOCK.
                RELEASE qpayment-gateway.
            END.

            FIND CURRENT paramqsy NO-LOCK.
            RELEASE paramqsy.
        END.        
    END.
END PROCEDURE.

PROCEDURE remove-rsv-table:
    DEFINE VARIABLE recid-q33 AS INTEGER.

    DEFINE BUFFER buffq33 FOR queasy.

    FIND FIRST queasy WHERE queasy.KEY EQ 251 AND queasy.number1 EQ recid-hbill NO-LOCK NO-ERROR.
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

/*MT
IF (h-artart = 2 OR h-artart = 7 OR h-artart = 12) AND closed THEN 
DO: 
  RUN disp-bill-line. 
  answer = NO. 
  IF must-print THEN 
  DO: 
    HIDE MESSAGE NO-PAUSE. 
    answer = YES. 
    MESSAGE translateExtended ("Print the bill?",lvCAREA,"") VIEW-AS ALERT-BOX QUESTION 
      BUTTONS YES-NO UPDATE answer. 
  END. 
  IF answer THEN 
  DO: 
    IF double-currency THEN 
      RUN print-hbill2.p(NO, curr-printer, RECID(vhp.h-bill)). 
    ELSE
    DO curr-num = 1 TO copy-num:     
      IF copy-num = 1 THEN 
        RUN print-hbill1.p(NO, curr-printer, RECID(vhp.h-bill)). 
      ELSE RUN print-hbill1.p(YES, curr-printer, RECID(vhp.h-bill)). 
    END.
    RUN del-queasy. 
  END. 
  ELSE RUN del-queasy. 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 88 NO-LOCK.
  IF vhp.htparam.flogical THEN
  DO:
    HIDE MESSAGE NO-PAUSE. 
    answer = YES. 
    MESSAGE translateExtended ("Print the OFFICIAL INVOICE?",lvCAREA,"") VIEW-AS ALERT-BOX QUESTION 
    BUTTONS YES-NO UPDATE answer. 
    IF answer THEN 
    RUN print-hbill88.p(0, curr-printer, RECID(vhp.h-bill)). 
  END.
END. 

IF h-artart = 11 AND closed THEN 
/* compliment: NO tax & service  other programs FOR vhp.bill printing */ 
DO: 
  RUN disp-bill-line. 
  answer = NO. 
  IF must-print THEN 
  DO: 
    HIDE MESSAGE NO-PAUSE. 
    answer = YES. 
    MESSAGE translateExtended ("Print the bill?",lvCAREA,"") VIEW-AS ALERT-BOX QUESTION 
      BUTTONS YES-NO UPDATE answer. 
  END. 
  IF answer THEN 
  DO: 
    IF double-currency THEN 
      RUN print-hbill2.p(NO, curr-printer, RECID(vhp.h-bill)). 
    ELSE
    DO curr-num = 1 TO copy-num:     
      IF copy-num = 1 THEN 
        RUN print-hbill1.p(NO, curr-printer, RECID(vhp.h-bill)). 
      ELSE RUN print-hbill1.p(YES, curr-printer, RECID(vhp.h-bill)). 
    END.
    RUN del-queasy. 
  END. 
  ELSE RUN del-queasy. 
END. 

IF closed THEN RUN clear-bill-display. 
ELSE IF AVAILABLE vhp.h-bill AND NOT AVAILABLE menu-list 
  THEN RUN disp-bill-line. 
*/

