DEFINE TEMP-TABLE t-h-artikel  LIKE h-artikel  
    FIELD rec-id AS INT.  

DEFINE INPUT  PARAMETER curr-dept    AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER cash-foreign AS LOGICAL NO-UNDO.
DEFINE INPUT  PARAMETER pay-voucher  AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER cash-artnr   AS INTEGER NO-UNDO.

DEFINE VARIABLE p-854  AS INTEGER NO-UNDO.  
DEFINE VARIABLE p-855  AS INTEGER NO-UNDO.  
DEFINE VARIABLE p-1001 AS INTEGER NO-UNDO.  

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 854 NO-LOCK.
p-854 = vhp.htparam.finteger.
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK.
p-855 = vhp.htparam.finteger.
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 1001 NO-LOCK.
p-1001 = vhp.htparam.finteger.

IF cash-foreign THEN cash-artnr = p-854.  
ELSE 
DO:   
  IF NOT pay-voucher THEN cash-artnr = p-855.  
  ELSE cash-artnr = p-1001.  
END.   
