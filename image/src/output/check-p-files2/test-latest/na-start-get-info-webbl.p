DEFINE TEMP-TABLE plist
    FIELD bezeich AS CHAR FORMAT "x(50)"
    FIELD progres AS CHAR FORMAT "x(10)"
 .

DEFINE OUTPUT PARAMETER na-done AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR plist.

DEFINE VARIABLE inpFile    AS CHAR NO-UNDO.
DEFINE VARIABLE lic-nr     AS CHAR NO-UNDO.
DEFINE VARIABLE search-txt AS CHAR NO-UNDO.
DEFINE VARIABLE temp-char  AS CHAR NO-UNDO.
DEFINE STREAM s1.

/*
FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR.
IF AVAILABLE paramtext THEN 
    RUN decode-string(paramtext.ptexte, OUTPUT lic-nr).

ASSIGN inpFile = "/usr1/vhp/tmp/logNA_" + lic-nr + ".txt".
IF SEARCH(inpFile) = ? THEN ASSIGN na-done = YES.

INPUT STREAM s1 FROM VALUE(inpFile).
REPEAT:
    IMPORT STREAM s1 UNFORMATTED temp-char.
    IF temp-char NE "" THEN DO:
        CREATE plist.
        ASSIGN
            plist.bezeich = ENTRY(1, temp-char, ";")
            plist.progres = ENTRY(2, temp-char, ";")
         .
    END.   
END.
INPUT STREAM s1 CLOSE.*/

FOR EACH plist:
    DELETE plist.
END.

FIND FIRST queasy WHERE queasy.KEY = 232
    AND queasy.date1 = TODAY NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN DO:
    ASSIGN na-done = YES.
    RETURN.
END.

FOR EACH queasy WHERE queasy.KEY = 232
    AND queasy.date1 = TODAY NO-LOCK BY queasy.char3 DESC:
    CREATE plist.
    ASSIGN plist.bezeich = queasy.char2
           plist.progres = queasy.char3
     .
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
