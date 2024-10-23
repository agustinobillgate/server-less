DEFINE TEMP-TABLE summary-bill
    FIELD datum         AS DATE                             LABEL "Date"
    FIELD times         AS CHAR FORMAT "x(10)"              LABEL "Time"
    FIELD department    AS INT FORMAT ">>>"                 LABEL "Dept"
    FIELD rechnr        AS INT FORMAT ">>>>>"               LABEL "BillNo"
    FIELD total-food    AS DECIMAL FORMAT "->,>>>,>>9.99"   LABEL "Food"
    FIELD total-bev     AS DECIMAL FORMAT "->,>>>,>>9.99"   LABEL "Beverage"
    FIELD total-other   AS DECIMAL FORMAT "->,>>>,>>9.99"   LABEL "Other"
    FIELD total-service AS DECIMAL FORMAT "->,>>>,>>9.99"   LABEL "Service"
    FIELD total-tax     AS DECIMAL FORMAT "->,>>>,>>9.99"   LABEL "Tax"
    FIELD total-disc    AS DECIMAL FORMAT "->,>>>,>>9.99"   LABEL "Discount"
    FIELD total-tips    AS DECIMAL FORMAT "->,>>>,>>9.99"   LABEL "Tips"
    FIELD total-amount  AS DECIMAL FORMAT "->,>>>,>>9.99"   LABEL "Total"
    FIELD post-result   AS CHAR FORMAT "x(30)"              LABEL "RMS Response"
    FIELD body          AS CHAR     
    FIELD response      AS CHAR
    FIELD guest-name    AS CHAR FORMAT "x(25)"              LABEL "Guest Name"
    FIELD res-no        AS INT FORMAT ">>>>9"               LABEL "Res No"
    FIELD room-no       AS CHAR FORMAT "x(16)"              LABEL "Room No"
    .

DEFINE TEMP-TABLE dataList
    FIELD vKey   AS CHAR FORMAT "X(20)"
    FIELD vValue AS CHAR FORMAT "X(20)".

FUNCTION get-data RETURNS CHAR (INPUT vKey AS CHAR):
    FIND FIRST dataList WHERE dataList.vKey EQ vKey NO-LOCK NO-ERROR.
    IF AVAILABLE dataList THEN
    DO:
        RETURN dataList.vValue.
    END.
    RETURN "".
END.

DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE. 
DEFINE OUTPUT PARAMETER TABLE FOR summary-bill.

DEF VAR loop-i        AS INT.
DEF VAR messtaken     AS CHAR.
DEF VAR messkeyword   AS CHAR.
DEF VAR messvalue     AS CHAR.
DEF VAR response-char AS CHAR.
DEF VAR response-code AS CHAR.
DEF VAR currData      AS CHAR.
DEF VAR time-second   AS INT.

FOR EACH queasy WHERE queasy.KEY EQ 242 
    AND queasy.number1 EQ 99
    AND queasy.date1 GE from-date
    AND queasy.date1 LE to-date NO-LOCK BY queasy.date1:

    time-second = queasy.deci1.
    CREATE summary-bill.
    ASSIGN 
        summary-bill.datum         = queasy.date1
        summary-bill.times         = STRING(time-second,"HH:MM:SS") 
        summary-bill.department    = queasy.number3
        summary-bill.rechnr        = queasy.number2
        summary-bill.body          = queasy.char2
        summary-bill.response      = queasy.char3
        summary-bill.total-tax     = 0.


        DO loop-i = 1 TO NUM-ENTRIES(queasy.char1,"|"):
            messtaken   = ENTRY(loop-i,queasy.char1,"|").
            messkeyword = ENTRY(1,messtaken,"=").
            messvalue   = ENTRY(2,messtaken,"=").

            CASE messkeyword:
                WHEN "FOOD" THEN summary-bill.total-food    = DECIMAL(messvalue).   
                WHEN "BEVR" THEN summary-bill.total-bev     = DECIMAL(messvalue).   
                WHEN "OTHR" THEN summary-bill.total-other   = DECIMAL(messvalue).   
                WHEN "SERV" THEN summary-bill.total-service = DECIMAL(messvalue).   
                WHEN "DISC" THEN summary-bill.total-disc    = DECIMAL(messvalue). 
                WHEN "TIPS" THEN summary-bill.total-tips    = DECIMAL(messvalue). 
                WHEN "RESN" THEN summary-bill.res-no        = INT(messvalue). 
                WHEN "ROOM" THEN summary-bill.room-no       = messvalue. 
                WHEN "NAME" THEN summary-bill.guest-name    = messvalue. 
            END CASE.
        END.
        summary-bill.total-amount  = summary-bill.total-food +   
                                     summary-bill.total-bev +   
                                     summary-bill.total-other + 
                                     summary-bill.total-service +
                                     summary-bill.total-disc +  
                                     summary-bill.total-tips. 

        response-code = ENTRY(1,queasy.char3,"|").
        response-char = ENTRY(2,queasy.char3,"|").
        response-char = REPLACE(response-char,CHR(123),",").
        response-char = REPLACE(response-char,CHR(125),",").
        response-char = REPLACE(response-char,CHR(91),",").
        response-char = REPLACE(response-char,CHR(93),",").
        response-char = REPLACE(response-char,'"',"").

        EMPTY TEMP-TABLE dataList.
        DO loop-i = 1 TO NUM-ENTRIES(response-char,","):
            currData = ENTRY(loop-i,response-char,",").
        
            IF currData MATCHES "*:*" THEN
            DO:
                CREATE dataList.
                dataList.vKey   = TRIM(ENTRY(1,currData,":")).
                dataList.vValue = TRIM(ENTRY(2,currData,":")).
            END.
        END.

        IF response-code EQ "200" THEN summary-bill.post-result = CAPS(get-data("status")).
        ELSE IF response-code EQ "400" THEN summary-bill.post-result = CAPS(get-data("message")).
        ELSE IF response-code EQ "500" THEN summary-bill.post-result = CAPS(get-data("errorMessage")).
END.
