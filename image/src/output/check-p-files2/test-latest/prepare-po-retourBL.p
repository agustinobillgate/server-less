
DEF TEMP-TABLE t-l-artikel
    FIELD artnr    LIKE l-artikel.artnr
    FIELD vk-preis LIKE l-artikel.vk-preis
    FIELD ek-aktuell LIKE l-artikel.ek-aktuell
    FIELD bezeich  LIKE l-artikel.bezeich
    FIELD endkum   LIKE l-artikel.endkum
    FIELD jahrgang LIKE l-artikel.jahrgang.

DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER bediener-permissions   AS CHAR.
DEF INPUT  PARAMETER docu-nr                AS CHAR.

DEF OUTPUT PARAMETER show-price             AS LOGICAL.
DEF OUTPUT PARAMETER f-endkum               AS INT.
DEF OUTPUT PARAMETER b-endkum               AS INT.
DEF OUTPUT PARAMETER m-endkum               AS INT.
DEF OUTPUT PARAMETER billdate               AS DATE.
DEF OUTPUT PARAMETER fb-closedate           AS DATE.
DEF OUTPUT PARAMETER m-closedate            AS DATE.
DEF OUTPUT PARAMETER price-decimal          AS INT.
DEF OUTPUT PARAMETER lieferdatum            AS DATE.
DEF OUTPUT PARAMETER comments               AS CHAR.
DEF OUTPUT PARAMETER supplier               AS CHAR.
DEF OUTPUT PARAMETER currency-add-first     AS CHAR.
DEF OUTPUT PARAMETER currency-screen-value  AS CHAR.
DEF OUTPUT PARAMETER exchg-rate             AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER t-amount               AS DECIMAL.
DEF OUTPUT PARAMETER bestellart             LIKE l-orderhdr.bestellart.
DEF OUTPUT PARAMETER fl-code                AS INT INIT 0.
DEF OUTPUT PARAMETER p-1016                 AS LOGICAL.
DEF OUTPUT PARAMETER p-224                  AS DATE.
DEF OUTPUT PARAMETER p-221                  AS DATE.
DEF OUTPUT PARAMETER p-474                  AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN p-224 = htparam.fdate.
FIND FIRST htparam WHERE htparam.paramnr = 221 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN p-221 = htparam.fdate.
FIND FIRST htparam WHERE htparam.paramnr = 474 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN p-474 = htparam.fdate.
FIND FIRST htparam WHERE paramnr = 1016 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN p-1016 = htparam.flogical.
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN show-price = htparam.flogical. 
IF SUBSTR(bediener-permissions, 22, 1) NE "0" THEN show-price = YES. 

/* FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. */         /* Rulita 181024 | the supplier always appears in CASH PURCHASE */
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-orderhdr THEN RETURN.                                          /* Rulita 110225 | Fixing for serverless 570 */

CREATE t-l-orderhdr.
BUFFER-COPY l-orderhdr TO t-l-orderhdr.
ASSIGN t-l-orderhdr.rec-id  = RECID(l-orderhdr).

FIND FIRST htparam WHERE paramnr = 257 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 268 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN fb-closedate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN m-closedate = htparam.fdate. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
lieferdatum = l-orderhdr.lieferdatum. 
bestellart = l-orderhdr.bestellart. 
comments = l-orderhdr.lief-fax[3].

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK NO-ERROR.    /* Rulita 110225 | Fixing for serverless 570 */
IF AVAILABLE l-lieferant THEN supplier = l-lieferant.firma + " - " + l-lieferant.wohnort. 

RUN cal-tamount. 
RUN get-currency. 

FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.geliefert GE 0 NO-LOCK:
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-ERROR.
    IF AVAILABLE l-artikel THEN
    DO:
        CREATE t-l-artikel.
        ASSIGN
            t-l-artikel.artnr      = l-artikel.artnr
            t-l-artikel.vk-preis   = l-artikel.vk-preis
            t-l-artikel.ek-aktuell = l-artikel.ek-aktuell
            t-l-artikel.bezeich    = l-artikel.bezeich
            t-l-artikel.endkum     = l-artikel.endkum
            t-l-artikel.jahrgang   = l-artikel.jahrgang.
        CREATE t-l-order.
        BUFFER-COPY l-order TO t-l-order.
        ASSIGN t-l-order.rec-id = RECID(l-order).
    END.
END.

PROCEDURE get-currency: 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
    l-orderhdr.angebot-lief[3] NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO:
    fl-code = 1.
    currency-add-first = waehrung.wabkurz.
    currency-screen-value = waehrung.wabkurz. 
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
END. 
 
PROCEDURE cal-tamount: 
  t-amount = 0. 
END. 
 
