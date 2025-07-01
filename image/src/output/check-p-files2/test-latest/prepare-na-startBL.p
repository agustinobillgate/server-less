
DEF OUTPUT PARAMETER def-natcode    AS CHAR.
DEF OUTPUT PARAMETER na-date        AS DATE.
DEF OUTPUT PARAMETER na-time        AS INTEGER.
DEF OUTPUT PARAMETER na-name        AS CHAR.

FIND FIRST htparam WHERE htparam.paramnr = 276 NO-LOCK. 
FIND FIRST nation WHERE nation.kurzbez = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE nation THEN def-natcode = nation.kurzbez. 

FIND FIRST htparam WHERE paramnr = 102 NO-LOCK. 
na-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 103 NO-LOCK. 
na-time = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 253 NO-LOCK. 
na-name = htparam.fchar.
