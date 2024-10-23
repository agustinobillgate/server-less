DEFINE TEMP-TABLE pchase-list
    FIELD bestelldatum  AS DATE     
    FIELD firma         AS CHAR     
    FIELD docu-nr       AS CHAR     
    FIELD traubensort   AS CHAR     
    FIELD lief-einheit  AS DECIMAL  
    FIELD betriebsnr    AS INTEGER  
    FIELD anzahl        AS INTEGER  
    FIELD einzelpreis   AS DECIMAL  
    FIELD warenwert     AS DECIMAL  
    FIELD remark        AS CHAR    
    FIELD artnr         AS INTEGER 
    FIELD bezeich       AS CHAR 
    .

DEFINE INPUT PARAMETER sorttype   AS INT.
DEFINE INPUT PARAMETER from-date  AS DATE. 
DEFINE INPUT PARAMETER to-date    AS DATE.
DEFINE INPUT PARAMETER mtd-date   AS DATE.
DEFINE INPUT PARAMETER mi-ch      AS CHAR.
DEFINE INPUT PARAMETER mi-all     AS LOGICAL.
DEFINE INPUT PARAMETER s-artnr    AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR pchase-list.


DEFINE BUFFER l-art FOR l-artikel.
DEFINE BUFFER l-ppr FOR l-pprice.
DEFINE BUFFER l-lief FOR l-lieferant.

DEFINE VARIABLE tmpart    AS INT.
DEFINE VARIABLE f-date    AS DATE.
DEFINE VARIABLE t-date    AS DATE.
DEFINE VARIABLE datum     AS DATE.
DEFINE VARIABLE lief-nr   AS INTEGER.
DEFINE VARIABLE artnr     AS INTEGER.
DEFINE VARIABLE t-qty     AS INTEGER.
DEFINE VARIABLE tot-qty   AS INTEGER.
DEFINE VARIABLE t-price   AS DECIMAL.
DEFINE VARIABLE tot-price AS DECIMAL.

IF mi-ch = "FTD" THEN
DO:
    ASSIGN  f-date = from-date
            t-date = to-date.
END.               
ELSE               
DO:                
    ASSIGN  f-date = DATE(1, 1, year(mtd-date))
            t-date = mtd-date.
END.

/*new concept add summary by MG 0BAF7A*/
IF NOT mi-all THEN
DO:
    t-qty   = 0.
    t-price = 0.
    tot-qty = 0.
    tot-price = 0.

    IF sorttype = 1 THEN
    DO:
      FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date 
          AND l-pprice.bestelldatum LE t-date 
          AND l-pprice.artnr = s-artnr NO-LOCK, 
          FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
          FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
          BY l-pprice.bestelldatum DESCENDING BY l-lieferant.firma BY l-art.bezeich BY l-pprice.einzelpreis:
          
          IF datum NE l-pprice.bestelldatum THEN
          DO:
             CREATE pchase-list.
             ASSIGN pchase-list.docu-nr   = "T O T A L"
                    pchase-list.anzahl    = t-qty
                    pchase-list.warenwert = t-price.
             t-qty   = 0.
             t-price = 0.
          END.
          datum = l-pprice.bestelldatum.
      
          CREATE pchase-list.
          ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                 pchase-list.firma         = l-lieferant.firma 
                 pchase-list.docu-nr       = l-pprice.docu-nr 
                 pchase-list.traubensort   = l-art.traubensort
                 pchase-list.lief-einheit  = l-art.lief-einheit
                 pchase-list.betriebsnr    = l-pprice.betriebsnr
                 pchase-list.anzahl        = l-pprice.anzahl 
                 pchase-list.einzelpreis   = l-pprice.einzelpreis
                 pchase-list.warenwert     = l-pprice.warenwert
                 pchase-list.artnr         = l-art.artnr
                 pchase-list.bezeich       = l-art.bezeich.
      
          t-qty     = t-qty + l-pprice.anzahl.
          t-price   = t-price + l-pprice.warenwert.
          tot-qty   = tot-qty + l-pprice.anzahl.
          tot-price = tot-price + l-pprice.warenwert.
      
      
          /*sis 220814*/
          FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
              AND l-order.lief-nr = l-pprice.lief-nr
              AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
          /*end sis*/
      END.  
    END.
    ELSE IF sorttype = 2 THEN
    DO:
      FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date 
          AND l-pprice.bestelldatum LE t-date 
          AND l-pprice.artnr = s-artnr NO-LOCK, 
          FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
          FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
          BY l-lieferant.firma BY l-pprice.bestelldatum DESCENDING BY l-art.bezeich BY l-pprice.einzelpreis:
          
          IF lief-nr NE l-pprice.lief-nr THEN
          DO:
             CREATE pchase-list.
             ASSIGN pchase-list.docu-nr   = "T O T A L"
                    pchase-list.anzahl    = t-qty
                    pchase-list.warenwert = t-price.
             t-qty   = 0.
             t-price = 0.
          END.
          lief-nr = l-pprice.lief-nr.
      
          CREATE pchase-list.
          ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                 pchase-list.firma         = l-lieferant.firma 
                 pchase-list.docu-nr       = l-pprice.docu-nr 
                 pchase-list.traubensort   = l-art.traubensort
                 pchase-list.lief-einheit  = l-art.lief-einheit
                 pchase-list.betriebsnr    = l-pprice.betriebsnr
                 pchase-list.anzahl        = l-pprice.anzahl 
                 pchase-list.einzelpreis   = l-pprice.einzelpreis
                 pchase-list.warenwert     = l-pprice.warenwert
                 pchase-list.artnr         = l-art.artnr
                 pchase-list.bezeich       = l-art.bezeich.
      
          t-qty     = t-qty + l-pprice.anzahl.
          t-price   = t-price + l-pprice.warenwert.
          tot-qty   = tot-qty + l-pprice.anzahl.
          tot-price = tot-price + l-pprice.warenwert.
      
      
          /*sis 220814*/
          FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
              AND l-order.lief-nr = l-pprice.lief-nr
              AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
          /*end sis*/
      END.  
    END.
    ELSE IF sorttype = 3 THEN
    DO:
      FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date 
          AND l-pprice.bestelldatum LE t-date 
          AND l-pprice.artnr = s-artnr NO-LOCK, 
          FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
          FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
          BY l-pprice.einzelpreis BY l-lieferant.firma BY l-pprice.bestelldatum DESCENDING BY l-art.bezeich :
          
          IF lief-nr NE l-pprice.lief-nr THEN
          DO:
             CREATE pchase-list.
             ASSIGN pchase-list.docu-nr   = "T O T A L"
                    pchase-list.anzahl    = t-qty
                    pchase-list.warenwert = t-price.
             t-qty   = 0.
             t-price = 0.
          END.
          lief-nr = l-pprice.lief-nr.
      
          CREATE pchase-list.
          ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                 pchase-list.firma         = l-lieferant.firma 
                 pchase-list.docu-nr       = l-pprice.docu-nr 
                 pchase-list.traubensort   = l-art.traubensort
                 pchase-list.lief-einheit  = l-art.lief-einheit
                 pchase-list.betriebsnr    = l-pprice.betriebsnr
                 pchase-list.anzahl        = l-pprice.anzahl 
                 pchase-list.einzelpreis   = l-pprice.einzelpreis
                 pchase-list.warenwert     = l-pprice.warenwert
                 pchase-list.artnr         = l-art.artnr
                 pchase-list.bezeich       = l-art.bezeich.
      
          t-qty     = t-qty + l-pprice.anzahl.
          t-price   = t-price + l-pprice.warenwert.
          tot-qty   = tot-qty + l-pprice.anzahl.
          tot-price = tot-price + l-pprice.warenwert.
      
      
          /*sis 220814*/
          FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
              AND l-order.lief-nr = l-pprice.lief-nr
              AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
          /*end sis*/
      END.  
    END.
    ELSE
    DO:
      FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date 
          AND l-pprice.bestelldatum LE t-date 
          AND l-pprice.artnr = s-artnr NO-LOCK, 
          FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
          FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
          BY l-art.bezeich BY l-lieferant.firma BY l-pprice.bestelldatum DESCENDING BY l-pprice.einzelpreis :
          
          IF artnr NE l-pprice.artnr THEN
          DO:
             CREATE pchase-list.
             ASSIGN pchase-list.docu-nr   = "T O T A L"
                    pchase-list.anzahl    = t-qty
                    pchase-list.warenwert = t-price.
             t-qty   = 0.
             t-price = 0.
          END.
          artnr = l-pprice.artnr.
      
          CREATE pchase-list.
          ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                 pchase-list.firma         = l-lieferant.firma 
                 pchase-list.docu-nr       = l-pprice.docu-nr 
                 pchase-list.traubensort   = l-art.traubensort
                 pchase-list.lief-einheit  = l-art.lief-einheit
                 pchase-list.betriebsnr    = l-pprice.betriebsnr
                 pchase-list.anzahl        = l-pprice.anzahl 
                 pchase-list.einzelpreis   = l-pprice.einzelpreis
                 pchase-list.warenwert     = l-pprice.warenwert
                 pchase-list.artnr         = l-art.artnr
                 pchase-list.bezeich       = l-art.bezeich.
      
          t-qty     = t-qty + l-pprice.anzahl.
          t-price   = t-price + l-pprice.warenwert.
          tot-qty   = tot-qty + l-pprice.anzahl.
          tot-price = tot-price + l-pprice.warenwert.
      
      
          /*sis 220814*/
          FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
              AND l-order.lief-nr = l-pprice.lief-nr
              AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
          /*end sis*/
      END. 
    END.

    CREATE pchase-list.
    ASSIGN pchase-list.docu-nr  = "T O T A L"
          pchase-list.anzahl    = t-qty
          pchase-list.warenwert = t-price.

    CREATE pchase-list.
    ASSIGN pchase-list.docu-nr  = "GRAND TOTAL"
          pchase-list.anzahl    = tot-qty
          pchase-list.warenwert = tot-price.
END.
ELSE 
DO:
   IF sorttype = 1 THEN
   DO:
     FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK,
         FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK,
         FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
         BY l-pprice.bestelldatum DESCENDING BY l-lieferant.firma BY l-art.bezeich BY l-pprice.einzelpreis :

         IF datum NE l-pprice.bestelldatum THEN
         DO:
            CREATE pchase-list.
            ASSIGN pchase-list.docu-nr   = "T O T A L"
                   pchase-list.anzahl    = t-qty
                   pchase-list.warenwert = t-price.
            t-qty   = 0.
            t-price = 0.
         END.
         datum = l-pprice.bestelldatum.
     
         CREATE pchase-list.
         ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                pchase-list.firma         = l-lieferant.firma
                pchase-list.docu-nr       = l-pprice.docu-nr 
                pchase-list.traubensort   = l-art.traubensort
                pchase-list.lief-einheit  = l-art.lief-einheit
                pchase-list.betriebsnr    = l-pprice.betriebsnr
                pchase-list.anzahl        = l-pprice.anzahl 
                pchase-list.einzelpreis   = l-pprice.einzelpreis
                pchase-list.warenwert     = l-pprice.warenwert
                pchase-list.artnr         = l-art.artnr
                pchase-list.bezeich       = l-art.bezeich
             .

         t-qty     = t-qty + l-pprice.anzahl.
         t-price   = t-price + l-pprice.warenwert.
         tot-qty   = tot-qty + l-pprice.anzahl.
         tot-price = tot-price + l-pprice.warenwert.
          
         /*sis 220814*/
         FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr 
             AND l-order.lief-nr = l-pprice.lief-nr 
             AND l-order.artnr = l-pprice.artnr NO-LOCK NO-ERROR.
         IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
         /*end sis*/
     END.
   END.
   ELSE IF sorttype = 2 THEN
   DO:
     FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK,
         FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK,
         FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
         BY l-lieferant.firma BY l-pprice.bestelldatum DESCENDING BY l-art.bezeich BY l-pprice.einzelpreis :

         IF lief-nr NE l-pprice.lief-nr THEN
         DO:
            CREATE pchase-list.
            ASSIGN pchase-list.docu-nr   = "T O T A L"
                   pchase-list.anzahl    = t-qty
                   pchase-list.warenwert = t-price.
            t-qty   = 0.
            t-price = 0.
         END.
         lief-nr = l-pprice.lief-nr.
     
         CREATE pchase-list.
         ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                pchase-list.firma         = l-lieferant.firma
                pchase-list.docu-nr       = l-pprice.docu-nr 
                pchase-list.traubensort   = l-art.traubensort
                pchase-list.lief-einheit  = l-art.lief-einheit
                pchase-list.betriebsnr    = l-pprice.betriebsnr
                pchase-list.anzahl        = l-pprice.anzahl 
                pchase-list.einzelpreis   = l-pprice.einzelpreis
                pchase-list.warenwert     = l-pprice.warenwert
                pchase-list.artnr         = l-art.artnr
                pchase-list.bezeich       = l-art.bezeich
             .

         t-qty     = t-qty + l-pprice.anzahl.
         t-price   = t-price + l-pprice.warenwert.
         tot-qty   = tot-qty + l-pprice.anzahl.
         tot-price = tot-price + l-pprice.warenwert.
          
         /*sis 220814*/
         FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr 
             AND l-order.lief-nr = l-pprice.lief-nr 
             AND l-order.artnr = l-pprice.artnr NO-LOCK NO-ERROR.
         IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
         /*end sis*/
     END.
   END.
   ELSE IF sorttype = 3 THEN
   DO:
     FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK,
         FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK,
         FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
         BY l-pprice.einzelpreis BY l-lieferant.firma BY l-pprice.bestelldatum DESCENDING BY l-art.bezeich :

         IF lief-nr NE l-pprice.lief-nr THEN
         DO:
            CREATE pchase-list.
            ASSIGN pchase-list.docu-nr   = "T O T A L"
                   pchase-list.anzahl    = t-qty
                   pchase-list.warenwert = t-price.
            t-qty   = 0.
            t-price = 0.
         END.
         lief-nr = l-pprice.lief-nr.
     
         CREATE pchase-list.
         ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                pchase-list.firma         = l-lieferant.firma
                pchase-list.docu-nr       = l-pprice.docu-nr 
                pchase-list.traubensort   = l-art.traubensort
                pchase-list.lief-einheit  = l-art.lief-einheit
                pchase-list.betriebsnr    = l-pprice.betriebsnr
                pchase-list.anzahl        = l-pprice.anzahl 
                pchase-list.einzelpreis   = l-pprice.einzelpreis
                pchase-list.warenwert     = l-pprice.warenwert
                pchase-list.artnr         = l-art.artnr
                pchase-list.bezeich       = l-art.bezeich
             .

         t-qty     = t-qty + l-pprice.anzahl.
         t-price   = t-price + l-pprice.warenwert.
         tot-qty   = tot-qty + l-pprice.anzahl.
         tot-price = tot-price + l-pprice.warenwert.
          
         /*sis 220814*/
         FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr 
             AND l-order.lief-nr = l-pprice.lief-nr 
             AND l-order.artnr = l-pprice.artnr NO-LOCK NO-ERROR.
         IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
         /*end sis*/
     END.
   END.
   ELSE
   DO:
     FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date 
          AND l-pprice.bestelldatum LE t-date  NO-LOCK, 
          FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
          FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
          BY l-art.bezeich BY l-lieferant.firma BY l-pprice.bestelldatum DESCENDING BY l-pprice.einzelpreis :
          
          IF artnr NE l-pprice.artnr THEN
          DO:
             CREATE pchase-list.
             ASSIGN pchase-list.docu-nr   = "T O T A L"
                    pchase-list.anzahl    = t-qty
                    pchase-list.warenwert = t-price.
             t-qty   = 0.
             t-price = 0.
          END.
          artnr = l-pprice.artnr.
      
          CREATE pchase-list.
          ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                 pchase-list.firma         = l-lieferant.firma 
                 pchase-list.docu-nr       = l-pprice.docu-nr 
                 pchase-list.traubensort   = l-art.traubensort
                 pchase-list.lief-einheit  = l-art.lief-einheit
                 pchase-list.betriebsnr    = l-pprice.betriebsnr
                 pchase-list.anzahl        = l-pprice.anzahl 
                 pchase-list.einzelpreis   = l-pprice.einzelpreis
                 pchase-list.warenwert     = l-pprice.warenwert
                 pchase-list.artnr         = l-art.artnr
                 pchase-list.bezeich       = l-art.bezeich.
      
          t-qty     = t-qty + l-pprice.anzahl.
          t-price   = t-price + l-pprice.warenwert.
          tot-qty   = tot-qty + l-pprice.anzahl.
          tot-price = tot-price + l-pprice.warenwert.
      
      
          /*sis 220814*/
          FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
              AND l-order.lief-nr = l-pprice.lief-nr
              AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
          /*end sis*/
      END. 
   END.
   CREATE pchase-list.
   ASSIGN pchase-list.docu-nr  = "T O T A L"
         pchase-list.anzahl    = t-qty
         pchase-list.warenwert = t-price.
   
   CREATE pchase-list.
   ASSIGN pchase-list.docu-nr  = "GRAND TOTAL"
         pchase-list.anzahl    = tot-qty
         pchase-list.warenwert = tot-price.
END.


/*IF NOT mi-all THEN
DO:
    FIND FIRST l-pprice WHERE l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date AND l-pprice.artnr = s-artnr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-pprice:
        FIND FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK NO-ERROR.
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK NO-ERROR. 

        CREATE pchase-list.
        ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
               pchase-list.firma         = l-lieferant.firma 
               pchase-list.docu-nr       = l-pprice.docu-nr 
               pchase-list.traubensort   = l-art.traubensort
               pchase-list.lief-einheit  = l-art.lief-einheit
               pchase-list.betriebsnr    = l-pprice.betriebsnr
               pchase-list.anzahl        = l-pprice.anzahl 
               pchase-list.einzelpreis   = l-pprice.einzelpreis
               pchase-list.warenwert     = l-pprice.warenwert
               pchase-list.artikel-name  = l-art.bezeich.

        FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
            AND l-order.lief-nr = l-pprice.lief-nr
            AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
        IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.

        FIND NEXT l-pprice WHERE l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date AND l-pprice.artnr = s-artnr NO-LOCK NO-ERROR.
    END.
END.
ELSE
DO:
    FIND FIRST l-artikel NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-artikel:
        FIND FIRST l-ppr WHERE l-ppr.artnr EQ l-artikel.artnr AND l-ppr.bestelldatum GE f-date AND l-ppr.bestelldatum LE t-date NO-LOCK NO-ERROR.
            IF tmpart NE l-artikel.artnr THEN
            DO:
                tmpart = l-artikel.artnr.
                CREATE pchase-list.
                ASSIGN 
                pchase-list.bestelldatum = ?
                pchase-list.firma = CAPS(l-artikel.bezeich).
            END.

            FIND FIRST l-pprice WHERE l-pprice.artnr = tmpart AND l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK NO-ERROR. 
            DO WHILE AVAILABLE l-pprice:
                FIND FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK NO-ERROR. 
                FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK NO-ERROR.

                CREATE pchase-list.
                ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                       pchase-list.firma         = l-lieferant.firma 
                       pchase-list.docu-nr       = l-pprice.docu-nr 
                       pchase-list.traubensort   = l-art.traubensort
                       pchase-list.lief-einheit  = l-art.lief-einheit
                       pchase-list.betriebsnr    = l-pprice.betriebsnr
                       pchase-list.anzahl        = l-pprice.anzahl 
                       pchase-list.einzelpreis   = l-pprice.einzelpreis
                       pchase-list.warenwert     = l-pprice.warenwert
                       pchase-list.artikel-name  = l-art.bezeich.
        
                FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
                    AND l-order.lief-nr = l-pprice.lief-nr
                    AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
                IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.

                FIND NEXT l-pprice WHERE l-pprice.artnr = tmpart AND l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK NO-ERROR. 
            END.
        FIND NEXT l-artikel NO-LOCK NO-ERROR.
    END.
END.*/

FOR EACH pchase-list :
    IF pchase-list.anzahl EQ 0 AND pchase-list.warenwert EQ 0 THEN DELETE pchase-list.
END.
