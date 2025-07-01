DEF INPUT PARAMETER depart          AS INT.
DEF INPUT PARAMETER artnr           AS INT.
DEF INPUT PARAMETER datum           AS DATE.
DEF INPUT PARAMETER service-code    AS INT.
DEF INPUT PARAMETER mwst-code       AS INT.
DEF OUTPUT PARAMETER serv-htp       AS DECIMAL INITIAL 0.
DEF OUTPUT PARAMETER vat-htp        AS DECIMAL INITIAL 0.

DEF VAR serv-vat AS LOGICAL INITIAL NO NO-UNDO.
DEF VAR vat      AS DECIMAL         NO-UNDO.
DEF VAR service  AS DECIMAL         NO-UNDO.


/*
DEF VAR depart AS INT INITIAL 0.
DEF VAR art2 AS INT.
DEF VAR artnr AS INT INITIAL 110.
DEF VAR from-date AS DATE INITIAL 05/01/08.
DEF VAR to-date AS DATE INITIAL 05/01/09.
DEF VAR serv-htp    AS DEC.
DEF VAR vat-htp     AS DEC.*/

   
FIND FIRST kontplan NO-LOCK WHERE kontplan.betriebsnr = depart 
    AND kontplan.kontignr = artnr AND kontplan.datum = datum  NO-ERROR.
IF AVAILABLE kontplan THEN
DO:
    IF kontplan.anzkont GE 10000000 THEN
    ASSIGN  serv-htp    = kontplan.anzkont / 10000000
            vat-htp     = kontplan.anzconf / 10000000
    .    
    ELSE
    ASSIGN  serv-htp    = kontplan.anzkont / 10000
            vat-htp     = kontplan.anzconf / 10000
    .    
END.
ELSE 
DO:
    IF service-code NE 0 THEN 
       DO: 
         FIND FIRST htparam WHERE htparam.paramnr = service-code NO-LOCK. 
         IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN
         DO:
            serv-htp = htparam.fdecimal / 100. 
            FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
            serv-vat = htparam.flogical. 
         END.
       END.  
       IF mwst-code NE 0 THEN 
       DO: 
          FIND FIRST htparam WHERE htparam.paramnr = mwst-code NO-LOCK. 
          IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
            vat-htp = htparam.fdecimal / 100. 
/* SY 07/08/2013 */
          IF vat-htp = 1 THEN serv-htp = 0.
          ELSE
          IF serv-vat THEN vat-htp = vat-htp + vat-htp * serv-htp. 
       END.     
END.                                            
