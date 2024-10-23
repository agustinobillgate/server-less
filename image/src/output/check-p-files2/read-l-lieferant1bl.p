DEF TEMP-TABLE t-l-lieferant LIKE l-lieferant.

DEF INPUT  PARAMETER case-type AS INT.
DEF INPUT  PARAMETER char1     AS CHAR.
DEF INPUT  PARAMETER int1      AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-l-lieferant.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH l-lieferant WHERE l-lieferant.firma GE char1 
            NO-LOCK BY l-lieferant.firma:
            CREATE t-l-lieferant.
            BUFFER-COPY l-lieferant TO t-l-lieferant.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH l-lieferant WHERE l-lieferant.firma MATCHES ("*" + char1 + "*")
            NO-LOCK BY l-lieferant.firma:
            CREATE t-l-lieferant.
            BUFFER-COPY l-lieferant TO t-l-lieferant.
        END.
    END.
END CASE.
