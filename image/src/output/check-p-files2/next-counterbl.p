DEF TEMP-TABLE t-counters LIKE counters.
DEF INPUT  PARAMETER counterNo      AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-counters.

FIND FIRST counters WHERE counters.counter-no = counterNo EXCLUSIVE-LOCK NO-ERROR.

IF NOT AVAILABLE counters THEN
DO:
  CREATE counters.
  ASSIGN
      counters.counter-no  = counterNo
      counters.counter-bez = STRING(counterNo)
      counters.counter     = 0
  .
END.
ASSIGN counters.counter = counters.counter + 1.
FIND CURRENT counters NO-LOCK.

CREATE t-counters.
BUFFER-COPY counters TO t-counters.
