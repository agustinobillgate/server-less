
DEF INPUT PARAMETER res-recid AS INT.

DEF OUTPUT PARAMETER res-gatsnr AS INT.
DEF OUTPUT PARAMETER res-resnr AS INT.
DEF OUTPUT PARAMETER res-reslinnr AS INT.
DEF OUTPUT PARAMETER res-zipreis LIKE res-line.zipreis.

FIND FIRST res-line WHERE RECID(res-line) = res-recid NO-LOCK NO-ERROR. /* Malik Serverless : NO-LOCK -> NO-LOCK NO-ERROR */

/* Malik Serverless */
IF AVAILABLE res-line THEN
DO:
    res-gatsnr = res-line.gastnr.
    res-resnr = res-line.resnr.
    res-reslinnr = res-line.reslinnr.
    res-zipreis = res-line.zipreis.
END.
/* END Malik */

