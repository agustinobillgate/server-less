DEF TEMP-TABLE t-gl-jouhdr LIKE gl-jouhdr.


DEF INPUT  PARAMETER case-type   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int1        AS INTEGER.
DEF INPUT  PARAMETER int2        AS INTEGER.
DEF INPUT  PARAMETER char1       AS CHAR.
DEF INPUT  PARAMETER date1       AS DATE.
DEF OUTPUT PARAMETER successFlag AS LOGICAL     INITIAL NO NO-UNDO.

CASE case-type:
    WHEN 1 THEN
    DO:
      FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = char1
          AND gl-jouhdr.jnr = int1 AND gl-jouhdr.jtype = int2
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE gl-jouhdr THEN
      DO:
          DELETE gl-jouhdr.
          RELEASE gl-jouhdr.
          ASSIGN successFlag = YES.
      END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST gl-jouhdr WHERE RECID(gl-jouhdr) = int1
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE gl-jouhdr THEN
        DO:
            DELETE gl-jouhdr.
            RELEASE gl-jouhdr.
            ASSIGN successFlag = YES.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = int1
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE gl-jouhdr THEN
        DO:
            DELETE gl-jouhdr.
            RELEASE gl-jouhdr.
            ASSIGN successFlag = YES.
        END.
    END.
END.
