/*Guestbook Operation For Web
  Purpuse   : For Create Read Update Delete on table guestbook
  Custom By : FD 27 July, 2021
*/
    
DEFINE TEMP-TABLE t-data
    FIELD gastnr        AS INTEGER
    FIELD infostr       AS CHAR
    FIELD orig-infostr  AS CHAR.

DEFINE INPUT PARAMETER inStr AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER base64file AS LONGCHAR.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR t-data.
DEFINE OUTPUT PARAMETER outStr AS CHARACTER.
DEFINE OUTPUT PARAMETER mess-result AS CHARACTER INITIAL "".

DEFINE VARIABLE tCase   AS INTEGER NO-UNDO.
DEFINE VARIABLE tGastnr AS INTEGER NO-UNDO.
DEFINE VARIABLE pointer AS MEMPTR NO-UNDO.

tCase = INT(ENTRY(1,instr,";")).
IF NUM-ENTRIES(inStr,";") GT 1 THEN DO:
    tGastnr = INT(ENTRY(2,instr,";")).
END.

CASE tCase:
    WHEN 1 THEN /*Create*/
    DO: 
        FIND FIRST t-data NO-LOCK NO-ERROR.
        IF AVAILABLE t-data THEN 
        DO:
            CREATE vhp.guestbook.
            ASSIGN
                vhp.guestbook.gastnr = t-data.gastnr
                vhp.guestbook.infostr = t-data.infostr
                vhp.guestbook.orig-infostr = t-data.orig-infostr
                /*vhp.guestbook.imagefile = t-data.imagefile*/
            .

            pointer = BASE64-DECODE(base64file).
            COPY-LOB pointer TO vhp.guestbook.imagefile.
            base64file = "".
            mess-result = "1 - Successfully Created".
        END.
        EMPTY TEMP-TABLE t-data.
    END.
    WHEN 2 THEN /*Update*/
    DO: 
        FIND FIRST t-data NO-LOCK NO-ERROR.
        IF AVAILABLE t-data THEN 
        DO:
            FIND FIRST vhp.guestbook WHERE vhp.guestbook.gastnr = t-data.gastnr NO-ERROR.
            IF AVAILABLE vhp.guestbook THEN 
            DO:
                ASSIGN
                    vhp.guestbook.infostr = t-data.infostr
                    vhp.guestbook.orig-infostr = t-data.orig-infostr
                .
                /*IF t-data.imagefile NE ? THEN vhp.guestbook.imagefile = t-data.imagefile.*/
                IF base64file NE "" THEN
                DO:
                    pointer = BASE64-DECODE(base64file).
                    COPY-LOB pointer TO vhp.guestbook.imagefile.
                END.
                mess-result = "21 - Successfully Updated".
            END.
            ELSE 
            DO:
                CREATE vhp.guestbook.
                ASSIGN
                    vhp.guestbook.gastnr = t-data.gastnr
                    vhp.guestbook.infostr = t-data.infostr
                    vhp.guestbook.orig-infostr = t-data.orig-infostr
                    /*vhp.guestbook.imagefile = t-data.imagefile*/
                .
                pointer = BASE64-DECODE(base64file).
                COPY-LOB pointer TO vhp.guestbook.imagefile.
                mess-result = "22 - Successfully Created".
            END.
            base64file = "".
        END.
        EMPTY TEMP-TABLE t-data.
    END.
    WHEN 3 THEN /*Read*/
    DO: 
        EMPTY TEMP-TABLE t-data.
        FIND FIRST vhp.guestbook WHERE vhp.guestbook.gastnr = tGastnr NO-LOCK NO-ERROR.
        IF AVAILABLE vhp.guestbook THEN 
        DO:
            CREATE t-data.
            ASSIGN
                t-data.gastnr         = vhp.guestbook.gastnr   
                t-data.infostr        = vhp.guestbook.infostr 
                t-data.orig-infostr   = vhp.guestbook.orig-infostr
                /*t-data.imagefile      = vhp.guestbook.imagefile*/
            .
            COPY-LOB vhp.guestbook.imagefile TO pointer.
            base64file = BASE64-ENCODE(pointer).
            mess-result = "3 - Successfully Loaded".
        END.
        ELSE EMPTY TEMP-TABLE t-data.
    END.
    WHEN 4 THEN /*Delete*/
    DO: 
        FIND FIRST vhp.guestbook WHERE vhp.guestbook.gastnr = tGastnr NO-ERROR.
        IF AVAILABLE vhp.guestbook THEN 
        DO:
            DELETE vhp.guestbook.
            mess-result = "4 - Successfully Deleted".
        END.            
        EMPTY TEMP-TABLE t-data.
    END.
    WHEN 5 THEN /*Get MD5 Sums*/
    DO: 
        FIND FIRST vhp.guestbook WHERE vhp.guestbook.gastnr = tGastnr NO-LOCK NO-ERROR.
        IF AVAILABLE vhp.guestbook THEN
        DO:
            outStr = vhp.guestbook.orig-infostr.
            mess-result = "5 - Successfully Generated MD5".
        END.            
        EMPTY TEMP-TABLE t-data.
    END.
END CASE.
