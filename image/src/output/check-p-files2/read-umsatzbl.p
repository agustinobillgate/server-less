DEFINE TEMP-TABLE t-umsatz LIKE umsatz.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER artNo AS INTEGER.
DEF INPUT PARAMETER deptNo AS INTEGER.
DEF INPUT PARAMETER datum AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-umsatz.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST umsatz WHERE umsatz.artnr = artNo
            AND umsatz.departement = deptNo AND umsatz.datum = datum
            NO-LOCK NO-ERROR.
        IF AVAILABLE umsatz THEN
        DO:
            CREATE t-umsatz.
            BUFFER-COPY umsatz TO t-umsatz.
        END.
    END.
END CASE.
