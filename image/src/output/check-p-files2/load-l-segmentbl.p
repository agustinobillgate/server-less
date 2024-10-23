DEF TEMP-TABLE t-l-segment LIKE l-segment.

DEF OUTPUT PARAMETER TABLE FOR t-l-segment.

FOR EACH l-segment NO-LOCK:
  CREATE t-l-segment.
  BUFFER-COPY l-segment TO t-l-segment.
END.
