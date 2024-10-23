
DEF TEMP-TABLE t-list NO-UNDO
    FIELD autostart         AS LOGICAL
    FIELD period            AS INT
    FIELD delay             AS INT
    FIELD hotelcode         AS CHAR
    FIELD username          AS CHAR
    FIELD password          AS CHAR
    FIELD liveflag          AS LOGICAL
    FIELD defcurr           AS CHAR
    FIELD pushrateflag      AS LOGICAL
    FIELD pullbookflag      AS LOGICAL
    FIELD pushavailflag     AS LOGICAL
    FIELD workpath          AS CHAR
    FIELD progavail         AS CHAR
    FIELD prog-avail-update AS CHAR
    FIELD dyna-code         AS CHAR
    FIELD pushratebypax     AS LOGICAL
    FIELD uppercasename     AS LOGICAL
    FIELD delayrate         AS INTEGER
    FIELD delaypull         AS INTEGER
    FIELD delayavail        AS INTEGER
    FIELD pushall           AS LOGICAL
    FIELD re-calculate      AS LOGICAL
    FIELD restriction       AS LOGICAL
    FIELD allotment         AS LOGICAL
    FIELD pax               AS INTEGER
    FIELD bedsetup          AS LOGICAL
    FIELD pushbookflag      AS LOGICAL
    FIELD delaypushbook     AS INTEGER
    FIELD vcwsagent         AS CHAR
    FIELD vcwsagent2        AS CHAR
    FIELD vcwsagent3        AS CHAR
    FIELD vcwsagent4        AS CHAR
    FIELD vcwebhost         AS CHAR
    FIELD vcwebport         AS CHAR
    FIELD email             AS CHAR
    FIELD vcwsagent5        AS CHAR
    FIELD incl-tentative    AS LOGICAL
    FIELD restrictionFullSync AS LOGICAL
    FIELD crm-combo         AS LOGICAL.


DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER bookengID      AS INT.
DEF INPUT  PARAMETER autostart      AS LOGICAL.
DEF INPUT  PARAMETER period         AS INT.
DEF INPUT  PARAMETER delay          AS INT.
DEF INPUT  PARAMETER hotelcode      AS CHAR.
DEF INPUT  PARAMETER username       AS CHAR.
DEF INPUT  PARAMETER password       AS CHAR.
DEF INPUT  PARAMETER liveflag       AS LOGICAL.
DEF INPUT  PARAMETER defcurr        AS CHAR.
DEF INPUT  PARAMETER pushrateflag   AS LOGICAL.
DEF INPUT  PARAMETER pullbookflag   AS LOGICAL.
DEF INPUT  PARAMETER pushavailflag  AS LOGICAL.
DEF INPUT  PARAMETER workpath       AS CHAR.
DEF INPUT  PARAMETER progavail      AS CHAR.

DEF VAR i AS INT NO-UNDO.
DEF VAR str AS CHAR NO-UNDO.
DEF VAR ct AS CHAR NO-UNDO.
DEF VAR be-name AS CHAR NO-UNDO.

DEF BUFFER nameqsy FOR queasy.
DEF BUFFER bqueasy FOR queasy.

ct = "$autostart$" + STRING(autostart)      + ";"
   + "$period$"    + STRING(period)         + ";"
   + "$delay$"     + STRING(delay)          + ";"
   + "$liveflag$"  + STRING(liveflag)       + ";"
   + "$defcurr$"   + STRING(defcurr)        + ";"
   + "$workpath$"  + STRING(workpath)       + ";"
   + "$progname$"  + STRING(progavail)      + ";"
   + "$htlcode$"   + STRING(hotelcode)      + ";"
   + "$username$"  + STRING(username)       + ";"
   + "$password$"  + STRING(password)       + ";"
   + "$pushrate$"  + STRING(pushrateflag)   + ";"
   + "$pullbook$"  + STRING(pullbookflag)   + ";"
   + "$pushavail$" + STRING(pushavailflag)  .


FIND FIRST nameqsy WHERE nameqsy.KEY = 159 AND nameqsy.number1 = bookengID NO-LOCK NO-ERROR.
be-name = nameqsy.char1 + "|Config".

EMPTY TEMP-TABLE t-list.
FIND FIRST queasy WHERE queasy.KEY = 160 AND queasy.number1 = bookengID NO-LOCK NO-ERROR.
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
        ELSE IF SUBSTR(str,1,10) = "$progname$"  THEN t-list.progavail      = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,9)  = "$htlcode$"   THEN t-list.hotelcode      = SUBSTR(str,10).
        ELSE IF SUBSTR(str,1,10) = "$username$"  THEN t-list.username       = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10) = "$password$"  THEN t-list.password       = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10) = "$pushrate$"  THEN t-list.pushrateflag   = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,10) = "$pullbook$"  THEN t-list.pullbookflag   = LOGICAL(SUBSTR(str,11)).
        ELSE IF SUBSTR(str,1,11) = "$pushavail$" THEN t-list.pushavailflag  = LOGICAL(SUBSTR(str,12)).        
    END.
    RUN assign-tlist-values.

    IF queasy.char1 NE ct THEN 
    DO:
        RUN create-logdetails.
        /* RUN update-repeatflag-bl.p. NC - 24/08/23 move on this source*/
		FIND FIRST bqueasy WHERE bqueasy.KEY = 167 AND bqueasy.number1 = bookengID NO-LOCK NO-ERROR.
		IF AVAILABLE bqueasy THEN
		DO:
			FIND CURRENT bqueasy EXCLUSIVE-LOCK.
			bqueasy.date1 = TODAY.
			bqueasy.logi1 = YES.
			FIND CURRENT bqueasy NO-LOCK.
			RELEASE bqueasy.
		END.
		ELSE
		DO :
			CREATE bqueasy.
			ASSIGN
				bqueasy.KEY = 167
				bqueasy.date1 = TODAY
				bqueasy.number1 = bookengID
				bqueasy.logi1 = YES.
		END.

    END.
        
    FIND CURRENT queasy EXCLUSIVE-LOCK .
    queasy.char1 = ct.
    FIND CURRENT queasy NO-LOCK.
END.
ELSE
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY = 160
        queasy.number1 = bookengID
        queasy.char1 = ct.

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history. 
        ASSIGN 
            res-history.nr     = bediener.nr 
            res-history.datum  = TODAY 
            res-history.zeit   = TIME 
            res-history.action = "Booking Engine Interface".

        res-history.aenderung = CHR(40) + be-name + CHR(41) + " New Config Has Been Created".

        RELEASE res-history.
    END.
        
END.

PROCEDURE assign-tlist-values:

    IF NUM-ENTRIES(t-list.progavail,"=") GT 1 THEN
    DO:
        ASSIGN
            t-list.prog-avail-update = ENTRY(1,t-list.progavail,"=")
            t-list.dyna-code         = ENTRY(2,t-list.progavail,"=")
        .
        IF NUM-ENTRIES(t-list.progavail,"=") GE 3 THEN
            t-list.pushratebypax   = LOGICAL(ENTRY(3,t-list.progavail,"=")).
        ELSE t-list.pushratebypax  = NO.

        IF NUM-ENTRIES(t-list.progavail,"=") GE 4 THEN
            t-list.upperCaseName   = LOGICAL(ENTRY(4,t-list.progavail,"=")).
        ELSE t-list.upperCaseName  = NO.

        IF NUM-ENTRIES(t-list.progavail,"=") GE 5 THEN
            ASSIGN
                t-list.delayRate  = INT(ENTRY(5,t-list.progavail,"="))
                t-list.delayPull  = INT(ENTRY(6,t-list.progavail,"="))
                t-list.delayAvail = INT(ENTRY(7,t-list.progavail,"=")).
        ELSE
            ASSIGN
                t-list.delayRate   = 300
                t-list.delayPull   = 60
                t-list.delayAvail  = 60.

        IF NUM-ENTRIES(t-list.progavail,"=") GE 8 THEN
            ASSIGN
                t-list.pushAll      = LOGICAL(ENTRY(8,t-list.progavail,"="))
                t-list.re-calculate = LOGICAL(ENTRY(9,t-list.progavail,"=")).
        ELSE 
            ASSIGN
                t-list.pushAll      = NO
                t-list.re-calculate = NO.

        IF NUM-ENTRIES(t-list.progavail,"=") GE 10 THEN
            ASSIGN
                t-list.restriction   = LOGICAL(ENTRY(10,t-list.progavail,"="))
                t-list.allotment     = LOGICAL(ENTRY(11,t-list.progavail,"="))
                t-list.pax           = INT(ENTRY(12,t-list.progavail,"="))
                t-list.bedsetup      = LOGICAL(ENTRY(13,t-list.progavail,"=")).

        IF NUM-ENTRIES(t-list.progavail,"=") GE 14 THEN
            ASSIGN
                t-list.pushbookflag  = LOGICAL(ENTRY(14,t-list.progavail,"="))
                t-list.delaypushbook = INT(ENTRY(15,t-list.progavail,"=")).

        IF NUM-ENTRIES(t-list.progavail,"=") GE 16 THEN
            ASSIGN
                t-list.vcWSAgent     = ENTRY(16,t-list.progavail,"=")
                t-list.vcWSAgent2    = ENTRY(17,t-list.progavail,"=")
                t-list.vcWSAgent3    = ENTRY(18,t-list.progavail,"=")
                t-list.vcWSAgent4    = ENTRY(19,t-list.progavail,"=")               
                t-list.vcWebHost     = ENTRY(20,t-list.progavail,"=")
                t-list.vcWebPort     = ENTRY(21,t-list.progavail,"=")                
            .

        IF NUM-ENTRIES(t-list.progavail,"=") GE 22 THEN
            t-list.email             = ENTRY(22,t-list.progavail,"=").
        IF NUM-ENTRIES(t-list.progavail,"=") GE 23 THEN
            t-list.vcWSAgent5        = ENTRY(23,t-list.progavail,"=").
        IF NUM-ENTRIES(t-list.progavail,"=") GE 24 THEN
            t-list.incl-tentative    = LOGICAL(ENTRY(24,t-list.progavail,"=")).
        IF NUM-ENTRIES(t-list.progavail,"=") GE 25 THEN
            t-list.restrictionFullSync = LOGICAL(ENTRY(25,t-list.progavail,"=")).
        IF NUM-ENTRIES(t-list.progavail,"=") GE 26 THEN
            t-list.crm-combo         = LOGICAL(ENTRY(26,t-list.progavail,"=")).

    END. 

END PROCEDURE.


PROCEDURE create-logdetails:
    DEFINE VARIABLE logmessage AS LONGCHAR.

    logmessage = "".
    FIND FIRST t-list NO-LOCK NO-ERROR.
    IF AVAILABLE t-list THEN
    DO:
        IF t-list.autostart NE autostart THEN
            logmessage = logmessage + "autostart=" + STRING(t-list.autostart) + ">>" + STRING(autostart) + " ".
        IF t-list.period NE period THEN
            logmessage = logmessage + "period=" + STRING(t-list.period) + ">>" + STRING(period) + " ".
        IF t-list.delay NE delay THEN
            logmessage = logmessage + "delay=" + STRING(t-list.delay) + ">>" + STRING(delay) + " ".
        IF t-list.liveflag NE liveflag THEN
            logmessage = logmessage + "liveflag=" + STRING(t-list.liveflag) + ">>" + STRING(liveflag) + " ".
        IF t-list.defcurr NE defcurr THEN
            logmessage = logmessage + "defcurr=" + t-list.defcurr + ">>" + defcurr + " ".
        IF t-list.workpath NE workpath THEN
            logmessage = logmessage + "workpath=" + t-list.workpath + ">>" + workpath + " ".
        IF t-list.hotelcode NE hotelcode THEN
            logmessage = logmessage + "htlcode=" + t-list.hotelcode + ">>" + hotelcode + " ".
        IF t-list.username NE username THEN
            logmessage = logmessage + "usrname=" + t-list.username + ">>" + username + " ".
        IF t-list.password NE password THEN
            logmessage = logmessage + "pswd=" + t-list.password + ">>" + password + " ".
        IF t-list.pushrateflag NE pushrateflag THEN
            logmessage = logmessage + "pushrate=" + STRING(t-list.pushrateflag) + ">>" + STRING(pushrateflag) + " ".
        IF t-list.pullbookflag NE pullbookflag THEN
            logmessage = logmessage + "pullbook=" + STRING(t-list.pullbookflag) + ">>" + STRING(pullbookflag) + " ".
        IF t-list.pushavailflag NE pushavailflag THEN
            logmessage = logmessage + "pushavail=" + STRING(t-list.pushavailflag) + ">>" + STRING(pushavailflag) + " ".

        IF t-list.prog-avail-update NE ENTRY(1,progavail,"=") THEN
            logmessage = logmessage + "progname=" + t-list.prog-avail-update + ">>" + ENTRY(1,progavail,"=") + " ".
        IF t-list.dyna-code NE ENTRY(2,progavail,"=") THEN
            logmessage = logmessage + "dynacode=" + t-list.dyna-code + ">>" + ENTRY(2,progavail,"=") + " ".
        IF STRING(t-list.pushratebypax) NE ENTRY(3,progavail,"=") THEN
            logmessage = logmessage + "bypax=" + STRING(t-list.pushratebypax) + ">>" + ENTRY(3,progavail,"=") + " ".
        IF STRING(t-list.uppercasename) NE ENTRY(4,progavail,"=") THEN
            logmessage = logmessage + "uppercase=" + STRING(t-list.uppercasename) + ">>" + ENTRY(4,progavail,"=") + " ".
        IF STRING(t-list.delayrate) NE ENTRY(5,progavail,"=") THEN
            logmessage = logmessage + "delayrate=" + STRING(t-list.delayrate) + ">>" + ENTRY(5,progavail,"=") + " ".
        IF STRING(t-list.delaypull) NE ENTRY(6,progavail,"=") THEN
            logmessage = logmessage + "delaypull=" + STRING(t-list.delaypull) + ">>" + ENTRY(6,progavail,"=") + " ".
        IF STRING(t-list.delayavail) NE ENTRY(7,progavail,"=") THEN
            logmessage = logmessage + "delayavail=" + STRING(t-list.delayavail) + ">>" + ENTRY(7,progavail,"=") + " ".
        IF STRING(t-list.pushall) NE ENTRY(8,progavail,"=") THEN
            logmessage = logmessage + "pushall=" + STRING(t-list.pushall) + ">>" + ENTRY(8,progavail,"=") + " ".
        IF STRING(t-list.re-calculate) NE ENTRY(9,progavail,"=") THEN
            logmessage = logmessage + "recalc=" + STRING(t-list.re-calculate) + ">>" + ENTRY(9,progavail,"=") + " ".
        IF STRING(t-list.restriction) NE ENTRY(10,progavail,"=") THEN
            logmessage = logmessage + "restrict=" + STRING(t-list.restriction) + ">>" + ENTRY(10,progavail,"=") + " ".
        IF STRING(t-list.allotment) NE ENTRY(11,progavail,"=") THEN
            logmessage = logmessage + "allot=" + STRING(t-list.allotment) + ">>" + ENTRY(11,progavail,"=") + " ".
        IF STRING(t-list.pax) NE ENTRY(12,progavail,"=") THEN
            logmessage = logmessage + "pax=" + STRING(t-list.pax) + ">>" + ENTRY(12,progavail,"=") + " ".
        IF STRING(t-list.bedsetup) NE ENTRY(13,progavail,"=") THEN
            logmessage = logmessage + "bed=" + STRING(t-list.bedsetup) + ">>" + ENTRY(13,progavail,"=") + " ".
        IF STRING(t-list.pushbookflag) NE ENTRY(14,progavail,"=") THEN
            logmessage = logmessage + "pushbook=" + STRING(t-list.pushbookflag) + ">>" + ENTRY(14,progavail,"=") + " ".
        IF STRING(t-list.delaypushbook) NE ENTRY(15,progavail,"=") THEN
            logmessage = logmessage + "delaypushbook=" + STRING(t-list.delaypushbook) + ">>" + ENTRY(15,progavail,"=") + " ".
        IF t-list.vcwsagent NE ENTRY(16,progavail,"=") THEN
            logmessage = logmessage + "pullbookurl=" + t-list.vcwsagent + ">>" + ENTRY(16,progavail,"=") + " ".
        IF t-list.vcwsagent2 NE ENTRY(17,progavail,"=") THEN
            logmessage = logmessage + "pushavailurl=" + t-list.vcwsagent2 + ">>" + ENTRY(17,progavail,"=") + " ".
        IF t-list.vcwsagent3 NE ENTRY(18,progavail,"=") THEN
            logmessage = logmessage + "pushrateurl=" + t-list.vcwsagent3 + ">>" + ENTRY(18,progavail,"=") + " ".
        IF t-list.vcwsagent4 NE ENTRY(19,progavail,"=") THEN
            logmessage = logmessage + "notifurl=" + t-list.vcwsagent4 + ">>" + ENTRY(19,progavail,"=") + " ".
        IF t-list.vcwebhost NE ENTRY(20,progavail,"=") THEN
            logmessage = logmessage + "host=" + t-list.vcwebhost + ">>" + ENTRY(20,progavail,"=") + " ".
        IF t-list.vcwebport NE ENTRY(21,progavail,"=") THEN
            logmessage = logmessage + "port=" + t-list.vcwebport + ">>" + ENTRY(21,progavail,"=") + " ".
        IF t-list.email NE ENTRY(22,progavail,"=") THEN
            logmessage = logmessage + "email=" + t-list.email + ">>" + ENTRY(22,progavail,"=") + " ".
        IF t-list.vcwsagent5 NE ENTRY(23,progavail,"=") THEN
            logmessage = logmessage + "pushbookurl=" + t-list.vcwsagent5 + ">>" + ENTRY(23,progavail,"=") + " ".
        IF STRING(t-list.incl-tentative) NE ENTRY(24,progavail,"=") THEN
            logmessage = logmessage + "incltentative=" + STRING(t-list.incl-tentative) + ">>" + ENTRY(24,progavail,"=") + " ".
        IF STRING(t-list.restrictionFullSync) NE ENTRY(25,progavail,"=") THEN
            logmessage = logmessage + "restrictionsync=" + STRING(t-list.restrictionFullSync) + ">>" + ENTRY(25,progavail,"=") + " ".
        IF STRING(t-list.crm-combo) NE ENTRY(26,progavail,"=") THEN
            logmessage = logmessage + "crmcombo=" + STRING(t-list.crm-combo) + ">>" + ENTRY(26,progavail,"=") + " ".
    END.

    IF logmessage NE "" THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history. 
            ASSIGN 
                res-history.nr     = bediener.nr 
                res-history.datum  = TODAY 
                res-history.zeit   = TIME 
                res-history.action = "Booking Engine Interface".

            res-history.aenderung = CHR(40) + be-name + CHR(41) + " " + logmessage.

            RELEASE res-history.
        END.
    END.

END PROCEDURE.
