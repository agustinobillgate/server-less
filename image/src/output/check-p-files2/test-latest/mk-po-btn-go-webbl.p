
DEF TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

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

DEF INPUT  PARAMETER TABLE FOR t-l-orderhdr.
DEF INPUT  PARAMETER TABLE FOR t-l-order.
DEF INPUT  PARAMETER docu-nr            AS CHAR.
DEF INPUT  PARAMETER lief-nr            AS INTEGER.
DEF INPUT  PARAMETER billdate           AS DATE.
DEF INPUT  PARAMETER create-new         AS LOGICAL.
DEF INPUT  PARAMETER pr                 AS CHARACTER.
DEF INPUT  PARAMETER globaldisc         AS DECIMAL.
DEF INPUT  PARAMETER currency-screen-value AS CHARACTER.
DEF OUTPUT PARAMETER fl-code            AS INT INIT 0.
DEF OUTPUT PARAMETER avail-hdrbuff      AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER new-docu-nr        AS CHAR.

DEFINE BUFFER hdrbuff   FOR l-orderhdr.
DEFINE BUFFER l-od      FOR l-order.
DEFINE buffer l-art1    FOR l-artikel. 

FIND FIRST t-l-orderhdr.
FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = t-l-orderhdr.rec-id.
BUFFER-COPY t-l-orderhdr TO l-orderhdr.
FIND FIRST waehrung WHERE waehrung.wabkurz = currency-screen-value NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN l-orderhdr.angebot-lief[3] = waehrung.waehrungsnr.

FOR EACH t-l-order WHERE t-l-order.pos GT 0 AND t-l-order.docu-nr = docu-nr
    AND t-l-order.betriebsnr GE 98:
    IF t-l-order.betriebsnr = 99 THEN t-l-order.geliefert = 0.
    t-l-order.betriebsnr = 2.
END.

FIND FIRST t-l-order WHERE t-l-order.pos GT 0 
    AND t-l-order.docu-nr = docu-nr 
    AND t-l-order.betriebsnr = 2 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE t-l-order THEN 
DO: 
    fl-code = 1.
    FIND FIRST hdrbuff WHERE hdrbuff.docu-nr = l-orderhdr.docu-nr
        AND RECID(hdrbuff) NE RECID(l-orderhdr) NO-LOCK NO-ERROR.
    IF AVAILABLE hdrbuff THEN
    DO:
        RUN new-po-number.
        ASSIGN l-orderhdr.docu-nr = new-docu-nr.
        avail-hdrbuff = YES.
        RETURN NO-APPLY.
    END.
END. 
FIND FIRST t-l-order WHERE t-l-order.docu-nr = docu-nr 
    AND t-l-order.pos GT 0 AND t-l-order.einzelpreis = 0 
    AND t-l-order.betriebsnr = 2 NO-LOCK NO-ERROR. 
IF AVAILABLE t-l-order THEN 
DO:
    fl-code = 2.
    RETURN NO-APPLY.
END. 

FOR EACH t-l-order WHERE t-l-order.pos GT 0:
  FIND FIRST l-art1 WHERE l-art1.artnr = t-l-order.artnr NO-LOCK NO-ERROR.
  FIND FIRST l-order WHERE RECID(l-order) = t-l-order.rec-id EXCLUSIVE-LOCK NO-ERROR.
  IF AVAILABLE l-order THEN
  DO:
    ASSIGN
      l-order.quality = STRING(t-l-order.disc, "99.99 ") 
        + STRING(t-l-order.vat, "99.99") + STRING(t-l-order.disc2, " 99.99")
        + STRING(t-l-order.disc-val, " >,>>>,>>>,>>9.999") + STRING(t-l-order.disc2-val, " >,>>>,>>>,>>9.999")
        + STRING(t-l-order.vat-val, " >,>>>,>>>,>>9.999") 
      l-order.warenwert = t-l-order.warenwert
      l-order.einzelpreis = t-l-order.einzelpreis
      l-order.lief-nr = lief-nr
      l-order.betriebsnr = 0.
    l-order.geliefert = t-l-order.geliefert.
    IF NOT l-order.flag THEN l-order.warenwert = l-order.warenwert * l-art1.lief-einheit. 
    FIND CURRENT l-order NO-LOCK.
  END.                           
  ELSE 
  DO:
    CREATE l-order.
    BUFFER-COPY t-l-order TO l-order.
    IF t-l-order.disc NE 0 OR t-l-order.disc2 NE 0 OR t-l-order.vat NE 0 
        OR t-l-order.disc-val NE 0 OR t-l-order.disc2-val NE 0 OR t-l-order.vat-val NE 0 THEN
    ASSIGN l-order.quality = STRING(t-l-order.disc, "99.99 ") 
        + STRING(t-l-order.vat, "99.99") + STRING(t-l-order.disc2, " 99.99")
        + STRING(t-l-order.disc-val, " >,>>>,>>>,>>9.999") + STRING(t-l-order.disc2-val, " >,>>>,>>>,>>9.999")
        + STRING(t-l-order.vat-val, " >,>>>,>>>,>>9.999").
    l-order.betriebsnr = 0.
  END.                               
END.

IF create-new THEN
DO:
    create l-od. 
    ASSIGN 
      l-od.docu-nr = docu-nr 
      l-od.pos = 0 
      l-od.bestelldatum = l-orderhdr.bestelldatum 
      l-od.lief-nr = lief-nr 
      l-od.op-art = 2 
      l-od.lief-fax[1] = pr 
      l-od.betriebsnr = 2.
END.

FIND FIRST l-od WHERE 
      l-od.docu-nr = docu-nr AND
      l-od.pos     = 0       AND
      l-od.op-art = 2 EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE l-od THEN
DO:
    ASSIGN 
      l-od.warenwert = globaldisc
      l-od.lief-nr = lief-nr
      l-od.lief-fax[1] = pr.
    FIND CURRENT l-od NO-LOCK.
END.
  
PROCEDURE new-po-number: 
DEFINE BUFFER l-orderhdr1 FOR l-orderhdr. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 973 NO-LOCK. 
  IF htparam.paramgruppe = 21 AND htparam.flogical THEN  /* htparam.paramgr -> htparam.paramgruppe (malik : fixing for serverless) */
  DO: 
    mm = month(billdate). 
    yy = year(billdate). 
    s = "P" + SUBSTR(STRING(year(billdate)),3,2) 
      + STRING(MONTH(billdate), "99"). 
    FOR EACH l-orderhdr1 WHERE MONTH(l-orderhdr1.bestelldatum) = mm 
      AND year(l-orderhdr1.bestelldatum) = yy 
      AND l-orderhdr1.betriebsnr LE 1 
      AND l-orderhdr1.docu-nr MATCHES "P*" NO-LOCK BY l-orderhdr1.docu-nr DESCENDING: 
      i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,6,5)). 
      i = i + 1. 
      new-docu-nr = s + STRING(i, "99999"). 
      RETURN. 
    END. 
    new-docu-nr = s + STRING(i, "99999"). 
    RETURN. 
  END. 
  s = "P" + SUBSTR(STRING(YEAR(billdate)),3,2) + STRING(MONTH(billdate), "99") 
     + STRING(day(billdate), "99"). 
  FOR EACH l-orderhdr1 WHERE l-orderhdr1.bestelldatum = billdate 
    AND l-orderhdr1.betriebsnr LE 1 
    AND l-orderhdr1.docu-nr MATCHES "P*" NO-LOCK BY l-orderhdr1.docu-nr DESCENDING: 
    i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,8,3)). 
    i = i + 1. 
    new-docu-nr = s + STRING(i, "999"). 
    RETURN. 
  END. 
  new-docu-nr = s + STRING(i, "999"). 
END. 


