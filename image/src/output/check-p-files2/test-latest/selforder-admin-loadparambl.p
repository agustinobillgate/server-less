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

FOR EACH t-param:
    DELETE t-param.
END.

/*FDL Jan 09, 2023 => Add new general parameter*/
RUN selforder-addhtp5bl.p.

FIND FIRST queasy WHERE queasy.KEY EQ 222 AND queasy.number1 EQ 1 AND queasy.betriebsnr EQ dept-no NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 1
        queasy.char1    = "URL Image Logo Hotel"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 2
        queasy.char1    = "Font Color 1"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 3
        queasy.char1    = "Font Color 2"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        . 
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 4
        queasy.char1    = "Background Color"
        queasy.number3  = 5
        queasy.char2    = ""
        queasy.betriebsnr = dept-no
        . 
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 5
        queasy.char1    = "Using Payment Gateway"
        queasy.number3  = 4
        queasy.char2    = "" 
        queasy.logi1    = YES
        queasy.betriebsnr = dept-no
        .
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 6
        queasy.char1    = "URL Endpoint WebServices"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 7
        queasy.char1    = "Parameter Payment Gateway MIDTRANS"
        queasy.number3  = 5
        queasy.char2    = "MERCHANTID=11129189" 
        queasy.betriebsnr = dept-no
        .
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 8
        queasy.char1    = "Parameter Payment Gateway QRIS"
        queasy.number3  = 5
        queasy.char2    = "MALLID=3836;CLIENTID=3836"
        queasy.betriebsnr = dept-no
        .
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 9
        queasy.char1    = "UserInit For SelfOrder"
        queasy.number3  = 5
        queasy.char2    = "01" 
        queasy.betriebsnr = dept-no
        .
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 10
        queasy.char1    = "Parameter Payment Gateway DOKU"
        queasy.number3  = 5
        queasy.char2    = "MERCHANTID=11129189" 
        queasy.betriebsnr = dept-no
        .
        /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 11
        queasy.char1    = "Price Include Tax and Services"
        queasy.number3  = 4
        queasy.logi1    = NO 
        queasy.betriebsnr = dept-no
        . 
            /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 12
        queasy.char1    = "Enable Item Notes"
        queasy.number3  = 4
        queasy.logi1    = NO 
        queasy.betriebsnr = dept-no
        . 
        /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 13
        queasy.char1    = "Interval Refresh Selforder Dashboard"
        queasy.number3  = 1
        queasy.char2    = "60" 
        queasy.betriebsnr = dept-no
        . 
        /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 14
        queasy.char1    = "Use Dinamic QRCode"
        queasy.number3  = 4
        queasy.logi1    = YES 
        queasy.betriebsnr = dept-no
        . 
        /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 15
        queasy.char1    = "Allow Post Menu Without Confirmation"
        queasy.number3  = 4
        queasy.logi1    = YES 
        queasy.betriebsnr = dept-no
        . 
        /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 16
        queasy.char1    = "Range For Geofancing (in meters)"
        queasy.number3  = 1
        queasy.char2    = "1000" 
        queasy.betriebsnr = dept-no
        . 
            /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 17
        queasy.char1    = "Location For Geofancing (longitude, latitude)"
        queasy.number3  = 5
        queasy.char2    = "-6.147497652789192, 106.89989726843324" 
        queasy.betriebsnr = dept-no
        .
        /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 18
        queasy.char1    = "Hotel Additional Info"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .
        /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 19
        queasy.char1    = "Hotel Additional Link"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .
        /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 20
        queasy.char1    = "Email Receiver For Copy Bill"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .
    /*CREATE queasy.
    ASSIGN 
        queasy.KEY      = 222
        queasy.number1  = 1
        queasy.number2  = 21
        queasy.char1    = "Set This Outlet As Room Service"
        queasy.number3  = 4
        queasy.logi1    = NO 
        queasy.betriebsnr = dept-no
        .*/
END.

FOR EACH queasy WHERE queasy.KEY EQ 222 AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no NO-LOCK BY queasy.number2:
    CREATE t-param.
    ASSIGN
        t-param.dept    = queasy.betriebsnr 
        t-param.grup    = queasy.number1
        t-param.number  = queasy.number2
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


