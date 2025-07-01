DEF TEMP-TABLE t-bediener LIKE bediener.

DEF INPUT  PARAMETER case-type  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER uname      AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

/* SY JUL 25 2017 */
CASE case-type:
    /* SY AUG 16 2017 */
    WHEN 1 THEN
    DO:
      FIND FIRST bediener WHERE bediener.username = uname
        AND bediener.flag = 0 AND bediener.betriebsnr = 1 NO-LOCK NO-ERROR.
      IF AVAILABLE bediener THEN
      DO:
        CREATE t-bediener.
        BUFFER-COPY bediener TO t-bediener.
      END.
      ELSE IF uname = "sindata" THEN
      DO:
          FIND FIRST bediener WHERE bediener.username = (uname + CHR(3))
            AND bediener.flag = 1 AND bediener.betriebsnr = 1 NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN
          DO:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
          END.
      END.
      RETURN.
    END.
    /* SY AUG 16 2017 */
    WHEN 2 THEN
    DO:
      FOR EACH bediener WHERE bediener.username = uname
        AND bediener.flag = 0 AND bediener.betriebsnr = 1 NO-LOCK:
        CREATE t-bediener.
        BUFFER-COPY bediener TO t-bediener.
      END.
      FIND FIRST t-bediener NO-ERROR.
      IF NOT AVAILABLE t-bediener AND uname = "sindata" THEN
      DO:
          FIND FIRST bediener WHERE bediener.username = (uname + CHR(3))
            AND bediener.flag = 1 AND bediener.betriebsnr = 1 NO-LOCK NO-ERROR.
          IF AVAILABLE bediener THEN
          DO:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
          END.
       END.
    END.
    WHEN 3 THEN
    FOR EACH bediener WHERE bediener.flag = 0 NO-LOCK BY bediener.username:
      CREATE t-bediener.
      BUFFER-COPY bediener TO t-bediener.
    END.
    WHEN 4 THEN
    DO:
    DEF VARIABLE user-name      AS CHAR NO-UNDO INIT "".
    DEF VARIABLE htlgrp-code    AS CHAR NO-UNDO INIT "".
      ASSIGN
          user-name   = ENTRY(1, uname, CHR(2))
          htlgrp-code = ENTRY(2, uname, CHR(2))
      .
      IF user-name = "" OR htlgrp-code = "" THEN RETURN.
      FIND FIRST queasy WHERE queasy.KEY = 187 
          AND queasy.char1 = htlgrp-code NO-LOCK NO-ERROR.
      IF NOT AVAILABLE queasy THEN RETURN.
      FIND FIRST bediener WHERE bediener.username = user-name
        AND bediener.flag = 0 AND bediener.betriebsnr = 1 NO-LOCK NO-ERROR.
      IF AVAILABLE bediener THEN
      DO:
        CREATE t-bediener.
        BUFFER-COPY bediener TO t-bediener.
      END.
    END.
    WHEN 5 THEN  /* used for setup-userUI.p */
    FOR EACH bediener NO-LOCK:
        CREATE t-bediener.
        BUFFER-COPY bediener TO t-bediener.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST bediener WHERE bediener.username MATCHES "*" + CHR(2) + "*" NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN DO:
            CREATE t-bediener.
            BUFFER-COPY bediener TO t-bediener.
        END.
    END.
END CASE.
