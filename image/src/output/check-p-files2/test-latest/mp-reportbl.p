DEFINE TEMP-TABLE t-master
   FIELD resnr                       AS INTEGER       
   FIELD gastnr                      AS INTEGER       
   FIELD name                        AS CHARACTER       
   FIELD startDATE                   AS DATE       
   FIELD endDATE                     AS DATE       
   FIELD resstatus                   AS INTEGER       
   FIELD market-nr                   AS INTEGER       
   FIELD source-nr                   AS INTEGER       
   FIELD sales-nr                    AS INTEGER       
   FIELD restype                     AS INTEGER       
   FIELD origins                     AS INTEGER       
   FIELD sob                         AS INTEGER       
   FIELD catering-flag               AS LOGICAL       
   FIELD room-flag                   AS LOGICAL       
   FIELD cancel-flag                 AS LOGICAL EXTENT 2
   FIELD cancel-type                 AS CHARACTER       
   FIELD cancel-reason               AS CHARACTER       
   FIELD cancel-destination          AS CHARACTER       
   FIELD cancel-property             AS CHARACTER       
   FIELD res-CHARACTER               AS CHARACTER EXTENT 9
   FIELD res-int                     AS INTEGER EXTENT 9
   FIELD res-dec                     AS DECIMAL EXTENT 9  
   FIELD block-id                    AS CHARACTER       
   FIELD block-code                  AS CHARACTER       
   FIELD reservation-method          AS CHARACTER       
   FIELD rooming-list-due            AS DATE       
   FIELD arrival-time                AS INTEGER       
   FIELD departure-time              AS INTEGER       
   FIELD payment                     AS CHARACTER       
   FIELD cancel-penalty              AS DECIMAL.
   
DEFINE TEMP-TABLE t-master1 LIKE t-master.   
   
DEFINE TEMP-TABLE t-bk-queasy
   FIELD key                        AS INTEGER      
   FIELD number1                    AS INTEGER      
   FIELD number2                    AS INTEGER      
   FIELD number3                    AS INTEGER      
   FIELD DATE1                      AS DATE      
   FIELD DATE2                      AS DATE      
   FIELD DATE3                      AS DATE      
   FIELD char1                      AS CHARACTER      
   FIELD char2                      AS CHARACTER      
   FIELD char3                      AS CHARACTER      
   FIELD deci1                      AS DECIMAL    
   FIELD deci2                      AS DECIMAL    
   FIELD deci3                      AS DECIMAL    
   FIELD logi1                      AS LOGICAL      
   FIELD logi2                      AS LOGICAL      
   FIELD logi3                      AS LOGICAL      
   FIELD betriebsnr                 AS INTEGER.   
   
DEFINE TEMP-TABLE t-bediener
   FIELD nr                         AS INTEGER
   FIELD username                   AS CHARACTER.

DEFINE INPUT PARAMETER reportType       AS INTEGER.
/*DEFINE INPUT PARAMETER searchBy         AS CHARACTER.
DEFINE INPUT PARAMETER searchValue      AS CHARACTER.
DEFINE INPUT PARAMETER searchDate1      AS DATE.
DEFINE INPUT PARAMETER searchDate2      AS DATE.*/
DEFINE OUTPUT PARAMETER TABLE FOR t-master.
DEFINE OUTPUT PARAMETER TABLE FOR t-bk-queasy.
DEFINE OUTPUT PARAMETER TABLE FOR t-bediener.

/*searchValue = "*" + searchValue + "*".*/

FOR EACH bk-master /*WHERE bk-master.startdate GE searchDate1 
    AND bk-master.startdate LE searchDate2*/:
    CREATE t-master.
    BUFFER-COPY bk-master TO t-master.
END.

FOR EACH t-master:
    FIND FIRST bk-queasy WHERE bk-queasy.key EQ 1 
        AND bk-queasy.number1 EQ t-master.resstatus NO-LOCK NO-ERROR.
    IF AVAILABLE bk-queasy THEN
    DO:
        ASSIGN
            t-master.resstatus = bk-queasy.number2.
    END.
END.

IF reportType EQ 1 THEN
DO:
    FOR EACH t-master WHERE t-master.resstatus NE 6:
        DELETE t-master.
    END.
END.
ELSE IF reportType EQ 2 THEN
DO:
    FOR EACH t-master WHERE t-master.resstatus NE 7:
        DELETE t-master.
    END.
END.

FOR EACH bk-queasy NO-LOCK:
    CREATE t-bk-queasy.
    BUFFER-COPY bk-queasy TO t-bk-queasy.
END.

FOR EACH bediener NO-LOCK:
    CREATE t-bediener.
    ASSIGN
        t-bediener.nr       = bediener.nr
        t-bediener.username = bediener.username.
END.
/*
IF searchBy EQ "ResNo" THEN
DO:
    searchValue = REPLACE(searchValue, "*", "").
    FOR EACH t-master WHERE t-master.resnr NE INTEGER(searchValue):
        DELETE t-master.
    END.
END.
ELSE IF searchBy EQ "Block ID" THEN
DO:
    FOR EACH t-master WHERE NOT t-master.block-id MATCHES searchValue:
        DELETE t-master.
    END.
END.
ELSE IF searchBy EQ "Block Code" THEN
DO:
    FOR EACH t-master WHERE NOT t-master.block-code MATCHES searchValue:
        DELETE t-master.
    END.    
END.
ELSE IF searchBy EQ "Name" THEN
DO:
    FOR EACH t-master WHERE NOT t-master.name MATCHES searchValue:
        DELETE t-master.
    END.    
END.
ELSE IF searchBy EQ "Sales" THEN
DO:
    FOR EACH t-master WHERE NOT t-master.block-code MATCHES searchValue:
        FIND FIRST bediener WHERE bediener.nr EQ t-master.sales-nr NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            IF NOT bediener.username MATCHES searchValue THEN
            DO:
                DELETE t-master.
            END.
        END.
    END.    
END.
ELSE IF searchBy EQ "Type" THEN
DO:
    FOR EACH t-master WHERE NOT t-master.name MATCHES searchValue:
        FIND FIRST bk-queasy WHERE bk-queasy.key EQ 5
            AND bk-queasy.number1 EQ t-master.restype NO-LOCK NO-ERROR.
        IF AVAILABLE bk-queasy THEN
        DO:
            IF NOT bk-queasy.char1 MATCHES searchValue THEN
            DO:
                DELETE t-master.
            END.
        END.    
    END.    
END.
ELSE IF searchBy EQ "Date" THEN
DO:
    FOR EACH t-master WHERE t-master.startdate GE searchDate1 AND t-master.enddate LE searchDate2:
        CREATE t-master1.
        BUFFER-COPY t-master TO t-master1.
    END.
    
    EMPTY TEMP-TABLE t-master.
    
    FOR EACH t-master1:
        CREATE t-master.
        BUFFER-COPY t-master1 TO t-master.
    END.
END.
*/
