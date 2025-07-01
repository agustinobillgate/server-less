
DEF INPUT  PARAMETER rcvname   AS CHAR.
DEF OUTPUT PARAMETER avail-bed AS LOGICAL INIT NO.

FIND FIRST bediener WHERE bediener.username = rcvname NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN avail-bed = YES.
