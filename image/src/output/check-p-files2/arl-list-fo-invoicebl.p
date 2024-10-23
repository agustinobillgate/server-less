
DEF INPUT  PARAMETER recid-resline  AS INT.
DEF OUTPUT PARAMETER inp-rechnr     AS INTEGER INITIAL 0.

FIND FIRST res-line WHERE RECID(res-line) = recid-resline.
FIND FIRST bill WHERE bill.resnr = res-line.resnr
  AND bill.reslinnr = res-line.reslinnr
  AND bill.zinr = res-line.zinr 
  AND bill.flag = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE bill THEN inp-rechnr = bill.rechnr. 
