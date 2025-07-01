DEFINE TEMP-TABLE value-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD value-str AS CHAR FORMAT "x(20)".

DEFINE TEMP-TABLE signature-list
    FIELD var-name AS CHAR FORMAT "x(20)"
    FIELD signature AS CHAR FORMAT "x(40)".

/**/
DEFINE INPUT PARAMETER user-name AS CHARACTER.
DEFINE INPUT PARAMETER id-str AS CHARACTER.
DEFINE INPUT PARAMETER grp-no AS INTEGER.
DEFINE OUTPUT PARAMETER passwd-ok AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER epoch-signature AS INT64.
DEFINE OUTPUT PARAMETER TABLE FOR signature-list.

/*
DEFINE VARIABLE user-name AS CHARACTER INIT "sindata".
DEFINE VARIABLE id-str    AS CHARACTER INIT "59YC>9jmi3e4b^?<".
DEFINE VARIABLE grp-no    AS INTEGER   INIT 99.
DEFINE VARIABLE passwd-ok AS LOGICAL INIT NO.
DEFINE VARIABLE epoch-signature AS INT64.
*/
DEFINE VARIABLE fchar AS CHARACTER.
DEFINE VARIABLE pswd-str AS CHARACTER.
DEFINE VARIABLE nanci AS CHARACTER.
DEFINE VARIABLE s AS CHARACTER.
DEFINE VARIABLE i AS INTEGER.

DEFINE VARIABLE licenseNr AS CHARACTER.
FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT licenseNr). 

IF grp-no = 10 THEN
DO:
    RUN htpchar.p (1071, OUTPUT fchar).
    IF TRIM(fchar) = "" THEN
    DO:
        passwd-ok = YES.
        RUN gen-signature.
        RETURN.
    END.
    pswd-str = fchar.
END.

IF grp-no = 10 THEN nanci = pswd-str.
ELSE IF grp-no = 99 THEN
DO:
    DO i = 1 TO 9: 
        RUN aufbau(i, INPUT-OUTPUT nanci). 
    END. 
    
    s = s + SUBSTR(STRING(month(today),"99"),2,1) 
    + SUBSTR(STRING(month(today),"99"),1,1) 
    + SUBSTR(STRING(day(today),"99"),2,1) 
    + SUBSTR(STRING(day(today),"99"),1,1). 
    nanci = nanci + s. 
END.

IF nanci = id-str THEN  passwd-ok = YES.
RUN gen-signature.
/*
DISP epoch-signature FORMAT "" passwd-ok.
FOR EACH signature-list:
    DISP signature-list.
END.
*/
PROCEDURE aufbau: 
  DEFINE INPUT PARAMETER i AS INTEGER. 
  DEFINE INPUT-OUTPUT PARAMETER ch AS CHAR. 

  /* geheimmis */
  IF SUBSTRING(PROVERSION, 1, 1) = "1" THEN
  DO:
    IF i = 1 THEN ch = ch + "g". 
    ELSE IF i = 2 OR i = 4 THEN ch = ch + "e". 
    ELSE IF i = 3 THEN ch = ch + "h". 
    ELSE IF i = 5 OR i = 8 THEN ch = ch + "i". 
    ELSE IF i = 6 OR i = 7 THEN ch = ch + "n". 
    ELSE IF i = 9 THEN ch = ch + "s". 
  END.
  ELSE
  DO:
    IF i = 1 THEN ch = ch + "g". 
    ELSE IF i = 2 OR i = 4 THEN ch = ch + "e". 
    ELSE IF i = 3 THEN ch = ch + "h". 
    ELSE IF i = 5 OR i = 8 THEN ch = ch + "i". 
    ELSE IF i = 6 OR i = 7 THEN ch = ch + "m". 
    ELSE IF i = 9 THEN ch = ch + "s". 
  END.
END.

PROCEDURE gen-signature:
    CREATE value-list.
    ASSIGN
        value-list.var-name  = "passwdOk"
        value-list.value-str = STRING(passwd-ok).
    
    RUN create-signature(user-name,TABLE value-list, OUTPUT epoch-signature, OUTPUT TABLE signature-list).
END.

PROCEDURE create-signature:
    DEF INPUT PARAMETER user-name AS CHAR.
    DEF INPUT PARAMETER TABLE FOR value-list.
    DEF OUTPUT PARAMETER epoch AS INT64.
    DEF OUTPUT PARAMETER TABLE FOR signature-list.

    DEF VAR dtz1      AS DATETIME-TZ.
    DEF VAR dtz2      AS DATETIME-TZ.
    DEF VAR data      AS CHAR.
    DEF VAR value-str AS CHAR.

    dtz1 = NOW.
    dtz2 = 1970-01-01T00:00:00.000+0:00.

    epoch = INTERVAL(dtz1, dtz2, "milliseconds").

    FOR EACH value-list:
        value-str = LC(value-list.value-str).

        CASE value-str:
            WHEN "yes" THEN value-str = "true".
            WHEN "no" THEN value-str = "false".
        END CASE.

        data = value-str + "-" + STRING(epoch) + "-" + STRING(licenseNr) + "-" + LC(user-name).

        CREATE signature-list.
        signature-list.var-name = value-list.var-name.
        signature-list.signature = HEX-ENCODE(SHA1-DIGEST(data)).
    END.
END.

PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
    s   = in-str. 
    j   = ASC(SUBSTR(s, 1, 1)) - 70. 
    len = LENGTH(in-str) - 1. 
    s   = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
    END. 
END.
