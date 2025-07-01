
DEF TEMP-TABLE t-printer LIKE printer.

DEFINE TEMP-TABLE user-printers 
    FIELD nr AS INTEGER 
    FIELD selected AS LOGICAL INITIAL YES. 


DEF INPUT  PARAMETER session-param AS CHARACTER.
DEF OUTPUT PARAMETER TABLE FOR t-printer.

/*DEFINE VARIABLE session-param AS CHAR.
session-param =
"BeCode=1;RemoteLocal=local;POS=019901;location=C:\vhp10\vhplib\IF;printer-flag=Print;prorder=99;coder=01-01;eKTP=C:\e1-vhp\e-KTP\data\dataktp.xml;localscan=?;SCMODE=ADRIA;PRMODE=LNL;PREVIEWMODE=YES;S3FLAG=YES;INVPATH=C:\e1-vhp\file\".
*/
DEFINE VARIABLE s1 AS CHARACTER.
DEFINE VARIABLE s2 AS CHARACTER.
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE usr-pr-defined  AS LOGICAL INITIAL NO NO-UNDO. 


FOR EACH vhp.printer WHERE vhp.printer.bondrucker = NO 
    AND vhp.printer.opsysname = "DOS" NO-LOCK:
  CREATE t-printer.
  BUFFER-COPY vhp.printer TO t-printer.
END.

FOR EACH t-printer NO-LOCK: 
    CREATE user-printers. 
    user-printers.nr = t-printer.nr. 
END. 

IF session-param MATCHES("*PRINTERS=*") THEN 
DO: 
    FOR EACH user-printers: 
        user-printers.selected = NO. 
    END. 

    s1 = session-param.
    DO i = 1 TO LENGTH(s1): 
        IF SUBSTR(s1,i,9) = "PRINTERS=" THEN 
        DO: 
            s2 = SUBSTR(s1, (i + 9), LENGTH(s1)). 
            i = 999. 
        END. 
    END. 

    s1 = "". 
    DO i = 1 TO LENGTH(s2): 
        IF SUBSTR(s2,i,1) = ";" THEN 
        DO: 
            FIND FIRST user-printers WHERE user-printers.nr = INTEGER(s1) 
                NO-ERROR. 
            IF AVAILABLE user-printers THEN user-printers.selected = YES. 
            usr-pr-defined = YES. 
            RETURN. 
        END. 

        IF SUBSTR(s2,i,1) = "," THEN 
        DO: 
            FIND FIRST user-printers WHERE user-printers.nr = INTEGER(s1) 
                NO-ERROR. 
            IF AVAILABLE user-printers THEN user-printers.selected = YES. 
            s1 = "". 
        END. 
        ELSE IF SUBSTR(s2,i,1) GE "0" AND SUBSTR(s2,i,1) LE "9" THEN 
            s1 = s1 + SUBSTR(s2,i,1). 
    END. 
    usr-pr-defined = YES. 
END. 

FOR EACH t-printer:
    FIND FIRST user-printers WHERE user-printers.nr = t-printer.nr 
        AND user-printers.selected NO-LOCK NO-ERROR.
    IF NOT AVAILABLE user-printers THEN
        DELETE t-printer.
END.


    

