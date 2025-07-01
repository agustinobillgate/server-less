DEF INPUT PARAMETER htparam-recid AS INT.
DO TRANSACTION:
  FIND FIRST htparam WHERE RECID(htparam) = htparam-recid EXCLUSIVE-LOCK.
  htparam.flogical = NO.
END. 
