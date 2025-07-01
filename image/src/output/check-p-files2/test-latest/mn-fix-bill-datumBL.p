RUN fix-bill-datum.


PROCEDURE fix-bill-datum:
DEF VAR bill-date AS DATE.

  
   FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
   ASSIGN bill-date = htparam.fdate.

   FIND FIRST bill WHERE bill.rechnr GT 0 
       AND bill.datum GE (bill-date - 400) NO-LOCK NO-ERROR.
   DO WHILE AVAILABLE bill:
       FIND LAST bill-line WHERE bill-line.rechnr = bill.rechnr 
           USE-INDEX bildat_index NO-LOCK NO-ERROR.
       IF AVAILABLE bill-line THEN DO:
           IF bill.datum = ? OR bill-line.bill-datum GT bill.datum THEN DO:
               FIND CURRENT bill EXCLUSIVE-LOCK.
               ASSIGN bill.datum = bill-line.bill-datum.
               FIND CURRENT bill NO-LOCK.
           END.
       END.
       FIND NEXT bill WHERE bill.rechnr GT 0 
            AND bill.datum GE (bill-date - 400) NO-LOCK NO-ERROR.
   END.

END.
