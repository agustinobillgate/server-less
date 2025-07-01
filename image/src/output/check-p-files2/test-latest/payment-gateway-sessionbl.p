DEFINE INPUT PARAMETER resnr             AS INTEGER.
DEFINE INPUT PARAMETER reslinnr          AS INTEGER.
DEFINE INPUT PARAMETER trans-id-merchant AS CHAR.
DEFINE INPUT PARAMETER case-step         AS INTEGER.
DEFINE OUTPUT PARAMETER trans-status     AS CHAR.
DEFINE OUTPUT PARAMETER mess-str         AS CHAR.

IF trans-id-merchant EQ ? THEN trans-id-merchant = "".
IF case-step EQ ? THEN case-step = 0.
IF resnr EQ ? THEN resnr = 0.
IF reslinnr EQ ? THEN reslinnr = 0.

IF trans-id-merchant EQ "" THEN
DO:
    mess-str = "1-Transaction Id Merchant can't be Null".
    RETURN.
END.
IF (case-step NE 2 OR case-step NE 8) THEN
DO:
    mess-str = "3-Wrong Case Step, should be 2 or 8".
    RETURN.
END.
IF resnr EQ 0 THEN
DO:
    mess-str = "5-ResNr can't be Null".
    RETURN.
END.
IF reslinnr EQ 0 THEN
DO:
    mess-str = "6-ReslinNr can't be Null".
    RETURN.
END.

IF case-step EQ 2 THEN
DO :
    FIND FIRST queasy WHERE queasy.KEY EQ 223
    AND queasy.number1 EQ resnr   
    AND queasy.number2 EQ reslinnr
    NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        mess-str = "4-Transaction Already Exist!".
        trans-status = queasy.char1.
        RETURN.
    END.
    ELSE
    DO:
        trans-status = "PENDING".
        CREATE queasy.
        ASSIGN 
        queasy.KEY     = 223
        queasy.number1 = resnr
        queasy.number2 = reslinnr
        queasy.number3 = 1
        queasy.char1   = trans-status /*"PENDING"*/
        queasy.char2   = trans-id-merchant
        queasy.char3   = ""
        .
        mess-str = "0-Operation Success".
        RETURN.
    END.
END.
