
DEFINE TEMP-TABLE disc-list 
  FIELD l-recid     AS INTEGER 
  FIELD price0      AS DECIMAL FORMAT ">,>>>,>>>,>>9.999" LABEL "Unit-Price" 
  FIELD brutto      AS DECIMAL FORMAT "->,>>>,>>>,>>9.999" LABEL "Gross Amount" 
  FIELD disc        AS DECIMAL FORMAT ">9.99" LABEL "Disc" 
  FIELD disc2       AS DECIMAL FORMAT ">9.99" LABEL "Disc2" 
  FIELD vat         AS DECIMAL FORMAT ">9.99" LABEL "VAT"
  FIELD new-created AS LOGICAL INITIAL NO. 
DEF TEMP-TABLE t-l-artikel
    FIELD rec-id        AS INT
    FIELD artnr         LIKE l-artikel.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD ek-aktuell    LIKE l-artikel.ek-aktuell
    FIELD ek-letzter    LIKE l-artikel.ek-letzter
    FIELD traubensort   LIKE l-artikel.traubensort
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD lief-nr1      LIKE l-artikel.lief-nr1
    FIELD lief-nr2      LIKE l-artikel.lief-nr2
    FIELD lief-nr3      LIKE l-artikel.lief-nr3
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD alkoholgrad   LIKE l-artikel.alkoholgrad.

DEFINE TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER docu-nr AS CHAR.
DEF INPUT  PARAMETER lief-nr AS INT.

DEF OUTPUT PARAMETER local-nr AS INT.
DEF OUTPUT PARAMETER enforce-rflag AS LOGICAL.
DEF OUTPUT PARAMETER zeroprice-flag AS LOGICAL.
DEF OUTPUT PARAMETER potype AS INT INIT 1.
DEF OUTPUT PARAMETER lieferdatum LIKE l-lieferant.lieferdatum. 
DEF OUTPUT PARAMETER bestellart LIKE l-orderhdr.bestellart.
DEF OUTPUT PARAMETER comments AS CHAR.
DEF OUTPUT PARAMETER supplier AS CHAR.
DEF OUTPUT PARAMETER deptnr AS INT.
DEF OUTPUT PARAMETER deptname AS CHAR.
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER p-234 AS LOGICAL.
DEF OUTPUT PARAMETER p-266 AS DECIMAL.
DEF OUTPUT PARAMETER t-amount AS DECIMAL.
DEF OUTPUT PARAMETER pos AS INT.
DEF OUTPUT PARAMETER currency-add-first AS CHAR.
DEF OUTPUT PARAMETER currency-screen-value AS CHAR.
DEF OUTPUT PARAMETER err-flag AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR disc-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "insert-po".

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
DO:
  err-flag = YES.
  RETURN. 
END. 
local-nr = waehrung.waehrungsnr. 

FIND FIRST htparam WHERE paramnr = 222 NO-LOCK. 
enforce-rflag = flogical. 
 
FIND FIRST htparam WHERE paramnr = 776 NO-LOCK. 
zeroprice-flag = flogical. 

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr EXCLUSIVE-LOCK. 
IF l-orderhdr.betriebsnr = 1 THEN potype = 2. 
lieferdatum = l-orderhdr.lieferdatum. 
bestellart = l-orderhdr.bestellart. 
comments = l-orderhdr.lief-fax[3]. 
supplier = l-lieferant.firma + " - " + l-lieferant.wohnort. 
 
deptnr = l-orderhdr.angebot-lief[1]. 

CREATE t-l-orderhdr.
BUFFER-COPY l-orderhdr TO t-l-orderhdr.
ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).

IF deptnr GT 0 THEN 
DO: 
  FIND FIRST parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname EQ STRING(deptnr) NO-LOCK. 
  deptname = parameters.vstring.
END.


FIND FIRST htparam WHERE paramnr = 975 NO-LOCK. 
IF htparam.finteger NE 1 AND htparam.finteger NE 2 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  billdate = htparam.fdate. 
END. 
ELSE billdate = today.

RUN cal-tamount.
RUN get-currency.

FIND FIRST htparam WHERE paramnr = 234 NO-LOCK. 
p-234 = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 266 NO-LOCK. 
p-266 = htparam.fdecimal.

IF p-234 THEN
FOR EACH l-artikel WHERE (l-artikel.lief-nr1 = lief-nr OR l-artikel.lief-nr2 = lief-nr 
    OR l-artikel.lief-nr3 = lief-nr) NO-LOCK:
    CREATE t-l-artikel.
    ASSIGN
    t-l-artikel.rec-id        = RECID(l-artikel)
    t-l-artikel.artnr         = l-artikel.artnr
    t-l-artikel.bezeich       = l-artikel.bezeich
    t-l-artikel.ek-aktuell    = l-artikel.ek-aktuell
    t-l-artikel.ek-letzter    = l-artikel.ek-letzter
    t-l-artikel.traubensort   = l-artikel.traubensort
    t-l-artikel.lief-einheit  = l-artikel.lief-einheit
    t-l-artikel.lief-nr1      = l-artikel.lief-nr1
    t-l-artikel.lief-nr2      = l-artikel.lief-nr2
    t-l-artikel.lief-nr3      = l-artikel.lief-nr3
    t-l-artikel.jahrgang      = l-artikel.jahrgang
    t-l-artikel.alkoholgrad   = l-artikel.alkoholgrad.
END.
/*MT
FOR EACH l-artikel NO-LOCK:
    CREATE t-l-artikel.
    ASSIGN
    t-l-artikel.rec-id        = RECID(l-artikel)
    t-l-artikel.artnr         = l-artikel.artnr
    t-l-artikel.bezeich       = l-artikel.bezeich
    t-l-artikel.ek-aktuell    = l-artikel.ek-aktuell
    t-l-artikel.ek-letzter    = l-artikel.ek-letzter
    t-l-artikel.traubensort   = l-artikel.traubensort
    t-l-artikel.lief-einheit  = l-artikel.lief-einheit
    t-l-artikel.lief-nr1      = l-artikel.lief-nr1
    t-l-artikel.lief-nr2      = l-artikel.lief-nr2
    t-l-artikel.lief-nr3      = l-artikel.lief-nr3
    t-l-artikel.jahrgang      = l-artikel.jahrgang
    t-l-artikel.alkoholgrad   = l-artikel.alkoholgrad.
END.
*/
/* ST 30/09/14 GT 0 changed to GE 0 */
FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GE 0 AND l-order.loeschflag = 0 NO-LOCK:
    CREATE t-l-order.
    BUFFER-COPY l-order TO t-l-order.
    ASSIGN t-l-order.rec-id = RECID(l-order).
END.


PROCEDURE cal-tamount: 
  t-amount = 0. 
  pos = 0. 
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr AND 
      l-order.pos GT 0 NO-LOCK: 
    IF l-order.loeschflag = 0 THEN t-amount = t-amount + l-order.warenwert. 
    IF l-order.pos GT pos THEN pos = l-order.pos. 
    
    CREATE disc-list. 
    disc-list.l-recid = RECID(l-order). 
    IF length(l-order.quality) GE 5 THEN 
      disc-list.disc = INTEGER(SUBSTR(l-order.quality,1,2)) 
      + INTEGER(SUBSTR(l-order.quality,4,2)) / 100. 
    IF length(l-order.quality) GE 11 THEN 
      disc-list.vat = INTEGER(SUBSTR(l-order.quality,7,2)) 
      + INTEGER(SUBSTR(l-order.quality,10,2)) / 100. 
    IF length(l-order.quality) GE 17 THEN 
      disc-list.disc2 = INTEGER(SUBSTR(l-order.quality,13,2)) 
      + INTEGER(SUBSTR(l-order.quality,16,2)) / 100. 
    disc-list.price0 =  l-order.einzelpreis / (1 - disc-list.disc * 0.01) 
      / (1 - disc-list.disc2 * 0.01) / (1 + disc-list.vat * 0.01). 
    disc-list.brutto = disc-list.price0 * l-order.anzahl. 
/* 
    ASSIGN 
      disc-list.l-recid = l-order.pos 
      disc-list.disc = DECIMAL(SUBSTR(l-order.quality,1,5)) 
      disc-list.disc2 = DECIMAL(SUBSTR(l-order.quality,13,5)) 
      disc-list.vat = DECIMAL(SUBSTR(l-order.quality,7,5)). 
*/ 
  END. 
END. 

PROCEDURE get-currency: 
  IF l-orderhdr.angebot-lief[3] = 0 THEN 
    l-orderhdr.angebot-lief[3] = local-nr. 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
    l-orderhdr.angebot-lief[3] NO-LOCK. 
  currency-add-first = waehrung.wabkurz.
  currency-screen-value = waehrung.wabkurz.
END. 

