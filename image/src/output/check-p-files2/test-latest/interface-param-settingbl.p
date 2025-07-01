DEFINE TEMP-TABLE hotel-config
    FIELD keynr      AS INT
    FIELD number1    AS INT
    FIELD number2    AS INT
    FIELD number3    AS INT
    FIELD date1      AS DATE
    FIELD date2      AS DATE
    FIELD date3      AS DATE
    FIELD char1      AS CHAR
    FIELD char2      AS CHAR
    FIELD char3      AS CHAR
    FIELD deci1      AS DECIMAL
    FIELD deci2      AS DECIMAL
    FIELD deci3      AS DECIMAL
    FIELD logi1      AS LOGICAL
    FIELD logi2      AS LOGICAL
    FIELD logi3      AS LOGICAL
    FIELD betriebsnr AS INT.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR hotel-config.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.

IF case-type EQ 1 THEN /*add*/
DO :
    FIND FIRST hotel-config NO-ERROR.
    IF AVAILABLE hotel-config THEN
    DO:
        IF hotel-config.keynr NE 306 THEN
        DO:
            mess-result = "Invalid key, should be 306, key param is: " + STRING(hotel-config.keynr).
            RETURN.
        END.
        ELSE
        DO:
            CREATE queasy.
            BUFFER-COPY hotel-config TO queasy.
            queasy.KEY = hotel-config.keynr.
            mess-result = "add success".
        END.
    END.
    ELSE
    DO:
        mess-result = "hotel-config is empty!".
        RETURN.
    END.
END.
ELSE IF case-type EQ 2 THEN /*modify*/
DO:
    FIND FIRST hotel-config NO-ERROR.
    IF AVAILABLE hotel-config THEN
    DO:
        IF hotel-config.keynr NE 306 THEN
        DO:
            mess-result = "Invalid key, should be 306, key param is: " + STRING(hotel-config.keynr).
            RETURN.
        END.
        ELSE
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ hotel-config.keynr EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                BUFFER-COPY hotel-config TO queasy.
                mess-result = "modify success".
            END.
            ELSE
            DO:
                CREATE queasy.
                BUFFER-COPY hotel-config TO queasy.
                queasy.KEY = hotel-config.keynr.
                mess-result = "add success".
            END.
        END.
    END.
    ELSE
    DO:
        mess-result = "hotel-config is empty!".
        RETURN.
    END.
END.
ELSE IF case-type EQ 3 THEN /*delete*/
DO:
    FIND FIRST hotel-config NO-ERROR.
    IF AVAILABLE hotel-config THEN
    DO:
        IF hotel-config.keynr NE 306 THEN
        DO:
            mess-result = "Invalid key, should be 306, key param is: " + STRING(hotel-config.keynr).
            RETURN.
        END.
        ELSE
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ hotel-config.keynr EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                DELETE queasy.
                mess-result = "delete success".
            END.
        END.
    END.
    ELSE
    DO:
        mess-result = "hotel-config is empty!".
        RETURN.
    END.
END.
EMPTY TEMP-TABLE hotel-config.
FIND FIRST queasy WHERE queasy.KEY EQ 306 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    CREATE hotel-config.
    BUFFER-COPY queasy TO hotel-config.
    hotel-config.keynr = queasy.KEY.
END.

IF case-type EQ 0 THEN mess-result = "load data success".
