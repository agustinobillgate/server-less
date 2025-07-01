DEFINE WORKFILE w-list 
  FIELD nr AS INTEGER 
  FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

DEFINE BUFFER l-order1 FOR l-order.

DEFINE TEMP-TABLE q2-list
    FIELD lief-nr       LIKE l-orderhdr.lief-nr
    FIELD lief-fax-1    LIKE l-order1.lief-fax[1]
    FIELD docu-nr       LIKE l-orderhdr.docu-nr
    FIELD firma         LIKE l-lieferant.firma
    FIELD bestelldatum  LIKE l-orderhdr.bestelldatum
    FIELD lieferdatum   LIKE l-orderhdr.lieferdatum
    FIELD wabkurz       LIKE w-list.wabkurz
    FIELD bestellart    LIKE l-orderhdr.bestellart
    FIELD lief-fax-3    LIKE l-orderhdr.lief-fax[3]
    FIELD besteller     LIKE l-orderhdr.besteller
    FIELD lief-fax-2    LIKE l-order1.lief-fax[2]
    FIELD betriebsnr    LIKE l-orderhdr.betriebsnr
    FIELD gedruckt      LIKE l-orderhdr.gedruckt.

DEF INPUT PARAMETER sorttype    AS INT.
DEF INPUT PARAMETER ponum       AS CHAR.
DEF INPUT PARAMETER supplier    AS CHAR.
DEF INPUT PARAMETER to-supp     AS CHAR.
DEF INPUT PARAMETER order-date  AS DATE.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

RUN currency-list.

IF sorttype = 1 THEN 
FOR EACH l-orderhdr WHERE l-orderhdr.betriebsnr LE 1 
    AND l-orderhdr.docu-nr GE ponum NO-LOCK, 
    FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
    AND l-lieferant.firma GE supplier AND l-lieferant.firma LE to-supp NO-LOCK, 
    FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
    AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
    BY l-lieferant.firma BY l-orderhdr.docu-nr:
    RUN assign-it.
END.
ELSE 
FOR EACH l-orderhdr WHERE l-orderhdr.bestelldatum = order-date 
    AND l-orderhdr.betriebsnr LE 1 AND l-orderhdr.docu-nr GE ponum NO-LOCK, 
    FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
    FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
    AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
    BY l-orderhdr.docu-nr:
    RUN assign-it.
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

PROCEDURE assign-it:
    CREATE q2-list.
    ASSIGN
    q2-list.lief-nr       = l-orderhdr.lief-nr
    q2-list.lief-fax-1    = l-order1.lief-fax[1]
    q2-list.docu-nr       = l-orderhdr.docu-nr
    q2-list.firma         = l-lieferant.firma
    q2-list.bestelldatum  = l-orderhdr.bestelldatum
    q2-list.lieferdatum   = l-orderhdr.lieferdatum
    q2-list.wabkurz       = w-list.wabkurz
    q2-list.bestellart    = l-orderhdr.bestellart
    q2-list.lief-fax-3    = l-orderhdr.lief-fax[3]
    q2-list.besteller     = l-orderhdr.besteller
    q2-list.lief-fax-2    = l-order1.lief-fax[2]
    q2-list.betriebsnr    = l-orderhdr.betriebsnr
    q2-list.gedruckt      = l-orderhdr.gedruckt.
END.
