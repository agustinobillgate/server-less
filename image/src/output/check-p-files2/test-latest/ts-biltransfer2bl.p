
DEF TEMP-TABLE t-queasy 
    FIELD char3   LIKE queasy.char3
    FIELD char1   LIKE queasy.char1
    FIELD number3 LIKE queasy.number3
    FIELD deci3   LIKE queasy.deci3.

DEF INPUT  PARAMETER mc-str AS CHAR.
DEF OUTPUT PARAMETER do-it  AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FIND FIRST vhp.queasy WHERE vhp.queasy.key = 105
    AND vhp.queasy.number2 = 0 AND vhp.queasy.deci2 = 0
    AND vhp.queasy.char2 = mc-str AND vhp.queasy.logi2 = NO
    NO-LOCK NO-ERROR.
do-it = AVAILABLE vhp.queasy.
IF AVAILABLE queasy THEN
DO:
    CREATE t-queasy.
    ASSIGN
        t-queasy.char3   = queasy.char3
        t-queasy.char1   = queasy.char1
        t-queasy.number3 = queasy.number3
        t-queasy.deci3   = queasy.deci3.
END.
