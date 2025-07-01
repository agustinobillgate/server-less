DEFINE TEMP-TABLE t-nitestor LIKE nitestor.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER int1         AS INTEGER.
DEFINE INPUT PARAMETER int2         AS INTEGER.
DEFINE INPUT PARAMETER int3         AS INTEGER.
DEFINE INPUT PARAMETER int4         AS INTEGER.
DEFINE INPUT PARAMETER char1        AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-nitestor.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH nitestor WHERE nitestor.reihenfolge = int1 NO-LOCK:
            CREATE t-nitestor.
            BUFFER-COPY nitestor TO t-nitestor.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH nitestor WHERE nitestor.night-type = int1 
            AND nitestor.reihenfolge = int2 NO-LOCK:
            CREATE t-nitestor.
            BUFFER-COPY nitestor TO t-nitestor.
        END.
    END.
END CASE.
