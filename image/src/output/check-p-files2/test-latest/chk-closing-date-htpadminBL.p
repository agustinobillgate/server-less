DEF TEMP-TABLE t-htparam LIKE htparam.

DEF INPUT PARAMETER htp-number AS INT.
DEF INPUT PARAMETER user-init  AS CHAR.
DEF INPUT PARAMETER intval     AS INT.
DEF INPUT PARAMETER decval     AS DECIMAL.
DEF INPUT PARAMETER dateval    AS DATE.
DEF INPUT PARAMETER logval     AS LOGICAL.
DEF INPUT PARAMETER charval    AS CHAR.
DEF INPUT PARAMETER htl-name   AS CHAR.

DEF OUTPUT PARAMETER htp-wert AS CHAR.
DEF OUTPUT PARAMETER htp-logv AS LOGICAL.
DEF OUTPUT PARAMETER htp-note AS CHAR.
DEF OUTPUT PARAMETER zahl     AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-htparam.

RUN update-htparam. 

FOR EACH htparam WHERE htparam.paramgr = 40 NO-LOCK:
    CREATE t-htparam.
    BUFFER-COPY htparam TO t-htparam.
END.

PROCEDURE update-htparam: 
DEFINE VARIABLE htpchar AS CHAR FORMAT "x(16)". 
DEFINE VARIABLE lic-nr AS CHAR INITIAL "". 
  FIND FIRST htparam WHERE htparam.paramnr = htp-number EXCLUSIVE-LOCK. 
 
  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
  CREATE res-history. 
  ASSIGN 
      res-history.nr = bediener.nr 
      res-history.datum = TODAY 
      res-history.zeit = TIME 
      res-history.aenderung = "Change ParamNo " + STRING(htparam.paramnr) 
        + ": " 
      res-history.action = "htparam". 
 
  IF htparam.feldtyp = 1 THEN 
  DO: 
    res-history.aenderung = res-history.aenderung 
      + STRING(htparam.finteger) + " TO: " + STRING(intval). 
    htparam.finteger = intval. 
    htp-wert = STRING(htparam.finteger). 
  END. 
  ELSE IF htparam.feldtyp = 2 THEN 
  DO: 
    res-history.aenderung = res-history.aenderung 
      + STRING(htparam.fdecimal) + " TO: " + STRING(decval). 
    htparam.fdecimal = decval. 
    htp-wert = STRING(htparam.fdecimal). 
  END. 
  ELSE IF htparam.feldtyp = 3 THEN 
  DO: 
    res-history.aenderung = res-history.aenderung 
      + STRING(htparam.fdate) + " TO: " + STRING(dateval). 
    htparam.fdate = dateval. 
    htp-wert = STRING(htparam.fdate). 
  END. 
  ELSE IF htparam.feldtyp = 4 THEN 
  DO: 
    res-history.aenderung = res-history.aenderung 
      + STRING(htparam.flogical) + " TO: " + STRING(logval). 
    htparam.flogical = logval. 
    htp-wert = STRING(htparam.flogical). 
    htp-logv = htparam.flogical. 
  END. 
  ELSE IF feldtyp = 5 THEN 
  DO: 
    res-history.aenderung = res-history.aenderung 
      + STRING(htparam.fchar) + " TO: " + STRING(charval). 
    htparam.fchar = charval. 
    htp-wert = STRING(htparam.fchar). 
  END. 
 
  htparam.lupdate = today. 
  htparam.fdefault = user-init + " - " + STRING(time, "HH:MM:SS"). 
  htp.lupdate = htparam.lupdate. 
  htp-note = htparam.fdefault. 
 
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history. 
 
  IF htparam.paramgruppe = 99 OR htparam.paramgruppe = 100 THEN 
  DO: 
    FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
    IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
    DO: 
      RUN decode-string(ptexte, OUTPUT lic-nr). 
      htpchar = "". 
      IF htparam.feldtyp = 1 THEN  /* INTEGER */ 
        htpchar = STRING(lic-nr,"x(4)") + STRING(paramnr,"9999") 
          + STRING(finteger,"9999"). 
      IF htparam.feldtyp = 3 THEN /* DATE */ 
        htpchar = STRING(lic-nr,"x(4)") + STRING(paramnr,"9999") 
          + STRING(month(fdate),"99") 
          + STRING(day(fdate),"99") 
          + STRING(year(fdate),"9999"). 
      ELSE IF feldtyp = 4 THEN 
        htpchar = STRING(lic-nr,"x(4)") + STRING(paramnr,"9999") 
          + STRING(flogical). 
      RUN encode-string(htpchar, OUTPUT htpchar). 
      htparam.fchar = htpchar. 
    END. 
  END. 
 
  IF htparam.paramnr = 976 THEN 
  DO: 
    FIND FIRST paramtext WHERE paramtext.txtnr = 976 EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE paramtext THEN 
    DO: 
      paramtext.ptexte = STRING(htparam.fdate,"99/99/9999"). 
      paramtext.notes = htparam.fchar. 
      FIND CURRENT paramtext NO-LOCK. 
    END. 
    IF SUBSTRING(PROVERSION, 1, 1) = "1" THEN
      RUN encode-serial(lic-nr, htparam.fdate, htl-name).
  END. 

  FIND CURRENT htparam NO-LOCK. 
END. 



PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = asc(SUBSTR(s, 1, 1)) - 70. 
  len = length(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO length(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 


PROCEDURE encode-string: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR. 
DEFINE VARIABLE s AS CHAR FORMAT "x(50)". 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
DEFINE VARIABLE ch AS CHAR. 
 
  j = random(1,9). 
  ch = CHR(ASC(STRING(j)) + 23). 
  out-str = ch. 
  j = asc(ch) - 70. 
  DO len = 1 TO length(in-str): 
    out-str = out-str + chr(asc(SUBSTR(in-str,len,1)) + j). 
  END. 
END. 


PROCEDURE encode-serial:
DEF INPUT PARAM license     AS CHAR.
DEF INPUT PARAM curr-date   AS DATE. 
DEF INPUT PARAM hotel       AS CHAR.

DEF VARIABLE datum          AS CHAR.
DEF VARIABLE str1           AS CHAR.
DEF VARIABLE str2           AS CHAR.

DEF VAR license-enc AS CHAR INITIAL "".
DEF VAR datum-1-enc AS CHAR INITIAL "".
DEF VAR datum-2-enc AS CHAR INITIAL "".
DEF VAR schluessel  AS CHAR INITIAL "".

DEF VAR nama1 AS CHAR INITIAL "".
DEF VAR nama2 AS CHAR INITIAL "".
DEF VAR nama3 AS CHAR INITIAL "".
DEF VAR nama4 AS CHAR INITIAL "".

  ASSIGN datum = STRING(MONTH(curr-date), "99") +
                 STRING(DAY(curr-date),   "99") +
                 STRING(YEAR(curr-date),  "9999").

  RUN encode-all(license, datum, OUTPUT datum-1-enc, OUTPUT license-enc, OUTPUT datum-2-enc, OUTPUT schluessel).
  RUN encode-hotel(datum-2-enc, schluessel, datum-1-enc, license-enc, hotel, OUTPUT nama1, OUTPUT nama2, OUTPUT nama3, OUTPUT nama4).

  ASSIGN
    str1 = datum-1-enc + " " + license-enc + " " + datum-2-enc + " " + schluessel
    str2 = nama1 + " " + nama2 + " " + nama3 + " " + nama4.

  FIND FIRST paramtext WHERE paramtext.txtnr = 200 NO-ERROR.
  IF AVAILABLE paramtext THEN paramtext.passwort = str1.
  FIND FIRST paramtext WHERE paramtext.txtnr = 203 NO-ERROR.
  IF AVAILABLE paramtext THEN paramtext.passwort = str2.  

END.


PROCEDURE encode-all:

    DEF INPUT PARAMETER license AS CHAR.
    DEF INPUT PARAMETER datum AS CHAR.

    DEF OUTPUT PARAMETER license3 AS CHAR INITIAL "".
    DEF OUTPUT PARAMETER datum1-teil1 AS CHAR INITIAL "".
    DEF OUTPUT PARAMETER datum1-teil2 AS CHAR INITIAL "".
    DEF OUTPUT PARAMETER schluessel AS CHAR INITIAL "".
    
    DEF VAR datum2 AS CHAR.
    DEF VAR license2 AS CHAR.
    DEF VAR datum-teil1 AS CHAR.
    DEF VAR datum-teil2 AS CHAR.
    DEF VAR flag AS LOGICAL INITIAL YES.
    DEF VAR accept AS LOGICAL INITIAL NO.
    DEF VAR accept1 AS LOGICAL INITIAL NO.

    DO WHILE (flag):

        ASSIGN 
            zahl = "".

        RUN encode-serial-str(license, NO, OUTPUT license2).
        RUN encode-serial-str(datum, NO, OUTPUT datum2).

        RUN cutword(datum2, OUTPUT datum-teil1, OUTPUT datum-teil2).

        RUN encode-serial-str(zahl, YES, OUTPUT zahl).
        RUN encode-serial-str(zahl, YES, OUTPUT zahl).

        ASSIGN
            schluessel = zahl.

        RUN modulo-check(schluessel, OUTPUT accept1).

        IF accept1 THEN
        DO:

            RUN encode-next(datum-teil2, schluessel, OUTPUT datum1-teil2).
            RUN encode-next(license2, datum1-teil2, OUTPUT license3).
            RUN encode-next(datum-teil1, license3, OUTPUT datum1-teil1).
            
            RUN serial-check(license3, datum1-teil1, datum1-teil2, schluessel, OUTPUT accept).
            
            IF accept THEN
            DO:
                flag = FALSE.
            END.
        END.
    END.
END.



PROCEDURE encode-hotel:
    DEF INPUT PARAMETER datum2 AS CHAR.
    DEF INPUT PARAMETER schluessel AS CHAR.
    DEF INPUT PARAMETER datum1 AS CHAR.
    DEF INPUT PARAMETER license AS CHAR.
    DEF INPUT PARAMETER hotel AS CHAR.
    
    DEF OUTPUT PARAMETER name1 AS CHAR INITIAL "".
    DEF OUTPUT PARAMETER name2 AS CHAR INITIAL "".
    DEF OUTPUT PARAMETER name3 AS CHAR INITIAL "".
    DEF OUTPUT PARAMETER name4 AS CHAR INITIAL "".

    RUN encode-name(datum2, hotel, 1, OUTPUT name1).
    RUN encode-name(schluessel, hotel, 2, OUTPUT name2).
    RUN encode-name(datum1, hotel, 3, OUTPUT name3).
    RUN encode-name(license, hotel, 4, OUTPUT name4).

END.


PROCEDURE encode-serial-str: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE INPUT PARAMETER prefix AS LOGICAL.
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "".

DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
DEFINE VARIABLE len1 AS INTEGER.
DEFINE VARIABLE ch AS CHAR INITIAL "". 
  
    ASSIGN
      j = RANDOM(1,12)
      ch = CHR(ASC(STRING(j)) + 27)
      zahl = zahl + ch.
  
  IF prefix THEN
  DO:
      ASSIGN 
          out-str = ch
          j = ASC(ch) - 70.
  END.
  ELSE
  DO:
      ASSIGN j = ASC(ch) - 49.

  END.
  DO len = 1 TO length(in-str): 
    ASSIGN 
        len1 = (13 * len) MODULO 5 + 6
        out-str = out-str + chr(asc(SUBSTR(in-str,len,1)) + j - len1). 
  END. 
END. 


PROCEDURE cutword:
DEFINE INPUT PARAMETER word AS CHAR.
DEFINE OUTPUT PARAMETER teil1 AS CHAR INITIAL "".
DEFINE OUTPUT PARAMETER teil2 AS CHAR INITIAL "".

DEFINE VAR len AS INT.
DEFINE VAR halb AS INT.

ASSIGN
    len = LENGTH(word)
    halb = len / 2
    teil1 = SUBSTR(word,1,halb)
    teil2 = SUBSTR(word, halb + 1,halb).
END.


PROCEDURE modulo-check:
    DEFINE INPUT PARAMETER wort AS CHAR.
    DEFINE OUTPUT PARAMETER accept-key AS LOGICAL INITIAL NO.

    DEFINE VARIABLE i AS INTEGER.
    DEFINE VARIABLE summe AS INTEGER INITIAL 0.

    DO  i = 1 TO LENGTH(wort).
        summe = summe + (ASC(SUBSTR(wort,i,1)) - 64) + i.
    END.

    IF (summe MODULO 13) = 0 THEN
    DO:
        accept-key = TRUE.
    END.
END.


PROCEDURE encode-next:
    DEFINE INPUT PARAMETER in-str AS CHAR.
    DEFINE INPUT PARAMETER schluessel AS CHAR.
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "".

    DEFINE VARIABLE schluessel1 AS INT.
    DEFINE VARIABLE len AS INTEGER.
    DEFINE VARIABLE reverse AS INTEGER.
    DEFINE VARIABLE len1 AS INTEGER.

    DO len = 1 TO length(in-str): 
        ASSIGN
         reverse = LENGTH(in-str) - len + 1
         schluessel1 = asc(SUBSTR(schluessel,reverse,1)) MODULO 7 - 1
         out-str = out-str + chr(asc(SUBSTR(in-str,len,1)) - schluessel1 + len + 5).
    END. 
END.


PROCEDURE serial-check:
    DEFINE INPUT PARAMETER wort1 AS CHAR.
    DEFINE INPUT PARAMETER wort2 AS CHAR.
    DEFINE INPUT PARAMETER wort3 AS CHAR.
    DEFINE INPUT PARAMETER wort4 AS CHAR.
    DEFINE OUTPUT PARAMETER accept AS LOGICAL INITIAL YES.

    DEFINE VAR i AS INT.
    DEFINE VAR j AS INT.
    DEFINE VAR alpha AS INT.
    DEFINE VAR wort AS CHAR EXTENT 4.

    ASSIGN
        wort[1] = wort1
        wort[2] = wort2
        wort[3] = wort3
        wort[4] = wort4.

    DO i = 1 TO 4:
        DO j = 1 TO 4:
            alpha = asc(SUBSTR(wort[i],j,1)).
            IF alpha < 65 OR alpha > 90 THEN
            DO:
                accept = NO.
            END.
        END.
    END.
END.


PROCEDURE encode-name:
    DEF INPUT PARAMETER in-string AS CHAR.
    DEF INPUT PARAMETER hotel AS CHAR.
    DEF INPUT PARAMETER pos AS INT.
    DEF OUTPUT PARAMETER out-string AS CHAR INITIAL "".

    DEF VAR i AS INT.
    DEF VAR hotel-int AS INT INITIAL 0.
    DEF VAR string-int AS INT INITIAL 0.
    DEF VAR summe AS CHAR.
    DEF VAR len AS INT.

    len = LENGTH(in-string).

    DO i = 1 TO len:
        RUN char-number(SUBSTR(hotel, i + (pos - 1) * 4 , 1), OUTPUT hotel-int).
        RUN char-number(SUBSTR(in-string, i, 1), OUTPUT string-int).
        
        RUN number-char(hotel-int + (2 * string-int MODULO 10) + 1, OUTPUT summe).
        out-string = out-string + summe.
    END.
    
END.


PROCEDURE char-number:
    DEF INPUT PARAMETER in-char AS CHAR.
    DEF OUTPUT PARAMETER out-int AS INT INITIAL 0.

    IF asc(SUBSTR(in-char,1,1)) > 64 AND asc(SUBSTR(in-char,1,1)) < 91 THEN
    DO :
        out-int = asc(SUBSTR(in-char,1,1)) - 64.
    END.

    ELSE IF asc(SUBSTR(in-char,1,1)) > 48 AND asc(SUBSTR(in-char,1,1)) < 58 THEN
    DO:
        out-int = asc(SUBSTR(in-char,1,1)) - 22.
    END.
    ELSE IF asc(SUBSTR(in-char,1,1)) = 32 THEN
    DO:
        out-int = 0.
    END.
END.


PROCEDURE number-char:
    DEF INPUT PARAMETER in-int AS INT.
    DEF OUTPUT PARAMETER out-char AS CHAR INITIAL "".

    IF in-int > 0 AND in-int < 27 THEN
    DO:
        out-char = CHR(in-int + 64).
    END.
    ELSE IF in-int > 26 AND in-int < 37 THEN
    DO:
        out-char = CHR(in-int + 22).
    END.
    ELSE IF in-int = 0 THEN
    DO:
        out-char = " ".
    END.
END.

