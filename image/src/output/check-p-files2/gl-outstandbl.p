
DEF INPUT PARAMETER date1 AS DATE.
DEF INPUT PARAMETER int1  AS INT.
DEF INPUT PARAMETER deci1 AS DECIMAL.

FIND FIRST uebertrag WHERE uebertrag.datum = date1
    AND uebertrag.betriebsnr = int1 EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE uebertrag THEN
DO:
    ASSIGN
        uebertrag.betrag = deci1.
    RELEASE uebertrag.
END.
