
DEF INPUT  PARAMETER inp-rechnr AS INT.
DEF OUTPUT PARAMETER room       AS CHAR.
DEF OUTPUT PARAMETER gname      AS CHAR.
DEF OUTPUT PARAMETER bill-recid AS INT INIT 0.

DEF BUFFER rline FOR res-line. 
FIND FIRST bill WHERE bill.rechnr = inp-rechnr NO-LOCK. 
bill-recid = RECID(bill).
FIND FIRST rline WHERE rline.resnr = bill.resnr 
    AND rline.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
room = bill.zinr. 
IF AVAILABLE rline THEN gname = rline.name. 
