DEFINE INPUT PARAMETER input-username AS CHARACTER.
DEFINE INPUT PARAMETER input-userkey AS CHARACTER.
DEFINE OUTPUT PARAMETER output-ok-flag AS LOGICAL INITIAL NO.
Run check-userkeybl.p(input-username,input-userkey, OUTPUT output-ok-flag).
IF NOT output-ok-flag THEN RETURN.


DEFINE TEMP-TABLE pci-setup
    FIELD number1         AS INT
    FIELD number2         AS INT
    FIELD descr           AS CHAR
    FIELD setupflag       AS LOGICAL
    FIELD price           AS DECIMAL
    .
DEFINE INPUT PARAMETER icase AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR pci-setup.

IF icase EQ 1 THEN
DO:
    FOR EACH queasy WHERE queasy.KEY = 216 NO-LOCK:
        CREATE pci-setup.
        ASSIGN 
            pci-setup.number1         = queasy.number1  
            pci-setup.number2         = queasy.number2  
            pci-setup.descr           = queasy.char3
            pci-setup.setupflag       = queasy.logi1
            pci-setup.price           = queasy.deci1
            .
    END.
END.
ELSE IF icase EQ 2 THEN
DO:
    FOR EACH queasy WHERE queasy.KEY = 216 AND queasy.logi1 EQ YES NO-LOCK:
        CREATE pci-setup.
        ASSIGN 
            pci-setup.number1         = queasy.number1  
            pci-setup.number2         = queasy.number2  
            pci-setup.descr           = queasy.char3
            pci-setup.setupflag       = queasy.logi1
            pci-setup.price           = queasy.deci1
            .
    END.
END.

