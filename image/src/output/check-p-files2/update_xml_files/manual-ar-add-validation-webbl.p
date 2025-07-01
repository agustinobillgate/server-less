/* Oscar - E00833 - Add validation to prevent duplicate AR Manual Reference No */

DEFINE TEMP-TABLE payload-list
    FIELD refno AS CHARACTER.

DEFINE TEMP-TABLE response-list
    FIELD success-flag AS LOGICAL
    FIELD err-msg      AS CHARACTER.

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR response-list.

DEFINE VARIABLE refno AS CHARACTER.

CREATE response-list.
response-list.success-flag = YES.

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        refno    = payload-list.refno
    .

    FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno EQ refno NO-LOCK NO-ERROR.
    IF AVAILABLE gl-jouhdr THEN
    DO:
        response-list.success-flag = NO.
        response-list.err-msg = "Reference Number already used".
        RETURN.
    END.

    FIND FIRST gl-jhdrhis WHERE gl-jhdrhis.refno EQ refno NO-LOCK NO-ERROR.
    IF AVAILABLE gl-jhdrhis THEN
    DO:
        response-list.success-flag = NO.
        response-list.err-msg = "Reference Number already used".
        RETURN.
    END.
END.
ELSE
DO:
    response-list.success-flag = NO.
END.
