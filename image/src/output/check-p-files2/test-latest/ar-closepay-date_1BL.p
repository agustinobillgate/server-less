DEF OUTPUT PARAMETER bill-date      AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER last-transfer  AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER rundung        AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER p121           AS INTEGER  NO-UNDO.

RUN htpdate.p (110, OUTPUT bill-date).
RUN htpdate.p (1014, OUTPUT last-transfer). /* LAST A/R Transfer DATE */
RUN htpint.p (491, OUTPUT rundung).
RUN htpint.p (121, OUTPUT p121).

