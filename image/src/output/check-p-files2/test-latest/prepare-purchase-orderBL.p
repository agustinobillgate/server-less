DEFINE buffer l-order1 FOR l-order. 

DEFINE WORKFILE w-list 
  FIELD nr AS INTEGER 
  FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

/*MTDEFINE TEMP-TABLE q1-list
    FIELD lief-nr           LIKE l-order.lief-nr
    FIELD docu-nr           LIKE l-order.docu-nr
    FIELD pos               LIKE l-order.pos
    FIELD artnr             LIKE l-order.artnr
    FIELD bezeich           LIKE l-art.bezeich
    FIELD anzahl            LIKE l-order.anzahl
    FIELD geliefert         LIKE l-order.geliefert
    FIELD angebot-lief-1    LIKE l-order.angebot-lief[1]
    FIELD rechnungswert     LIKE l-order.rechnungswert
    FIELD lief-fax-3        LIKE l-order.lief-fax[3]
    FIELD txtnr             LIKE l-order.txtnr
    FIELD lieferdatum-eff   LIKE l-order.lieferdatum-eff
    FIELD einzelpreis       LIKE l-order.einzelpreis
    FIELD lief-fax-2        LIKE l-order.lief-fax[2].*/

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

DEF INPUT  PARAMETER lief-nr        AS INTEGER.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER enforce-rflag  AS LOGICAL.
DEF OUTPUT PARAMETER p-1093         AS INT.
DEF OUTPUT PARAMETER p-464          AS INT.
DEF OUTPUT PARAMETER p-220          AS INT.
/*MTDEF OUTPUT PARAMETER TABLE FOR q1-list.*/
DEF OUTPUT PARAMETER TABLE FOR q2-list.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
 
FIND FIRST htparam WHERE paramnr = 222 NO-LOCK. 
enforce-rflag = flogical. 
 
RUN currency-list. 
RUN disp-it. 

RUN htpint.p(1093, OUTPUT p-1093).
RUN htpint.p(464, OUTPUT p-464).
RUN htpint.p(220, OUTPUT p-220).

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

PROCEDURE disp-it: 
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
 
  FIND FIRST q2-list NO-ERROR.
  IF AVAILABLE q2-list THEN
  DO: 
    /*MTFOR EACH l-order WHERE l-order.docu-nr = q2-list.docu-nr 
        AND l-order.pos GT 0 AND l-order.loeschflag = 0, 
        FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK BY l-order.pos:
        CREATE q1-list.
        ASSIGN
            q1-list.lief-nr           = l-order.lief-nr
            q1-list.docu-nr           = l-order.docu-nr
            q1-list.pos               = l-order.pos
            q1-list.artnr             = l-order.artnr
            q1-list.bezeich           = l-art.bezeich
            q1-list.anzahl            = l-order.anzahl
            q1-list.geliefert         = l-order.geliefert
            q1-list.angebot-lief-1    = l-order.angebot-lief[1]
            q1-list.rechnungswert     = l-order.rechnungswert
            q1-list.lief-fax-3        = l-order.lief-fax[3]
            q1-list.txtnr             = l-order.txtnr
            q1-list.lieferdatum-eff   = l-order.lieferdatum-eff
            q1-list.einzelpreis       = l-order.einzelpreis
            q1-list.lief-fax-2        = l-order.lief-fax[2].
    END.*/
    /*MTAPPLY "entry" TO b2 IN FRAME frame1.*/
  END. 
END. 

