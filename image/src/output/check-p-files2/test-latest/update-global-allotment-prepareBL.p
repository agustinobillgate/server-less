DEF TEMP-TABLE q-list
    FIELD char1 AS CHAR.

DEF OUTPUT PARAMETER ci-date AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR q-list.

RUN htpdate.p(87, OUTPUT ci-date).
FOR EACH queasy WHERE queasy.KEY = 147 NO-LOCK 
    BY queasy.char1:
    CREATE q-list.
    ASSIGN q-list.char1 = queasy.char1.
END.


