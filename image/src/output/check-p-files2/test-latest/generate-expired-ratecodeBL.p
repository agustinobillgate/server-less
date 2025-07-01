DEFINE TEMP-TABLE output-list
    FIELD ratecode  AS CHARACTER FORMAT "x(15)"
    FIELD bezeich   AS CHARACTER FORMAT "x(30)"
    FIELD remarks   AS CHARACTER FORMAT "x(20)".

DEFINE INPUT PARAMETER fdate AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE BUFFER bratecode FOR ratecode.

FOR EACH queasy WHERE KEY EQ 2 BY char1.
    FIND FIRST ratecode WHERE ratecode.CODE EQ queasy.char1 NO-ERROR.
    IF AVAILABLE ratecode THEN
    DO:
        FIND FIRST bratecode WHERE bratecode.CODE EQ queasy.char1
            AND bratecode.endperiode GE fdate NO-ERROR.
        IF NOT AVAILABLE bratecode THEN 
        DO:
            CREATE output-list.
            ASSIGN
                output-list.ratecode = queasy.char1
                output-list.bezeich  = queasy.char2
                output-list.remarks  = "Expired Rate".
        END.
    END.
    IF NOT AVAILABLE ratecode THEN
    DO:
        CREATE output-list.
        ASSIGN
            output-list.ratecode = queasy.char1
            output-list.bezeich  = queasy.char2
            output-list.remarks  = "Empty Rate".
    END.
END.
