DEF TEMP-TABLE t-parameters LIKE parameters.

DEF INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT PARAMETER char1 AS CHAR NO-UNDO.
DEF INPUT PARAMETER char2 AS CHAR NO-UNDO.
DEF INPUT PARAMETER char3 AS CHAR NO-UNDO.
DEF INPUT PARAMETER int1  AS INT NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST parameters WHERE parameters.progname = char1
            AND parameters.section = char2 
            AND parameters.varname GT char3 NO-LOCK NO-ERROR.
        IF AVAILABLE parameters THEN
        DO:
            CREATE t-parameters.
            BUFFER-COPY parameters TO t-parameters.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST parameters WHERE parameters.progname = char1
            AND parameters.section = char2 
            AND parameters.varname = char3 NO-LOCK NO-ERROR.
        IF AVAILABLE parameters THEN
        DO:
            CREATE t-parameters.
            BUFFER-COPY parameters TO t-parameters.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST parameters WHERE RECID(parameters) = int1 NO-LOCK NO-ERROR.
        IF AVAILABLE parameters THEN
        DO:
            CREATE t-parameters.
            BUFFER-COPY parameters TO t-parameters.
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH parameters WHERE parameters.progname = char1 
            AND parameters.section = char2
            AND parameters.varname GT char3 NO-LOCK:
            CREATE t-parameters.
            BUFFER-COPY parameters TO t-parameters.
        END.
    END.
    WHEN 5 THEN
    DO:
        FIND FIRST parameters WHERE parameters.progname = char1
            AND parameters.section = char2 
            AND INTEGER(parameters.varname) = INTEGER(char3) NO-LOCK NO-ERROR.
        IF AVAILABLE parameters THEN
        DO:
            CREATE t-parameters.
            BUFFER-COPY parameters TO t-parameters.
        END.
    END.
END CASE.
