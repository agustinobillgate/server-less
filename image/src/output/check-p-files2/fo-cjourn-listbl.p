
DEFINE TEMP-TABLE output-list 
    FIELD STR AS CHAR.

DEFINE TEMP-TABLE cjourn-list
    FIELD artnr       AS INTEGER    FORMAT ">>>>>"
    FIELD bezeich     AS CHARACTER  FORMAT "x(24)"
    FIELD dept        AS CHARACTER  FORMAT "x(16)"
    FIELD datum       AS DATE       
    FIELD zinr        AS CHARACTER  FORMAT "x(8)"
    FIELD rechnr      AS INTEGER    FORMAT ">>>>>>>>>"
    FIELD canc-reason AS CHARACTER  FORMAT "x(24)"
    FIELD qty         AS INTEGER    FORMAT "->>>>"
    FIELD amount      AS DECIMAL    FORMAT "->,>>>,>>>,>>9.99"
    FIELD zeit        AS CHARACTER  FORMAT "x(5)"
    FIELD ID          AS CHARACTER  FORMAT "x(3)"
    .

/**/
DEFINE INPUT PARAMETER from-art     AS INTEGER.
DEFINE INPUT PARAMETER to-art       AS INTEGER.
DEFINE INPUT PARAMETER from-dept    AS INTEGER.
DEFINE INPUT PARAMETER to-dept      AS INTEGER.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER foreign-flag AS LOGICAL.
DEFINE INPUT PARAMETER long-digit   AS LOGICAL.

DEFINE OUTPUT PARAMETER TABLE FOR cjourn-list.

/*
DEFINE VARIABLE from-art     AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE to-art       AS INTEGER NO-UNDO INITIAL 99999.
DEFINE VARIABLE from-dept    AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE to-dept      AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE from-date    AS DATE    NO-UNDO INITIAL 01/13/19.
DEFINE VARIABLE to-date      AS DATE    NO-UNDO INITIAL 01/13/19.
DEFINE VARIABLE foreign-flag AS LOGICAL NO-UNDO INITIAL NO.
DEFINE VARIABLE long-digit   AS LOGICAL NO-UNDO INITIAL NO.
*/
RUN fo-cjournbl.p(from-art, to-art, from-dept, to-dept, from-date, 
    to-date, foreign-flag, long-digit, OUTPUT TABLE output-list).

FOR EACH cjourn-list:
    DELETE cjourn-list.
END.

FOR EACH output-list:
    CREATE cjourn-list.
    ASSIGN
        cjourn-list.artnr       = INTEGER(SUBSTRING(output-list.STR, 40, 5))
        cjourn-list.bezeich     = SUBSTRING(output-list.STR, 45, 24)
        cjourn-list.dept        = SUBSTRING(output-list.STR, 9, 16)
        cjourn-list.datum       = DATE(SUBSTRING(output-list.STR, 1, 8))
        cjourn-list.zinr        = SUBSTRING(output-list.STR, 25, 6)
        cjourn-list.rechnr      = INTEGER(SUBSTRING(output-list.STR, 31, 9))
        cjourn-list.canc-reason = SUBSTRING(output-list.STR, 69, 74)
        cjourn-list.qty         = INTEGER(SUBSTRING(output-list.STR, 93, 5))
        cjourn-list.amount      = DECIMAL(SUBSTRING(output-list.STR, 148, 17))
        cjourn-list.zeit        = SUBSTRING(output-list.STR, 165, 5)
        cjourn-list.ID          = SUBSTRING(output-list.STR, 170, 3)
        .
END.       

