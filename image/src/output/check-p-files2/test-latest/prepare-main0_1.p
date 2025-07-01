/* ADD new output parameter newDB as LOGICAL */

DEF TEMP-TABLE t-queasy LIKE queasy.

DEF INPUT  PARAMETER pvILanguage AS INTEGER        NO-UNDO.

DEF OUTPUT PARAMETER lstopped    AS LOGICAL INIT NO  NO-UNDO.
DEF OUTPUT PARAMETER lic-nr      AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER htl-name    AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER h-name      AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER htl-city    AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER h-city      AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER htl-adr     AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER htl-tel     AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER vhp-multi   AS LOGICAL          NO-UNDO.
DEF OUTPUT PARAMETER vhp-lite    AS LOGICAL          NO-UNDO.
DEF OUTPUT PARAMETER rest-lic    AS LOGICAL          NO-UNDO.
DEF OUTPUT PARAMETER eng-dept    AS INTEGER          NO-UNDO.
DEF OUTPUT PARAMETER i-param111  AS INTEGER          NO-UNDO.
DEF OUTPUT PARAMETER i-param297  AS INTEGER          NO-UNDO.
DEF OUTPUT PARAMETER p-decimal   AS INTEGER          NO-UNDO.
DEF OUTPUT PARAMETER d-currency  AS LOGICAL          NO-UNDO.
DEF OUTPUT PARAMETER msg-str     AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER coa-format  AS CHAR             NO-UNDO.
DEF OUTPUT PARAMETER dateFlag    AS DATE             NO-UNDO.
DEF OUTPUT PARAMETER lic-room    AS INTEGER INIT 0   NO-UNDO.
DEF OUTPUT PARAMETER lic-pos     AS INTEGER INIT 0   NO-UNDO.
DEF OUTPUT PARAMETER condo-flag  AS LOGICAL          NO-UNDO.
DEF OUTPUT PARAMETER newDB       AS LOGICAL          NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

DEF VARIABLE p-787          AS CHAR      NO-UNDO.
DEF VARIABLE p-223          AS LOGICAL   NO-UNDO.
DEF VARIABLE loyalty-flag   AS LOGICAL   NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "main0". 

FIND FIRST bediener WHERE SUBSTR(bediener.username, LENGTH(bediener.username), 1) = CHR(2)
    NO-LOCK NO-ERROR.
newDB = AVAILABLE bediener.

RUN htpchar.p(787, OUTPUT p-787).
RUN htplogic.p(223, OUTPUT p-223).
ASSIGN
    loyalty-flag = (p-787 NE "") AND (p-223 = YES)
    msg-str      = STRING(loyalty-flag) + CHR(3)
.

RUN check-htp (OUTPUT lstopped). 
IF lstopped THEN RETURN. 

RUN decode-strings.  /* paramtext FOR hotel name, city AND lic NO */ 
IF lstopped THEN RETURN. 
 
IF SUBSTRING(PROVERSION, 1, 1) = "1" THEN
DO:
  RUN decode-serial(OUTPUT lstopped).
  IF lstopped THEN RETURN.
END.

RUN check-room-pos-license(OUTPUT lstopped).
IF lstopped THEN RETURN. 
 
RUN htpchar.p  (977, OUTPUT coa-format).

RUN htplogic.p (240, OUTPUT d-currency).
RUN htplogic.p (990, OUTPUT rest-lic).
RUN htplogic.p (996, OUTPUT vhp-multi).
RUN htplogic.p (1015, OUTPUT vhp-lite).

RUN htpint.p   (111, OUTPUT i-param111).
RUN htpint.p   (297, OUTPUT i-param297).
RUN htpint.p   (491, OUTPUT p-decimal).
RUN htpint.p   (1060, OUTPUT eng-dept).

RUN htpdate.p  (976, OUTPUT dateFlag).
RUN htpint.p   (975, OUTPUT lic-room).
RUN htpint.p   (989, OUTPUT lic-pos).

RUN htplogic.p (981, OUTPUT condo-flag).  /* License FOR Condominium */ 

FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.queasy THEN
DO:
  CREATE t-queasy.
  BUFFER-COPY queasy TO t-queasy.
END.

PROCEDURE check-htp: 
DEFINE OUTPUT PARAMETER lstopped    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE flogic1             AS LOGICAL. 
DEFINE VARIABLE lic-nr              AS CHAR. 
DEFINE VARIABLE lic-nr1             AS CHAR. 
DEFINE VARIABLE str1                AS CHAR FORMAT "x(16)". 
DEFINE VARIABLE s                   AS CHAR. 
DEFINE VARIABLE nr1                 AS INTEGER. 
DEFINE VARIABLE fint1               AS INTEGER. 
DEFINE VARIABLE fdate1              AS DATE. 

DEFINE BUFFER htp FOR htparam. 
 
  FIND FIRST htparam WHERE paramnr = 976 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE htparam OR (AVAILABLE htparam AND htparam.fdate = ?) THEN 
  DO: 
    lstopped = YES. 
    RETURN. 
  END. 
 
  FIND FIRST paramtext WHERE paramtext.txtnr = 976 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE paramtext THEN 
  DO: 
    CREATE paramtext. 
    ASSIGN
      paramtext.txtnr  = 976 
      paramtext.ptexte = STRING(htparam.fdate,"99/99/9999") 
      paramtext.notes  = htparam.fchar
    . 
    RELEASE paramtext. 
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
    RUN decode-string(htparam.fchar, OUTPUT str1). 
    IF htparam.feldtyp = 1 THEN 
    DO: 
      ASSIGN
        lic-nr1 = SUBSTR(str1,1,4)
        nr1     = INTEGER(SUBSTR(str1,5,4))
        fint1   = INTEGER(SUBSTR(str1,9,4))
      . 
      IF fint1 NE htparam.finteger THEN 
      DO: 
        FIND FIRST htp WHERE htp.paramnr = htparam.paramnr EXCLUSIVE-LOCK. 
        htp.finteger = fint1. 
        FIND CURRENT htp NO-LOCK. 
      END. 
    END. 
    ELSE IF htparam.feldtyp = 3 THEN /* DATE */ 
    DO:
      ASSIGN
        lic-nr1 = SUBSTR(str1,1,4) 
        nr1     = INTEGER(SUBSTR(str1,5,4)) 
        s       = SUBSTR(str1,9,8)
        fdate1  = DATE(INTEGER(SUBSTR(s,1,2)), INTEGER(SUBSTR(s,3,2)), 
          INTEGER(SUBSTR(s,5,4)))
      . 
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
      ASSIGN
        lic-nr1 = SUBSTR(str1,1,4)
        nr1     = INTEGER(SUBSTR(str1,5,4)) 
        flogic1  = (SUBSTR(str1,9,3) = "YES")
      . 
      IF flogic1 NE htparam.flogical AND flogic1 = NO THEN 
      DO: 
        FIND FIRST htp WHERE htp.paramnr = htparam.paramnr EXCLUSIVE-LOCK. 
        htp.flogical = flogic1. 
        FIND CURRENT htp NO-LOCK. 
      END. 
    END. 
    IF (INTEGER(lic-nr1) NE INTEGER(lic-nr)) OR (nr1 NE htparam.paramnr) THEN 
    DO:    
      IF htparam.feldtyp = 4 AND htparam.flogical = YES THEN lstopped = YES.
      ELSE IF htparam.feldtyp NE 4 THEN lstopped = YES.
    END.
  END.
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

PROCEDURE decode-strings: 
DEFINE VARIABLE s     AS CHAR FORMAT "x(50)". 
DEFINE VARIABLE j     AS INTEGER. 
DEFINE VARIABLE len   AS INTEGER. 
 
  htl-name = "". 
  FIND FIRST paramtext WHERE txtnr = 240 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE paramtext THEN lstopped = YES. 
  IF ptexte = "" THEN lstopped = YES. 
  IF AVAILABLE paramtext AND ptexte NE "" THEN 
    RUN decode-string(ptexte, OUTPUT htl-name). 
 
  htl-city = "". 
  FIND FIRST paramtext WHERE txtnr = 242 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE paramtext THEN lstopped = YES. 
  IF ptexte = "" THEN lstopped = YES. 
  IF AVAILABLE paramtext AND ptexte NE "" THEN 
    RUN decode-string(ptexte, OUTPUT htl-city). 
 
  htl-adr = "". 
  FIND FIRST paramtext WHERE txtnr = 201 NO-ERROR.
  IF AVAILABLE paramtext THEN htl-adr = paramtext.ptexte.

  htl-tel = "". 
  FIND FIRST paramtext WHERE txtnr = 204 NO-ERROR. 
  IF AVAILABLE paramtext THEN htl-tel = paramtext.ptexte.

  lic-nr = "". 
  FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE paramtext THEN lstopped = YES. 
  IF ptexte = "" THEN lstopped = YES. 
  IF AVAILABLE paramtext AND ptexte NE "" THEN 
    RUN decode-string(ptexte, OUTPUT lic-nr). 

  lic-nr = "LICENSE NO: " + lic-nr. 
 
/* check hotel name AND city */ 
  FIND FIRST paramtext WHERE txtnr = 200 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE paramtext THEN lstopped = YES. 
  IF ptexte = "" THEN lstopped = YES. 
  IF AVAILABLE paramtext THEN h-name = ptexte. 
 
  FIND FIRST paramtext WHERE txtnr = 203 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE paramtext THEN lstopped = YES. 
  IF ptexte = "" THEN lstopped = YES. 
  IF AVAILABLE paramtext THEN h-city = ptexte. 
 
  IF htl-name NE h-name OR htl-city NE h-city THEN 
  DO: 
    FIND FIRST paramtext WHERE txtnr = 200 NO-ERROR. 
    IF AVAILABLE paramtext THEN ptexte = htl-name. 
    FIND FIRST paramtext WHERE txtnr = 203 NO-ERROR. 
    IF AVAILABLE paramtext THEN ptexte = htl-city. 
  END. 

/* SY 18/05/2017 White Labeling's PMS Name */
FIND FIRST paramtext WHERE paramtext.txtnr = 11000
    AND paramtext.number = 1 NO-LOCK NO-ERROR.
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
    h-name = h-name + CHR(2) + paramtext.ptexte.

END. 

PROCEDURE decode-serial:
DEF OUTPUT PARAM lstopped AS LOGICAL INIT NO NO-UNDO.

DEF VAR do-it AS LOGICAL INIT YES.

DEF VAR str11 AS CHAR INITIAL "".
DEF VAR str12 AS CHAR INITIAL "".
DEF VAR str13 AS CHAR INITIAL "".
DEF VAR str14 AS CHAR INITIAL "".

DEF VAR str21 AS CHAR INITIAL "".
DEF VAR str22 AS CHAR INITIAL "".
DEF VAR str23 AS CHAR INITIAL "".
DEF VAR str24 AS CHAR INITIAL "".

DEF VAR license-dec  AS CHAR INITIAL "".
DEF VAR datum-dec    AS CHAR INITIAL "".
DEF VAR hotel-dec    AS CHAR INITIAL "".
DEF VAR next-expired AS CHAR.

  FIND FIRST paramtext WHERE paramtext.txtnr = 200 NO-LOCK.
  do-it = (LENGTH(paramtext.passwort) = 19).
  IF do-it THEN
  ASSIGN
      str11 = ENTRY(1, paramtext.passwort, " ")
      str12 = ENTRY(2, paramtext.passwort, " ")
      str13 = ENTRY(3, paramtext.passwort, " ")
      str14 = ENTRY(4, paramtext.passwort, " ").
  IF do-it THEN
  DO:
    FIND FIRST paramtext WHERE paramtext.txtnr = 203 NO-LOCK.
    do-it = (LENGTH(paramtext.passwort) = 19).
    IF do-it THEN
    ASSIGN
      str21 = ENTRY(1, paramtext.passwort, " ")
      str22 = ENTRY(2, paramtext.passwort, " ")
      str23 = ENTRY(3, paramtext.passwort, " ")
      str24 = ENTRY(4, paramtext.passwort, " ").
  END.
  IF do-it THEN RUN decode-serial1(str11, str12, str13, str14, 
    str21, str22, str23, str24, OUTPUT license-dec, OUTPUT datum-dec, 
    OUTPUT hotel-dec).

  FIND FIRST htparam WHERE htparam.paramnr = 976 NO-LOCK.
  ASSIGN next-expired = STRING(MONTH(htparam.fdate), "99") +
                        STRING(DAY(htparam.fdate), "99")   +
                        STRING(YEAR(htparam.fdate)).

  IF (license-dec NE SUBSTR(lic-nr, LENGTH(lic-nr) - 3)) OR
     (datum-dec NE next-expired) THEN
  MESSAGE translateExtended ("Your Program Serial Number is incorrect",lvCAREA,"")
    SKIP
    translateExtended ("Please contact our local Technical Support.",lvCAREA,"")
    VIEW-AS ALERT-BOX WARNING.

END.

PROCEDURE decode-serial1:
DEF INPUT PARAMETER datum-1-enc AS CHAR.    /* encoded license no. and exp date */
DEF INPUT PARAMETER license-enc AS CHAR.
DEF INPUT PARAMETER datum-2-enc AS CHAR.
DEF INPUT PARAMETER schluessel AS CHAR.

DEF INPUT PARAMETER nama1 AS CHAR.          /* encoded hotel name */
DEF INPUT PARAMETER nama2 AS CHAR.
DEF INPUT PARAMETER nama3 AS CHAR.
DEF INPUT PARAMETER nama4 AS CHAR.

DEF OUTPUT PARAMETER license-dec AS CHAR INITIAL "".
DEF OUTPUT PARAMETER datum-dec   AS CHAR INITIAL "".
DEF OUTPUT PARAMETER hotel-dec   AS CHAR INITIAL "".

DEF VAR datum-1-enc-2 AS CHAR.
DEF VAR license-enc-2 AS CHAR.
DEF VAR datum-2-enc-2 AS CHAR.
DEF VAR schluessel-2  AS CHAR.

  RUN decode-all(datum-1-enc, license-enc, datum-2-enc, schluessel, 
      OUTPUT license-dec, OUTPUT datum-dec).
  RUN decode-hotel(nama1, nama2, nama3, nama4, datum-2-enc, schluessel, 
      datum-1-enc, license-enc, OUTPUT hotel-dec).
END.

    /*------------------START: DECCODE HOTEL NAME-------------------------*/
PROCEDURE decode-hotel:
    DEF INPUT PARAMETER name1 AS CHAR.
    DEF INPUT PARAMETER name2 AS CHAR.
    DEF INPUT PARAMETER name3 AS CHAR.
    DEF INPUT PARAMETER name4 AS CHAR.
    DEF INPUT PARAMETER datum2 AS CHAR.
    DEF INPUT PARAMETER schluessel AS CHAR.
    DEF INPUT PARAMETER datum1 AS CHAR.
    DEF INPUT PARAMETER license AS CHAR.
    
    DEF OUTPUT PARAMETER hotel AS CHAR INITIAL "".

    DEF VAR temp1 AS CHAR INITIAL "".
    DEF VAR temp2 AS CHAR INITIAL "".
    DEF VAR temp3 AS CHAR INITIAL "".
    DEF VAR temp4 AS CHAR INITIAL "".

    RUN decode-name(name1, datum2, OUTPUT temp1).
    RUN decode-name(name2, schluessel, OUTPUT temp2).
    RUN decode-name(name3, datum1, OUTPUT temp3).
    RUN decode-name(name4, license, OUTPUT temp4).
  
    hotel = temp1 + temp2 + temp3 + temp4.
    
END.
    /*------------------END: DECCODE HOTEL NAME-------------------------*/

    
    /*------------------START: DECODE NAME-------------------------*/
PROCEDURE decode-name:
    DEF INPUT PARAMETER hotel-enc AS CHAR.
    DEF INPUT PARAMETER in-string AS CHAR.
    DEF OUTPUT PARAMETER out-string AS CHAR INITIAL "".

    
    DEF VAR i AS INT.
    DEF VAR string-int AS INT INITIAL 0.
    DEF VAR hotel-int AS INT INITIAL 0.
    DEF VAR name-dec AS CHAR INITIAL "".
    DEF VAR len AS INT.
    
    len = LENGTH(in-string).

    DO i = 1 TO len:
        RUN char-number(substr(hotel-enc, i, 1), OUTPUT hotel-int).
        RUN char-number(SUBSTR(in-string, i, 1), OUTPUT string-int).
        RUN number-char(hotel-int - (2 * string-int MODULO 10) - 1, OUTPUT name-dec).
        out-string = out-string + name-dec.

    END.
    
END.

    /*------------------END: DECODE NAME-------------------------*/


              /*-----------------START: DECODE SERIAL NUMBER---------------------- */
PROCEDURE decode-all:
    DEF INPUT PARAMETER license-enc AS CHAR.
    DEF INPUT PARAMETER datum-teil1 AS CHAR.
    DEF INPUT PARAMETER datum-teil2 AS CHAR.
    DEF INPUT PARAMETER schluessel AS CHAR.
    
    DEF OUTPUT PARAMETER license3 AS CHAR INITIAL "".
    DEF OUTPUT PARAMETER datum3 AS CHAR INITIAL "".
    
    DEF VAR datum-combined AS CHAR.
    DEF VAR license2 AS CHAR.
    
    DEF VAR zahl2 AS CHAR.
    DEF VAR zahl3 AS CHAR.
 
    DEF VAR license-next AS CHAR.
    DEF VAR datum-teil1-next AS CHAR.
    DEF VAR datum-teil2-next AS CHAR.

    DEF VAR summe AS INTEGER INITIAL 0.
    DEF VAR i AS INTEGER.

    RUN decode-next(datum-teil1, license-enc, OUTPUT datum-teil1-next).
    RUN decode-next(license-enc, datum-teil2, OUTPUT license-next).
    RUN decode-next(datum-teil2, schluessel, OUTPUT datum-teil2-next).

    RUN decode-serial-str (schluessel, "", 0, OUTPUT zahl2).
    RUN decode-serial-str (zahl2, "", 0, OUTPUT zahl3).

      /*  the sum of last digit must be specified  */
/*
    DO  i = 1 TO LENGTH(schluessel).
        summe = summe + (ASC(SUBSTR(schluessel,i,1)) - 64) + i.
    END.

    IF (summe MODULO 13) > 0 THEN
    DO:
        DISPLAY "WRONG SERIAL NUMBER".
    END.
*/

    RUN decode-serial-str (license-next, zahl3, 1, OUTPUT license3).
    RUN combineword (datum-teil1-next, datum-teil2-next, OUTPUT datum-combined).
    RUN decode-serial-str (datum-combined, zahl3, 2, OUTPUT datum3).

END.

              /*-----------------END: DECODE SERIAL NUMBER---------------------- */

              /*-----------------START: DECODE STRING---------------------- */
PROCEDURE decode-serial-str: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE INPUT PARAMETER schluessel AS CHAR.
DEFINE INPUT PARAMETER keychar AS INT.
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 

DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
DEFINE VARIABLE len1 AS INTEGER.
  ASSIGN S = in-str. 

  IF keychar = 0 THEN
  DO:
      ASSIGN j = asc(SUBSTR(s, 1, 1)) - 70 
      len = length(in-str) - 1
      s = SUBSTR(in-str, 2, len). 
  END.
  ELSE
  DO:
      ASSIGN j = asc(SUBSTR(schluessel,keychar,1)) - 49 
      len = length(in-str)
      s = SUBSTR(in-str, 1, len). 
  END.

  DO len = 1 TO length(s): 
      ASSIGN len1 = 13 * len MODULO 5 + 6
      out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j + len1). 
  END. 
END. 
 

              /*-----------------END: DECODE STRING---------------------- */

              /*-----------------START: CUT WORD--------------------------*/  
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

              /*-----------------END: CUT WORD--------------------------*/  

              /*-----------------START: COMBINE WORD--------------------------*/  
PROCEDURE combineword:
    DEFINE INPUT PARAMETER teil1 AS CHAR.
    DEFINE INPUT PARAMETER teil2 AS CHAR.
    DEFINE OUTPUT PARAMETER word AS CHAR.

    ASSIGN word = teil1 + teil2.
END.
              /*-----------------END: COMBINE WORD--------------------------*/  

/*-----------------START: NEXT DECODING---------------------- */
PROCEDURE decode-next:
    DEFINE INPUT PARAMETER in-str AS CHAR.
    DEFINE INPUT PARAMETER schluessel AS CHAR.
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "".

    DEFINE VARIABLE schluessel1 AS INT.
    DEFINE VARIABLE len AS INTEGER.
    DEFINE VARIABLE reverse AS INTEGER.
    DEFINE VARIABLE len1 AS INTEGER.

    DO len = 1 TO length(in-str): 
        reverse = LENGTH(in-str) - len + 1.
        schluessel1 = asc(SUBSTR(schluessel,reverse,1)) MODULO 7 - 1.
        out-str = out-str + chr(asc(SUBSTR(in-str,len,1)) + schluessel1 - len - 5).
    END. 
END.

              /*-----------------END: NEXT DECODING---------------------- */

              /*-----------------START: CHARACTER CHECKING---------------------- */
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
              /*-----------------END: CHARACTER CHECKING---------------------- */

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

    /*------------------START: CONVERT CHAR TO NUMBER-------------------------*/
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
    /*------------------END: CONVERT CHAR TO NUMBER-------------------------*/

    /*------------------START: CONVERT NUMBER TO CHAR-------------------------*/
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
    /*------------------END: CONVERT NUMBER TO CHAR-------------------------*/


PROCEDURE check-room-pos-license:
DEFINE OUTPUT PARAMETER lstopped AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE lic-room AS INTEGER INIT 0 NO-UNDO.
DEFINE VARIABLE lic-pos  AS INTEGER INIT 0 NO-UNDO.
DEFINE VARIABLE max-room AS INTEGER INIT 0 NO-UNDO.
DEFINE VARIABLE max-pos  AS INTEGER INIT 0 NO-UNDO.
  
  RUN htpint.p(975, OUTPUT lic-room).
  RUN htpint.p(989, OUTPUT lic-pos).
/*
  IF lic-room = 0 THEN
  DO:
    lstopped = YES.
    RETURN.
  END.
*/
  FOR EACH zimmer NO-LOCK:
      max-room = max-room + 1.
  END.
  IF max-room GT lic-room THEN
  DO:
    msg-str = msg-str 
      + translateExtended ("Maximum Room License",lvCAREA,"") + " = "
      + STRING(lic-room) + " [" + STRING(max-room) + "!!]"
      + CHR(10)
      + translateExtended ("Please contact our local Technical Support.",lvCAREA,"")
      + CHR(2).
    lstopped = YES.
    RETURN.
  END.

  FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
      max-pos = max-pos + 1.
  END.

  IF max-pos GT lic-pos THEN
  DO:
    msg-str = msg-str
      + translateExtended ("Maximum Outlet License",lvCAREA,"") + " = "
      + STRING(lic-pos) + " [" + STRING(max-pos) + "!!]"
      + CHR(10)
      + translateExtended ("Please contact our local Technical Support.",lvCAREA,"")
      + CHR(2).
    lstopped = YES.
    RETURN.
  END.

END.

