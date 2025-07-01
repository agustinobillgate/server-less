
DEF TEMP-TABLE t-l-untergrup
    FIELD zwkum      AS INT
    FIELD bezeich    AS CHAR
    FIELD fibukonto  AS CHAR
    FIELD betriebsnr AS INT
    FIELD main-nr    AS INT
    FIELD eng-art    AS LOGICAL.

DEF OUTPUT PARAMETER TABLE FOR t-l-untergrup.

FOR EACH l-untergrup NO-LOCK BY l-untergrup.zwkum:
    CREATE t-l-untergrup.
    ASSIGN
    t-l-untergrup.zwkum      = l-untergrup.zwkum
    t-l-untergrup.bezeich    = l-untergrup.bezeich
    t-l-untergrup.fibukonto  = l-untergrup.fibukonto
    t-l-untergrup.betriebsnr = l-untergrup.betriebsnr.

    FIND FIRST queasy WHERE queasy.KEY = 29 AND queasy.number2 = l-untergrup.zwkum
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN t-l-untergrup.main-nr = queasy.number1.
    ELSE t-l-untergrup.main-nr = 0.

    IF l-untergrup.betriebsnr = 1 THEN t-l-untergrup.eng-art = YES.
    ELSE t-l-untergrup.eng-art = NO.
END.
