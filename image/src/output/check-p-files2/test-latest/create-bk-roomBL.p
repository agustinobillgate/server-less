DEFINE TEMP-TABLE t-bk-room
    FIELD resnr           AS INTEGER      FORMAT "->,>>>,>>9"
    FIELD resttype        AS INTEGER      FORMAT "->,>>>,>>9"
    FIELD pax             AS INTEGER      FORMAT "->,>>>,>>9"
    FIELD cutoffdate      AS DATE         FORMAT "99/99/9999"
    FIELD followupdate    AS DATE         FORMAT "99/99/9999"
    FIELD depositduedate  AS DATE         FORMAT "99/99/9999"
    FIELD salesID         AS CHARACTER    FORMAT "x(8)"
    FIELD res-char        AS CHARACTER    FORMAT "x(50)"          EXTENT 9
    FIELD res-int         AS INTEGER      FORMAT "->,>>>,>>9"     EXTENT 9
    FIELD res-dec         AS DECIMAL      FORMAT "->>,>>9.99"     EXTENT 9
    FIELD block-id        AS CHARACTER    FORMAT "x(8)"
    FIELD block-code      AS CHARACTER    FORMAT "x(8)"
    FIELD trace-code      AS CHARACTER    FORMAT "x(8)"
    FIELD ratecode        AS CHARACTER    FORMAT "x(8)"
    FIELD cutoffdays      AS INTEGER      FORMAT "->,>>>,>>9"
    FIELD fo-resnr        AS INTEGER      FORMAT "->,>>>,>>9"
    FIELD fo-reslinne     AS INTEGER
    FIELD ankunft         AS DATE 
    FIELD abreise         AS DATE
    FIELD cancellation-no AS CHARACTER 
    FIELD reason          AS CHARACTER 
    FIELD comments        AS CHARACTER           
    FIELD destination     AS CHARACTER   
    FIELD property        AS CHARACTER   
    FIELD cancel-penalty  AS DECIMAL.    
    
DEFINE INPUT PARAMETER casetype       AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR t-bk-room.

/*
DEFINE INPUT PARAMETER resno          AS INTEGER.
DEFINE INPUT PARAMETER blockcode      AS INTEGER.
DEFINE INPUT PARAMETER resttype       AS INTEGER.
DEFINE INPUT PARAMETER pax            AS INTEGER.
DEFINE INPUT PARAMETER cutoffdate     AS DATE.
DEFINE INPUT PARAMETER followupdate   AS DATE.
DEFINE INPUT PARAMETER depositduedate AS DATE.
DEFINE INPUT PARAMETER tracecode      AS INTEGER.
DEFINE INPUT PARAMETER cuttoffdays    AS INTEGER.
DEFINE INPUT PARAMETER salesID        AS CHARACTER.
*/

IF casetype EQ 1 THEN
DO:
    FIND FIRST t-bk-room NO-LOCK NO-ERROR.   
    IF AVAILABLE t-bk-room THEN 
    DO:
        FIND FIRST bk-room WHERE bk-room.resnr EQ t-bk-room.resnr EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE bk-room THEN 
        DO:
            CREATE bk-room.
            ASSIGN 
                bk-room.resnr           = t-bk-room.resnr
                bk-room.block-code      = t-bk-room.block-code
                bk-room.block-id        = t-bk-room.block-id
                bk-room.resttype        = t-bk-room.resttype
                bk-room.pax             = t-bk-room.pax 
                bk-room.ratecode        = t-bk-room.ratecode   
                bk-room.cutoffdate      = t-bk-room.cutoffdate
                bk-room.followupdate    = t-bk-room.followupdate
                bk-room.depositduedate  = t-bk-room.depositduedate
                bk-room.trace-code      = t-bk-room.trace-code
                bk-room.cutoffdays      = t-bk-room.cutoffdays   
                bk-room.salesID         = t-bk-room.salesID
                bk-room.cancellation-no = t-bk-room.cancellation-no
                bk-room.reason          = t-bk-room.reason
                bk-room.comments        = t-bk-room.comments
                bk-room.destination     = t-bk-room.destination
                bk-room.property        = t-bk-room.property
                bk-room.cancel-penalty  = t-bk-room.cancel-penalty.
        END.
        ELSE 
        DO:
            ASSIGN 
                bk-room.resttype        = t-bk-room.resttype
                bk-room.pax             = t-bk-room.pax 
                bk-room.ratecode        = t-bk-room.ratecode   
                bk-room.cutoffdate      = t-bk-room.cutoffdate
                bk-room.followupdate    = t-bk-room.followupdate
                bk-room.depositduedate  = t-bk-room.depositduedate
                bk-room.trace-code      = t-bk-room.trace-code
                bk-room.cutoffdays      = t-bk-room.cutoffdays   
                bk-room.salesID         = t-bk-room.salesID
                bk-room.cancellation-no = t-bk-room.cancellation-no
                bk-room.reason          = t-bk-room.reason
                bk-room.comments        = t-bk-room.comments
                bk-room.destination     = t-bk-room.destination
                bk-room.property        = t-bk-room.property
                bk-room.cancel-penalty  = t-bk-room.cancel-penalty.
        END.
    END.
END.

