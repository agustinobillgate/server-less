DEF TEMP-TABLE t-bediener
    FIELD nr        LIKE bediener.nr
    FIELD userinit  LIKE bediener.userinit
    FIELD username  LIKE bediener.username
.

DEF INPUT  PARAMETER case-type  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER uname      AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

IF case-type = 1 THEN
DO:
  FIND FIRST bediener WHERE bediener.username = uname
    AND bediener.flag = 0 AND bediener.betriebsnr = 1 NO-LOCK NO-ERROR.
  IF AVAILABLE bediener THEN
  DO:
    CREATE t-bediener.
    BUFFER-COPY bediener TO t-bediener.
  END.
  RETURN.
END.

ELSE IF case-type = 2 THEN
FOR EACH bediener WHERE bediener.username = uname
  AND bediener.flag = 0 AND bediener.betriebsnr = 1 NO-LOCK:
  CREATE t-bediener.
  BUFFER-COPY bediener TO t-bediener.
END.

ELSE IF case-type = 3 THEN
FOR EACH bediener WHERE bediener.flag = 0 NO-LOCK BY bediener.username:
  CREATE t-bediener.
  BUFFER-COPY bediener TO t-bediener.
END.
