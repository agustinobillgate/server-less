DEFINE TEMP-TABLE supplier
    FIELD supplier-name AS CHAR
    FIELD lief-nr       AS CHAR
    FIELD supplierid    AS CHAR
.

DEFINE INPUT PARAMETER TABLE FOR supplier.

FOR EACH supplier NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY = 256
        AND queasy.char1 = supplier.supplier-name NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY   = 256
            queasy.char1 = supplier.supplier-name 
            queasy.char2 = supplier.lief-nr       
            queasy.char3 = supplier.supplierid   
        .
    END.
    ELSE DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN 
            queasy.char1 = supplier.supplier-name 
            queasy.char2 = supplier.lief-nr       
            queasy.char3 = supplier.supplierid   
        .
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.       
    END.
END.
