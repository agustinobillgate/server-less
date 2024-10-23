DEF TEMP-TABLE t-gl-jouhdr          LIKE gl-jouhdr.
DEF TEMP-TABLE t-gl-journal         LIKE gl-journal.

DEF INPUT PARAMETER pvILanguage   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER curr-date     AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER msg-str      AS CHAR    NO-UNDO INIT "".

DEFINE VARIABLE hServer       AS HANDLE     NO-UNDO.
DEFINE VARIABLE first-date    AS DATE       NO-UNDO.
DEFINE VARIABLE lReturn       AS LOGICAL    NO-UNDO.
DEFINE VARIABLE map-acct      AS CHAR       NO-UNDO.
DEFINE VARIABLE HOappParam    AS CHAR       NO-UNDO.
DEFINE VARIABLE vHost         AS CHAR       NO-UNDO.
DEFINE VARIABLE vService      AS CHAR       NO-UNDO.
DEFINE VARIABLE lic-nr        AS CHAR       NO-UNDO INIT "".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "closemonth". 

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR.
IF NOT AVAILABLE paramtext THEN 
DO:    
    msg-str = translateExtended ("parmtext[243] was not available.",lvCAREA,"").
    RETURN.
END.
RUN decode-string(paramtext.ptexte, OUTPUT lic-nr).

ASSIGN first-date = DATE (MONTH(curr-date), 1, YEAR(curr-date)).
FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE first-date 
    AND gl-jouhdr.datum LE curr-date NO-LOCK BY gl-jouhdr.jnr:
    CREATE t-gl-jouhdr.
    BUFFER-COPY gl-jouhdr TO t-gl-jouhdr.
    FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK:
        CREATE t-gl-journal.
        BUFFER-COPY gl-journal TO t-gl-journal.
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto
            NO-LOCK.
        ASSIGN
            map-acct = ""
            map-acct = TRIM(ENTRY(2, gl-acct.userinit, ";")) NO-ERROR
        .
        IF map-acct NE "" THEN ASSIGN t-gl-journal.fibukonto = map-acct.
    END.
END.

FIND FIRST htparam WHERE htparam.paramnr = 2843 NO-LOCK.
ASSIGN
    vHost      = ENTRY(1, htparam.fchar, ":")
    vService   = ENTRY(2, htparam.fchar, ":")
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
RUN gl-transf-headoffice2bl.p ON hServer (lic-nr, 
    TABLE t-gl-jouhdr, TABLE t-gl-journal).

ASSIGN 
    success-flag = YES
    msg-str = translateExtended ("Journals have been transferred to the Heaad Office DB.",lvCAREA,"").
.

lReturn = hServer:DISCONNECT() NO-ERROR.
DELETE OBJECT hServer NO-ERROR.

PROCEDURE decode-string:
DEFINE INPUT PARAMETER in-str   AS CHAR NO-UNDO.
DEFINE OUTPUT parameter out-str AS CHAR NO-UNDO INITIAL "".
DEFINE VARIABLE s   AS CHAR     NO-UNDO.
DEFINE VARIABLE j   AS INTEGER  NO-UNDO.
DEFINE VARIABLE len AS INTEGER  NO-UNDO.
  ASSIGN
      s   = in-str
      j   = ASC(SUBSTR(s, 1, 1)) - 70 
      len = LENGTH(in-str) - 1
      s   = SUBSTR(in-str, 2, len)
  .
  DO len = 1 TO LENGTH(s):
    out-str = out-str + CHR(ASC(SUBSTR(s,len,1)) - j).
  END.
END.
