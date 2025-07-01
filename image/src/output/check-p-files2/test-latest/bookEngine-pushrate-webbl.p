DEFINE TEMP-TABLE rate-list2
    FIELD origcode  AS CHAR
    FIELD rcode     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" EXTENT 31 COLUMN-LABEL "Rcode"
    FIELD BERates   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" EXTENT 31 COLUMN-LABEL "BERates"
    FIELD datum     AS DATE
.

DEFINE TEMP-TABLE rlist
    FIELD rcode AS CHARACTER
. 

DEFINE INPUT PARAMETER TABLE FOR rate-list2.
DEFINE OUTPUT PARAMETER echotoken AS CHARACTER INITIAL "".
DEFINE OUTPUT PARAMETER timestamp AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR rlist.

DEFINE VARIABLE uuid AS RAW NO-UNDO.

ASSIGN
   uuid        = GENERATE-UUID
   echotoken   = GUID(uuid)
   timestamp   = STRING(YEAR(TODAY),"9999") + "-" + STRING(MONTH(TODAY),"99") + "-" +
                 STRING(DAY(TODAY),"99") + "T" + STRING(TIME,"HH:MM:SS") + "+00:00".

/*change from rate-list1 to rate-list2*/
FOR EACH rate-list2:
    FIND FIRST rlist WHERE rlist.rcode EQ ENTRY(1,rate-list2.origcode,":") NO-LOCK NO-ERROR.
    IF NOT AVAILABLE rlist THEN
    DO:
        CREATE rlist.
        ASSIGN
            rlist.rcode = ENTRY(1,rate-list2.origcode,":").    
    END.                       
END.  
