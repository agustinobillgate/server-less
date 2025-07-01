DEFINE TEMP-TABLE setup-list
    FIELD payment     AS CHAR FORMAT "x(1000)"
    FIELD statistic   AS CHAR FORMAT "x(1000)"
    FIELD outlets     AS CHAR FORMAT "x(1000)".

DEFINE INPUT PARAMETER TABLE FOR setup-list.

FIND FIRST setup-list NO-LOCK NO-ERROR.
IF AVAILABLE setup-list THEN DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 265 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO :
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN 
            queasy.char1 = ""
            queasy.char2 = ""
            queasy.char3 = "".

        ASSIGN  
            queasy.char1 = setup-list.payment   
            queasy.char2 = setup-list.statistic 
            queasy.char3 = setup-list.outlets.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
    ELSE DO:  
     CREATE queasy.
     ASSIGN 
        queasy.KEY   = 265   
        queasy.char1 = setup-list.payment   
        queasy.char2 = setup-list.statistic 
        queasy.char3 = setup-list.outlets.
    END.
END.

