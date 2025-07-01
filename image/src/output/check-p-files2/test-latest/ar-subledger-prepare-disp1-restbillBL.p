
DEF TEMP-TABLE t-h-journal LIKE h-journal.

DEFINE BUFFER bline             FOR blinehis.

DEF INPUT PARAMETER s-recid AS INT.
DEF OUTPUT PARAMETER billno AS INTEGER NO-UNDO. 
DEF OUTPUT PARAMETER TABLE FOR t-h-journal.

DEFINE VARIABLE i               AS INTEGER NO-UNDO. 

FIND FIRST bline WHERE RECID(bline) = s-recid NO-LOCK.
DO i = 1 TO LENGTH(bline.bezeich): 
    IF SUBSTR(bline.bezeich, i, 1) = "*" THEN 
    DO: 
        billno = INTEGER(SUBSTR(bline.bezeich, i + 1, 
           LENGTH(bline.bezeich))). 
        i = 999. 
    END. 
END.

FOR EACH h-journal WHERE h-journal.rechnr 
    = billno AND h-journal.departement = bline.departement 
    AND h-journal.bill-datum = bline.bill-datum NO-LOCK :
    CREATE t-h-journal.
    BUFFER-COPY h-journal TO t-h-journal.
END.
    
