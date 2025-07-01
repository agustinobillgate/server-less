DEFINE INPUT PARAMETER blockID      AS CHARACTER.
DEFINE OUTPUT PARAMETER startDate   AS DATE.
DEFINE OUTPUT PARAMETER endDate     AS DATE.

FIND FIRST bk-master WHERE bk-master.block-id EQ blockID NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN 
DO:
    ASSIGN         
        startDate   = bk-master.startdate
        endDate     = bk-master.enddate.    
END.
