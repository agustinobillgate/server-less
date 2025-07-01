DEFINE TEMP-TABLE input-list
    FIELD guestno         AS INT
    FIELD first-name      AS CHARACTER 
    FIELD last-name       AS CHARACTER  
    FIELD country         AS CHARACTER 
    FIELD city            AS CHARACTER 
    FIELD segment         AS CHARACTER 
    FIELD keyaccount      AS CHARACTER 
    .

DEFINE INPUT PARAMETER TABLE FOR input-list.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.

DEF VAR i         AS INT.
DEF VAR keynumber AS INT.
DEF VAR ans       AS LOGICAL.
DEFINE BUFFER ilist FOR input-list.
DEFINE BUFFER q212 FOR queasy.

FIND FIRST ilist NO-ERROR.
IF AVAILABLE ilist THEN
DO:
    FOR EACH input-list WHERE input-list.keyaccount NE "":
        FIND FIRST queasy WHERE queasy.KEY EQ 211 
        AND queasy.char1 MATCHES ("*" + input-list.keyaccount + "*") NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            i = 1.
            keynumber = queasy.number1.
            FOR EACH q212 WHERE q212.KEY EQ 212 AND q212.number1 EQ keynumber BY q212.number2 DESC:
                i = q212.number2 + 1.
                IF i EQ 0 THEN i = 1.
                LEAVE.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 212 AND queasy.number3 EQ input-list.guestno EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                CREATE queasy.
                ASSIGN 
                 queasy.KEY      = 212
                 queasy.number1  = keynumber
                 queasy.number2  = i
                 queasy.char1    = input-list.last-name
                 queasy.number3  = input-list.guestno.
            END. 
            ELSE 
            DO:  
                 queasy.number1  = keynumber.
            END.
        END.
    END.
    mess-result = "Import Data Success".
END.
ELSE 
DO:
    mess-result = "Please load data first, press ENTER in CSV Delimiter".
END.



