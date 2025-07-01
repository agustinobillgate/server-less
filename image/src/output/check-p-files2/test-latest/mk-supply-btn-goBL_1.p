DEFINE TEMP-TABLE t-l-lieferant     LIKE l-lieferant.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER lname        AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER zcode        AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-l-lieferant.   
DEFINE OUTPUT PARAMETER msg-str     AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER created     AS LOGICAL  NO-UNDO INIT NO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-supply". 

IF lname = "" THEN 
DO:
    msg-str = msg-str + translateExtended("Company Name not yet defined.", 
              lvCAREA, "") + CHR(2).
    RETURN.
END.
                                     
DEFINE BUFFER l-supp FOR l-lieferant.    

FIND FIRST l-supp WHERE l-supp.firma = lname NO-LOCK NO-ERROR. 
IF AVAILABLE l-supp THEN 
DO:
    msg-str = msg-str + translateExtended
              ("Other Supplier with the same company name exists.", 
              lvCAREA, "") + CHR(2).
    RETURN.
END.
    
IF zcode NE "" THEN 
DO: 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = zcode NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN 
    DO:
        msg-str = msg-str + translateExtended("Account Number not found.", 
                  lvCAREA, "") + CHR(2).
        RETURN.
    END.
END.
        
FIND FIRST t-l-lieferant EXCLUSIVE-LOCK NO-ERROR.
FIND FIRST counters WHERE counters.counter-no = 14 EXCLUSIVE-LOCK. 
counters.counter = counters.counter + 1. 
t-l-lieferant.lief-nr = counters.counter. 
FIND CURRENT counter NO-LOCK. 
FIND CURRENT t-l-lieferant NO-LOCK. 

CREATE l-lieferant.
BUFFER-COPY t-l-lieferant TO l-lieferant.
created = YES.                         

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN 
DO:
    CREATE res-history.
    ASSIGN 
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.aenderung   = "Create Supplier - Supplier No : " + STRING(t-l-lieferant.lief-nr)
        res-history.action      = "Create".
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.
