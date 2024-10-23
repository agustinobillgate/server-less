
DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER shift     AS INTEGER.

DEF BUFFER journal FOR billjournal. 

FOR EACH artikel WHERE (artikel.artart = 2 OR 
    artikel.artart = 6 OR artikel.artart = 7) 
    AND artikel.departement = 0 NO-LOCK: 
 
    FOR EACH billjournal WHERE billjournal.userinit = user-init 
      AND billjournal.artnr = artikel.artnr AND billjournal.anzahl NE 0 
      AND billjournal.departement = artikel.departement 
      AND billjournal.bill-datum = from-date AND billjournal.betriebsnr = 0 
      NO-LOCK: 
      DO TRANSACTION: 
        FIND FIRST journal WHERE RECID(journal) = RECID(billjournal) 
          EXCLUSIVE-LOCK. 
        journal.betriebsnr = shift. 
        FIND CURRENT journal NO-LOCK. 
        RELEASE journal. 
      END. 
    END. 
END. 
