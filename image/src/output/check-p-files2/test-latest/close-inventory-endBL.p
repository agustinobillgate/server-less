
DEF INPUT PARAMETER user-init AS CHAR.

DO TRANSACTION: 
  FIND FIRST htparam WHERE paramnr = 232 EXCLUSIVE-LOCK. 
  htparam.flogical = NO. 
  htparam.lupdate = TODAY. 
  htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 
END.
