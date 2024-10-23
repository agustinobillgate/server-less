DEFINE INPUT PARAMETER mode         AS INTEGER. /* 0 = Create | 1 = Delete */
DEFINE INPUT PARAMETER blockId      AS CHARACTER.
DEFINE INPUT PARAMETER strAmendment AS CHARACTER.
DEFINE INPUT PARAMETER userInit     AS CHARACTER.

IF mode EQ 0 THEN
DO:
    FIND FIRST bk-amendment WHERE bk-amendment.blockId EQ blockId EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE bk-amendment THEN
    DO:
        IF ENTRY(1, strAmendment, "|") NE "" THEN
        DO:
            CREATE bk-amendment.
            ASSIGN
                bk-amendment.blockId            = blockId
                bk-amendment.strAmendment       = strAmendment
                bk-amendment.userInit           = userInit.
        END.       
    END.
    ELSE
    DO:
        IF ENTRY(1, strAmendment, "|") EQ "" THEN 
        DO:
            DELETE bk-amendment.            
        END.
        ELSE
        DO:
            ASSIGN
                bk-amendment.blockId            = blockId
                bk-amendment.strAmendment       = strAmendment
                bk-amendment.userInit           = userInit.            
        END.
    END.
    
    RELEASE bk-amendment.
END.
ELSE IF mode EQ 1 THEN
DO:
    FIND FIRST bk-amendment WHERE bk-amendment.blockId EQ blockId EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE bk-amendment THEN
    DO:
        DELETE bk-amendment.
    END.
    
    RELEASE bk-amendment.
END.
