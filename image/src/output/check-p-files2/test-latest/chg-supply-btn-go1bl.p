DEFINE TEMP-TABLE t-l-lieferant     LIKE l-lieferant.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER lname        AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER zcode        AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER supply-recid AS INT      NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-l-lieferant.   
DEFINE OUTPUT PARAMETER msg-str     AS CHAR     NO-UNDO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "chg-supply". 

IF lname = "" THEN 
DO:
    msg-str = msg-str + translateExtended("Company Name not yet defined.", 
              lvCAREA, "") + CHR(2).
    RETURN.
END.
                                     
DEFINE BUFFER l-supp FOR l-lieferant.    

FIND FIRST l-supp WHERE l-supp.firma = lname 
    AND RECID(l-supp) NE supply-recid NO-LOCK NO-ERROR. 
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
        
FIND FIRST t-l-lieferant NO-LOCK.
FIND FIRST l-lieferant WHERE RECID(l-lieferant) = supply-recid EXCLUSIVE-LOCK.
IF AVAILABLE l-lieferant THEN BUFFER-COPY t-l-lieferant TO l-lieferant.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN 
DO:
    CREATE res-history.
    ASSIGN 
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.aenderung   = "Modify Supplier - Supplier No : " + STRING(t-l-lieferant.lief-nr)
        res-history.action      = "Modify".
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.

