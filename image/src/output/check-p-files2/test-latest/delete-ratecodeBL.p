DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER int1         AS INTEGER.
DEF INPUT PARAMETER user-init    AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL  NO-UNDO INITIAL NO.

DEFINE VARIABLE prcode          AS CHAR NO-UNDO.
DEFINE VARIABLE RmType          AS CHAR NO-UNDO.
/*naufal 231219 - add variable for deleting linked child*/
DEFINE VARIABLE chcode          AS CHAR NO-UNDO.
DEFINE VARIABLE startperiode    AS DATE NO-UNDO.
DEFINE VARIABLE endperiode      AS DATE NO-UNDO.
DEFINE VARIABLE wday            AS INTEGER NO-UNDO.
DEFINE VARIABLE adult           AS INTEGER NO-UNDO.
DEFINE VARIABLE rmcode          AS INTEGER NO-UNDO.
DEFINE VARIABLE price           AS CHAR NO-UNDO.
/*end*/

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST ratecode WHERE RECID(ratecode) EQ int1 NO-LOCK NO-ERROR.
        IF AVAILABLE ratecode THEN
        DO:
            FIND CURRENT ratecode EXCLUSIVE-LOCK.
            FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ ratecode.zikatnr NO-LOCK NO-ERROR. 
            IF AVAILABLE zimkateg THEN
            DO:
                ASSIGN
                    rmcode = ratecode.zikatnr /*naufal 200220 - add validation for delete linked child*/
                    RmType = zimkateg.kurzbez.
            END.
                
            prcode = ratecode.CODE.
            /*naufal 231219 - add variable for deleting linked child*/
            ASSIGN
                startperiode    = ratecode.startperiode
                endperiode      = ratecode.endperiode
                wday            = ratecode.wday
                adult           = ratecode.erwachs
                price           = STRING(ratecode.zipreis).
            /*end*/
            DELETE ratecode.
            RELEASE ratecode.

            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN 
            DO:
                CREATE res-history.
                ASSIGN 
                    res-history.nr          = bediener.nr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.aenderung   = "Delete RateCode, Code: " + prcode + " RmType : " + RmType + " Start:" + STRING(startperiode)
                                        + "|End:" + STRING(endperiode) + "|DW" + STRING(wday) + "|Adult:" + STRING(adult) + "|Rate:" + price
                    res-history.action      = "RateCode".
                FIND CURRENT res-history NO-LOCK.
                RELEASE res-history.
            END.
        END.  
        /*naufal 231219 - add condition for deleting linked child*/
        FOR EACH queasy WHERE queasy.KEY = 2 AND NOT queasy.logi2
            AND NUM-ENTRIES(queasy.char3, ";") GT 2
            AND ENTRY(2, queasy.char3, ";") = prcode NO-LOCK:
            chcode = queasy.char1.
            FIND FIRST ratecode WHERE ratecode.CODE EQ queasy.char1 
                AND ratecode.startperiode EQ startperiode
                AND ratecode.endperiode EQ endperiode
                AND ratecode.wday EQ wday
                AND ratecode.erwachs EQ adult 
                AND ratecode.zikatnr EQ rmcode NO-LOCK NO-ERROR.
            IF AVAILABLE ratecode THEN
            DO:
                FIND CURRENT ratecode EXCLUSIVE-LOCK.

                DELETE ratecode.
                RELEASE ratecode.
            END.

            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN 
            DO:
                CREATE res-history.
                ASSIGN 
                    res-history.nr          = bediener.nr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.aenderung   = "Delete Child RateCode, Code: " + chcode + " RmType : " + RmType
                    res-history.action      = "RateCode".
                FIND CURRENT res-history NO-LOCK.
                RELEASE res-history.
            END.
        END.
        /*
        FIND FIRST queasy WHERE queasy.KEY = 2 AND NOT queasy.logi2
            AND NUM-ENTRIES(queasy.char3, ";") GT 2
            AND ENTRY(2, queasy.char3, ";") = prcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            chcode = queasy.char1.
            FIND FIRST ratecode WHERE ratecode.CODE EQ queasy.char1 
                AND ratecode.startperiode EQ startperiode
                AND ratecode.endperiode EQ endperiode
                AND ratecode.erwachs EQ adult NO-LOCK NO-ERROR.
            IF AVAILABLE ratecode THEN
            DO:
                FIND CURRENT ratecode EXCLUSIVE-LOCK.
                DELETE ratecode.
                RELEASE ratecode.
            END.

            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN 
            DO:
                CREATE res-history.
                ASSIGN 
                    res-history.nr          = bediener.nr
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.aenderung   = "Delete Child RateCode, Code: " + chcode + " RmType : " + RmType.
                    res-history.action      = "RateCode".
                FIND CURRENT res-history NO-LOCK.
                RELEASE res-history.
            END.
        END.
        */
        /*end*/
    END.
END CASE.
