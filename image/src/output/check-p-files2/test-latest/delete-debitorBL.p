DEF TEMP-TABLE t-debitor     LIKE debitor
    FIELD tb-recid      AS INTEGER.


DEF INPUT  PARAMETER case-type   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int1        AS INTEGER     NO-UNDO.
DEF OUTPUT PARAMETER successFlag AS LOGICAL     INITIAL NO NO-UNDO.

CASE case-type:
    WHEN 1 THEN
    DO:
      FIND FIRST debitor WHERE RECID(debitor) = int1
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE debitor THEN
      DO:
          DELETE debitor.
          RELEASE debitor.
          ASSIGN successFlag = YES.
      END.
    END.
END.
