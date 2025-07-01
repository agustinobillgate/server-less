DEFINE INPUT PARAMETER zinr AS CHAR NO-UNDO.

DEFINE VARIABLE sysdate AS DATE.

FIND FIRST htparam WHERE paramnr = 87.
sysdate = DATE(MONTH(htparam.fdate), DAY(htparam.fdate), YEAR(htparam.fdate)).

FOR EACH outorder WHERE outorder.zinr = zinr
    /*AND sysdate GE outorder.gespstart
    AND sysdate LE outorder.gespende*/
    AND outorder.gespende LT sysdate
    AND outorder.betriebsnr NE 2:
    
    FIND FIRST zimmer WHERE zimmer.zinr EQ outorder.zinr NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN
    DO:
        IF NUM-ENTRIES(outorder.gespgrund, "$") GE 1 THEN
            FIND FIRST bediener WHERE bediener.nr = INT(ENTRY(2, outorder.gespgrund, "$")) NO-LOCK NO-ERROR.
        ELSE
            FIND FIRST bediener WHERE bediener.nr = zimmer.bediener-nr-stat NO-LOCK NO-ERROR.
        
        FIND FIRST queasy WHERE queasy.KEY EQ 900 
            AND queasy.date2 EQ outorder.gespstart  
            AND queasy.date3 EQ outorder.gespende   
            AND queasy.char1 EQ outorder.zinr EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY     = 900
                queasy.number1 = zimmer.zikatnr
                queasy.char1   = outorder.zinr
                queasy.char2   = outorder.gespgrund
                queasy.date1   = sysdate
                queasy.date2   = outorder.gespstart
                queasy.date3   = outorder.gespende
                queasy.char3   = bediener.userinit.
        END.
    END.
END.
