
DEF INPUT PARAMETER l-segmentcode AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST l-segment WHERE l-segment.l-segmentcode = l-segmentcode.
FIND FIRST l-lieferant WHERE l-lieferant.segment1 = l-segmentcode NO-LOCK NO-ERROR. 
IF AVAILABLE l-artikel THEN 
DO:
  flag = 1.
END. 
ELSE 
DO: 
    FIND CURRENT l-segment EXCLUSIVE-LOCK. 
    delete l-segment. 
END.
