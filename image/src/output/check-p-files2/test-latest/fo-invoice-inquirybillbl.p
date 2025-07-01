DEFINE VARIABLE pvILanguage AS INTEGER INIT 1.
{supertransBL.i}

DEFINE TEMP-TABLE t-bill LIKE bill
    FIELD bl-recid      AS INTEGER.
DEFINE TEMP-TABLE t-billhis LIKE billhis.

DEFINE VARIABLE lvCAREA AS CHAR INITIAL "". 
DEFINE INPUT PARAMETER inq-bill AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str AS CHARACTER.

DEFINE VARIABLE str         AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE done        AS LOGICAL.
DEFINE VARIABLE bill-exist  AS LOGICAL.

RUN read-bill1bl.p (1, inq-bill, ?,?,?,?,?,?,?,?, OUTPUT TABLE t-bill).
FIND FIRST t-bill NO-ERROR.
IF NOT AVAILABLE t-bill AND inq-bill NE 0 THEN 
DO: 
    RUN read-billhisbl.p (1, inq-bill, ?,?, OUTPUT bill-exist, OUTPUT TABLE t-billhis).
    FIND FIRST t-billhis NO-ERROR.
    IF AVAILABLE t-billhis THEN
    DO:
        IF t-billhis.resnr > 0 AND t-billhis.reslinnr = 0 THEN 
            str = translateExtended ("1Master Bill History found.",lvCAREA,"").
        ELSE IF t-billhis.resnr > 0 AND t-billhis.reslinnr > 0  THEN 
            str = translateExtended ("1Hotel Guest Bill History found.",lvCAREA,"").
        ELSE 
            str = translateExtended ("1Non Stay Guest Bill History found.",lvCAREA,"").

        msg-str = str.
        RETURN.
    END.
    ELSE
    DO:
        msg-str = translateExtended ("No such bill number.",lvCAREA,"").
    END.
END. 
ELSE IF AVAILABLE t-bill AND t-bill.flag = 0 THEN 
DO: 
    IF t-bill.resnr = 0 THEN 
    DO: 
        msg-str = translateExtended ("Non-stay Guest Bill - Status: active.",lvCAREA,"").  
        RETURN. 
    END. 
    ELSE IF t-bill.resnr GT 0 AND t-bill.reslinnr = 0 THEN 
    DO: 
        msg-str = translateExtended ("Master Bill - Status: active.",lvCAREA,""). 
        RETURN. 
    END. 
    ELSE IF t-bill.resnr GT 0 AND t-bill.reslinnr GT 0 THEN 
    DO: 
        msg-str = translateExtended ("Hotel Guest Bill - Status: active.",lvCAREA,""). 
        RETURN. 
    END. 
END. 
ELSE IF AVAILABLE t-bill AND t-bill.flag = 1 THEN 
DO: 
    IF t-bill.resnr = 0 THEN 
    DO: 
        msg-str = translateExtended ("Non-stay Guest Bill - Status: closed.",lvCAREA,""). 
        RETURN. 
    END. 
    ELSE IF t-bill.resnr GT 0 AND t-bill.reslinnr = 0 THEN 
    DO: 
        msg-str = translateExtended ("Master Bill - Status: closed.",lvCAREA,""). 
        RETURN. 
    END. 
    ELSE IF t-bill.resnr GT 0 AND t-bill.reslinnr GT 0 THEN 
    DO: 
        msg-str =  translateExtended ("Hotel Guest Bill - Status: closed.",lvCAREA,"").
        RETURN. 
    END. 
END. 
 
