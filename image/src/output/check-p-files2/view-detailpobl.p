
DEF TEMP-TABLE q1-list
    FIELD artnr             LIKE l-order.artnr
    FIELD pos               LIKE l-order.pos
    FIELD bezeich           LIKE l-artikel.bezeich
    FIELD geliefert         LIKE l-order.geliefert
    FIELD angebot-lief1     LIKE l-order.angebot-lief[1]
    FIELD masseinheit       LIKE l-artikel.masseinheit
    FIELD lief-fax3         LIKE l-order.lief-fax[3]
    FIELD txtnr             LIKE l-order.txtnr
    FIELD lieferdatum-eff   LIKE l-order.lieferdatum-eff
    FIELD anzahl            LIKE l-order.anzahl
    FIELD einzelpreis       LIKE l-order.einzelpreis
    FIELD warenwert         LIKE l-order.warenwert
    FIELD lief-fax2         LIKE l-order.lief-fax[2]
    FIELD jahrgang          LIKE l-artikel.jahrgang
    FIELD comment           AS CHAR
    FIELD curr-bez          AS CHAR INIT ""
    FIELD fg-col            AS INTEGER INIT 0.

DEF INPUT  PARAMETER docu-nr    AS CHAR. 
DEF INPUT  PARAMETER user-init  AS CHAR.
DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 

FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 


IF show-price THEN 
FOR EACH l-order WHERE l-order.docu-nr = docu-nr
    AND l-order.pos GT 0 AND l-order.loeschflag LE 1,
    FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr
    NO-LOCK BY l-order.pos:
    RUN assign-it.
END.
ELSE 
FOR EACH l-order WHERE l-order.docu-nr = docu-nr
    AND l-order.pos GT 0 AND l-order.loeschflag LE 1,
    FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr
    NO-LOCK BY l-order.pos:
    RUN assign-it.
END.
 

PROCEDURE assign-it:
    CREATE q1-list.
    ASSIGN
    q1-list.artnr             = l-order.artnr
    q1-list.pos               = l-order.pos
    q1-list.bezeich           = l-artikel.bezeich
    q1-list.geliefert         = l-order.geliefert
    q1-list.angebot-lief1     = l-order.angebot-lief[1]
    q1-list.masseinheit       = l-artikel.masseinheit
    q1-list.lief-fax3         = l-order.lief-fax[3]
    q1-list.txtnr             = l-order.txtnr
    q1-list.lieferdatum-eff   = l-order.lieferdatum-eff
    q1-list.anzahl            = l-order.anzahl
    q1-list.einzelpreis       = l-order.einzelpreis
    q1-list.warenwert         = l-order.warenwert
    q1-list.lief-fax2         = l-order.lief-fax[2]
    q1-list.jahrgang          = l-artikel.jahrgang.

    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr 
      AND l-orderhdr.lief-nr = l-order.lief-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-orderhdr THEN q1-list.comment = l-orderhdr.lief-fax[3].

    IF AVAILABLE l-artikel AND l-artikel.jahrgang = 1 
    AND AVAILABLE l-order AND length(l-order.quality) GT 11 THEN 
    ASSIGN q1-list.fg-col = 12.

    IF l-artikel.jahrgang = 1 THEN 
    DO: 
      IF length(l-order.quality) GT 11 THEN 
      DO: 
        q1-list.curr-bez = SUBSTR(l-order.quality,12,length(l-order.quality)). 
      END. 
    END. 
END.
