DEF TEMP-TABLE t-push-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0.

DEF INPUT  PARAMETER TABLE FOR t-push-list.
DEF INPUT  PARAMETER bookengID AS INT.

DEF VAR str AS CHAR.
DEF BUFFER bufQ FOR queasy.
FOR EACH queasy WHERE queasy.KEY = 163 AND queasy.number1 = bookengID:
    DELETE queasy.
END.
FOR EACH t-push-list NO-LOCK:
    str = t-push-list.rcodeVHP   + ";"
        + t-push-list.rcodeBE    + ";"
        + t-push-list.rmtypeVHP  + ";"
        + t-push-list.rmtypeBE   + ";"
        + t-push-list.argtVHP.

    CREATE bufQ.
    ASSIGN
        bufQ.KEY = 163
        bufQ.number1 = bookengID
        bufQ.char1 = str.
    RELEASE bufQ.
END.
