
DEF OUTPUT PARAMETER p-417 AS CHAR.
DEF OUTPUT PARAMETER p-547 AS INT.

FIND FIRST htparam WHERE htparam.paramnr = 417 NO-LOCK.
p-417 = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 547 NO-LOCK.
p-547 = htparam.finteger.
