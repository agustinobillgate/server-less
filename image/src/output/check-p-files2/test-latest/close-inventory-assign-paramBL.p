
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER inv-type AS INT.

IF inv-type = 1 THEN 
DO TRANSACTION: 
  FIND FIRST htparam WHERE htparam.paramnr = 224 EXCLUSIVE-LOCK. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS").
  FIND CURRENT htparam NO-LOCK. 
END.
ELSE IF inv-type = 2 THEN 
DO TRANSACTION: 
  FIND FIRST htparam WHERE htparam.paramnr = 221 EXCLUSIVE-LOCK. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 
END.
ELSE IF inv-type = 3 THEN 
DO TRANSACTION: 

  FIND FIRST htparam WHERE htparam.paramnr = 221 EXCLUSIVE-LOCK. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 

  FIND FIRST htparam WHERE htparam.paramnr = 224 EXCLUSIVE-LOCK. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 
END.
