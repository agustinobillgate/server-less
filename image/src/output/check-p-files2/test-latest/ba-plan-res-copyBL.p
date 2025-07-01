
DEF INPUT  PARAMETER t-resnr                AS INT.
DEF INPUT  PARAMETER t-reslinnr             AS INT.
DEF OUTPUT PARAMETER resline-veran-nr       AS INT INIT 0.
DEF OUTPUT PARAMETER resline-veran-resnr    AS INT INIT 0.
DEF OUTPUT PARAMETER avail-resline          AS LOGICAL INIT NO.

DEFINE BUFFER resline FOR bk-reser.

FIND FIRST resline WHERE resline.veran-nr = t-resnr
    AND resline.veran-resnr = t-reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE resline THEN 
DO: 
    ASSIGN
        resline-veran-nr    = resline.veran-nr
        resline-veran-resnr = resline.veran-resnr
        avail-resline       = YES.
END. 
