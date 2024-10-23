DEF TEMP-TABLE t-argt-line LIKE argt-line.

DEF INPUT  PARAMETER argtNo AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE  FOR t-argt-line.
FOR EACH argt-line WHERE argt-line.argtnr = argtNo NO-LOCK:
    CREATE t-argt-line.
    BUFFER-COPY argt-line TO t-argt-line.
END.
