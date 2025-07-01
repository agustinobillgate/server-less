DEFINE TEMP-TABLE if-list
    FIELD month-val  AS INT
    FIELD month-str  AS CHAR FORMAT "x(20)" LABEL "Month"
    FIELD week       AS INT  LABEL "Week"
    FIELD send-date  AS DATE LABEL "Send Date"
    FIELD fr-date    AS DATE LABEL "From Date"
    FIELD to-date    AS DATE LABEL "To Date    "
    FIELD sendflag   AS LOGICAL LABEL "Send Flag"
    FIELD resendflag AS LOGICAL
    .

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER month-val AS INT.
DEFINE INPUT PARAMETER week      AS INT.
DEFINE INPUT PARAMETER send-date AS DATE.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR if-list.

IF case-type EQ 1 THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY        = 259
        queasy.betriebsnr = MONTH(send-date) 
        queasy.number1    = week
        queasy.number2    = month-val
        queasy.date1      = send-date
        queasy.date2      = from-date
        queasy.date3      = to-date
        queasy.logi1      = NO.
END.
ELSE IF case-type EQ 2 THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 259 
        AND queasy.number2 EQ month-val
        AND queasy.number1 EQ week EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN 
        queasy.date1      = send-date
        queasy.date2      = from-date
        queasy.date3      = to-date
        queasy.logi1      = NO.
    END.
END.
ELSE IF case-type EQ 3 THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 259 
        AND queasy.number2 EQ month-val
        AND queasy.number1 EQ week EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        DELETE queasy.
    END.
END.

FOR EACH queasy WHERE queasy.KEY EQ 259 NO-LOCK BY queasy.number2 BY queasy.date1:
    CREATE if-list.
    ASSIGN 
        if-list.month-val  = queasy.number2
        if-list.week       = queasy.number1
        if-list.send-date  = queasy.date1
        if-list.fr-date    = queasy.date2
        if-list.to-date    = queasy.date3
        if-list.sendflag   = queasy.logi1.

         IF queasy.number2 EQ 1 THEN if-list.month-str = "January".   
    ELSE IF queasy.number2 EQ 2 THEN if-list.month-str = "February".  
    ELSE IF queasy.number2 EQ 3 THEN if-list.month-str = "March".     
    ELSE IF queasy.number2 EQ 4 THEN if-list.month-str = "April".     
    ELSE IF queasy.number2 EQ 5 THEN if-list.month-str = "May".       
    ELSE IF queasy.number2 EQ 6 THEN if-list.month-str = "June".      
    ELSE IF queasy.number2 EQ 7 THEN if-list.month-str = "July".      
    ELSE IF queasy.number2 EQ 8 THEN if-list.month-str = "August".    
    ELSE IF queasy.number2 EQ 9 THEN if-list.month-str = "September". 
    ELSE IF queasy.number2 EQ 10 THEN if-list.month-str = "October".   
    ELSE IF queasy.number2 EQ 11 THEN if-list.month-str = "November".  
    ELSE IF queasy.number2 EQ 12 THEN if-list.month-str = "December".  
END.
