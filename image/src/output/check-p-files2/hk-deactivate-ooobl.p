/*
MESSAGE "DEBUG hk-deactivate-ooobl.p - Start"
    VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug - Ticket C2CAD7*/
*/

DEFINE TEMP-TABLE om-list 
    FIELD zinr AS CHAR 
    FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID" 
    FIELD ind AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE ooo-list2
    FIELD zinr       AS CHARACTER
    FIELD gespgrund  AS CHARACTER  
    FIELD gespstart  AS DATE 
    FIELD gespende   AS DATE 
    FIELD userinit   AS CHARACTER
    FIELD etage      AS INTEGER 
    FIELD ind        AS INTEGER
    FIELD bezeich    AS CHARACTER 
    FIELD betriebsnr AS INTEGER
    FIELD selected-om AS LOGICAL INITIAL NO. 

DEFINE INPUT PARAMETER userinit AS CHAR.
DEFINE INPUT PARAMETER rec-id AS INTEGER.
/*
DEFINE INPUT PARAMETER zinr AS CHAR.
DEFINE INPUT PARAMETER betriebsnr AS INTEGER.
*/
DEFINE VARIABLE ci-date AS DATE.
DEFINE VARIABLE oos-flag AS LOGICAL.
DEFINE VARIABLE user-nr AS INTEGER.

FIND FIRST bediener WHERE bediener.userinit EQ userinit NO-LOCK.

FIND FIRST outorder WHERE RECID(outorder) EQ rec-id NO-LOCK NO-ERROR.

IF AVAILABLE bediener AND AVAILABLE outorder THEN
DO:
    user-nr = bediener.nr.
    
    oos-flag = (outorder.betriebsnr EQ 3 OR outorder.betriebsnr EQ 4).    
    
    FOR EACH queasy WHERE queasy.KEY EQ 195 AND
        queasy.char1 EQ "ooo;room=" + outorder.zinr + 
        ";from=" + STRING(DAY(outorder.gespstart),"99") + "/" + 
                   STRING(MONTH(outorder.gespstart),"99") + "/" +
                   STRING(YEAR(outorder.gespstart),"9999") +
        ";to=" +   STRING(DAY(outorder.gespende),"99") + "/" + 
                   STRING(MONTH(outorder.gespende),"99") + "/" +
                   STRING(YEAR(outorder.gespende),"9999") EXCLUSIVE-LOCK.
        
        FIND FIRST guestbook WHERE guestbook.gastnr EQ queasy.number1 EXCLUSIVE-LOCK.
        IF AVAILABLE guestbook THEN
        DO:
            DELETE guestbook.
        END.
        
        DELETE queasy.
    END.
    
    CREATE ooo-list2.
    ooo-list2.zinr        = outorder.zinr.
    ooo-list2.betriebsnr  = outorder.betriebsnr.
    ooo-list2.gespstart   = outorder.gespstart.
    ooo-list2.gespende    = outorder.gespende.

    RUN htpdate.p (87, OUTPUT ci-date).

    /*
    MESSAGE "DEBUG hk-deactivate-ooobl.p -> RUN deactivate-ooo2-cldbl.p - Start"
    VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug - Ticket C2CAD7*/
    */

    /*
    MESSAGE "ooo-list2.betriebsnr : " ooo-list2.betriebsnr
        VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug - Ticket C2CAD7*/
    */

    /*RUN deactivate-ooo2-cldbl.p (user-nr, oos-flag, ci-date, TABLE ooo-list2).*/  /*Alder Debug - Ticket C2CAD7*/
    RUN deactivate-ooo2_1-cldbl.p (user-nr, oos-flag, ci-date, TABLE ooo-list2).      /*Alder - Ticket C2CAD7*/

    /*
    MESSAGE "DEBUG hk-deactivate-ooobl.p -> RUN deactivate-ooo2-cldbl.p - End"
    VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug - Ticket C2CAD7*/
    */
END.

/*
MESSAGE "DEBUG hk-deactivate-ooobl.p - End"
    VIEW-AS ALERT-BOX INFO BUTTONS OK. /*Alder Debug - Ticket C2CAD7*/
*/
