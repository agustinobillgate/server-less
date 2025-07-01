DEFINE TEMP-TABLE period
    FIELD perideno  AS INT
    FIELD send-date AS DATE
    FIELD from-date AS DATE
    FIELD to-date   AS DATE.

DEFINE TEMP-TABLE if-list
    FIELD perideno   AS INT
    FIELD send-date  AS DATE 
    FIELD fr-date    AS DATE
    FIELD to-date    AS DATE
    FIELD sendflag   AS LOGICAL
    FIELD resendflag AS LOGICAL
    .

DEFINE INPUT PARAMETER casetype  AS INT.
DEFINE INPUT PARAMETER month-val AS INT.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR if-list.

DEFINE VARIABLE cur-time   AS CHARACTER.
DEFINE VARIABLE time-send  AS CHARACTER INIT "14:00".
DEFINE VARIABLE daylist    AS CHARACTER INIT "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".
DEFINE VARIABLE dayrun     AS CHARACTER INIT "Tuesday".
DEFINE VARIABLE dayrunfrom AS CHARACTER INIT "Monday".
DEFINE VARIABLE dayrunto   AS CHARACTER INIT "Sunday".
DEFINE VARIABLE daynum     AS INTEGER.
DEFINE VARIABLE daynumrun  AS INTEGER.
DEFINE VARIABLE dayname    AS CHARACTER.
DEFINE VARIABLE daynamerun AS CHARACTER.

DEFINE VARIABLE get-period AS INT.
DEFINE VARIABLE loop-i     AS INT.
DEFINE VARIABLE loop-run   AS INT.
DEFINE VARIABLE lastdate   AS DATE.
DEFINE VARIABLE lastday    AS INT.

DEFINE VARIABLE rundate      AS DATE.
DEFINE VARIABLE caldate      AS DATE.
DEFINE VARIABLE get-senddate AS DATE.
DEFINE VARIABLE get-sendday  AS INT.
DEFINE VARIABLE fdate        AS DATE.
DEFINE VARIABLE tdate        AS DATE.

DEF VAR datum AS DATE.
FIND FIRST htparam WHERE paramnr EQ 110 NO-LOCK NO-ERROR.
datum = htparam.fdate.

IF casetype EQ 1 THEN
DO:
    lastdate  = DATE(MONTH(datum) + 1,1,YEAR(datum)).
    lastdate  = lastdate - 1.
    lastday   = DAY(lastdate).
    
    daynum    = WEEKDAY(datum).
    dayname   = ENTRY(daynum, daylist).
    
    DO loop-i = 1 TO lastday:
        caldate = DATE(MONTH(datum),loop-i,YEAR(datum)).
        daynum  = WEEKDAY(caldate).
        dayname = ENTRY(daynum, daylist).
    
        IF dayname EQ dayrun THEN
        DO:
            get-senddate = caldate.
            get-sendday  = DAY(caldate).
            IF get-sendday LE 10 THEN
            DO:
                fdate = DATE(MONTH(caldate),1,YEAR(caldate)).
                DO loop-run = 1 TO get-sendday:
                    rundate    = DATE(MONTH(fdate),loop-run,YEAR(fdate)).
                    daynumrun  = WEEKDAY(rundate).
                    daynamerun = ENTRY(daynumrun, daylist).
                    IF daynamerun EQ dayrunto THEN tdate = DATE(MONTH(fdate),loop-run,YEAR(fdate)).
                END.
            END.
            ELSE /*IF get-sendday GE 20 THEN*/
            DO:
                DO loop-run = 1 TO get-sendday:
                    rundate    = DATE(MONTH(caldate),loop-run,YEAR(caldate)).
                    daynumrun  = WEEKDAY(rundate).
                    daynamerun = ENTRY(daynumrun, daylist).
                    IF daynamerun EQ dayrunfrom THEN fdate = DATE(MONTH(rundate),loop-run,YEAR(rundate)) - 7.
                    IF daynamerun EQ dayrunto   THEN tdate = DATE(MONTH(rundate),loop-run,YEAR(rundate)).
                END.
            END.
            IF tdate EQ ? THEN .
            ELSE
            DO:
                CREATE period.
                ASSIGN 
                get-period       = get-period + 1
                period.perideno  = get-period   
                period.send-date = get-senddate
                period.from-date = fdate 
                period.to-date   = tdate. 
            END.
        END.
    END.
    FOR EACH period BY perideno DESC:
        get-period = period.perideno + 1.   
        tdate      = period.to-date.
        LEAVE.
    END.
    IF tdate NE lastdate THEN
    DO:
        CREATE period.
        ASSIGN 
            period.perideno  = get-period  
            period.send-date = lastdate
            period.from-date = lastdate - ((lastdate - tdate) - 1) 
            period.to-date   = lastdate. 
    END.
    
    FOR EACH period:
        FIND FIRST queasy WHERE queasy.KEY EQ 259 
            AND queasy.betriebsnr EQ MONTH(period.send-date) 
            AND queasy.number1 EQ period.perideno EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY        = 259
                queasy.betriebsnr = MONTH(period.send-date) 
                queasy.number1    = period.perideno
                queasy.date1      = period.send-date
                queasy.date2      = period.from-date
                queasy.date3      = period.to-date
                queasy.logi1      = NO
                queasy.logi2      = NO.
        END.
    END.
    
    FOR EACH queasy WHERE queasy.KEY EQ 259 
        AND queasy.betriebsnr EQ MONTH(datum) NO-LOCK:
        CREATE if-list.
        ASSIGN 
        if-list.perideno   = queasy.number1 
        if-list.send-date  = queasy.date1   
        if-list.fr-date    = queasy.date2   
        if-list.to-date    = queasy.date3   
        if-list.sendflag   = queasy.logi1
        if-list.resendflag = queasy.logi2.
    END.
END.
ELSE IF casetype EQ 2 THEN
DO:
    FOR EACH if-list:
        FIND FIRST queasy WHERE queasy.KEY EQ 259 
            AND queasy.betriebsnr EQ MONTH(if-list.send-date) 
            AND queasy.number1 EQ if-list.perideno EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN 
                queasy.logi1 = YES.
                queasy.logi2 = YES.
        END.
    END.
END.
ELSE IF casetype EQ 3 THEN
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 259 
        AND queasy.betriebsnr EQ month-val AND YEAR(queasy.date1) EQ YEAR(TODAY) NO-LOCK:
        CREATE if-list.
        ASSIGN 
        if-list.perideno   = queasy.number1 
        if-list.send-date  = queasy.date1   
        if-list.fr-date    = queasy.date2   
        if-list.to-date    = queasy.date3   
        if-list.sendflag   = queasy.logi1
        if-list.resendflag = queasy.logi2.
    END.
END.


