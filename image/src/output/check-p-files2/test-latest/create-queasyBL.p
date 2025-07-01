DEF TEMP-TABLE t-queasy LIKE queasy.

DEFINE INPUT PARAMETER TABLE FOR t-queasy.
DEFINE OUTPUT PARAMETER q-recid AS INT.

FIND FIRST t-queasy NO-ERROR.
IF AVAILABLE t-queasy THEN
DO:
  CREATE queasy.
  BUFFER-COPY t-queasy TO queasy.
  FIND CURRENT queasy NO-LOCK.
  q-recid = RECID(queasy).
END.
