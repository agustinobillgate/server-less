DEF TEMP-TABLE t-guest LIKE guest.

DEF INPUT PARAMETER gastno      AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER i-param297 AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER i-cardtype AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER ext-char   AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER ci-date    AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-guest.

RUN htpint.p  (297,  OUTPUT i-param297).
RUN htpchar.p (148, OUTPUT ext-char).
RUN htpdate.p (87,  OUTPUT ci-date).

FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK.
ASSIGN i-cardtype = guest.karteityp.

CREATE t-guest.
BUFFER-COPY guest TO t-guest.
