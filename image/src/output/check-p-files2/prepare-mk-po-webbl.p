DEF TEMP-TABLE t-parameters
    FIELD varname LIKE parameters.varname
    FIELD vstring LIKE parameters.vstring.

DEF TEMP-TABLE t-waehrung
    FIELD wabkurz LIKE waehrung.wabkurz.

DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id      AS INT
    FIELD a-bezeich   AS CHARACTER 
    FIELD price0      AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Unit-Price" 
    FIELD brutto      AS DECIMAL FORMAT "->,>>>,>>>,>>9.999"  LABEL "Gross Amount" 
    FIELD disc        AS DECIMAL FORMAT ">9.99"               LABEL "Disc" 
    FIELD disc2       AS DECIMAL FORMAT ">9.99"               LABEL "Disc2" 
    FIELD vat         AS DECIMAL FORMAT ">9.99"               LABEL "VAT"
    FIELD disc-val    AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc Value" 
    FIELD disc2-val   AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc2 Value"
    FIELD vat-val     AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "VAT-Value".

DEF TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF INPUT-OUTPUT  PARAMETER docu-nr         AS CHAR.
DEF INPUT  PARAMETER pvILanguage            AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER lief-nr                AS INT.
DEF INPUT  PARAMETER pr-deptnr              AS INT.
DEF INPUT  PARAMETER po-type                AS INT.
DEF INPUT  PARAMETER potype                 AS INT.
DEF INPUT  PARAMETER bediener-username      AS CHAR.
DEF INPUT  PARAMETER ordername-screen-value AS CHAR.
DEF INPUT  PARAMETER crterm                 AS INT.

DEF OUTPUT PARAMETER local-nr               AS INT.
DEF OUTPUT PARAMETER billdate               AS DATE.
DEF OUTPUT PARAMETER zeroprice-flag         AS LOGICAL.
DEF OUTPUT PARAMETER deptname               AS CHAR.
DEF OUTPUT PARAMETER supplier               AS CHAR.
DEF OUTPUT PARAMETER curr-liefnr            AS INT.
DEF OUTPUT PARAMETER p-222                  AS LOGICAL.
DEF OUTPUT PARAMETER p-234                  AS LOGICAL.
DEF OUTPUT PARAMETER p-266                  AS DECIMAL.
DEF OUTPUT PARAMETER pos                    AS INT.
DEF OUTPUT PARAMETER t-amount               AS DECIMAL.
DEF OUTPUT PARAMETER currency-add-first     AS CHAR.
DEF OUTPUT PARAMETER currency-screen-value  AS CHAR.
DEF OUTPUT PARAMETER msg-str                AS CHAR.
DEF OUTPUT PARAMETER p-1093                 AS INT.
DEF OUTPUT PARAMETER p-464                  AS INT.
DEF OUTPUT PARAMETER p-220                  AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-po".

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)",lvCAREA,"").
  RETURN. 
END. 

local-nr = waehrung.waehrungsnr. 
 
FIND FIRST htparam WHERE paramnr = 975 NO-LOCK. 
IF htparam.finteger NE 1 AND htparam.finteger NE 2 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  billdate = htparam.fdate. 
END. 
ELSE billdate = TODAY. 

FIND FIRST htparam WHERE paramnr = 776 NO-LOCK. 
zeroprice-flag = flogical.

IF docu-nr = "" THEN 
DO: 
  RUN new-po-number. 
END. 

RUN currency-list. 
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 

RUN htpint.p (1093, OUTPUT p-1093).
RUN htpint.p (464, OUTPUT p-464).
RUN htpint.p (220, OUTPUT p-220).


DO TRANSACTION:
  IF po-type = 1 THEN 
  DO: 
    FIND FIRST l-orderhdr WHERE l-orderhdr.lief-nr = lief-nr
        AND l-orderhdr.docu-nr = docu-nr EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE l-orderhdr THEN
    DO:
      CREATE l-orderhdr. 
      ASSIGN 
        l-orderhdr.lief-nr = lief-nr 
        l-orderhdr.docu-nr = docu-nr
      .
    END.
    ASSIGN 
      l-orderhdr.angebot-lief[1] = pr-deptnr 
      l-orderhdr.bestelldatum = billdate 
      l-orderhdr.lieferdatum = billdate + 1 
      l-orderhdr.besteller = bediener-username 
      l-orderhdr.lief-fax[1] = l-lieferant.fax 
      l-orderhdr.lief-fax[2] = ordername-screen-value
      l-orderhdr.angebot-lief[2] = crterm 
      l-orderhdr.angebot-lief[3] = local-nr 
      l-orderhdr.gedruckt = ?. 
      IF potype = 2 THEN l-orderhdr.betriebsnr = 1. 
    IF pr-deptnr NE 0 THEN 
    FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
      AND parameters.section = "Name" 
      AND INTEGER(parameters.varname) = l-orderhdr.angebot-lief[1] 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE parameters THEN 
    DO: 
      deptname = parameters.vstring. 
    END.
    FIND CURRENT l-orderhdr NO-LOCK.
  END. 
  FIND FIRST l-orderhdr WHERE l-orderhdr.lief-nr = lief-nr 
    AND l-orderhdr.docu-nr = docu-nr EXCLUSIVE-LOCK.
  CREATE t-l-orderhdr.
  BUFFER-COPY l-orderhdr TO t-l-orderhdr.
  ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).
END.

supplier = l-lieferant.firma + " - " + l-lieferant.wohnort. 
curr-liefnr = lief-nr.

FIND FIRST htparam WHERE paramnr = 222 NO-LOCK.
p-222 = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 234 NO-LOCK.
p-234 = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 266 NO-LOCK.
p-266 = htparam.fdecimal.

ASSIGN
    pos = 0
    t-amount = 0.

FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.loeschflag = 0 NO-LOCK:
    CREATE t-l-order.
    BUFFER-COPY l-order TO t-l-order.
    ASSIGN t-l-order.rec-id = RECID(l-order).

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK.
    ASSIGN t-l-order.a-bezeich = l-artikel.bezeich.
    IF l-order.lief-nr = lief-nr AND l-order.loeschflag = 0 AND docu-nr NE "" THEN
    DO:
        pos = pos + 1. 
        IF length(l-order.quality) GE 5 THEN 
            t-l-order.disc = INTEGER(SUBSTR(l-order.quality,1,2)) 
                            + INTEGER(SUBSTR(l-order.quality,4,2)) / 100. 
        IF length(l-order.quality) GE 11 THEN 
            t-l-order.vat = INTEGER(SUBSTR(l-order.quality,7,2)) 
                            + INTEGER(SUBSTR(l-order.quality,10,2)) / 100. 
        IF length(l-order.quality) GE 17 THEN 
            t-l-order.disc2 = INTEGER(SUBSTR(l-order.quality,13,2)) 
                            + INTEGER(SUBSTR(l-order.quality,16,2)) / 100. 
        t-l-order.price0 =  l-order.einzelpreis / (1 - t-l-order.disc * 0.01) 
                        / (1 - t-l-order.disc2 * 0.01) / (1 + t-l-order.vat * 0.01). 
        t-l-order.brutto = t-l-order.price0 * l-order.anzahl. 
        t-amount = t-amount + l-order.warenwert.
    END.
END.

FOR EACH parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Name" NO-LOCK:
    CREATE t-parameters.
    ASSIGN
    t-parameters.varname = parameters.varname
    t-parameters.vstring = parameters.vstring.
END.


PROCEDURE new-po-number: 
DEFINE BUFFER l-orderhdr1 FOR l-orderhdr. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 973 NO-LOCK. 
  IF htparam.paramgruppe = 21 AND htparam.flogical THEN /* htparam.paramgr -> htparam.paramgruppe (malik : fixing for serverless) */
  DO: 
    mm = month(billdate). 
    yy = year(billdate). 
    s = "P" + SUBSTR(STRING(year(billdate)),3,2) 
      + STRING(MONTH(billdate), "99"). 
    FOR EACH l-orderhdr1 WHERE MONTH(l-orderhdr1.bestelldatum) = mm 
      AND year(l-orderhdr1.bestelldatum) = yy 
      AND l-orderhdr1.betriebsnr LE 1 
      AND l-orderhdr1.docu-nr MATCHES "P*"
      NO-LOCK BY l-orderhdr1.docu-nr DESCENDING: 
      i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,6,5)). 
      i = i + 1. 
      docu-nr = s + STRING(i, "99999"). 
      RETURN. 
    END. 
    docu-nr = s + STRING(i, "99999"). 
    RETURN. 
  END. 
  s = "P" + SUBSTR(STRING(YEAR(billdate)),3,2) + STRING(MONTH(billdate), "99") 
     + STRING(day(billdate), "99"). 
  FOR EACH l-orderhdr1 WHERE l-orderhdr1.bestelldatum = billdate 
    AND l-orderhdr1.betriebsnr LE 1 
    AND l-orderhdr1.docu-nr MATCHES "P*"
    NO-LOCK BY l-orderhdr1.docu-nr DESCENDING: 
    i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,8,3)). 
    i = i + 1. 
    docu-nr = s + STRING(i, "999"). 
    RETURN. 
  END. 
  docu-nr = s + STRING(i, "999"). 
END. 

PROCEDURE currency-list: 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = local-nr NO-LOCK. 
  currency-add-first = waehrung.wabkurz.
  currency-screen-value = waehrung.wabkurz.
  FOR EACH waehrung WHERE waehrung.waehrungsnr NE local-nr 
      AND waehrung.ankauf GT 0 AND waehrung.betriebsnr NE 0 NO-LOCK 
      BY waehrung.wabkurz:
      CREATE t-waehrung.
      ASSIGN t-waehrung.wabkurz = waehrung.wabkurz.
      /*MTcurrency:add-last(waehrung.wabkurz) IN FRAME frame1.*/
  END. 
END. 

