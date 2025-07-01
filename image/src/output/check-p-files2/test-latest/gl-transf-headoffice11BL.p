DEF TEMP-TABLE t-gl-acct            LIKE gl-acct.
DEF TEMP-TABLE t-gl-accthis         LIKE gl-accthis.

DEF INPUT PARAMETER pvILanguage   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER close-month   AS DATE    NO-UNDO.
DEF INPUT PARAMETER close-year    AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER msg-str      AS CHAR    NO-UNDO INIT "".

DEFINE VARIABLE hServer       AS HANDLE     NO-UNDO.
DEFINE VARIABLE first-date    AS DATE       NO-UNDO.
DEFINE VARIABLE lReturn       AS LOGICAL    NO-UNDO.
DEFINE VARIABLE map-acct      AS CHAR       NO-UNDO.
DEFINE VARIABLE HOappParam    AS CHAR       NO-UNDO.
DEFINE VARIABLE vHost         AS CHAR       NO-UNDO.
DEFINE VARIABLE vService      AS CHAR       NO-UNDO.
DEFINE VARIABLE htl-code      AS CHAR       NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "closemonth". 

FIND FIRST htparam WHERE htparam.paramnr = 2843 NO-LOCK.
ASSIGN
    vHost      = ENTRY(1, htparam.fchar, ":")
    vService   = ENTRY(2, htparam.fchar, ":")
    htl-code   = ENTRY(3, htparam.fchar, ":")
    HOappParam = " -H " + vHost + " -S " + vService + " -DirectConnect -sessionModel Session-free"
.

CREATE SERVER hServer.
lReturn = hServer:CONNECT(HOappParam, ? , ? , ?) /*NO-ERROR*/.
IF NOT lReturn THEN
DO:
    msg-str = translateExtended ("Failed to connect to HO server",lvCAREA,"") 
            + CHR(10)
            + translateExtended ("Journals could not be transferred to the Heaad Office DB.",lvCAREA,"").
    DELETE OBJECT hServer NO-ERROR.
    RETURN.
END.  

IF close-month NE ? THEN
FOR EACH gl-acct NO-LOCK:
    CREATE t-gl-acct.
    BUFFER-COPY gl-acct TO t-gl-acct.
END.

IF close-year NE ? THEN
FOR EACH gl-accthis WHERE gl-accthis.YEAR = YEAR(close-year) NO-LOCK:
    CREATE t-gl-accthis.
    BUFFER-COPY gl-accthis TO t-gl-accthis.
END.

RUN gl-transf-headoffice22bl.p ON hServer (htl-code, close-month, 
    close-year, TABLE t-gl-acct, TABLE t-gl-accthis,
    OUTPUT success-flag ).

IF NOT success-flag THEN ASSIGN msg-str = 
    translateExtended ("Property Code not defined in the HO DB.",lvCAREA,"").
ELSE ASSIGN msg-str = 
    translateExtended ("GL COA have been transferred to the HO DB.",lvCAREA,"").

lReturn = hServer:DISCONNECT() NO-ERROR.
DELETE OBJECT hServer NO-ERROR.
