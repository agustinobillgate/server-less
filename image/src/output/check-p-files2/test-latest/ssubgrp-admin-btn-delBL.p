
DEF INPUT PARAMETER l-untergrup-zwkum AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-untergrup-zwkum.

FIND FIRST l-artikel WHERE l-artikel.zwkum = l-untergrup-zwkum NO-LOCK NO-ERROR. 
IF AVAILABLE l-artikel THEN flag = 1.
ELSE 
DO: 
    FIND FIRST queasy WHERE queasy.KEY = 29 
      AND queasy.number2 = l-untergrup-zwkum EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DELETE queasy.
    FIND CURRENT l-untergrup EXCLUSIVE-LOCK. 
    delete l-untergrup.
END.
