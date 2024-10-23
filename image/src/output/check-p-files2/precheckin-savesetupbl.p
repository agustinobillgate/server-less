DEFINE TEMP-TABLE pci-setup
    FIELD number1         AS INT                     LABEL "MAIN GROUP"
    FIELD number2         AS INT                     LABEL "SUB GROUP"
    FIELD descr           AS CHAR    FORMAT "x(35)"  LABEL "DESCRIPTION"
    FIELD setupvalue      AS CHAR    FORMAT "x(84)"  LABEL "SETUP VALUE"
    FIELD setupflag       AS LOGICAL                 LABEL "SETUP FLAG"
    FIELD price           AS DECIMAL                 LABEL "DECIMAL VALUE"
    FIELD remarks         AS CHAR
    .

DEFINE INPUT PARAMETER TABLE FOR pci-setup.
DEFINE OUTPUT PARAMETER mess-str AS CHAR.

DEFINE BUFFER bqueasy FOR queasy.

FOR EACH pci-setup BY pci-setup.number1:
    DO TRANSACTION:
        FIND FIRST queasy WHERE queasy.KEY EQ 216 
            AND queasy.number1 EQ pci-setup.number1 
            AND queasy.number2 EQ pci-setup.number2 EXCLUSIVE-LOCK NO-ERROR.
        CASE pci-setup.number1:
            WHEN 1 THEN /*DEFAULT PURPOSE OF STAY*/
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag
                    queasy.char3 = pci-setup.setupvalue.
            END.
            WHEN 2 THEN /*PICKUP REQUEST*/
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag
                    queasy.deci1 = pci-setup.price.
            END.
            WHEN 3 THEN /*ROOM PREFERENCE*/
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag.
            END.
            WHEN 4 THEN /*BGCOLOR SELECTION*/
            DO:
                IF pci-setup.number2 EQ 99 THEN
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag
                        queasy.char3 = pci-setup.setupvalue.

                        FIND FIRST bqueasy WHERE bqueasy.KEY EQ 216 
                        AND bqueasy.number1 EQ 4 
                        AND bqueasy.number2 EQ 1 EXCLUSIVE-LOCK NO-ERROR.
                        ASSIGN bqueasy.logi1 = NO.
                END.
                ELSE
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag
                        queasy.char3 = pci-setup.setupvalue.

                        FIND FIRST bqueasy WHERE bqueasy.KEY EQ 216 
                        AND bqueasy.number1 EQ 4 
                        AND bqueasy.number2 EQ 99 EXCLUSIVE-LOCK NO-ERROR.
                        ASSIGN bqueasy.logi1 = NO.   
                END.
            END.
            WHEN 5 THEN /*FGCOLOR SELECTION*/
            DO:
                IF pci-setup.number2 EQ 99 THEN
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag
                        queasy.char3 = pci-setup.setupvalue.

                        FIND FIRST bqueasy WHERE bqueasy.KEY EQ 216 
                        AND bqueasy.number1 EQ 5 
                        AND bqueasy.number2 EQ 1 EXCLUSIVE-LOCK NO-ERROR.
                        ASSIGN bqueasy.logi1 = NO.
                END.
                ELSE
                DO:
                    ASSIGN
                        queasy.logi1 = pci-setup.setupflag
                        queasy.char3 = pci-setup.setupvalue.

                        FIND FIRST bqueasy WHERE bqueasy.KEY EQ 216 
                        AND bqueasy.number1 EQ 5 
                        AND bqueasy.number2 EQ 99 EXCLUSIVE-LOCK NO-ERROR.
                        ASSIGN bqueasy.logi1 = NO.   
                END.
            END.
            WHEN 6 THEN /*TERM AND CONDITION*/
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag
                    queasy.char3 = pci-setup.setupvalue.
            END.
            WHEN 7 THEN  /*IMAGE HOTEL URL*/
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag
                    queasy.char3 = pci-setup.setupvalue.
            END.
            WHEN 8 THEN /*FLAG UPLOAD IMAGE*/
            DO:
                ASSIGN
                    queasy.logi1 = pci-setup.setupflag.
            END.
            OTHERWISE .
        END CASE.
    END.
END.

mess-str = "Setup Updated Successfully".

