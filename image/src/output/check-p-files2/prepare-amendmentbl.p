DEFINE INPUT PARAMETER blockId          AS CHARACTER.
DEFINE OUTPUT PARAMETER amendmentStr    AS CHARACTER.


FIND FIRST bk-amendment WHERE bk-amendment.blockId EQ blockId NO-LOCK NO-ERROR.
IF AVAILABLE bk-amendment THEN
DO:
    amendmentStr        = bk-amendment.strAmendment.
END.
