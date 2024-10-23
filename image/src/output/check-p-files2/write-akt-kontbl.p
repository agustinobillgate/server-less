
DEF TEMP-TABLE t-akt-kont LIKE akt-kont.

DEF INPUT  PARAMETER case-type    AS INTEGER            NO-UNDO.
DEF INPUT  PARAMETER TABLE        FOR t-akt-kont.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO NO-UNDO.

CASE case-type:
  WHEN 1 THEN /* update and create new */
  DO:
    FIND FIRST t-akt-kont NO-ERROR.
    IF NOT AVAILABLE t-akt-kont THEN RETURN.
    FIND FIRST akt-kont WHERE akt-kont.gastnr = t-akt-kont.gastnr
      AND akt-kont.kontakt-nr = t-akt-kont.kontakt-nr
      EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE akt-kont THEN CREATE akt-kont.
    DO:
      BUFFER-COPY t-akt-kont TO akt-kont.
      FIND CURRENT akt-kont NO-LOCK.
      success-flag = YES.
    END.
  END.
  WHEN 2 THEN /* delete */
  DO:
    FIND FIRST t-akt-kont NO-ERROR.
    IF NOT AVAILABLE t-akt-kont THEN RETURN.
    FIND FIRST akt-kont WHERE akt-kont.gastnr = t-akt-kont.gastnr
      AND akt-kont.kontakt-nr = t-akt-kont.kontakt-nr
      EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE akt-kont THEN
    DO:
      DELETE akt-kont.
      RELEASE akt-kont.
      success-flag = YES.
    END.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST t-akt-kont NO-ERROR.
    IF NOT AVAILABLE t-akt-kont THEN RETURN.
    CREATE akt-kont.
    BUFFER-COPY t-akt-kont TO akt-kont.
    success-flag = YES.
  END.
END CASE.
