
DEF OUTPUT PARAMETER integerFlag AS INT.
DEF OUTPUT PARAMETER new-contrate AS LOGICAL.
DEF OUTPUT PARAMETER ci-date AS DATE.

RUN htpint.p  (297, OUTPUT integerFlag).
RUN htplogic.p (550, OUTPUT new-contrate).
RUN htpdate.p  (87, OUTPUT ci-date).
