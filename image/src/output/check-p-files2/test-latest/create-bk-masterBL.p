DEFINE TEMP-TABLE t-bk-master
   FIELD resnr                      AS INTEGER      
   FIELD gastnr                     AS INTEGER      
   FIELD name                       AS CHARACTER      
   FIELD startDATE                  AS DATE      
   FIELD endDATE                    AS DATE      
   FIELD resstatus                  AS INTEGER      
   FIELD market-nr                  AS INTEGER      
   FIELD source-nr                  AS INTEGER      
   FIELD sales-nr                   AS INTEGER      
   FIELD restype                    AS INTEGER      
   FIELD origins                    AS INTEGER      
   FIELD sob                        AS INTEGER      
   FIELD catering-flag              AS LOGICAL      
   FIELD room-flag                  AS LOGICAL      
   FIELD cancel-flag                AS LOGICAL     EXTENT 2
   FIELD cancel-type                AS CHARACTER      
   FIELD cancel-reason              AS CHARACTER      
   FIELD cancel-destination         AS CHARACTER      
   FIELD cancel-property            AS CHARACTER      
   FIELD res-CHARACTER              AS CHARACTER   EXTENT 9
   FIELD res-int                    AS INTEGER     EXTENT 9
   FIELD res-dec                    AS DECIMAL     EXTENT 9
   FIELD block-id                   AS CHARACTER      
   FIELD block-code                 AS CHARACTER      
   FIELD reservation-method         AS CHARACTER      
   FIELD rooming-list-due           AS DATE      
   FIELD arrival-time               AS INTEGER      
   FIELD departure-time             AS INTEGER      
   FIELD payment                    AS CHARACTER      
   FIELD cancel-penalty             AS DECIMAL.   
 
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
        
DEFINE TEMP-TABLE t-bk-catering
    FIELD block-id             AS CHARACTER
    FIELD attendees            AS INTEGER    
    FIELD guaranteedFlag       AS LOGICAL    
    FIELD info                 AS CHARACTER  
    FIELD cutoff-date          AS DATE       
    FIELD deposit-due          AS DATE       
    FIELD function-name        AS CHARACTER  
    FIELD contract-no          AS CHARACTER  
    FIELD sales-nr             AS INTEGER    
    FIELD str-status           AS CHARACTER
    FIELD cancellation-no      AS CHARACTER
    FIELD reason               AS CHARACTER
    FIELD comments             AS CHARACTER
    FIELD amounPax             AS DECIMAL 
    FIELD totalAmount          AS DECIMAL.
    
DEFINE INPUT PARAMETER casetype     AS INTEGER.
DEFINE INPUT PARAMETER name         AS CHARACTER.          
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER TABLE        FOR t-bk-master. 
DEFINE INPUT PARAMETER TABLE        FOR t-bk-room. 
DEFINE INPUT PARAMETER TABLE        FOR t-bk-catering.

DEFINE VARIABLE resnr AS INTEGER NO-UNDO.  
           
/*Commented by IF on 180419
DEFINE INPUT PARAMETER gastnr             AS INTEGER.
DEFINE INPUT PARAMETER name               AS CHARACTER.
DEFINE INPUT PARAMETER startdate          AS DATE.
DEFINE INPUT PARAMETER enddate            AS DATE.
DEFINE INPUT PARAMETER resstatus          AS INTEGER.
DEFINE INPUT PARAMETER marketnr           AS INTEGER.
DEFINE INPUT PARAMETER sourcenr           AS INTEGER.
DEFINE INPUT PARAMETER salesnr            AS INTEGER.
DEFINE INPUT PARAMETER restype            AS INTEGER.
DEFINE INPUT PARAMETER origins            AS INTEGER.
DEFINE INPUT PARAMETER sob                AS INTEGER.
DEFINE INPUT PARAMETER cateringflag       AS LOGICAL.
DEFINE INPUT PARAMETER cancelflag         AS LOGICAL.
DEFINE INPUT PARAMETER canceltype         AS CHARACTER.
DEFINE INPUT PARAMETER cancelreason       AS CHARACTER.
DEFINE INPUT PARAMETER canceldestination  AS CHARACTER.
DEFINE INPUT PARAMETER cancelproperty     AS CHARACTER.
DEFINE INPUT PARAMETER cancelpenalty      AS CHARACTER.
*/

DEFINE VARIABLE bk-count AS INTEGER     NO-UNDO.
DEFINE VARIABLE oriStr   AS CHARACTER   NO-UNDO.
DEFINE VARIABLE chgStr   AS CHARACTER   NO-UNDO.

bk-count = 0.
FIND LAST bk-master NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN 
DO:
    bk-count = bk-master.resnr + 1.
END.
ELSE 
DO:
    bk-count = 1.
END.

IF casetype EQ 1 THEN
DO:
    FIND FIRST t-bk-master NO-LOCK NO-ERROR.
    IF AVAILABLE t-bk-master THEN 
    DO:
        FIND FIRST bk-master WHERE bk-master.block-id EQ t-bk-master.block-id NO-ERROR.
        IF NOT AVAILABLE bk-master THEN 
        DO:
            CREATE bk-master.
            ASSIGN 
                bk-master.block-id              = t-bk-master.block-id
                bk-master.block-code            = t-bk-master.block-code
                bk-master.resnr                 = bk-count           
                bk-master.gastnr                = t-bk-master.gastnr           
                bk-master.name                  = name             
                bk-master.startdate             = t-bk-master.startdate        
                bk-master.enddate               = t-bk-master.enddate          
                bk-master.resstatus             = t-bk-master.resstatus        
                bk-master.market-nr             = t-bk-master.market-nr 
                bk-master.source-nr             = t-bk-master.source-nr             
                bk-master.sales-nr              = t-bk-master.sales-nr          
                bk-master.restype               = t-bk-master.restype          
                bk-master.origins               = t-bk-master.origins          
                bk-master.catering-flag         = t-bk-master.catering-flag
                bk-master.reservation-method    = t-bk-master.reservation-method
                bk-master.rooming-list-due      = t-bk-master.rooming-list-due
                bk-master.arrival-time          = t-bk-master.arrival-time
                bk-master.departure-time        = t-bk-master.departure-time
                bk-master.payment               = t-bk-master.payment.
            
            /*Assign resnr into bk-room*/
            FIND FIRST t-bk-room EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE t-bk-room THEN
            DO:
                ASSIGN 
                    t-bk-room.resnr     = bk-count
                    t-bk-room.block-id  = t-bk-master.block-id.
                RELEASE t-bk-room.                    
            END.   
            
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN 
            DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.action      = "Banquet"
                res-history.aenderung   = "Create Master Plan With Block ID " + t-bk-master.block-id.                            
            END.                      
            
            RUN create-bk-roombl.p(1, TABLE t-bk-room).         
        END.
        ELSE 
        DO:     
            ASSIGN 
                chgStr  = ""
                oriStr  = ""
                resnr   = bk-master.resnr.
            
            IF bk-master.gastnr NE t-bk-master.gastnr THEN 
            DO:
                ASSIGN
                    oriStr = STRING(bk-master.gastnr) + ";"
                    chgStr = STRING(t-bk-master.gastnr) + ";".
            END.
            ELSE IF bk-master.startdate NE t-bk-master.startdate THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.startdate, "99/99/9999") + ";"
                    chgStr = chgStr + STRING(t-bk-master.startdate, "99/99/9999") + ";".
            END.
            ELSE IF bk-master.enddate NE t-bk-master.enddate THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.enddate, "99/99/9999") + ";"
                    chgStr = chgStr + STRING(t-bk-master.enddate, "99/99/9999") + ";".                
            END.
            ELSE IF bk-master.resstatus NE t-bk-master.resstatus THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.resstatus) + ";"
                    chgStr = chgStr + STRING(t-bk-master.resstatus) + ";".                
            END.
            ELSE IF bk-master.market-nr NE t-bk-master.market-nr THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.market-nr) + ";"
                    chgStr = chgStr + STRING(t-bk-master.market-nr) + ";".
            END.
            ELSE IF bk-master.source-nr NE t-bk-master.source-nr THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.source-nr) + ";"
                    chgStr = chgStr + STRING(t-bk-master.source-nr) + ";".
            END.
            ELSE IF bk-master.sales-nr NE t-bk-master.sales-nr THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.sales-nr) + ";"
                    chgStr = chgStr + STRING(t-bk-master.sales-nr) + ";".
            END.
            ELSE IF bk-master.restype NE t-bk-master.restype THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.restype) + ";"
                    chgStr = chgStr + STRING(t-bk-master.restype) + ";".
            END.            
            ELSE IF bk-master.origins NE t-bk-master.origins THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.origins) + ";"
                    chgStr = chgStr + STRING(t-bk-master.origins) + ";".
            END.
            ELSE IF bk-master.catering-flag NE t-bk-master.catering-flag THEN 
            DO:
                ASSIGN
                    oriStr = oriStr + STRING(bk-master.catering-flag) + ";"
                    chgStr = chgStr + STRING(t-bk-master.catering-flag) + ";".
            END.
                        
            ASSIGN 
                bk-master.gastnr                = t-bk-master.gastnr           
                bk-master.name                  = name             
                bk-master.startdate             = t-bk-master.startdate        
                bk-master.enddate               = t-bk-master.enddate          
                bk-master.resstatus             = t-bk-master.resstatus        
                bk-master.market-nr             = t-bk-master.market-nr 
                bk-master.source-nr             = t-bk-master.source-nr             
                bk-master.sales-nr              = t-bk-master.sales-nr          
                bk-master.restype               = t-bk-master.restype          
                bk-master.origins               = t-bk-master.origins          
                bk-master.catering-flag         = t-bk-master.catering-flag
                bk-master.reservation-method    = t-bk-master.reservation-method
                bk-master.rooming-list-due      = t-bk-master.rooming-list-due
                bk-master.arrival-time          = t-bk-master.arrival-time
                bk-master.departure-time        = t-bk-master.departure-time
                bk-master.payment               = t-bk-master.payment.
            
            FIND FIRST t-bk-room EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE t-bk-room THEN 
            DO:
                ASSIGN 
                    t-bk-room.resnr     = resnr.
                
                RELEASE t-bk-room.    
            END.    
            
            RUN create-bk-roombl.p(1, TABLE t-bk-room).                     
        END.
    END.
    
    FIND FIRST t-bk-catering NO-LOCK NO-ERROR.
    IF AVAILABLE t-bk-catering THEN
    DO:     
        FIND FIRST bk-catering WHERE bk-catering.block-id EQ t-bk-catering.block-id EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE bk-catering THEN
        DO:
            CREATE bk-catering.
            BUFFER-COPY t-bk-catering TO bk-catering.
            
            RELEASE bk-catering.
        END.
        ELSE
        DO:
            BUFFER-COPY t-bk-catering TO bk-catering.
            
            RELEASE bk-catering.
        END.
    END.
END.


