DEFINE TEMP-TABLE htv-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar AS CHAR. 
DEFINE TEMP-TABLE htp-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar AS CHAR. 
DEFINE TEMP-TABLE brief-list 
  FIELD b-text AS CHAR. 
DEFINE TEMP-TABLE batch-list 
  FIELD briefnr AS INTEGER 
  FIELD fname AS CHAR. 
DEFINE TEMP-TABLE briefzei-list LIKE briefzei.
DEFINE TEMP-TABLE gl-main-list LIKE gl-main.

DEFINE TEMP-TABLE gl-department-list LIKE gl-department.

DEFINE TEMP-TABLE t-gl-acct
    FIELD fibukonto     LIKE gl-acct.fibukonto
    FIELD bezeich       LIKE gl-acct.bezeich
    FIELD acc-type      LIKE gl-acct.acc-type
    FIELD main-nr       LIKE gl-acct.main-nr
    FIELD deptnr        LIKE gl-acct.deptnr
    FIELD actual        LIKE gl-acct.actual
    FIELD budget        LIKE gl-acct.budget
    FIELD last-yr       LIKE gl-acct.last-yr
    FIELD ly-budget     LIKE gl-acct.ly-budget
    FIELD debit         LIKE gl-acct.debit.

DEFINE TEMP-TABLE t-exrate  LIKE exrate.
DEFINE TEMP-TABLE t-exrate1 LIKE exrate.
DEFINE TEMP-TABLE t-gl-accthis
    FIELD fibukonto     LIKE gl-accthis.fibukonto
    FIELD year          LIKE gl-accthis.year
    FIELD actual        LIKE gl-accthis.actual
    FIELD budget        LIKE gl-accthis.budget
    FIELD last-yr       LIKE gl-accthis.last-yr
    FIELD ly-budget     LIKE gl-accthis.ly-budget
    FIELD debit         LIKE gl-accthis.debit.

DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER briefnr     AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER to-date     AS DATE.
DEF INPUT  PARAMETER close-month AS INTEGER.

DEF OUTPUT PARAMETER end-month   AS INTEGER.
DEF OUTPUT PARAMETER prev-month  AS INTEGER.
DEF OUTPUT PARAMETER beg-month   AS INTEGER.

DEF OUTPUT PARAMETER keycmd         AS CHAR.
DEF OUTPUT PARAMETER keyvar         AS CHAR.
DEF OUTPUT PARAMETER keycont        AS CHAR.
DEF OUTPUT PARAMETER c-param64      AS CHAR.
DEF OUTPUT PARAMETER c-param977     AS CHAR.
DEF OUTPUT PARAMETER c-param170     AS CHAR.
DEF OUTPUT PARAMETER c-param144     AS CHAR.
DEF OUTPUT PARAMETER c-foreign-nr   AS INT INIT 0.
DEF OUTPUT PARAMETER d-param795     AS DATE.

DEF OUTPUT PARAMETER xls-dir        AS CHAR.

DEF OUTPUT PARAMETER prog-error     AS LOGICAL.
DEF OUTPUT PARAMETER error-nr       AS INT.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

DEF OUTPUT PARAMETER TABLE FOR htv-list.
DEF OUTPUT PARAMETER TABLE FOR htp-list.
DEF OUTPUT PARAMETER TABLE FOR brief-list.
DEF OUTPUT PARAMETER TABLE FOR batch-list.

DEF OUTPUT PARAMETER TABLE FOR briefzei-list.

DEF OUTPUT PARAMETER TABLE FOR gl-main-list.
DEF OUTPUT PARAMETER TABLE FOR gl-department-list.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.
DEF OUTPUT PARAMETER TABLE FOR t-exrate.
DEF OUTPUT PARAMETER TABLE FOR t-exrate1.
DEF OUTPUT PARAMETER TABLE FOR t-gl-accthis.


DEFINE VARIABLE batch-file      AS LOGICAL INITIAL NO.
DEFINE VARIABLE curr-row        AS INTEGER INITIAL 0.
DEFINE VARIABLE curr-texte      AS CHAR. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-parxls".


FIND FIRST htparam WHERE htparam.paramnr = 418 NO-LOCK. 
IF htparam.fchar EQ "" THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Excel Output Directory not defined (Param 418 Grp 15)",lvCAREA,"").
  RETURN.
END. 
xls-dir = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 993 NO-LOCK. 
end-month = htparam.finteger. 
beg-month = htparam.finteger + 1. 
IF beg-month GT 12 THEN beg-month = 1. 
prev-month = close-month - 1.
IF prev-month = 0 THEN prev-month = 12.

IF close-month = 0 THEN RETURN.

RUN fill-list. 
RUN check-batch.

IF prog-error THEN RETURN.

FIND FIRST htparam WHERE htparam.paramnr = 64 NO-LOCK.
c-param64 = htparam.fchar.
FOR EACH briefzei WHERE briefzei.briefnr = briefnr 
    NO-LOCK BY briefzei.briefzeilnr:
    CREATE briefzei-list.
    BUFFER-COPY briefzei TO briefzei-list.
END.

FOR EACH gl-main:
    CREATE gl-main-list.
    BUFFER-COPY gl-main TO gl-main-list.
    /*FIND FIRST gl-acct WHERE gl-acct.main-nr = gl-main.nr NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
        CREATE gl-acct-list-main.
        BUFFER-COPY gl-acct TO gl-acct-list-main.
    END.*/
END.

FOR EACH gl-department:
    CREATE gl-department-list.
    BUFFER-COPY gl-department TO gl-department-list.
    /*FIND FIRST gl-acct WHERE gl-acct.deptnr = gl-department.nr NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
        CREATE gl-acct-list-dept.
        BUFFER-COPY gl-acct TO gl-acct-list-dept.
    END.*/
END.

FOR EACH gl-acct:
    DEF VAR i AS INT.
    CREATE t-gl-acct.
    ASSIGN
      t-gl-acct.fibukonto     = gl-acct.fibukonto
      t-gl-acct.bezeich       = gl-acct.bezeich
      t-gl-acct.acc-type      = gl-acct.acc-type
      t-gl-acct.main-nr       = gl-acct.main-nr
      t-gl-acct.deptnr        = gl-acct.deptnr.

    DO i = 1 TO 12: 
      ASSIGN
        t-gl-acct.actual[i]    = gl-acct.actual[i]
        t-gl-acct.budget[i]    = gl-acct.budget[i]
        t-gl-acct.last-yr[i]   = gl-acct.last-yr[i]
        t-gl-acct.ly-budget[i] = gl-acct.ly-budget[i]
        t-gl-acct.debit[i]     = gl-acct.debit[i].
    END. 
END.

FOR EACH exrate WHERE exrate.artnr = 99999 OR exrate.artnr = 99998:
    CREATE t-exrate.
    BUFFER-COPY exrate TO t-exrate.
END.

FIND FIRST htparam WHERE htparam.paramnr = 795 NO-LOCK.
d-param795 = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 977 NO-LOCK. 
c-param977 = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 170 NO-LOCK. 
c-param170 = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
c-param144 = htparam.fchar.
IF c-param144 NE "" THEN
DO:
    FIND FIRST waehrung WHERE waehrung.wabkurz = c-param144 NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN c-foreign-nr = waehrung.waehrungsnr. 
END.
IF c-foreign-nr NE 0 THEN 
DO:
    FOR EACH exrate WHERE exrate.artnr = c-foreign-nr :
        CREATE t-exrate1.
        BUFFER-COPY exrate TO t-exrate1.
    END.
END.

FOR EACH gl-accthis WHERE gl-accthis.YEAR = YEAR(to-date) :
    CREATE t-gl-accthis.
    ASSIGN
    t-gl-accthis.fibukonto     = gl-accthis.fibukonto
    t-gl-accthis.year          = gl-accthis.year.
    DO i = 1 TO 12: 
      ASSIGN
        t-gl-accthis.actual[i]    = gl-accthis.actual[i]
        t-gl-accthis.budget[i]    = gl-accthis.budget[i]
        t-gl-accthis.last-yr[i]   = gl-accthis.last-yr[i]
        t-gl-accthis.ly-budget[i] = gl-accthis.ly-budget[i]
        t-gl-accthis.debit[i]     = gl-accthis.debit[i].
    END.
END.

PROCEDURE fill-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE l AS INTEGER. 
DEFINE VARIABLE continued AS LOGICAL INITIAL NO. 
 
  FIND FIRST htparam WHERE paramnr = 600 NO-LOCK. 
  keycmd = htparam.fchar. 
  FIND FIRST htparam WHERE paramnr = 2030 NO-LOCK. 
  keyvar = htparam.fchar. 
  FIND FIRST htparam WHERE paramnr = 1122 NO-LOCK. 
  keycont = keycmd + htparam.fchar. 
 
  FOR EACH htparam WHERE paramgruppe = 39 
    AND htparam.paramnr NE 2030 NO-LOCK BY length(htparam.fchar) descending: 
     IF SUBSTR(htparam.fchar,1 ,1) = "." THEN 
     DO: 
       create htv-list. 
       htv-list.paramnr = htparam.paramnr. 
       htv-list.fchar = htparam.fchar. 
     END. 
     ELSE 
     DO: 
       create htp-list. 
       htp-list.paramnr = htparam.paramnr. 
       htp-list.fchar = keycmd + htparam.fchar. 
     END. 
  END. 
 
/***** additional internal declaration FOR ratio *****/ 
  
  create htv-list. 
  htv-list.paramnr = 2055.   /* this month balance */ 
  htv-list.fchar = ".a". 
  create htv-list. 
  htv-list.paramnr = 2059.   /* this month budget */ 
  htv-list.fchar = ".2". 
  create htv-list. 
  htv-list.paramnr = 2067.   /* ratio this month balance:budget */ 
  htv-list.fchar = ".3". 
  create htv-list. 
  htv-list.paramnr = 2057.   /* LAST year this month */ 
  htv-list.fchar = ".4". 
  create htv-list. 
  htv-list.paramnr = 2058.   /* ytd balance */ 
  htv-list.fchar = ".5". 
  create htv-list. 
  htv-list.paramnr = 2062.   /* ytd budget */ 
  htv-list.fchar = ".6". 
  create htv-list. 
  htv-list.paramnr = 2043.   /* ratio ytd balance:budget */ 
  htv-list.fchar = ".7". 
  create htv-list. 
  htv-list.paramnr = 2044.   /* LAST year ytd */ 
  htv-list.fchar = ".8". 
  create htv-list. 
  htv-list.paramnr = 2056.   /* this year LAST month */ 
  htv-list.fchar = ".9". 
  create htv-list. 
  htv-list.paramnr = 2069.   /* ratio LAST year this month */ 
  htv-list.fchar = ".10". 
 
  create htv-list. 
  htv-list.paramnr = 3001.   /* Budget Jan - This Year */ 
  htv-list.fchar = ".BJAN". 
  create htv-list. 
  htv-list.paramnr = 3002.   /* Budget Feb - This Year */ 
  htv-list.fchar = ".BFEB". 
  create htv-list. 
  htv-list.paramnr = 3003.   /* Budget Mar - This Year */ 
  htv-list.fchar = ".BMAR". 
  create htv-list. 
  htv-list.paramnr = 3004.   /* Budget Apr - This Year */ 
  htv-list.fchar = ".BAPR". 
  create htv-list. 
  htv-list.paramnr = 3005.   /* Budget May - This Year */ 
  htv-list.fchar = ".BMAY". 
  create htv-list. 
  htv-list.paramnr = 3006.   /* Budget Jun - This Year */ 
  htv-list.fchar = ".BJUN". 
  create htv-list. 
  htv-list.paramnr = 3007.   /* Budget Jul - This Year */ 
  htv-list.fchar = ".BJUL". 
  create htv-list. 
  htv-list.paramnr = 3008.   /* Budget Aug - This Year */ 
  htv-list.fchar = ".BAUG". 
  create htv-list. 
  htv-list.paramnr = 3009.   /* Budget Sep - This Year */ 
  htv-list.fchar = ".BSEP". 
  create htv-list. 
  htv-list.paramnr = 3010.   /* Budget Oct - This Year */ 
  htv-list.fchar = ".BOCT". 
  create htv-list. 
  htv-list.paramnr = 3011.   /* Budget Nov - This Year */ 
  htv-list.fchar = ".BNOV". 
  create htv-list. 
  htv-list.paramnr = 3012.   /* Budget Dec - This Year */ 
  htv-list.fchar = ".BDEC". 
 
  create htv-list. 
  htv-list.paramnr = 3021.   /* Budget Jan - NEXT Year */ 
  htv-list.fchar = ".NBJAN". 
  create htv-list. 
  htv-list.paramnr = 3022.   /* Budget Feb - NEXT Year */ 
  htv-list.fchar = ".NBFEB". 
  create htv-list. 
  htv-list.paramnr = 3023.   /* Budget Mar - NEXT Year */ 
  htv-list.fchar = ".NBMAR". 
  create htv-list. 
  htv-list.paramnr = 3024.   /* Budget Apr - NEXT Year */ 
  htv-list.fchar = ".NBAPR". 
  create htv-list. 
  htv-list.paramnr = 3025.   /* Budget May - NEXT Year */ 
  htv-list.fchar = ".NBMAY". 
  create htv-list. 
  htv-list.paramnr = 3026.   /* Budget Jun - NEXT Year */ 
  htv-list.fchar = ".NBJUN". 
  create htv-list. 
  htv-list.paramnr = 3027.   /* Budget Jul - NEXT Year */ 
  htv-list.fchar = ".NBJUL". 
  create htv-list. 
  htv-list.paramnr = 3028.   /* Budget Aug - NEXT Year */ 
  htv-list.fchar = ".NBAUG". 
  create htv-list. 
  htv-list.paramnr = 3029.   /* Budget Sep - NEXT Year */ 
  htv-list.fchar = ".NBSEP". 
  create htv-list. 
  htv-list.paramnr = 3030.   /* Budget Oct - NEXT Year */ 
  htv-list.fchar = ".NBOCT". 
  create htv-list. 
  htv-list.paramnr = 3031.   /* Budget Nov - NEXT Year */ 
  htv-list.fchar = ".NBNOV". 
  create htv-list. 
  htv-list.paramnr = 3032.   /* Budget Dec - NEXT Year */ 
  htv-list.fchar = ".NBDEC". 
 
  CREATE htv-list. 
  htv-list.paramnr = 3041.   /* Actual Jan - THIS Year */ 
  htv-list.fchar = ".JAN". 
  CREATE htv-list. 
  htv-list.paramnr = 3042.   /* Actual Feb - THIS Year */ 
  htv-list.fchar = ".FEB". 
  CREATE htv-list. 
  htv-list.paramnr = 3043.   /* Actual Mar - THIS Year */ 
  htv-list.fchar = ".MAR". 
  CREATE htv-list. 
  htv-list.paramnr = 3044.   /* Actual Apr - THIS Year */ 
  htv-list.fchar = ".APR". 
  CREATE htv-list. 
  htv-list.paramnr = 3045.   /* Actual May - THIS Year */ 
  htv-list.fchar = ".MAY". 
  CREATE htv-list. 
  htv-list.paramnr = 3046.   /* Actual Jun - THIS Year */ 
  htv-list.fchar = ".JUN". 
  CREATE htv-list. 
  htv-list.paramnr = 3047.   /* Actual Jul - THIS Year */ 
  htv-list.fchar = ".JUL". 
  CREATE htv-list. 
  htv-list.paramnr = 3048.   /* Actual Aug - THIS Year */ 
  htv-list.fchar = ".AUG". 
  CREATE htv-list. 
  htv-list.paramnr = 3049.   /* Actual Sep - THIS Year */ 
  htv-list.fchar = ".SEP". 
  CREATE htv-list. 
  htv-list.paramnr = 3050.   /* Actual Oct - THIS Year */ 
  htv-list.fchar = ".OCT". 
  CREATE htv-list. 
  htv-list.paramnr = 3051.   /* Actual Nov - THIS Year */ 
  htv-list.fchar = ".NOV". 
  CREATE htv-list. 
  htv-list.paramnr = 3052.   /* Actual Dec - THIS Year */ 
  htv-list.fchar = ".DEC". 

  CREATE htv-list. 
  htv-list.paramnr = 3061.   /* Actual Jan - LAST yea */ 
  htv-list.fchar = ".LJAN". 
  CREATE htv-list. 
  htv-list.paramnr = 3062.   /* Actual Feb - LAST yea */ 
  htv-list.fchar = ".LFEB". 
  CREATE htv-list. 
  htv-list.paramnr = 3063.   /* Actual Mar - LAST yea */ 
  htv-list.fchar = ".LMAR". 
  CREATE htv-list. 
  htv-list.paramnr = 3064.   /* Actual Apr - LAST yea */ 
  htv-list.fchar = ".LAPR". 
  CREATE htv-list. 
  htv-list.paramnr = 3065.   /* Actual May - LAST yea */ 
  htv-list.fchar = ".LMAY". 
  CREATE htv-list. 
  htv-list.paramnr = 3066.   /* Actual Jun - LAST yea */ 
  htv-list.fchar = ".LJUN". 
  CREATE htv-list. 
  htv-list.paramnr = 3067.   /* Actual Jul - LAST yea */ 
  htv-list.fchar = ".LJUL". 
  CREATE htv-list. 
  htv-list.paramnr = 3068.   /* Actual Aug - LAST yea */ 
  htv-list.fchar = ".LAUG". 
  CREATE htv-list. 
  htv-list.paramnr = 3069.   /* Actual Sep - LAST yea */ 
  htv-list.fchar = ".LSEP". 
  CREATE htv-list. 
  htv-list.paramnr = 3070.   /* Actual Oct - LAST yea */ 
  htv-list.fchar = ".LOCT". 
  CREATE htv-list. 
  htv-list.paramnr = 3071.   /* Actual Nov - LAST yea */ 
  htv-list.fchar = ".LNOV". 
  CREATE htv-list. 
  htv-list.paramnr = 3072.   /* Actual Dec - LAST yea */ 
  htv-list.fchar = ".LDEC". 

  DO: 
    FOR EACH briefzei WHERE briefzei.briefnr = briefnr 
      NO-LOCK BY briefzei.briefzeilnr: 
      j = 1. 
      DO i = 1 TO length(briefzei.texte): 
         IF ASC(SUBSTR(briefzei.texte, i , 1)) EQ 10 THEN 
         DO: 
           n = i - j. 
           c = SUBSTR(briefzei.texte, j,  n). 
           l = length(c). 
           IF NOT continued THEN CREATE brief-list. 
           brief-list.b-text = brief-list.b-text + c. 
           j = i + 1. 
           IF l GT length(keycont) AND 
             SUBSTR(c, l - length(keycont) + 1, length(keycont)) = keycont THEN 
           DO: 
             continued = YES. 
             b-text = SUBSTR(b-text, 1, length(b-text) - length(keycont)). 
           END. 
           ELSE continued = NO. 
         END. 
      END. 
      n = length(briefzei.texte) - j + 1. 
      c = SUBSTR(briefzei.texte, j,  n). 
      IF NOT continued THEN create brief-list. 
      b-text = b-text + c. 
    END. 
  END. 
END. 



PROCEDURE check-batch: 
DEFINE VARIABLE texte   AS CHAR. 
DEFINE VARIABLE correct AS LOGICAL. 
DEFINE VARIABLE bnr     AS INTEGER. 
DEFINE VARIABLE row-nr  AS INTEGER INITIAL 0. 
DEF VARIABLE return-flag AS LOGICAL INIT NO NO-UNDO.
 
  FIND FIRST htp-list WHERE htp-list.paramnr = 2038 NO-LOCK. 
  FOR EACH brief-list: 
    row-nr = row-nr + 1. 
    texte = TRIM(brief-list.b-text). 
    IF batch-file THEN 
    DO: 
      RUN check-integer(texte, OUTPUT correct). 
      IF correct THEN 
      DO: 
        bnr = INTEGER(texte). 
        FIND FIRST brief WHERE brief.briefnr = bnr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE brief THEN 
        DO: 
            msg-str = msg-str + CHR(2)
                    + translateExtended ("No such report file number",lvCAREA,"") + " " + STRING(bnr)
                    + CHR(10)
                    + translateExtended ("at line number",lvCAREA,"") + " " + STRING(row-nr)
                    + CHR(10)
                    + SUBSTR(texte, 1, length(texte)).
            prog-error = YES. 
            error-nr = - 1. 
            return-flag = YES.
            LEAVE.
        END. 
        CREATE batch-list. 
        batch-list.briefnr = bnr. 
        batch-list.fname = brief.fname. 
      END. 
      ELSE
      DO:
        return-flag = YES.
        LEAVE.
      END.
    END. 
    IF texte = htp-list.fchar THEN batch-file = YES. 
  END.

  IF return-flag THEN RETURN.

  IF NOT batch-file THEN 
  DO: 
    create batch-list. 
    FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK. 
    batch-list.briefnr = briefnr. 
    batch-list.fname = brief.fname. 
  END. 
END. 



PROCEDURE check-integer: 
DEFINE INPUT PARAMETER texte AS CHAR. 
DEFINE OUTPUT PARAMETER correct AS LOGICAL INITIAL YES. 
DEFINE VARIABLE i AS INTEGER. 
  IF length (texte) = 0 THEN correct = NO. 
  DO i = 1 TO length(texte): 
     IF ASC(SUBSTR(texte, i, 1)) GT 57 OR ASC(SUBSTR(texte, i, 1)) LT 48 
     THEN correct = NO. 
  END. 
  IF NOT correct THEN 
  DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Program expected a number:",lvCAREA,"") + " " + texte 
              + CHR(10)
              + translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
              + CHR(10)
              + SUBSTR(curr-texte, 1, length(curr-texte)).
       prog-error = YES. 
       error-nr = - 1. 
       RETURN. 
  END. 
END. 

