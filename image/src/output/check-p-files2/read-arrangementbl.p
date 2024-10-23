DEF TEMP-TABLE t-arrangement LIKE arrangement.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER argtNo    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER argtStr   AS CHAR    NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-arrangement.

CASE case-type:
  WHEN 1 THEN 
  DO:
      FIND FIRST arrangement WHERE arrangement.argtnr = argtNo NO-LOCK NO-ERROR.
      IF AVAILABLE arrangement THEN RUN assign-it.
  END.
  WHEN 2 THEN 
  DO:
      FIND FIRST arrangement WHERE arrangement.arrangement = argtStr NO-LOCK NO-ERROR.
      IF AVAILABLE arrangement THEN RUN assign-it.
  END.
  WHEN 3 THEN
  DO:
      FIND FIRST arrangement WHERE arrangement.arrangement = argtStr 
          AND arrangement.argtnr NE argtNo NO-LOCK NO-ERROR.
      IF AVAILABLE arrangement THEN RUN assign-it.
  END.
  WHEN 4 THEN
  DO:
      FOR EACH arrangement NO-LOCK:
          RUN assign-it.
      END.
  END.
  WHEN 5 THEN
  DO:
      FOR EACH arrangement WHERE arrangement.segmentcode NE argtNo NO-LOCK :
          RUN assign-it.
      END.
  END.
END CASE.

PROCEDURE assign-it:
  CREATE t-arrangement.
  BUFFER-COPY arrangement TO t-arrangement.
END.
