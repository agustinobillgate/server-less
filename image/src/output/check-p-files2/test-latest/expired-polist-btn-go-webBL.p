DEFINE TEMP-TABLE exp-polist
    FIELD bestelldatum      LIKE l-orderhdr.bestelldatum 
    FIELD firma             LIKE l-lieferant.firma 
    FIELD docu-nr           LIKE l-orderhdr.docu-nr
    FIELD lieferdatum       LIKE l-orderhdr.lieferdatum 
    FIELD anzahl            LIKE l-order.anzahl 
    FIELD warenwert         LIKE l-order.warenwert 
    FIELD geliefert         LIKE l-order.geliefert 
    FIELD rechnungswert     LIKE l-order.rechnungswert 
    FIELD hlief-fax         LIKE l-orderhdr.lief-fax
    FIELD bestellart        LIKE l-orderhdr.bestellart 
    FIELD gedruckt          LIKE l-orderhdr.gedruckt 
    FIELD besteller         LIKE l-orderhdr.besteller
    FIELD lief-fax          AS CHARACTER EXTENT 3 
    FIELD lieferdatum1      LIKE l-order.lieferdatum 
    FIELD lieferdatum-eff   LIKE l-order.lieferdatum-eff 
    .

DEFINE TEMP-TABLE exp-polist-items
    FIELD artnr             LIKE l-order.artnr
    FIELD bezeich           LIKE l-artikel.bezeich
    FIELD anzahl            LIKE l-order.anzahl
    FIELD einzelpreis       LIKE l-order.einzelpreis
    FIELD warenwert         LIKE l-order.warenwert
    FIELD docu-nr           LIKE l-order.docu-nr
    FIELD lief-fax          LIKE l-order.lief-fax
    FIELD geliefert         LIKE l-order.geliefert
    FIELD rechnungspreis    LIKE l-order.rechnungspreis
    FIELD txtnr             LIKE l-order.txtnr
    FIELD lieferdatum-eff   LIKE l-order.lieferdatum-eff 
    FIELD angebot-lief	    LIKE l-order.angebot-lief
    FIELD masseinheit       LIKE l-artikel.masseinheit
    FIELD jahrgang          LIKE l-artikel.jahrgang
    FIELD quality           LIKE l-order.quality
    FIELD pos               LIKE l-order.pos
    FIELD remark            LIKE l-order.besteller
.

DEFINE INPUT PARAMETER from-date    AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER to-date      AS DATE     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR exp-polist.
DEFINE OUTPUT PARAMETER TABLE FOR exp-polist-items.

/******************************************************************************/ 
DEFINE BUFFER l-order1 FOR l-order. 
/* DEFINE BUFFER l-order2 FOR l-order. */ 
DEFINE BUFFER l-art    FOR l-artikel.

DEFINE VARIABLE billdate    AS DATE NO-UNDO.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate.                   

/* FOR EACH l-orderhdr WHERE l-orderhdr.bestelldatum GE from-date 
AND l-orderhdr.bestelldatum LE to-date 
AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK, 
FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr 
AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 
AND l-order2.geliefert LT l-order2.anzahl NO-LOCK 
BY l-orderhdr.bestelldatum BY l-lieferant.firma BY l-orderhdr.docu-nr: */
FOR EACH l-orderhdr WHERE l-orderhdr.bestelldatum GE from-date 
AND l-orderhdr.bestelldatum LE to-date 
AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
AND l-order1.loeschflag = 0 AND l-order1.pos GE 0
AND l-order1.geliefert LT l-order1.anzahl NO-LOCK
BY l-orderhdr.bestelldatum BY l-lieferant.firma BY l-orderhdr.docu-nr:
    CREATE exp-polist.
    ASSIGN 
        exp-polist.bestelldatum      = l-orderhdr.bestelldatum
        exp-polist.firma             = l-lieferant.firma
        exp-polist.docu-nr           = l-orderhdr.docu-nr
        exp-polist.lieferdatum       = l-orderhdr.lieferdatum
        exp-polist.anzahl            = l-order1.anzahl
        exp-polist.warenwert         = l-order1.warenwert
        exp-polist.geliefert         = l-order1.geliefert
        exp-polist.rechnungswert     = l-order1.rechnungswert
        exp-polist.hlief-fax[3]      = l-orderhdr.lief-fax[3]
        exp-polist.bestellart        = l-orderhdr.bestellart
        exp-polist.gedruckt          = l-orderhdr.gedruckt
        exp-polist.besteller         = l-orderhdr.besteller
        exp-polist.lief-fax[2]       = l-order1.lief-fax[2]
        exp-polist.lieferdatum1      = l-order1.lieferdatum
        exp-polist.lief-fax[3]       = l-order1.lief-fax[3]
        exp-polist.lieferdatum-eff   = l-order1.lieferdatum-eff.

    FOR EACH l-order WHERE l-order.docu-nr EQ l-orderhdr.docu-nr NO-LOCK,
    FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK:
        CREATE exp-polist-items.
        ASSIGN
            exp-polist-items.docu-nr         = l-order.docu-nr
            exp-polist-items.artnr           = l-order.artnr
            exp-polist-items.bezeich         = l-art.bezeich
            exp-polist-items.anzahl          = l-order.anzahl
            exp-polist-items.einzelpreis     = l-order.einzelpreis
            exp-polist-items.warenwert       = l-order.warenwert
            exp-polist-items.lief-fax        = l-order.lief-fax
            exp-polist-items.geliefert       = l-order.geliefert
            exp-polist-items.rechnungspreis  = l-order.rechnungspreis
            exp-polist-items.txtnr           = l-order.txtnr
            exp-polist-items.lieferdatum-eff = l-order.lieferdatum-eff
            exp-polist-items.angebot-lief    = l-order.angebot-lief
            exp-polist-items.masseinheit     = l-art.masseinheit
            exp-polist-items.jahrgang        = l-art.jahrgang
            exp-polist-items.quality         = l-order.quality
            exp-polist-items.pos             = l-order.pos
            exp-polist-items.remark          = l-order.besteller
        .
    END.
END.
