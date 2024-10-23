/*****************************************
AUTHOR      : Irfan Fadhillah
CREATED     : 16 May 2019
PURPOSE     : Insert & Update Event Catering
*****************************************/

DEFINE TEMP-TABLE t-event
  FIELD blockId         AS CHARACTER
  FIELD startDate       AS DATE
  FIELD endDate         AS DATE
  FIELD packageNr       AS INTEGER
  FIELD userInit        AS CHARACTER.

DEFINE TEMP-TABLE t-bkQueasy
  FIELD nr              AS INTEGER
  FIELD startDate       AS DATE
  FIELD endDate         AS DATE
  FIELD userInit        AS CHARACTER
  FIELD packageNr       AS INTEGER
  FIELD flag            AS CHARACTER
  FIELD key             AS INTEGER
  FIELD number1         AS INTEGER
  FIELD number2         AS INTEGER
  FIELD number3         AS INTEGER
  FIELD char1           AS CHARACTER
  FIELD char2           AS CHARACTER  
  FIELD char3           AS CHARACTER  
  FIELD deci1           AS DECIMAL
  FIELD deci2           AS DECIMAL
  FIELD deci3           AS DECIMAL.

DEFINE INPUT PARAMETER blockId              AS CHARACTER.
DEFINE INPUT PARAMETER caseType             AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR t-event.

DEFINE BUFFER buffQueasy FOR bk-queasy.

DEFINE VARIABLE nr  AS INTEGER NO-UNDO.

FIND LAST bk-event NO-LOCK NO-ERROR.
IF AVAILABLE bk-event THEN
DO:
    nr = bk-event.nr.
END.
ELSE
DO:
    nr = 0.
END.    

FIND FIRST t-event NO-LOCK NO-ERROR.
FIND FIRST bk-queasy WHERE bk-queasy.key EQ 10
    AND bk-queasy.number1 EQ t-event.packageNr NO-LOCK NO-ERROR.
IF AVAILABLE bk-queasy THEN 
DO:            
    FOR EACH buffQueasy WHERE buffQueasy.key EQ 11
        AND buffQueasy.number2 EQ bk-queasy.number1:            
        
        nr = nr + 1.           
        CREATE t-bkQueasy.
        ASSIGN 
            t-bkQueasy.nr           = nr            
            t-bkQueasy.startDate    = t-event.startDate
            t-bkQueasy.endDate      = t-event.endDate
            t-bkQueasy.userInit     = t-event.userInit
            t-bkQueasy.packageNr    = t-event.packageNr 
            t-bkQueasy.flag         = "**"
            t-bkQueasy.key          = buffQueasy.key
            t-bkQueasy.number1      = buffQueasy.number1
            t-bkQueasy.number2      = buffQueasy.number2
            t-bkQueasy.number3      = buffQueasy.number3
            t-bkQueasy.char1        = buffQueasy.char1
            t-bkQueasy.char2        = buffQueasy.char2 + " [" + ENTRY(1, bk-queasy.char2, "|") + "]"
            t-bkQueasy.char3        = buffQueasy.char3
            t-bkQueasy.deci1        = buffQueasy.deci1
            t-bkQueasy.deci2        = buffQueasy.deci2
            t-bkQueasy.deci3        = buffQueasy.deci3.          
    END.    
END.

IF caseType EQ 1 THEN
DO:
    FOR EACH t-bkQueasy:        
        FIND FIRST bk-event WHERE bk-event.block-id EQ blockId
            AND bk-event.nr EQ t-bkQueasy.nr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bk-event THEN 
        DO:
            CREATE bk-event.
            ASSIGN 
                bk-event.nr             = t-bkQueasy.nr
                bk-event.block-id       = blockId
                bk-event.amount         = t-bkQueasy.deci1                
                bk-event.package-nr     = t-bkQueasy.packageNr                
                bk-event.start-date     = t-bkQueasy.startDate
                bk-event.end-date       = t-bkQueasy.endDate
                bk-event.user-init      = t-bkQueasy.userInit
                bk-event.created-date   = TODAY
                bk-event.bezeich        = t-bkQueasy.char2
                bk-event.flag           = t-bkQueasy.flag.   
        END.    
    END.
END.
ELSE IF caseType EQ 2 THEN 
DO:
    FIND FIRST t-event NO-LOCK NO-ERROR.
    FIND FIRST bk-event WHERE bk-event.block-id EQ blockId
        AND bk-event.nr EQ t-event.packageNr EXCLUSIVE-LOCK NO-ERROR. /*for deleting bk-event, packageNr mean bk-event.nr*/
    IF AVAILABLE bk-event THEN 
    DO:
        DELETE bk-event.
        RELEASE bk-event.
    END.    
END.
