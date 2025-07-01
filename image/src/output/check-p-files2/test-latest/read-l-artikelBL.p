DEFINE TEMP-TABLE t-l-artikel   LIKE l-artikel.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER zwkum        AS INTEGER.
DEFINE INPUT PARAMETER artNo        AS INTEGER.
DEFINE INPUT PARAMETER s-artnr      AS INTEGER.
DEFINE INPUT PARAMETER s-bezeich    AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-artikel.


CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST l-artikel NO-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN RUN cr-l-artikel.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST l-artikel WHERE l-artikel.zwkum = zwkum
            AND l-artikel.artnr = artNo NO-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN
        DO:
            FIND NEXT l-artikel NO-LOCK NO-ERROR.
            IF AVAILABLE l-artikel THEN RUN cr-l-artikel.
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH l-artikel WHERE l-artikel.artnr GE s-artnr NO-LOCK :
            RUN cr-l-artikel.
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH l-artikel WHERE l-artikel.bezeich MATCHES(s-bezeich) NO-LOCK :
            RUN cr-l-artikel.
        END.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH l-artikel WHERE l-artikel.bezeich GE s-bezeich NO-LOCK :
            RUN cr-l-artikel.
        END.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST l-artikel WHERE l-artikel.artnr = artNo NO-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN RUN cr-l-artikel.
    END.
    WHEN 7 THEN
    DO:
        FOR EACH l-artikel  NO-LOCK :
            RUN cr-l-artikel.
        END.
    END.
    WHEN 8 THEN
    DO:
        FIND FIRST l-artikel WHERE NOT l-artikel.bezeich MATCHES "(Don't use)*"
            AND NOT l-artikel.bezeich MATCHES "(Dont use)*"
            AND NOT l-artikel.bezeich MATCHES "(Don't used)*"
            AND NOT l-artikel.bezeich MATCHES "(Dont used)*"
            AND NOT l-artikel.bezeich MATCHES "(Don't Use )*"
            AND NOT l-artikel.bezeich MATCHES "*(Don't Use)" NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE l-artikel:
                
            RUN cr-l-artikel.

            FIND NEXT l-artikel WHERE NOT l-artikel.bezeich MATCHES "(Don't use)*"
                AND NOT l-artikel.bezeich MATCHES "(Dont use)*"
                AND NOT l-artikel.bezeich MATCHES "(Don't used)*"
                AND NOT l-artikel.bezeich MATCHES "(Dont used)*"
                AND NOT l-artikel.bezeich MATCHES "(Don't Use )*"
                AND NOT l-artikel.bezeich MATCHES "*(Don't Use)" NO-LOCK NO-ERROR.
        END.
    END.
END CASE.

PROCEDURE cr-l-artikel :
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
END.
