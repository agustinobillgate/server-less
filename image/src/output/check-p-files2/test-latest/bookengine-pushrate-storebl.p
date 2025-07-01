/********************************************************************
Author  : Irfan Fadhillah
Date    : 03 Agustus 2018
Purpose : Store Manually UpDATE Rates AND Delete Setting
********************************************************************/
DEFINE TEMP-TABLE updQ
 FIELD ratecode     AS CHARACTER
 FIELD VHPRates     AS DECIMAL
 FIELD BERates      AS DECIMAL
 FIELD datum        AS DATE
 FIELD user-init    AS CHARACTER
 FIELD sysDATE      AS DATE
 FIELD systime      AS INTEGER.
  
DEFINE INPUT PARAMETER booken-selected AS INTEGER no-undo.
DEFINE INPUT PARAMETER TABLE FOR updQ.
DEFINE INPUT PARAMETER mode AS INTEGER.

DEFINE VARIABLE prevRates   AS DECIMAL.

/***********************************************************
    Mode
    1 = insert
    2 = delete setting
***********************************************************/    

IF mode EQ 1 THEN
DO:
    /*for log*/
    FOR EACH updQ:
        FIND FIRST queasy WHERE queasy.key EQ 201
            AND queasy.number1 EQ 5
            AND queasy.DATE1 EQ updQ.datum NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN
             queasy.key     = 201
             queasy.number1 = 5
             queasy.number2 = booken-selected
             queasy.number3 = updQ.sysTime         
             queasy.char1   = updQ.ratecode
             queasy.char2   = updQ.user-init
             queasy.deci1   = updQ.VHPRates
             queasy.DATE1   = updQ.datum
             queasy.DATE2   = updQ.sysDATE
             queasy.deci2   = 0
             queasy.deci3   = updQ.BERates.
        END.            
        ELSE
        DO:
            prevRates = queasy.deci3.
            CREATE queasy.
            ASSIGN
             queasy.key     = 201
             queasy.number1 = 5
             queasy.number2 = booken-selected
             queasy.number3 = updQ.sysTime           
             queasy.char1   = updQ.ratecode
             queasy.char2   = updQ.user-init
             queasy.deci1   = updQ.VHPRates
             queasy.DATE1   = updQ.datum
             queasy.DATE2   = updQ.sysDATE
             queasy.deci2   = prevRates
             queasy.deci3   = updQ.BERates.         
        END.       
    END.
    
    /*delete setting with same DATE*/
    FOR EACH updQ:
        FIND FIRST queasy WHERE queasy.key EQ 201
            AND queasy.number1 EQ 6
            AND queasy.DATE1 EQ updQ.datum
            AND queasy.char1 EQ updQ.rateCode NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
        END.    
    END.
    
    /*for setting*/
    FOR EACH updQ:
        CREATE queasy.
        ASSIGN
         queasy.key     = 201
         queasy.number1 = 6
         queasy.number2 = booken-selected
         queasy.number3 = updQ.sysTime
         queasy.char1   = updQ.ratecode
         queasy.char2   = updQ.user-init
         queasy.deci1   = updQ.VHPRates
         queasy.DATE1   = updQ.datum
         queasy.DATE2   = updQ.sysDATE
         queasy.deci2   = 0
         queasy.deci3   = updQ.BERates.
    END.
END.
ELSE IF mode EQ 2 THEN
DO:
    FOR EACH updQ:
        FIND FIRST queasy WHERE queasy.key EQ 201
            AND queasy.number1 EQ 6
            AND queasy.number2 EQ booken-selected
            AND queasy.DATE1 EQ updQ.datum EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
        END.            
    END.
END.
