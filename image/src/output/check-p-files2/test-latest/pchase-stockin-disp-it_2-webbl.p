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
DEF INPUT PARAMETER f-date      AS DATE. /* Penambahan fromdate-todate by gerald 110220 */
DEF INPUT PARAMETER t-date      AS DATE. /* Penambahan fromdate-todate by gerald 110220 */
DEFINE INPUT PARAMETER app-sort     AS CHARACTER. /* Dzikri 6BFA2B - sort by approval */
DEF OUTPUT PARAMETER TABLE FOR q2-list.

/* Dzikri 6BFA2B - sort by approval */
DEFINE VARIABLE p-71              AS LOGICAL.
DEFINE VARIABLE approval          AS INTEGER.
DEFINE VARIABLE app-lvl           AS INTEGER.

FIND FIRST htparam WHERE paramnr EQ 71 NO-LOCK.
IF htparam.paramgr EQ 21 THEN
    ASSIGN p-71 = htparam.flogical.
    
IF app-sort EQ "Approve 2" THEN
    ASSIGN approval = 1.
IF app-sort EQ "Approve 3" THEN
    ASSIGN approval = 2.
IF app-sort EQ "Approve 4" THEN
    ASSIGN approval = 3.
IF app-sort EQ "Approved" THEN
    ASSIGN approval = 4.
/* Dzikri 6BFA2B - END*/

RUN currency-list.

/* Modified Penambahan fromdate-todate by gerald 110220 */

/* Oscar (26/03/25) - 7211C6 - changes query to fix bug*/
IF supplier EQ ? THEN supplier = "".
IF to-supp EQ ? THEN to-supp = "".
IF TRIM(ponum) EQ "" THEN ponum = "".

supplier = "*" + supplier + "*".
to-supp = "*" + to-supp + "*".
ponum = "*" + ponum + "*".

IF sorttype EQ 1 THEN
DO:
    FOR EACH l-orderhdr WHERE l-orderhdr.betriebsnr LE 1 
        AND l-orderhdr.docu-nr MATCHES ponum NO-LOCK, 
        FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
        AND l-lieferant.firma MATCHES supplier NO-LOCK, 
        FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
        AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK 
        BY l-lieferant.firma BY l-orderhdr.docu-nr:

        RUN assign-it.
    END.
END.
IF sorttype EQ 2 THEN
DO:
    FOR EACH l-orderhdr WHERE l-orderhdr.bestelldatum = order-date 
        AND l-orderhdr.betriebsnr LE 1 
        AND l-orderhdr.docu-nr MATCHES ponum NO-LOCK, 
        FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
        FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
        AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK 
        BY l-orderhdr.docu-nr:

        RUN assign-it.
    END.
END.

/* Oscar (26/03/25) - 7211C6 - changes query to fix bug
/*modified by agung*/
IF sorttype = 1 AND supplier NE "" THEN DO:
    FOR EACH l-orderhdr WHERE l-orderhdr.betriebsnr LE 1 
        AND l-orderhdr.docu-nr GE ponum NO-LOCK, 
        FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
        AND l-lieferant.firma GE supplier AND l-lieferant.firma LE to-supp NO-LOCK, 
        FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
        AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
        BY l-lieferant.firma BY l-orderhdr.docu-nr :
        RUN assign-it.
    END.
END.
ELSE IF sorttype = 1 AND ponum NE "" THEN DO:
    FOR EACH l-orderhdr WHERE l-orderhdr.betriebsnr LE 1 
        AND l-orderhdr.docu-nr GE ponum NO-LOCK, 
        FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
        AND l-lieferant.firma GE supplier AND l-lieferant.firma LE to-supp NO-LOCK, 
        FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
        AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
        BY l-orderhdr.docu-nr BY l-lieferant.firma  :
        RUN assign-it.
    END.
END.
ELSE IF sorttype = 2 THEN
FOR EACH l-orderhdr WHERE l-orderhdr.bestelldatum = order-date 
    AND l-orderhdr.betriebsnr LE 1 AND l-orderhdr.docu-nr GE ponum NO-LOCK, 
    FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
    FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
    AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
    BY l-orderhdr.docu-nr:
    RUN assign-it.
END.
ELSE
FOR EACH l-orderhdr WHERE l-orderhdr.bestelldatum GE f-date AND l-orderhdr.bestelldatum LE t-date
    AND l-orderhdr.betriebsnr LE 1 AND l-orderhdr.docu-nr GE ponum NO-LOCK, 
    FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
    FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
    AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
    BY l-orderhdr.docu-nr:
    RUN assign-it.
END. */

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
    /*
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
        q2-list.gedruckt      = l-orderhdr.gedruckt
    . 
    */
    /* Dzikri 6BFA2B - sort by approval */
    IF p-71 AND app-sort NE "ALL" THEN
    DO:
        ASSIGN app-lvl = 0.
        FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE queasy:
            ASSIGN app-lvl = queasy.number1.
            FIND NEXT queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
        END.

        IF app-sort EQ "Approve 1" AND app-lvl = 0 THEN
        DO:
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
                q2-list.gedruckt      = l-orderhdr.gedruckt
            .
        END.
        ELSE 
        DO:
            IF app-lvl EQ approval THEN
            DO:
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
                    q2-list.gedruckt      = l-orderhdr.gedruckt
                .
            END.
        END.
    END.
    ELSE
    DO:
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
            q2-list.gedruckt      = l-orderhdr.gedruckt
        .
    END.
    /* Dzikri 6BFA2B - END */
END.
