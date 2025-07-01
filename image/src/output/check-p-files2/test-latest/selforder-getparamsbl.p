DEFINE TEMP-TABLE selforder-setup
    FIELD nr AS INT
    FIELD setup-keyword AS CHAR
    FIELD setup-value AS CHAR
    .

DEFINE INPUT PARAMETER session-parameter AS CHAR.
DEFINE OUTPUT PARAMETER department-number AS INT.
DEFINE OUTPUT PARAMETER table-no AS INT.
DEFINE OUTPUT PARAMETER guest-name AS CHAR.
DEFINE OUTPUT PARAMETER pax AS INT.
DEFINE OUTPUT PARAMETER room AS CHAR.
DEFINE OUTPUT PARAMETER checkin-date AS CHAR.
DEFINE OUTPUT PARAMETER checkout-date AS CHAR.
DEFINE OUTPUT PARAMETER package AS CHAR.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.
DEFINE OUTPUT PARAMETER session-expired AS LOGICAL INIT YES.
DEFINE OUTPUT PARAMETER TABLE FOR selforder-setup. 

IF session-parameter EQ "" OR session-parameter EQ ? THEN
DO:
    session-parameter = "1-session-parameter cannot be empty!".
    RETURN.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 230 AND queasy.char1 EQ session-parameter NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    ASSIGN 
        department-number = queasy.number1
        table-no          = queasy.number2
        guest-name        = queasy.char2
        pax               = queasy.number3
        checkin-date      = ENTRY(2,queasy.char3,"|")
        checkout-date     = ENTRY(3,queasy.char3,"|")
        package           = ENTRY(4,queasy.char3,"|")
        room              = ENTRY(1,queasy.char3,"|")
        session-expired   = queasy.logi1
        .
END.
ELSE
DO:
    session-parameter = "2-data not found, please check your session!".
    RETURN.
END.

FOR EACH queasy WHERE queasy.KEY EQ 222 AND queasy.number1 EQ 1 NO-LOCK BY queasy.number2:
    CREATE selforder-setup.
    ASSIGN
    selforder-setup.nr            = queasy.number2. 
    selforder-setup.setup-keyword = queasy.char1. 
    IF queasy.number3 EQ 1 THEN selforder-setup.setup-value = STRING(queasy.char2).
    ELSE IF queasy.number3 EQ 2 THEN selforder-setup.setup-value = STRING(queasy.deci1).
    ELSE IF queasy.number3 EQ 3 THEN selforder-setup.setup-value = STRING(queasy.date1).
    ELSE IF queasy.number3 EQ 4 THEN selforder-setup.setup-value = STRING(queasy.logi1).
    ELSE IF queasy.number3 EQ 5 THEN selforder-setup.setup-value = STRING(queasy.char2).
    ELSE IF queasy.number3 EQ 6 THEN selforder-setup.setup-value = STRING(queasy.char2).
END.
mess-result = "0-get param success".
