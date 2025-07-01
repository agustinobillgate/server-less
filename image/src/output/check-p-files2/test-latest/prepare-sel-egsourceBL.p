
DEF TEMP-TABLE t-queasy
    FIELD number1 LIKE queasy.number1
    FIELD char1   LIKE queasy.char1.

DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH queasy WHERE queasy.KEY = 130 NO-LOCK BY queasy.number1:
    CREATE t-queasy.
    ASSIGN
        t-queasy.number1 = queasy.number1
        t-queasy.char1   = queasy.char1.
END.
