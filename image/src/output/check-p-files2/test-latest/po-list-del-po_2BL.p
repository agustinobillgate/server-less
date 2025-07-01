DEFINE TEMP-TABLE cost-list 
    FIELD nr AS INTEGER 
    FIELD bezeich AS CHAR FORMAT "x(24)". 

DEFINE TEMP-TABLE w-list 
    FIELD nr AS INTEGER 
    FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

DEFINE TEMP-TABLE q2-list
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
    /*Naufal - add field user yang merelease po*/
    FIELD username                  AS CHAR	
    FIELD del-reason                AS CHAR LABEL "Delete Reason" FORMAT "x(32)" /*gerald 080520 Reason on delete*/
    .

DEFINE INPUT PARAMETER TABLE FOR q2-list.
DEFINE INPUT PARAMETER user-init           AS CHAR.
DEFINE INPUT PARAMETER billdate            AS DATE.
DEFINE INPUT PARAMETER l-orderhdr-docu-nr  AS CHAR.
DEFINE INPUT PARAMETER bediener-username   AS CHAR.
DEFINE INPUT PARAMETER curr-mode           AS CHAR.

RUN del-reason.
IF curr-mode EQ "delete" THEN
DO:
    RUN del-po.
END.
ELSE IF curr-mode EQ "partial" THEN
DO:
    RUN close-po.
END.

PROCEDURE del-reason:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    FIND FIRST q2-list WHERE q2-list.docu-nr = l-orderhdr-docu-nr NO-LOCK NO-ERROR.
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = q2-list.docu-nr NO-LOCK NO-ERROR.
    IF AVAILABLE l-orderhdr THEN 
    DO:
        FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
        ASSIGN l-orderhdr.lief-fax[3] = l-orderhdr.lief-fax[3] + "-" + user-init + ";" + q2-list.del-reason.
        FIND CURRENT l-orderhdr NO-LOCK.
        RELEASE l-orderhdr.
    END.
END PROCEDURE.

PROCEDURE del-po:   /* NO incoming stocks / cancel PO , OR A/P paid ==> see ap-debtpay.p */ 
    DEFINE BUFFER l-od FOR l-order. 
    /*MTCURRENT-WINDOW:LOAD-MOUSE-POINTER("wait"). 
    PROCESS EVENTS.*/

    /*Alder - Serverless - Issue 573 - Start*/
    /*FIND FIRST l-od WHERE l-od.docu-nr = l-orderhdr-docu-nr AND l-od.pos EQ 0 EXCLUSIVE-LOCK.*/
    FIND FIRST l-od WHERE l-od.docu-nr EQ l-orderhdr-docu-nr AND l-od.pos EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-od THEN
    DO:
        FIND CURRENT l-od EXCLUSIVE-LOCK.
        ASSIGN
            l-od.loeschflag = 2
            l-od.lieferdatum-eff = billdate 
            l-od.lief-fax[3] = bediener-username. 
        FIND CURRENT l-od NO-LOCK.
    
        /*Ragung add log*/
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN 
        DO:
            CREATE res-history.
            ASSIGN 
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Delete Po - Document No : " + STRING(l-od.docu-nr)
                res-history.action      = "Delete Po".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.

        RELEASE l-od.
    END.
    /*Alder - Serverless - Issue 573 - End*/
  
    FOR EACH l-od WHERE l-od.docu-nr = l-orderhdr-docu-nr 
        AND l-od.pos GT 0 
        AND l-od.loeschflag = 0 
        EXCLUSIVE-LOCK:
        ASSIGN
            l-od.loeschflag = 2 
            l-od.lieferdatum = billdate 
            l-od.lief-fax[2] = bediener-username. 
        RELEASE l-od. 
    END. 
    /*MTCURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow").*/
END PROCEDURE. 

PROCEDURE close-po:   /*MNAUFAL - new procedure po will be closed if some of the items already received */ 
    DEFINE BUFFER l-od FOR l-order. 

    /*Alder - Serverless - Issue 573 - Start*/
    /*FIND FIRST l-od WHERE l-od.docu-nr = l-orderhdr-docu-nr AND l-od.pos EQ 0 EXCLUSIVE-LOCK.*/
    FIND FIRST l-od WHERE l-od.docu-nr EQ l-orderhdr-docu-nr AND l-od.pos EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-od THEN
    DO:
        FIND CURRENT l-od EXCLUSIVE-LOCK.
        ASSIGN
            l-od.loeschflag = 1
            l-od.lieferdatum-eff = billdate 
            l-od.lief-fax[3] = bediener-username. 
        FIND CURRENT l-od NO-LOCK.
    
        /*Ragung add log*/
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN 
        DO:
            CREATE res-history.
            ASSIGN 
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Delete Po - Document No : " + STRING(l-od.docu-nr)
                res-history.action      = "Delete Po Partial".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.

        RELEASE l-od.
    END.
    /*Alder - Serverless - Issue 573 - End*/
    
    FOR EACH l-od WHERE l-od.docu-nr EQ l-orderhdr-docu-nr 
        AND l-od.pos GT 0 
        AND l-od.loeschflag = 0 
        EXCLUSIVE-LOCK:
        ASSIGN
            l-od.loeschflag = 1 
            l-od.lieferdatum = billdate 
            l-od.lief-fax[2] = bediener-username. 
        RELEASE l-od. 
    END.
END PROCEDURE. 
