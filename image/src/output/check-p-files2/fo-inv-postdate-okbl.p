DEFINE INPUT PARAMETER billdate     AS DATE.
DEFINE INPUT PARAMETER curr-date    AS DATE.
DEFINE OUTPUT PARAMETER transdate   AS DATE.
DEFINE OUTPUT PARAMETER msgStr      AS CHARACTER.

DEFINE VARIABLE its-ok  AS LOGICAL INITIAL YES NO-UNDO.
DEFINE VARIABLE pdate   AS DATE NO-UNDO.

IF billdate GT curr-date THEN its-ok = NO. 
ELSE 
DO:    
    RUN htpdate.p(1003, OUTPUT pdate).
    IF billdate LE pdate THEN 
    DO: 
        its-ok = NO. 
        msgStr = "Wrong posting date;" + CHR(10) 
                + "Last transferred date F/O -> G/L = " + STRING(pdate).
         
        billdate = curr-date.
        transdate = billdate.
        RETURN.
    END.
END.

IF NOT its-ok THEN 
DO: 
    msgStr = "Wrong posting date".  
    billdate = curr-date. 
END. 

transdate = billdate.
