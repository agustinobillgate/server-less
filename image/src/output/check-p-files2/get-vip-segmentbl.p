/*** GET VIP SEGMENT LIST : RT - 02/01/2018 ***/

DEFINE TEMP-TABLE t-segment LIKE segment.

DEFINE INPUT PARAMETER inp-gastnr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-segment.
DEFINE OUTPUT PARAMETER segm-code AS INTEGER.
DEFINE OUTPUT PARAMETER segm-bez AS CHAR.

/*
DEF VAR inp-gastnr as int init 5566.
def var segm-code as int.
def var segm-bez as char.
*/
DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999.   

RUN get-vipnrbl.p  
    (OUTPUT vipnr1, OUTPUT vipnr2, OUTPUT vipnr3, OUTPUT vipnr4,  
     OUTPUT vipnr5, OUTPUT vipnr6, OUTPUT vipnr7, OUTPUT vipnr8,  
     OUTPUT vipnr9).  

FIND FIRST guestseg WHERE guestseg.gastnr = inp-gastnr
/*    AND (guestseg.segmentcode = vipnr1 OR   
    guestseg.segmentcode = vipnr2 OR   
    guestseg.segmentcode = vipnr3 OR   
    guestseg.segmentcode = vipnr4 OR   
    guestseg.segmentcode = vipnr5 OR   
    guestseg.segmentcode = vipnr6 OR   
    guestseg.segmentcode = vipnr7 OR   
    guestseg.segmentcode = vipnr8 OR   
    guestseg.segmentcode = vipnr9)*/ NO-LOCK NO-ERROR. 
    
IF NOT AVAILABLE guestseg THEN
DO:
    FOR EACH segment WHERE segment.betriebsnr EQ 3: /* VIP */
        CREATE t-segment.
        BUFFER-COPY segment TO t-segment.
    END.
END.
ELSE IF AVAILABLE guestseg THEN
DO:    
    FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.   
    IF AVAILABLE segment THEN segm-bez = ENTRY(1, segment.bezeich, "$$0").
    
    FOR EACH segment WHERE segment.betriebsnr EQ 3: /* VIP */
        CREATE t-segment.
        BUFFER-COPY segment TO t-segment.
    END.
END.    



