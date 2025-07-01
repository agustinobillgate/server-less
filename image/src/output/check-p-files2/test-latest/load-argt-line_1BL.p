
DEF TEMP-TABLE t-argt-line LIKE argt-line.
DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER argtNo AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER argtnr AS INTEGER NO-UNDO.
DEF INPUT-OUTPUT PARAMETER TABLE  FOR t-argt-line.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH argt-line WHERE argt-line.argtnr = argtNo NO-LOCK:
            CREATE t-argt-line.
            BUFFER-COPY argt-line TO t-argt-line.    
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH argt-line WHERE argt-line.argtnr = argtnr NO-LOCK:
            CREATE t-argt-line.
            BUFFER-COPY argt-line TO t-argt-line.    
        END.
    END.
END CASE.


