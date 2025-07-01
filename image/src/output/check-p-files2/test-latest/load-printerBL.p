DEF TEMP-TABLE t-printer LIKE vhp.printer.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER druckMode AS LOGICAL NO-UNDO.
DEF INPUT  PARAMETER osName    AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE     FOR t-printer.

CASE case-type :
    WHEN 1 THEN
    FOR EACH vhp.printer WHERE vhp.printer.bondrucker = druckMOde 
        AND vhp.printer.opsysname = osName NO-LOCK:
      CREATE t-printer.
      BUFFER-COPY vhp.printer TO t-printer.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST PRINTER WHERE bondrucker = druckMOde 
            AND vhp.printer.opsysname = osName NO-LOCK NO-ERROR.
        IF AVAILABLE PRINTER THEN
        DO:
            CREATE t-printer.
            BUFFER-COPY vhp.printer TO t-printer.
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH PRINTER NO-LOCK:
            CREATE t-printer.
            BUFFER-COPY vhp.printer TO t-printer.
        END.
    END.
END CASE.
