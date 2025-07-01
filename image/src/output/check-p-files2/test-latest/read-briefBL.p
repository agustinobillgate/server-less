
DEF TEMP-TABLE t-brief          LIKE brief.

DEF INPUT  PARAMETER briefno    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER grpno      AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-brief.

IF briefno NE 0 AND (grpno EQ 0 OR grpno = ?) THEN
DO:
  FIND FIRST brief WHERE brief.briefnr = briefno NO-LOCK NO-ERROR.
  IF AVAILABLE brief THEN
  DO:
    CREATE t-brief.
    BUFFER-COPY brief TO t-brief.
  END.
END.
ELSE IF grpno NE 0 THEN
DO:
    IF briefno NE 0 THEN
    DO:
        FIND FIRST brief WHERE brief.briefkateg = grpno 
            AND brief.briefnr = briefno NO-LOCK NO-ERROR.
        IF AVAILABLE brief THEN
        DO:
            CREATE t-brief.
            BUFFER-COPY brief TO t-brief.
        END.
    END.
    ELSE
    DO:
        FOR EACH brief WHERE brief.briefkateg = grpno  NO-LOCK BY brief.briefnr:
          CREATE t-brief.
          BUFFER-COPY brief TO t-brief.
        END.
    END.
END.
