DEFINE TEMP-TABLE disc-list 
  FIELD l-recid     AS INTEGER 
  FIELD price0      AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Unit-Price" 
  FIELD brutto      AS DECIMAL FORMAT "->,>>>,>>>,>>9.999"  LABEL "Gross Amount" 
  FIELD disc        AS DECIMAL FORMAT ">9.99"               LABEL "Disc" 
  FIELD disc2       AS DECIMAL FORMAT ">9.99"               LABEL "Disc2" 
  FIELD vat         AS DECIMAL FORMAT ">9.99"               LABEL "VAT"
  FIELD disc-val    AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc Value" 
  FIELD disc2-val   AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc2 Value"
  FIELD vat-val     AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "VAT-Value". 


DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id        AS INT
    FIELD a-bezeich     AS CHARACTER
    FIELD lief-einheit  AS CHARACTER.

DEFINE INPUT-OUTPUT PARAMETER t-amount     AS DECIMAL.
DEFINE INPUT  PARAMETER TABLE FOR t-l-order.
DEFINE INPUT  PARAMETER TABLE FOR disc-list.

DEFINE OUTPUT PARAMETER t-l-order-quality      AS CHARACTER. 
DEFINE OUTPUT PARAMETER t-l-order-einzelpreis  AS DECIMAL. 
DEFINE OUTPUT PARAMETER t-l-order-warenwert    AS DECIMAL.
DEFINE OUTPUT PARAMETER disc-list-brutto       AS DECIMAL.

DEFINE VARIABLE amt AS DECIMAL. 
DEFINE buffer l-art1 FOR l-artikel. 

FIND FIRST l-order WHERE RECID(l-order) = t-l-order.rec-id.
DO transaction: 
    FIND CURRENT l-order EXCLUSIVE-LOCK.
     l-order.quality = STRING(disc-list.disc, "99.99 ") 
                     + STRING(disc-list.vat, "99.99") + STRING(disc-list.disc2, " 99.99")
                     + STRING(disc-list.disc-val, " >,>>>,>>>,>>9.999") + STRING(disc-list.disc2-val, " >,>>>,>>>,>>9.999")
                     + STRING(disc-list.vat-val, " >,>>>,>>>,>>9.999") . 
     amt = l-order.warenwert. 

     FIND FIRST l-art1 WHERE l-art1.artnr = l-order.artnr NO-LOCK. 
     disc-list-brutto       = disc-list.price0 * t-l-order.anzahl.                                                                                     
     l-order.warenwert      = (disc-list-brutto - disc-list.disc-val - disc-list.disc2-val + disc-list.vat-val).                            
     l-order.einzelpreis    = l-order.warenwert / l-order.anzahl.

     IF NOT l-order.flag THEN l-order.warenwert = l-order.warenwert * l-art1.lief-einheit. 
     t-amount               = t-amount - amt + l-order.warenwert. 
     t-l-order-quality      = l-order.quality.           
     t-l-order-einzelpreis  = l-order.einzelpreis.   
     t-l-order-warenwert    = l-order.warenwert.       
     FIND CURRENT l-order NO-LOCK.                  
END.          
