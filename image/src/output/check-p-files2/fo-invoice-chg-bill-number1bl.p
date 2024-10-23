
DEFINE BUFFER bill1 FOR bill. 

DEF INPUT-OUTPUT PARAMETER bil-recid      AS INT.
DEF INPUT  PARAMETER curr-billnr    AS INT.

FIND FIRST bill1 WHERE RECID(bill1) = bil-recid NO-LOCK. 

FIND FIRST bill WHERE bill.resnr = bill1.resnr 
  AND bill.parent-nr = bill1.parent-nr 
  AND bill.flag = 0 AND bill.zinr = bill1.zinr 
  AND bill.billnr = curr-billnr NO-LOCK NO-ERROR.

IF NOT AVAILABLE bill THEN
DO:
    FIND FIRST bill WHERE bill.resnr = bill1.resnr 
      AND bill.parent-nr = bill1.parent-nr 
      AND bill.flag = 0 
      AND bill.billnr = curr-billnr NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
        FIND FIRST res-line WHERE res-line.resnr = bill.resnr
            AND res-line.reslinnr = bill.parent-nr
            NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN bill.zinr = res-line.zinr.
        FIND CURRENT bill NO-LOCK.
    END.
END.

IF AVAILABLE bill THEN bil-recid = RECID(bill). 
