
DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER p-855 AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK.
p-855 = vhp.htparam.finteger.
/* cash local currency */ 
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = curr-dept
    AND vhp.h-artikel.artnr = vhp.htparam.finteger NO-LOCK.
CREATE t-h-artikel.
BUFFER-COPY h-artikel TO t-h-artikel.
ASSIGN t-h-artikel.rec-id = RECID(h-artikel).
