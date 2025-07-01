DEF TEMP-TABLE t-bediener LIKE bediener.
DEF TEMP-TABLE t-kellner
    FIELD kellner-nr LIKE kellner.kellner-nr.

DEF INPUT PARAMETER curr-dept  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER kellner-nr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER user-init  AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.
DEF OUTPUT PARAMETER TABLE FOR t-kellner.

IF user-init NE "" THEN
DO:
  FIND FIRST bediener WHERE bediener.userinit = user-init
      AND bediener.flag = 0 NO-LOCK NO-ERROR.
  IF NOT AVAILABLE bediener THEN RETURN.
  CREATE t-bediener.
  BUFFER-COPY bediener TO t-bediener.
  FIND FIRST kellner WHERE kellner.kellner-nr = INTEGER(bediener.userinit)
    AND kellner.departement = curr-dept NO-LOCK NO-ERROR.
  IF NOT AVAILABLE kellner THEN RETURN.
  CREATE t-kellner.
  BUFFER-COPY kellner TO t-kellner.
END.
ELSE IF kellner-nr NE 0 THEN
DO:
  FIND FIRST kellner WHERE kellner.kellner-nr = kellner-nr
    AND kellner.departement = curr-dept NO-LOCK NO-ERROR.
  IF NOT AVAILABLE kellner THEN RETURN.
  CREATE t-kellner.
  BUFFER-COPY kellner TO t-kellner.
  IF kellner.kellner-nr LT 10 THEN
  FIND FIRST bediener WHERE bediener.userinit = STRING(kellner.kellner-nr,"99")
      NO-LOCK NO-ERROR.
  ELSE
  FIND FIRST bediener WHERE bediener.userinit = STRING(kellner.kellner-nr)
      NO-LOCK NO-ERROR.
  IF NOT AVAILABLE bediener THEN RETURN.
  CREATE t-bediener.
  BUFFER-COPY bediener TO t-bediener.
END.

