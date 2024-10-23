DEF TEMP-TABLE t-uebertrag LIKE uebertrag.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER date1 AS DATE.
DEF INPUT PARAMETER date2 AS DATE.
DEF INPUT PARAMETER deci1 AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-uebertrag.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH uebertrag WHERE uebertrag.datum LE date2
            AND uebertrag.datum GE date1 NO-LOCK BY uebertrag.datum:
            CREATE t-uebertrag.
            BUFFER-COPY uebertrag TO t-uebertrag.
        END.
    END.
END CASE.
