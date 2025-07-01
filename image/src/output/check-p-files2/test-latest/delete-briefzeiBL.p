
DEF INPUT  PARAMETER case-type   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int1        AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER int2        AS INTEGER     NO-UNDO.
DEF OUTPUT PARAMETER successFlag AS LOGICAL     INITIAL NO NO-UNDO.


CASE case-type:
    WHEN 1 THEN
    DO:
      FIND FIRST briefzei WHERE briefzei.briefnr = int1 
            AND briefzei.briefzeilnr = int2 EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE briefzei THEN
      DO:
          DELETE briefzei.
          RELEASE briefzei.
          ASSIGN successFlag = YES.
      END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST briefzei WHERE briefzei.briefnr = int1 
              AND briefzei.briefzeilnr = 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE briefzei THEN
        DO:
            DELETE briefzei.
            RELEASE briefzei.
        END.
        FIND FIRST brief WHERE brief.briefnr = int2 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE brief THEN
        DO:
          DELETE brief.
          RELEASE brief.
          ASSIGN successFlag = YES.
        END.
    END.
END.


