
DEF INPUT  PARAMETER arl-list-resnr AS INT.
DEF OUTPUT PARAMETER avail-resline  AS LOGICAL INIT NO.
DEFINE buffer resline FOR res-line.

FIND FIRST resline WHERE resline.resnr = arl-list-resnr
    AND resline.active-flag = 1 
    AND (resline.resstatus EQ 6 OR resline.resstatus EQ 13) 
    NO-LOCK NO-ERROR. 
IF AVAILABLE resline THEN 
DO: 
    avail-resline = YES.
    RETURN. 
END. 
