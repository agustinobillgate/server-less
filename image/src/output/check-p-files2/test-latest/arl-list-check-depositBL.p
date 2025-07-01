
DEF INPUT  PARAMETER arl-list-resnr AS INT.
DEF OUTPUT PARAMETER anzahl         AS INTEGER INITIAL 0.

DEFINE BUFFER resline FOR res-line.

FIND FIRST resline WHERE resline.resnr = arl-list-resnr
    AND resline.active-flag = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE resline THEN RETURN.

FIND FIRST resline WHERE resline.resnr = arl-list-resnr
  AND resline.active-flag = 2 AND resline.resstatus = 8        
  NO-LOCK NO-ERROR. 
IF AVAILABLE resline THEN RETURN.

FOR EACH resline WHERE resline.resnr = arl-list-resnr
  AND resline.active-flag = 0 NO-LOCK: 
  anzahl = anzahl + 1. 
END.
