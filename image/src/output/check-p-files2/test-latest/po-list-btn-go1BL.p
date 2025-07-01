DEF TEMP-TABLE q2-list
    FIELD bestelldatum           LIKE l-orderhdr.bestelldatum
    FIELD bezeich                AS CHAR
    FIELD firma                  LIKE l-lieferant.firma
    FIELD docu-nr                LIKE l-orderhdr.docu-nr
    FIELD l-orderhdr-lieferdatum LIKE l-orderhdr.lieferdatum
    FIELD wabkurz                AS CHAR
    FIELD bestellart             LIKE l-orderhdr.bestellart
    FIELD gedruckt               LIKE l-orderhdr.gedruckt
    FIELD l-orderhdr-besteller   LIKE l-orderhdr.besteller
    FIELD l-order-gedruckt       LIKE l-order.gedruckt
    FIELD zeit                   LIKE l-order.zeit
    FIELD lief-fax-2             LIKE l-order.lief-fax[2]
    FIELD l-order-lieferdatum    LIKE l-order.lieferdatum
    FIELD lief-fax-3             LIKE l-order.lief-fax[3]
    FIELD lieferdatum-eff        LIKE l-order.lieferdatum-eff
    FIELD lief-fax-1             LIKE l-order.lief-fax[1]
    FIELD lief-nr                LIKE l-order.lief-nr.

DEFINE WORKFILE w-list 
  FIELD nr AS INTEGER 
  FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

DEFINE WORKFILE cost-list 
  FIELD nr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

DEF INPUT PARAMETER usrName AS CHAR.
DEF INPUT PARAMETER po-number AS CHAR.
DEF OUTPUT PARAMETER p-267          AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

DEFINE buffer l-order1 FOR l-order. 

RUN create-costlist.
RUN currency-list.
RUN disp-po.
FIND FIRST htparam WHERE paramnr = 267 NO-LOCK.
p-267 = htparam.flogical.


PROCEDURE disp-po:
  IF usrName = "" THEN 
  FOR EACH l-orderhdr 
      WHERE l-orderhdr.betriebsnr LE 1 
      AND l-orderhdr.docu-nr = po-number NO-LOCK, 
      FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
      FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
      FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
      AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
      BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
      RUN cr-temp-table.
  END.
  ELSE IF usrName NE "" THEN 
  FOR EACH l-orderhdr 
      WHERE l-orderhdr.betriebsnr LE 1 
      AND l-orderhdr.docu-nr = po-number 
      AND l-orderhdr.besteller = usrName NO-LOCK, 
      FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
      FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
      FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
      AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
      BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
      RUN cr-temp-table.
  END.
END.

PROCEDURE create-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.nr = INTEGER(parameters.varname). 
    cost-list.bezeich = parameters.vstring. 
  END. 
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

PROCEDURE cr-temp-table:
    /*MTCREATE t-l-orderhdr.
    BUFFER-COPY l-orderhdr TO t-l-orderhdr.*/
    CREATE q2-list.
    ASSIGN
    q2-list.bestelldatum = l-orderhdr.bestelldatum
    q2-list.bezeich = cost-list.bezeich
    q2-list.firma = l-lieferant.firma
    q2-list.docu-nr = l-orderhdr.docu-nr
    q2-list.l-orderhdr-lieferdatum = l-orderhdr.lieferdatum
    q2-list.wabkurz = w-list.wabkurz
    q2-list.bestellart = l-orderhdr.bestellart
    q2-list.gedruckt = l-orderhdr.gedruckt
    q2-list.l-orderhdr-besteller = l-orderhdr.besteller
    q2-list.l-order-gedruckt = l-order1.gedruckt
    q2-list.zeit = l-order1.zeit
    q2-list.lief-fax-2 = l-order1.lief-fax[2]
    q2-list.l-order-lieferdatum = l-order1.lieferdatum
    q2-list.lief-fax-3 = l-order1.lief-fax[3]
    q2-list.lieferdatum-eff = l-order1.lieferdatum-eff
    q2-list.lief-fax-1 = l-order1.lief-fax[1]
    q2-list.lief-nr = l-order1.lief-nr.
END.
