DEFINE TEMP-TABLE ponumber-list
    FIELD docu-nr       LIKE l-orderhdr.docu-nr 
    FIELD bestelldatum  LIKE l-orderhdr.bestelldatum 
    FIELD lieferdatum   LIKE l-orderhdr.lieferdatum 
    FIELD lief-fax      LIKE l-order.lief-fax
    .

DEFINE INPUT PARAMETER  lief-nr     AS INTEGER.
DEFINE INPUT PARAMETER  currNo      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR ponumber-list.
        
FOR EACH l-orderhdr WHERE l-orderhdr.lief-nr  = lief-nr 
    AND (l-orderhdr.angebot-lief[3] = currNo OR l-orderhdr.angebot-lief[3] = 0) /*M 040612 -> to read the selected currency */
    AND l-orderhdr.gedruckt = ? NO-LOCK, 
    FIRST l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
    AND l-order.loeschflag = 0 AND l-order.pos = 0
    AND (l-order.angebot-lief[3] = currNo OR l-order.angebot-lief[3] = 0) /*M 040612 -> to read the selected currency */
    NO-LOCK BY l-orderhdr.docu-nr:
    CREATE ponumber-list.
    ASSIGN  ponumber-list.docu-nr       = l-orderhdr.docu-nr 
            ponumber-list.bestelldatum  = l-orderhdr.bestelldatum 
            ponumber-list.lieferdatum   = l-orderhdr.lieferdatum 
            ponumber-list.lief-fax[1]   = l-order.lief-fax[1] 
            .
END.

 
