DEF TEMP-TABLE t-res-line   LIKE res-line.

DEF INPUT  PARAMETER case-type    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER TABLE        FOR t-res-line.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEF VARIABLE hHandle AS HANDLE NO-UNDO.
hHandle = THIS-PROCEDURE.

FIND FIRST t-res-line.
CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = t-res-line.resnr 
      AND res-line.reslinnr = t-res-line.reslinnr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      BUFFER-COPY t-res-line TO res-line.
      RELEASE res-line.
      success-flag = YES.
    END.
  END.
  WHEN 2 THEN
  DO:
    CREATE res-line.
    BUFFER-COPY t-res-line TO res-line.
    RELEASE res-line.
    success-flag = YES.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = t-res-line.resnr
      AND res-line.reslinnr = t-res-line.reslinnr
      EXCLUSIVE-LOCK NO-ERROR NO-WAIT.
    IF AVAILABLE res-line THEN ASSIGN success-flag = YES.
  END.

END CASE.

PROCEDURE delete-procedure:
    DELETE PROCEDURE hHandle NO-ERROR.
END.
