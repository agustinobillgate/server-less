
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

RUN del-old-outlet-umsatz.

PROCEDURE del-old-outlet-umsatz: 
DEFINE VARIABLE billdate AS DATE. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  billdate = htparam.fdate. 
  /*MTmess-str = translateExtended ("Deleted old outlet turnover records",lvCAREA,"") 
      + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FOR EACH hoteldpt NO-LOCK: 
    FOR EACH artikel WHERE artikel.departement = hoteldpt.num 
      AND artikel.artart = 1 AND artikel.activeflag = YES NO-LOCK: 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
        AND umsatz.departement = artikel.departement 
        AND umsatz.datum LE (billdate - 14) NO-LOCK NO-ERROR. 
      DO WHILE AVAILABLE umsatz: 
        DO TRANSACTION: 
          i = i + 1. 
          /*MTmess-str = translateExtended ("Deleted old outlet turnover records",lvCAREA,"") 
              + " " + STRING(i). 
          DISP mess-str WITH FRAME frame1. */
          FIND CURRENT umsatz EXCLUSIVE-LOCK. 
          delete umsatz. 
        END. 
        FIND NEXT umsatz WHERE umsatz.artnr = artikel.artnr 
          AND umsatz.departement = artikel.departement 
          AND umsatz.datum LE (billdate - 14) NO-LOCK NO-ERROR. 
      END. 
    END. 
  END. 
END.
