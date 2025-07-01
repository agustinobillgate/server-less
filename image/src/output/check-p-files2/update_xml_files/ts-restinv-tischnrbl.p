
DEF INPUT  PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL INIT NO.

FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 31 
    AND vhp.queasy.number1 = curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN avail-queasy = YES.
