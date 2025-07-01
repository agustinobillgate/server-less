DEFINE TEMP-TABLE stream-list
    FIELD crow AS INTEGER
    FIELD ccol AS INTEGER
    FIELD cval AS CHARACTER
    .



DEFINE INPUT PARAMETER gsheet-link   AS CHAR.

DEFINE VARIABLE file-path       AS CHARACTER NO-UNDO.

DEF VAR ch        AS CHAR NO-UNDO.
DEF VAR counter   AS INTEGER NO-UNDO.

DEFINE VARIABLE htl-no     AS CHAR.
DEF VAR crow    AS INTEGER NO-UNDO.
DEF VAR ccol    AS INTEGER NO-UNDO.
DEF VAR cval    AS CHAR NO-UNDO.

DEFINE STREAM s1.
DEFINE STREAM s2.

FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
    RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 

/* file-path = "C:\vhp\php-script\tmp\outputDRR_" + htl-no + ".txt ".  */

file-path = "usr1/vhp/tmp/outputFO_" + htl-no + ".txt ".

IF SEARCH(file-path) = ? THEN RETURN.

INPUT STREAM s1 FROM VALUE(file-path).
counter = 0.
REPEAT:
	IMPORT STREAM s1 UNFORMATTED ch.
	ch = TRIM(ch).
	IF ch = "" THEN .
	ELSE IF counter = 0 THEN .
	ELSE 
	DO:
		crow = INTEGER(ENTRY(1,ch,";")).            
		ccol = INTEGER(ENTRY(2,ch,";")).
        cval = TRIM(ENTRY(3,ch,";")).

			CREATE stream-list.
			ASSIGN 
                stream-list.crow = crow
                stream-list.ccol = ccol
    			stream-list.cval = cval
             .
	END.
    counter = counter + 1.
END.
INPUT STREAM s1 CLOSE.

/*OS-DELETE VALUE ("C:\vhp\php-script\tmp\outputDRR_" + htl-no + ".txt").
OUTPUT STREAM s1 TO VALUE("C:\vhp\php-script\tmp\outputDRR_" + htl-no + ".txt") APPEND UNBUFFERED.*/
OS-DELETE VALUE ("/usr1/vhp/tmp/outputFO_" + htl-no + ".txt").
OUTPUT STREAM s1 TO VALUE("/usr1/vhp/tmp/outputFO_" + htl-no + ".txt") APPEND UNBUFFERED.

FOR EACH stream-list NO-LOCK BY stream-list.crow BY stream-list.ccol:
    IF stream-list.cval NE "" THEN
    PUT STREAM s1 UNFORMATTED 
         STRING(stream-list.crow) ";" STRING(stream-list.ccol) ";" "''" SKIP.
END.

OUTPUT STREAM s1 CLOSE.

/* OS-COMMAND SILENT VALUE("php C:\vhp\php-script\write-sheet.php C:\vhp\php-script\tmp\outputDRR_" + htl-no + ".txt " + gsheet-link).  */

OS-COMMAND SILENT VALUE ("php /usr1/vhp/php-script/write-sheet.php /usr1/vhp/tmp/outputFO_" + htl-no + ".txt " + gsheet-link).

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

