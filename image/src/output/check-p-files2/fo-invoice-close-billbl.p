
DEF INPUT-OUTPUT PARAMETER bil-recid AS INT.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER bill-date   AS DATE.

DEFINE VARIABLE bill-anzahl AS INTEGER INITIAL 0.
DEFINE VARIABLE curr-billnr AS INTEGER.
DEFINE VARIABLE max-anzahl AS INTEGER INITIAL 0.

DEFINE BUFFER bill1 FOR bill.

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.
bill-anzahl = 0.
curr-billnr = bill.billnr. 

FOR EACH bill1 WHERE bill1.resnr = bill.resnr 
    AND bill1.parent-nr = bill.parent-nr 
    AND bill1.parent-nr NE 0 
    AND bill1.flag = 0 AND bill1.zinr = bill.zinr NO-LOCK: 
    bill-anzahl = bill-anzahl + 1. 
END. 
IF bill-anzahl NE curr-billnr THEN 
DO: 
    FIND FIRST bill1 WHERE bill1.resnr = bill.resnr 
      AND bill1.parent-nr = bill.parent-nr AND bill1.billnr EQ bill-anzahl 
      AND bill1.flag = 0 AND bill1.zinr = bill.zinr EXCLUSIVE-LOCK. 
    bill1.billnr = curr-billnr. 
    FIND CURRENT bill1 NO-LOCK. 
END. 
max-anzahl = bill-anzahl + 1. 
IF max-anzahl LT 5 THEN max-anzahl = 5. 
FOR EACH bill1 WHERE bill1.resnr = bill.resnr 
    AND bill1.parent-nr = bill.parent-nr 
    AND bill1.parent-nr NE 0 
    AND bill1.flag = 1 AND bill1.zinr = bill.zinr NO-LOCK: 
    max-anzahl = max-anzahl + 1. 
END. 
FIND CURRENT bill EXCLUSIVE-LOCK. 
bill.billnr = max-anzahl. 
bill.flag = 1. 
bill.vesrcod = user-init. 
FIND CURRENT bill NO-LOCK. 
 
FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.reslinnr 
    AND res-line.zinr = bill.zinr EXCLUSIVE-LOCK. 
res-line.abreise = bill-date. 
res-line.abreisezeit = time. 
res-line.changed = TODAY. 
res-line.changed-id = user-init. 
res-line.active-flag = 2. 
FIND CURRENT res-line NO-LOCK. 
 
FIND FIRST bill1 WHERE bill1.resnr = bill.resnr 
    AND bill1.parent-nr = bill.parent-nr AND bill1.billnr = 1 
    AND bill1.flag = 0 AND bill1.zinr = bill.zinr NO-LOCK. 
bil-recid = RECID(bill1). 
