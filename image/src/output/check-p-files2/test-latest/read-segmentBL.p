
DEF TEMP-TABLE t-segment          LIKE segment.

DEF INPUT  PARAMETER case-type    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER segmentNo    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER segmName     AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-segment.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST segment WHERE segment.segmentcode = segmentNo NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN
    DO:
      CREATE t-segment.
      BUFFER-COPY segment TO t-segment.
    END.
  END.
  WHEN 2 THEN
  FOR EACH segment WHERE segment.betriebsnr LE 2 
    AND NUM-ENTRIES(segment.bezeich, "$$0") = 1 /* $$0 --> SEGM not active */
    NO-LOCK BY segment.betriebsnr BY segment.segmentcode:
    CREATE t-segment.
    BUFFER-COPY segment TO t-segment.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST segment WHERE ENTRY(1, segment.bezeich, "$$0") = segmName NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN
    DO:
      CREATE t-segment.
      BUFFER-COPY segment TO t-segment.
    END.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST segment WHERE segment.betriebsnr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN
    DO:
      CREATE t-segment.
      BUFFER-COPY segment TO t-segment.
    END.
  END.
  WHEN 5 THEN
  DO:
    FOR EACH segment WHERE segment.segmentcode NE segmentNo AND 
        segment.segmentgrup NE 0 NO-LOCK:
        CREATE t-segment.
        BUFFER-COPY segment TO t-segment.
    END.
  END.
    WHEN 6 THEN
    FOR EACH segment WHERE segment.vip-level = 0
      AND NUM-ENTRIES(segment.bezeich, "$$0") = 1 /* $$0 --> SEGM not active */
      NO-LOCK BY segment.betriebsnr BY segment.segmentcode:
      CREATE t-segment.
      BUFFER-COPY segment TO t-segment.
    END.

END CASE.
