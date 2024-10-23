
DEF INPUT PARAMETER all-user    AS LOGICAL.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER ci-date     AS DATE.
DEF INPUT PARAMETER shift       AS INT.
DEF INPUT PARAMETER bediener-nr AS INT.

DEF BUFFER journal FOR billjournal. 

FOR EACH artikel WHERE (artikel.artart = 2 OR 
    artikel.artart = 6 OR artikel.artart = 7) 
    AND artikel.departement = 0 NO-LOCK: 
 
    IF NOT all-user THEN
    FOR EACH billjournal WHERE billjournal.userinit = user-init 
        AND billjournal.artnr = artikel.artnr AND billjournal.anzahl NE 0 
        AND billjournal.departement = artikel.departement 
        AND billjournal.bill-datum = ci-date AND billjournal.betriebsnr = 0 
        NO-LOCK: 
        DO TRANSACTION: 
          FIND FIRST journal WHERE RECID(journal) = RECID(billjournal) 
            EXCLUSIVE-LOCK. 
          journal.betriebsnr = shift. 
          FIND CURRENT journal NO-LOCK. 
          RELEASE journal. 
        END. 
    END. 
    ELSE     
    FOR EACH billjournal 
        WHERE billjournal.artnr = artikel.artnr AND billjournal.anzahl NE 0 
        AND billjournal.departement = artikel.departement 
        AND billjournal.bill-datum = ci-date AND billjournal.betriebsnr = 0 
        NO-LOCK: 
        DO TRANSACTION: 
          FIND FIRST journal WHERE RECID(journal) = RECID(billjournal) 
            EXCLUSIVE-LOCK. 
          journal.betriebsnr = shift. 
          FIND CURRENT journal NO-LOCK. 
          RELEASE journal. 
        END. 
    END.     
END.   /*for each artikel*/

IF all-user THEN
DO TRANSACTION:
    CREATE res-history.
    ASSIGN res-history.nr     = bediener-nr
        res-history.datum     = TODAY
        res-history.zeit      = TIME
        res-history.aenderung = "Close Shift(ALL)"
        res-history.action    = "FO Cashier".
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.
