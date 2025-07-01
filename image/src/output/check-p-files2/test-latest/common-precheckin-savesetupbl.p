DEFINE INPUT PARAMETER input-username AS CHARACTER.
DEFINE INPUT PARAMETER input-userkey AS CHARACTER.
DEFINE OUTPUT PARAMETER output-ok-flag AS LOGICAL INITIAL NO.
Run check-userkeybl.p(input-username,input-userkey, OUTPUT output-ok-flag).
IF NOT output-ok-flag THEN RETURN.


DEFINE TEMP-TABLE pci-setup
    FIELD number1         AS INT
    FIELD number2         AS INT
    FIELD number3         AS INT
    FIELD descr           AS CHAR
    FIELD setupflag       AS LOGICAL
    FIELD price           AS DECIMAL
    .
DEFINE INPUT PARAMETER TABLE FOR pci-setup.
FOR EACH pci-setup BY pci-setup.number1:
    DO TRANSACTION:
        FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ pci-setup.number1 
        AND queasy.number2 EQ pci-setup.number2 EXCLUSIVE-LOCK NO-ERROR.
        CASE pci-setup.number1:
            WHEN 1 THEN 
            DO:
                IF pci-setup.number2 EQ 99 THEN
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag
                        queasy.char3 = pci-setup.descr
                        .
                END.
                ELSE
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag.     
                END.
            END.
            WHEN 2 THEN 
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag
                    queasy.deci1 = pci-setup.price.
            END.
            WHEN 3 THEN 
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag.
            END.
            WHEN 4 THEN 
            DO:
                IF pci-setup.number2 EQ 99 THEN
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag
                        queasy.char3 = pci-setup.descr.
                END.
                ELSE
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag.     
                END.
            END.
            WHEN 5 THEN 
            DO:
                IF pci-setup.number2 EQ 99 THEN
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag
                        queasy.char3 = pci-setup.descr.
                END.
                ELSE
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag.     
                END.
            END.
            WHEN 6 THEN 
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag
                    queasy.char3 = pci-setup.descr.
            END.
            WHEN 7 THEN  
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag
                    queasy.char3 = pci-setup.descr.
            END.
            OTHERWISE .
        END CASE.
    END.
END.
