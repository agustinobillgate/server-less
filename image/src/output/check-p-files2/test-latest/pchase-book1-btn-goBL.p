DEFINE TEMP-TABLE pchase-list
    FIELD bestelldatum  LIKE l-pprice.bestelldatum 
    FIELD firma         LIKE l-lieferant.firma 
    FIELD docu-nr       LIKE l-pprice.docu-nr 
    FIELD traubensort   LIKE l-artikel.traubensort 
    FIELD lief-einheit  LIKE l-artikel.lief-einheit 
    FIELD betriebsnr    LIKE l-pprice.betriebsnr 
    FIELD anzahl        LIKE l-pprice.anzahl 
    FIELD einzelpreis   LIKE l-pprice.einzelpreis 
    FIELD warenwert     LIKE l-pprice.warenwert.

DEFINE INPUT PARAMETER s-artnr      AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR pchase-list.

FOR EACH l-pprice WHERE l-pprice.artnr = s-artnr NO-LOCK, 
    FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK :
    CREATE pchase-list.
    ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
           pchase-list.firma         = l-lieferant.firma 
           pchase-list.docu-nr       = l-pprice.docu-nr 
           pchase-list.traubensort   = l-artikel.traubensort 
           pchase-list.lief-einheit  = l-artikel.lief-einheit 
           pchase-list.betriebsnr    = l-pprice.betriebsnr 
           pchase-list.anzahl        = l-pprice.anzahl 
           pchase-list.einzelpreis   = l-pprice.einzelpreis 
           pchase-list.warenwert     = l-pprice.warenwert.
END.
