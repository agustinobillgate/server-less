
DEF TEMP-TABLE q-20 LIKE queasy.

DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id        AS INT
    FIELD art-bezeich   AS CHAR
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD alkoholgrad   LIKE l-artikel.alkoholgrad
    FIELD lief-einheit  LIKE l-artikel.lief-einheit.

DEF TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-l-artikel LIKE l-artikel.

DEF INPUT  PARAMETER lief-nr            AS INT.
DEF INPUT  PARAMETER docu-nr            AS CHAR.
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF OUTPUT PARAMETER enforce-rflag      AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER show-price         AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER qty-flag           AS LOGICAL INITIAL NO NO-UNDO.
DEF OUTPUT PARAMETER qty-tol            AS INT INITIAL 0 NO-UNDO.
DEF OUTPUT PARAMETER higherprice-flag   AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER disc-flag          AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER crterm             AS INT NO-UNDO.
DEF OUTPUT PARAMETER price-decimal      AS INT NO-UNDO.
DEF OUTPUT PARAMETER lieferdatum        LIKE l-lieferant.lieferdatum NO-UNDO.
DEF OUTPUT PARAMETER bestellart         LIKE l-orderhdr.bestellart NO-UNDO.
DEF OUTPUT PARAMETER comments           AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER supplier           AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER deptname           AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER billdate           AS DATE NO-UNDO.
DEF OUTPUT PARAMETER last-mdate         AS DATE NO-UNDO.
DEF OUTPUT PARAMETER last-fbdate        AS DATE NO-UNDO.
DEF OUTPUT PARAMETER f-endkum           AS INT NO-UNDO.
DEF OUTPUT PARAMETER b-endkum           AS INT NO-UNDO.
DEF OUTPUT PARAMETER m-endkum           AS INT NO-UNDO.
DEF OUTPUT PARAMETER fb-closedate       AS DATE NO-UNDO.
DEF OUTPUT PARAMETER m-closedate        AS DATE NO-UNDO.
DEF OUTPUT PARAMETER t-amount           AS DECIMAL NO-UNDO.
DEF OUTPUT PARAMETER order-amt          AS DECIMAL NO-UNDO.
DEF OUTPUT PARAMETER exchg-rate         AS DECIMAL INITIAL 1 NO-UNDO.
DEF OUTPUT PARAMETER waehrung-wabkurz   AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER fl-code            AS INT INIT 0 NO-UNDO.
DEF OUTPUT PARAMETER fl-code1           AS INT INIT 0 NO-UNDO.
DEF OUTPUT PARAMETER avail-param        AS LOGICAL INIT NO NO-UNDO.
DEF OUTPUT PARAMETER fl-warn            AS LOGICAL INIT NO NO-UNDO.
DEF OUTPUT PARAMETER avail-waehrung     AS LOGICAL INIT NO NO-UNDO.
DEF OUTPUT PARAMETER ci-date            AS DATE    NO-UNDO. /*gerald 100720*/
DEF OUTPUT PARAMETER rcv-po             AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR q-20.

FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr EXCLUSIVE-LOCK 
  no-wait NO-ERROR. 
IF AVAILABLE l-orderhdr THEN
DO:
    CREATE t-l-orderhdr.
    BUFFER-COPY l-orderhdr TO t-l-orderhdr.
    ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).
END.
 
FIND FIRST htparam WHERE paramnr = 222 NO-LOCK. 
enforce-rflag = flogical. 
 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.
 
FIND FIRST htparam WHERE paramnr = 1010 AND htparam.paramgr = 21 
  NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN 
DO: 
  qty-flag = htparam.flogical. 
  FIND FIRST htparam WHERE paramnr = 1011 AND htparam.paramgr = 21 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE htparam THEN qty-tol = htparam.finteger. 
END. 
 
FIND FIRST htparam WHERE paramnr = 350 NO-LOCK. 
higherprice-flag = flogical. 
 
FIND FIRST htparam WHERE paramnr = 349 NO-LOCK. 
IF htparam.feldtyp NE 4 THEN disc-flag = NO. 
ELSE disc-flag = htparam.flogical. 
 
IF NOT AVAILABLE l-orderhdr THEN 
DO:
  fl-code = 1.
  RETURN. 
END. 
 
IF l-orderhdr.gedruckt = ? AND enforce-rflag THEN 
DO:
  fl-code1 = 1.
END. 
 
crterm = l-orderhdr.angebot-lief[2]. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 


FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
 
lieferdatum = l-orderhdr.lieferdatum. 
bestellart = l-orderhdr.bestellart. 
comments = l-orderhdr.lief-fax[3]. 
supplier = l-lieferant.firma + " - " + l-lieferant.wohnort. 
 
FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
  AND parameters.section = "Name" 
  AND INTEGER(parameters.varname) = l-orderhdr.angebot-lief[1] 
  NO-LOCK NO-ERROR. 
IF AVAILABLE parameters THEN 
DO: 
  deptname = parameters.vstring.
  avail-param = YES.
END. 
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
IF billdate = ? OR billdate GT TODAY THEN billdate = TODAY. 
ELSE 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 221 NO-LOCK. 
  IF htparam.fdate NE ? THEN last-mdate = DATE(month(htparam.fdate), 
    1, year(htparam.fdate)) - 1. 
  FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK. 
  IF htparam.fdate NE ? THEN last-fbdate = DATE(month(htparam.fdate), 
    1, year(htparam.fdate)) - 1. 
  IF (billdate LE last-mdate) OR (billdate LE last-fbdate) THEN 
  DO: 
    fl-warn = YES.
  END. 

  FIND FIRST htparam WHERE htparam.paramnr = 269 NO-LOCK. 
  IF htparam.fdate NE ? AND billdate LE htparam.fdate THEN 
  DO:
    fl-code = 2.
    RETURN.
  END. 
END. 
 
FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-closedate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-closedate = htparam.fdate. 
 
RUN cal-tamount. 

RUN get-currency. 

FIND FIRST l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.loeschflag = 0 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE l-order:
    CREATE t-l-order.
    BUFFER-COPY l-order TO t-l-order.
    ASSIGN t-l-order.rec-id = RECID(l-order).

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK.
    ASSIGN 
        t-l-order.art-bezeich   = l-artikel.bezeich
        t-l-order.jahrgang      = l-artikel.jahrgang
        t-l-order.alkoholgrad   = l-artikel.alkoholgrad
        t-l-order.lief-einheit  = l-artikel.lief-einheit.


    FIND NEXT l-order WHERE l-order.docu-nr = docu-nr 
        AND l-order.pos GT 0 AND l-order.loeschflag = 0 NO-LOCK NO-ERROR.
END.
/*
FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.loeschflag = 0:
    CREATE t-l-order.
    BUFFER-COPY l-order TO t-l-order.
    ASSIGN t-l-order.rec-id = RECID(l-order).

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK.
    ASSIGN 
        t-l-order.art-bezeich = l-artikel.bezeich
        t-l-order.jahrgang = l-artikel.jahrgang
        t-l-order.alkoholgrad = l-artikel.alkoholgrad.
END.*/

FOR EACH queasy WHERE queasy.KEY = 20:
    CREATE q-20.
    BUFFER-COPY queasy TO q-20.
END.

FIND FIRST htparam WHERE htparam.paramnr = 1354 
    AND htparam.bezeich NE "not used" NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN rcv-po = htparam.flogical.

PROCEDURE cal-tamount: 
  t-amount = 0. 
  order-amt = 0. 

  FIND FIRST l-order WHERE l-order.docu-nr = docu-nr AND 
      l-order.pos GT 0 AND l-order.loeschflag = 0 
      NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE l-order:
        ASSIGN order-amt = order-amt + l-order.warenwert. 

        FIND NEXT l-order WHERE l-order.docu-nr = docu-nr AND 
          l-order.pos GT 0 AND l-order.loeschflag = 0 
          NO-LOCK NO-ERROR.
  END.
  
  /*FOR EACH l-order WHERE l-order.docu-nr = docu-nr AND 
      l-order.pos GT 0 AND l-order.loeschflag = 0 
      NO-LOCK: 
    order-amt = order-amt + l-order.warenwert. 
  END. */
END. 
 
PROCEDURE get-currency: 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
    l-orderhdr.angebot-lief[3] NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    waehrung-wabkurz = waehrung.wabkurz.
    avail-waehrung = YES.
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
END. 
