DEF TEMP-TABLE t-h-rezept LIKE h-rezept.

DEFINE INPUT  PARAMETER case-type   AS INT.
DEFINE INPUT  PARAMETER int1        AS INT.
DEFINE INPUT  PARAMETER int2        AS INT.
DEFINE INPUT  PARAMETER int3        AS INT.
DEFINE INPUT  PARAMETER char1       AS CHAR.
DEFINE INPUT  PARAMETER date1       AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-rezept.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST h-rezept WHERE h-rezept.artnrrezept = int1 NO-LOCK NO-ERROR.
        IF AVAILABLE h-rezept THEN RUN assign-it.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH h-rezept NO-LOCK:
            RUN assign-it.
        END.
    END.
END CASE.


PROCEDURE assign-it:
    CREATE t-h-rezept.
    BUFFER-COPY h-rezept TO t-h-rezept.
END.
