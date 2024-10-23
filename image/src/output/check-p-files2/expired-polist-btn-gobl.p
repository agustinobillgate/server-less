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

DEFINE INPUT PARAMETER from-date    AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER to-date      AS DATE     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR exp-polist.

/******************************************************************************/ 
DEFINE BUFFER l-order1 FOR l-order. 
DEFINE BUFFER l-order2 FOR l-order. 

DEFINE VARIABLE billdate    AS DATE NO-UNDO.
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate.                   

FOR EACH l-orderhdr WHERE l-orderhdr.bestelldatum GE from-date 
    AND l-orderhdr.bestelldatum LE to-date 
    AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
    FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
      AND l-order1.loeschflag = 0 AND l-order1.pos = 0 NO-LOCK, 
    FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr 
      AND l-order2.loeschflag = 0 AND l-order2.pos GT 0 
      AND l-order2.geliefert LT l-order2.anzahl NO-LOCK 
    BY l-orderhdr.bestelldatum BY l-lieferant.firma BY l-orderhdr.docu-nr.
    CREATE exp-polist.
    ASSIGN 
        exp-polist.bestelldatum      = l-orderhdr.bestelldatum
        exp-polist.firma             = l-lieferant.firma
        exp-polist.docu-nr           = l-orderhdr.docu-nr
        exp-polist.lieferdatum       = l-orderhdr.lieferdatum
        exp-polist.anzahl            = l-order2.anzahl
        exp-polist.warenwert         = l-order2.warenwert
        exp-polist.geliefert         = l-order2.geliefert
        exp-polist.rechnungswert     = l-order1.rechnungswert
        exp-polist.hlief-fax[3]      = l-orderhdr.lief-fax[3]
        exp-polist.bestellart        = l-orderhdr.bestellart
        exp-polist.gedruckt          = l-orderhdr.gedruckt
        exp-polist.besteller         = l-orderhdr.besteller
        exp-polist.lief-fax[2]       = l-order1.lief-fax[2]
        exp-polist.lieferdatum1      = l-order1.lieferdatum
        exp-polist.lief-fax[3]       = l-order1.lief-fax[3]
        exp-polist.lieferdatum-eff   = l-order1.lieferdatum-eff.
END.
