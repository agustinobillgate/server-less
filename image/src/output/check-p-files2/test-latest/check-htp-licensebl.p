DEF OUTPUT PARAMETER lstopped AS LOGICAL NO-UNDO.
RUN check-htp-license(OUTPUT lstopped).

PROCEDURE check-htp-license: 
DEFINE OUTPUT PARAMETER lstopped AS LOGICAL INITIAL NO. 
DEFINE VARIABLE lic-nr AS CHAR. 
DEFINE VARIABLE lic-nr1 AS CHAR. 
DEFINE VARIABLE nr1 AS INTEGER. 
DEFINE VARIABLE flogic1 AS LOGICAL. 
DEFINE VARIABLE fint1 AS INTEGER. 
DEFINE VARIABLE fdate1 AS DATE. 
DEFINE VARIABLE STR AS CHAR FORMAT "x(16)". 
DEFINE VARIABLE s AS CHAR. 
DEFINE buffer htp FOR htparam. 
 
  FIND FIRST htparam WHERE paramnr = 976 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE htparam OR (AVAILABLE htparam AND htparam.fdate = ?) THEN 
  DO: 
    lstopped = YES. 
    RETURN. 
  END. 
 
  FIND FIRST paramtext WHERE paramtext.txtnr = 976 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE paramtext THEN 
  DO: 
    create paramtext. 
    paramtext.txtnr = 976. 
    paramtext.ptexte = STRING(htparam.fdate,"99/99/9999"). 
    paramtext.notes = htparam.fchar. 
    release paramtext. 
  END. 
  ELSE 
  DO: 
    IF paramtext.notes NE htparam.fchar THEN 
    DO: 
      lstopped = YES. 
      RETURN. 
    END. 
  END. 
 
  FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
  IF AVAILABLE paramtext AND ptexte NE "" THEN 
    RUN decode-string(ptexte, OUTPUT lic-nr). 
  ELSE 
  DO: 
    lstopped = YES. 
    RETURN. 
  END. 

  FOR EACH htparam WHERE htparam.paramgruppe = 99 
    AND (htparam.feldtyp = 1 OR htparam.feldtyp = 3 OR htparam.feldtyp = 4) NO-LOCK: 
    RUN decode-string(htparam.fchar, OUTPUT STR). 
    IF htparam.feldtyp = 1 THEN 
    DO: 
      lic-nr1 = SUBSTR(STR,1,4). 
      nr1 = INTEGER(SUBSTR(STR,5,4)). 
      fint1 = INTEGER(SUBSTR(STR,9,4)). 
      IF fint1 NE htparam.finteger THEN 
      DO: 
        FIND FIRST htp WHERE htp.paramnr = htparam.paramnr EXCLUSIVE-LOCK. 
        htp.finteger = fint1. 
        FIND CURRENT htp NO-LOCK. 
      END. 
    END. 
    ELSE IF htparam.feldtyp = 3 THEN /* DATE */ 
    DO: 
      lic-nr1 = SUBSTR(STR,1,4). 
      nr1 = INTEGER(SUBSTR(STR,5,4)). 
      s = SUBSTR(STR,9,8). 
      fdate1 = DATE(INTEGER(SUBSTR(s,1,2)), INTEGER(SUBSTR(s,3,2)), 
        INTEGER(SUBSTR(s,5,4))). 
      IF fdate1 NE htparam.fdate THEN 
      DO: 
        FIND FIRST htp WHERE htp.paramnr = htparam.paramnr EXCLUSIVE-LOCK. 
        IF fdate1 = ? THEN htp.fdate = ?. 
        ELSE htp.fdate = fdate1. 
        FIND CURRENT htp NO-LOCK. 
      END. 
    END. 
    ELSE IF htparam.feldtyp = 4 THEN 
    DO: 
      lic-nr1 = SUBSTR(STR,1,4). 
      nr1 = INTEGER(SUBSTR(STR,5,4)). 
      flogic1 = (SUBSTR(STR,9,3) = "YES"). 
      IF flogic1 NE htparam.flogical AND flogic1 = NO THEN 
      DO: 
        FIND FIRST htp WHERE htp.paramnr = htparam.paramnr EXCLUSIVE-LOCK. 
        htp.flogical = flogic1. 
        FIND CURRENT htp NO-LOCK. 
      END. 
    END. 
/*
    DISP  htparam.fchar STR nr1 htparam.paramnr. 
*/ 
    DO:
/*      
      DISP lic-nr1 lic-nr nr1 htparam.paramnr.
*/
      IF (INTEGER(lic-nr1) NE INTEGER(lic-nr)) OR (nr1 NE htparam.paramnr) THEN 
      DO:    
          IF htparam.feldtyp = 4 AND htparam.flogical = YES THEN lstopped = YES.
          ELSE IF htparam.feldtyp NE 4 THEN lstopped = YES.
      END.
    END.
  END.

END. 
  
PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = length(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO length(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 
