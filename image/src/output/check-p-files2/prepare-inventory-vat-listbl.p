DEFINE TEMP-TABLE invvat-list
    FIELD nr        AS INTEGER
    FIELD bezeich   AS CHAR
    FIELD vat-value AS DECIMAL
    FIELD fibukonto AS CHAR
 .

DEFINE OUTPUT PARAMETER TABLE FOR invvat-list.

FOR EACH queasy WHERE queasy.KEY = 303 NO-LOCK:
    CREATE invvat-list.
    ASSIGN invvat-list.nr           = queasy.number1
           invvat-list.bezeich      = queasy.char1
           invvat-list.vat-value    = queasy.deci1
           invvat-list.fibukonto    = queasy.char2
     .
END.
