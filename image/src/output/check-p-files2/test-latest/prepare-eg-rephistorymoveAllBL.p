
DEF TEMP-TABLE t-queasy133 LIKE queasy.

DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-queasy133.

RUN htpdate.p(87, OUTPUT ci-date).
FOR EACH queasy WHERE KEY = 133:
    CREATE t-queasy133.
    BUFFER-COPY queasy TO t-queasy133.
END.
