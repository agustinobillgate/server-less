DEFINE INPUT PARAMETER casetype  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER inp-param AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER flogical AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER fdate    AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER fchar    AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER fint     AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER fdec     AS DECIMAL NO-UNDO.

CASE casetype:
    WHEN 1 THEN DO:
        RUN htplogic.p(inp-param, OUTPUT flogical).
    END.
    WHEN 2 THEN DO:
        RUN htpdate.p(inp-param, OUTPUT fdate).
    END.
    WHEN 3 THEN DO:
        RUN htpchar.p(inp-param, OUTPUT fchar).
    END.
    WHEN 4 THEN DO:
        RUN htpint.p(inp-param, OUTPUT fint).
    END.
    WHEN 5 THEN DO:
        RUN htpdec.p(inp-param, OUTPUT fdec).
    END.
END CASE.
