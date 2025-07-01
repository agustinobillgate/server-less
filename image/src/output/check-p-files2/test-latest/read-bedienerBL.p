DEF TEMP-TABLE t-bediener LIKE bediener.
DEF INPUT  PARAMETER userNo   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER user-init AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

IF user-init = "&Sales Group" THEN /* sales-usrUI */
DO:
  FOR EACH bediener WHERE bediener.user-group = userNo 
    AND bediener.flag = 0 NO-LOCK BY bediener.username:
    CREATE t-bediener.
    BUFFER-COPY bediener TO t-bediener.
  END.
  RETURN.
END.

IF user-init NE "" THEN 
DO:    
  FIND FIRST bediener WHERE bediener.userinit = user-init
    NO-LOCK NO-ERROR.
  IF NOT AVAILABLE bediener THEN
  FIND FIRST bediener WHERE bediener.username = user-init
      NO-LOCK NO-ERROR.
END.
ELSE IF userNo NE 0 THEN FIND FIRST bediener WHERE bediener.nr = userNo
    NO-LOCK NO-ERROR.

IF AVAILABLE bediener THEN
DO:
  CREATE t-bediener.
  BUFFER-COPY bediener TO t-bediener.
END.
