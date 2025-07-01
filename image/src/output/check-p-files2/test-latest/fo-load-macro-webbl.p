DEFINE TEMP-TABLE excel-list
    FIELD curr-xlsrow AS INTEGER
    FIELD curr-xlscol AS INTEGER
    FIELD curr-val AS CHARACTER.

DEFINE TEMP-TABLE error-list 
    FIELD curr-xlsrow AS INTEGER
    FIELD curr-xlscol AS INTEGER
    FIELD curr-val AS CHARACTER
    FIELD msg    AS CHAR.

DEFINE TEMP-TABLE brief-list 
  FIELD b-text AS CHAR. 

DEFINE TEMP-TABLE art-list 
  FIELD str-art AS CHAR
  FIELD anzahl  AS INT INIT 0.

DEFINE TEMP-TABLE t-parameters LIKE parameters.
DEF BUFFER parambuff FOR parameters.

DEFINE INPUT PARAMETER briefnr AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR excel-list.
DEFINE OUTPUT PARAMETER TABLE FOR error-list.
DEFINE OUTPUT PARAMETER error-flag AS LOGICAL INIT NO.

DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE l           AS INTEGER. 
DEFINE VARIABLE continued   AS LOGICAL INITIAL NO. 
DEFINE VARIABLE c           AS CHAR. 
DEFINE VARIABLE ct          AS CHAR.
DEFINE VARIABLE ch          AS CHAR.
DEFINE VARIABLE curr-str    AS CHAR.
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 
DEFINE VARIABLE counter     AS INTEGER.
DEFINE VARIABLE counter-i   AS INTEGER.

DEF VAR ChCol       AS CHAR EXTENT 52 INITIAL
    ["A","B","C","D","E","F","G","H","I","J","K","L","M",
     "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
     "AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM",
     "AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ"].
DEF VAR mbuff      AS CHAR EXTENT 12 INITIAL
    ["jan", "feb", "mar", "apr", "mei",
     "jun", "jul", "aug", "sep", "oct",
     "nov", "des"].

FOR EACH briefzei WHERE briefzei.briefnr = briefnr 
    NO-LOCK BY briefzei.briefzeilnr: 
    j = 1. 
    DO i = 1 TO LENGTH(briefzei.texte): 
       IF ASC(SUBSTR(briefzei.texte, i , 1)) EQ 10 THEN 
       DO: 
         n = i - j. 
         c = SUBSTR(briefzei.texte, j,  n). 
         l = LENGTH(c). 
         IF NOT continued THEN CREATE brief-list. 
         brief-list.b-text = brief-list.b-text + c. 
         j = i + 1. 
       END. 
    END. 
    n = LENGTH(briefzei.texte) - j + 1. 
    c = SUBSTR(briefzei.texte, j,  n). 
    IF NOT continued THEN CREATE brief-list. 
    b-text = b-text + c. 
END.

FOR EACH brief-list NO-LOCK:
  IF b-text = "" OR SUBSTR(b-text,1,1) = "#" THEN.
  ELSE
  DO:
    CREATE art-list.
    DO i = 1 TO NUM-ENTRIES(b-text," "):
      IF SUBSTR(ENTRY(i,b-text," "),1,1) = "^" THEN
        ASSIGN
          art-list.str-art = ENTRY(i,b-text," ")
          art-list.anzahl = 0.
    END.
  END.
END.


FOR EACH excel-list BY excel-list.curr-xlsrow BY excel-list.curr-xlscol:
  IF SUBSTR(excel-list.curr-val,1,1) = "$" 
    OR SUBSTR(excel-list.curr-val,1,1) = "^" THEN
  DO:
    RUN create-colom(excel-list.curr-xlscol, OUTPUT ch).
    CREATE t-parameters.
    ASSIGN
      t-parameters.progname = "FO-Macro"
      t-parameters.SECTION  = STRING(briefnr)
      t-parameters.varname  = ch + STRING(excel-list.curr-xlsrow)
      curr-str = excel-list.curr-val.
    IF curr-str = ? THEN curr-str = "".
    IF SUBSTR(curr-str,1,1) = "$" THEN 
      ASSIGN t-parameters.vstring = curr-str.
    ELSE
    DO:
      FIND FIRST art-list WHERE art-list.str-art = curr-str 
        OR art-list.str-art = ENTRY(1,curr-str,".") EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE art-list THEN
      DO:
        ASSIGN
          t-parameters.vstring = ENTRY(1,curr-str,".")
          art-list.anzahl    = art-list.anzahl + 1.                              
        CASE ENTRY(2,curr-str,"."):
          WHEN "rlyddiff"     THEN t-parameters.vtype = 2047.
          WHEN "lyddiff"      THEN t-parameters.vtype = 2046.
          WHEN "lytdbg"       THEN t-parameters.vtype = 2045.
          WHEN "lytdbl"       THEN t-parameters.vtype = 2044.
          WHEN "ryddiff"      THEN t-parameters.vtype = 2043.
          WHEN "rlydiff"      THEN t-parameters.vtype = 2069.
          WHEN "rlmdiff"      THEN t-parameters.vtype = 2068.
          WHEN "rdiff"        THEN t-parameters.vtype = 2067.
          WHEN "yddiff"       THEN t-parameters.vtype = 2066.
          WHEN "lydiff"       THEN t-parameters.vtype = 2065.
          WHEN "lmdiff"       THEN t-parameters.vtype = 822.
          WHEN "mdiff"        THEN t-parameters.vtype = 821.
          WHEN "diff"         THEN t-parameters.vtype = 820.
          WHEN "lytd-budget"  THEN t-parameters.vtype = 828.
          WHEN "ly-budget"    THEN t-parameters.vtype = 827.
          WHEN "lm-budget"    THEN t-parameters.vtype = 819.
          WHEN "ytd-budget"   THEN t-parameters.vtype = 818.
          WHEN "mtd-budget"   THEN t-parameters.vtype = 817.
          WHEN "budget"       THEN t-parameters.vtype = 816.
          WHEN "l-ytd"        THEN t-parameters.vtype = 815.
          WHEN "l-mtd"        THEN t-parameters.vtype = 196.
          WHEN "lytoday"      THEN t-parameters.vtype = 185.
          WHEN "p-mtd"        THEN t-parameters.vtype = 96.
          WHEN "ytd"          THEN t-parameters.vtype = 95.
          WHEN "mtd"          THEN t-parameters.vtype = 94.
          WHEN "today"        THEN t-parameters.vtype = 93.
          WHEN "yesterday"    THEN t-parameters.vtype = 9199.
          WHEN "lm-today"     THEN t-parameters.vtype = 9198.
          WHEN "ny-budget"    THEN t-parameters.vtype = 9197.
          WHEN "nmtd-budget"  THEN t-parameters.vtype = 9196.
          WHEN "nytd-budget"  THEN t-parameters.vtype = 9195.
          WHEN "today-serv"   THEN t-parameters.vtype = 9194.
          WHEN "today-tax"    THEN t-parameters.vtype = 9193.
          WHEN "mtd-serv"     THEN t-parameters.vtype = 9192.
          WHEN "mtd-tax"      THEN t-parameters.vtype = 9191.
          WHEN "ytd-serv"     THEN t-parameters.vtype = 9190.
          WHEN "ytd-tax"      THEN t-parameters.vtype = 9189.
          WHEN "lmtoday-serv" THEN t-parameters.vtype = 9188.
          WHEN "lmtoday-tax"  THEN t-parameters.vtype = 9187.
          WHEN "pmtd-serv"    THEN t-parameters.vtype = 9186.
          WHEN "pmtd-tax"     THEN t-parameters.vtype = 9185.
          WHEN "lmtd-serv"    THEN t-parameters.vtype = 9184.
          WHEN "lmtd-tax"     THEN t-parameters.vtype = 9183.
          WHEN "lm-mtd"       THEN t-parameters.vtype = 9182.
          WHEN "lm-ytd"       THEN t-parameters.vtype = 9181.
          WHEN "lmtd-tax"     THEN t-parameters.vtype = 9183.
          WHEN "lytd-serv"    THEN t-parameters.vtype = 9200.
          WHEN "lytd-tax"     THEN t-parameters.vtype = 9201.
          WHEN "lytoday-serv" THEN t-parameters.vtype = 9202.
          WHEN "lytoday-tax"  THEN t-parameters.vtype = 9203.
        END CASE.

        DO counter = 1 TO 31:
          IF ENTRY(2,curr-str,".") = STRING(counter)THEN
          DO:
            t-parameters.vtype = 9149 + counter.
            LEAVE.
          END.
          IF ENTRY(2,curr-str,".") = STRING(counter) + "budget" THEN
          DO:
            t-parameters.vtype = 9118 + counter.
            LEAVE.
          END.
          IF ENTRY(2,curr-str,".") = STRING(counter) + "lytoday" THEN
          DO:
            t-parameters.vtype = 8119 + counter.
            LEAVE.
          END.
          /*MG E478DD*/
          IF ENTRY(2,curr-str,".") = STRING(counter) + "serv" THEN
          DO:
            t-parameters.vtype = 9230 + counter.
            LEAVE.
          END.
          IF ENTRY(2,curr-str,".") = STRING(counter) + "tax" THEN
          DO:
            t-parameters.vtype = 9261 + counter.
            LEAVE.
          END.
          /*end MG*/
        END.
              
        DO counter-i = 1 TO 12:
          IF ENTRY(2,curr-str,".") = mbuff[counter-i] THEN 
          DO:
            ASSIGN
              t-parameters.vtype   = 9200 + counter-i
              t-parameters.vstring = ENTRY(1,curr-str,".") + "." + mbuff[counter-i].
            END.
          END.                                 
        END.
      ELSE
      DO:
        CREATE error-list.
        BUFFER-COPY excel-list TO error-list.
        error-list.msg = "Postfix not defined in Macro".
        error-flag = YES.
      END.
    END.
  END.
END.

IF NOT error-flag THEN
DO:
  FIND FIRST parameters WHERE
    parameters.progname            = "FO-Macro"      AND
    parameters.SECTION             = STRING(briefnr) 
    NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE parameters:
    DO TRANSACTION:
      FIND FIRST parambuff WHERE RECID(parambuff) = RECID(parameters).
      DELETE parambuff.
    END.
    FIND NEXT parameters WHERE
      parameters.progname   = "FO-Macro"      AND
      parameters.SECTION    = STRING(briefnr)
    NO-LOCK NO-ERROR.
  END.

  FOR EACH t-parameters:
    CREATE parameters.
    BUFFER-COPY t-parameters TO parameters.
  END. 
END.

PROCEDURE create-colom:   /*FT130513*/
  DEFINE INPUT PARAMETER i AS INT.
  DEFINE OUTPUT PARAMETER ch              AS CHAR.
  
  IF i GT 26 THEN
  DO:
    IF i MOD 26 = 0 THEN ch = chCol[INT(TRUNCATE(i / 26 ,0 )) - 1] + "Z".
    ELSE ch = chCol[INT(TRUNCATE(i / 26 ,0 ))] + chCol[i MOD 26].
  END.
  ELSE ch = chCol[i].
END.
