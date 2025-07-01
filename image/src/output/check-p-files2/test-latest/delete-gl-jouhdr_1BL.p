DEF TEMP-TABLE t-gl-jouhdr LIKE gl-jouhdr.


DEF INPUT  PARAMETER case-type   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int1        AS INTEGER.
DEF INPUT  PARAMETER int2        AS INTEGER.
DEF INPUT  PARAMETER char1       AS CHAR.
DEF INPUT  PARAMETER date1       AS DATE.
DEF INPUT  PARAMETER user-init   AS CHAR.
DEF OUTPUT PARAMETER successFlag AS LOGICAL     INITIAL NO NO-UNDO.

DEF VAR datum   AS DATE NO-UNDO.
DEF VAR refno   AS CHAR NO-UNDO.
DEF VAR bezeich AS CHAR NO-UNDO.

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
            ASSIGN
                datum   = gl-jouhdr.datum
                refno   = gl-jouhdr.refno
                bezeich = gl-jouhdr.bezeich.
            DELETE gl-jouhdr.
            RELEASE gl-jouhdr.
            ASSIGN successFlag = YES.

            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = bediener.nr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.aenderung   = "Delete Journal, Date: " + STRING(datum) + ", RefNo: " + refno + ", Desc: " + bezeich
                    res-history.action      = "G/L".
                FIND CURRENT res-history NO-LOCK.
                RELEASE res-history.
            END.
        END.
    END.
END.
