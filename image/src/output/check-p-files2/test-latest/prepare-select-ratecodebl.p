DEFINE TEMP-TABLE t-ratecode
  FIELD code        as CHARACTER
  FIELD bez         as CHARACTER
  FIELD startDate   as DATE
  FIELD endDate     as DATE
  FIELD zikatnr     as INTEGER
  FIELD roomType    as CHARACTER
  FIELD argt        as CHARACTER.
  
DEFINE INPUT PARAMETER gastnr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-ratecode.  

DEFINE VARIABLE i       AS INTEGER      NO-UNDO INITIAL 0.
DEFINE VARIABLE rCode   AS CHARACTER    NO-UNDO.
DEFINE VARIABLE rmType  AS CHARACTER    NO-UNDO.

/*IF 170519
FOR EACH guest-pr WHERE guest-pr.gastnr EQ gastnr:
    FOR EACH ratecode WHERE ratecode.code EQ guest-pr.code:

        FIND FIRST zimkateg WHERE INTEGER(zimkateg.zikatnr) EQ ratecode.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN 
        DO:
            ASSIGN 
                rmType = zimkateg.kurzbez.
        END.    
        
        FIND FIRST arrangement WHERE arrangement.argtnr EQ ratecode.argtnr NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN
        DO:
            ASSIGN 
                t-ratecode.argt = arrangement.arrangement.
        END.        
        
        FIND FIRST t-ratecode WHERE t-ratecode.code EQ ratecode.code
            AND t-ratecode.roomType EQ roomType NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-ratecode THEN
        DO:            
            CREATE t-ratecode.
            ASSIGN 
                t-ratecode.code         = ratecode.code
                t-ratecode.bez          = ratecode.bezeichnung
                t-ratecode.startDate    = ratecode.startperiod
                t-ratecode.endDate      = ratecode.endperiod
                t-ratecode.zikatnr      = ratecode.zikatnr
                t-ratecode.roomType     = rmType.
        END.    
    END.
END.
END IF*/

/**/
FIND FIRST htparam WHERE htparam.paramnr EQ 1020 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN 
DO:
    IF NUM-ENTRIES(htparam.fchar, ";") GT 1 THEN 
    DO:
        DO i = 1 TO NUM-ENTRIES(htparam.fchar, ";"):
            rCode = ENTRY(i, htparam.fchar, ";").
            
            FIND FIRST ratecode WHERE ratecode.code EQ rCode NO-LOCK NO-ERROR.
            IF AVAILABLE ratecode THEN 
            DO:
                CREATE t-ratecode.
                ASSIGN 
                    t-ratecode.code         = rCode
                    t-ratecode.bez          = ratecode.bezeichnung
                    t-ratecode.startDate    = ratecode.startperiod
                    t-ratecode.endDate      = ratecode.endperiod
                    t-ratecode.zikatnr      = ratecode.zikatnr.
                FIND FIRST zimkateg WHERE INTEGER(zimkateg.zikatnr) EQ ratecode.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN 
                DO:
                    ASSIGN 
                        t-ratecode.roomType = zimkateg.kurzbez.
                END.    
                
                FIND FIRST arrangement WHERE arrangement.argtnr EQ ratecode.argtnr NO-LOCK NO-ERROR.
                IF AVAILABLE arrangement THEN
                DO:
                    ASSIGN 
                        t-ratecode.argt = arrangement.arrangement.
                END.
            END.            
        END.
    END.
END.
/**/

/*
FOR EACH guest-pr WHERE guest-pr.gastnr EQ gastnr:
    FIND FIRST ratecode WHERE ratecode.code EQ guest-pr.code NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN
    DO:
        CREATE t-ratecode.
        ASSIGN
            t-ratecode.code         = guest-pr.code
            t-ratecode.bez          = ratecode.bezeichnung
            t-ratecode.startDate    = ratecode.startperiod
            t-ratecode.endDate      = ratecode.endperiod
            t-ratecode.zikatnr      = ratecode.zikatnr.
        
        FIND FIRST zimkateg WHERE INTEGER(zimkateg.zikatnr) EQ ratecode.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN
        DO:
            ASSIGN
                t-ratecode.roomType = zimkateg.kurzbez.
        END.   
        
        FIND FIRST arrangement WHERE arrangement.argtnr EQ ratecode.argtnr NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN
        DO:
            ASSIGN
                t-ratecode.argt     = arrangement.arrangement.
        END.
    END.
END.
*/
