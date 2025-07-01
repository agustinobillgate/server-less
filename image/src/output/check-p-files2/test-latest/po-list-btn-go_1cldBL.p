
DEFINE WORKFILE w-list 
  FIELD nr AS INTEGER 
  FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

DEFINE WORKFILE cost-list 
  FIELD nr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

DEF TEMP-TABLE q2-list
    FIELD bestelldatum              LIKE l-orderhdr.bestelldatum
    FIELD bezeich                   LIKE cost-list.bezeich
    FIELD firma                     LIKE l-lieferant.firma
    FIELD docu-nr                   LIKE l-orderhdr.docu-nr
    FIELD l-orderhdr-lieferdatum    LIKE l-orderhdr.lieferdatum
    FIELD wabkurz                   LIKE w-list.wabkurz
    FIELD bestellart                LIKE l-orderhdr.bestellart
    FIELD gedruckt                  LIKE l-orderhdr.gedruckt
    FIELD l-orderhdr-besteller      LIKE l-orderhdr.besteller
    FIELD l-order-gedruckt          LIKE l-order.gedruckt
    FIELD zeit                      LIKE l-order.zeit
    FIELD lief-fax-2                LIKE l-order.lief-fax[2]
    FIELD l-order-lieferdatum       LIKE l-order.lieferdatum
    FIELD lief-fax-3                LIKE l-order.lief-fax[3]
    FIELD lieferdatum-eff           LIKE l-order.lieferdatum-eff
    FIELD lief-fax-1                LIKE l-order.lief-fax[1]
    FIELD lief-nr                   LIKE l-order.lief-nr
    FIELD username                  AS CHAR
    FIELD del-reason                AS CHAR FORMAT "x(32)" /*gerald 080520 Reason on delete*/
    FIELD tot-amount                AS DECIMAL
    .

DEF INPUT PARAMETER usrName     AS CHAR.
DEF INPUT PARAMETER po-number   AS CHAR.
DEF INPUT PARAMETER dml-only    AS LOGICAL.
DEF INPUT PARAMETER pr-only     AS LOGICAL.
DEF INPUT PARAMETER excl-dml-pr AS LOGICAL.
DEF OUTPUT PARAMETER p-267      AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

DEFINE buffer l-order1 FOR l-order.
DEFINE BUFFER l-order2 FOR l-order.
DEFINE BUFFER l-art    FOR l-artikel.

DEFINE VARIABLE p-71 AS LOGICAL.
DEFINE VARIABLE loop AS INTEGER.
DEFINE VARIABLE cost-list-bezeich LIKE cost-list.bezeich. /* Oscar (09 September 2024) - 1ECC1E */
DEFINE VARIABLE w-list-wabkurz    LIKE w-list.wabkurz. /* Oscar (09 September 2024) - 1ECC1E */

RUN create-costlist.
RUN currency-list.
RUN disp-po.

FIND FIRST htparam WHERE paramnr = 267 NO-LOCK.
p-267 = htparam.flogical.

FIND FIRST htparam WHERE paramnr EQ 71 NO-LOCK.
IF htparam.paramgr EQ 21 THEN
    p-71 = htparam.flogical.

PROCEDURE disp-po:
  IF usrName = "" THEN 
  FOR EACH l-orderhdr 
      WHERE l-orderhdr.betriebsnr LE 1 
      AND l-orderhdr.docu-nr = po-number NO-LOCK, 
      /* FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
      FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  */  /* Oscar (09 September 2024) - 1ECC1E */
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
      FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
      AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
      BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
        
        /* Start - 1ECC1E */
        ASSIGN
        cost-list-bezeich   = ""
        w-list-wabkurz      = "".

        FIND FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK NO-ERROR.
        FIND FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK NO-ERROR.

        IF AVAILABLE w-list THEN w-list-wabkurz = w-list.wabkurz.
        IF AVAILABLE cost-list THEN cost-list-bezeich = cost-list.bezeich.
        /* End - 1ECC1E */

        IF dml-only THEN DO:
             IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                 RUN cr-temp-table.
        END.
        ELSE IF pr-only THEN
        DO:
            IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN RUN cr-temp-table.
        END.
        ELSE IF excl-dml-pr THEN
        DO:
            IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN RUN cr-temp-table.
        END.
        ELSE RUN cr-temp-table.
  END.
  ELSE IF usrName NE "" THEN 
  FOR EACH l-orderhdr 
      WHERE l-orderhdr.betriebsnr LE 1 
      AND l-orderhdr.docu-nr = po-number 
      AND l-orderhdr.besteller = usrName NO-LOCK, 
      /* FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
      FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  */
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
      FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
      AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
      BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
        
        ASSIGN
        cost-list-bezeich   = ""
        w-list-wabkurz      = "".

        FIND FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK NO-ERROR.
        FIND FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK NO-ERROR.

        IF AVAILABLE w-list THEN w-list-wabkurz = w-list.wabkurz.
        IF AVAILABLE cost-list THEN cost-list-bezeich = cost-list.bezeich.

        IF dml-only THEN DO:
             IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                 RUN cr-temp-table.
        END.
        ELSE IF pr-only THEN
        DO:
            IF SUBSTR(l-order1.lief-fax[1],1,1) EQ "R" THEN RUN cr-temp-table.
        END.
        ELSE IF excl-dml-pr THEN
        DO:
            IF SUBSTR(l-order1.lief-fax[1],1,1) NE "R" AND 
                (SUBSTR(l-order1.lief-fax[1],1,1) NE "D" AND l-order1.lief-fax[3] NE "DML") THEN RUN cr-temp-table.
        END.
        ELSE RUN cr-temp-table.
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
    DEFINE VARIABLE t-amount AS DECIMAL.
    /*MTCREATE t-l-orderhdr.
    BUFFER-COPY l-orderhdr TO t-l-orderhdr.*/
    CREATE q2-list.
    ASSIGN
    q2-list.bestelldatum = l-orderhdr.bestelldatum
    q2-list.bezeich = cost-list-bezeich /* Oscar (09 September 2024) - 1ECC1E */
    q2-list.firma = l-lieferant.firma
    q2-list.docu-nr = l-orderhdr.docu-nr
    q2-list.l-orderhdr-lieferdatum = l-orderhdr.lieferdatum
    q2-list.wabkurz = w-list-wabkurz /* Oscar (09 September 2024) - 1ECC1E */
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
    /*Naufal - if param 71 then fill from queasy 245*/
    IF p-71 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE queasy:
            IF q2-list.username NE "" THEN
            DO:
                IF NUM-ENTRIES(q2-list.username,";") LT 4 THEN
                    q2-list.username = q2-list.username + ENTRY(1,queasy.char3,"|") + ";".
                ELSE
                    q2-list.username = q2-list.username + ENTRY(1,queasy.char3,"|").
            END.
            ELSE
            DO:
                q2-list.username = ENTRY(1,queasy.char3,"|") + ";".
            END.
            FIND NEXT queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
        END.
        DO loop = 1 TO 4:
            IF NUM-ENTRIES(q2-list.username,";") NE 4 THEN
            DO:
                q2-list.username = q2-list.username + ";".
            END.
        END.
    END.
    ELSE
    DO:
	    /*Naufal - add look for user that release po on queasy*/
        FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            /*Naufal - assign field user yang merelease po*/
            q2-list.username = queasy.char3.
        END.
        ELSE 
        DO:
            q2-list.username = "".
        END.
    END.
    FIND FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
        AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-order2:
        FIND FIRST l-art WHERE l-art.artnr = l-order2.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE l-art THEN 
        DO:
            t-amount = t-amount + l-order2.warenwert.
        END.
        FIND NEXT l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
            AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
    END.
    ASSIGN
        q2-list.tot-amount = t-amount.
END.
