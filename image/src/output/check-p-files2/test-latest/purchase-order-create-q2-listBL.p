DEFINE buffer l-order1 FOR l-order. 

DEFINE WORKFILE w-list 
  FIELD nr AS INTEGER 
  FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

DEFINE TEMP-TABLE q2-list
    FIELD lief-nr       AS INTEGER      FORMAT ">,>>>,>>9"
    FIELD docu-nr       AS CHARACTER    FORMAT "x(16)"
    FIELD bestelldatum  AS DATE         FORMAT "99/99/99"
    FIELD lieferdatum   AS DATE         FORMAT "99/99/99"
    FIELD wabkurz       AS CHARACTER    FORMAT "x(4)"
    FIELD bestellart    AS CHARACTER    FORMAT "x(10)"
    FIELD gedruckt      AS DATE         FORMAT "99/99/99"
    FIELD besteller     AS CHARACTER    FORMAT "x(24)"
    FIELD lief-fax-3    AS CHARACTER    FORMAT "x(15)"
    FIELD lief-fax-2    AS CHARACTER    FORMAT "x(15)"
    FIELD rechnungswert AS DECIMAL      FORMAT "->,>>>,>>9.999"
    FIELD rec-id        AS INT.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF INPUT PARAMETER lief-nr AS INT.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

RUN currency-list.

/*
IF case-type = 1 THEN /*chg*/
DO:
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-LOCK.
    FIND FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK.
    FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
        AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK.
    CREATE q2-list.
        ASSIGN
            q2-list.lief-nr       = l-orderhdr.lief-nr
            q2-list.docu-nr       = l-orderhdr.docu-nr
            q2-list.bestelldatum  = l-orderhdr.bestelldatum
            q2-list.lieferdatum   = l-orderhdr.lieferdatum
            q2-list.wabkurz       = w-list.wabkurz
            q2-list.bestellart    = l-orderhdr.bestellart
            q2-list.gedruckt      = l-orderhdr.gedruckt
            q2-list.besteller     = l-orderhdr.besteller
            q2-list.lief-fax-3    = l-orderhdr.lief-fax[3]
            q2-list.lief-fax-2    = l-order1.lief-fax[2]
            q2-list.rechnungswert = l-order1.rechnungswert
            q2-list.rec-id        = RECID(l-orderhdr).
END.
ELSE IF case-type = 2 THEN /*new*/
DO:
    FOR EACH l-orderhdr WHERE l-orderhdr.lief-nr = lief-nr NO-LOCK, 
        FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
        FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
        AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
        BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
        CREATE q2-list.
        ASSIGN
            q2-list.lief-nr       = l-orderhdr.lief-nr
            q2-list.docu-nr       = l-orderhdr.docu-nr
            q2-list.bestelldatum  = l-orderhdr.bestelldatum
            q2-list.lieferdatum   = l-orderhdr.lieferdatum
            q2-list.wabkurz       = w-list.wabkurz
            q2-list.bestellart    = l-orderhdr.bestellart
            q2-list.gedruckt      = l-orderhdr.gedruckt
            q2-list.besteller     = l-orderhdr.besteller
            q2-list.lief-fax-3    = l-orderhdr.lief-fax[3]
            q2-list.lief-fax-2    = l-order1.lief-fax[2]
            q2-list.rechnungswert = l-order1.rechnungswert
            q2-list.rec-id        = RECID(l-orderhdr).
    END.
END.
*/

FOR EACH l-orderhdr WHERE l-orderhdr.lief-nr = lief-nr NO-LOCK, 
    FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
    FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
    AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
    BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
    CREATE q2-list.
    ASSIGN
      q2-list.lief-nr       = l-orderhdr.lief-nr
      q2-list.docu-nr       = l-orderhdr.docu-nr
      q2-list.bestelldatum  = l-orderhdr.bestelldatum
      q2-list.lieferdatum   = l-orderhdr.lieferdatum
      q2-list.wabkurz       = w-list.wabkurz
      q2-list.bestellart    = l-orderhdr.bestellart
      q2-list.gedruckt      = l-orderhdr.gedruckt
      q2-list.besteller     = l-orderhdr.besteller
      q2-list.lief-fax-3    = l-orderhdr.lief-fax[3]
      q2-list.lief-fax-2    = l-order1.lief-fax[2]
      q2-list.rechnungswert = l-order1.rechnungswert
      q2-list.rec-id        = RECID(l-orderhdr).
END.

PROCEDURE currency-list: 
DEFINE VARIABLE local-nr AS INTEGER INITIAL 0. 
  FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN local-nr = waehrung.waehrungsnr. 
 
  create w-list. 
  IF local-nr NE 0 THEN w-list.wabkurz = waehrung.wabkurz. 
 
  FOR EACH waehrung NO-LOCK BY waehrung.wabkurz: 
      create w-list. 
      w-list.nr = waehrung.waehrungsnr. 
      w-list.wabkurz = waehrung.wabkurz. 
  END. 
END. 

