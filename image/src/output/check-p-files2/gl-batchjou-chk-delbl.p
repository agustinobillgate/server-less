
DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER jnr AS INT.
DEF INPUT  PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR INIT "".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-batchjou-chk-del". 

FIND FIRST gl-journal WHERE gl-journal.jnr = jnr NO-LOCK NO-ERROR. 
IF AVAILABLE gl-journal THEN 
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Journal entries exist, deleting not possible",lvCAREA,"").
  RETURN NO-APPLY. 
END. 
IF NOT AVAILABLE gl-journal THEN 
DO:
  FIND FIRST gl-jouhdr WHERE RECID(gl-jouhd) = rec-id EXCLUSIVE-LOCK. 
  delete gl-jouhdr.
END.
