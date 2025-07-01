DEFINE TEMP-TABLE plist
    FIELD bezeich AS CHAR FORMAT "x(50)"
    FIELD progres AS CHAR FORMAT "x(10)"
    FIELD counter AS INTEGER
 .


DEFINE INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER close-done AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER msg-str    AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR plist.

DEFINE VARIABLE inpFile    AS CHAR NO-UNDO.
DEFINE VARIABLE lic-nr     AS CHAR NO-UNDO.
DEFINE VARIABLE search-txt AS CHAR NO-UNDO.
DEFINE VARIABLE temp-char  AS CHAR NO-UNDO.
DEFINE VARIABLE counter    AS INTEGER NO-UNDO.
DEFINE STREAM s1.

{ supertransbl.i }
DEF VAR lvCAREA AS CHAR INITIAL "close-inventory". 

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER mqueasy FOR queasy.


FOR EACH plist:
    DELETE plist.
END.

FOR EACH queasy WHERE queasy.KEY = 279
    AND queasy.date1 = TODAY NO-LOCK BY queasy.number1:
    CREATE plist.
    ASSIGN plist.bezeich = queasy.char2
           plist.progres = queasy.char3
           counter       = counter + 1
           plist.counter = counter
     .
END.

FIND FIRST bqueasy WHERE bqueasy.KEY = 283
    AND bqueasy.date1 = TODAY NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    ASSIGN msg-str    = bqueasy.char1
           close-done = YES
    .
    
    FOR EACH pqueasy WHERE pqueasy.KEY = 279
        AND pqueasy.date1 = TODAY:
        DELETE pqueasy.
    END.
    RETURN.
END.

FIND FIRST bqueasy WHERE bqueasy.KEY = 279
    AND bqueasy.date1 = TODAY NO-LOCK NO-ERROR.
IF NOT AVAILABLE bqueasy THEN DO:
    FIND FIRST mqueasy WHERE mqueasy.KEY = 296
        AND mqueasy.number2 = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE mqueasy THEN ASSIGN close-done = NO.
    ELSE DO: 
        ASSIGN close-done = YES.
        
        FIND FIRST pqueasy WHERE pqueasy.KEY = 296
            AND pqueasy.number2 = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE pqueasy THEN DO:
            FIND CURRENT pqueasy EXCLUSIVE-LOCK.
            DELETE pqueasy.
            RELEASE pqueasy.
        END.
    END.
END.
ELSE DO:
     FIND FIRST mqueasy WHERE mqueasy.KEY = 296
        AND mqueasy.number2 = 0 NO-LOCK NO-ERROR.
     IF AVAILABLE mqueasy THEN DO:
          ASSIGN close-done = YES.

        FIND FIRST pqueasy WHERE pqueasy.KEY = 296
            AND pqueasy.number2 = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE pqueasy THEN DO:
            FIND CURRENT pqueasy EXCLUSIVE-LOCK.
            DELETE pqueasy.
            RELEASE pqueasy.
        END.

        FOR EACH bqueasy WHERE bqueasy.KEY = 279
            AND bqueasy.date1 = TODAY:
            DELETE bqueasy.
        END.
     END.

    /*FIND FIRST bqueasy WHERE bqueasy.KEY = 279
        AND bqueasy.date1 = TODAY
        AND bqueasy.logi1 = YES NO-LOCK NO-ERROR.
    IF AVAILABLE bqueasy THEN DO:
        msg-str = msg-str + CHR(2)
              + translateExtended ("Not updated Stock Onhand found for article :",lvCAREA,"")          
              + CHR(10)              
              + translateExtended ("Fix the possible errors, then restart the program.",lvCAREA,"").

        FOR EACH pqueasy WHERE pqueasy.KEY = 279
            AND pqueasy.date1 = TODAY:
            DELETE pqueasy.
        END.
        RETURN.
    END.*/

END.


