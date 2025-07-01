DEF TEMP-TABLE t-argt-line LIKE argt-line
    FIELD bezeich AS CHARACTER.

DEF TEMP-TABLE t-arrangement LIKE arrangement.

DEF INPUT  PARAMETER argtNo AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-argt-line.
DEF OUTPUT PARAMETER TABLE FOR t-arrangement.

FIND FIRST arrangement WHERE arrangement.argtnr = argtNo NO-LOCK NO-ERROR.
IF AVAILABLE arrangement THEN 
DO:
    CREATE t-arrangement.
    BUFFER-COPY arrangement TO t-arrangement.
END.

FOR EACH argt-line WHERE argt-line.argtnr = argtNo NO-LOCK:
    CREATE t-argt-line.
    BUFFER-COPY argt-line TO t-argt-line.
    FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr
        AND artikel.departement = argt-line.departement NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN
    DO:
        t-argt-line.bezeich = artikel.bezeich.
    END.
END.
