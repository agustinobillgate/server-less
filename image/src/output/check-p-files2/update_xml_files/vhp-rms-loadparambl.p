DEFINE TEMP-TABLE t-param
    FIELD dept      AS INTEGER   FORMAT ">>9"
    FIELD grup      AS INTEGER   FORMAT ">>9"
    FIELD number    AS INTEGER   FORMAT ">>9"   LABEL "No"
    FIELD bezeich   AS CHARACTER FORMAT "x(50)" LABEL "Description"
    FIELD typ       AS INTEGER 
    FIELD logv      AS LOGICAL 
    FIELD val       AS CHARACTER FORMAT "x(30)" LABEL "Value".

DEFINE INPUT PARAMETER dept-no AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-param.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 1 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 1
        queasy.char1      = "Username"
        queasy.number3    = 5
        queasy.char2      = "".  
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 2 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 2
        queasy.char1      = "Password"
        queasy.number3    = 5
        queasy.char2      = "".  
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 3 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 3
        queasy.char1      = "Hotel Code"
        queasy.number3    = 5
        queasy.char2      = "".  
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 4 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 4
        queasy.char1      = "Interval Refresh Time"
        queasy.number3    = 1
        queasy.char2      = "".  
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 5 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 5
        queasy.char1      = "Output Local Filepath"
        queasy.number3    = 5
        queasy.char2      = "C:\e1-vhp\rms\".  
END.

DEFINE VARIABLE loop-i AS INT.
DEFINE VARIABLE rpt-list AS CHAR EXTENT 19.
rpt-list[6]  = "Master Data".
rpt-list[7]  = "Room Overview".
rpt-list[8]  = "Room Availability".
rpt-list[9]  = "Monthly Forecast Of Room Occupancy".
rpt-list[10] = "Forecast Room Production".
rpt-list[11] = "Future Booking".
rpt-list[12] = "Reservation By Creation Date".
rpt-list[13] = "Inhouse Guest List".
rpt-list[14] = "Cancelled Reservation".
rpt-list[15] = "Room Revenue Breakdown".
rpt-list[16] = "Front Office Turnover Report".
rpt-list[17] = "Company Room Production".
rpt-list[18] = "Travel Agent Room Production".
rpt-list[19] = "Room Recapitulation With Guest Segment".

DO loop-i = 6 TO 19:
    FIND FIRST queasy WHERE queasy.KEY EQ 347
        AND queasy.betriebsnr EQ 3
        AND queasy.number1 EQ loop-i NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY        = 347
            queasy.betriebsnr = 3
            queasy.number1    = loop-i
            queasy.char1      = "URL " + rpt-list[loop-i] + " (method;url)"
            queasy.number3    = 5
            queasy.char2      = "". 
    END.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 20 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 20
        queasy.char1      = "Debug Mode"
        queasy.number3    = 4
        queasy.logi1      = YES.  
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 21 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 21
        queasy.char1      = "Using Token"
        queasy.number3    = 4
        queasy.logi1      = NO.  
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 22 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 22
        queasy.char1      = "URL Get Token"
        queasy.number3    = 5
        queasy.char2      = "".  
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 23 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 23
        queasy.char1      = "Authentication Method"
        queasy.number3    = 5
        queasy.char2      = "".  
END.

FIND FIRST queasy WHERE queasy.KEY EQ 347
    AND queasy.betriebsnr EQ 3 
    AND queasy.number1 EQ 24 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 347
        queasy.betriebsnr = 3
        queasy.number1    = 24
        queasy.char1      = "Authentication Code"
        queasy.number3    = 5
        queasy.char2      = "".  
END.
/*LOAD PARAM TO UI*/
FOR EACH queasy WHERE queasy.KEY EQ 347 AND queasy.betriebsnr EQ 3 NO-LOCK BY queasy.number1:
    CREATE t-param.
    ASSIGN
        t-param.dept    = queasy.betriebsnr 
        t-param.number  = queasy.number1
        t-param.bezeich = queasy.char1
        t-param.typ     = queasy.number3.
    IF queasy.number3 EQ 1 THEN t-param.val = STRING(queasy.char2).
    ELSE IF queasy.number3 EQ 2 THEN t-param.val = STRING(queasy.deci1).
    ELSE IF queasy.number3 EQ 3 THEN t-param.val = STRING(queasy.date1).
    ELSE IF queasy.number3 EQ 4 THEN
    DO:
        t-param.val  = STRING(queasy.logi1).
        t-param.logv = queasy.logi1.
    END.
    ELSE IF queasy.number3 EQ 5 THEN t-param.val = STRING(queasy.char2).
END.


