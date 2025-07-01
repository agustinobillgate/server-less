DEFINE TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id AS INT
    FIELD a-bezeich AS CHARACTER
    FIELD jahrgang AS INTEGER
    FIELD alkoholgrad AS DECIMAL
    FIELD curr-disc AS INTEGER
    FIELD curr-disc2 AS INTEGER
    FIELD curr-vat AS INTEGER.

DEF TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-l-lager LIKE l-lager.

DEF INPUT  PARAMETER pvILanguage        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER lief-nr            AS INTEGER.
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF INPUT  PARAMETER docu-nr            AS CHAR.
DEF OUTPUT PARAMETER enforce-rflag      AS LOGICAL.
DEF OUTPUT PARAMETER show-price         AS LOGICAL.
DEF OUTPUT PARAMETER higherprice-flag   AS LOGICAL.
DEF OUTPUT PARAMETER disc-flag          AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal      AS INT.
DEF OUTPUT PARAMETER qty-flag           AS LOGICAL.
DEF OUTPUT PARAMETER qty-tol            AS INT.
DEF OUTPUT PARAMETER crterm             AS INT.
DEF OUTPUT PARAMETER lieferdatum        LIKE l-lieferant.lieferdatum.
DEF OUTPUT PARAMETER bestellart         LIKE l-orderhdr.bestellart.
DEF OUTPUT PARAMETER comments           AS CHAR.
DEF OUTPUT PARAMETER supplier           AS CHAR.
DEF OUTPUT PARAMETER deptname           AS CHAR.
DEF OUTPUT PARAMETER f-endkum           AS INT.
DEF OUTPUT PARAMETER b-endkum           AS INT.
DEF OUTPUT PARAMETER m-endkum           AS INT.
DEF OUTPUT PARAMETER billdate           AS DATE.
DEF OUTPUT PARAMETER fb-closedate       AS DATE.
DEF OUTPUT PARAMETER m-closedate        AS DATE.
DEF OUTPUT PARAMETER last-mdate         AS DATE.
DEF OUTPUT PARAMETER last-fbdate        AS DATE.
DEF OUTPUT PARAMETER err-code           AS INT INIT 0.
DEF OUTPUT PARAMETER t-amount           AS DECIMAL.
DEF OUTPUT PARAMETER waehrung-wabkurz   AS CHAR.
DEF OUTPUT PARAMETER exchg-rate         AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER msg-str            AS CHAR.
DEF OUTPUT PARAMETER ci-date              AS DATE NO-UNDO. /*gerald 030820*/
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.


FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-ERROR. 
 
IF NOT AVAILABLE l-orderhdr THEN 
DO:
  err-code = 1.
  RETURN. 
END. 
 
CREATE t-l-orderhdr.
BUFFER-COPY l-orderhdr TO t-l-orderhdr.
ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).
FIND FIRST htparam WHERE paramnr = 222 NO-LOCK. 
enforce-rflag = flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
FIND FIRST htparam WHERE paramnr = 350 NO-LOCK. 
higherprice-flag = flogical. 

FIND FIRST htparam WHERE paramnr = 349 NO-LOCK. 
IF htparam.feldtyp NE 4 THEN disc-flag = NO. 
ELSE disc-flag = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 

FIND FIRST htparam WHERE paramnr = 1010 AND htparam.paramgr = 21 
  NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN 
DO: 
  qty-flag = htparam.flogical. 
  FIND FIRST htparam WHERE paramnr = 1011 AND htparam.paramgr = 21 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE htparam THEN qty-tol = htparam.finteger. 
END. 

crterm = l-orderhdr.angebot-lief[2]. 


FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
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
END. 
 
FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-closedate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-closedate = htparam.fdate. 
 
IF billdate = ? OR billdate GT today THEN billdate = today. 
ELSE 
DO: 
  IF m-closedate NE ? THEN last-mdate = DATE(month(m-closedate), 
    1, year(m-closedate)) - 1. 
  IF fb-closedate NE ? THEN last-fbdate = DATE(month(fb-closedate), 
    1, year(fb-closedate)) - 1. 
  IF (billdate LE last-mdate) OR (billdate LE last-fbdate) THEN 
  DO: 
    msg-str = msg-str + CHR(2) + "&W"
            + "Receiving Date might be incorrect (too old),"
            + CHR(10)
            + "Please re-check it.".
  END. 
  FIND FIRST htparam WHERE htparam.paramnr = 269 NO-LOCK. 
    IF htparam.fdate NE ? AND billdate LE htparam.fdate THEN 
  DO: 
    msg-str = msg-str + CHR(2) + "&W"
            + "Wrong receiving date (ParamNo 474):" 
            + CHR(10)
            + "Older than last transfer date to the G/L.".
    /*MTscreen-tooltip = SUBSTR(screen-tooltip, 1, LENGTH(screen-tooltip) - 15).*/
    RETURN.
  END. 

END. 
 
RUN cal-tamount. 
RUN get-currency. 

FOR EACH l-lager:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.

FOR EACH l-order WHERE l-order.pos GT 0 AND l-order.loeschflag = 0 AND l-order.docu-nr = docu-nr:
    CREATE t-l-order.
    BUFFER-COPY l-order TO t-l-order.
    ASSIGN t-l-order.rec-id = RECID(l-order).

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-artikel THEN
    ASSIGN 
        t-l-order.a-bezeich = l-artikel.bezeich
        t-l-order.jahrgang = l-artikel.jahrgang
        t-l-order.alkoholgrad = l-artikel.alkoholgrad
        t-l-order.curr-disc = INTEGER(SUBSTR(t-l-order.quality,1,2)) * 100 
                            + INTEGER(SUBSTR(t-l-order.quality,4,2))
        t-l-order.curr-vat = INTEGER(SUBSTR(t-l-order.quality,7,2)) * 100 
                            + INTEGER(SUBSTR(t-l-order.quality,10,2))
        t-l-order.curr-disc2 = 0. 

    IF l-artikel.lief-einheit GT 1 AND t-l-order.geliefert GT 0 THEN
    DO:
        t-l-order.angebot-lief[1] = t-l-order.geliefert MOD l-artikel.lief-einheit.
        t-l-order.geliefert = (t-l-order.geliefert - t-l-order.angebot-lief [1]) / l-artikel.lief-einheit.
    END.

    IF length(t-l-order.quality) GE 17 THEN 
        t-l-order.curr-disc2 = INTEGER(SUBSTR(t-l-order.quality,13,2)) * 100 
            + INTEGER(SUBSTR(t-l-order.quality,16,2)). 
END.

PROCEDURE cal-tamount: 
  t-amount = 0. 
/* 
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr AND 
      l-order.pos GT 0 AND l-order.loeschflag = 0 
      AND l-order.geliefert NE 0 NO-LOCK: 
    t-amount = t-amount + l-order.rechnungswert. 
  END. 
*/ 
END. 

PROCEDURE get-currency: 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
    l-orderhdr.angebot-lief[3] NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    waehrung-wabkurz = waehrung.wabkurz.
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
END. 
