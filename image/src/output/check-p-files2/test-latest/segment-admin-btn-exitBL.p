DEFINE TEMP-TABLE t-l-segment
    FIELD l-segmentcode LIKE l-segment.l-segmentcode
    FIELD l-bezeich     LIKE l-segment.l-bezeich.

DEFINE TEMP-TABLE l-list LIKE l-segment. 

DEFINE INPUT PARAMETER TABLE FOR l-list.
DEFINE INPUT PARAMETER case-type AS INT.

FIND FIRST l-list NO-ERROR.
IF NOT AVAILABLE l-list THEN RETURN.

IF case-type = 1 THEN        /*add*/
DO:
    CREATE l-segment.
    ASSIGN
        l-segment.l-segmentcode = l-list.l-segmentcode. 
        l-segment.l-bezeich = l-list.l-bezeich. 
END.
ELSE IF case-type = 2 THEN   /*chg*/
DO:
    /*Alder - Serverless - Issue 690 - Start*/
    FIND FIRST l-segment WHERE l-segment.l-segmentcode = l-list.l-segmentcode NO-LOCK NO-ERROR.
    IF AVAILABLE l-segment THEN 
    DO:
        FIND CURRENT l-segment EXCLUSIVE-LOCK.
        ASSIGN l-segment.l-bezeich = l-list.l-bezeich. 
        FIND CURRENT l-segment NO-LOCK.
        RELEASE l-segment.
    END.
    /*Alder - Serverless - Issue 690 - End*/
END.
