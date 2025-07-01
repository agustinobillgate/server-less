DEFINE TEMP-TABLE mess-list 
    FIELD nr AS INTEGER 
    FIELD mess-recid AS INTEGER.

DEFINE TEMP-TABLE t-messages LIKE messages
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE mess-data 
    FIELD gname         AS CHARACTER   
    FIELD arrival       AS DATE   
    FIELD depart        AS DATE   
    FIELD zinr          AS CHARACTER   
    FIELD pguest        AS LOGICAL
    FIELD nr            AS INTEGER   
    FIELD tot           AS INTEGER     
    FIELD username      AS CHARACTER
    FIELD messText      AS CHARACTER
    FIELD currTime      AS CHARACTER
    FIELD caller        AS CHARACTER
    FIELD phoneNo       AS CHARACTER
    FIELD currDate      AS DATE    
    .

DEFINE INPUT  PARAMETER gastnr      AS INTEGER.
DEFINE INPUT  PARAMETER resnr       AS INTEGER.
DEFINE INPUT  PARAMETER reslinnr    AS INTEGER.
DEFINE INPUT  PARAMETER v-key       AS CHARACTER.   /*PREPARATION;DEL;DEACTIVE*/
DEFINE INPUT  PARAMETER v-deactive  AS LOGICAL.     /*Button Deactive Messages Lamp*/
DEFINE OUTPUT PARAMETER v-success   AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-messages.
DEFINE OUTPUT PARAMETER TABLE FOR mess-list.
DEFINE OUTPUT PARAMETER TABLE FOR mess-data.

DEFINE VARIABLE gname       AS CHARACTER.
DEFINE VARIABLE arrival     AS DATE.
DEFINE VARIABLE depart      AS DATE.
DEFINE VARIABLE zinr        AS CHARACTER.
DEFINE VARIABLE pguest      AS LOGICAL.
DEFINE VARIABLE nr          AS INTEGER.
DEFINE VARIABLE tot         AS INTEGER.
DEFINE VARIABLE num         AS INTEGER.
DEFINE VARIABLE username    AS CHARACTER.
DEFINE VARIABLE mess-text   AS CHARACTER.
DEFINE VARIABLE curr-time   AS CHARACTER.
DEFINE VARIABLE caller      AS CHARACTER.
DEFINE VARIABLE rufnr       AS CHARACTER.
DEFINE VARIABLE curr-date   AS DATE.

RUN prepare-messagesbl.p
    (gastnr, resnr, reslinnr, OUTPUT gname, OUTPUT arrival,
    OUTPUT depart, OUTPUT zinr, OUTPUT pguest).

IF v-key EQ "DEL" OR v-key EQ "DEACTIVE" THEN
DO:
    RUN init-var(YES).
    IF v-deactive THEN RUN messages-update-reslinebl.p(t-messages.resnr, t-messages.reslinnr).
END.    
ELSE
DO:
    RUN init-var(NO).
END.

CREATE mess-data.
ASSIGN
    mess-data.gname      = gname      
    mess-data.arrival    = arrival  
    mess-data.depart     = depart   
    mess-data.zinr       = zinr     
    mess-data.pguest     = pguest   
    mess-data.nr         = nr       
    mess-data.tot        = tot      
    mess-data.username   = username 
    mess-data.messText   = mess-text
    mess-data.currTime   = curr-time
    mess-data.caller     = caller   
    mess-data.phoneNo    = rufnr    
    mess-data.currDate   = curr-date
    .

/*************************************** PROCEDURES ***************************************/
PROCEDURE init-var: 
    DEFINE INPUT PARAMETER if-flag AS LOGICAL. 
  
    RUN messages-init-varbl.p(if-flag, gastnr, resnr, reslinnr, OUTPUT nr, OUTPUT tot,
                              OUTPUT TABLE mess-list).
    
    mess-text = "". 
    curr-date = ?. 
    curr-time = "". 
    username = "". 
    caller = "". 
    rufnr = "". 
    
    /*IF tot = 0 THEN DISABLE btn-mess WITH FRAME frame1.*/
    
    IF v-key EQ "FIRST" THEN
    DO:
        RUN get-messages(1).
        nr = 1.
    END.        
    ELSE IF v-key MATCHES("*NEXT*") THEN
    DO:        
        num = INT(SUBSTRING(v-key,5)).
        RUN get-messages(num + 1).
        nr = num + 1.
    END.        
    ELSE IF v-key MATCHES("*PREV*") THEN
    DO:
        num = INT(SUBSTRING(v-key,5)).
        RUN get-messages(num - 1).
        nr = num - 1.
    END.   
    ELSE IF v-key MATCHES("*DEACTIVE*") THEN
    DO:
        num = INT(SUBSTRING(v-key,9)).
        RUN get-messages(num).
    END.
    ELSE RUN get-messages(nr). 
END. 

PROCEDURE get-messages: 
    DEFINE INPUT PARAMETER i AS INTEGER. 
    /*ASSIGN mess-text:BGCOLOR IN FRAME frame1 = 8.*/ 
    IF i LT 1 THEN RETURN. 
    ELSE IF i GT tot THEN RETURN. 
    ELSE IF tot = 0 THEN RETURN. 
    ELSE DO: 
        nr = i. 
        FIND FIRST mess-list WHERE mess-list.nr = i.
        RUN messages-get-messagebl.p(mess-list.mess-recid, OUTPUT username, OUTPUT TABLE t-messages).
        FIND FIRST t-messages.
        
        mess-text = t-messages.messtext[1]. 
        caller = t-messages.messtext[2]. 
        rufnr = t-messages.messtext[3]. 
        curr-date = t-messages.datum. 
        curr-time = STRING(t-messages.zeit, "HH:MM:SS"). 
        /*
        IF t-messages.betriebsnr = 0 THEN ENABLE btn-mess WITH FRAME frame1. 
        ELSE DISABLE btn-mess WITH FRAME frame1. 
        */
    END. 
END. 
