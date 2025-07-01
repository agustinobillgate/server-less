/*****************************************
Author      : Fadly Muflih 
Created     : 022/03/2021
Purpose     : Delete Event & Event Detail
*****************************************/

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER block-id     AS CHARACTER.
DEFINE INPUT PARAMETER nr           AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO NO-UNDO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST bk-event WHERE bk-event.block-id EQ block-id
            AND bk-event.nr EQ nr EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE bk-event THEN
        DO:
            FIND FIRST bk-event-detail WHERE bk-event-detail.block-id EQ bk-event.block-id
                AND bk-event-detail.nr EQ bk-event.nr EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE bk-event-detail THEN
            DO:
                DELETE bk-event-detail.
                RELEASE bk-event-detail.
            END.

            DELETE bk-event.
            RELEASE bk-event.
            success-flag = YES.
        END.
    END.
END CASE.
