 
/* Delete  SUPPLIER */ 
 
DEFINE INPUT PARAMETER lief-nr AS INTEGER. 
DEFINE INPUT PARAMETER user-init   AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER error-code AS INTEGER INITIAL 0. 
 
FIND FIRST l-orderhdr WHERE l-orderhdr.lief-nr = lief-nr NO-LOCK NO-ERROR. 
IF AVAILABLE l-orderhdr THEN 
DO: 
  error-code = 1. 
  RETURN. 
END. 
 
FIND FIRST l-kredit WHERE l-kredit.lief-nr = lief-nr AND l-kredit.zahlkonto = 0 
  NO-LOCK NO-ERROR. 
IF AVAILABLE l-kredit THEN 
DO: 
  error-code = 2. 
  RETURN. 
END. 
 
FIND FIRST l-op WHERE l-op.lief-nr = lief-nr AND l-op.op-art = 1 
  NO-LOCK NO-ERROR. 
IF AVAILABLE l-op THEN 
DO: 
  error-code = 3. 
  RETURN. 
END. 
 
IF error-code = 0 THEN 
DO: 
  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-lieferant THEN /*FT serverless*/
  DO:
    delete l-lieferant. 
    RELEASE l-lieferant.
  END.                  
END. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN 
DO:
    CREATE res-history.
    ASSIGN 
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.aenderung   = "Delete Supplier - Supplier No : " + STRING(lief-nr)
        res-history.action      = "Delete".
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.
