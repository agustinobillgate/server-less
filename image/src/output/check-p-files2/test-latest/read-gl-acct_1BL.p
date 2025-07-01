DEF TEMP-TABLE t-gl-acct LIKE gl-acct
    FIELD map-acct AS CHAR.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER frAcctNo  AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER toAcctNo  AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = frAcctNo NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
      CREATE t-gl-acct.
      BUFFER-COPY gl-acct TO t-gl-acct.
      ASSIGN
          t-gl-acct.map-acct = ENTRY(2, gl-acct.userinit, ";"). /*NA 191020 - tambah field untuk mapping acct*/     
    END.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto GE frAcctNo
      AND gl-acct.fibukonto LE toAcctNo
      AND (gl-acct.acc-type = 1 OR gl-acct.acc-type = 2 OR gl-acct.acc-type = 5)
      NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
        DISP gl-acct.
        MESSAGE "2"
            VIEW-AS ALERT-BOX INFO BUTTONS OK.
      CREATE t-gl-acct.
      BUFFER-COPY gl-acct TO t-gl-acct.
      ASSIGN
          t-gl-acct.map-acct = ENTRY(2, gl-acct.userinit, ";"). /*NA 191020 - tambah field untuk mapping acct*/
    END.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto GE frAcctNo
      AND gl-acct.fibukonto LE toAcctNo
      AND gl-acct.acc-type = 3
      NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
      CREATE t-gl-acct.
      BUFFER-COPY gl-acct TO t-gl-acct.
      ASSIGN
          t-gl-acct.map-acct = ENTRY(2, gl-acct.userinit, ";"). /*NA 191020 - tambah field untuk mapping acct*/
    END.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto GE frAcctNo
      AND gl-acct.fibukonto LE toAcctNo
      AND gl-acct.acc-type = 4
      NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
      CREATE t-gl-acct.
      BUFFER-COPY gl-acct TO t-gl-acct.
      ASSIGN
          t-gl-acct.map-acct = ENTRY(2, gl-acct.userinit, ";"). /*NA 191020 - tambah field untuk mapping acct*/
    END.
  END.
  WHEN 5 THEN
  DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = frAcctNo 
        AND gl-acct.activeflag = YES NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
      CREATE t-gl-acct.
      BUFFER-COPY gl-acct TO t-gl-acct.
      ASSIGN
          t-gl-acct.map-acct = ENTRY(2, gl-acct.userinit, ";"). /*NA 191020 - tambah field untuk mapping acct*/
    END.
  END.
  WHEN 6 THEN
  DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = frAcctNo 
        AND gl-acct.activeflag = YES AND gl-acct.bezeich NE "" NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
      CREATE t-gl-acct.
      BUFFER-COPY gl-acct TO t-gl-acct.
      ASSIGN
          t-gl-acct.map-acct = ENTRY(2, gl-acct.userinit, ";"). /*NA 191020 - tambah field untuk mapping acct*/
    END.
  END.
  WHEN 7 THEN
  DO:
    FIND FIRST gl-acct WHERE gl-acct.bezeich = toAcctNo
        AND gl-acct.fibukonto NE frAcctNo NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
      CREATE t-gl-acct.
      BUFFER-COPY gl-acct TO t-gl-acct.
      ASSIGN
          t-gl-acct.map-acct = ENTRY(2, gl-acct.userinit, ";"). /*NA 191020 - tambah field untuk mapping acct*/
    END.
  END.
  WHEN 8 THEN
  DO:
      FIND FIRST gl-acct WHERE INTEGER(gl-acct.fibukonto) = 0 
          AND gl-acct.bezeich = "" AND gl-acct.main-nr = 0 NO-ERROR. 
      IF AVAILABLE gl-acct THEN delete gl-acct.
  END.

END CASE.
