
/************************************************************************ 
Program FOR interpreting User's FO-Reports, OUTPUT exported TO EXCEL 
This will be called FOR example BY XXXXXXXX 

RESTRICTIONS: 
1. BEGIN AND END commands have TO be defined IN a seperate line 
2. LM+ 10,  TAB 10 AND skip10 are allowed !! 
 
*********************************************************/ 
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER.
DEFINE INPUT PARAMETER briefnr          AS INTEGER. 
DEFINE INPUT PARAMETER from-date        AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER link             AS CHARACTER.
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER INITIAL "".
DEFINE OUTPUT PARAMETER mess-result     AS CHARACTER INITIAL "Failed to generate data".
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL INITIAL NO.

/**************************** WIDGET ************************************/
{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "fo-parxls-gs".

DEFINE VARIABLE ch              AS CHAR FORMAT "x(80)". 
DEFINE VARIABLE xls-dir         AS CHAR     NO-UNDO.

DEFINE VARIABLE budget-flag     AS LOGICAL INITIAL NO. 
DEFINE VARIABLE ytd-flag        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE lytd-flag       AS LOGICAL INITIAL NO. 
DEFINE VARIABLE lmtd-flag       AS LOGICAL INITIAL NO. 
DEFINE VARIABLE pmtd-flag       AS LOGICAL INITIAL NO.
DEFINE VARIABLE budget-all      AS LOGICAL INITIAL NO.  /*geral ambil nilai awal - akhir tahun to-date E9DE63*/
DEFINE VARIABLE serv-vat        AS LOGICAL. 

DEFINE VARIABLE zeit            AS INTEGER. 
DEFINE VARIABLE no-decimal      AS LOGICAL INITIAL NO. 

DEFINE VARIABLE prog-error      AS LOGICAL INITIAL NO. 
DEFINE VARIABLE error-nr        AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-row        AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-column     AS INTEGER. 
DEFINE VARIABLE curr-cmd        AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-texte      AS CHAR.
DEFINE VARIABLE curr-pos        AS INTEGER. 
DEFINE VARIABLE actual-cmd      AS INTEGER INITIAL 0. 
 
DEFINE VARIABLE grp-nr          AS INTEGER. 
DEFINE VARIABLE curr-nr         AS INTEGER INITIAL 0. 
DEFINE VARIABLE varname         AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE bezeich         AS CHAR. 
DEFINE VARIABLE grpflag         AS INTEGER. 
  /* 0 = single account, 1 = main account, 2 = group account, 3 = dept  */  
 
DEFINE VARIABLE Lfrom-date      AS DATE. 
DEFINE VARIABLE Lto-date        AS DATE. 
DEFINE VARIABLE jan1            AS DATE. 
DEFINE VARIABLE Ljan1           AS DATE. 
DEFINE VARIABLE Pfrom-date      AS DATE. 
DEFINE VARIABLE Pto-date        AS DATE.
DEFINE VARIABLE curr-month      AS INTEGER INITIAL 1. 
  
DEFINE VARIABLE n               AS INTEGER. 
DEFINE VARIABLE keycmd          AS CHAR. 
DEFINE VARIABLE keyvar          AS CHAR. 
 
DEFINE VARIABLE foreign-flag    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE foreign-nr      AS INTEGER INITIAL 0 NO-UNDO. 
 
DEFINE VARIABLE start-date      AS DATE INITIAL ?. 
DEFINE VARIABLE lytoday         AS DATE. 
DEFINE VARIABLE lytoday-flag    AS LOGICAL INITIAL YES.  

DEFINE VARIABLE price-decimal   AS INTEGER.
DEFINE VARIABLE msg-ans         AS LOGICAL.
DEFINE VARIABLE outfile-dir     AS CHAR.
DEFINE VARIABLE anz0            AS INTEGER.

/************************ TEMP-TABLE ********************************************/ 
DEFINE TEMP-TABLE detail-list 
  FIELD nr          AS INTEGER INITIAL 0 
  FIELD str-buffer  AS CHAR 
  FIELD field-value AS DECIMAL EXTENT 12 
  FIELD use-flag    AS LOGICAL EXTENT 12 INITIAL 
    [no,NO,NO,NO,NO,NO,NO,NO,NO,NO,NO,no]. 
 
DEFINE TEMP-TABLE brief-list 
  FIELD b-text AS CHAR. 
 
DEFINE TEMP-TABLE batch-list 
  FIELD briefnr AS INTEGER 
  FIELD fname   AS CHAR. 
 
DEFINE TEMP-TABLE htp-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar   AS CHAR
  INDEX idx1 paramnr
  INDEX idx2 fchar.
 
DEFINE TEMP-TABLE htv-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar   AS CHAR
  INDEX idx1 fchar.
 
DEFINE TEMP-TABLE t-brief LIKE brief.

DEFINE TEMP-TABLE w1 
  FIELD nr          AS INTEGER 
  FIELD varname     AS CHAR 
  FIELD main-code   AS INTEGER   /* eg. 805 FOR AVAILABLE room */ 
  FIELD s-artnr     AS CHAR
  FIELD artnr       AS INTEGER 
  FIELD dept        AS INTEGER 
  FIELD grpflag     AS INTEGER INITIAL 0 
  FIELD done        AS LOGICAL INITIAL NO 
  FIELD bezeich     AS CHAR 
  FIELD int-flag    AS LOGICAL INITIAL NO 
 
  FIELD tday        AS DECIMAL INITIAL 0 
  FIELD tday-serv   AS DECIMAL INITIAL 0 
  FIELD tday-tax    AS DECIMAL INITIAL 0 
  FIELD mtd-serv    AS DECIMAL INITIAL 0 
  FIELD mtd-tax     AS DECIMAL INITIAL 0 
  FIELD ytd-serv    AS DECIMAL INITIAL 0 
  FIELD ytd-tax     AS DECIMAL INITIAL 0 
  FIELD yesterday   AS DECIMAL INITIAL 0 
  FIELD saldo       AS DECIMAL INITIAL 0 
  FIELD lastmon     AS DECIMAL INITIAL 0
  FIELD pmtd-serv   AS DECIMAL INITIAL 0 
  FIELD pmtd-tax    AS DECIMAL INITIAL 0 
  FIELD lmtd-serv   AS DECIMAL INITIAL 0 
  FIELD lmtd-tax    AS DECIMAL INITIAL 0 
  FIELD lastyr      AS DECIMAL INITIAL 0 
  FIELD lytoday     AS DECIMAL INITIAL 0 
  FIELD ytd-saldo   AS DECIMAL INITIAL 0 
  FIELD lytd-saldo  AS DECIMAL INITIAL 0 
 
  FIELD year-saldo  AS DECIMAL EXTENT 12 INITIAL 
    [0,0,0,0,0,0,0,0,0,0,0,0] 

  FIELD mon-saldo   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0]

  FIELD mon-budget   AS DECIMAL EXTENT 31 INITIAL 
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0]

  FIELD mon-lmtd     AS DECIMAL EXTENT 31 INITIAL 
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0]

  FIELD tbudget     AS DECIMAL INITIAL 0 
  FIELD budget      AS DECIMAL INITIAL 0 
  FIELD lm-budget   AS DECIMAL INITIAL 0 
  FIELD lm-today    AS DECIMAL INITIAL 0 
  FIELD lm-today-serv  AS DECIMAL INITIAL 0 
  FIELD lm-today-tax   AS DECIMAL INITIAL 0 
  FIELD lm-mtd      AS DECIMAL INITIAL 0 
  FIELD lm-ytd      AS DECIMAL INITIAL 0 
  FIELD ly-budget   AS DECIMAL INITIAL 0 
  FIELD ny-budget   AS DECIMAL INITIAL 0   /*FT*/
  FIELD ytd-budget  AS DECIMAL INITIAL 0 
  FIELD nytd-budget AS DECIMAL INITIAL 0  /*FT*/
  FIELD nmtd-budget AS DECIMAL INITIAL 0  /*FT*/
  FIELD lytd-budget AS DECIMAL INITIAL 0
  FIELD lytd-serv     AS DECIMAL INITIAL 0 
  FIELD lytd-tax      AS DECIMAL INITIAL 0 
  FIELD lytoday-serv  AS DECIMAL INITIAL 0 
  FIELD lytoday-tax   AS DECIMAL INITIAL 0 
  FIELD month-budget  AS DECIMAL INITIAL 0 /*gerald awal - akhir bulan*/
  FIELD year-budget   AS DECIMAL INITIAL 0 /*gerald awal - akhir tahun*/
  FIELD tischnr       AS INTEGER INITIAL 0 /*gerald tableno for pax-table 72AF1A*/
  FIELD mon-serv     AS DECIMAL EXTENT 31 INITIAL                       /*MG E478DD*/
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0]
  FIELD mon-tax     AS DECIMAL EXTENT 31 INITIAL                        /*MG E478DD*/
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0]
  INDEX idx1 varname
  INDEX idx2 nr
  INDEX idx3 main-code
  INDEX idx4 main-code done
  INDEX idx5 main-code artnr
  INDEX idx6 main-code dept 
.
 
DEFINE TEMP-TABLE w2 
  FIELD val-sign    AS INTEGER INITIAL 1 
  FIELD nr1         AS INTEGER 
  FIELD nr2         AS INTEGER.
 
DEF TEMP-TABLE t-parameters LIKE parameters.
/*************** MAIN LOGIC ***************/ 

RUN prepare-fo-parxlsbl.p 
    (pvILanguage, briefnr, OUTPUT xls-dir, OUTPUT msg-str,
     OUTPUT serv-vat, OUTPUT foreign-nr, OUTPUT start-date,
     OUTPUT price-decimal, OUTPUT no-decimal, OUTPUT keycmd,
     OUTPUT keyvar, OUTPUT outfile-dir, OUTPUT anz0,
     OUTPUT TABLE htv-list, OUTPUT TABLE htp-list,
     OUTPUT TABLE brief-list, OUTPUT TABLE t-brief, OUTPUT TABLE t-parameters).  

zeit = TIME. 

CREATE detail-list. 
detail-list.nr = 0. 

DO: 
DEFINE VARIABLE datum AS DATE. 

  IF MONTH(to-date) EQ 2 AND DAY(to-date) EQ 29 THEN 
    ASSIGN lytoday = DATE(2, 28, YEAR(to-date) - 1).
  ELSE
  ASSIGN lytoday = DATE(MONTH(to-date), DAY(to-date), YEAR(to-date) - 1).

  jan1  = DATE(1, 1, year(to-date)). 
  Ljan1 = DATE(1, 1, year(to-date) - 1). 
 
  IF (start-date NE ?) AND (start-date GT from-date) THEN 
  DO: 
    from-date = start-date. 
    jan1      = start-date. 
    Ljan1     = DATE(month(jan1), day(jan1), year(jan1) - 1). 
  END. 
 
  DO: 
    Pto-date = from-date - 1. 
    IF (MONTH(to-date) = MONTH(to-date + 1)) THEN
    DO:
      IF MONTH(Pto-date) = 2 THEN
      DO:
        IF DAY(to-date) LT DAY(Pto-date) THEN
        Pto-date = DATE(MONTH(Pto-date), DAY(to-date), YEAR(Pto-date)). 
      END.
      ELSE Pto-date = DATE(MONTH(Pto-date), DAY(to-date), YEAR(Pto-date)). 
    END.
    Pfrom-date = DATE(MONTH(Pto-date), 1, YEAR(Pto-date)). 
  END. 
 
  IF (month(to-date) NE 2) OR (day(to-date) NE 29) THEN 
    Lto-date = DATE(month(to-date), day(to-date), year(to-date) - 1). 
  ELSE Lto-date = DATE(month(to-date), 28, year(to-date) - 1). 
 
  Lfrom-date = DATE(month(to-date), 1, year(Lto-date)).  
END.
 
FIND FIRST t-brief.

CREATE batch-list. 
ASSIGN
  batch-list.briefnr = briefnr
  batch-list.fname = t-brief.fname
.

FOR EACH brief-list: 
  curr-texte = TRIM(b-text). 
  curr-pos = 1. 
  curr-column = 1. 
  curr-row = curr-row + 1. 
 
  FOR EACH detail-list WHERE detail-list.nr GT 0: 
    DELETE detail-list. 
  END. 
 
  FIND FIRST detail-list WHERE detail-list.nr = 0. 
  detail-list.str-buffer = "". 
  DO n = 1 TO 12: 
    detail-list.field-value[n] = 0. 
    detail-list.use-flag[n] = NO. 
  END. 
  
  IF SUBSTR(curr-texte, 1, 1) NE "#" THEN 
  DO: 
    IF actual-cmd = 0 AND curr-texte NE "" THEN 
    DO: 
      RUN analyse-textheader (INPUT curr-texte). 
      IF prog-error THEN RETURN. 

      IF curr-cmd = 184 THEN foreign-flag = YES. 
      ELSE IF curr-cmd = 801 THEN budget-flag = YES. 
      ELSE IF curr-cmd = 802 THEN ytd-flag = YES.       
      ELSE IF curr-cmd = 803 THEN lytd-flag = YES.       
      ELSE IF curr-cmd = 841 THEN lmtd-flag = YES. 
      ELSE IF curr-cmd = 804 THEN pmtd-flag = YES. 
      ELSE IF curr-cmd = 829 THEN budget-all = YES.  /*geral ambil nilai awal - akhir tahun to-date E9DE63*/
 
      ELSE IF curr-cmd = 182 THEN /* guest ledger */ 
      DO:
        RUN create-var0(curr-texte, NO).
        IF prog-error THEN RETURN.
      END.        
      ELSE IF curr-cmd = 183 THEN /* compliment rooms OF paying segments */ 
      DO:
        RUN create-var0(curr-texte, NO).
        IF prog-error THEN RETURN.
      END.     
      ELSE IF curr-cmd = 807 OR curr-cmd = 808 
        OR curr-cmd EQ 811 OR curr-cmd = 812 THEN 
      DO:
        RUN create-var0(curr-texte, NO).
        IF prog-error THEN RETURN.
      END.
         
      ELSE IF curr-cmd EQ 129 /* vacant rooms */
        OR curr-cmd EQ 805 OR curr-cmd EQ 806 
        OR curr-cmd EQ 810 OR curr-cmd = 122 OR curr-cmd = 752 
        OR curr-cmd = 288
        OR curr-cmd = 1019 /* Day Use Rooms */ THEN 
      DO:
        RUN create-var0(curr-texte, YES). 
        IF prog-error THEN RETURN.
      END.     
      ELSE IF curr-cmd GE 753 AND curr-cmd LE 755 THEN 
      DO:
        RUN create-var0(curr-texte, YES). 
        IF prog-error THEN RETURN.
      END.        
       
      ELSE IF curr-cmd = 85  OR curr-cmd = 86 
        OR curr-cmd = 106 OR curr-cmd = 107 
        OR curr-cmd = 187 OR curr-cmd = 188 
        OR curr-cmd = 189 OR curr-cmd = 190 
        OR curr-cmd = 191 
        OR curr-cmd = 193 OR curr-cmd = 194 
        OR curr-cmd = 195 
        OR curr-cmd = 211 OR curr-cmd = 231 
        OR curr-cmd = 742 
        OR curr-cmd = 750 OR curr-cmd = 751 
        OR curr-cmd = 969 OR curr-cmd = 9106 /*MT*/
        OR curr-cmd = 7194 
        OR curr-cmd = 7195
        OR curr-cmd = 9188 OR curr-cmd = 9190 
        OR curr-cmd = 9000 THEN 
      DO:
        RUN create-var0(curr-texte, YES). 
        IF prog-error THEN RETURN.
      END.
        
      ELSE IF curr-cmd EQ 92 THEN
      DO:
        RUN create-var1(curr-texte, NO).
        IF prog-error THEN RETURN.
      END.          
      ELSE IF curr-cmd EQ 800 THEN 
      DO:
        RUN create-var1(curr-texte, NO).
        IF prog-error THEN RETURN.
      END.

      ELSE IF curr-cmd EQ 9985 OR curr-cmd EQ 9986 OR curr-cmd EQ 1995 
        OR curr-cmd EQ 1996 OR curr-cmd EQ 1997 OR curr-cmd EQ 1998
        OR curr-cmd EQ 1999 THEN  
      DO:
        RUN create-var1(curr-texte, NO).
        IF prog-error THEN RETURN.
      END.
 
      ELSE IF curr-cmd = 179 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd = 180 OR curr-cmd = 181 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd = 813 OR curr-cmd = 814 OR 
        (curr-cmd GE 756 AND curr-cmd LE 758) THEN 
      DO:
         RUN create-var1(curr-texte, YES).
         IF prog-error THEN RETURN.
      END.
 
      ELSE IF curr-cmd EQ 192 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 197 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 552 THEN 
      DO:
        RUN create-var1(curr-texte, YES). 
        IF prog-error THEN RETURN.
      END.

      ELSE IF curr-cmd EQ 1921 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1922 THEN
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1923 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1924 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1971 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1972 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1973 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1974 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1991 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1992 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1993 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1994 THEN  
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
 
      ELSE IF curr-cmd EQ 1008 THEN 
      DO:
        RUN create-var2(curr-texte, NO).
        IF prog-error THEN RETURN.
      END.
      
      ELSE IF curr-cmd EQ 809  THEN 
      DO:
        RUN create-var2(curr-texte, NO).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1084 THEN 
      DO:
        RUN create-var2(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.

      ELSE IF curr-cmd EQ 2001 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2002 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2003 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2004 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2005 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2006 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2007 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2008 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2009 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2010 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2011 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2012 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2013 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2014 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2015 THEN RUN create-var1(curr-texte, YES). /*ITA*/
      ELSE IF curr-cmd EQ 2016 THEN RUN create-var1(curr-texte, YES). /*ITA*/

      /*Gerald Pax food by shift 4079F5*/
      ELSE IF curr-cmd EQ 2020 THEN RUN create-var1(curr-texte, YES). 
      ELSE IF curr-cmd EQ 2021 THEN RUN create-var1(curr-texte, YES). 
      ELSE IF curr-cmd EQ 2022 THEN RUN create-var1(curr-texte, YES). 
      ELSE IF curr-cmd EQ 2023 THEN RUN create-var1(curr-texte, YES). 

      /*Gerald Pax bev by shift 4079F5*/
      ELSE IF curr-cmd EQ 2024 THEN RUN create-var1(curr-texte, YES). 
      ELSE IF curr-cmd EQ 2025 THEN RUN create-var1(curr-texte, YES). 
      ELSE IF curr-cmd EQ 2026 THEN RUN create-var1(curr-texte, YES). 
      ELSE IF curr-cmd EQ 2027 THEN RUN create-var1(curr-texte, YES).

      /*geral G-total daily sales 0ADD87*/
      ELSE IF curr-cmd EQ 2028 THEN RUN create-var1(curr-texte, YES).

      /*gerald tot-bill daily sales 72AF1A*/
      ELSE IF curr-cmd EQ 2029 THEN RUN create-var1(curr-texte, YES).

      /*gerald pax-table daily sales 72AF1A*/
      ELSE IF curr-cmd EQ 2031 THEN RUN create-var3(curr-texte, YES).

      /*gerald Pax Compliment Inhouse , Pax Outsider, Compliment Outsider, Revenue Inhouse & Revenue Outsider E122F2*/
      ELSE IF curr-cmd EQ 2032 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2033 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2034 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2035 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2036 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2037 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2038 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2039 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2040 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2041 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2042 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2043 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2044 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2045 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2046 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2047 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2048 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2049 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2050 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2051 THEN RUN create-var1(curr-texte, YES).
      /*end geral*/

      /*MG QTY-FOOD QTY-BEV E78F9A*/
      ELSE IF curr-cmd EQ 2052 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2053 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2054 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2055 THEN RUN create-var1(curr-texte, YES).
      /*end MG*/  

      /*MG Daily FB Flash : DirectPurchase, TransferSideStore, Cost, Compliment 61236D*/
      ELSE IF curr-cmd EQ 2056 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2057 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2058 THEN RUN create-var1(curr-texte, YES).
      ELSE IF curr-cmd EQ 2059 THEN RUN create-var1(curr-texte, YES).
      /*end MG*/
 
      ELSE IF curr-cmd EQ 9092 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 9813 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 9814 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.

      ELSE IF curr-cmd EQ 8092 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 8813 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 8814 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.

      ELSE IF curr-cmd EQ 9981 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 9982 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 9983 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 9984 THEN 
      DO:
        RUN create-var1(curr-texte, YES).
        IF prog-error THEN RETURN.
      END.
 
      ELSE IF curr-cmd = 840 THEN 
      DO: 
        actual-cmd = curr-cmd. 
        RUN create-group(curr-texte).
        IF prog-error THEN RETURN.
      END. 
    END. 
    ELSE IF actual-cmd = 840 AND curr-texte NE "" THEN 
    DO:
      RUN create-group-variable(curr-texte).
      IF prog-error THEN RETURN.
    END.       
  END. 
END. 

IF prog-error THEN RETURN.
              
RUN fo-parxls-gsbl.p
    (pvILanguage, ytd-flag, jan1, Ljan1, Lfrom-date, Lto-date,
     Pfrom-date, Pto-date, from-date, to-date, start-date, lytd-flag,
     lmtd-flag, pmtd-flag, lytoday-flag, lytoday, foreign-flag,
     budget-flag, foreign-nr, price-decimal,briefnr,link,budget-all,TABLE w1,TABLE w2,
     OUTPUT msg-str, OUTPUT error-nr).
IF msg-str NE "" THEN RETURN.
ELSE
DO:
  mess-result = "Successfully generate data".
  success-flag = YES.
END.

/*OS-COMMAND SILENT VALUE("start " + link).*/
 
/*************************  PROCEDURES  ****************************************/ 
PROCEDURE create-var0: 
  DEFINE INPUT PARAMETER texte AS CHAR. 
  DEFINE INPUT PARAMETER int-flag AS LOGICAL. 
  DEFINE VARIABLE subtext AS CHAR. 
  RUN get-subtext (texte, INPUT-OUTPUT subtext). 
  
  IF subtext = "" THEN 
  DO:     
    msg-str = translateExtended ("Program expected a new key variable name .xxx",lvCAREA,"") 
      + CHR(10) +
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) +
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
  ELSE IF SUBSTR(subtext, 1, 1) NE keyvar THEN 
  DO:    
    msg-str = translateExtended ("Program expected",lvCAREA,"") + " " + keyvar + " " + translateExtended ("for any variable",lvCAREA,"") 
      + CHR(10) + 
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) +  
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
  ELSE 
  DO: 
    varname = subtext. 
    CREATE w1. 
    curr-nr = curr-nr + 1. 
    w1.nr = curr-nr. 
    w1.int-flag = int-flag. 
    w1.varname = varname. 
    w1.main-code = curr-cmd. 
    curr-column = LENGTH(curr-texte) + 1. 
    curr-cmd = 0. 
  END. 
END. 
 
PROCEDURE create-var1: 
  DEFINE INPUT PARAMETER texte      AS CHAR. 
  DEFINE INPUT PARAMETER int-flag   AS LOGICAL. 
  DEFINE VARIABLE subtext   AS CHAR. 
  DEFINE VARIABLE correct   AS LOGICAL. 
  DEFINE VARIABLE nr        AS INTEGER INITIAL 0. 
  IF texte = "" THEN RETURN.
  RUN get-subtext (texte, INPUT-OUTPUT subtext). 
  IF subtext = "" THEN 
  DO:     
    msg-str = translateExtended ("Program expected a new key variable name .xxx",lvCAREA,"") 
      + CHR(10) + 
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) + 
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
  ELSE IF SUBSTR(subtext, 1, 1) NE keyvar THEN 
  DO:     
    msg-str = translateExtended ("Program expected",lvCAREA,"") + " " + keyvar + " " + translateExtended ("for any variable",lvCAREA,"") 
      + CHR(10) + 
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) + 
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
  ELSE 
  DO: 
    varname = subtext. 
    subtext = TRIM(SUBSTR(texte, curr-column, LENGTH(texte) - curr-column + 1)). 
    IF curr-cmd = 800 OR curr-cmd = 180 OR curr-cmd = 181 OR curr-cmd = 9985
        OR curr-cmd = 9986 OR curr-cmd = 1995 OR curr-cmd = 1996 
        OR curr-cmd = 1997 OR curr-cmd = 1998 OR curr-cmd = 1999 THEN.
    ELSE RUN check-integer(subtext, OUTPUT correct). 
    IF correct THEN nr = INTEGER(subtext). 
    CREATE w1. 
    curr-nr = curr-nr + 1. 
    w1.nr = curr-nr. 
    w1.int-flag = int-flag. 
    w1.varname = varname. 
    w1.main-code = curr-cmd. 
 
    IF curr-cmd = 192 THEN w1.dept = nr. 
    ELSE IF curr-cmd = 197 THEN w1.dept = nr. 
    ELSE IF curr-cmd = 552 THEN w1.dept = nr. 
    ELSE w1.artnr = nr. 

    IF curr-cmd = 1921 THEN w1.dept = nr. 
    IF curr-cmd = 1922 THEN w1.dept = nr. 
    IF curr-cmd = 1923 THEN w1.dept = nr. 
    IF curr-cmd = 1924 THEN w1.dept = nr. 

    IF curr-cmd = 1971 THEN w1.dept = nr. 
    IF curr-cmd = 1972 THEN w1.dept = nr. 
    IF curr-cmd = 1973 THEN w1.dept = nr. 
    IF curr-cmd = 1974 THEN w1.dept = nr. 

    IF curr-cmd = 1991 THEN w1.dept = nr. 
    IF curr-cmd = 1992 THEN w1.dept = nr. 
    IF curr-cmd = 1993 THEN w1.dept = nr. 
    IF curr-cmd = 1994 THEN w1.dept = nr. 
    
    IF curr-cmd = 2001 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2002 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2003 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2004 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).

    IF curr-cmd = 2005 THEN w1.dept = nr. 
    IF curr-cmd = 2006 THEN w1.dept = nr. 
    IF curr-cmd = 2007 THEN w1.dept = nr. 
    IF curr-cmd = 2008 THEN w1.dept = nr. 
    
    IF curr-cmd = 2009 THEN w1.dept = nr. 
    IF curr-cmd = 2010 THEN w1.dept = nr. 
    IF curr-cmd = 2011 THEN w1.dept = nr. 
    IF curr-cmd = 2012 THEN w1.dept = nr. 

    IF curr-cmd = 2013 THEN w1.dept = nr. 
    IF curr-cmd = 2014 THEN w1.dept = nr. 
    IF curr-cmd = 2015 THEN w1.dept = nr. 
    IF curr-cmd = 2016 THEN w1.dept = nr. 

    /*Gerald Pax food by shift 4079F5*/
    IF curr-cmd = 2020 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2021 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2022 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)). 
    IF curr-cmd = 2023 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).

    /*Gerald Pax bev by shift 4079F5*/
    IF curr-cmd = 2024 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2025 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2026 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2027 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).

    /*geral G-total daily sales 0ADD87*/
    IF curr-cmd = 2028 THEN w1.dept = nr. 

    /*gerald tot-bill daily sales 72AF1A*/
    IF curr-cmd = 2029 THEN w1.dept = nr.

    IF curr-cmd = 2032 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2033 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2034 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2035 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2036 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2037 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2038 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2039 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2040 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2041 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2042 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2043 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2044 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2045 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2046 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2047 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2048 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2049 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2050 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).
    IF curr-cmd = 2051 THEN w1.dept = INTEGER(SUBSTR(subtext,2,3)).

    /*MG QTY-FOOD QTY-BEV E78F9A*/
    IF curr-cmd = 2052 THEN w1.dept = nr. 
    IF curr-cmd = 2053 THEN w1.dept = nr. 
    IF curr-cmd = 2054 THEN w1.dept = nr. 
    IF curr-cmd = 2055 THEN w1.dept = nr.
    /*end MG*/

    /*MG Daily FB Flash : DirectPurchase, TransferSideStore, Cost, Compliment 61236D*/
    IF curr-cmd = 2056 THEN w1.dept = nr. 
    IF curr-cmd = 2057 THEN w1.dept = nr. 
    IF curr-cmd = 2058 THEN w1.dept = nr. 
    IF curr-cmd = 2059 THEN w1.dept = nr.
    /*end MG*/

    IF curr-cmd = 800 OR curr-cmd = 180 OR curr-cmd = 181 OR curr-cmd = 9985
        OR curr-cmd = 9986 OR curr-cmd = 1995 OR curr-cmd = 1996 
        OR curr-cmd = 1997 OR curr-cmd = 1998 OR curr-cmd = 1999 THEN
        w1.s-artnr = subtext.

    curr-column = LENGTH(curr-texte) + 1. 
    curr-cmd = 0. 
  END. 
END. 
 
PROCEDURE create-var2: 
  DEFINE INPUT PARAMETER texte AS CHAR. 
  DEFINE INPUT PARAMETER int-flag AS LOGICAL. 
  DEFINE VARIABLE subtext AS CHAR. 
  DEFINE VARIABLE correct AS LOGICAL. 
  DEFINE VARIABLE nr      AS INTEGER INITIAL 0. 
  DEFINE VARIABLE dept    AS INTEGER. 
  RUN get-subtext (texte, INPUT-OUTPUT subtext). 
  IF subtext = "" THEN 
  DO:     
    msg-str = translateExtended ("Program expected a new key variable name .xxx",lvCAREA,"") 
      + CHR(10) + 
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) + 
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
  ELSE IF SUBSTR(subtext, 1, 1) NE keyvar THEN 
  DO:  
    msg-str = translateExtended ("Program expected",lvCAREA,"") + " " + keyvar + " " + translateExtended ("for any variable",lvCAREA,"") 
      + CHR(10) + 
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) + 
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
  ELSE 
  DO: 
    varname = subtext. 
    subtext = TRIM(SUBSTR(texte, curr-column, LENGTH(texte) - curr-column + 1)). 
    RUN check-integer(subtext, OUTPUT correct). 
    IF correct THEN 
    DO: 
      dept = INTEGER(SUBSTR(subtext,1,2)). 
      nr = INTEGER(SUBSTR(subtext,3,6)). 
    END. 
    CREATE w1. 
    curr-nr = curr-nr + 1. 
    w1.nr = curr-nr. 
    w1.int-flag = int-flag. 
    w1.varname = varname. 
    w1.main-code = curr-cmd. 
    w1.artnr = nr. 
    w1.dept = dept. 
    curr-column = LENGTH(curr-texte) + 1. 
    curr-cmd = 0. 
  END. 
END.
 
PROCEDURE create-w1: 
  DEFINE OUTPUT PARAMETER ind AS INTEGER. 
  DEFINE VARIABLE w1-nr AS INTEGER. 
  CREATE w1. 
  curr-nr = curr-nr + 1. 
  ind = curr-nr. 
  w1-nr = curr-nr. 
  w1.nr = curr-nr. 
  w1.varname = varname. 
  w1.grpflag = grpflag. 
  /* 0 = single VARIABLE, 2 = group, 3 = dept, 9 = abbreviation  */ 
  IF grpflag = 2 THEN 
  DO: 
      w1.bezeich = bezeich. 
  END. 
  ELSE IF grpflag = 9 THEN 
  DO: 
    w1.bezeich = bezeich. 
  END. 
END. 
 
 
PROCEDURE create-w2: 
DEFINE INPUT PARAMETER ind AS INTEGER. 
DEFINE INPUT PARAMETER nr2 AS INTEGER. 
DEFINE INPUT PARAMETER nr AS INTEGER. 
DEFINE INPUT PARAMETER val-sign AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
  IF nr = 2 THEN  /* this is VARIABLE */ 
  DO: 
    CREATE w2. 
    w2.nr1 = ind. 
    w2.nr2 = nr2. 
  END. 
  w2.val-sign = val-sign. 
END. 
 
PROCEDURE analyse-textheader: 
DEFINE INPUT PARAMETER texte AS CHAR. 
DEFINE VARIABLE subtext AS CHAR INITIAL "". 
  RUN get-subtext (texte, INPUT-OUTPUT subtext). 
  IF subtext NE "" THEN  RUN interprete-subtext (texte, subtext). 
END. 
 
PROCEDURE get-subtext: 
  DEFINE INPUT PARAMETER texte AS CHAR. 
  DEFINE INPUT-OUTPUT PARAMETER subtext AS CHAR. 
  DEFINE VARIABLE j AS INTEGER. 
  DEFINE VARIABLE stopped AS LOGICAL. 
  texte = TRIM(SUBSTR(texte, curr-column, LENGTH(texte) - curr-column + 1)). 
  
  stopped = NO. 
  j = 1. 
  DO WHILE NOT stopped: 
    IF  j EQ LENGTH(texte) OR SUBSTR(texte, j + 1, 1) = " " THEN stopped = YES. 
    ELSE j = j + 1. 
  END.
   subtext = SUBSTR(texte, 1, j). 
   curr-column = curr-column + j + 1.
END. 
 
PROCEDURE interprete-subtext: 
  DEFINE INPUT PARAMETER texte AS CHAR. 
  DEFINE INPUT PARAMETER subtext AS CHAR. 
  DEFINE VARIABLE j AS INTEGER. 
  DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
  FIND FIRST htp-list NO-LOCK. 
  DO WHILE AVAILABLE htp-list AND NOT found: 
    IF htp-list.fchar = subtext THEN 
    DO: 
      found = YES. 
      curr-cmd = htp-list.paramnr. 
    END. 
    FIND NEXT htp-list NO-LOCK NO-ERROR. 
  END. 
  IF NOT found THEN 
  DO:    
    msg-str = translateExtended ("Can not understand line",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) + SUBSTR(curr-texte, 1, LENGTH(curr-texte)).             
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
END. 
 
PROCEDURE check-integer: 
DEFINE INPUT PARAMETER texte AS CHAR. 
DEFINE OUTPUT PARAMETER correct AS LOGICAL INITIAL YES. 
DEFINE VARIABLE i AS INTEGER. 
  IF length (texte) = 0 THEN correct = NO. 
  DO i = 1 TO LENGTH(texte): 
    IF ASC(SUBSTR(texte, i, 1)) GT 57 OR ASC(SUBSTR(texte, i, 1)) LT 48 
    THEN correct = NO. 
  END. 
  IF NOT correct THEN 
  DO:     
    msg-str = translateExtended ("Program expected a number : ",lvCAREA,"") + texte 
      + CHR(10) +
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) + 
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
END. 
 
PROCEDURE create-group: 
  DEFINE INPUT PARAMETER texte AS CHAR. 
  DEFINE VARIABLE subtext AS CHAR. 
  DEFINE VARIABLE correct AS LOGICAL. 
  RUN get-subtext (texte, INPUT-OUTPUT subtext). 
  IF subtext = "" THEN 
  DO:     
    msg-str = translateExtended ("Program expected a variable name",lvCAREA,"") 
      + CHR(10) + 
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) +
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)).      
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
  ELSE IF SUBSTR(subtext, 1, 1) NE keyvar THEN 
  DO:     
    msg-str = translateExtended ("Program expected",lvCAREA,"") + " " + keyvar + " " + translateExtended ("for any variable",lvCAREA,"") 
      + CHR(10) + 
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row) 
      + CHR(10) + 
      SUBSTR(curr-texte, 1, LENGTH(curr-texte)).     
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
  ELSE 
  DO: 
    varname = subtext. 
    bezeich = TRIM(SUBSTR(texte, curr-column, LENGTH(texte) - curr-column + 1)). 
    IF  bezeich = "" THEN 
    DO:       
      msg-str = translateExtended ("Program expected a description",lvCAREA,"") 
        + CHR(10) + 
        translateExtended ("at line number : ",lvCAREA,"") + STRING(curr-row) 
        + CHR(10) + 
        SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
      prog-error = YES. 
      error-nr = - 1. 
      RETURN. 
    END. 
    ELSE 
    DO: 
      grpflag = 2. 
      RUN create-w1(OUTPUT grp-nr). 
      curr-column = LENGTH(texte) + 1. 
    END. 
  END. 
END. 
 
PROCEDURE create-group-variable: 
DEFINE INPUT PARAMETER texte AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE val-sign AS INTEGER INITIAL 1. 
  FIND FIRST htp-list WHERE htp-list.paramnr = 287 no-lock.  /* $END */ 
  IF texte = htp-list.fchar THEN 
  DO: 
    actual-cmd = 0. 
    RETURN. 
  END. 
  IF SUBSTR(texte, 1, 1) = "-" THEN 
  DO: 
    val-sign = - 1. 
    texte = SUBSTR(texte, 2, LENGTH(texte)). 
    texte = TRIM(texte). 
  END. 
  IF SUBSTR(texte, 1, 1) = keyvar THEN 
  DO: 
    FIND FIRST w1 WHERE w1.varname = texte NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE w1 THEN 
    DO:       
      msg-str = translateExtended ("No such variable found",lvCAREA,"") + " "+ texte 
        + CHR(10) + 
        translateExtended ("at line number :",lvCAREA,"") + " " + STRING(curr-row) 
        + CHR(10) + 
        SUBSTR(curr-texte, 1, LENGTH(curr-texte)). 
      prog-error = YES. 
      error-nr = - 1. 
      RETURN. 
    END. 
    ELSE RUN create-w2(grp-nr, w1.nr, 2, val-sign). 
  END. 
END. 
 
 


