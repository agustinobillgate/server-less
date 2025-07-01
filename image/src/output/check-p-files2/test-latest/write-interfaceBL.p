DEF TEMP-TABLE t-interface1 LIKE interface.
DEF TEMP-TABLE t-interface2 LIKE interface.

DEF INPUT  PARAMETER case-type  AS INTEGER.
DEF INPUT  PARAMETER TABLE FOR t-interface1.
DEF INPUT  PARAMETER TABLE FOR t-interface2.
DEF OUTPUT PARAMETER successFlag AS LOGICAL INITIAL NO NO-UNDO.
/* Dzikri 719501 */
DEFINE VARIABLE bediener-nr AS INTEGER.

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST t-interface1 NO-ERROR.
        IF AVAILABLE t-interface1 THEN
        DO:
          CREATE interface.
          BUFFER-COPY t-interface1 TO interface.
          RELEASE interface.
          successFlag = YES.
        END.                            
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST t-interface2 NO-LOCK NO-ERROR.
        FIND FIRST INTERFACE WHERE INTERFACE.KEY = t-interface2.KEY
            AND INTERFACE.zinr = t-interface2.zinr
            AND interface.nebenstelle = t-interface2.nebenstelle
            AND interface.action = t-interface2.action
            AND interface.parameters = t-interface2.parameters
            AND interface.intfield = t-interface2.intfield
            AND interface.decfield = t-interface2.decfield
            AND interface.intdate = t-interface2.intdate
            AND interface.int-time = t-interface2.int-time
            AND interface.betriebsnr = t-interface2.betriebsnr
            AND interface.resnr = t-interface2.resnr
            AND interface.reslinnr = t-interface2.reslinnr
            AND interface.zinr-old = t-interface2.zinr-old
            EXCLUSIVE-LOCK.
        IF AVAILABLE INTERFACE THEN
        DO:
            BUFFER-COPY t-interface1 TO interface.
            FIND CURRENT INTERFACE NO-LOCK.
            RELEASE interface.
            successFlag = YES.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST interface WHERE interface.KEY = 17 NO-LOCK NO-ERROR.
        IF AVAILABLE interface THEN RETURN.
        DO:
            CREATE interface.
            ASSIGN
                interface.KEY = 17
                interface.intdate = TODAY
                interface.int-time = TIME
            .
            FIND CURRENT interface NO-LOCK.
            RELEASE interface.
        END.
    END.
    /* SY 05 JUL 2017 */
    WHEN 4 THEN
    DO:
    DEF VAR user-init AS CHAR NO-UNDO.
        FOR EACH t-interface1:
            CREATE INTERFACE.
            BUFFER-COPY t-interface1 TO INTERFACE.
            ASSIGN
                user-init = ENTRY(2, INTERFACE.parameters,";")
                INTERFACE.parameters = ENTRY(1, INTERFACE.parameters, ";") NO-ERROR
            .
            IF INTERFACE.nebenstelle = "" THEN
            DO:
                FIND FIRST nebenst WHERE 
                    nebenst.zinr = INTERFACE.zinr AND  
                    nebenst.nebst-type = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE nebenst THEN INTERFACE.nebenstelle = nebenst.nebenstelle.
                ELSE
                DO:
                    FIND FIRST zimmer WHERE zimmer.zinr = interface.zinr NO-LOCK NO-ERROR.
                    IF AVAILABLE zimmer THEN INTERFACE.nebenstelle = zimmer.nebenstelle.
                END.
				/* Dzikri 719501 */
                FIND FIRST bediener where bediener.userinit EQ user-init NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN bediener-nr = bediener.nr.
				/* Dzikri END */
                CREATE res-history.
                ASSIGN
                    res-history.nr        = bediener-nr /* Dzikri modify */
                    res-history.resnr     = INTERFACE.resnr
                    res-history.reslinnr  = INTERFACE.reslinnr
                    res-history.datum     = INTERFACE.intdate
                    res-history.zeit      = INTERFACE.int-time
                    res-history.action    = "Wake Up Call"
                .
                IF INTERFACE.parameters = "Wakeup Calls OFF" THEN
                    res-history.aenderung = "Cancel Wake Up Call;".
                ELSE res-history.aenderung = "Set Wake Up Call;".
                res-history.aenderung = res-history.aenderung
                    + " RmNo: " + INTERFACE.zinr + ";"
                    + " TIME: " 
                    + STRING(INTERFACE.intfield,"HH:MM") + ";".
                IF user-init NE "" THEN
                res-history.aenderung = res-history.aenderung
                    + "UID :" + user-init + ";".
            END.
        END.
    END.
END CASE.

