/************************************************************************   
Program FOR interpreting User's FO-Reports, OUTPUT exported TO EXCEL   
This will be called FOR example BY XXXXXXXX   
   
RESTRICTIONS:   
1. BEGIN AND END commands have TO be defined IN a seperate line   
2. LM+ 10,  TAB 10 AND skip10 are allowed !!   
   
*********************************************************/   
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.      
DEFINE INPUT PARAMETER briefnr          AS INTEGER.   
DEFINE INPUT PARAMETER to-date          AS DATE.  
DEFINE INPUT PARAMETER check-only       AS LOGICAL. /*Yes*/  
DEFINE INPUT PARAMETER view-only        AS LOGICAL. /*No*/  
DEFINE INPUT PARAMETER jobnr            AS CHAR.    /*""*/
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER INITIAL "".
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL INITIAL NO.

/**************************** WIDGET ****************************/
{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "fo-parexcel".
  
DEFINE VARIABLE budget-flag     AS LOGICAL INITIAL NO.   
DEFINE VARIABLE ytd-flag        AS LOGICAL INITIAL NO.   
DEFINE VARIABLE lytd-flag       AS LOGICAL INITIAL NO.   
DEFINE VARIABLE lmtd-flag       AS LOGICAL INITIAL NO.   
DEFINE VARIABLE pmtd-flag       AS LOGICAL INITIAL NO.   
   
DEFINE VARIABLE integer-flag    AS LOGICAL.   
DEFINE VARIABLE serv-vat        AS LOGICAL.   
   
DEFINE VARIABLE zeit            AS INTEGER.   
DEFINE VARIABLE margin-c        AS CHAR.   
DEFINE VARIABLE len-flag        AS LOGICAL INITIAL YES.   
DEFINE VARIABLE detail-nr       AS INTEGER.   
   
DEFINE VARIABLE no-decimal      AS LOGICAL INITIAL NO.   
DEFINE VARIABLE num-digit       AS INTEGER INITIAL 12.   
   
DEFINE VARIABLE value-filled    AS LOGICAL INITIAL NO.   
DEFINE VARIABLE prog-error      AS LOGICAL INITIAL NO.   
DEFINE VARIABLE error-nr        AS INTEGER INITIAL 0.   
DEFINE VARIABLE curr-row        AS INTEGER INITIAL 0.   
DEFINE VARIABLE curr-column     AS INTEGER.   
DEFINE VARIABLE curr-cmd        AS INTEGER INITIAL 0.   
DEFINE VARIABLE curr-texte      AS CHAR.   
DEFINE VARIABLE actual-cmd      AS INTEGER INITIAL 0.   
DEFINE VARIABLE detail-loop     AS INTEGER INITIAL 0.   
   
DEFINE VARIABLE grp-nr          AS INTEGER.   
DEFINE VARIABLE curr-nr         AS INTEGER INITIAL 0.   
DEFINE VARIABLE varname         AS CHAR FORMAT "x(24)".   
DEFINE VARIABLE bezeich         AS CHAR.   
DEFINE VARIABLE grpflag         AS INTEGER.   
/* 0 = single account, 1 = main account, 2 = group account, 3 = dept  */   
DEFINE VARIABLE textlen         AS INTEGER INITIAL 30.   
DEFINE VARIABLE report-title    AS CHAR FORMAT "x(80)".   
   
DEFINE VARIABLE from-date       AS DATE.   
DEFINE VARIABLE Lfrom-date      AS DATE.   
DEFINE VARIABLE Lto-date        AS DATE.   
DEFINE VARIABLE jan1            AS DATE.   
DEFINE VARIABLE Ljan1           AS DATE.   
DEFINE VARIABLE Pfrom-date      AS DATE.   
DEFINE VARIABLE Pto-date        AS DATE.   
   
DEFINE VARIABLE outfile-dir     AS CHAR.  
   
DEFINE VARIABLE efield AS CHAR VIEW-AS EDITOR INNER-LINES 23 INNER-CHARS 80   
  FONT 1 BGCOLOR 1 FGCOLOR 15.

DEFINE VARIABLE dayname AS CHAR FORMAT "x(12)" EXTENT 7 INITIAL   
  ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].   
   
DEFINE VARIABLE curr-loop       AS INTEGER INITIAL 0.   
DEFINE VARIABLE f-lmargin       AS LOGICAL INITIAL NO.   
DEFINE VARIABLE lmargin         AS INTEGER INITIAL 1.   
DEFINE VARIABLE nskip           AS INTEGER INITIAL 1.   
DEFINE VARIABLE ntab            AS INTEGER INITIAL 1.   
DEFINE VARIABLE n               AS INTEGER.   
DEFINE VARIABLE curr-pos        AS INTEGER.   
DEFINE VARIABLE keycmd          AS CHAR.   
DEFINE VARIABLE keyvar          AS CHAR.   
DEFINE VARIABLE infile          AS CHAR FORMAT "x(60)".   
DEFINE VARIABLE outfile         AS CHAR FORMAT "x(60)".   
   
DEFINE VARIABLE foreign-flag    AS LOGICAL INITIAL NO.   
DEFINE VARIABLE foreign-nr      AS INTEGER INITIAL 0 NO-UNDO.   
   
DEFINE VARIABLE start-date      AS DATE INITIAL ?.   
DEFINE VARIABLE lytoday         AS DATE.   
DEFINE VARIABLE lytoday-flag    AS LOGICAL.   
   
DEFINE VARIABLE ratio-flag      AS INTEGER INITIAL 0.   
DEFINE VARIABLE price-decimal   AS INTEGER.  
DEFINE VARIABLE msg-ans         AS LOGICAL.
   
DEFINE STREAM s1.   
DEFINE STREAM s2.   
     
/******************** TEMP-TABLE ********************/      
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
  FIELD fchar   AS CHAR.   
   
DEFINE TEMP-TABLE htv-list   
  FIELD paramnr AS INTEGER   
  FIELD fchar   AS CHAR.   
   
DEFINE TEMP-TABLE w1   
  FIELD nr          AS INTEGER   
  FIELD varname     AS CHAR   
  FIELD main-code   AS INTEGER   /* eg. 805 FOR AVAILABLE room */   
  FIELD artnr       AS INTEGER  
  FIELD s-artnr     AS CHARACTER 
  FIELD dept        AS INTEGER   
  FIELD grpflag     AS INTEGER INITIAL 0   
  FIELD done        AS LOGICAL INITIAL NO   
  FIELD bezeich     AS CHAR   
  FIELD int-flag    AS LOGICAL INITIAL NO   
   
  FIELD tday        AS DECIMAL INITIAL 0   
  FIELD saldo       AS DECIMAL INITIAL 0   
  FIELD lastmon     AS DECIMAL INITIAL 0   
  FIELD lastyr      AS DECIMAL INITIAL 0   
  FIELD lytoday     AS DECIMAL INITIAL 0   
  FIELD ytd-saldo   AS DECIMAL INITIAL 0   
  FIELD lytd-saldo  AS DECIMAL INITIAL 0   
   
  FIELD tbudget     AS DECIMAL INITIAL 0   
  FIELD budget      AS DECIMAL INITIAL 0   
  FIELD lm-budget   AS DECIMAL INITIAL 0   
  FIELD ly-budget   AS DECIMAL INITIAL 0   
  FIELD ytd-budget  AS DECIMAL INITIAL 0   
  FIELD lytd-budget AS DECIMAL INITIAL 0.   
   
DEFINE TEMP-TABLE w2   
  FIELD val-sign    AS INTEGER INITIAL 1   
  FIELD nr1         AS INTEGER   
  FIELD nr2         AS INTEGER.   
   
DEFINE TEMP-TABLE w11   
  FIELD nr      AS INTEGER   
  FIELD debit   AS DECIMAL   
  FIELD credit  AS DECIMAL.   
   
DEFINE BUFFER parent-w1 FOR w1.   
DEFINE BUFFER child-w1  FOR w1.   
DEFINE BUFFER w1-ratio  FOR w1.     
DEFINE BUFFER segmbuff  FOR segmentstat.   

/******************** MAIN LOGIC ********************/     
zeit = TIME.   
  
RUN prepare-fo-parexcelbl.p  
    (briefnr, OUTPUT serv-vat, OUTPUT foreign-nr, OUTPUT start-date,  
    OUTPUT price-decimal, OUTPUT no-decimal, OUTPUT outfile-dir,  
    OUTPUT keycmd, OUTPUT keyvar, OUTPUT TABLE batch-list,  
    OUTPUT TABLE htv-list, OUTPUT TABLE htp-list,  
    OUTPUT TABLE brief-list).  
  
CREATE detail-list.   
detail-list.nr = 0.   
/*   
IF NOT check-only THEN   
*/   
DO:   
DEFINE VARIABLE datum AS DATE.   
  from-date  = TODAY - 1.
  IF to-date = ? THEN RETURN.   
  from-date  = DATE(MONTH(to-date), 1, YEAR(to-date)).   
    
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
  
FIND FIRST batch-list.  
/*
IF NOT check-only AND NOT view-only THEN   
DO:   
  infile = batch-list.fname.  
  INPUT STREAM s2 FROM VALUE(infile).  
  IF jobnr = "" THEN outfile = "VHP.SLK".  
  ELSE outfile = outfile-dir + "r" + jobnr + ".SLK".  
  OUTPUT STREAM s1 TO VALUE(outfile).  
END.   
*/   
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
          OR curr-cmd = 288 OR curr-cmd = 1019 /* Day Use Rooms */ THEN 
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
          OR curr-cmd = 969 OR curr-cmd = 9106 
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
      ELSE IF curr-cmd EQ 809 THEN 
      DO:
          RUN create-var2(curr-texte, NO).
          IF prog-error THEN RETURN.
      END.
      ELSE IF curr-cmd EQ 1084 THEN 
      DO:
          RUN create-var2(curr-texte, YES).
          IF prog-error THEN RETURN.
      END.

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
      END.   
    END.   
    ELSE IF actual-cmd = 840 AND curr-texte NE "" THEN   
      RUN create-group-variable(curr-texte).   
  END.   
END.  
/*   
IF NOT check-only AND NOT value-filled THEN   
DO:   
  /*MTRUN fill-value.*/  
  RUN fo-parexcelbl.p  
      (pvILanguage, ytd-flag, jan1, Ljan1, Lfrom-date, Lto-date,  
       from-date, to-date, start-date, lytd-flag, lmtd-flag, pmtd-flag,  
       Pfrom-date, Pto-date, lytoday-flag, lytoday, foreign-flag,  
       budget-flag, OUTPUT error-nr, OUTPUT msg-str,  
       INPUT-OUTPUT TABLE w1, INPUT-OUTPUT TABLE w2).  
  IF msg-str NE "" THEN  
  DO:  
      RUN program-message.p(msg-str, OUTPUT msg-ans).  
      RETURN.  
  END.  
  RUN read-exfile.  
  IF prog-error THEN RETURN.   
  INPUT STREAM s2 CLOSE.   
  OUTPUT STREAM s1 CLOSE.   
  IF jobnr EQ "" THEN RUN excel-slk.   
END.   
*/     
   
IF check-only AND error-nr EQ 0 THEN   
DO:  
    msg-str = translateExtended("Syntax is correct.",lvCAREA,"").
    success-flag = YES.
END.   
   
/*************************************  PROCEDURES  **********************************/      
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
      SUBSTR(curr-texte, 1, length(curr-texte)).   
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
      SUBSTR(curr-texte, 1, length(curr-texte)).      
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
  DEFINE INPUT PARAMETER texte AS CHAR.   
  DEFINE INPUT PARAMETER int-flag AS LOGICAL.   
  DEFINE VARIABLE subtext AS CHAR.   
  DEFINE VARIABLE correct AS LOGICAL.   
  DEFINE VARIABLE nr AS INTEGER INITIAL 0.   
  RUN get-subtext (texte, INPUT-OUTPUT subtext).   
  IF subtext = "" THEN   
  DO:       
    msg-str = translateExtended ("Program expected a new key variable name .xxx",lvCAREA,"")   
      + CHR(10) +   
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
      + CHR(10) +   
      SUBSTR(curr-texte, 1, length(curr-texte)).   
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
      SUBSTR(curr-texte, 1, length(curr-texte)).   
    prog-error = YES.   
    error-nr = - 1.   
    RETURN.   
  END.   
  ELSE   
  DO:   
    varname = subtext.   
    subtext = TRIM(SUBSTR(texte, curr-column, length(texte) - curr-column + 1)).   
    IF curr-cmd = 800 OR curr-cmd = 180 OR curr-cmd = 181 THEN.
    ELSE
    RUN check-integer(subtext, OUTPUT correct).   
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
   
    curr-column = LENGTH(curr-texte) + 1.   
    curr-cmd = 0.   
  END.   
END.   
   
PROCEDURE create-var2:   
  DEFINE INPUT PARAMETER texte AS CHAR.   
  DEFINE INPUT PARAMETER int-flag AS LOGICAL.   
  DEFINE VARIABLE subtext AS CHAR.   
  DEFINE VARIABLE correct AS LOGICAL.   
  DEFINE VARIABLE nr AS INTEGER INITIAL 0.   
  DEFINE VARIABLE dept AS INTEGER.   
  RUN get-subtext (texte, INPUT-OUTPUT subtext).   
  IF subtext = "" THEN   
  DO:       
    msg-str = translateExtended ("Program expected a new key variable name .xxx",lvCAREA,"")   
      + CHR(10) +   
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
      + CHR(10) +   
      SUBSTR(curr-texte, 1, length(curr-texte)).   
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
      SUBSTR(curr-texte, 1, length(curr-texte)).     
    prog-error = YES.   
    error-nr = - 1.   
    RETURN.   
  END.   
  ELSE   
  DO:   
    varname = subtext.   
    subtext = TRIM(SUBSTR(texte, curr-column, length(texte) - curr-column + 1)).   
    RUN check-integer(subtext, OUTPUT correct).   
    IF correct THEN   
    DO:   
      dept = INTEGER(SUBSTR(subtext,1,2)).   
      nr = INTEGER(SUBSTR(subtext,3,6)).   
    END.   
    create w1.   
    curr-nr = curr-nr + 1.   
    w1.nr = curr-nr.   
    w1.int-flag = int-flag.   
    w1.varname = varname.   
    w1.main-code = curr-cmd.   
    w1.artnr = nr.   
    w1.dept = dept.   
    curr-column = length(curr-texte) + 1.   
    curr-cmd = 0.   
  END.   
END.   
  
/*   
PROCEDURE build-text-line:   
DEFINE INPUT PARAMETER texte AS CHAR.   
DEFINE VARIABLE i AS INTEGER.   
DEFINE VARIABLE j AS INTEGER INITIAL 1.   
DEFINE VARIABLE n AS INTEGER.   
DEFINE VARIABLE found AS LOGICAL INITIAL NO.   
   
  DO i = 1 TO length(texte):   
    IF SUBSTR(texte,i,1) = keycmd THEN   
    DO:   
      IF i = length(texte) THEN found = NO.   
      ELSE IF SUBSTR(texte, i + 1, 1) = " " THEN found = NO.   
      ELSE   
      DO:   
        len-flag = YES.   
        RUN put-string(SUBSTR(texte, j, i - j)).   
        RUN interprete-cmd(texte, INPUT-OUTPUT i, OUTPUT found).   
        j = i + 1.   
      END.   
    END.   
   
    ELSE IF SUBSTR(texte,i,1) = keyvar THEN   
    DO:   
      IF i = length(texte) THEN found = NO.   
      ELSE IF SUBSTR(texte, i + 1, 1) = " " THEN found = NO.   
      ELSE   
      DO:   
        len-flag = YES.   
        RUN put-string(SUBSTR(texte, j, i - j - 1)).   
        /* - 1 because exclude " */   
        RUN interprete-var(texte, INPUT-OUTPUT i, OUTPUT found).   
        j = i + 1.   
      END.   
    END.   
    ELSE found = NO.   
  END.   
  IF NOT found THEN   
  DO:   
    IF curr-loop = 1 THEN   
    DO:   
      hide MESSAGE NO-PAUSE.   
      MESSAGE translateExtended ("Can not interprete the command - line",lvCAREA,"") + " " + STRING(curr-row)   
         SKIP   
         SUBSTR(curr-texte, 1, length(curr-texte))   
         VIEW-AS ALERT-BOX ERROR.   
         prog-error = YES.   
         error-nr = - 1.   
       RETURN.   
    END.   
    ELSE IF curr-loop = 2 THEN RUN put-string (SUBSTR(texte, j,   
      length(texte) - j + 1)).   
    ELSE   
    DO:   
       RUN put-string (SUBSTR(curr-texte, j, length(curr-texte) - j + 1)).   
    END.   
  END.   
END.   
*/
/*
PROCEDURE interprete-cmd:   
DEFINE INPUT PARAMETER texte AS CHAR.   
DEFINE INPUT-OUTPUT PARAMETER i AS INTEGER.   
DEFINE OUTPUT PARAMETER found AS LOGICAL INITIAL NO.   
DEFINE VARIABLE j AS INTEGER.   
  j = i.   
  FIND FIRST htp-list.   
  DO WHILE AVAILABLE htp-list AND NOT found:   
    IF htp-list.fchar = SUBSTR(texte, j, length(htp-list.fchar)) THEN   
    DO:   
      found = YES.   
      i = j + length(htp-list.fchar) - 1.   
      RUN decode-key(texte, INPUT htp-list.paramnr, INPUT-OUTPUT i).   
      IF prog-error THEN RETURN.   
    END.   
    FIND NEXT htp-list NO-ERROR.   
  END.   
  IF NOT found THEN   
  DO:   
   len-flag = YES.   
   RUN put-string(SUBSTR(texte, j, 1)).   
  END.   
END.   
*/
/*
PROCEDURE interprete-var:   
DEFINE INPUT PARAMETER texte AS CHAR.   
DEFINE INPUT-OUTPUT PARAMETER i AS INTEGER.   
DEFINE OUTPUT PARAMETER found AS LOGICAL INITIAL NO.   
DEFINE VARIABLE j AS INTEGER.   
DEFINE VARIABLE text1 AS CHAR.   
DEFINE buffer ww1 FOR w1.   
  j = i.   
  text1 = texte.   
  FOR EACH w1 NO-LOCK BY w1.varname descending:   
    IF NOT found THEN   
    DO:   
      IF w1.varname = SUBSTR(texte, j, length(w1.varname))   
        AND w1.grpflag EQ 9 THEN   
      DO:   
        text1 = SUBSTR(texte, 1, j - 1) + w1.bezeich   
              + SUBSTR(texte, j + length(w1.varname), length(texte)).   
        found = YES.   
      END.   
    END.   
  END.   
   
  found = NO.   
  FOR EACH w1 NO-LOCK BY w1.varname descending:   
    IF NOT found THEN   
    DO:   
      IF w1.varname = SUBSTR(text1, j, length(w1.varname)) THEN   
      DO:   
        found = YES.   
        i = j + length(w1.varname) - 1.   
   
        integer-flag = w1.int-flag.   
        RUN interprete-field(text1, INPUT-OUTPUT i, OUTPUT found).   
     END.   
   END.   
  END.   
  IF NOT found THEN   
  DO:   
   len-flag = YES.   
   RUN put-string(SUBSTR(texte, j, 1)).   
  END.   
END.   
*/
/*
PROCEDURE interprete-field:   
DEFINE INPUT PARAMETER texte    AS CHAR.   
DEFINE INPUT-OUTPUT PARAMETER i AS INTEGER.   
DEFINE OUTPUT PARAMETER found   AS LOGICAL INITIAL NO.   
DEFINE VARIABLE var-found       AS LOGICAL INITIAL NO.   
DEFINE VARIABLE j               AS INTEGER.  
DEFINE VARIABLE paramNo         AS INTEGER INITIAL 0.  
DEFINE BUFFER curr-w1 FOR w1.   
   
  j = i + 1.   
  ratio-flag = 0.   
/* check, IF it is a ratio (absolute) e.g. ^v1/^v2.balance  */   
  IF SUBSTR(texte, j, 1) = "/" THEN   
  DO:   
    j = j + 1.   
    FOR EACH curr-w1 NO-LOCK BY curr-w1.varname descending:   
      IF NOT var-found THEN   
      DO:   
        IF curr-w1.varname = SUBSTR(texte, j, length(curr-w1.varname)) THEN   
        DO:   
          ratio-flag = 3.   
          var-found = YES.   
          i = j + length(curr-w1.varname) - 1.   
          j = i + 1.   
          FIND FIRST w1-ratio WHERE w1-ratio.nr = curr-w1.nr NO-LOCK.   
        END.   
      END.   
    END.   
    IF NOT var-found THEN   
    DO:   
       hide MESSAGE NO-PAUSE.   
       MESSAGE translateExtended ("Ratio-Variable was missing",lvCAREA,"")   
           SKIP   
           translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
           SKIP   
           SUBSTR(curr-texte, 1, length(curr-texte))   
           VIEW-AS ALERT-BOX ERROR.   
       prog-error = YES.   
       error-nr = - 1.   
       RETURN.   
    END.   
  END.   
   
/* check, IF it is a ratio (IN %) e.g. ^v1:^v2.balance  */   
  ELSE IF SUBSTR(texte, j, 1) = ":" THEN   
  DO:   
    j = j + 1.   
    FOR EACH curr-w1 NO-LOCK BY curr-w1.varname descending:   
      IF NOT var-found THEN   
      DO:   
        IF curr-w1.varname = SUBSTR(texte, j, length(curr-w1.varname)) THEN   
        DO:   
          ratio-flag = 1.   
          var-found = YES.   
          i = j + length(curr-w1.varname) - 1.   
          j = i + 1.   
          FIND FIRST w1-ratio WHERE w1-ratio.nr = curr-w1.nr NO-LOCK.   
        END.   
      END.   
    END.   
    IF NOT var-found THEN   
    DO:   
       hide MESSAGE NO-PAUSE.   
       MESSAGE translateExtended ("Ratio-Variable was missing",lvCAREA,"")   
           SKIP   
           translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
           SKIP   
           SUBSTR(curr-texte, 1, length(curr-texte))   
           VIEW-AS ALERT-BOX ERROR.   
       prog-error = YES.   
       error-nr = - 1.   
       RETURN.   
    END.   
  END.   
   
/* check, IF it is a difference e.g. ^v1-^v2.balance  */   
  ELSE IF SUBSTR(texte, j, 1) = "-" THEN   
  DO:   
    j = j + 1.   
    FOR EACH curr-w1 NO-LOCK BY curr-w1.varname descending:   
      IF NOT var-found THEN   
      DO:   
        IF curr-w1.varname = SUBSTR(texte, j, length(curr-w1.varname)) THEN   
        DO:   
          ratio-flag = 2.   
          var-found = YES.   
          i = j + length(curr-w1.varname) - 1.   
          j = i + 1.   
          FIND FIRST w1-ratio WHERE w1-ratio.nr = curr-w1.nr NO-LOCK.   
        END.   
      END.   
    END.   
    IF NOT var-found THEN   
    DO:   
       hide MESSAGE NO-PAUSE.   
       MESSAGE translateExtended ("Minus-Variable was missing",lvCAREA,"")   
           SKIP   
           translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
           SKIP   
           SUBSTR(curr-texte, 1, length(curr-texte))   
           VIEW-AS ALERT-BOX ERROR.   
       prog-error = YES.   
       error-nr = - 1.   
       RETURN.   
    END.   
  END.   
   
  texte = SUBSTR(texte, j, length(texte)).   
  found = NO.  
  FOR EACH htv-list BY LENGTH(htv-list.fchar) DESCENDING:  
    IF htv-list.fchar = SUBSTR(texte, 1, length(htv-list.fchar)) THEN   
    DO:   
      found = YES.   
      paramNo = htv-list.paramnr.  
      i = j + length(htv-list.fchar).   
      RUN decode-key(texte, INPUT htv-list.paramnr, INPUT-OUTPUT i).   
      IF prog-error THEN RETURN.   
      ELSE LEAVE.  
    END.   
  END.   
  IF NOT found THEN   
  DO:   
       hide MESSAGE NO-PAUSE.   
       MESSAGE translateExtended ("Variable's field was missing",lvCAREA,"")   
           SKIP   
           translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
           SKIP   
           SUBSTR(curr-texte, 1, length(curr-texte))   
           VIEW-AS ALERT-BOX ERROR.   
       prog-error = YES.   
       error-nr = - 1.   
       RETURN.   
  END.   
  ELSE   
  DO:   
    IF NOT check-only THEN RUN print-field(paramNo).   
    i = i + 1.   
  END.   
END.   
*/   
/*
PROCEDURE print-field:   
  DEFINE INPUT PARAMETER paramnr AS INTEGER.   
  DEFINE VARIABLE c AS CHAR FORMAT "x(80)".   
  DEFINE VARIABLE ch AS CHAR.   
  DEFINE buffer curr-w1 FOR w1.   
  DEFINE VARIABLE i AS INTEGER.   
  DEFINE VARIABLE wert AS DECIMAL.   
  DEFINE buffer parent FOR w1.   
   
  DO:   
    FIND FIRST curr-w1 WHERE curr-w1.nr = w1.nr NO-LOCK.   
    DO:   
      detail-nr = 0.   
      FIND FIRST detail-list WHERE detail-list.nr = curr-w1.nr NO-ERROR.   
      IF NOT AVAILABLE detail-list THEN   
      DO:   
        create detail-list.   
        detail-list.nr = curr-w1.nr.   
      END.   
   
      IF paramnr = 93 THEN  /* TODAY */   
      DO:   
        IF ratio-flag GT 0 THEN   
        DO:   
          RUN convert-ratio(curr-w1.tday, w1-ratio.tday, OUTPUT c).   
        END.   
        ELSE RUN convert-balance(curr-w1.tday, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 94 THEN  /* Month TO DATE */   
      DO:   
        IF ratio-flag GT 0 THEN   
        DO:   
          RUN convert-ratio(curr-w1.saldo, w1-ratio.saldo, OUTPUT c).   
        END.   
        ELSE RUN convert-balance(curr-w1.saldo, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 96 THEN   
      DO:   
        IF ratio-flag GT 0   
          THEN RUN convert-ratio(curr-w1.lastmon, w1-ratio.lastmon, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.lastmon, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 95 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio(curr-w1.ytd-saldo, w1-ratio.ytd-saldo, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.ytd-saldo, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 185 THEN  /* LAST YEAR TODAY */   
      DO:   
        IF ratio-flag GT 0 THEN   
        DO:   
          RUN convert-ratio(curr-w1.lytoday, w1-ratio.lytoday, OUTPUT c).   
        END.   
        ELSE RUN convert-balance(curr-w1.lytoday, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 196 THEN   
      DO:   
        IF ratio-flag GT 0   
          THEN RUN convert-ratio(curr-w1.lastyr, w1-ratio.lastyr, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.lastyr, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 815 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio(curr-w1.lytd-saldo, w1-ratio.lytd-saldo, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.lytd-saldo, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 816 THEN   
      DO:   
        IF ratio-flag GT 0   
          THEN RUN convert-ratio(curr-w1.tbudget, w1-ratio.tbudget, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.tbudget, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 817 THEN   
      DO:   
        IF ratio-flag GT 0   
          THEN RUN convert-ratio(curr-w1.budget, w1-ratio.budget, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.budget, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 819 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio(curr-w1.lm-budget, w1-ratio.lm-budget, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.lm-budget, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 679 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio(curr-w1.ly-budget, w1-ratio.ly-budget, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.ly-budget, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 818 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio(curr-w1.ytd-budget, w1-ratio.ytd-budget, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.ytd-budget, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 843 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio(curr-w1.lytd-budget, w1-ratio.lytd-budget, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.lytd-budget, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 820 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio((curr-w1.tday - curr-w1.tbudget),   
            (w1-ratio.tday - w1-ratio.tbudget), OUTPUT c).   
        ELSE RUN convert-diff(curr-w1.tday, curr-w1.tbudget, NO, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 821 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio((curr-w1.saldo - curr-w1.budget),   
            (w1-ratio.saldo - w1-ratio.budget), OUTPUT c).   
        ELSE RUN convert-diff(curr-w1.saldo, curr-w1.budget, NO, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 822 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio((curr-w1.lastmon - curr-w1.lm-budget),   
            (w1-ratio.lastmon - w1-ratio.lm-budget), OUTPUT c).   
        ELSE RUN convert-diff(curr-w1.lastmon, curr-w1.lm-budget, NO, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
      ELSE IF paramnr = 2065 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio((curr-w1.lastyr - curr-w1.ly-budget),   
            (w1-ratio.lastyr - w1-ratio.ly-budget), OUTPUT c).   
          ELSE RUN convert-diff(curr-w1.lastyr, curr-w1.ly-budget, NO, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
      ELSE IF paramnr = 2066 THEN   
      DO:   
        RUN convert-diff(curr-w1.ytd-saldo, curr-w1.ytd-budget, NO, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
      ELSE IF paramnr = 2067 THEN   
      DO:   
        RUN convert-diff(curr-w1.saldo, curr-w1.budget, YES, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
      ELSE IF paramnr = 2068 THEN   
      DO:   
        RUN convert-diff(curr-w1.lastmon, curr-w1.lm-budget, YES, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
      ELSE IF paramnr = 2069 THEN   
      DO:   
        RUN convert-diff(curr-w1.lastyr, curr-w1.ly-budget, NO, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
      ELSE IF paramnr = 2043 THEN   
      DO:   
        RUN convert-diff(curr-w1.ytd-saldo, curr-w1.ytd-budget, YES, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
   
      ELSE IF paramnr = 2044 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio(curr-w1.lytd-saldo, w1-ratio.lytd-saldo, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.lytd-saldo, OUTPUT c).   
        RUN detail-put-string(c).   
        detail-list.field-value[7] = curr-w1.lytd-saldo.   
        detail-list.use-flag[7] = YES.   
      END.   
      ELSE IF paramnr = 2045 THEN   
      DO:   
        IF ratio-flag GT 0 THEN   
          RUN convert-ratio(curr-w1.lytd-budget, w1-ratio.lytd-budget, OUTPUT c).   
        ELSE RUN convert-balance(curr-w1.lytd-budget, OUTPUT c).   
        RUN detail-put-string(c).   
        detail-list.field-value[12] = curr-w1.lytd-budget.   
        detail-list.use-flag[12] = YES.   
      END.   
      ELSE IF paramnr = 2046 THEN   
      DO:   
        RUN convert-diff(curr-w1.lytd-saldo, curr-w1.lytd-budget, NO, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
      ELSE IF paramnr = 2047 THEN   
      DO:   
        RUN convert-diff(curr-w1.lytd-saldo, curr-w1.lytd-budget, YES, OUTPUT c).   
        RUN detail-put-string(c).   
      END.   
    END.   
  END.   
END.   
*/   
/*
PROCEDURE decode-key:   
DEFINE INPUT PARAMETER texte AS CHAR FORMAT "x(132)".   
DEFINE INPUT PARAMETER paramnr AS INTEGER.   
DEFINE INPUT-OUTPUT PARAMETER i AS INTEGER.   
DEFINE VARIABLE out-str AS CHAR.   
DEFINE VARIABLE status-code AS INTEGER INITIAL 0.   
DEFINE VARIABLE n AS INTEGER.   
DEFINE VARIABLE m AS INTEGER.   
   
/*   
status-code = 0   ==> NO-ERROR   
              1       TAB   
              2       SKIP   
              3       left margin ON   
              4       number OF digit   
   
              6       detail-print   
*/   
   
  RUN decode-key1 (paramnr, OUTPUT out-str, OUTPUT status-code).   
   
  IF status-code GE 1 AND status-code LE 4 AND NOT check-only THEN   
  DO:   
    RUN find-parameter(paramnr, texte, status-code, INPUT-OUTPUT i).   
    IF status-code = 1 THEN   
    DO:   
      m = curr-pos + 1.   
      IF curr-pos GT ntab THEN   
      DO:   
        RUN print-buffer.   
        curr-pos = 1.   
        margin-c = "".   
        DO n = 2 TO ntab:   
          margin-c = margin-c + " ".   
        END.   
        RUN put-string(margin-c).   
      END.   
      ELSE   
      DO:   
        margin-c = "".   
        DO n = m TO ntab:   
          margin-c = margin-c + " ".   
        END.   
        RUN put-string(margin-c).   
      END.   
      curr-pos = ntab.   
    END.   
    ELSE IF status-code = 2 THEN   
    DO:   
      DO n = 1 TO nskip:   
        IF NOT view-only THEN PUT STREAM s1 "" SKIP.   
        ELSE efield = efield + chr(10).   
      END.   
      margin-c = "".   
      DO n = 1 TO lmargin:   
        margin-c = margin-c + " ".   
      END.   
      RUN put-string(margin-c).   
      curr-pos = 1.   
    END.   
    ELSE IF status-code = 3  THEN   
    DO:   
      margin-c = "".   
      DO n = 1 TO lmargin:   
        margin-c = margin-c + " ".   
      END.   
      RUN put-string (margin-c).   
    END.   
  END.   
   
  ELSE IF status-code = 6 THEN   
  DO:   
    varname = TRIM(SUBSTR(texte, i + 1, length(texte))).   
    IF varname = "" THEN   
    DO:   
         hide MESSAGE NO-PAUSE.   
         MESSAGE translateExtended ("Variable name not defined",lvCAREA,"")   
             SKIP   
             translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
             SKIP   
             SUBSTR(curr-texte, 1, length(curr-texte))   
             VIEW-AS ALERT-BOX ERROR.   
         prog-error = YES.   
         error-nr = - 1.   
         RETURN.   
    END.   
    i = length(texte) + 1.   
    FIND FIRST parent-w1 WHERE parent-w1.varname = varname NO-LOCK NO-ERROR.   
    IF NOT AVAILABLE parent-w1 THEN   
    DO:   
         hide MESSAGE NO-PAUSE.   
         MESSAGE translateExtended ("Variable name not found : ",lvCAREA,"") + varname   
             SKIP   
             translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
             SKIP   
             SUBSTR(curr-texte, 1, length(curr-texte))   
             VIEW-AS ALERT-BOX ERROR.   
         prog-error = YES.   
         error-nr = - 1.   
         RETURN.   
    END.   
  END.   
END.   
*/
/*
PROCEDURE find-parameter:   
DEFINE INPUT PARAMETER paramnr AS INTEGER.   
DEFINE INPUT PARAMETER curr-texte AS CHAR FORMAT "x(132)".   
DEFINE INPUT PARAMETER status-code AS INTEGER.   
DEFINE INPUT-OUTPUT PARAMETER i AS INTEGER.   
DEFINE VARIABLE j AS INTEGER.   
DEFINE VARIABLE n AS INTEGER.   
DEFINE VARIABLE stopped AS LOGICAL INITIAL NO.   
  FIND FIRST htp-list WHERE htp-list.paramnr = paramnr.   
   
  /* SKIP the blank chars */   
    j = i + 1.   
    DO WHILE NOT stopped:   
       IF SUBSTR(curr-texte, j, 1) NE " "  THEN stopped = YES.   
      ELSE   
      DO:   
         IF j GT length(curr-texte) THEN   
         DO:   
           hide MESSAGE NO-PAUSE.   
           MESSAGE translateExtended ("Incorrect command line; missing variable name",lvCAREA,"")   
             SKIP   
             translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
             SKIP   
             SUBSTR(curr-texte, 1, length(curr-texte))   
             VIEW-AS ALERT-BOX ERROR.   
           prog-error = YES.   
           error-nr = - 1.   
           RETURN.   
         END.   
         ELSE j = j + 1.   
      END.   
    END.   
   
  i = j.   
  j = j + 1.   
  stopped = NO.   
  DO WHILE NOT stopped:   
     IF SUBSTR(curr-texte, j, 1) LT "0"   
        OR SUBSTR(curr-texte, j, 1) GT "9"  OR j GT length(curr-texte)   
        THEN stopped = YES.   
     ELSE j = j + 1.   
  END.   
   
  IF (j - i ) GT 0  THEN   
  DO:   
    n = INTEGER(SUBSTR(curr-texte, i, j - i)).   
    IF status-code = 1 THEN ntab = n.   
    ELSE IF status-code = 2 THEN nskip = n.   
    ELSE IF status-code = 3 THEN lmargin = n.   
    ELSE IF status-code = 4 THEN   
    DO:   
      num-digit = n.   
      IF num-digit GT 12 THEN num-digit = 12.   
      ELSE IF num-digit LT 7 THEN num-digit = 7.   
    END.   
    i = j.   
  END.   
  ELSE   
  DO:   
       hide MESSAGE NO-PAUSE.   
       MESSAGE translateExtended ("Incorrect  line; command expected a number",lvCAREA,"")   
           SKIP   
           translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
           SKIP   
           SUBSTR(curr-texte, 1, length(curr-texte))   
           VIEW-AS ALERT-BOX ERROR.   
       prog-error = YES.   
       error-nr = - 1.   
       RETURN.   
  END.   
END. 
*/  
/*   
PROCEDURE decode-key1:   
DEFINE buffer htp1 FOR htparam.   
DEFINE INPUT PARAMETER paramnr AS INTEGER.   
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "".   
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0.   
DEFINE VARIABLE ch AS CHAR FORMAT "x(80)".   
DEFINE VARIABLE exrate-betrag AS DECIMAL INITIAL 0.   
DEFINE VARIABLE gl AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".   
   
  IF paramnr = 2071                /*  begin OF detail command */     THEN   
  DO:   
    detail-loop = 1.   
    status-code = 6.   
  END.   
  ELSE IF paramnr = 2072       /* END OF detail, now print all variables   */   
     THEN detail-loop = 2.   
   
  ELSE IF paramnr = 2073      /* TAB                        */   
     THEN status-code = 1.   
   
  ELSE IF paramnr = 290      /* today's DATE       */   THEN   
  DO:   
    ch = STRING(today).   
    RUN put-string(ch).   
  END.   
  ELSE IF paramnr = 289      /* To-date       */   THEN   
  DO:   
    ch = STRING(to-date).   
    RUN put-string(ch).   
  END.   
  ELSE IF paramnr = 843      /* Print To-date's week day  */   THEN   
  DO:   
    ch = dayname[weekday(to-date)].   
    RUN put-string(ch).   
  END.   
  ELSE IF paramnr = 679      /* Print To-date's Exchange-Rate  */   THEN   
  DO:   
    exrate-betrag = 0.   
    RUN find-exrate(to-date).   
    IF AVAILABLE exrate THEN exrate-betrag = exrate.betrag.   
    ch = TRIM(STRING(exrate-betrag, ">>>,>>9.99")).   
    RUN put-string(ch).   
  END.   
  ELSE IF paramnr = 995       /* NO DECIMAL */ THEN   
     no-decimal = YES.   
  ELSE IF paramnr = 2075      /* SKIP                       */   
     THEN status-code = 2.   
  ELSE IF paramnr = 2076      /* Left Margin ON  */   THEN   
  DO:   
    f-lmargin = YES.   
    status-code = 3.   
  END.   
  ELSE IF paramnr = 994       /* number OF digit */   
    THEN status-code = 4.   
  ELSE IF paramnr = 2077      /* Left Margin OFF  */   THEN f-lmargin = NO.   
  ELSE IF (paramnr GE 2078) AND (paramnr LE 2089)   
    AND AVAILABLE PRINTER      /* printcod */    THEN   
  DO:   
    /*MTFIND FIRST printcod WHERE printcod.emu = printer.emu   
      AND printcod.code = htparam.fchar NO-LOCK NO-ERROR.   
    IF AVAILABLE printcod THEN RUN put-string(TRIM(printcod.contcod)). */  
  END.   
END.   
*/
/*
PROCEDURE put-string:   
DEFINE INPUT PARAMETER STR AS CHAR.   
DEFINE VARIABLE len AS INTEGER.   
DEFINE VARIABLE i AS INTEGER.   
  IF check-only THEN RETURN.   
  len = length(STR).   
  FIND FIRST detail-list WHERE detail-list.nr = 0.   
  detail-list.str-buffer = detail-list.str-buffer + STR.   
  IF len-flag THEN curr-pos = curr-pos + len.   
  len-flag = NO.   
END.   
   
PROCEDURE detail-put-string:   
DEFINE INPUT PARAMETER STR AS CHAR.   
DEFINE VARIABLE len AS INTEGER.   
DEFINE VARIABLE i AS INTEGER.   
  IF check-only THEN RETURN.   
  FIND FIRST detail-list WHERE detail-list.nr = detail-nr NO-ERROR.   
  IF NOT AVAILABLE detail-list THEN   
  DO:   
    create detail-list.   
    detail-list.nr = detail-nr.   
  END.   
  len = length(STR).   
  detail-list.str-buffer = detail-list.str-buffer + STR.   
  IF len-flag OR detail-nr = 0 THEN curr-pos = curr-pos + len.   
  len-flag = NO.   
END.  
*/ 
/*   
PROCEDURE print-buffer:   
DEFINE VARIABLE i AS INTEGER.   
DEFINE VARIABLE n AS INTEGER INITIAL 0.   
DEFINE VARIABLE c AS CHAR FORMAT "x(1)".   
  n = length(detail-list.str-buffer).   
  DO i = 1 TO n:   
    c = SUBSTR(detail-list.str-buffer, i, 1).   
    PUT STREAM s1 c FORMAT "x(1)".   
  END.   
  PUT STREAM s1 "" SKIP.   
  detail-list.str-buffer = "".   
END.   
*/   
PROCEDURE create-w1:   
  DEFINE OUTPUT PARAMETER ind AS INTEGER.   
  DEFINE VARIABLE w1-nr AS INTEGER.   
  create w1.   
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
    create w2.   
    w2.nr1 = ind.   
    w2.nr2 = nr2.   
  END.   
  w2.val-sign = val-sign.   
END.   
/*   
PROCEDURE fill-w11:   
DEFINE INPUT PARAMETER recid1-w1 AS INTEGER.   
DEFINE INPUT PARAMETER recid2-w1 AS INTEGER.   
DEFINE buffer curr1-w1 FOR w1.   
DEFINE buffer curr2-w1 FOR w1.   
DEFINE buffer curr-child FOR w1.   
DEFINE buffer curr-w2 FOR w2.   
DEFINE VARIABLE texte AS CHAR.   
DEFINE VARIABLE n AS INTEGER.   
  FIND FIRST curr1-w1 WHERE RECID(curr1-w1) = recid1-w1.   
  FIND FIRST curr2-w1 WHERE RECID(curr2-w1) = recid2-w1.   
  FIND FIRST w11 WHERE w11.nr = curr1-w1.nr NO-ERROR.   
  IF NOT AVAILABLE w11 THEN   
  DO:   
    create w11.   
    w11.nr = curr1-w1.nr.   
  END.   
  IF curr2-w1.grpflag EQ 0 THEN   
  DO:   
  END.   
  ELSE   
  DO:   
    FOR EACH curr-w2 WHERE curr-w2.nr1 = curr2-w1.nr NO-LOCK:   
      FIND FIRST curr-child WHERE curr-child.nr = curr-w2.nr2 NO-LOCK.   
      RUN fill-w11(recid1-w1, RECID(curr-child)).   
    END.   
  END.   
END.   
*/   
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
  texte = TRIM(SUBSTR(texte, curr-column, length(texte) - curr-column + 1)).   
  stopped = NO.   
  j = 1.   
  DO WHILE NOT stopped:   
    IF  j EQ length(texte) OR SUBSTR(texte, j + 1, 1) = " " THEN stopped = YES.   
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
      + CHR(10) + 
      SUBSTR(curr-texte, 1, length(curr-texte)).       
    prog-error = YES.   
    error-nr = - 1.   
    RETURN.   
  END.   
END.   
/*   
PROCEDURE get-texlen:   
DEFINE INPUT PARAMETER texte AS CHAR.   
DEFINE VARIABLE correct AS LOGICAL.   
  texte = TRIM(texte).   
  RUN check-integer(texte, OUTPUT correct).   
  IF correct THEN   
  DO:   
     IF texte NE "" THEN textlen = INTEGER(texte).   
     curr-cmd = 0.   
  END.   
END.   
   
PROCEDURE get-digitlen:   
DEFINE INPUT PARAMETER texte AS CHAR.   
DEFINE VARIABLE correct AS LOGICAL.   
  texte = TRIM(texte).   
  RUN check-integer(texte, OUTPUT correct).   
  IF correct THEN   
  DO:   
     IF texte NE "" THEN num-digit = INTEGER(texte).   
     IF num-digit GT 12 THEN num-digit = 12.   
     ELSE IF num-digit LT 7 THEN num-digit = 7.   
     curr-cmd = 0.   
  END.   
END.   
*/   
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
    msg-str = translateExtended ("Program expected a number : ",lvCAREA,"") + texte   
      + CHR(10) +   
      translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
      + CHR(10) +   
      SUBSTR(curr-texte, 1, length(curr-texte)).      
    prog-error = YES.   
    error-nr = - 1.   
    RETURN.   
  END.   
END.   
/*   
PROCEDURE get-title:   
DEFINE INPUT PARAMETER texte AS CHAR.   
  report-title = texte.   
  curr-cmd = 0.   
END.   
   
PROCEDURE abbrev-var:   
  DEFINE INPUT PARAMETER texte AS CHAR.   
  DEFINE VARIABLE subtext AS CHAR.   
  DEFINE VARIABLE ind AS INTEGER.   
  DEFINE VARIABLE correct AS LOGICAL.   
  RUN get-subtext (texte, INPUT-OUTPUT subtext).   
  IF SUBSTR(subtext, 1, 1) NE keyvar THEN   
  DO:   
      hide MESSAGE NO-PAUSE.   
      MESSAGE translateExtended ("Program expected a variable name",lvCAREA,"")   
        SKIP   
        translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
        SKIP   
        SUBSTR(curr-texte, 1, length(curr-texte))   
        VIEW-AS ALERT-BOX ERROR.   
      prog-error = YES.   
      error-nr = - 1.   
      RETURN.   
  END.   
  varname = subtext.   
  bezeich = TRIM(SUBSTR(texte, curr-column, length(texte) - curr-column + 1)).   
  IF bezeich = "" THEN   
  DO:   
    hide MESSAGE NO-PAUSE.   
    MESSAGE translateExtended ("Program expected a string",lvCAREA,"")   
           SKIP   
           translateExtended ("at line number : ",lvCAREA,"") STRING(curr-row)   
           SKIP   
           SUBSTR(curr-texte, 1, length(curr-texte))   
           VIEW-AS ALERT-BOX ERROR.   
    prog-error = YES.   
    error-nr = - 1.   
    RETURN.   
  END.   
  ELSE   
  DO:   
    grpflag = 9.   
    RUN create-w1(OUTPUT ind).   
    curr-column = length(curr-texte) + 1.   
    curr-cmd = 0.   
  END.   
END.   
   
PROCEDURE rename-keyvar:   
  DEFINE INPUT PARAMETER texte AS CHAR.   
  DEFINE VARIABLE subtext AS CHAR.   
  DEFINE VARIABLE ind AS INTEGER.   
  DEFINE VARIABLE correct AS LOGICAL.   
  RUN get-subtext (texte, INPUT-OUTPUT subtext).   
  IF SUBSTR(subtext, 1, 1) NE "." THEN   
  DO:   
      hide MESSAGE NO-PAUSE.   
      MESSAGE translateExtended ("Program expected a new key variable name '.xxx'",lvCAREA,"")   
        SKIP   
        translateExtended ("at line number",lvCAREA,"") + " " + STRING(curr-row)   
        SKIP   
        SUBSTR(curr-texte, 1, length(curr-texte))   
        VIEW-AS ALERT-BOX ERROR.   
      prog-error = YES.   
      error-nr = - 1.   
      RETURN.   
  END.   
  varname = subtext.   
  subtext = TRIM(SUBSTR(texte, curr-column, length(texte) - curr-column + 1)).   
  FIND FIRST htv-list WHERE htv-list.fchar = subtext NO-ERROR.   
  IF NOT AVAILABLE htv-list THEN   
  DO:   
    hide MESSAGE NO-PAUSE.   
    MESSAGE translateExtended ("No such key variable found : ",lvCAREA,"") + subtext   
           SKIP   
           translateExtended ("at line number :",lvCAREA,"") + " " + STRING(curr-row)   
           SKIP   
           SUBSTR(curr-texte, 1, length(curr-texte))   
           VIEW-AS ALERT-BOX ERROR.   
    prog-error = YES.   
    error-nr = - 1.   
    RETURN.   
  END.   
  ELSE   
  DO:   
    htv-list.fchar = varname.   
    curr-cmd = 0.   
  END.   
END.   
*/   
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
      SUBSTR(curr-texte, 1, length(curr-texte)).   
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
      SUBSTR(curr-texte, 1, length(curr-texte)).   
    prog-error = YES.   
    error-nr = - 1.   
    RETURN.   
  END.   
  ELSE   
  DO:   
    varname = subtext.   
    bezeich = TRIM(SUBSTR(texte, curr-column, length(texte) - curr-column + 1)).   
    IF bezeich = "" THEN   
    DO:         
      msg-str = translateExtended ("Program expected a description",lvCAREA,"")   
        + CHR(10) +   
        translateExtended ("at line number : ",lvCAREA,"") + STRING(curr-row)   
        + CHR(10) +   
        SUBSTR(curr-texte, 1, length(curr-texte)).   
      prog-error = YES.   
      error-nr = - 1.   
      RETURN.   
    END.   
    ELSE   
    DO:   
      grpflag = 2.   
      RUN create-w1(OUTPUT grp-nr).   
      curr-column = length(texte) + 1.   
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
    texte = SUBSTR(texte, 2, length(texte)).   
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
        SUBSTR(curr-texte, 1, length(curr-texte)).   
      prog-error = YES.   
      error-nr = - 1.   
      RETURN.   
    END.   
    ELSE RUN create-w2(grp-nr, w1.nr, 2, val-sign).   
  END.   
END.   
/*   
PROCEDURE convert-balance:   
DEFINE INPUT PARAMETER balance AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".   
DEFINE OUTPUT PARAMETER s AS CHAR FORMAT "x(20)" INITIAL "".   
DEFINE VARIABLE ch AS CHAR.   
DEFINE VARIABLE i AS INTEGER.   
DEFINE VARIABLE j AS INTEGER.   
DEFINE VARIABLE jj AS INTEGER.   
  IF no-decimal OR integer-flag THEN s = STRING(balance, "->>>>>>>>>>>>>>9").   
  ELSE s = STRING(balance, "->>>>>>>>>>>9.99").   
  s = TRIM(s).   
  ch = "".   
  DO i = 1 TO length(s):   
    IF SUBSTR(s, i, 1) NE "," THEN ch = ch + SUBSTR(s, i, 1).   
    ELSE ch = ch + ".".   
  END.   
  s = ch.   
END.   
   
PROCEDURE convert-diff:   
DEFINE INPUT PARAMETER v1 AS DECIMAL.   
DEFINE INPUT PARAMETER v2 AS DECIMAL.   
DEFINE INPUT PARAMETER in-ratio AS LOGICAL.   
DEFINE OUTPUT PARAMETER s AS CHAR FORMAT "x(20)" INITIAL "".   
DEFINE VARIABLE balance AS DECIMAL.   
DEFINE VARIABLE b AS DECIMAL.   
DEFINE VARIABLE rs AS CHAR FORMAT "x(7)".   
DEFINE VARIABLE ch AS CHAR.   
DEFINE VARIABLE i AS INTEGER.   
DEFINE VARIABLE j AS INTEGER.   
  IF NOT in-ratio THEN   
  DO:   
    balance = v1 - v2.   
    IF no-decimal THEN s  = STRING(balance, "->>>>>>>>>>>>>>9 ").   
    ELSE s  = STRING(balance, "->>>>>>>>>>>9.99 ").   
  END.   
  ELSE   
  DO:   
    IF v2 = 0 THEN rs = "0.00".   
    ELSE   
    DO:   
      balance = (v1 - v2) / v2 * 100.   
      IF balance GE 0 THEN b = balance.   
      ELSE b = - balance.   
      IF b LE 999 THEN rs = STRING(balance, "->>9.99").   
      ELSE IF b LE 9999 THEN rs = STRING(balance, "->>>9.9").   
      ELSE rs = STRING(balance, "->>>>>>>>>9").   
    END.   
    s = rs.   
  END.   
  s = TRIM(s).   
  ch = "".   
  DO i = 1 TO length(s):   
    IF SUBSTR(s, i, 1) NE "," THEN ch = ch + SUBSTR(s, i, 1).   
    ELSE ch = ch + ".".   
  END.   
  s = ch.   
END.   
   
PROCEDURE convert-ratio:   
DEFINE INPUT PARAMETER v1 AS DECIMAL.   
DEFINE INPUT PARAMETER v2 AS DECIMAL.   
DEFINE OUTPUT PARAMETER s AS CHAR FORMAT "x(20)" INITIAL "".   
DEFINE VARIABLE balance AS DECIMAL.   
DEFINE VARIABLE b AS DECIMAL.   
DEFINE VARIABLE rs AS CHAR FORMAT "x(7)".   
DEFINE VARIABLE ch AS CHAR.   
DEFINE VARIABLE i AS INTEGER.   
DEFINE VARIABLE j AS INTEGER.   
   
  IF ratio-flag = 1 THEN   
  DO:   
    IF v2 = 0 THEN rs = "100.00".   
    ELSE   
    DO:   
      balance = v1 / v2 * 100.   
      IF balance GE 0 THEN b = balance.   
      ELSE b = - balance.   
      IF b LE 999 THEN rs = STRING(balance, "->>9.99").   
      ELSE IF b LE 9999 THEN rs = STRING(balance, "->>>9.9").   
      ELSE rs = TRIM(STRING(balance, "->>>>>>>>>9")).   
    END.   
    s = rs.   
    s = TRIM(s).   
    ch = "".   
    DO i = 1 TO length(s):   
      IF SUBSTR(s, i, 1) NE "," THEN ch = ch + SUBSTR(s, i, 1).   
      ELSE ch = ch + ".".   
    END.   
    s = ch.   
  END.   
  ELSE IF ratio-flag = 2 THEN   
  DO:   
    balance = v1 - v2.   
    RUN convert-balance(balance, OUTPUT s).   
  END.   
  ELSE IF ratio-flag = 3 THEN   
  DO:   
    IF v2 NE 0 THEN s = TRIM(STRING(v1 / v2, "->>>>>>>>>>>9.9999")).   
    ELSE s = "0".   
  END.   
END.   
*/
/*   
PROCEDURE read-exfile:   
DEFINE VARIABLE key-found AS LOGICAL.   
DEFINE VARIABLE i AS INTEGER.   
  curr-row = 0.   
  REPEAT:   
    curr-texte = "".   
    IMPORT STREAM s2 unformatted curr-texte.   
    RUN search-key(curr-texte, OUTPUT key-found).   
    IF NOT key-found THEN   
    DO:   
      DO i = 1 TO length(curr-texte):   
        PUT STREAM s1 SUBSTR(curr-texte,i,1) FORMAT "x(1)".   
      END.   
      PUT STREAM s1 "" SKIP.   
    END.   
    ELSE   
    DO:   
      curr-pos = 1.   
      curr-column = 1.   
      curr-row = curr-row + 1.   
      RUN build-text-line (curr-texte).   
      IF prog-error THEN RETURN.   
      RUN print-buffer.   
    END.   
  END.   
END.   
*/
/*
PROCEDURE search-key:   
DEFINE INPUT PARAMETER ct AS CHAR.   
DEFINE OUTPUT PARAMETER found AS LOGICAL INITIAL NO.   
DEFINE VARIABLE i AS INTEGER.   
  DO i = 1 TO LENGTH(ct):   
    IF SUBSTR(ct,i,3) = ('"' + '$' + '"') THEN i = i + 2.   
    ELSE IF SUBSTR(ct,i,1) = keycmd OR SUBSTR(ct,i,1) = keyvar THEN   
    DO:   
      found = YES.   
      RETURN.   
    END.   
  END.   
END.   
*/   
/*
PROCEDURE excel-slk:   
DEFINE VARIABLE prog-path AS CHAR FORMAT "x(32)".   
DEFINE VARIABLE prog-name AS CHAR FORMAT "x(32)".   
DEFINE VARIABLE s AS CHAR FORMAT "x(80)".   
DEFINE VARIABLE not-defined AS LOGICAL.   
DEFINE VARIABLE f-char AS CHAR.  
  RUN htpchar.p(406, OUTPUT f-char).  
  not-defined = (f-char = "").   
  IF f-char NE "" THEN prog-path = f-char.  
  ELSE prog-path = "\""program files""\""microsoft office""\office\".   
  
  RUN htpchar.p(407, OUTPUT f-char).  
  IF f-char NE "" THEN   
    prog-name = f-char.  
  ELSE prog-name = "excel.exe".   
/*   
  IF not-defined THEN   
  DO:   
    FILE-INFO:FILE-NAME = prog-path + prog-name.   
    IF FILE-INFO:FILE-TYPE = ? THEN   
    DO:   
      prog-path = "\""program files""\""microsoft office""\office10\".   
      prog-name = "excel.exe".   
    END.   
  END.   
*/   
  OUTPUT TO ".\runexcel.bat".   
  s = SEARCH(prog-name).   
  IF s EQ ? THEN s = prog-path + prog-name.   
  s = s + " " + outfile.   
  PUT s FORMAT "x(80)".   
   
  IF NOT view-only THEN OUTPUT CLOSE.   
  dos silent ".\runexcel.bat".   
  dos silent "del .\runexcel.bat".   
END.   
   
PROCEDURE find-exrate:   
DEFINE INPUT PARAMETER curr-date AS DATE NO-UNDO.   
  /*MTIF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr   
    AND exrate.datum = curr-date NO-LOCK NO-ERROR.   
  ELSE FIND FIRST exrate WHERE exrate.datum = curr-date NO-LOCK NO-ERROR. */  
END.     
*/
