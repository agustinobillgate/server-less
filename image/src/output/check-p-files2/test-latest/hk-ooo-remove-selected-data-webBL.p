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
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO. /*Alder Debug*/

DEFINE VARIABLE oos-flag    AS LOGICAL INITIAL NO NO-UNDO.
DEFINE VARIABLE user-nr     AS INTEGER.
DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(23)" NO-UNDO. /*william C2CAD7*/
stat-list[1]  = "Vacant Clean Checked". 
stat-list[2]  = "Vacant Clean Unchecked". 
stat-list[3]  = "Vacant Dirty". 
stat-list[4]  = "Expected Departure". 
stat-list[5]  = "Occupied Dirty". 
stat-list[6]  = "Occupied Cleaned". 
stat-list[7]  = "Out-of-Order". 
stat-list[8]  = "Off-Market". 
stat-list[9]  = "Do not Disturb". 
stat-list[10] = "Out-of-Service".

IF case-type EQ 1 THEN  /*Off-Market*/
DO:
    FOR EACH ooo-list: 
        FIND FIRST outorder WHERE RECID(outorder) EQ ooo-list.rec-id NO-LOCK NO-ERROR.
        FIND FIRST zimmer WHERE zimmer.zinr EQ outorder.zinr NO-LOCK NO-ERROR.
        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE outorder THEN
        DO:     
            CREATE res-history. 
            ASSIGN 
              res-history.nr = bediener.nr 
              res-history.datum = TODAY 
              res-history.zeit = TIME 
              res-history.aenderung = "Room " + zimmer.zinr 
                 + " Status Changed From " 
                 + STRING(zimmer.zistatus) + " Off-Market" + " to " + STRING(zimmer.zistatus) + " " + stat-list[zimmer.zistatus + 1]
              res-history.action = "HouseKeeping". 
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history.

            FIND CURRENT outorder EXCLUSIVE-LOCK.           
            DELETE outorder.
            RELEASE outorder.          
        END.
    END.

    success-flag = YES. /*Alder Debug*/
END.
ELSE IF case-type EQ 2 THEN
DO:
    FOR EACH ooo-list2:
        DELETE ooo-list2.
    END.

    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR. /* malik serverless: WHERE bediener.userinit EQ userinit -> WHERE bediener.userinit EQ user-init */
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

    success-flag = YES. /*Alder Debug*/
END.
