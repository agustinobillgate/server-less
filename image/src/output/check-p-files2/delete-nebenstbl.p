
DEF INPUT  PARAMETER case-type   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int1        AS INTEGER     NO-UNDO.
DEF OUTPUT PARAMETER successFlag AS LOGICAL     INITIAL NO NO-UNDO.


CASE case-type:
    WHEN 1 THEN
    DO:
      FIND FIRST nebenst WHERE RECID(nebenst) = int1
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE nebenst THEN
      DO:
          DELETE nebenst.
          RELEASE nebenst.
          ASSIGN successFlag = YES.
      END.
    END.
END.

