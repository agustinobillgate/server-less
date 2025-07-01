
DEF OUTPUT PARAMETER i AS INT.
DEFINE buffer arr FOR arrangement. 
FOR EACH arr NO-LOCK: 
    IF i LT arr.argtnr THEN i = arr.argtnr. 
END. 
i = i + 1. 
