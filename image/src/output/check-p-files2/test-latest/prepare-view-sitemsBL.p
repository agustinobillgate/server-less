/*Eko 29062015 add field remark on temp-table sitem-list*/

DEFINE TEMP-TABLE sitem-list
    FIELD artnr             LIKE l-order.artnr
    FIELD bezeich           LIKE l-artikel.bezeich 
    FIELD lief-fax          LIKE l-order.lief-fax 
    FIELD txtnr             LIKE l-order.txtnr 
    FIELD anzahl            LIKE l-order.anzahl
    FIELD geliefert         LIKE l-order.geliefert 
    FIELD einzelpreis       LIKE l-order.einzelpreis 
    FIELD warenwert         LIKE l-order.warenwert 
    FIELD lieferdatum-eff   LIKE l-order.lieferdatum-eff 
    FIELD angebot-lief      LIKE l-order.angebot-lief
    FIELD masseinheit       LIKE l-artikel.masseinheit 
    FIELD jahrgang          LIKE l-artikel.jahrgang
    FIELD quality           LIKE l-order.quality
    FIELD pos               LIKE l-order.pos
    FIELD remark            AS CHARACTER /*Eko 29062015 For Remarks*/
    .


DEFINE INPUT PARAMETER user-init        AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER docu-nr          AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER show-price      AS LOG  NO-UNDO.
DEFINE OUTPUT PARAMETER comments        AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR sitem-list.
/****************************************************************************/

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 

IF show-price THEN 
FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.loeschflag = 0, 
    FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr 
    NO-LOCK BY l-order.pos .
    RUN assign-it.
END.
ELSE 
FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.loeschflag = 0, 
    FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr 
    NO-LOCK BY l-order.pos. 
    RUN assign-it.
END.
 
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr 
    /*AND l-orderhdr.lief-nr = l-order.lief-nr*/ NO-LOCK NO-ERROR. 
IF AVAILABLE l-orderhdr THEN comments = l-orderhdr.lief-fax[3].

PROCEDURE assign-it :
    CREATE sitem-list.
    ASSIGN sitem-list.artnr             = l-order.artnr
           sitem-list.bezeich           = l-artikel.bezeich 
           sitem-list.lief-fax[3]       = l-order.lief-fax[3] 
           sitem-list.txtnr             = l-order.txtnr 
           sitem-list.anzahl            = l-order.anzahl
           sitem-list.geliefert         = l-order.geliefert 
           sitem-list.einzelpreis       = l-order.einzelpreis 
           sitem-list.warenwert         = l-order.warenwert 
           sitem-list.lieferdatum-eff   = l-order.lieferdatum-eff 
           sitem-list.angebot-lief[1]   = l-order.angebot-lief[1] 
           sitem-list.masseinheit       = l-artikel.masseinheit 
           sitem-list.lief-fax[2]       = l-order.lief-fax[2] 
           sitem-list.jahrgang          = l-artikel.jahrgang
           sitem-list.quality           = l-order.quality
           sitem-list.pos               = l-order.pos
           sitem-list.remark            = l-order.besteller /*Eko 29062015*/
        .
END.
