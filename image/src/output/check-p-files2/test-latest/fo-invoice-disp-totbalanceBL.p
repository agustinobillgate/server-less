
DEF INPUT  PARAMETER bil-recid AS INT.
DEF OUTPUT PARAMETER tot-balance AS DECIMAL.

DEFINE BUFFER bill1 FOR bill.

tot-balance = 0. 
FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.

FOR EACH bill1 WHERE bill1.resnr = bill.resnr 
    AND bill1.parent-nr = bill.parent-nr AND bill1.flag = 0 
    AND bill1.zinr = bill.zinr NO-LOCK: 
    tot-balance = tot-balance + bill1.saldo. 
END.
