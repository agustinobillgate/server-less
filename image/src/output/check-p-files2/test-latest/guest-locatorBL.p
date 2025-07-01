DEFINE INPUT PARAMETER resno    AS INTEGER.
DEFINE INPUT PARAMETER reslino  AS INTEGER.
DEFINE INPUT PARAMETER curr-s  AS CHARACTER.


FIND FIRST res-line WHERE res-line.resnr = resno 
    AND res-line.reslinnr = reslino EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE res-line THEN res-line.voucher-nr = curr-s. 
