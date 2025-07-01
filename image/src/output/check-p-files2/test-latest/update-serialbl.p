DEF INPUT PARAMETER inp-serial AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER i-case      AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER i-number    AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER d-datum     AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER error-flag  AS LOGICAL  NO-UNDO INIT YES.

DEF VARIABLE license-nr          AS INTEGER  NO-UNDO.
DEF VARIABLE lic-nr              AS CHAR     NO-UNDO INIT "".
DEF VARIABLE htl-name            AS CHAR     NO-UNDO INIT "".
DEF VARIABLE max-ext-date        AS DATE     NO-UNDO INIT ?.
DEF VARIABLE zahl                AS CHAR     NO-UNDO.
DEF VARIABLE valid-flag          AS LOGICAL  NO-UNDO.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR.
IF NOT AVAILABLE paramtext THEN RETURN.
IF paramtext.ptexte = "" THEN RETURN.

RUN e1-serial-decodebl.p (inp-serial, OUTPUT license-nr,
    OUTPUT d-datum, OUTPUT i-case, OUTPUT i-number, 
    OUTPUT valid-flag).

error-flag = NOT valid-flag.
IF error-flag THEN RETURN.

RUN decode-string(ptexte, OUTPUT lic-nr).

IF MONTH(TODAY) = 2 AND DAY(TODAY) GE 28 THEN
    ASSIGN max-ext-date = DATE(2, 28, YEAR(TODAY) + 3).
ELSE ASSIGN 
    max-ext-date = DATE(MONTH(TODAY), DAY(TODAY), YEAR(TODAY) + 3).

IF INTEGER(lic-nr) NE license-nr THEN error-flag = YES.
ELSE IF (i-case EQ 2 OR i-case EQ 3) AND i-number = 0 THEN error-flag = YES.
ELSE IF (i-case EQ 1 OR i-case GT 3) AND i-number NE 0 THEN error-flag = YES.
ELSE IF i-number LT 0 THEN error-flag = YES.
ELSE IF d-datum = ? THEN error-flag = YES.
ELSE IF d-datum GT max-ext-date THEN error-flag = YES.
/* remove below condition if it causes problem */
ELSE IF i-case NE 1 AND d-datum GT (TODAY + 1) THEN error-flag = YES.

IF error-flag THEN RETURN.




CASE i-case:
    WHEN 1  THEN RUN extent-vhp-license-date.
    
    WHEN 2  THEN RUN vhp-rooms-pos(975).   /* max room 975 */
    WHEN 3  THEN RUN vhp-rooms-pos(989).   /* max pos  989 */

    WHEN 4  THEN RUN activate-license("1002").  /* activate sales */
    WHEN 5  THEN RUN activate-license("985").  /* activate bqt */
    WHEN 6  THEN RUN activate-license("1114").  /* activate Club */
    WHEN 7  THEN RUN activate-license("988").  /* activate INV */
    WHEN 8  THEN RUN activate-license("992,1016"). /* activate PO */
    WHEN 9  THEN RUN activate-license("991").  /* activate GC */
    WHEN 10 THEN RUN activate-license("2000"). /* activate GL 2000 */
    WHEN 11 THEN RUN activate-license("319").  /* activate ENG 319 */
    WHEN 12 THEN RUN activate-license("329").  /* activate FA 329 */
    WHEN 13 THEN RUN activate-license("997").  /* activate AR 997 */
    WHEN 14 THEN RUN activate-license("1016"). /* activate AP 1016 */
    WHEN 15 THEN RUN activate-license("1112"). /* activate Handy POS 1112 */
    WHEN 16 THEN RUN activate-license("223").  /* activate Membership 223 */    
    WHEN 17 THEN RUN activate-license("1072"). /* activate RepGen 1072 */    
    WHEN 18 THEN RUN activate-license("1102"). /* activate VHP Mobile 1102 */    
    WHEN 19 THEN RUN activate-license("981").  /* activate Condominium 981 */    
    WHEN 20 THEN RUN activate-license("996"). /* activate FO 996 */
    WHEN 21 THEN RUN activate-license("990,254"). /* activate POS 990, 254 */
    WHEN 22 THEN RUN activate-license("982"). /* activate Combo 982 */
    
    WHEN 23 THEN RUN activate-license("1111"). /* activate kcard 1111 */
    WHEN 24 THEN RUN activate-license("306").  /* activate SMDR 306 */
    WHEN 25 THEN RUN activate-license("307,308,309,310,311,348").  /* PBX PMS */
    WHEN 26 THEN RUN activate-license("358"). /* activate Internet Bill 358 */
    WHEN 27 THEN RUN activate-license("359"). /* activate Video Bill 359 */
    WHEN 28 THEN RUN activate-license("472"). /* activate Scanner 472 */    
    WHEN 29 THEN RUN activate-license("299"). /* activate Scanner 472 */ 
    WHEN 30 THEN RUN activate-license("1074"). /* activate OrderTaker */ 
    WHEN 31 THEN RUN activate-license("1075"). /* activate HKMobile */ 
    WHEN 32 THEN RUN activate-license("1073"). /* activate DashboardMobile */ 
    WHEN 33 THEN RUN activate-license("1055"). /* activate MobileApps */ 
    WHEN 34 THEN RUN activate-license("1357"). /* activate VHP SelfOrder */ 
    WHEN 35 THEN RUN activate-license("1358"). /* activate VHP PreArrival Checkin */ 
    WHEN 36 THEN RUN activate-license("1359"). /* activate VHP BI */ 
    WHEN 37 THEN RUN activate-license("1022"). /* activate cashless payment */ 
    WHEN 38 THEN RUN activate-license("1023"). /* activate salesboard */ 
    WHEN 39 THEN RUN activate-license("282"). /* activate CM License */ 
    WHEN 40 THEN RUN activate-license("280"). /* activate KDS */
/*    
    WHEN 29 THEN RUN activate-license(29). /* activate Golf  */
    WHEN 30 THEN RUN activate-license(30). /* activate  */
*/
    OTHERWISE
    DO:
    END.
END CASE.
/************************* PROCEDURE *********************/

PROCEDURE activate-license:
DEFINE INPUT PARAMETER lic-string AS CHAR   NO-UNDO.
DEFINE VARIABLE htpchar     AS CHAR         NO-UNDO.
DEFINE VARIABLE htpchar1    AS CHAR         NO-UNDO.
DEFINE VARIABLE vhp-lite    AS LOGICAL      NO-UNDO.
DEFINE VARIABLE maxRoom     AS INTEGER      NO-UNDO.
DEFINE VARIABLE curr-i      AS INTEGER      NO-UNDO.
DEFINE VARIABLE ct          AS CHAR         NO-UNDO.
MESSAGE lic-string VIEW-AS ALERT-BOX INFO.
  DO curr-i = 1 TO NUM-ENTRIES(lic-string, ","):
     ct = TRIM(ENTRY(curr-i, lic-string, ",")).


     MESSAGE "ct" ct VIEW-AS ALERT-BOX INFO.
     IF ct NE "" THEN
     DO:
       FIND FIRST htparam WHERE htparam.paramnr = INTEGER(ct) EXCLUSIVE-LOCK.
       ASSIGN
           htparam.flogical = YES
           htpchar = STRING(lic-nr,"x(4)") + STRING(paramnr,"9999") 
                   + STRING(htparam.flogical)
       .
       RUN encode-string(htpchar, OUTPUT htpchar1).
       htparam.fchar = htpchar1.
       FIND CURRENT htparam NO-LOCK.
     END.
  END.
END.

PROCEDURE extent-vhp-license-date:
    IF MONTH(TODAY) = 2 AND DAY(TODAY) GE 28 THEN
        ASSIGN max-ext-date = DATE(2, 28, YEAR(TODAY) + 3).
    ELSE ASSIGN 
        max-ext-date = DATE(MONTH(TODAY), DAY(TODAY), YEAR(TODAY) + 3).
    IF d-datum LT TODAY THEN
    DO:
        error-flag = YES.
        RETURN.
    END.
    RUN extent-lic-date.
    htl-name = "". 
    FIND FIRST paramtext WHERE paramtext.txtnr = 240 NO-LOCK NO-ERROR. 
    IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN         
    DO:    
      RUN decode-string(paramtext.ptexte, OUTPUT htl-name). 
      htl-name = CAPS(htl-name). 
      RUN encode-serial(lic-nr, d-datum, htl-name).
    END.
END.

PROCEDURE vhp-rooms-pos:
DEF INPUT PARAMETER i-param  AS INTEGER NO-UNDO.
DEF VARIABLE htpchar         AS CHAR    NO-UNDO INIT "".
DEF VARIABLE htpchar1        AS CHAR    NO-UNDO INIT "".
  FIND FIRST htparam WHERE paramnr = i-param EXCLUSIVE-LOCK.
  htparam.finteger = i-number.  
  htpchar = STRING(lic-nr,"x(4)") + STRING(paramnr,"9999") 
        + STRING(htparam.finteger).
  RUN encode-string(htpchar, OUTPUT htpchar1).
  htparam.fchar = htpchar1.
  FIND CURRENT htparam NO-LOCK.
END.

PROCEDURE decode-string:
DEFINE INPUT  PARAMETER in-str  AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER out-str AS CHAR NO-UNDO INITIAL "".
DEFINE VARIABLE s   AS CHAR    NO-UNDO.
DEFINE VARIABLE j   AS INTEGER NO-UNDO.
DEFINE VARIABLE len AS INTEGER NO-UNDO.
  ASSIGN  
      s   = in-str
      j   = ASC(SUBSTR(s, 1, 1)) - 70 
      len = LENGTH(in-str) - 1
      s   = SUBSTR(in-str, 2, len)
  .
  DO len = 1 TO LENGTH(s):
    out-str = out-str + CHR(ASC(SUBSTR(s,len,1)) - j).
  END.
END.

PROCEDURE encode-string:
DEFINE INPUT  PARAMETER in-str  AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER out-str AS CHAR NO-UNDO. 

DEFINE VARIABLE s   AS CHAR FORMAT "x(50)" NO-UNDO.
DEFINE VARIABLE j   AS INTEGER NO-UNDO.
DEFINE VARIABLE len AS INTEGER NO-UNDO.
DEFINE VARIABLE ch  AS CHAR    NO-UNDO INITIAL "".

  ASSIGN
      j       = RANDOM(1,9)
      ch      = CHR(ASC(STRING(j)) + 23)
      out-str = ch
      j       = ASC(ch) - 70
  . 
  DO len = 1 TO LENGTH(in-str):
    out-str = out-str + CHR(ASC(SUBSTR(in-str,len,1)) + j).
  END.
END.

PROCEDURE extent-lic-date:
DEFINE VARIABLE htpchar     AS CHAR     NO-UNDO.
DEFINE VARIABLE htpchar1    AS CHAR     NO-UNDO.
DEFINE VARIABLE vhp-lite    AS LOGICAL  NO-UNDO.
DEFINE VARIABLE maxRoom     AS INTEGER  NO-UNDO.

  FIND FIRST htparam WHERE paramnr = 976 NO-LOCK.
  FIND CURRENT htparam EXCLUSIVE-LOCK.
  htparam.fdate = d-datum.
  htpchar = STRING(lic-nr,"x(4)") + STRING(paramnr,"9999") 
        + STRING(MONTH(fdate),"99")
        + STRING(DAY(fdate),"99")
        + STRING(YEAR(fdate),"9999").
  RUN encode-string(htpchar, OUTPUT htpchar1).
  htparam.fchar = htpchar1.
  FIND CURRENT htparam NO-LOCK.
  
  FIND FIRST paramtext WHERE paramtext.txtnr = 976 EXCLUSIVE-LOCK NO-ERROR.
  IF AVAILABLE paramtext THEN
  do:
    paramtext.ptexte = STRING(htparam.fdate,"99/99/9999").
    paramtext.notes = htparam.fchar.
    FIND CURRENT paramtext NO-LOCK.
  END.

  FIND FIRST htparam WHERE htparam.paramnr = 1072 EXCLUSIVE-LOCK.
  ASSIGN htparam.finteger = 0.
  FIND CURRENT htparam NO-LOCK.

  FIND FIRST htparam WHERE htparam.paramnr = 996 NO-LOCK.
  IF htparam.fchar = "" THEN
  DO:
    FIND FIRST htparam WHERE paramnr = 1015 NO-LOCK.  /* VHP Lite */ 
    vhp-lite = htparam.flogical. 
    FIND FIRST htparam WHERE paramnr = 975 NO-LOCK.   /* max room No */
    maxRoom = htparam.finteger.
    IF NOT vhp-lite AND maxRoom NE 1 THEN
    DO:
      FIND FIRST htparam WHERE htparam.paramnr = 996 EXCLUSIVE-LOCK.
      htparam.flogical = YES.
      htpchar = STRING(lic-nr,"x(4)") + STRING(htparam.paramnr,"9999") 
        + STRING(htparam.flogical).
      RUN encode-string(htpchar, OUTPUT htpchar1).
      htparam.fchar = htpchar1.
    END.
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

/*------------------START: ENCCODE HOTEL NAME-------------------------*/
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
/*------------------END: ENCCODE HOTEL NAME-------------------------*/

/*------------------START: ENCCODE NAME-------------------------*/
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
/*------------------END: ENCCODE NAME-------------------------*/

/*-----------------START: GENERATE SERIAL NUMBER---------------------- */
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
/*-----------------END: GENERATE SERIAL NUMBER---------------------- */

/*-----------------START: ENCODE STRING---------------------- */
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
/*-----------------END: ENCODE STRING---------------------- */
             
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

/*-----------------START: NEXT ENCODING---------------------- */
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
/*-----------------END: NEXT ENCODING---------------------- */

         
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

    IF ASC(SUBSTR(in-char,1,1)) > 96 AND ASC(SUBSTR(in-char,1,1)) < 123 THEN
    DO :
        out-int = ASC(SUBSTR(in-char,1,1)) - 60.
    END.
    
    ELSE IF asc(SUBSTR(in-char,1,1)) > 64 AND asc(SUBSTR(in-char,1,1)) < 91 THEN
    DO :
        out-int = asc(SUBSTR(in-char,1,1)) - 64.
    END.

    ELSE IF asc(SUBSTR(in-char,1,1)) > 48 AND asc(SUBSTR(in-char,1,1)) < 58 THEN
    DO:
        out-int = asc(SUBSTR(in-char,1,1)) - 21.
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
        out-char = CHR(in-int + 21).
    END.
    ELSE IF in-int > 36 AND in-int < 63 THEN
    DO:
        out-char = CHR(in-int + 60).
    END.
    ELSE IF in-int = 0 THEN
    DO:
        out-char = " ".
    END.
END.
/*------------------END: CONVERT NUMBER TO CHAR-------------------------*/
