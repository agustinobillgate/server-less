DEF TEMP-TABLE t-l-lieferant
    FIELD lief-nr     LIKE l-lieferant.lief-nr
    FIELD firma       LIKE l-lieferant.firma
    FIELD telefon     LIKE l-lieferant.telefon
    FIELD fax         LIKE l-lieferant.fax
    FIELD namekontakt LIKE l-lieferant.namekontakt
    FIELD rec-id      AS INT.

DEFINE TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF INPUT PARAMETER lief-nr AS INTEGER.
DEF OUTPUT PARAMETER local-nr AS INT.
DEF OUTPUT PARAMETER supplier AS CHAR.
DEF OUTPUT PARAMETER currdate AS DATE.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR t-l-lieferant.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN err-code = 1.
ELSE
DO:
    local-nr = waehrung.waehrungsnr. 
 
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
    supplier = l-lieferant.firma. 
    RUN new-po-number. 
    FIND CURRENT l-orderhdr.
    CREATE t-l-orderhdr.
    BUFFER-COPY l-orderhdr TO t-l-orderhdr.
    ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).
    FIND CURRENT l-lieferant.
    CREATE t-l-lieferant.
    ASSIGN
    t-l-lieferant.lief-nr     = l-lieferant.lief-nr
    t-l-lieferant.firma       = l-lieferant.firma
    t-l-lieferant.rec-id      = RECID(l-lieferant)
    t-l-lieferant.telefon     = l-lieferant.telefon
    t-l-lieferant.fax         = l-lieferant.fax
    t-l-lieferant.namekontakt = l-lieferant.namekontakt.
END.

PROCEDURE new-po-number: 
DEFINE BUFFER l-orderhdr1 FOR l-orderhdr. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE docu-nr AS CHAR. 

  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  currdate = htparam.fdate. 
  FIND FIRST htparam WHERE paramnr = 973 NO-LOCK. 
  create l-orderhdr. 
  IF htparam.paramgruppe = 21 AND htparam.flogical THEN /* htparam.paramgr -> htparam.paramgruppe (malik : fixing for serverless) */
  DO: 
    mm = month(currdate). 
    yy = year(currdate). 
    s = "P" + SUBSTR(STRING(year(currdate)),3,2) 
      + STRING(MONTH(currdate), "99"). 
    FOR EACH l-orderhdr1 WHERE MONTH(l-orderhdr1.bestelldatum) = mm 
      AND year(l-orderhdr1.bestelldatum) = yy 
      AND l-orderhdr1.betriebsnr LE 1 
      AND l-orderhdr1.docu-nr MATCHES "P*" NO-LOCK BY l-orderhdr1.docu-nr DESCENDING: 
      i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,6,5)). 
      i = i + 1. 
      docu-nr = s + STRING(i, "99999"). 
      l-orderhdr.docu-nr = docu-nr.
      RETURN. 
    END. 
    docu-nr = s + STRING(i, "99999"). 
    l-orderhdr.docu-nr = docu-nr.
    RETURN. 
  END. 
  
  s = "P" + SUBSTR(STRING(YEAR(currdate)),3,2) + STRING(MONTH(currdate), "99") 
     + STRING(day(currdate), "99"). 
  FOR EACH l-orderhdr1 WHERE l-orderhdr1.bestelldatum = currdate 
    AND l-orderhdr1.betriebsnr LE 1 
    AND l-orderhdr1.docu-nr MATCHES "P*" NO-LOCK BY l-orderhdr1.docu-nr DESCENDING: 
    i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,8,3)). 
    i = i + 1. 
    docu-nr = s + STRING(i, "999"). 
    l-orderhdr.docu-nr = docu-nr.
    RETURN. 
  END. 
  docu-nr = s + STRING(i, "999"). 
  l-orderhdr.docu-nr = docu-nr.
END. 
