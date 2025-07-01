
DEF TEMP-TABLE t-fa-ordheader LIKE fa-ordheader.
DEF TEMP-TABLE t-add-last
    FIELD wabkurz LIKE waehrung.wabkurz.
DEFINE TEMP-TABLE tfa-order LIKE fa-order
    FIELD desc-budget        AS CHARACTER
    FIELD date-budget        AS DATE
    FIELD amount-budget      AS DECIMAL
    FIELD remain-budget      AS DECIMAL.
DEFINE TEMP-TABLE t-waehrung
    FIELD wabkurz LIKE waehrung.wabkurz
    FIELD waehrungsnr LIKE waehrung.waehrungsnr.

DEFINE TEMP-TABLE disclist 
  FIELD fa-recid AS INTEGER
  FIELD fa-pos   AS INTEGER
  FIELD price0   AS DECIMAL FORMAT ">,>>>,>>>,>>9.999" LABEL "Unit-Price" 
  FIELD brutto   AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>>,>>9.999" LABEL "Gross Amount" 
  FIELD disc     AS DECIMAL FORMAT ">9.99" LABEL "Disc" 
  FIELD disc2    AS DECIMAL FORMAT ">9.99" LABEL "Disc2" 
  FIELD vat      AS DECIMAL FORMAT ">9.99" LABEL "VAT". 

DEF TEMP-TABLE t-mathis
    FIELD artnr          AS INTEGER
    FIELD asset-name     AS CHARACTER
    FIELD asset-number   AS CHARACTER
    FIELD remain-budget  AS DECIMAL /*MG D710C2*/
    FIELD init-budget  AS DECIMAL.
    
DEF TEMP-TABLE t-lief-list
    FIELD firma AS CHARACTER
    FIELD lief-nr AS INTEGER.

DEF TEMP-TABLE t-dept-list
    FIELD NAME AS CHARACTER
    FIELD nr   AS INTEGER.

DEFINE TEMP-TABLE budget-fix-asset-list
  FIELD nr-budget          AS INTEGER
  FIELD desc-budget        AS CHARACTER
  FIELD date-budget        AS DATE
  FIELD amount-budget      AS DECIMAL
  FIELD remain-budget      AS DECIMAL
.

DEF INPUT  PARAMETER docu-nr                    AS CHAR.
DEF OUTPUT PARAMETER err-no                     AS INT INIT 0.
DEF OUTPUT PARAMETER local-nr                   AS INT.
DEF OUTPUT PARAMETER str-approved1              AS CHARACTER.
DEF OUTPUT PARAMETER enforce-rflag              AS LOGICAL.
DEF OUTPUT PARAMETER deptname                   AS CHARACTER.
DEF OUTPUT PARAMETER billdate                   AS DATE.
DEF OUTPUT PARAMETER t-amount                   AS DECIMAL INIT 0.
DEF OUTPUT PARAMETER add-first-waehrung-wabkurz AS CHAR INIT "".
DEF OUTPUT PARAMETER add-last-waehrung-wabkurz  AS CHAR INIT "".
DEF OUTPUT PARAMETER p-464 AS INTEGER.
DEF OUTPUT PARAMETER p-1093 AS INTEGER.
DEF OUTPUT PARAMETER p-220 AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR t-fa-ordheader.
DEF OUTPUT PARAMETER TABLE FOR tfa-order.
DEF OUTPUT PARAMETER TABLE FOR disclist.
DEF OUTPUT PARAMETER TABLE FOR t-add-last.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.
DEF OUTPUT PARAMETER TABLE FOR t-mathis.
DEF OUTPUT PARAMETER TABLE FOR t-lief-list.
DEF OUTPUT PARAMETER TABLE FOR t-dept-list.

DEFINE VARIABLE mtd-budget    AS DECIMAL.
DEFINE VARIABLE mtd-balance   AS DECIMAL.
DEFINE VARIABLE t-warenwert   AS DECIMAL.
DEFINE VARIABLE remain-budget AS DECIMAL.
DEFINE VARIABLE order-date    AS DATE.

DEFINE BUFFER b-fa-order FOR fa-order.

RUN htpint.p (1093, OUTPUT p-1093).
RUN htpint.p (464,  OUTPUT p-464).
RUN htpint.p (220, OUTPUT p-220).

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
DO: 
  err-no = 1.
  RETURN. 
END.

local-nr = waehrung.waehrungsnr.

FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = docu-nr EXCLUSIVE-LOCK. 


CREATE t-fa-ordheader.
BUFFER-COPY fa-ordheader TO t-fa-ordheader.
order-date = fa-ordheader.order-date.

IF fa-ordheader.approved-1 = YES THEN
DO:
    FIND FIRST bediener WHERE bediener.userinit = fa-ordheader.approved-1-by NO-LOCK. 
    IF AVAILABLE bediener THEN str-approved1 = bediener.username .
    ELSE str-approved1 = "".
END.

FIND FIRST htparam WHERE paramnr = 222 NO-LOCK.
enforce-rflag = flogical.

FIND FIRST htparam WHERE paramnr = 975 NO-LOCK. 
IF htparam.finteger NE 1 AND htparam.finteger NE 2 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  billdate = htparam.fdate. 
END. 
ELSE billdate = TODAY. 

FOR EACH tfa-order WHERE tfa-order.order-nr = docu-nr  :
    DELETE tfa-order.
END.

FOR EACH disclist :
    DELETE disclist.
END.

FOR EACH t-mathis :
    DELETE t-mathis.
END.

FOR EACH queasy WHERE queasy.key EQ 324 NO-LOCK:

  t-warenwert = 0.0.

  CREATE budget-fix-asset-list.
  
  ASSIGN 
      budget-fix-asset-list.nr-budget          = queasy.number1
      budget-fix-asset-list.desc-budget        = queasy.char1
      budget-fix-asset-list.date-budget        = queasy.date1
      budget-fix-asset-list.amount-budget      = queasy.deci1
  .

  FOR EACH fa-order WHERE fa-order.ActiveReason EQ STRING(queasy.number1) NO-LOCK:
      FIND FIRST fa-op WHERE fa-op.loeschflag LE 1 
      AND fa-op.opart EQ 1 
      AND fa-op.anzahl GT 0
      AND fa-op.docu-nr EQ fa-order.Order-Nr NO-LOCK NO-ERROR.
      IF AVAILABLE fa-op THEN
      DO:
          t-warenwert = t-warenwert + fa-op.warenwert.
      END.
  END.

  budget-fix-asset-list.remain-budget = queasy.deci1 - t-warenwert.
END.

RUN call-tamount.
RUN currency-list.

FOR EACH waehrung NO-LOCK:
    CREATE t-waehrung.
    ASSIGN t-waehrung.wabkurz = waehrung.wabkurz
           t-waehrung.waehrungsnr = waehrung.waehrungsnr.
END.

FOR EACH l-lieferant NO-LOCK:
    CREATE t-lief-list.
    ASSIGN
        t-lief-list.firma = l-lieferant.firma
        t-lief-list.lief-nr = l-lieferant.lief-nr
    .
END.

/* 
FOR EACH remain-budget-list:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ remain-budget-list.fa-account NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN 
        ASSIGN 
            remain-budget-list.remain-budget = gl-acct.budget[MONTH(order-date)]
            remain-budget-list.init-budget = gl-acct.budget[MONTH(order-date)].
END.
*/

/*FDL July 17, 2024 => Ticket D710C2*/
/* t-warenwert = 0.
FOR EACH fa-op WHERE fa-op.loeschflag LE 1
    AND MONTH(fa-op.datum) EQ MONTH(order-date)
    AND YEAR(fa-op.datum) EQ YEAR(order-date) NO-LOCK,
    FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
    /* FIRST fa-grup WHERE fa-grup.gnr EQ fa-artikel.subgrp AND fa-grup.flag GT 0 NO-LOCK, */ /* Dzikri 01B1DB */
    FIRST gl-acct WHERE gl-acct.fibukonto EQ fa-artikel.fibukonto NO-LOCK
    BY fa-artikel.fibukonto:

    t-warenwert = t-warenwert + fa-op.warenwert.
    FIND FIRST remain-budget-list WHERE remain-budget-list.fa-account EQ fa-artikel.fibukonto NO-LOCK NO-ERROR.
    IF AVAILABLE remain-budget-list THEN
    DO:
        ASSIGN
           mtd-budget  = gl-acct.budget[MONTH(order-date)]
           mtd-balance = (mtd-budget - t-warenwert).

        remain-budget-list.amount = t-warenwert.
        remain-budget-list.remain-budget = mtd-balance.
    END.         
END.   */

FOR EACH mathis NO-LOCK:
    CREATE t-mathis.
    ASSIGN
        t-mathis.artnr = mathis.nr
        t-mathis.asset-name = mathis.NAME
        t-mathis.asset-number = mathis.asset
    .

    /*FDL July 17, 2024 => Ticket D710C2*/
    /* FIND FIRST remain-budget-list WHERE remain-budget-list.fa-number EQ mathis.nr NO-LOCK NO-ERROR.
    IF AVAILABLE remain-budget-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ remain-budget-list.fa-account NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        ASSIGN
          t-mathis.remain-budget = remain-budget-list.remain-budget
          t-mathis.init-budget = remain-budget-list.init-budget.
    END. */
    
    /* FDL Comment
    /*MG D710C2*/
    FIND FIRST fa-artikel WHERE fa-artikel.nr EQ mathis.nr 
        AND fa-artikel.posted 
        AND fa-artikel.loeschflag EQ 0 
        AND fa-artikel.next-depn EQ ? NO-LOCK NO-ERROR.
    IF AVAILABLE fa-artikel THEN
    DO:
        FOR EACH fa-op WHERE fa-op.loeschflag LE 1
            AND MONTH(fa-op.datum) EQ MONTH(order-date) 
            AND fa-op.fibukonto EQ fa-artikel.fibukonto NO-LOCK:
            
            t-warenwert = t-warenwert + fa-op.warenwert.
        END.
        
        /*MG find remain balance each subgroup <=> COA D710C2*/
        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ fa-artikel.fibukonto NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
           ASSIGN
               mtd-budget  = gl-acct.budget[MONTH(order-date)].
               mtd-balance = (mtd-budget - t-warenwert).
               t-mathis.remain-budget = mtd-balance. 
        END.
    END.
    /*end MG*/
    */
END.

FOR EACH parameters WHERE progname = "CostCenter" AND SECTION = "Name" NO-LOCK:
    CREATE t-dept-list.
    ASSIGN
        t-dept-list.NAME = parameters.vstring
        t-dept-list.nr = INT(parameters.varname)
    .
END.


PROCEDURE call-tamount :
  t-amount = 0. 
  FOR EACH fa-order WHERE fa-order.order-nr = docu-nr 
  AND fa-order.fa-pos GT 0 
  AND fa-order.activeflag = 0 NO-LOCK, 
  FIRST mathis WHERE mathis.nr = fa-order.fa-nr NO-LOCK: 

      t-amount = t-amount + fa-order.order-amount. 

      create tfa-order. 
      ASSIGN 
        tfa-order.order-nr = fa-order.order-nr 
        tfa-order.statflag = RECID(l-order) 
        tfa-order.fa-nr = fa-order.fa-nr 
        tfa-order.order-qty = fa-order.order-qty 
        tfa-order.activeflag = fa-order.activeflag 
        tfa-order.order-price = fa-order.order-price 
        tfa-order.order-amount = fa-order.order-amount 
        tfa-order.activereason = fa-order.activereason 
        tfa-order.fa-pos = fa-order.fa-pos
        tfa-order.fa-remarks = fa-order.fa-remarks
        tfa-order.discount1 = fa-order.discount1
        tfa-order.discount2 = fa-order.discount2
        tfa-order.vat       = fa-order.vat
        .
      
      /* comment because change budget fix asset concept
      /* Dzikri - 01B1DB create new input */
      FIND FIRST queasy WHERE queasy.key = 315 AND queasy.char1 EQ fa-order.order-nr AND queasy.number1 EQ fa-order.Fa-Nr AND queasy.number3 EQ fa-order.Fa-Pos NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      ASSIGN
        tfa-order.budget-date    = queasy.date1
      .
      /* Dzikri - 01B1DB END */
      */

      FIND FIRST budget-fix-asset-list WHERE STRING(budget-fix-asset-list.nr-budget) EQ fa-order.activereason NO-LOCK NO-ERROR.
      IF AVAILABLE budget-fix-asset-list THEN
      DO:
        tfa-order.desc-budget   = budget-fix-asset-list.desc-budget.
        tfa-order.date-budget   = budget-fix-asset-list.date-budget.
        tfa-order.amount-budget = budget-fix-asset-list.amount-budget.
        tfa-order.remain-budget = budget-fix-asset-list.remain-budget.
      END.


      create disclist. 
      ASSIGN 
        disclist.fa-recid = fa-order.fa-nr 
        disclist.fa-pos   = fa-order.fa-pos
        disclist.price0 =  fa-order.order-price / (1 - fa-order.discount1 * 0.01) 
                          / (1 - fa-order.discount2 * 0.01) / (1 + fa-order.vat * 0.01)

        disclist.brutto = disclist.price0 * fa-order.order-qty. 

      /* FDL July 17, 2024 => Ticket D710C2 */
      /* move to outside loop so it can show budget ammount and remaining when insert new item by Oscar (21 Oktober 2024) */
      /* FIND FIRST fa-artikel WHERE fa-artikel.nr EQ fa-order.fa-nr NO-LOCK NO-ERROR.
      IF AVAILABLE fa-artikel THEN
      DO:
          FIND FIRST fa-grup WHERE fa-grup.gnr EQ fa-artikel.subgrp AND fa-grup.flag GT 0 NO-LOCK NO-ERROR.
          IF AVAILABLE fa-grup THEN
          DO:
              CREATE remain-budget-list.
              ASSIGN
                  remain-budget-list.fa-number = fa-artikel.nr
                  remain-budget-list.fa-account = fa-artikel.fibukonto
                  .
          END.
      END. */
  END.

  /* move to outside loop so it can show budget ammount and remaining when insert new item by Oscar (21 Oktober 2024) */
  /* FOR EACH fa-artikel WHERE NOT fa-artikel.posted 
  AND fa-artikel.loeschflag = 0 
  AND fa-artikel.next-depn = ? :
    FIND FIRST fa-grup WHERE fa-grup.gnr EQ fa-artikel.subgrp 
    AND fa-grup.flag GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE fa-grup THEN
    DO:
        CREATE remain-budget-list.
        ASSIGN
            remain-budget-list.fa-number = fa-artikel.nr
            remain-budget-list.fa-account = fa-artikel.fibukonto
            .
    END.
  END. */
END PROCEDURE.

PROCEDURE currency-list :
    DEF VAR strCurr AS CHAR.

    IF fa-ordheader.currency = 0 THEN 
        fa-ordheader.currency = local-nr. 

    FIND FIRST waehrung WHERE waehrung.waehrungsnr = fa-ordheader.currency NO-LOCK. 
    add-first-waehrung-wabkurz = waehrung.wabkurz.

    IF fa-ordheader.currency NE local-nr THEN 
    DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = local-nr NO-LOCK. 
        IF waehrung.betriebsnr = 0 THEN 
            add-last-waehrung-wabkurz = waehrung.wabkurz.
    END. 

    FOR EACH waehrung WHERE /*waehrung.waehrungsnr NE fa-ordheader.currency  
        AND*/ waehrung.ankauf GT 0 AND waehrung.betriebsnr NE 0 NO-LOCK 
        BY waehrung.wabkurz: 
        CREATE t-add-last.
        t-add-last.wabkurz = waehrung.wabkurz.
    END. 

END PROCEDURE.

