/******************************************
Author          : Irfan Fadhillah
Created Date    : 23 May 2019
Purpose         : Insert & Update Event Data
******************************************/
DEFINE TEMP-TABLE t-event
    FIELD blockId       AS CHARACTER
    FIELD counter       AS INTEGER
    FIELD nr            AS INTEGER
    FIELD eventType     AS CHARACTER
    FIELD eventStatus   AS CHARACTER
    FIELD eventName     AS CHARACTER
    FIELD startDate     AS DATE
    FIELD endDate       AS DATE
    FIELD startTime     AS CHARACTER
    FIELD endTime       AS CHARACTER
    FIELD atendees      AS INTEGER
    FIELD minGuaranteed AS INTEGER
    FIELD actual        AS INTEGER
    FIELD venue         AS CHARACTER
    FIELD setup         AS CHARACTER
    FIELD amount        AS DECIMAL.    

DEFINE INPUT PARAMETER blockId      AS CHARACTER.
DEFINE INPUT PARAMETER TABLE FOR t-event.
DEFINE OUTPUT PARAMETER okFlag      AS LOGICAL.

DEFINE VARIABLE counter     AS INTEGER NO-UNDO.
DEFINE VARIABLE i           AS INTEGER NO-UNDO.
DEFINE VARIABLE s-time      AS INTEGER NO-UNDO.
DEFINE VARIABLE e-time      AS INTEGER NO-UNDO.

FIND LAST bk-event-detail USE-INDEX counter_ix NO-LOCK NO-ERROR.
IF AVAILABLE bk-event-detail THEN 
DO:
    counter = bk-event-detail.counter + 1.
END.
ELSE
DO:
    counter = 1.
END.

FIND FIRST t-event NO-LOCK NO-ERROR.
IF AVAILABLE t-event THEN
DO:
    s-time   = (INTEGER(ENTRY(1, t-event.startTime, ":")) * 3600) + (INTEGER(ENTRY(2, t-event.startTime, ":")) * 60).
    e-time = (INTEGER(ENTRY(1, t-event.endTime, ":")) * 3600) + (INTEGER(ENTRY(2, t-event.endTime, ":")) * 60).
END.

RUN checkVenue.

IF NOT okFlag THEN RETURN.

FIND FIRST bk-event-detail WHERE bk-event-detail.block-id EQ blockId
    /*AND bk-event-detail.start-date EQ t-event.startDate*/
    AND bk-event-detail.nr EQ t-event.nr NO-ERROR.
IF AVAILABLE bk-event-detail THEN 
DO:
    ASSIGN 
        bk-event-detail.block-id        = blockId
        bk-event-detail.event-type      = t-event.eventType
        bk-event-detail.event-status    = t-event.eventStatus
        bk-event-detail.event-name      = t-event.eventName
        bk-event-detail.start-date      = t-event.startDate
        bk-event-detail.end-date        = t-event.endDate
        bk-event-detail.start-time      = s-time  
        bk-event-detail.end-time        = e-time
        bk-event-detail.atendees        = t-event.atendees 
        bk-event-detail.min-guaranteed  = t-event.minGuaranteed
        bk-event-detail.actual          = t-event.actual
        bk-event-detail.venue           = t-event.venue
        bk-event-detail.setup           = t-event.setup
        bk-event-detail.nr              = t-event.nr
        bk-event-detail.amount          = t-event.amount.
    okFlag = YES.    
END.
ELSE
DO:
    CREATE bk-event-detail.
    ASSIGN 
        bk-event-detail.counter         = counter        
        bk-event-detail.block-id        = blockId        
        bk-event-detail.event-type      = t-event.eventType       
        bk-event-detail.event-status    = t-event.eventStatus        
        bk-event-detail.event-name      = t-event.eventName        
        bk-event-detail.start-date      = t-event.startDate
        bk-event-detail.end-date        = t-event.endDate        
        bk-event-detail.start-time      = s-time  
        bk-event-detail.end-time        = e-time
        bk-event-detail.atendees        = t-event.atendees
        bk-event-detail.min-guaranteed  = t-event.minGuaranteed
        bk-event-detail.actual          = t-event.actual
        bk-event-detail.venue           = t-event.venue
        bk-event-detail.setup           = t-event.setup        
        bk-event-detail.nr              = t-event.nr
        bk-event-detail.amount          = t-event.amount.
        
    okFlag = YES.
END.

/*FIND FIRST t-event NO-LOCK NO-ERROR.*/
IF AVAILABLE t-event THEN
DO:
    FIND FIRST bk-event WHERE bk-event.block-id EQ blockID 
        AND bk-event.nr EQ t-event.nr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE bk-event THEN
    DO:
        ASSIGN
            bk-event.start-date = t-event.startDate
            bk-event.end-date   = t-event.endDate.
    END.    
    FIND CURRENT bk-event NO-LOCK.
    RELEASE bk-event.
END.

PROCEDURE checkVenue:
    DEFINE VARIABLE startDate       AS DATE         NO-UNDO.
    DEFINE VARIABLE endDate         AS DATE         NO-UNDO.
    
    FIND FIRST t-event NO-LOCK NO-ERROR.
    IF AVAILABLE t-event THEN
    DO:
        ASSIGN
            startDate       = t-event.startDate
            endDate         = t-event.endDate.
    END.    

    FIND FIRST bk-event-detail WHERE ((bk-event-detail.start-date GE t-event.startDate AND bk-event-detail.start-date LE t-event.endDate) OR
        (bk-event-detail.end-date GE t-event.startDate AND bk-event-detail.end-date LE t-event.endDate) OR
        (bk-event-detail.start-date LE t-event.startDate AND bk-event-detail.end-date GE t-event.endDate))
        AND bk-event-detail.venue EQ t-event.venue
        AND ((s-time GE bk-event-detail.start-time AND s-time LE bk-event-detail.end-time) OR
            (e-time GE bk-event-detail.start-time AND e-time LE bk-event-detail.end-time ) OR 
            (s-time LE bk-event-detail.start-time AND e-time GE bk-event-detail.end-time)) NO-ERROR.
    DO WHILE AVAILABLE bk-event-detail:
        IF bk-event-detail.block-id NE blockId THEN
        DO:
            okFlag = NO.   
            
            RETURN.         
        END.
        ELSE
        DO:            
            IF bk-event-detail.nr NE t-event.nr THEN
            DO:
                okFlag = NO.
                RETURN.
            END.
            ELSE
            DO:
                okFlag = YES.
            END.
        END.
        
        FIND NEXT bk-event-detail WHERE ((bk-event-detail.start-date GE t-event.startDate AND bk-event-detail.start-date LE t-event.endDate) OR
            (bk-event-detail.end-date GE t-event.startDate AND bk-event-detail.end-date LE t-event.endDate) OR
            (bk-event-detail.start-date LE t-event.startDate AND bk-event-detail.end-date GE t-event.endDate))
            AND bk-event-detail.venue EQ t-event.venue
            AND ((s-time GE bk-event-detail.start-time AND s-time LE bk-event-detail.end-time) OR
                (e-time GE bk-event-detail.start-time AND e-time LE bk-event-detail.end-time ) OR 
                (s-time LE bk-event-detail.start-time AND e-time GE bk-event-detail.end-time)) NO-ERROR.        
    END.
    
    okFlag = YES.

/*    
    FIND FIRST bk-event-detail WHERE bk-event-detail.start-date EQ currDate
        AND bk-event-detail.venue EQ t-event.venue
        AND ((s-time GE bk-event-detail.start-time AND s-time LE bk-event-detail.end-time) OR
            (e-time GE bk-event-detail.start-time AND e-time LE bk-event-detail.end-time ) OR 
            (s-time LE bk-event-detail.start-time AND e-time GE bk-event-detail.end-time)) NO-ERROR.
    IF AVAILABLE bk-event-detail THEN
    DO:
        IF bk-event-detail.block-id NE blockId THEN
        DO:
            okFlag = NO.   
            
            RETURN.         
        END.
        ELSE
        DO:            
            IF bk-event-detail.nr NE t-event.nr THEN
            DO:
                okFlag = NO.
                RETURN.
            END.
            ELSE
            DO:
                okFlag = YES.
            END.
        END.
    END.        
    ELSE
    DO:
        okFlag = YES.        
    END.
*/    

END PROCEDURE.
