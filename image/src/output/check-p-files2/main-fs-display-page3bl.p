
DEF TEMP-TABLE t-q
    FIELD number1 LIKE queasy.number1
    FIELD char3   LIKE queasy.char3.
 
  
DEF OUTPUT PARAMETER TABLE FOR t-q.

FOR EACH queasy WHERE queasy.KEY = 148 AND queasy.char3 NE "" 
    AND queasy.number1 NE 0 NO-LOCK :
    CREATE t-q.
    ASSIGN t-q.number1 = queasy.number1
           t-q.char3   = queasy.char3.
END.
