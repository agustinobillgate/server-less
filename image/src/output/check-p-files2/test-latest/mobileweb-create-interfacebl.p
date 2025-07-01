/*Program ini akan berjalan jika status code kamar 2 / 3*/

DEFINE INPUT PARAMETER rsv-number      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER rsvline-number  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init       AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER email           AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER guest-phnumber  AS CHAR    NO-UNDO. 
DEFINE INPUT PARAMETER hotel-code      AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER room-preference AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER url-MCI         AS CHAR    NO-UNDO.

DEFINE OUTPUT PARAMETER result-message AS CHAR             NO-UNDO.

DEFINE VARIABLE hServer     AS HANDLE     NO-UNDO.
DEFINE VARIABLE lReturn     AS LOGICAL    NO-UNDO.
DEFINE VARIABLE HtlappParam AS CHAR       NO-UNDO.
DEFINE VARIABLE vHost       AS CHAR       NO-UNDO.
DEFINE VARIABLE vService    AS CHAR       NO-UNDO.

DEFINE VARIABLE hotel-name   AS CHAR NO-UNDO.
DEFINE VARIABLE room-number  AS CHAR NO-UNDO.
DEFINE VARIABLE guest-name   AS CHAR NO-UNDO.

DEFINE VARIABLE cPersonalKey   AS CHARACTER NO-UNDO.
DEFINE VARIABLE rKey           AS RAW.
DEFINE VARIABLE mMemptrOut     AS MEMPTR.
DEFINE VARIABLE str-text       AS CHARACTER NO-UNDO.
DEFINE VARIABLE encrypted-text AS CHARACTER NO-UNDO.

IF email           EQ ? THEN email           = "".
IF guest-phnumber  EQ ? THEN guest-phnumber  = "".
IF hotel-code      EQ ? THEN hotel-code      = "".
IF url-MCI         EQ ? THEN url-MCI         = "".
IF room-preference EQ ? THEN room-preference = "".

IF guest-phnumber EQ "" THEN
DO:
    result-message = "1 - Phone Number must be filled-in!".
    RETURN.
END.

str-text = hotel-code + "|" + STRING(rsv-number) + "|" + STRING(rsvline-number).

ASSIGN 
    cPersonalKey    = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
    rKey            = GENERATE-PBE-KEY(cPersonalKey)
    mMemptrOut      = ENCRYPT(str-text, rKey )
    encrypted-text  = BASE64-ENCODE(MMEMPTROUT).  

url-MCI = ENTRY(1,url-MCI,"?") + "?SMS=" + encrypted-text.

FIND FIRST paramtext WHERE txtnr = 240 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT hotel-name). 

FIND FIRST res-line WHERE res-line.resnr EQ rsv-number AND res-line.reslinnr EQ rsvline-number NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    room-number = res-line.zinr.
    guest-name  = res-line.NAME.

    CREATE INTERFACE.
    ASSIGN
        INTERFACE.key         = 50
        INTERFACE.zinr        = room-number
        INTERFACE.nebenstelle = "" 
        INTERFACE.intfield    = 0
        INTERFACE.decfield    = 1
        INTERFACE.int-time    = TIME
        INTERFACE.intdate     = TODAY
        INTERFACE.parameters  = hotel-code + ";" + hotel-name + ";" + guest-name + ";" + guest-phnumber + ";" + email + ";" + room-preference + ";" + url-MCI
        INTERFACE.resnr       = rsv-number
        INTERFACE.reslinnr    = rsvline-number
        . 

    /*create queuing room*/
    /*report queuing room diubah untuk status ne 0*/
    IF room-number NE "" THEN
    DO:
        FIND FIRST zimmer WHERE zimmer.zinr = room-number NO-LOCK.
        IF zimmer.zistatus NE 0 THEN 
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 162 AND queasy.char1 = room-number NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                CREATE queasy.
                ASSIGN
                    queasy.KEY      = 162
                    queasy.char1    = room-number
                .
            END.
            ASSIGN        
                queasy.char2    = user-init
                queasy.number1  = 0
                queasy.number2  = TIME
                queasy.date2    = TODAY
                .
            FIND CURRENT queasy NO-LOCK.
        END.
    END.
    FIND CURRENT res-line NO-LOCK.
    result-message = "0 - Success".
END.
ELSE
DO:
    result-message = "2 - No Reservation found!".
    RETURN.
END.


PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
    s = in-str. 
    j = ASC(SUBSTR(s, 1, 1)) - 70. 
    len = LENGTH(in-str) - 1. 
    s = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
    END. 
END.
