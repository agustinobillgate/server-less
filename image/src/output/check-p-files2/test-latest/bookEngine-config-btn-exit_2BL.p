

DEF INPUT PARAMETER bookengID       AS INT.
DEF INPUT PARAMETER autostart       AS LOGICAL.
DEF INPUT PARAMETER period          AS INT.
DEF INPUT PARAMETER delay           AS INT.
DEF INPUT PARAMETER hotelcode       AS CHAR.
DEF INPUT PARAMETER username        AS CHAR.
DEF INPUT PARAMETER password        AS CHAR.
DEF INPUT PARAMETER liveflag        AS LOGICAL.
DEF INPUT PARAMETER defcurr         AS CHAR.
DEF INPUT PARAMETER pushrateflag    AS LOGICAL.
DEF INPUT PARAMETER pullbookflag    AS LOGICAL.
DEF INPUT PARAMETER pushavailflag   AS LOGICAL.
DEF INPUT PARAMETER workpath        AS CHAR.
DEF INPUT PARAMETER progavail       AS CHAR.
/*naufal - add for logfile*/
DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER pushratebypax   AS LOGICAL.
DEF INPUT PARAMETER upperCaseName   AS LOGICAL.
DEF INPUT PARAMETER delayRate       AS INTEGER.
DEF INPUT PARAMETER delayPull       AS INTEGER.
DEF INPUT PARAMETER delayAvail      AS INTEGER.
DEF INPUT PARAMETER pushAll         AS LOGICAL.
DEF INPUT PARAMETER re-calculate    AS LOGICAL.
DEF INPUT PARAMETER restriction     AS LOGICAL.
DEF INPUT PARAMETER allotment       AS LOGICAL.
DEF INPUT PARAMETER pax             AS INTEGER.
DEF INPUT PARAMETER bedsetup        AS LOGICAL.
DEF INPUT PARAMETER pushbookflag    AS LOGICAL.
DEF INPUT PARAMETER delaypushbook   AS INTEGER.
DEF INPUT PARAMETER vcWSAgent       AS CHAR.
DEF INPUT PARAMETER vcWSAgent2      AS CHAR.
DEF INPUT PARAMETER vcWSAgent3      AS CHAR.
DEF INPUT PARAMETER vcWSAgent4      AS CHAR.
DEF INPUT PARAMETER vcWSAgent5      AS CHAR.
DEF INPUT PARAMETER vcWebHost       AS CHAR.
DEF INPUT PARAMETER vcWebPort       AS CHAR.
DEF INPUT PARAMETER email           AS CHAR.
DEF INPUT PARAMETER dyna-code       AS CHAR.


DEF VAR i       AS INT  NO-UNDO.
DEF VAR str     AS CHAR NO-UNDO.
DEF VAR oldstr  AS CHAR NO-UNDO.
DEF VAR ct      AS CHAR NO-UNDO.
DEF VAR oldct   AS CHAR NO-UNDO.
DEF VAR progavail1 AS CHAR NO-UNDO.

/* Modify by Michael 31/12/2020 - rename progravail into progravail1 & casting non char variable into char & remove double pushbookflag */
ASSIGN 
    progavail1 =  progavail             + "=" +
                  dyna-code             + "=" +
                  STRING(pushratebypax) + "=" +
                  STRING(upperCaseName) + "=" +
                  STRING(delayRate)     + "=" +
                  STRING(delayPull)     + "=" +
                  STRING(delayAvail)    + "=" +
                  STRING(pushAll)       + "=" +
                  STRING(re-calculate)  + "=" +
                  STRING(restriction)   + "=" +
                  STRING(allotment)     + "=" +
                  STRING(pax)           + "=" +
                  STRING(bedsetup)      + "=" +
                  STRING(pushbookflag)  + "=" +
                  STRING(delaypushbook) + "=" +
                  vcWSAgent             + "=" +
                  vcWSAgent2            + "=" +
                  vcWSAgent3            + "=" +
                  vcWSAgent4            + "=" +
                  vcWebHost             + "=" +
                  vcWebPort             + "=" +
                  email                 + "=" +
                  vcWSAgent5.

ct = "$autostart$" + STRING(autostart)      + ";"
   + "$period$"    + STRING(period)         + ";"
   + "$delay$"     + STRING(delay)          + ";"
   + "$liveflag$"  + STRING(liveflag)       + ";"
   + "$defcurr$"   + STRING(defcurr)        + ";"
   + "$workpath$"  + STRING(workpath)       + ";"
   + "$progname$"  + STRING(progavail1)     + ";"
   + "$htlcode$"   + STRING(hotelcode)      + ";"
   + "$username$"  + STRING(username)       + ";"
   + "$password$"  + STRING(password)       + ";"
   + "$pushrate$"  + STRING(pushrateflag)   + ";"
   + "$pullbook$"  + STRING(pullbookflag)   + ";"
   + "$pushavail$" + STRING(pushavailflag)  .

FIND FIRST queasy WHERE KEY = 160 AND queasy.number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    IF queasy.char1 NE ct THEN 
        RUN update-repeatflag-bl.p.
        
    oldct = queasy.char1.
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    queasy.char1 = ct.
    FIND CURRENT queasy NO-LOCK.
    
    DO i = 1 TO NUM-ENTRIES(ct, ";"):
        str = ENTRY(i, ct, ";").
        oldstr = ENTRY(i, oldct, ";").
        IF oldstr NE str THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
                CREATE res-history.
                ASSIGN
                    res-history.nr          = bediener.nr       
                    res-history.datum       = TODAY
                    res-history.zeit        = TIME
                    res-history.aenderung   = "Change Config from: " + oldstr + ", to: " + str
                    res-history.action      = "Booking Engine Interface".
                FIND CURRENT res-history NO-LOCK.
                RELEASE res-history.
            END.
        END.
    END.
END.
ELSE
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY = 160
        queasy.number1 = bookengID
        queasy.char1 = ct.
        
    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr       
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Set Config, Booking Engine ID: " + STRING(bookengID) + ", Config: " + ct
            res-history.action      = "Booking Engine Interface".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END.

