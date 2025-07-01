DEFINE TEMP-TABLE segm-list
    FIELD segm-code    AS INTEGER
    FIELD segm-bezeich AS CHAR.

DEF OUTPUT PARAMETER ci-date       AS DATE NO-UNDO.
DEF OUTPUT PARAMETER first-segment AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR segm-list.

RUN htpdate.p (87, OUTPUT ci-date).

FIND FIRST segment NO-LOCK NO-ERROR.
IF AVAILABLE segment THEN first-segment = " ".

FOR EACH segment WHERE segment.bezeich NE first-segment 
    AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) NO-LOCK:
    CREATE segm-list.
    ASSIGN 
        segm-list.segm-code      = segment.segmentcode
        segm-list.segm-bezeich   = segment.bezeich.
END.
