DEFINE TEMP-TABLE t-bediener LIKE bediener.

DEFINE INPUT  PARAMETER case-type   AS INTEGER   NO-UNDO.
DEFINE INPUT  PARAMETER name-str    AS CHAR      NO-UNDO.
DEFINE INPUT  PARAMETER id-str      AS CHAR      NO-UNDO.
DEFINE INPUT  PARAMETER nr          AS INT       NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR t-bediener.

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST bediener WHERE bediener.username = name-str 
            AND bediener.flag = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN
        DO:
          CREATE t-bediener.
          BUFFER-COPY bediener TO t-bediener.
        END.                                                                
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST bediener WHERE bediener.username = name-str 
            AND bediener.usercode = id-str AND bediener.betriebsnr = 0 
            AND bediener.flag = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN
        DO:
          CREATE t-bediener.
          BUFFER-COPY bediener TO t-bediener.
        END.                                                                
    END.
    WHEN 3 THEN
    DO:
        FOR EACH bediener WHERE bediener.username = name-str 
            AND bediener.betriebsnr = 1 AND bediener.flag = 0 NO-LOCK :
          CREATE t-bediener.
          BUFFER-COPY bediener TO t-bediener.
        END.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST bediener WHERE bediener.nr = nr NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
          CREATE t-bediener.
          BUFFER-COPY bediener TO t-bediener.
        END.   
    END.
END CASE.


