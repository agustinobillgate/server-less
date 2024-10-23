DEF TEMP-TABLE t-l-segment
    FIELD l-segmentcode LIKE l-segment.l-segmentcode
    FIELD l-bezeich     LIKE l-segment.l-bezeich.

DEFINE TEMP-TABLE l-list LIKE l-segment. 

DEF INPUT PARAMETER TABLE FOR l-list.
DEF INPUT PARAMETER case-type AS INT.

FIND FIRST l-list NO-ERROR.
IF NOT AVAILABLE l-list THEN RETURN.

IF case-type = 1 THEN        /*add*/
DO:
  create l-segment.
  ASSIGN
  l-segment.l-segmentcode = l-list.l-segmentcode. 
  l-segment.l-bezeich = l-list.l-bezeich. 
END.
ELSE IF case-type = 2 THEN   /*chg*/
DO:
    FIND FIRST l-segment WHERE l-segment.l-segmentcode = l-list.l-segmentcode NO-ERROR.
    l-segment.l-bezeich = l-list.l-bezeich. 
END.
