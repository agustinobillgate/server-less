
DEF TEMP-TABLE pur-list
    FIELD number1   LIKE queasy.number1
    FIELD char1     LIKE queasy.char1
    FIELD char3     LIKE queasy.char3.

DEF OUTPUT PARAMETER TABLE FOR pur-list.

FOR EACH queasy WHERE queasy.KEY = 143 NO-LOCK 
    BY queasy.char1:
    CREATE pur-list.
    ASSIGN
        pur-list.number1   = queasy.number1
        pur-list.char1     = queasy.char1
        pur-list.char3     = queasy.char3.
END.
