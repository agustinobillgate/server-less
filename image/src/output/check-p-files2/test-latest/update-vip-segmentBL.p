/*** UPDATE VIP SEGMENT : RT - 02/01/2018 ***/

DEFINE INPUT PARAMETER inp-gastnr AS INTEGER.
DEFINE INPUT PARAMETER inp-segmcode AS INTEGER.

DEFINE TEMP-TABLE gsegm-list LIKE segment.
DEFINE TEMP-TABLE hsegm-list LIKE segment.

DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999.   

DEFINE VARIABLE vip-flag1 AS LOGICAL.
DEFINE VARIABLE vip-flag2 AS LOGICAL INITIAL NO.
DEFINE VARIABLE vip-segm AS INTEGER INITIAL 0.

DEFINE VARIABLE prev-segm AS INTEGER.

RUN get-vipnrbl.p  
    (OUTPUT vipnr1, OUTPUT vipnr2, OUTPUT vipnr3, OUTPUT vipnr4,  
     OUTPUT vipnr5, OUTPUT vipnr6, OUTPUT vipnr7, OUTPUT vipnr8,  
     OUTPUT vipnr9).  


FOR EACH guestseg WHERE guestseg.gastnr EQ inp-gastnr:
    DELETE guestseg.
END.

/*DELETE*/
IF inp-segmcode EQ 0 THEN
DO:
    FIND FIRST guestseg WHERE guestseg.gastnr EQ inp-gastnr NO-ERROR.
    IF AVAILABLE guestseg THEN
    DO:
        DELETE guestseg.
    END.
	
	FOR EACH res-line WHERE res-line.gastnrmember = inp-gastnr 
		AND res-line.active-flag LE 1:
		res-line.betrieb-gastmem = 0.
	END.
END.

/*CREATE NEW RECORD*/
FIND FIRST segment WHERE segment.segmentcode = inp-segmcode NO-ERROR.
IF AVAILABLE segment THEN
DO:
    CREATE guestseg.
    guestseg.gastnr = inp-gastnr.
    guestseg.segmentcode = inp-segmcode.
    guestseg.reihenfolge = 1.
END.

/*UPDATE*/
FIND FIRST guestseg WHERE guestseg.gastnr = inp-gastnr NO-ERROR.
IF AVAILABLE guestseg THEN
DO:
	prev-segm = guestseg.segmentcode.
	IF prev-segm NE inp-segmcode THEN
	DO:
		UPDATE guestseg.segmentcode = inp-segmcode.
	END.
END.

FIND FIRST segment WHERE segment.segmentcode = inp-segmcode NO-LOCK NO-ERROR.    
IF AVAILABLE segment THEN
DO:
    vip-flag2 = YES.
	IF (inp-segmcode = vipnr1 OR
		inp-segmcode = vipnr2 OR 
		inp-segmcode = vipnr3 OR 
		inp-segmcode = vipnr4 OR 
		inp-segmcode = vipnr5 OR 
		inp-segmcode = vipnr6 OR 
		inp-segmcode = vipnr7 OR 
		inp-segmcode = vipnr8 OR 
		inp-segmcode = vipnr9) THEN
	DO:
		vip-segm = segment.segmentcode.
	END.
END.     

FOR EACH segment WHERE segment.vip-level = 0
    AND NUM-ENTRIES(segment.bezeich, "$$0") = 1 NO-LOCK:
    CREATE hsegm-list.
    BUFFER-COPY segment TO hsegm-list.    
END.    

FOR EACH guestseg WHERE guestseg.gastnr = inp-gastnr:
    FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode.
    CREATE gsegm-list.
    gsegm-list.segmentcode = segment.segmentcode.
    gsegm-list.bezeich = segment.bezeich.
    
    FIND FIRST hsegm-list WHERE
        hsegm-list.segmentcode = gsegm-list.segmentcode NO-ERROR.
    IF AVAILABLE hsegm-list THEN DELETE hsegm-list.    
END.

FIND FIRST gsegm-list WHERE   
 (gsegm-list.segmentcode = vipnr1 OR   
  gsegm-list.segmentcode = vipnr2 OR   
  gsegm-list.segmentcode = vipnr3 OR   
  gsegm-list.segmentcode = vipnr4 OR   
  gsegm-list.segmentcode = vipnr5 OR   
  gsegm-list.segmentcode = vipnr6 OR   
  gsegm-list.segmentcode = vipnr7 OR   
  gsegm-list.segmentcode = vipnr8 OR   
  gsegm-list.segmentcode = vipnr9) NO-LOCK NO-ERROR.   
IF AVAILABLE gsegm-list THEN vip-flag1 = YES.   
    

IF vip-flag1 /*NE vip-flag2*/ THEN
DO:
    FIND FIRST res-line WHERE res-line.gastnrmember = inp-gastnr
        AND res-line.active-flag LE 1 NO-ERROR.
    DO WHILE AVAILABLE res-line:
        FIND CURRENT res-line EXCLUSIVE-LOCK.
        res-line.betrieb-gastmem = vip-segm.
        FIND CURRENT res-line NO-LOCK.
        FIND NEXT res-line WHERE res-line.gastnrmember = inp-gastnr
            AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
    END.    
END.






