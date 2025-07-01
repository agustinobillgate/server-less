
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.


RUN del-old-ap.

PROCEDURE del-old-ap: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
DEFINE BUFFER debt1 FOR l-kredit. 
DEFINE BUFFER debt2 FOR l-kredit.
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE total-saldo AS DECIMAL.

    FIND FIRST htparam WHERE paramnr = 1085 NO-LOCK. 
    anz = htparam.finteger. 
    IF anz = 0 THEN 
    DO: 
      FIND FIRST htparam WHERE paramnr = 163 NO-LOCK. 
      anz = htparam.finteger. 
    END. 
    IF anz = 0 THEN anz = 90. 
    
    FIND FIRST l-kredit WHERE l-kredit.opart EQ 2 
        AND l-kredit.zahlkonto GT 0 
        AND (l-kredit.rgdatum + anz) LE (ci-date + 1) NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE l-kredit: 
        i = i + 1. 
        /*FDL Sept 10, 2024: F26504*/
        total-saldo = 0.       
        FOR EACH debt1 WHERE debt1.counter EQ l-kredit.counter
            AND debt1.lscheinnr EQ l-kredit.lscheinnr NO-LOCK:

            total-saldo = total-saldo + debt1.saldo.                
        END.  
        IF total-saldo EQ 0 THEN /*Balance*/
        DO:
            FOR EACH debt2 WHERE debt2.counter EQ l-kredit.counter
                AND debt2.lscheinnr EQ l-kredit.lscheinnr EXCLUSIVE-LOCK: 
                DELETE debt2. 
            END. 
        END.      
        /* FDL Comment: F26504
        FOR EACH debt1 WHERE debt1.counter = l-kredit.counter
            AND debt1.lscheinnr = l-kredit.lscheinnr EXCLUSIVE-LOCK: 
            DELETE debt1. 
        END. 
        */
        /*FIND FIRST debt1 WHERE debt1.counter = l-kredit.counter 
          AND debt1.zahlkonto GT 0 AND RECID(debt1) NE RECID(l-kredit) 
          AND (debt1.rgdatum + anz) GE ci-date NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE debt1 THEN 
        DO TRANSACTION: 
          i = i + 1.       
          FOR EACH debt1 WHERE debt1.counter = l-kredit.counter
              AND debt1.lscheinnr = l-kredit.lscheinnr EXCLUSIVE-LOCK: 
            DELETE debt1. 
          END. 
        END.*/ 
        FIND NEXT l-kredit WHERE l-kredit.opart EQ 2 
            AND l-kredit.zahlkonto GT 0 
            AND (l-kredit.rgdatum + anz) LE (ci-date + 1) NO-LOCK NO-ERROR. 
    END. 
    /* FDL Comment move to find first do while above: F26504
    FIND FIRST l-kredit WHERE l-kredit.opart = 2 
      AND l-kredit.zahlkonto = 0 
      AND (l-kredit.rgdatum + anz) LT ci-date NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE l-kredit: 
          i = i + 1. 
         FOR EACH debt1 WHERE debt1.counter = l-kredit.counter
            AND debt1.lscheinnr = l-kredit.lscheinnr EXCLUSIVE-LOCK: 
            DELETE debt1. 
        END. 
    
      /*FIND FIRST debt1 WHERE debt1.counter = l-kredit.counter 
        AND debt1.zahlkonto GT 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE debt1 THEN 
      DO TRANSACTION: 
        FIND FIRST debt1 WHERE RECID(debt1) = RECID(l-kredit)
          EXCLUSIVE-LOCK. 
        DELETE debt1. 
        RELEASE debt1. 
      END.*/
    
      FIND NEXT l-kredit WHERE l-kredit.opart = 2 
        AND l-kredit.zahlkonto = 0 
        AND (l-kredit.rgdatum + anz) LT ci-date NO-LOCK NO-ERROR. 
    END. 
    */
END. 

