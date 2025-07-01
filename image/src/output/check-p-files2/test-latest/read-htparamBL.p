DEF TEMP-TABLE t-htparam LIKE htparam.

DEFINE INPUT  PARAMETER case-type   AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER paramNo     AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER paramGrup   AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-htparam.

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = paramNo NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN
        DO:
          CREATE t-htparam.
          BUFFER-COPY htparam TO t-htparam.
        END.                                                                
    END.
    WHEN 2 THEN
    DO:
        FOR EACH htparam WHERE htparam.paramgruppe = paramGrup NO-LOCK :
            CREATE t-htparam.
            BUFFER-COPY htparam TO t-htparam.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = paramNo 
            AND htparam.paramgr = paramGrup NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN
        DO:
          CREATE t-htparam.
          BUFFER-COPY htparam TO t-htparam.
        END.                                                                
    END.
    WHEN 4 THEN
    DO:
        FOR EACH htparam WHERE  htparam.paramnr LE paramNo NO-LOCK:
            CREATE t-htparam.
            BUFFER-COPY htparam TO t-htparam.
        END.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH htparam WHERE htparam.paramnr GE 1 
            AND htparam.paramnr LE 16 NO-LOCK:
            CREATE t-htparam.
            BUFFER-COPY htparam TO t-htparam.
        END.
    END.
    WHEN 6 THEN
    DO:
        FOR EACH htparam WHERE htparam.paramgr = paramGrup NO-LOCK:
            CREATE t-htparam.
            BUFFER-COPY htparam TO t-htparam.
        END.
    END.
    WHEN 7 THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr = paramNo 
            AND htparam.bezeich NE "Not used" NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN
        DO:
          CREATE t-htparam.
          BUFFER-COPY htparam TO t-htparam.
        END.                                                                
    END.
END CASE.
