
DEFINE INPUT PARAMETER bk-veran-recid AS INT.
DEFINE INPUT PARAMETER fsl-limit-date AS DATE.


FIND FIRST bk-veran WHERE RECID(bk-veran) = bk-veran-recid NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN       
DO TRANSACTION:
  FIND CURRENT bk-veran EXCLUSIVE-LOCK.  
  ASSIGN bk-veran.limit-date = fsl-limit-date.  
  FIND CURRENT bk-veran NO-LOCK. 
END.
