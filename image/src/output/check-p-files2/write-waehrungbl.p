
DEF TEMP-TABLE t-waehrung LIKE waehrung.

DEF INPUT  PARAMETER case-type   AS INTEGER            NO-UNDO.
DEF INPUT  PARAMETER TABLE       FOR t-waehrung.
DEF OUTPUT PARAMETER successFlag AS LOGICAL INITIAL NO NO-UNDO.

FIND FIRST t-waehrung NO-ERROR.
IF NOT AVAILABLE t-waehrung THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
      CREATE waehrung.
      BUFFER-COPY t-waehrung TO waehrung.
      RELEASE waehrung.
      successFlag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = t-waehrung.waehrungsnr
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
        DO:
            BUFFER-COPY t-waehrung TO waehrung.
            FIND CURRENT waehrung NO-LOCK.
            successFlag = YES.
        END.
    END.
    /* SY AUG 11 2017 */
    WHEN 3 THEN
    DO:
    DEF VARIABLE useFlag AS LOGICAL NO-UNDO INIT NO.
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = t-waehrung.waehrungsnr
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
        DO:
            FIND FIRST res-line WHERE res-line.betriebsnr =
                waehrung.waehrungsnr NO-LOCK NO-ERROR.
            useFlag = AVAILABLE res-line.
            IF NOT useflag THEN
            DO:
                FIND FIRST artikel WHERE artikel.departement LT 90
                    AND artikel.betriebsnr = waehrung.waehrungsnr
                    NO-LOCK NO-ERROR.
                useFlag = AVAILABLE artikel.
            END.
            IF NOT useFlag THEN
            DO:
                FIND FIRST htparam WHERE htparam.paramnr = 152
                    NO-LOCK.
                IF htparam.fchar = waehrung.wabkurz THEN
                DO:
                    FIND CURRENT htparam EXCLUSIVE-LOCK.
                    ASSIGN htparam.fchar = "".
                    FIND CURRENT htparam NO-LOCK.
                    RELEASE htparam.
                END.
                FIND CURRENT waehrung EXCLUSIVE-LOCK.
                DELETE waehrung.
                RELEASE waehrung.
                successFlag = YES.
            END.
        END.
    END.
END CASE.
