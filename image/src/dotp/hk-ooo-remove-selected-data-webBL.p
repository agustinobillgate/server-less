DEFINE TEMP-TABLE om-list 
    FIELD zinr AS CHAR 
    FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID" 
    FIELD ind AS INTEGER INITIAL 0
    . 

DEFINE TEMP-TABLE ooo-list
    FIELD zinr          LIKE outorder.zinr  
    FIELD gespgrund     LIKE outorder.gespgrund  
    FIELD gespstart     LIKE outorder.gespstart  
    FIELD gespende      LIKE outorder.gespende  
    FIELD userinit      AS CHAR  
    FIELD etage         LIKE zimmer.etage  
    FIELD ind           AS INTEGER  
    FIELD bezeich       LIKE zimmer.bezeich  
    FIELD betriebsnr    LIKE outorder.betriebsnr
    FIELD selected-om   AS LOGICAL INITIAL NO
    FIELD rec-id        AS INTEGER
    .

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

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER ci-date      AS DATE.
DEFINE INPUT PARAMETER TABLE FOR ooo-list.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEFINE VARIABLE oos-flag    AS LOGICAL INITIAL NO NO-UNDO.
DEFINE VARIABLE user-nr     AS INTEGER.

IF case-type EQ 1 THEN  /*Off-Market*/
DO:
    FOR EACH ooo-list:
        FIND FIRST outorder WHERE RECID(outorder) EQ ooo-list.rec-id NO-LOCK NO-ERROR.
        IF AVAILABLE outorder THEN
        DO:
            FIND CURRENT outorder EXCLUSIVE-LOCK.
            DELETE outorder.
            RELEASE outorder.
        END.
    END.

    success-flag = YES.
END.
ELSE IF case-type EQ 2 THEN
DO:
    FOR EACH ooo-list2:
        DELETE ooo-list2.
    END.

    FIND FIRST bediener WHERE bediener.userinit EQ userinit NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN user-nr = bediener.nr.

    FOR EACH ooo-list:
        RUN genoooroom-dailybl.p(INPUT ooo-list.zinr, user-init).

        oos-flag = (ooo-list.betriebsnr = 3 OR ooo-list.betriebsnr = 4).

        CREATE ooo-list2.
        ooo-list2.zinr        = ooo-list.zinr.
        ooo-list2.betriebsnr  = ooo-list.betriebsnr.
        ooo-list2.gespstart   = ooo-list.gespstart.
        ooo-list2.gespende    = ooo-list.gespende.

        RUN deactivate-ooo2-cldbl.p(user-nr, oos-flag, ci-date, TABLE ooo-list2).
    END.

    success-flag = YES.
END.
