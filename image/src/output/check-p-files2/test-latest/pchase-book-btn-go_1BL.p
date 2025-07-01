/* Modified by gerald 040320 [F03BD6] fromdate-todate */

DEFINE TEMP-TABLE pchase-list
    FIELD bestelldatum  LIKE l-pprice.bestelldatum 
    FIELD firma         LIKE l-lieferant.firma 
    FIELD docu-nr       LIKE l-pprice.docu-nr 
    FIELD traubensort   LIKE l-artikel.traubensort
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD betriebsnr    LIKE l-pprice.betriebsnr
    FIELD anzahl        LIKE l-pprice.anzahl 
    FIELD einzelpreis   LIKE l-pprice.einzelpreis
    FIELD warenwert     LIKE l-pprice.warenwert
    FIELD remark        LIKE l-order.besteller
    FIELD artnr         LIKE l-pprice.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    .

DEFINE INPUT PARAMETER sorttype     AS INT.
DEFINE INPUT PARAMETER f-date       AS DATE. 
DEFINE INPUT PARAMETER t-date       AS DATE.
DEFINE INPUT PARAMETER to-dt        AS DATE.
DEFINE INPUT PARAMETER mi-ch        AS CHAR.
DEFINE INPUT PARAMETER mi-call      AS CHAR.
DEFINE INPUT PARAMETER s-artnr      AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR pchase-list.

DEFINE BUFFER l-art FOR l-artikel.
DEFINE BUFFER l-ppr FOR l-pprice.
DEFINE BUFFER l-lief FOR l-lieferant.

DEFINE VARIABLE tmpart AS INT.
                       
IF mi-ch = 'ytd' THEN
    ASSIGN f-date      = DATE(1,1, YEAR(to-dt))
           t-date      = to-dt. 

/*
FOR EACH l-pprice WHERE l-pprice.artnr = s-artnr NO-LOCK, 
    FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
    BY l-pprice.bestelldatum descending BY l-pprice.einzelpreis. 
    CREATE pchase-list.
    ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
           pchase-list.firma         = l-lieferant.firma 
           pchase-list.docu-nr       = l-pprice.docu-nr 
           pchase-list.traubensort   = l-art.traubensort
           pchase-list.lief-einheit  = l-art.lief-einheit
           pchase-list.betriebsnr    = l-pprice.betriebsnr
           pchase-list.anzahl        = l-pprice.anzahl 
           pchase-list.einzelpreis   = l-pprice.einzelpreis
           pchase-list.warenwert     = l-pprice.warenwert.

    /*sis 220814*/
    FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
        AND l-order.lief-nr = l-pprice.lief-nr
        AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
    /*end sis*/
END.
*/

/*Modified by gerald 040320 Display All Fromdate-Todate*/
IF NOT mi-call = 'all' THEN
DO:
    FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date 
        AND l-pprice.bestelldatum LE t-date 
        AND l-pprice.artnr = s-artnr NO-LOCK, 
        FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
        BY l-pprice.bestelldatum DESCENDING BY l-pprice.einzelpreis:
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
    
        /*sis 220814*/
        FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr
            AND l-order.lief-nr = l-pprice.lief-nr
            AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
        IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
        /*end sis*/
    END.  
END.
ELSE IF mi-call = 'all' THEN
DO:
   IF s-artnr EQ 0 THEN
   DO:
     FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK,
         FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK,
         FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
         BY l-pprice.bestelldatum DESCENDING BY l-pprice.einzelpreis :
     
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
     FOR EACH l-pprice WHERE l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date
         AND l-pprice.artnr = s-artnr NO-LOCK,
         FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK,
         FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
         BY l-pprice.bestelldatum DESCENDING BY l-pprice.einzelpreis :
     
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
         
         /*sis 220814*/
         FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr 
             AND l-order.lief-nr = l-pprice.lief-nr 
             AND l-order.artnr = l-pprice.artnr NO-LOCK NO-ERROR.
         IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
         /*end sis*/
     END.
   END.
END.

/*gerald comment old concept*/
/*ELSE IF mi-call = 'all' THEN
DO:
   IF sorttype EQ 1 THEN
   DO:
      FOR EACH l-artikel NO-LOCK,
         l-ppr WHERE l-ppr.artnr EQ l-artikel.artnr AND l-ppr.bestelldatum GE f-date AND l-ppr.bestelldatum LE t-date NO-LOCK 
          BY l-ppr.bestelldatum DESCENDING BY l-artikel.bezeich: 
        
         IF tmpart NE l-artikel.artnr THEN
         DO:
            tmpart = l-artikel.artnr.
            CREATE pchase-list.
            ASSIGN 
            pchase-list.bestelldatum = ?
            pchase-list.firma = CAPS(l-artikel.bezeich)
            .
         END.
      
         FOR EACH l-pprice WHERE l-pprice.artnr = tmpart AND l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK, 
            FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
            BY l-pprice.bestelldatum DESCENDING BY l-lieferant.firma BY l-pprice.einzelpreis.
            
            CREATE pchase-list.
            ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                   pchase-list.firma         = l-lieferant.firma
                   pchase-list.docu-nr       = l-pprice.docu-nr 
                   pchase-list.traubensort   = l-art.traubensort
                   pchase-list.lief-einheit  = l-art.lief-einheit
                   pchase-list.betriebsnr    = l-pprice.betriebsnr
                   pchase-list.anzahl        = l-pprice.anzahl 
                   pchase-list.einzelpreis   = l-pprice.einzelpreis
                   pchase-list.warenwert     = l-pprice.warenwert.
            
            /*sis 220814*/
            FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr 
                AND l-order.lief-nr = l-pprice.lief-nr 
                AND l-order.artnr = l-pprice.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
            /*end sis*/
         END.
      END.
   END.

   IF sorttype = 2 THEN
   DO:
      FOR EACH l-artikel NO-LOCK,
         l-ppr WHERE l-ppr.artnr EQ l-artikel.artnr AND l-ppr.bestelldatum GE f-date AND l-ppr.bestelldatum LE t-date NO-LOCK 
          BY l-ppr.bestelldatum DESCENDING BY l-artikel.bezeich: 
        
         IF tmpart NE l-artikel.artnr THEN
         DO:
            tmpart = l-artikel.artnr.
            CREATE pchase-list.
            ASSIGN 
            pchase-list.bestelldatum = ?
            pchase-list.firma = CAPS(l-artikel.bezeich)
            .
         END.
      
         FOR EACH l-pprice WHERE l-pprice.artnr = tmpart AND l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK, 
            FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
            BY l-lieferant.firma BY l-pprice.bestelldatum DESCENDING BY l-pprice.einzelpreis.
            
            CREATE pchase-list.
            ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                   pchase-list.firma         = l-lieferant.firma
                   pchase-list.docu-nr       = l-pprice.docu-nr 
                   pchase-list.traubensort   = l-art.traubensort
                   pchase-list.lief-einheit  = l-art.lief-einheit
                   pchase-list.betriebsnr    = l-pprice.betriebsnr
                   pchase-list.anzahl        = l-pprice.anzahl 
                   pchase-list.einzelpreis   = l-pprice.einzelpreis
                   pchase-list.warenwert     = l-pprice.warenwert.
            
            /*sis 220814*/
            FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr 
                AND l-order.lief-nr = l-pprice.lief-nr 
                AND l-order.artnr = l-pprice.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
            /*end sis*/
         END.
      END.
   END.

   IF sorttype = 3 THEN
   DO:
      FOR EACH l-artikel NO-LOCK,
          l-ppr WHERE l-ppr.artnr EQ l-artikel.artnr AND l-ppr.bestelldatum GE f-date AND l-ppr.bestelldatum LE t-date NO-LOCK 
          BY l-ppr.bestelldatum DESCENDING BY l-artikel.bezeich: 
        
         IF tmpart NE l-artikel.artnr THEN
         DO:
            tmpart = l-artikel.artnr.
            CREATE pchase-list.
            ASSIGN 
            pchase-list.bestelldatum = ?
            pchase-list.firma = CAPS(l-artikel.bezeich)
            .
         END.
      
         FOR EACH l-pprice WHERE l-pprice.artnr = tmpart AND l-pprice.bestelldatum GE f-date AND l-pprice.bestelldatum LE t-date NO-LOCK , 
            FIRST l-art WHERE l-art.artnr = l-pprice.artnr NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
            BY l-pprice.einzelpreis BY l-pprice.bestelldatum DESCENDING BY l-lieferant.firma  .
            
            CREATE pchase-list.
            ASSIGN pchase-list.bestelldatum  = l-pprice.bestelldatum 
                   pchase-list.firma         = l-lieferant.firma
                   pchase-list.docu-nr       = l-pprice.docu-nr 
                   pchase-list.traubensort   = l-art.traubensort
                   pchase-list.lief-einheit  = l-art.lief-einheit
                   pchase-list.betriebsnr    = l-pprice.betriebsnr
                   pchase-list.anzahl        = l-pprice.anzahl 
                   pchase-list.einzelpreis   = l-pprice.einzelpreis
                   pchase-list.warenwert     = l-pprice.warenwert.
            
            /*sis 220814*/
            FIND FIRST l-order WHERE l-order.docu-nr = l-pprice.docu-nr 
                AND l-order.lief-nr = l-pprice.lief-nr 
                AND l-order.artnr = l-pprice.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-order THEN pchase-list.remark = l-order.besteller.
            /*end sis*/
         END.
      END.
   END.
END.*/

/*gerald DFFC07*/
FOR EACH pchase-list :
    IF  pchase-list.anzahl EQ 0 AND pchase-list.warenwert EQ 0 THEN DELETE pchase-list.
END.
