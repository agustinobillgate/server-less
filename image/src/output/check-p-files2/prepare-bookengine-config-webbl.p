
DEF TEMP-TABLE currency-list
    FIELD waehrungsnr AS INT
    FIELD bezeich     AS CHAR
    FIELD wabkurz     AS CHAR.

/*DEF TEMP-TABLE t-list
    FIELD autostart     AS LOGICAL
    FIELD period        AS INT
    FIELD delay         AS INT
    FIELD hotelcode     AS CHAR
    FIELD username      AS CHAR
    FIELD password      AS CHAR
    FIELD liveflag      AS LOGICAL
    FIELD defcurr       AS CHAR
    FIELD pushrateflag  AS LOGICAL
    FIELD pullbookflag  AS LOGICAL
    FIELD pushavailflag AS LOGICAL
    FIELD workpath      AS CHAR
    FIELD progavail     AS CHAR.*/

DEF TEMP-TABLE t-list
    FIELD autostart     AS LOGICAL
    FIELD period        AS INT
    FIELD delay         AS INT
    FIELD hotelcode     AS CHAR
    FIELD username      AS CHAR
    FIELD password      AS CHAR
    FIELD liveflag      AS LOGICAL
    FIELD defcurr       AS CHAR
    FIELD pushrateflag  AS LOGICAL
    FIELD pullbookflag  AS LOGICAL
    FIELD pushavailflag AS LOGICAL
    FIELD workpath      AS CHAR
    FIELD progavail     AS CHAR
    FIELD progavail1    AS CHAR
    FIELD pushratebypax AS LOGICAL
    FIELD upperCaseName AS LOGICAL
    FIELD delayRate     AS INTEGER
    FIELD delayPull     AS INTEGER
    FIELD delayAvail    AS INTEGER
    FIELD pushAll       AS LOGICAL
    FIELD re-calculate  AS LOGICAL
    FIELD restriction   AS LOGICAL
    FIELD allotment     AS LOGICAL
    FIELD pax           AS INTEGER
    FIELD bedsetup      AS LOGICAL
    FIELD pushbookflag  AS LOGICAL
    FIELD delaypushbook AS INTEGER
    FIELD vcWSAgent     AS CHARACTER
    FIELD vcWSAgent1    AS CHARACTER
    FIELD vcWSAgent2    AS CHARACTER
    FIELD vcWSAgent3    AS CHARACTER
    FIELD vcWSAgent4    AS CHARACTER
    FIELD vcWSAgent5    AS CHARACTER
    FIELD vcWebHost     AS CHARACTER
    FIELD vcWebPort     AS CHARACTER
    FIELD email         AS CHARACTER
    FIELD dyna-code     AS CHARACTER
    FIELD inclTentative AS LOGICAL.

DEF INPUT  PARAMETER bookengID      AS INT.
DEF OUTPUT PARAMETER bookeng-name   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-list.
DEF OUTPUT PARAMETER TABLE FOR currency-list.

/*DEF VAR bookengID      AS INT INIT 1.
DEF VAR bookeng-name   AS CHAR.*/


DEF VAR i AS INT.
DEF VAR str AS CHAR.

FIND FIRST queasy WHERE KEY = 159 AND number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN bookeng-name = queasy.char1.

FIND FIRST queasy WHERE KEY = 160 AND number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    CREATE t-list.
    DO i = 1 TO NUM-ENTRIES(queasy.char1,";"):
        str = ENTRY(i, queasy.char1, ";").
        IF SUBSTR(str,1,11)      = "$autostart$" THEN t-list.autostart      = LOGICAL(SUBSTR(str,12)).
        ELSE IF SUBSTR(str,1,8)  = "$period$"    THEN t-list.period         = INT(SUBSTR(str,9)).
        ELSE IF SUBSTR(str,1,7)  = "$delay$"     THEN t-list.delay          = INT(SUBSTR(str,8)).
        ELSE IF SUBSTR(str,1,10) = "$liveflag$"  THEN t-list.liveflag       = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,9)  = "$defcurr$"   THEN t-list.defcurr        = SUBSTR(str,10).
        ELSE IF SUBSTR(str,1,10) = "$workpath$"  THEN t-list.workpath       = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10) = "$progname$"  THEN t-list.progavail1      = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,9)  = "$htlcode$"   THEN t-list.hotelcode      = SUBSTR(str,10).
        ELSE IF SUBSTR(str,1,10) = "$username$"  THEN t-list.username       = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10) = "$password$"  THEN t-list.password       = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10) = "$pushrate$"  THEN t-list.pushrateflag   = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,10) = "$pullbook$"  THEN t-list.pullbookflag   = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,11) = "$pushavail$" THEN t-list.pushavailflag  = LOGICAL(SUBSTR(str,12)).        
    END.
END.

FOR EACH waehrung WHERE waehrung.betriebsnr = 0 NO-LOCK:
    CREATE currency-list.
    ASSIGN
        currency-list.waehrungsnr = waehrung.waehrungsnr
        currency-list.bezeich     = waehrung.bezeich
        currency-list.wabkurz     = waehrung.wabkurz.
END.

RUN fill-list.

/******************** PROCEDURES ********************/
PROCEDURE fill-list:

    IF NUM-ENTRIES(t-list.progavail1,"=") GT 1 THEN
    DO:
        ASSIGN
            t-list.progavail       = ENTRY(1,t-list.progavail1,"=")
            /*dyna-code       = ENTRY(2,t-list.progavail1,"=")*/
        .
        IF NUM-ENTRIES(t-list.progavail1,"=") GE 3 THEN
            t-list.pushratebypax   = LOGICAL(ENTRY(3,t-list.progavail1,"=")).
        ELSE t-list.pushratebypax  = NO.

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 4 THEN
            t-list.upperCaseName   = LOGICAL(ENTRY(4,t-list.progavail1,"=")).
        ELSE t-list.upperCaseName  = NO.

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 5 THEN
            ASSIGN
                t-list.delayRate  = INT(ENTRY(5,t-list.progavail1,"="))
                t-list.delayPull  = INT(ENTRY(6,t-list.progavail1,"="))
                t-list.delayAvail = INT(ENTRY(7,t-list.progavail1,"=")).
        ELSE
            ASSIGN
                t-list.delayRate   = 300
                t-list.delayPull   = 60
                t-list.delayAvail  = 60.

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 8 THEN
            ASSIGN
                t-list.pushAll      = LOGICAL(ENTRY(8,t-list.progavail1,"="))
                t-list.re-calculate = LOGICAL(ENTRY(9,t-list.progavail1,"=")).
        ELSE 
            ASSIGN
                t-list.pushAll      = NO
                t-list.re-calculate = NO.

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 10 THEN
            ASSIGN
                t-list.restriction   = LOGICAL(ENTRY(10,t-list.progavail1,"="))
                t-list.allotment     = LOGICAL(ENTRY(11,t-list.progavail1,"="))
                t-list.pax           = INT(ENTRY(12,t-list.progavail1,"="))
                t-list.bedsetup      = LOGICAL(ENTRY(13,t-list.progavail1,"=")).

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 14 THEN
            ASSIGN
                t-list.pushbookflag  = LOGICAL(ENTRY(14,t-list.progavail1,"="))
                t-list.delaypushbook = INT(ENTRY(15,t-list.progavail1,"=")).

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 16 THEN
            ASSIGN
                t-list.vcWSAgent     = ENTRY(16,t-list.progavail1,"=")
                t-list.vcWSAgent2    = ENTRY(17,t-list.progavail1,"=")
                t-list.vcWSAgent3    = ENTRY(18,t-list.progavail1,"=")
                t-list.vcWSAgent4    = ENTRY(19,t-list.progavail1,"=")               
                t-list.vcWebHost     = ENTRY(20,t-list.progavail1,"=")
                t-list.vcWebPort     = ENTRY(21,t-list.progavail1,"=")                
            .

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 22 THEN
            ASSIGN
                t-list.email         = ENTRY(22,t-list.progavail1,"=").

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 23 THEN
            t-list.vcWSAgent5    = ENTRY(23,t-list.progavail1,"=").

        IF NUM-ENTRIES(t-list.progavail1,"=") GE 24 THEN
        DO:
            t-list.inclTentative    = LOGICAL(ENTRY(24,t-list.progavail1,"=")).
        END.
    END. 
    ELSE 
        ASSIGN
            t-list.progavail       = t-list.progavail1
            t-list.dyna-code       = ""
            t-list.pushratebypax   = NO
            t-list.upperCaseName   = NO
            t-list.delayRate       = 300
            t-list.delayPull       = 60
            t-list.delayAvail      = 60
            t-list.pushAll         = YES
            t-list.re-calculate    = NO
            t-list.delaypushbook   = 60            
        .
END.

