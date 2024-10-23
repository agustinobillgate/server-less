/*****************************************
AUTHOR      : Irfan Fadhillah
CREATED     : 09 July 2019
PURPOSE     : Insert Events
*****************************************/

DEFINE TEMP-TABLE t-event
    FIELD nr            AS INTEGER
    FIELD blockId       AS CHARACTER
    FIELD startDate     AS DATE
    FIELD endDate       AS DATE
    FIELD packageNr     AS INTEGER
    FIELD packageDesc   AS CHARACTER
    FIELD amount        AS DECIMAL
    FIELD flag          AS CHARACTER
    FIELD gName         AS CHARACTER.

DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER blockID      AS CHARACTER.
DEFINE INPUT PARAMETER TABLE FOR t-event.

DEFINE VARIABLE lastNr  AS INTEGER      NO-UNDO.

FIND LAST bk-event NO-LOCK NO-ERROR.
IF AVAILABLE bk-event THEN
DO:
    lastNr  = bk-event.nr + 1.
END.
ELSE
DO:
    lastNr  = 1.
END.

FIND FIRST t-event NO-ERROR.
IF AVAILABLE t-event THEN
DO:
    CREATE bk-event.
    ASSIGN
        bk-event.nr             = lastNr
        bk-event.block-id       = t-event.blockID
        bk-event.start-date     = t-event.startDate
        bk-event.end-date       = t-event.endDate
        bk-event.package-nr     = 0
        bk-event.bezeich        = t-event.packageDesc
        bk-event.amount         = t-event.amount
        bk-event.flag           = "**"
        bk-event.user-init      = user-init
        bk-event.created-date   = TODAY
    .
END.
