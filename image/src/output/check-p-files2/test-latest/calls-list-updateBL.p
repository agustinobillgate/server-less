DEF INPUT PARAM i-case      AS INTEGER  NO-UNDO.
DEF INPUT PARAM s-recid     AS INTEGER  NO-UNDO.
DEF INPUT PARAM destination AS CHAR     NO-UNDO.

FIND FIRST calls WHERE RECID(calls) = s-recid NO-ERROR.
IF AVAILABLE calls THEN
DO:
  IF i-case = 1 THEN calls.satz-id = destination.
  ELSE IF i-case = 2 THEN calls.betriebsnr = 0.
  FIND CURRENT calls NO-LOCK.
END.
