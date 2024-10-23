/* Created by Michael @ 25/07/2019 */
DEF INPUT  PARAMETER case-type   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int1        AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER str1        AS CHARACTER   NO-UNDO.
DEF OUTPUT PARAMETER successFlag AS LOGICAL     INITIAL NO NO-UNDO.

CASE case-type:
    WHEN 1 THEN
    DO:
      FIND FIRST gl-journal WHERE RECID(gl-journal) = int1
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE gl-journal THEN
      DO:
              DELETE gl-journal.
              RELEASE gl-journal.
              ASSIGN successFlag = YES.
      END.
      ELSE ASSIGN successFlag = NO.
    END.
    WHEN 2 THEN
    DO:
      FOR EACH gl-journal WHERE gl-journal.bemerk EQ str1:
          DELETE gl-journal.
      END.
      RELEASE gl-journal.
      ASSIGN successFlag = YES.
    END.
    WHEN 3 THEN
    DO:
      FOR EACH gl-journal WHERE gl-journal.jnr EQ int1:
          DELETE gl-journal.
      END.
      RELEASE gl-journal.
      ASSIGN successFlag = YES.
    END.
END.

