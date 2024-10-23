
DEFINE TEMP-TABLE t-akt-line LIKE akt-line.

DEF INPUT  PARAMETER lineNr      AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER record-use  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER init-time   AS INT.
DEF OUTPUT PARAMETER init-date   AS DATE.
DEF OUTPUT PARAMETER p-400       AS CHAR.
DEF OUTPUT PARAMETER p-405       AS CHAR.
DEF OUTPUT PARAMETER p-406       AS CHAR.
DEF OUTPUT PARAMETER p-407       AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-akt-line.

DEF VAR flag-ok AS LOGICAL.

RUN check-timebl.p(1, lineNr, ?, "akt-line", ?, ?, OUTPUT flag-ok,
                   OUTPUT init-time, OUTPUT init-date).
IF NOT flag-ok THEN
DO:
    record-use = YES.
    RETURN NO-APPLY.
END.

FIND FIRST akt-line WHERE akt-line.linenr = lineNr NO-LOCK NO-ERROR.
IF AVAILABLE akt-line THEN
DO :
    CREATE t-akt-line.
    BUFFER-COPY akt-line TO t-akt-line.
END.

RUN htpchar.p (400, OUTPUT p-400).
RUN htpchar.p (405, OUTPUT p-405).
RUN htpchar.p (406, OUTPUT p-406).
RUN htpchar.p (407, OUTPUT p-407).
