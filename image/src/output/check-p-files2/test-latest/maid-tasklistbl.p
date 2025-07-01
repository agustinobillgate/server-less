DEFINE TEMP-TABLE t-queasy LIKE queasy.
DEFINE TEMP-TABLE maid-tasklist 
    FIELD datum         AS DATE
    FIELD maidcode      AS CHAR
    FIELD maidname      AS CHAR
    FIELD roomnumber    AS CHAR
    FIELD roomcateg     AS CHAR
    FIELD starttime     AS CHAR
    FIELD endtime       AS CHAR
    FIELD duration      AS CHAR
    FIELD progrestat    AS CHAR.


DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE INPUT PARAMETER rpt-flag  AS INT. /*1=hk view (today), 2=report view(mtd)*/

DEFINE OUTPUT PARAMETER TABLE FOR maid-tasklist.

DEFINE VARIABLE tmp-userinit AS CHARACTER NO-UNDO.          /* Rulita 031224 | Fixing for serverless issue 249 */

IF rpt-flag EQ 1 THEN
DO:
    FIND FIRST htparam WHERE paramnr EQ 110 NO-LOCK NO-ERROR.
    from-date = htparam.fdate.
    to-date   = from-date.
END.

FOR EACH queasy WHERE queasy.KEY EQ 196
    AND queasy.date1 GE from-date AND queasy.date1 LE to-date NO-LOCK :
    FIND FIRST zimmer WHERE zimmer.zinr EQ ENTRY(1, queasy.char1, ";") NO-LOCK NO-ERROR.
    FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ zimmer.zikatnr NO-LOCK NO-ERROR.
    IF queasy.char1 NE "" AND NUM-ENTRIES(queasy.char1,";") GE 2 THEN
    DO:
        /* Rulita 031224 | Fixing for serverless issue 249 */
        CREATE maid-tasklist.
        ASSIGN 
            maid-tasklist.datum      = queasy.date1
            maid-tasklist.maidcode   = ENTRY(2, queasy.char1, ";")
            maid-tasklist.roomnumber = ENTRY(1, queasy.char1, ";")
            maid-tasklist.roomcateg  = zimkateg.bezeichnung
            maid-tasklist.starttime  = STRING(queasy.number1,"HH:MM:SS")
            maid-tasklist.endtime    = STRING(queasy.number2,"HH:MM:SS").
            
            IF queasy.number2 NE 0 THEN
                maid-tasklist.duration  = STRING((queasy.number2 - queasy.number1),"HH:MM:SS").
            ELSE 
                maid-tasklist.duration  = STRING(queasy.number2,"HH:MM:SS").

            IF queasy.number2 EQ 0 THEN
            maid-tasklist.progrestat = "On Going".
            ELSE
            maid-tasklist.progrestat = "Done".
        
        tmp-userinit = ENTRY(2, queasy.char1, ";").
        FIND FIRST bediener WHERE bediener.userinit EQ tmp-userinit NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            maid-tasklist.maidname   = bediener.username.
        END.
        /* End Rulita */    
    END.
END.
