/* NightAudit Program yang akan create table interface untuk...
reservasi yang C/I date adalah tepat ... hari sebelumnya dan
reservasi yang C/O date adalah tepat ... hari setelah C/O,
CHIRAG 10Jan2019 */

DEFINE VARIABLE datum           AS DATE     NO-UNDO.
DEFINE VARIABLE ci-days         AS INT      NO-UNDO.
DEFINE VARIABLE co-days         AS INT      NO-UNDO.
DEFINE VARIABLE ci-flag         AS CHAR     NO-UNDO.
DEFINE VARIABLE co-flag         AS CHAR     NO-UNDO.
DEFINE BUFFER resline FOR res-line.
DEFINE STREAM s1.

RUN readsession.
RUN htpdate.p(87, OUTPUT datum).
datum = datum - 1.

/* ... days earlier, check-in trigger */
IF ci-flag MATCHES "*e*" THEN   /* matches "yes" */
DO:
    FIND FIRST res-line WHERE res-line.active-flag EQ 0 
        AND res-line.resstatus LT 6
        AND res-line.ankunft - datum EQ ci-days
        AND NOT res-line.zimmer-wunsch MATCHES "*$CI7DAYSMAIL$*" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE res-line:
    
        FIND FIRST INTERFACE WHERE INTERFACE.KEY = 7
            AND INTERFACE.resnr = res-line.resnr AND INTERFACE.reslinnr = res-line.reslinnr 
            AND NOT INTERFACE.nebenstelle MATCHES "*$CI7DAYSMAIL$*" NO-LOCK NO-ERROR.
        IF NOT AVAILABLE INTERFACE THEN
        DO:
            /*RUN intevent-1.p( 1, INTERFACE.zinr, "My Checkin!", INTERFACE.resnr, INTERFACE.reslinnr).*/
            CREATE INTERFACE.
            ASSIGN
                INTERFACE.KEY         = 7
                INTERFACE.zinr        = res-line.zinr
                INTERFACE.nebenstelle = ""
                INTERFACE.intfield    = 0
                INTERFACE.decfield    = 1
                INTERFACE.int-time    = TIME
                INTERFACE.intdate     = TODAY
                INTERFACE.parameters  = "My Checkin!"
                INTERFACE.resnr       = res-line.resnr
                INTERFACE.reslinnr    = res-line.reslinnr
            .
            RELEASE INTERFACE.
    
            FIND CURRENT res-line EXCLUSIVE-LOCK.
            res-line.zimmer-wunsch = res-line.zimmer-wunsch + "$CI7DAYSMAIL$;".
            FIND CURRENT res-line NO-LOCK.
        END.
    
        FIND NEXT res-line WHERE res-line.active-flag EQ 0 
            AND res-line.resstatus LT 6
            AND res-line.ankunft - datum LE 7
            AND NOT res-line.zimmer-wunsch MATCHES "*$CI7DAYSMAIL$*" NO-LOCK NO-ERROR.
    END.
END.

/* ... days after, check-out trigger */
IF co-flag MATCHES "*e*" THEN   /* matches "yes" */
DO:
    FIND FIRST res-line WHERE res-line.resstatus EQ 8 AND active-flag = 2
        AND datum - res-line.abreise = co-days
        AND NOT res-line.zimmer-wunsch MATCHES "*$CO3DAYSMAIL$*" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE res-line:
    
        FIND FIRST INTERFACE WHERE INTERFACE.KEY = 7
            AND INTERFACE.resnr = res-line.resnr AND INTERFACE.reslinnr = res-line.reslinnr 
            AND NOT INTERFACE.nebenstelle MATCHES "*$CO3DAYSMAIL$*" NO-LOCK NO-ERROR.
        IF NOT AVAILABLE INTERFACE THEN
        DO:
            CREATE INTERFACE.
            ASSIGN
                INTERFACE.KEY         = 7
                INTERFACE.zinr        = res-line.zinr
                INTERFACE.nebenstelle = ""
                INTERFACE.intfield    = 0
                INTERFACE.decfield    = 2
                INTERFACE.int-time    = TIME
                INTERFACE.intdate     = TODAY
                INTERFACE.parameters  = "My Checkout!"
                INTERFACE.resnr       = res-line.resnr
                INTERFACE.reslinnr    = res-line.reslinnr
            .
            RELEASE INTERFACE.
    
            FIND CURRENT res-line EXCLUSIVE-LOCK.
            res-line.zimmer-wunsch = res-line.zimmer-wunsch + "$CO3DAYSMAIL$;".
            FIND CURRENT res-line NO-LOCK.
        END.
    
        FIND NEXT res-line WHERE res-line.resstatus EQ 8 AND active-flag = 2
            AND datum - res-line.abreise = 2
            AND NOT res-line.zimmer-wunsch MATCHES "*$CO3DAYSMAIL$*" NO-LOCK NO-ERROR.
    END.
END.

PROCEDURE readsession:
    
    DEFINE VARIABLE str-param   AS CHAR NO-UNDO FORMAT "x(64)".
    DEFINE VARIABLE param1      AS CHAR NO-UNDO.
    DEFINE VARIABLE param-file  AS CHAR NO-UNDO.
    DEFINE VARIABLE fpath       AS CHAR NO-UNDO.
    fpath = SEARCH("C:\e1-vhp\greetmail.cfg").

    IF fpath NE ? THEN
    DO:
        INPUT STREAM s1 FROM VALUE (fpath).
        REPEAT:
            IMPORT STREAM s1 UNFORMATTED str-param NO-ERROR.
            IF NOT str-param MATCHES "*#*" THEN
            DO:
                IF NUM-ENTRIES(str-param, "=") = 2 THEN
                DO:
                    param1 = ENTRY(1, str-param, "=").
                    IF param1 MATCHES ("*checkin-flag*") THEN
                        ci-flag = TRIM(ENTRY(2, str-param, "=")).
                    IF param1 MATCHES ("*checkout-flag*") THEN
                        co-flag = TRIM(ENTRY(2, str-param, "=")).
                    IF param1 MATCHES ("*days-before-checkin*") THEN
                        ci-days = INT(TRIM(ENTRY(2, str-param, "="))).
                    IF param1 MATCHES ("*days-after-checkout*") THEN
                        co-days = INT(TRIM(ENTRY(2, str-param, "="))).
                END.
            END.
        END.
        INPUT STREAM s1 CLOSE.

        IF co-flag MATCHES "*e*" AND co-days GT 0 THEN /* matches "yes"... */
            co-days = co-days - 1.
    END.
    ELSE
    DO:
        ASSIGN
            ci-days = 7
            co-days = 2
            ci-flag = "yes"
            co-flag = "yes".
    END.

END PROCEDURE.
