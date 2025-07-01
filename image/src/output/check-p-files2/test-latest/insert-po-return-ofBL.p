
DEF INPUT  PARAMETER rec-id                 AS INT.
DEF INPUT  PARAMETER l-order-anzahl         LIKE l-order.anzahl.
DEF INPUT  PARAMETER l-order-einzelpreis    LIKE l-order.einzelpreis.
DEF INPUT  PARAMETER disc-list-disc         AS CHAR.
DEF INPUT  PARAMETER disc-list-disc2        AS CHAR.
DEF INPUT  PARAMETER disc-list-vat          AS DECIMAL.

DEF INPUT-OUTPUT PARAMETER t-amount         AS DECIMAL.

DEF OUTPUT PARAMETER amt                    AS DECIMAL.
DEF OUTPUT PARAMETER l-order-warenwert      LIKE l-order.warenwert.
DEF OUTPUT PARAMETER l-order-quality        LIKE l-order.quality.

DEFINE buffer l-art1 FOR l-artikel.
FIND FIRST l-order WHERE RECID(l-order) = rec-id.

DO transaction: 
    FIND CURRENT l-order EXCLUSIVE-LOCK. 
    l-order.anzahl = l-order-anzahl.
    IF l-order.flag THEN 
    DO: 
      amt = l-order.warenwert. 
      l-order.warenwert = DECIMAL(l-order-anzahl) * 
        DECIMAL(l-order-einzelpreis) 
        * (1 - DECIMAL(disc-list-disc) / 100) 
        * (1 - DECIMAL(disc-list-disc2) / 100) 
        * (1 + DECIMAL(disc-list-vat) / 100). 
      l-order.quality = STRING(DECIMAL(disc-list-disc),"99.99 ") 
        + STRING(DECIMAL(disc-list-vat),"99.99") 
        + STRING(DECIMAL(disc-list-disc)," 99.99"). 
      t-amount = t-amount - amt + l-order.warenwert. 
      l-order-warenwert = l-order.warenwert.
      l-order-quality = l-order.quality.
    END. 
    ELSE 
    DO: 
      amt = l-order.warenwert. 
      FIND FIRST l-art1 WHERE l-art1.artnr = l-order.artnr NO-LOCK. 
      l-order.warenwert = DECIMAL(l-order-anzahl) * 
        DECIMAL(l-order-einzelpreis) 
        * (1 - DECIMAL(disc-list-disc) / 100) 
        * (1 - DECIMAL(disc-list-disc2) / 100) 
        * (1 + DECIMAL(disc-list-vat) / 100) 
        * l-art1.lief-einheit. 
      l-order.quality = STRING(DECIMAL(disc-list-disc),"99.99 ") 
        + STRING(DECIMAL(disc-list-vat),"99.99") 
        + STRING(DECIMAL(disc-list-disc)," 99.99"). 
      t-amount = t-amount - amt + l-order.warenwert.
      l-order-warenwert = l-order.warenwert.
      l-order-quality = l-order.quality.
    END. 
    FIND CURRENT l-order NO-LOCK. 
END.
