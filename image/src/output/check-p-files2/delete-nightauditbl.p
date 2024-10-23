
DEF INPUT  PARAMETER case-type   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int1        AS INTEGER     NO-UNDO.
DEF OUTPUT PARAMETER successFlag AS LOGICAL     INITIAL NO NO-UNDO.


CASE case-type:
    WHEN 1 THEN
    DO:
      FIND FIRST nightaudit WHERE RECID(nightaudit) = int1
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE nightaudit THEN
      DO:
          DELETE nightaudit.
          RELEASE nightaudit.
          ASSIGN successFlag = YES.
      END.
    END.
END.

