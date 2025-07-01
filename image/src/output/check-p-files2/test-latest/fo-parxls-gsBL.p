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

DEFINE TEMP-TABLE shift-list
  FIELD shift AS INT
  FIELD ftime AS INT
  FIELD ttime AS INT
.

DEFINE TEMP-TABLE w2 
  FIELD val-sign    AS INTEGER INITIAL 1 
  FIELD nr1         AS INTEGER 
  FIELD nr2         AS INTEGER. 

DEFINE TEMP-TABLE tmp-room
    FIELD gastnr    AS INTEGER
    FIELD zinr      LIKE zimmer.zinr
    FIELD flag      AS INTEGER
    INDEX gstnr gastnr DESC zinr. 

DEFINE TEMP-TABLE t-list
    FIELD dept      AS INT
    FIELD datum     AS DATE
    FIELD shift     AS INT
    FIELD pax-food  AS INT
    FIELD pax-bev   AS INT.

DEFINE TEMP-TABLE t-rechnr 
    FIELD datum       AS DATE
    FIELD dept        AS INT
    FIELD rechnr      AS INT
    FIELD shift       AS INT
    FIELD found-food  AS LOGICAL INIT NO
    FIELD found-bev   AS LOGICAL INIT NO.

DEFINE TEMP-TABLE temp-rechnr
    FIELD datum       AS DATE
    FIELD dept        AS INT
    FIELD rechnr      AS INT
    FIELD shift       AS INT
    FIELD belegung    AS INTEGER
    FIELD artnrfront  AS INTEGER
    FIELD compli-flag AS LOGICAL
    FIELD tischnr     AS INTEGER
    FIELD betrag      AS DECIMAL
    FIELD artnr       AS INTEGER
    FIELD artart      AS INTEGER
    FIELD resnr       AS INTEGER
    FIELD reslinnr    AS INTEGER
    FIELD f-pax       AS INTEGER
    FIELD b-pax       AS INTEGER
    FIELD f-qty       AS INTEGER
    FIELD b-qty       AS INTEGER.

DEFINE TEMP-TABLE s-list 
    FIELD datum       AS DATE
    FIELD reihenfolge AS INTEGER INITIAL 1 /* 1 = food, 2 = beverage */ 
    FIELD lager-nr    AS INTEGER 
    FIELD fibukonto   LIKE gl-acct.fibukonto 
    FIELD bezeich     LIKE gl-acct.bezeich 
    FIELD flag        AS INTEGER INITIAL 2  /* 0 cost, 5 = expense */ 
    FIELD betrag      AS DECIMAL INITIAL 0 
    FIELD t-betrag    AS DECIMAL INITIAL 0
    FIELD betrag1     AS DECIMAL INITIAL 0
    FIELD t-betrag1   AS DECIMAL INITIAL 0
. 

DEFINE TEMP-TABLE fbstat-dept 
    FIELD done AS LOGICAL
    FIELD dept AS INTEGER
.

DEFINE TEMP-TABLE stream-list
    FIELD crow AS INTEGER
    FIELD ccol AS INTEGER
    FIELD cval AS CHARACTER
.

DEFINE INPUT PARAMETER pvILanguage   AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER ytd-flag      AS LOGICAL.
DEFINE INPUT PARAMETER jan1          AS DATE.
DEFINE INPUT PARAMETER Ljan1         AS DATE.
DEFINE INPUT PARAMETER Lfrom-date    AS DATE.
DEFINE INPUT PARAMETER Lto-date      AS DATE.
DEFINE INPUT PARAMETER Pfrom-date    AS DATE.
DEFINE INPUT PARAMETER Pto-date      AS DATE.
DEFINE INPUT PARAMETER from-date     AS DATE.
DEFINE INPUT PARAMETER to-date       AS DATE.
DEFINE INPUT PARAMETER start-date    AS DATE.
DEFINE INPUT PARAMETER lytd-flag     AS LOGICAL.
DEFINE INPUT PARAMETER lmtd-flag     AS LOGICAL.
DEFINE INPUT PARAMETER pmtd-flag     AS LOGICAL.
DEFINE INPUT PARAMETER lytoday-flag  AS LOGICAL.
DEFINE INPUT PARAMETER lytoday       AS DATE.
DEFINE INPUT PARAMETER foreign-flag  AS LOGICAL.
DEFINE INPUT PARAMETER budget-flag   AS LOGICAL.
DEFINE INPUT PARAMETER foreign-nr    AS INTEGER.
DEFINE INPUT PARAMETER price-decimal AS INTEGER.
DEFINE INPUT PARAMETER briefnr       AS INTEGER.
DEFINE INPUT PARAMETER link          AS CHARACTER.
DEFINE INPUT PARAMETER budget-all    AS LOGICAL.
DEFINE INPUT PARAMETER TABLE FOR w1.
DEFINE INPUT PARAMETER TABLE FOR w2.

DEFINE OUTPUT PARAMETER msg-str      AS CHARACTER.
DEFINE OUTPUT PARAMETER error-nr     AS INT.

DEFINE VARIABLE Lfr-date    AS DATE.

DEFINE VARIABLE exrate-betrag   AS DECIMAL INITIAL 0.
DEFINE VARIABLE frate           AS DECIMAL INITIAL 1.
DEFINE VARIABLE prog-error      AS LOGICAL INITIAL NO.
DEFINE VARIABLE ch              AS CHARACTER.
DEFINE BUFFER   segmbuff FOR segmentstat.


DEFINE VARIABLE month-str AS CHAR EXTENT 12 
  INITIAL ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE", 
  "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fo-parxls".
RUN fill-value.

RUN find-exrate(to-date).
exrate-betrag = 0.
IF AVAILABLE exrate THEN exrate-betrag = exrate.betrag.
ch = TRIM(STRING(exrate-betrag, ">>>,>>9.99")).

Lfr-date = from-date - 1.

PROCEDURE fill-value: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE BUFFER curr-child FOR w1. 
DEFINE VARIABLE val-sign AS INTEGER. 
DEFINE BUFFER ww1 FOR w1. 
DEFINE BUFFER ww2 FOR w1. 

    /* rd, oct 04, calculate num of records */
DEFINE VARIABLE num_row AS INTEGER. 
DEFINE VARIABLE z       AS INTEGER. 
DEFINE VARIABLE n_bar   AS INTEGER. 
DEFINE VARIABLE n_pct   AS INTEGER INIT 50.
DEFINE VARIABLE done-pax-shift AS LOGICAL INIT NO.
DEFINE VARIABLE done-fbstat AS LOGICAL INIT NO.
DEFINE VARIABLE done-los AS LOGICAL INIT NO.
DEFINE VARIABLE done-adddayuse  AS LOGICAL INIT NO.

  EMPTY TEMP-TABLE fbstat-dept.

  FOR EACH ww1 WHERE ww1.grpflag = 0: 
      num_row = num_row + 1.
  END.
/*--------------------------------------*/
  /*LN*/
  FOR EACH ww1 WHERE ww1.grpflag = 0: 
    
    FIND FIRST ww2 WHERE ww2.varname = ww1.varname 
      AND RECID(ww1) NE RECID(ww2) NO-LOCK NO-ERROR. 
    IF AVAILABLE ww2 THEN 
    DO: 
        msg-str = msg-str + CHR(2)
                + translateExtended ("Duplicate name found : ",lvCAREA,"") + ww2.varname.
        error-nr = -1. 
        RETURN. 
    END. 
  END. 
 
  /* rd */  z = 0.
  FOR EACH ww1 WHERE ww1.grpflag = 0 BY ww1.main-code DESC: 
      /* rd */
      ASSIGN    z       = z + 1
                n_bar   = INTEGER(z * n_pct / num_row).
      
    /*-------------*/
    FIND FIRST ww2 WHERE ww2.varname = ww1.varname 
      AND RECID(ww1) NE RECID(ww2) NO-LOCK NO-ERROR. 
    IF AVAILABLE ww2 THEN 
    DO: 
        msg-str = msg-str + CHR(2)
                + translateExtended ("Duplicate name found : ",lvCAREA,"") + ww2.varname.
        error-nr = -1.
        RETURN.
    END. 
    IF ww1.main-code = 288 THEN RUN fill-totroom(RECID(ww1)). 
    ELSE IF ww1.main-code = 805 THEN RUN fill-rmavail(RECID(ww1)). 

    ELSE IF ww1.main-code = 122  THEN RUN fill-rmstat(RECID(ww1), "ooo").     
    ELSE IF ww1.main-code = 752  THEN RUN fill-rmstat(RECID(ww1), "oos"). 
    ELSE IF ww1.main-code = 129  THEN RUN fill-rmstat(RECID(ww1), "vacant"). 
    ELSE IF ww1.main-code = 1019 THEN RUN fill-rmstat(RECID(ww1), "dayuse"). 

   /*FD Comment
    ELSE IF ww1.main-code = 192 THEN RUN fill-cover(RECID(ww1)). 
    ELSE IF ww1.main-code = 197 THEN RUN fill-cover(RECID(ww1)). 
    ELSE IF ww1.main-code = 552 THEN RUN fill-cover(RECID(ww1)). */
    

    /*FD Sept 22, 2022 => Ticket AB666C, new procedure for cover*/
    /*ELSE IF ww1.main-code = 192 THEN RUN fill-new-cover(RECID(ww1)). 
    ELSE IF ww1.main-code = 197 THEN RUN fill-new-cover(RECID(ww1)). 
    ELSE IF ww1.main-code = 552 THEN RUN fill-new-cover(RECID(ww1)).*/

    /*MG fix variable $F-COVER & $B-COVER 2048E4*/
    ELSE IF ww1.main-code = 192 THEN RUN fill-pax-cover-shift1(RECID(ww1)). 
    ELSE IF ww1.main-code = 197 THEN RUN fill-pax-cover-shift1(RECID(ww1)).

    /*gerald fix variable $COVER 0CA886*/
    ELSE IF ww1.main-code = 552 THEN RUN fill-pax-cover-shift1(RECID(ww1)). 

    ELSE IF ww1.main-code = 1921 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1922 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1923 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1924 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1971 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1972 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1973 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1974 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1991 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1992 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1993 THEN RUN fill-cover-shift(RECID(ww1)). 
    ELSE IF ww1.main-code = 1994 THEN RUN fill-cover-shift(RECID(ww1)).

    /*ITA 201218*/
    /*ELSE IF ww1.main-code = 2001 THEN RUN fill-cover-shift1(RECID(ww1)). 
    ELSE IF ww1.main-code = 2002 THEN RUN fill-cover-shift1(RECID(ww1)). 
    ELSE IF ww1.main-code = 2003 THEN RUN fill-cover-shift1(RECID(ww1)). 
    ELSE IF ww1.main-code = 2004 THEN RUN fill-cover-shift1(RECID(ww1)).*/

    /*Gerald pindah procedure main-code 2001 - 2004*/
    ELSE IF ww1.main-code GE 2001 AND ww1.main-code LE 2004 THEN RUN fill-pax-cover-shift1(RECID(ww1)).

    ELSE IF ww1.main-code = 2005 THEN RUN fill-cover-shift1(RECID(ww1)). 
    ELSE IF ww1.main-code = 2006 THEN RUN fill-cover-shift1(RECID(ww1)). 
    ELSE IF ww1.main-code = 2007 THEN RUN fill-cover-shift1(RECID(ww1)). 
    ELSE IF ww1.main-code = 2008 THEN RUN fill-cover-shift1(RECID(ww1)).
    /*end ita*/

    /*ITA 260220*/
    ELSE IF ww1.main-code = 2009 THEN RUN fill-cover-shift2(RECID(ww1)). 
    ELSE IF ww1.main-code = 2010 THEN RUN fill-cover-shift2(RECID(ww1)). 
    ELSE IF ww1.main-code = 2011 THEN RUN fill-cover-shift2(RECID(ww1)). 
    ELSE IF ww1.main-code = 2012 THEN RUN fill-cover-shift2(RECID(ww1)).

    ELSE IF ww1.main-code = 2013 THEN RUN fill-cover-shift2(RECID(ww1)). 
    ELSE IF ww1.main-code = 2014 THEN RUN fill-cover-shift2(RECID(ww1)). 
    ELSE IF ww1.main-code = 2015 THEN RUN fill-cover-shift2(RECID(ww1)). 
    ELSE IF ww1.main-code = 2016 THEN RUN fill-cover-shift2(RECID(ww1)).
    /*end*/

    /*ELSE IF (ww1.main-code = 1995 OR ww1.main-code = 1996) AND NOT done-pax-shift THEN
        RUN fill-pax-cover-shift(OUTPUT done-pax-shift).*/

    ELSE IF (ww1.main-code = 1995 OR ww1.main-code = 1996) THEN RUN fill-pax-cover-shift1(RECID(ww1)).

    ELSE IF (ww1.main-code = 1997 OR ww1.main-code = 1998 OR ww1.main-code = 1999) THEN
        RUN fill-fbstat (RECID(ww1)).

    /*Gerald Pax food-bev by shift 4079F5*/
    ELSE IF ww1.main-code GE 2020 AND ww1.main-code LE 2051 THEN RUN fill-pax-cover-shift1(RECID(ww1)).
    /*MG QTY-FOOD QTY-BEV E78F9A*/
    ELSE IF ww1.main-code GE 2052 AND ww1.main-code LE 2055 THEN RUN fill-pax-cover-shift1(RECID(ww1)).
    /*MG Daily FB Flash : DirectPurchase, TransferSideStore, Cost, Compliment 61236D*/
    ELSE IF ww1.main-code GE 2056 AND ww1.main-code LE 2059 THEN RUN fill-fb-flash(RECID(ww1)).

    ELSE IF ww1.main-code = 9000 THEN RUN fill-los(OUTPUT done-los).
    
    /*ELSE IF ww1.main-code = 9106 THEN RUN fill-wig(RECID(ww1)). */

    /*MG new procedure for walkin guest 8B2F9F*/
    ELSE IF ww1.main-code = 9106 THEN RUN fill-new-wig(RECID(ww1)).  
 
    ELSE IF ww1.main-code = 85
      THEN RUN fill-arrdep(RECID(ww1), "arrival-RSV", 85, 86, 0). 
    ELSE IF ww1.main-code = 86 
      THEN RUN fill-arrdep(RECID(ww1), "arrival-RSV", 85, 86, 0). 

    ELSE IF ww1.main-code = 106
      THEN RUN fill-arrdep(RECID(ww1), "arrival-WIG", 106, 107, 0). 
    ELSE IF ww1.main-code = 107 
      THEN RUN fill-arrdep(RECID(ww1), "arrival-WIG", 106, 107, 0). 
    
    ELSE IF ww1.main-code = 187 
      THEN RUN fill-arrdep(RECID(ww1), "arrival", 187, 188, 0). 
    ELSE IF ww1.main-code = 188 
      THEN RUN fill-arrdep(RECID(ww1), "arrival", 187, 188, 0).
    ELSE IF ww1.main-code = 9188 
      THEN RUN fill-arrdep(RECID(ww1), "arrival", 0, 0, 9188).
 
    ELSE IF ww1.main-code = 189 
      THEN RUN fill-arrdep(RECID(ww1), "departure", 189, 190, 0). 
    ELSE IF ww1.main-code = 190 
      THEN RUN fill-arrdep(RECID(ww1), "departure", 189, 190, 0).
    ELSE IF ww1.main-code = 9190 
      THEN RUN fill-arrdep(RECID(ww1), "departure", 0, 0, 9190).

    ELSE IF ww1.main-code = 191 
      THEN RUN fill-arrdep(RECID(ww1), "VIP", 0, 191, 0). 
 
    ELSE IF ww1.main-code = 193 
      THEN RUN fill-arrdep(RECID(ww1), "NewRes", 193, 0, 0). 
 
    ELSE IF ww1.main-code = 194 
      THEN RUN fill-arrdep(RECID(ww1), "CancRes", 194, 0, 0). 

    ELSE IF ww1.main-code = 7194 
      THEN RUN fill-canc-room-night(RECID(ww1)). 

    ELSE IF ww1.main-code = 7195 
      THEN RUN fill-canc-cidate(RECID(ww1)). 
 
    ELSE IF ww1.main-code = 195 
      THEN RUN fill-avrgstay(RECID(ww1), "Avrg-Stay", 195). 
 
    ELSE IF ww1.main-code = 211 
      THEN RUN fill-arrdep(RECID(ww1), "ArrTmrw", 211, 231, 0). 
    ELSE IF ww1.main-code = 231 
      THEN RUN fill-arrdep(RECID(ww1), "ArrTmrw", 211, 231, 0). 
 
    ELSE IF ww1.main-code = 742 
      THEN RUN fill-arrdep(RECID(ww1), "Early-CO", 742, 0, 0). 
 
    ELSE IF ww1.main-code = 750 
      THEN RUN fill-arrdep(RECID(ww1), "DepTmrw", 750, 751, 0). 
    ELSE IF ww1.main-code = 751 
      THEN RUN fill-arrdep(RECID(ww1), "DepTmrw", 750, 751, 0). 
 
    ELSE IF ww1.main-code = 969 
      THEN RUN fill-arrdep(RECID(ww1), "No-Show", 969, 0, 0). 
 
    ELSE IF ww1.main-code = 806 THEN 
    DO: 
      /*RUN fill-rmocc (RECID(ww1)). */
      RUN fill-new-rmocc(RECID(ww1)). /*MG Disamakan dengan room production */
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 182 THEN 
    DO: 
      RUN fill-gledger(RECID(ww1)). 
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 183 THEN 
    DO: 
      /*RUN fill-comprooms(RECID(ww1)). */
      RUN fill-comproomsnew(RECID(ww1)).
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 807 THEN 
    DO: 
      RUN fill-rmocc%(RECID(ww1)). 
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 808 THEN 
    DO: 
      RUN fill-docc%(RECID(ww1)). 
      IF error-nr NE 0 THEN RETURN. 
    END. 
    ELSE IF ww1.main-code = 1008 THEN RUN fill-fbcost(RECID(ww1)). 
    ELSE IF ww1.main-code = 9985 OR ww1.main-code = 9986 THEN
        RUN fill-sgfb(RECID(ww1),ww1.main-code). 
    ELSE IF ww1.main-code = 1084 THEN RUN fill-quantity(RECID(ww1)). 
    ELSE IF ww1.main-code = 809 THEN RUN fill-revenue(RECID(ww1)).
    ELSE IF ww1.main-code = 810 THEN RUN fill-persocc(RECID(ww1)). 
    ELSE IF ww1.main-code = 811 THEN RUN fill-avrgrate(RECID(ww1)). 
    ELSE IF ww1.main-code = 812 THEN RUN fill-avrgLrate(RECID(ww1)). 
    ELSE IF ww1.main-code = 842 THEN RUN fill-avrglodg(RECID(ww1)). 
    ELSE IF ww1.main-code = 46 THEN RUN fill-avrgLlodge(RECID(ww1)). 
    ELSE IF ww1.main-code = 92 OR ww1.main-code = 813 
      OR ww1.main-code = 814 OR ww1.main-code = 756 
      OR ww1.main-code = 757 OR ww1.main-code = 758
      THEN RUN fill-segment(RECID(ww1), ww1.main-code). 
    ELSE IF ww1.main-code = 8092 OR ww1.main-code = 8813 
      OR ww1.main-code = 8814 THEN RUN fill-nation(RECID(ww1), ww1.main-code).
    ELSE IF ww1.main-code = 9981 OR ww1.main-code = 9982 
      OR ww1.main-code = 9983 OR ww1.main-code = 9984 THEN 
        RUN fill-competitor (RECID(ww1), ww1.main-code). 
    ELSE IF ww1.main-code = 179 THEN RUN fill-rmcatstat(RECID(ww1), ww1.main-code). 
    ELSE IF ww1.main-code = 180 OR ww1.main-code = 181 
      OR ww1.main-code = 800 THEN RUN fill-zinrstat(RECID(ww1), ww1.main-code). 
  
    ELSE IF ww1.main-code = 9092 OR ww1.main-code = 9813 
      OR ww1.main-code = 9814 THEN RUN fill-source(RECID(ww1), ww1.main-code). 
    ELSE IF ww1.main-code = 9008 AND NOT done-adddayuse THEN RUN fill-adddayuse(OUTPUT done-adddayuse).

  END. 
  
  FOR EACH w1 WHERE w1.grpflag GE 1 AND w1.grpflag NE 9 BY w1.nr: 
    FOR EACH w2 WHERE w2.nr1 = w1.nr NO-LOCK: 
      FIND FIRST curr-child WHERE curr-child.nr = w2.nr2 NO-LOCK. 
      RUN fill-value1(RECID(w1), RECID(curr-child), w2.val-sign). 
    END. 
  END.
END. 

/***************************************************************/
PROCEDURE fill-adddayuse: 
DEFINE OUTPUT PARAMETER done AS LOGICAL.

DEFINE VARIABLE datum1 AS DATE.         
DEFINE BUFFER wdu FOR w1.
        
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 

    FOR EACH res-line WHERE active-flag = 2 AND res-line.ankunft GE datum1
        AND res-line.ankunft LE to-date
        AND res-line.abreise = res-line.ankunft AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 AND res-line.resstatus NE 99 NO-LOCK, 
        FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK
        BY res-line.zinr BY res-line.resnr BY res-line.reslinnr:                      

        FIND FIRST bill-line WHERE bill-line.departement = 0
            AND bill-line.artnr = arrangement.argt-artikelnr
            AND bill-line.bill-datum = res-line.ankunft
            AND bill-line.massnr = res-line.resnr
            AND bill-line.billin-nr = res-line.reslinnr
            USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bill-line THEN
        DO:
            IF res-line.ankunft = to-date THEN
                wdu.tday = wdu.tday + res-line.zimmeranz. 
            IF res-line.ankunft GE from-date THEN
                wdu.saldo = wdu.saldo + res-line.zimmeranz. 
            wdu.ytd-saldo = wdu.ytd-saldo + res-line.zimmeranz. 
        END.                                                    
    END.
  
    done = YES.
END. 


PROCEDURE fill-totroom: 
DEFINE INPUT PARAMETER rec-w1   AS INTEGER. 

DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE datum2          AS DATE. 
DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE anz             AS INTEGER. 
DEFINE VARIABLE anz0            AS INTEGER.
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  anz0 = 0. 
  FOR EACH zimmer NO-LOCK: 
    anz0 = anz0 + 1. 
  END. 

  IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
    OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
    OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
    w1.lm-today = 0.
  ELSE 
  DO:
    IF MONTH(to-date) EQ 1 THEN
      curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
    ELSE
      curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
    FIND FIRST zinrstat WHERE zinrstat.datum = curr-date
      AND zinrstat.zinr = "tot-rm" NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN
      w1.lm-today = zinrstat.zimmeranz.
    ELSE
      w1.lm-today = anz0.
  END.
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
 
  DO datum = datum1 TO to-date: 
    FIND FIRST zinrstat WHERE zinrstat.datum = datum
      AND zinrstat.zinr = "tot-rm" NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN anz = zinrstat.zimmeranz.
    ELSE anz = anz0.

    d-flag = AVAILABLE zinrstat AND (MONTH(zinrstat.datum) = MONTH(to-date))
      AND (YEAR(zinrstat.datum) = YEAR(to-date)).
    IF AVAILABLE zinrstat  THEN
      IF d-flag THEN w1.mon-saldo[DAY(zinrstat.datum)] = w1.mon-saldo[DAY(zinrstat.datum)] + anz.
    
    IF datum = to-date - 1 THEN w1.yesterday = w1.yesterday + anz.
    
    IF datum = to-date THEN w1.tday = w1.tday + anz. 
    IF start-date NE ? THEN
    DO:
      IF (datum LT from-date) AND (datum GE start-date) 
        THEN w1.ytd-saldo = w1.ytd-saldo + anz. 
      ELSE 
      DO: 
        IF (datum GE start-date) THEN w1.saldo = w1.saldo + anz. 
        IF ytd-flag AND (datum GE start-date) THEN 
          w1.ytd-saldo = w1.ytd-saldo + anz. 
      END.
    END.
    ELSE
    DO:
      IF datum LE Lfr-date THEN w1.lm-ytd = w1.lm-ytd + anz.
      IF (datum LT from-date) THEN w1.ytd-saldo = w1.ytd-saldo + anz. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + anz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + anz. 
      END.
    END.
  END. 

  IF (lytd-flag OR lmtd-flag) THEN 
  DO: 
    IF lytd-flag THEN datum2 = Ljan1. 
    ELSE datum2 = Lfrom-date. 
    DO datum = datum2 TO Lto-date: 
      FIND FIRST zinrstat WHERE zinrstat.datum = datum
        AND zinrstat.zinr = "tot-rm" NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN anz = zinrstat.zimmeranz.
        ELSE anz = anz0.
      dlmtd-flag = AVAILABLE zinrstat AND (MONTH(zinrstat.datum) = MONTH(to-date)) 
        AND (YEAR(zinrstat.datum) = YEAR(to-date) - 1).
      IF dlmtd-flag THEN w1.mon-lmtd[DAY(zinrstat.datum)] 
        = w1.mon-lmtd[DAY(zinrstat.datum)] + anz.
      IF start-date NE ? THEN
      DO:
        IF (datum LT Lfrom-date) AND (datum GE start-date) 
          THEN w1.lytd-saldo = w1.lytd-saldo + anz. 
        ELSE IF (datum GE start-date) THEN 
        DO: 
          w1.lastyr = w1.lastyr + anz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + anz. 
        END.
      END. 
      ELSE
      DO:
        IF (datum LT Lfrom-date) THEN w1.lytd-saldo = w1.lytd-saldo + anz. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + anz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + anz. 
        END.
      END.
    END. 
  END. 
  
  IF pmtd-flag THEN /* previous MTD */ 
  DO datum = Pfrom-date TO Pto-date: 
    FIND FIRST zinrstat WHERE zinrstat.datum = datum
        AND zinrstat.zinr = "tot-rm" NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN anz = zinrstat.zimmeranz.
    ELSE anz = anz0.
    IF start-date NE ? THEN
    DO:
      IF (datum GE start-date) THEN w1.lastmon = w1.lastmon + anz. 
    END.
    ELSE w1.lastmon = w1.lastmon + anz. 
  END. 

  IF lytoday-flag THEN w1.lytoday = anz. /* SY: figure might be wrong */

  w1.done = YES. 
END. 

PROCEDURE fill-rmavail: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1    AS DATE. 
DEFINE VARIABLE datum2    AS DATE. 
DEFINE VARIABLE curr-date AS DATE. 

    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 

    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 

    IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
      OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
      OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
      w1.lm-today = 0.
    ELSE
    DO:
      IF MONTH(to-date) EQ 1 THEN
        curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
      ELSE
        curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
      FIND FIRST zkstat WHERE zkstat.datum EQ curr-date 
        AND zkstat.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR.
      IF AVAILABLE zkstat THEN
        w1.lm-today = w1.lm-today + zkstat.anz100.
    END.

    FOR EACH zkstat WHERE zkstat.datum GE datum1 AND zkstat.datum LE to-date NO-LOCK: 
      IF zkstat.datum = to-date - 1 THEN w1.yesterday = w1.yesterday + zkstat.anz100. 
      IF zkstat.datum = to-date THEN w1.tday = w1.tday + zkstat.anz100. 
      IF zkstat.datum LT from-date THEN 
        w1.ytd-saldo = w1.ytd-saldo + zkstat.anz100. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zkstat.anz100. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + zkstat.anz100. 
      END. 
      IF MONTH(zkstat.datum) = MONTH(to-date) AND YEAR(zkstat.datum) = YEAR(to-date) THEN
        w1.mon-saldo[DAY(zkstat.datum)] 
          = w1.mon-saldo[DAY(zkstat.datum)] + zkstat.anz100.
    END. 

    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum2 = Ljan1. 
      ELSE datum2 = Lfrom-date. 
      FOR EACH zkstat WHERE zkstat.datum GE datum2 AND zkstat.datum LE Lto-date NO-LOCK: 
        IF zkstat.datum LT Lfrom-date THEN 
        w1.lytd-saldo = w1.lytd-saldo + zkstat.anz100. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + zkstat.anz100. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + zkstat.anz100. 
        END. 
      END. 
    END. 
    
    IF lytoday-flag THEN 
    FOR EACH zkstat WHERE zkstat.datum = lytoday NO-LOCK: 
      w1.lytoday = w1.lytoday + zkstat.anz100. 
    END. 
    
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zkstat WHERE zkstat.datum GE Pfrom-date 
      AND zkstat.datum LE Pto-date NO-LOCK: 
      w1.lastmon = w1.lastmon + zkstat.anz100. 
    END. 

    w1.done = YES. 
END. 


PROCEDURE fill-ooo: 
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF INPUT PARAMETER key-word AS CHAR. 
DEF VARIABLE datum1 AS DATE. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      IF zinrstat.datum = to-date THEN w1.tday = w1.tday + zinrstat.zimmeranz. 
      IF zinrstat.datum LT from-date THEN 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = key-word NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.zimmeranz. 
    END. 
    IF lytoday-flag THEN
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday 
        AND zinrstat.zinr = key-word NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN w1.lytoday = zinrstat.zimmeranz. 
    END.   
  END. 
  w1.done = YES. 
END. 

PROCEDURE fill-vacant: 
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF INPUT PARAMETER key-word AS CHAR. 
DEF VARIABLE datum1 AS DATE. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      IF zinrstat.datum = to-date THEN w1.tday = w1.tday + zinrstat.zimmeranz. 
      IF zinrstat.datum LT from-date THEN 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = key-word NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.zimmeranz. 
    END. 
    IF lytoday-flag THEN 
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday 
        AND zinrstat.zinr = key-word NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN w1.lytoday = zinrstat.zimmeranz. 
    END. 
  END. 
  w1.done = YES. 
END. 

PROCEDURE fill-cover: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
DEFINE BUFFER hbuff FOR h-umsatz.
DEF BUFFER w11 FOR w1. 
DEF BUFFER w12 FOR w1. 
DEF BUFFER w13 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  RELEASE w11. 
  RELEASE w12. 
  RELEASE w13. 
  /*FIND FIRST w11 WHERE w11.main-code = 552 AND w11.dept = w1.dept NO-ERROR.*/
  FIND FIRST w12 WHERE w12.main-code = 192 AND w12.dept = w1.dept NO-ERROR. 
  FIND FIRST w13 WHERE w13.main-code = 197 AND w13.dept = w1.dept NO-ERROR. 
 
  IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
    OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
    OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
  DO:
    IF AVAILABLE w11 THEN w11.lm-today = 0. 
    IF AVAILABLE w12 THEN w12.lm-today = 0.
    IF AVAILABLE w13 THEN w13.lm-today = 0. 
  END.
  ELSE
  DO:
    IF MONTH(to-date) EQ 1 THEN
      curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
    ELSE
      curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
    FIND FIRST h-umsatz WHERE h-umsatz.datum  EQ curr-date 
      AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept 
      AND h-umsatz.betriebsnr = w1.dept NO-LOCK NO-ERROR.
    IF AVAILABLE h-umsatz THEN
    DO:
      IF AVAILABLE w11 THEN w11.lm-today = h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN w12.lm-today = h-umsatz.betrag. 
      IF AVAILABLE w13 THEN w13.lm-today = h-umsatz.nettobetrag. 
    END.
  END.


  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 AND h-umsatz.datum LE to-date 
    AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept 
    AND h-umsatz.betriebsnr = w1.dept NO-LOCK: 

    d-flag = (MONTH(h-umsatz.datum) = MONTH(to-date)) AND (YEAR(h-umsatz.datum) = YEAR(to-date)).
    IF d-flag THEN 
    DO:
      IF AVAILABLE w11 THEN
        w11.mon-saldo[DAY(h-umsatz.datum)] = h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN
        w12.mon-saldo[DAY(h-umsatz.datum)] = h-umsatz.betrag. 
      IF AVAILABLE w13 THEN 
        w13.mon-saldo[DAY(h-umsatz.datum)] = h-umsatz.nettobetrag. 
    END.
    
    IF h-umsatz.datum = to-date - 1 THEN
    DO: 
      IF AVAILABLE w11 THEN w11.yesterday = h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN w12.yesterday = h-umsatz.betrag. 
      IF AVAILABLE w13 THEN w13.yesterday = h-umsatz.nettobetrag. 
    END.
    
    IF h-umsatz.datum = to-date THEN
    DO: 
      IF AVAILABLE w11 THEN w11.tday = h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN w12.tday = h-umsatz.betrag. 
      IF AVAILABLE w13 THEN w13.tday = h-umsatz.nettobetrag. 
    END.

    IF h-umsatz.datum LE Lfr-date THEN   /*FT 060313*/
    DO: 
      IF AVAILABLE w11 THEN w11.lm-ytd = w11.lm-ytd + h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN w12.lm-ytd = w12.lm-ytd + h-umsatz.betrag. 
      IF AVAILABLE w13 THEN w13.lm-ytd = w13.lm-ytd + h-umsatz.nettobetrag. 
    END. 
 
    IF h-umsatz.datum LT from-date THEN 
    DO: 
      IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo + h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN w12.ytd-saldo = w12.ytd-saldo + h-umsatz.betrag. 
      IF AVAILABLE w13 THEN w13.ytd-saldo = w13.ytd-saldo + h-umsatz.nettobetrag. 
    END. 
    ELSE 
    DO: 
      IF AVAILABLE w11 THEN w11.saldo = w11.saldo + h-umsatz.anzahl. 
      IF ytd-flag AND AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo + h-umsatz.anzahl. 
      IF AVAILABLE w12 THEN w12.saldo = w12.saldo + h-umsatz.betrag. 
      IF ytd-flag AND AVAILABLE w12 THEN w12.ytd-saldo = w12.ytd-saldo + h-umsatz.betrag. 
      IF AVAILABLE w13 THEN w13.saldo = w13.saldo + h-umsatz.nettobetrag. 
      IF ytd-flag AND AVAILABLE w13 THEN w13.ytd-saldo = w13.ytd-saldo + h-umsatz.nettobetrag. 
    END. 
  END. 
  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum1 = Ljan1. 
    ELSE datum1 = Lfrom-date. 
    FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 
      AND h-umsatz.datum LE Lto-date 
      AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept 
      AND h-umsatz.betriebsnr = w1.dept NO-LOCK: 
      IF h-umsatz.datum LT Lfrom-date THEN 
      DO: 
        IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo + h-umsatz.anzahl. 
        IF AVAILABLE w12 THEN w12.lytd-saldo = w12.lytd-saldo + h-umsatz.betrag. 
        IF AVAILABLE w13 THEN w13.lytd-saldo = w13.lytd-saldo + h-umsatz.nettobetrag. 
      END. 
      ELSE 
      DO: 
        dlmtd-flag = (MONTH(h-umsatz.datum) = MONTH(to-date)) 
          AND (YEAR(h-umsatz.datum) = YEAR(to-date) - 1).
        IF dlmtd-flag THEN
        DO:
          IF AVAILABLE w11 THEN 
            w11.mon-lmtd[DAY(h-umsatz.datum)] = w11.mon-lmtd[DAY(h-umsatz.datum)] + h-umsatz.anzahl.
          IF AVAILABLE w12 THEN 
            w12.mon-lmtd[DAY(h-umsatz.datum)] = w12.mon-lmtd[DAY(h-umsatz.datum)] + h-umsatz.betrag.
          IF AVAILABLE w13 THEN 
            w13.mon-lmtd[DAY(h-umsatz.datum)] = w13.mon-lmtd[DAY(h-umsatz.datum)] + h-umsatz.nettobetrag.
        END.
        IF AVAILABLE w11 THEN w11.lastyr = w11.lastyr + h-umsatz.anzahl. /* LAST year MTD */ 
        IF lytd-flag AND AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo + h-umsatz.anzahl. 
        IF AVAILABLE w12 THEN w12.lastyr = w12.lastyr + h-umsatz.betrag. 
        IF lytd-flag AND AVAILABLE w12 THEN w12.lytd-saldo = w12.lytd-saldo + h-umsatz.betrag. 
        IF AVAILABLE w13 THEN w13.lastyr = w13.lastyr + h-umsatz.nettobetrag. 
        IF lytd-flag AND AVAILABLE w13 THEN w13.lytd-saldo = w13.lytd-saldo + h-umsatz.nettobetrag. 
      END. 
    END. 
  END. 
  IF pmtd-flag THEN /* previous MTD */ 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE Pfrom-date 
    AND h-umsatz.datum LE Pto-date 
    AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept 
    AND h-umsatz.betriebsnr = w1.dept NO-LOCK: 
    IF AVAILABLE w11 THEN w11.lastmon = w11.lastmon + h-umsatz.anzahl. 
    IF AVAILABLE w12 THEN w12.lastmon = w12.lastmon + h-umsatz.betrag. 
    IF AVAILABLE w13 THEN w13.lastmon = w13.lastmon + h-umsatz.nettobetrag. 
  END. 
  
  IF lytoday-flag THEN  
  FOR EACH h-umsatz WHERE h-umsatz.datum = lytoday
    AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept 
    AND h-umsatz.betriebsnr = w1.dept NO-LOCK: 
    IF AVAILABLE w11 THEN w11.lytoday = w11.lytoday + h-umsatz.anzahl. 
    IF AVAILABLE w12 THEN w12.lytoday = w12.lytoday + h-umsatz.betrag. 
    IF AVAILABLE w13 THEN w13.lytoday = w13.lytoday + h-umsatz.nettobetrag. 
  END. 

  IF AVAILABLE w11 THEN w11.done = YES. 
  IF AVAILABLE w12 THEN w12.done = YES. 
  IF AVAILABLE w13 THEN w13.done = YES. 
END. 

PROCEDURE fill-canc-room-night:
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF VAR datum1 AS DATE.
DEF BUFFER resbuff FOR res-line.

FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 

IF ytd-flag THEN datum1 = jan1. 
ELSE datum1 = from-date. 
IF AVAILABLE w1 THEN
DO: 
 FOR EACH resbuff WHERE resbuff.resstatus = 9 AND resbuff.active-flag = 2
   AND resbuff.betrieb-gastpay NE 3
   AND resbuff.CANCELLED GE datum1
   AND resbuff.CANCELLED LE to-date
   AND resbuff.l-zuordnung[3] = 0:
   IF resbuff.CANCELLED = to-date THEN
     w1.tday = w1.tday + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
   IF resbuff.CANCELLED LT from-date THEN 
     w1.ytd-saldo = w1.ytd-saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
   ELSE
   DO:
     w1.saldo = w1.saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
     IF ytd-flag THEN 
       w1.ytd-saldo = w1.ytd-saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
   END.
 END.
 IF lytd-flag OR lmtd-flag THEN 
 DO: 
   IF lytd-flag THEN datum1 = Ljan1. 
   ELSE datum1 = Lfrom-date. 
   FOR EACH resbuff WHERE resbuff.resstatus = 9 AND resbuff.active-flag = 2
   AND resbuff.betrieb-gastpay NE 3
   AND resbuff.CANCELLED GE datum1
   AND resbuff.CANCELLED LE Lto-date
   AND resbuff.l-zuordnung[3] = 0:
     IF resbuff.CANCELLED LT Lfrom-date THEN 
       w1.lytd-saldo = w1.ytd-saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
     ELSE
     DO:
       w1.lastyr = w1.lastyr + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
       IF lytd-flag THEN 
         w1.lytd-saldo = w1.lytd-saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
     END.
   END.
 END.
END.

END.

PROCEDURE fill-canc-cidate:
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF VAR datum1 AS DATE.
DEF BUFFER resbuff FOR res-line.

FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 

IF ytd-flag THEN datum1 = jan1. 
ELSE datum1 = from-date. 
IF AVAILABLE w1 THEN
DO: 
 FOR EACH resbuff WHERE resbuff.resstatus = 9 AND resbuff.active-flag = 2
   AND resbuff.betrieb-gastpay NE 3
   AND resbuff.CANCELLED GE datum1
   AND resbuff.CANCELLED LE to-date
   AND resbuff.CANCELLED = resbuff.ankunft
   AND resbuff.l-zuordnung[3] = 0:
   IF resbuff.ankunft = to-date THEN
     w1.tday = w1.tday + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
   IF resbuff.CANCELLED LT from-date THEN 
     w1.ytd-saldo = w1.ytd-saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
   ELSE
   DO:
     w1.saldo = w1.saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
     IF ytd-flag THEN 
       w1.ytd-saldo = w1.ytd-saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
   END.
 END.
 IF lytd-flag OR lmtd-flag THEN 
 DO: 
   IF lytd-flag THEN datum1 = Ljan1. 
   ELSE datum1 = Lfrom-date. 
   FOR EACH resbuff WHERE resbuff.resstatus = 9 AND resbuff.active-flag = 2
   AND resbuff.betrieb-gastpay NE 3
   AND resbuff.CANCELLED GE datum1
   AND resbuff.CANCELLED LE Lto-date
   AND resbuff.CANCELLED = resbuff.ankunft
   AND resbuff.l-zuordnung[3] = 0:
     IF resbuff.ankunft LT Lfrom-date THEN 
       w1.lytd-saldo = w1.ytd-saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
     ELSE
     DO:
       w1.lastyr = w1.lastyr + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
       IF lytd-flag THEN 
         w1.lytd-saldo = w1.lytd-saldo + (resbuff.abreise - resbuff.ankunft) * resbuff.zimmeranz.
     END.
   END.
 END.
END.
END.

PROCEDURE fill-arrdep: 
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF INPUT PARAMETER key-word AS CHAR. 
DEF INPUT PARAMETER number1 AS INTEGER. 
DEF INPUT PARAMETER number2 AS INTEGER. 
DEF INPUT PARAMETER number3 AS INTEGER. 
DEF VAR datum1    AS DATE. 
DEF VAR curr-date AS DATE. 
DEF VAR d-flag    AS LOGICAL.
DEF BUFFER w11 FOR w1. 
DEF BUFFER w12 FOR w1. 
DEF BUFFER w13 FOR w1.
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  RELEASE w11. 
  RELEASE w12. 
  RELEASE w13.
  IF number1 NE 0 THEN 
    FIND FIRST w11 WHERE w11.main-code = number1 AND NOT w11.done NO-ERROR. 
  IF number2 NE 0 THEN 
    FIND FIRST w12 WHERE w12.main-code = number2 AND NOT w12.done NO-ERROR. 
  IF number3 NE 0 THEN 
    FIND FIRST w13 WHERE w13.main-code = number3 AND NOT w13.done NO-ERROR. 

  IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
    OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
    OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
  DO:
    IF AVAILABLE w11 THEN w11.lm-today = 0.
    IF AVAILABLE w12 THEN w12.lm-today = 0.
  END.
  ELSE
  DO:
    IF MONTH(to-date) EQ 1 THEN
      curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
    ELSE
      curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
    FIND FIRST zinrstat WHERE zinrstat.datum EQ curr-date
      AND zinrstat.zinr = key-word NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN
    DO:
      IF AVAILABLE w11 THEN w11.lm-today = w11.lm-today + zinrstat.zimmeranz. 
      IF AVAILABLE w12 THEN w12.lm-today = w12.lm-today + zinrstat.personen. 
      IF AVAILABLE w13 THEN w13.lm-today = w13.lm-today + zinrstat.betriebsnr. 
    END.
  END.

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = key-word NO-LOCK:

      d-flag = (MONTH(zinrstat.datum) = MONTH(to-date))
          AND (YEAR(zinrstat.datum) = YEAR(to-date)).

      /*FT*/
      IF zinrstat.datum = to-date - 1 THEN 
      DO: 
          IF AVAILABLE w11 THEN w11.yesterday = w11.yesterday + zinrstat.zimmeranz. 
          IF AVAILABLE w12 THEN w12.yesterday = w12.yesterday + zinrstat.personen.
          IF AVAILABLE w13 THEN w13.yesterday = w13.yesterday + zinrstat.betriebsnr.
      END.
      /*FT*/
      IF zinrstat.datum = to-date THEN 
      DO: 
          IF AVAILABLE w11 THEN w11.tday = w11.tday + zinrstat.zimmeranz. 
          IF AVAILABLE w12 THEN w12.tday = w12.tday + zinrstat.personen. 
          IF AVAILABLE w13 THEN w13.tday = w13.tday + zinrstat.betriebsnr.
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        IF AVAILABLE w11 THEN 
            w11.ytd-saldo = w11.ytd-saldo + zinrstat.zimmeranz. 
        IF AVAILABLE w12 THEN 
            w12.ytd-saldo = w12.ytd-saldo + zinrstat.personen. 
        IF AVAILABLE w13 THEN 
            w13.ytd-saldo = w13.ytd-saldo + zinrstat.betriebsnr. 
      END. 
      ELSE 
      DO: 
        IF AVAILABLE w11 THEN w11.saldo = w11.saldo + zinrstat.zimmeranz. 
        IF ytd-flag AND AVAILABLE w11 
            THEN w11.ytd-saldo = w11.ytd-saldo + zinrstat.zimmeranz. 
        IF AVAILABLE w12 THEN w12.saldo = w12.saldo + zinrstat.personen. 
        IF ytd-flag AND AVAILABLE w12 
            THEN w12.ytd-saldo = w12.ytd-saldo + zinrstat.personen. 
        IF AVAILABLE w13 THEN w13.saldo = w13.saldo + zinrstat.betriebsnr. 
        IF ytd-flag AND AVAILABLE w13 
            THEN w13.ytd-saldo = w13.ytd-saldo + zinrstat.betriebsnr. 
      END. 

      IF AVAILABLE w11 THEN
      DO:
        /*MG 6B2C3D*/
        IF d-flag THEN 
        DO:  
          w11.mon-saldo[DAY(zinrstat.datum)] = w11.mon-saldo[DAY(zinrstat.datum)] + zinrstat.zimmeranz.
        END.
      END.
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = key-word NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          IF AVAILABLE w11 THEN 
              w11.lytd-saldo = w11.lytd-saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w12 THEN 
              w12.lytd-saldo = w12.lytd-saldo + zinrstat.personen. 
          IF AVAILABLE w13 THEN 
              w13.lytd-saldo = w13.lytd-saldo + zinrstat.betriebsnr. 
        END. 
        ELSE 
        DO: 
          /* LAST year MTD */ 
          IF AVAILABLE w11 THEN 
              w11.lastyr = w11.lastyr + zinrstat.zimmeranz. 
          IF lytd-flag AND AVAILABLE w11 
              THEN w11.lytd-saldo = w11.lytd-saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w12 THEN 
              w12.lastyr = w12.lastyr + zinrstat.personen. 
          IF lytd-flag AND AVAILABLE w12 
              THEN w12.lytd-saldo = w12.lytd-saldo + zinrstat.personen. 
          IF AVAILABLE w13 THEN 
              w13.lastyr = w13.lastyr + zinrstat.betriebsnr.
          IF lytd-flag AND AVAILABLE w13 
              THEN w13.lytd-saldo = w13.lytd-saldo + zinrstat.betriebsnr. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      IF AVAILABLE w11 THEN 
          w11.lastmon = w11.lastmon + zinrstat.zimmeranz. 
      IF AVAILABLE w12 THEN 
          w12.lastmon = w12.lastmon + zinrstat.personen. 
      IF AVAILABLE w13 THEN 
          w13.lastmon = w13.lastmon + zinrstat.betriebsnr. 
    END. 
    IF lytoday-flag THEN  
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday
        AND zinrstat.zinr = key-word NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN
      DO:
        IF AVAILABLE w11 THEN w11.lytoday = zinrstat.zimmeranz. 
        IF AVAILABLE w12 THEN w12.lytoday = zinrstat.personen. 
        IF AVAILABLE w13 THEN w13.lytoday = zinrstat.betriebsnr. 
      END.
    END.
  END. 
  IF AVAILABLE w11 THEN w11.done = YES. 
  IF AVAILABLE w12 THEN w12.done = YES. 
  IF AVAILABLE w13 THEN w13.done = YES. 
END. 


PROCEDURE fill-avrgstay: 
DEF INPUT PARAMETER rec-w1 AS INTEGER. 
DEF INPUT PARAMETER key-word AS CHAR. 
DEF INPUT PARAMETER number1 AS INTEGER. 
DEF VAR datum1 AS DATE. 
DEF BUFFER w11 FOR w1. 
DEF BUFFER tbuff FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF number1 NE 0 THEN FIND FIRST w11 WHERE w11.main-code = number1 
    AND NOT w11.done NO-ERROR. 
  IF NOT AVAILABLE w11 THEN RETURN. 
 
  CREATE tbuff. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date AND zinrstat.zinr = key-word NO-LOCK: 
 
      IF zinrstat.datum = to-date THEN 
        w11.tday = w11.tday + zinrstat.personen / zinrstat.zimmeranz. 
 
      IF (zinrstat.datum LT from-date) THEN 
      DO: 
        w11.ytd-saldo = w11.ytd-saldo + zinrstat.personen. 
        tbuff.ytd-saldo = tbuff.ytd-saldo + zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w11.saldo = w11.saldo + zinrstat.personen. 
        tbuff.saldo = tbuff.saldo + zinrstat.zimmeranz. 
        IF ytd-flag THEN 
        DO: 
          w11.ytd-saldo = w11.ytd-saldo + zinrstat.personen. 
          tbuff.ytd-saldo = tbuff.ytd-saldo + zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date AND zinrstat.zinr = key-word NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w11.lytd-saldo = w11.lytd-saldo + zinrstat.personen. 
          tbuff.lytd-saldo = tbuff.lytd-saldo + zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w11.lastyr = w11.lastyr + zinrstat.personen. /* LAST year MTD */ 
          tbuff.lastyr = tbuff.lastyr + zinrstat.zimmeranz. 
          IF lytd-flag THEN 
          DO: 
            w11.lytd-saldo = w11.lytd-saldo + zinrstat.personen. 
            tbuff.lytd-saldo = tbuff.lytd-saldo + zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date AND zinrstat.zinr = key-word NO-LOCK: 
      w11.lastmon = w11.lastmon + zinrstat.personen. 
      tbuff.lastmon = tbuff.lastmon + zinrstat.zimmeranz. 
    END. 
    IF lytoday-flag THEN 
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday
        AND zinrstat.zinr = key-word NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN
      ASSIGN
        w11.lytoday   = zinrstat.personen 
        tbuff.lytoday = zinrstat.zimmeranz
      . 
    END.
  END. 
 
  IF tbuff.saldo NE 0 THEN w11.saldo = w11.saldo / tbuff.saldo. 
  IF tbuff.ytd-saldo NE 0 THEN w11.ytd-saldo = w11.ytd-saldo / tbuff.ytd-saldo. 
  IF tbuff.lytd-saldo NE 0 THEN w11.lytd-saldo = w11.lytd-saldo / tbuff.lytd-saldo. 
  IF tbuff.lastyr NE 0 THEN w11.lastyr = w11.lastyr / tbuff.lastyr. 
  IF tbuff.lastmon NE 0 THEN w11.lastmon = w11.lastmon / tbuff.lastmon. 
  IF tbuff.lytoday NE 0 THEN w11.lytoday = w11.lytoday / tbuff.lytoday. 
 
  w11.done = YES. 
  DELETE tbuff. 
END. 


PROCEDURE fill-rmocc: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 

DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE datum2          AS DATE. 
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dbudget-flag    AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
DEFINE VARIABLE frate1          AS DECIMAL NO-UNDO.

DEFINE BUFFER w1a FOR w1. 
/*DEFINE BUFFER w11 FOR w1. 
DEFINE BUFFER w12 FOR w1. 
DEFINE BUFFER w13 FOR w1. */
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1.            /* Room Occ     */
  IF w1.done THEN RETURN. 
 
  FIND FIRST w1a WHERE w1a.main-code = 810 NO-ERROR. /* #pay guest   */
  IF AVAILABLE w1a AND w1a.done THEN release w1a. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  
  FOR EACH segment NO-LOCK: 
    /*FIND FIRST w11 WHERE w11.main-code = 92          /* Room Rev */
      AND w11.artnr = segment.segmentcode NO-ERROR. 
    IF AVAILABLE w11 AND w11.done THEN release w11. 
    FIND FIRST w12 WHERE w12.main-code = 813         /* Room Occ */
      AND w12.artnr = segment.segmentcode NO-ERROR. 
    IF AVAILABLE w12 AND w12.done THEN release w12. 
    FIND FIRST w13 WHERE w13.main-code = 814         /* Pax      */
      AND w13.artnr = segment.segmentcode NO-ERROR. 
    IF AVAILABLE w13 AND w13.done THEN release w13. */
 
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      
      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 

      d-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
          AND (YEAR(segmentstat.datum) = YEAR(to-date)).
      dbudget-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
        AND (YEAR(segmentstat.datum) = YEAR(to-date)).
      
      IF segmentstat.datum = to-date - 1 THEN
      DO:
        IF AVAILABLE w1a THEN 
        DO: 
          ASSIGN
            w1a.yesterday = w1a.yesterday + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        END. 
      END.
      
      IF segmentstat.datum = to-date THEN 
      DO:         
        ASSIGN
          w1.tday = w1.tday + segmentstat.zimmeranz
          w1.tbudget = w1.tbudget + segmentstat.budzimmeranz.         
        IF AVAILABLE w1a THEN 
        DO: 
          ASSIGN
            w1a.tday = w1a.tday + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1a.tbudget = w1a.tbudget + segmentstat.budpersanz. 
        END. 
        /*IF AVAILABLE w11 THEN 
        DO: 
          ASSIGN
            w11.tday = w11.tday + segmentstat.logis / frate
            w11.tbudget = w11.tbudget + segmentstat.budlogis. 
        END. 
        IF AVAILABLE w12 THEN 
        DO: 
          ASSIGN
            w12.tday = w12.tday + segmentstat.zimmeranz
            w12.tbudget = w12.tbudget + segmentstat.budzimmeranz. 
        END. 
        IF AVAILABLE w13 THEN 
        DO: 
          ASSIGN
            w13.tday = w13.tday + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
            w13.tbudget = w13.tbudget + segmentstat.budpersanz. 
        END. */
      END. 
 
      IF segmentstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + segmentstat.zimmeranz. 
        w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
        IF AVAILABLE w1a THEN 
        DO: 
          w1a.ytd-saldo = w1a.ytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1a.ytd-budget = w1a.ytd-budget + segmentstat.budpersanz. 
        END. 
        /*IF AVAILABLE w11 THEN 
        DO: 
          w11.ytd-saldo = w11.ytd-saldo + segmentstat.logis / frate. 
          w11.ytd-budget = w11.ytd-budget + segmentstat.budlogis. 
        END. 
        IF AVAILABLE w12 THEN 
        DO: 
          w12.ytd-saldo = w12.ytd-saldo + segmentstat.zimmeranz. 
          w12.ytd-budget = w12.ytd-budget + segmentstat.budzimmeranz. 
        END. 
        IF AVAILABLE w13 THEN 
        DO: 
          w13.ytd-saldo = w13.ytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w13.ytd-budget = w13.ytd-budget + segmentstat.budpersanz. 
        END. */
      END. 
 
      ELSE 
      DO:
        ASSIGN
          w1.saldo = w1.saldo + segmentstat.zimmeranz
          w1.budget = w1.budget + segmentstat.budzimmeranz
        . 
        IF d-flag THEN w1.mon-saldo[DAY(segmentstat.datum)] 
          = w1.mon-saldo[DAY(segmentstat.datum)] + segmentstat.zimmeranz.
        IF dbudget-flag THEN w1.mon-budget[DAY(segmentstat.datum)] 
          = w1.mon-budget[DAY(segmentstat.datum)] + segmentstat.budzimmeranz.
        IF ytd-flag THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + segmentstat.zimmeranz. 
          w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
        END. 
 
        IF AVAILABLE w1a THEN 
        DO: 
          ASSIGN
            w1a.saldo = w1a.saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
            w1a.budget = w1a.budget + segmentstat.budpersanz
          . 
          IF d-flag THEN w1a.mon-saldo[DAY(segmentstat.datum)] 
            = w1a.mon-saldo[DAY(segmentstat.datum)] + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis.
          IF dbudget-flag THEN w1a.mon-budget[DAY(segmentstat.datum)] 
            = w1a.mon-budget[DAY(segmentstat.datum)] + segmentstat.budpersanz.
          IF ytd-flag THEN 
          DO: 
            w1a.ytd-saldo = w1a.ytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1a.ytd-budget = w1a.ytd-budget + segmentstat.budpersanz. 
          END. 
        END. 

        /*IF AVAILABLE w11 THEN 
        DO: 
          ASSIGN
            w11.saldo = w11.saldo + segmentstat.logis / frate
            w11.budget = w11.budget + segmentstat.budlogis. 
          IF d-flag THEN w11.mon-saldo[DAY(segmentstat.datum)] 
            = w11.mon-saldo[DAY(segmentstat.datum)] + segmentstat.logis / frate.
          IF dbudget-flag THEN w11.mon-budget[DAY(segmentstat.datum)] 
            = w11.mon-budget[DAY(segmentstat.datum)] + segmentstat.budlogis.
          IF ytd-flag THEN 
          DO: 
            w11.ytd-saldo = w11.ytd-saldo + segmentstat.logis / frate. 
            w11.ytd-budget = w11.ytd-budget + segmentstat.budlogis. 
          END. 
        END. 

        IF AVAILABLE w12 THEN 
        DO:
          ASSIGN
            w12.saldo = w12.saldo + segmentstat.zimmeranz
            w12.budget = w12.budget + segmentstat.budzimmeranz. 
          IF d-flag THEN w12.mon-saldo[DAY(segmentstat.datum)] 
            = w12.mon-saldo[DAY(segmentstat.datum)] + segmentstat.zimmeranz.
          IF dbudget-flag THEN w12.mon-budget[DAY(segmentstat.datum)] 
            = w12.mon-budget[DAY(segmentstat.datum)] + segmentstat.budzimmeranz.
          IF ytd-flag THEN 
          DO: 
            w12.ytd-saldo = w12.ytd-saldo + segmentstat.zimmeranz. 
            w12.ytd-budget = w12.ytd-budget + segmentstat.budzimmeranz. 
          END. 
        END. 

        IF AVAILABLE w13 THEN 
        DO: 
          ASSIGN
            w13.saldo = w13.saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
            w13.budget = w13.budget + segmentstat.budpersanz. 
          IF d-flag THEN w13.mon-saldo[DAY(segmentstat.datum)] 
            = w13.mon-saldo[DAY(segmentstat.datum)] + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis.
          IF dbudget-flag THEN w13.mon-budget[DAY(segmentstat.datum)] 
            = w13.mon-budget[DAY(segmentstat.datum)] + segmentstat.budpersanz.
          IF ytd-flag THEN 
          DO: 
            w13.ytd-saldo = w13.ytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.ytd-budget = w13.ytd-budget + segmentstat.budpersanz. 
          END. 
        END. */
      END. 
    END. 
 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum2 = Ljan1. 
      ELSE datum2 = Lfrom-date. 
      FOR EACH segmentstat WHERE segmentstat.datum GE datum2 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
        ASSIGN frate = 1.
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF segmentstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo + segmentstat.zimmeranz. 
          w1.lytd-budget = w1.lytd-budget + segmentstat.budzimmeranz. 
 
          IF AVAILABLE w1a THEN 
          DO: 
            w1a.lytd-saldo = w1a.lytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1a.lytd-budget = w1a.lytd-budget + segmentstat.budpersanz. 
          END. 
          /*IF AVAILABLE w11 THEN 
          DO: 
            w11.lytd-saldo = w11.lytd-saldo + segmentstat.logis / frate. 
            w11.lytd-budget = w11.lytd-budget + segmentstat.budlogis. 
          END. 
          IF AVAILABLE w12 THEN 
          DO: 
            w12.lytd-saldo = w12.lytd-saldo + segmentstat.zimmeranz. 
            w12.lytd-budget = w12.lytd-budget + segmentstat.budzimmeranz. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            w13.lytd-saldo = w13.lytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.lytd-budget = w13.lytd-budget + segmentstat.budpersanz. 
          END. */
        END. 
 
        ELSE DO: 
          dlmtd-flag = (MONTH(segmentstat.datum) = MONTH(to-date)) 
            AND (YEAR(segmentstat.datum) = YEAR(to-date) - 1).
          IF dlmtd-flag THEN w1.mon-lmtd[DAY(segmentstat.datum)] 
            = w1.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.zimmeranz.
          w1.lastyr = w1.lastyr + segmentstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + segmentstat.zimmeranz. 
          w1.ly-budget = w1.ly-budget + segmentstat.budzimmeranz. 
          IF lytd-flag THEN w1.lytd-budget = w1.lytd-budget 
            + segmentstat.budzimmeranz. 
 
          IF AVAILABLE w1a THEN 
          DO: 
            IF dlmtd-flag THEN w1a.mon-lmtd[DAY(segmentstat.datum)] 
              = w1a.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis.
            w1a.lastyr = w1a.lastyr + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1a.ly-budget = w1a.ly-budget + segmentstat.budpersanz. 
            IF lytd-flag THEN 
            DO: 
              w1a.lytd-saldo = w1a.lytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w1a.lytd-budget = w1a.lytd-budget + segmentstat.budpersanz. 
            END. 
          END. 
          /*IF AVAILABLE w11 THEN 
          DO: 
            IF dlmtd-flag THEN w11.mon-lmtd[DAY(segmentstat.datum)] 
              = w11.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.logis / frate.
            w11.lastyr = w11.lastyr + segmentstat.logis / frate. 
            w11.ly-budget = w11.ly-budget + segmentstat.budlogis. 
            IF lytd-flag THEN 
            DO: 
              w11.lytd-saldo = w11.lytd-saldo + segmentstat.logis / frate. 
              w11.lytd-budget = w11.lytd-budget + segmentstat.budlogis. 
            END. 
          END. 
          IF AVAILABLE w12 THEN 
          DO: 
            IF dlmtd-flag THEN w12.mon-lmtd[DAY(segmentstat.datum)] 
              = w12.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.zimmeranz.
            w12.lastyr = w12.lastyr + segmentstat.zimmeranz. 
            w12.ly-budget = w12.ly-budget + segmentstat.budzimmeranz. 
            IF lytd-flag THEN 
            DO: 
              w12.lytd-saldo = w12.lytd-saldo + segmentstat.zimmeranz. 
              w12.lytd-budget = w12.lytd-budget + segmentstat.budzimmeranz. 
            END. 
          END. 
          IF AVAILABLE w13 THEN 
          DO: 
            IF dlmtd-flag THEN w13.mon-lmtd[DAY(segmentstat.datum)] 
              = w13.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis.
            w13.lastyr = w13.lastyr + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w13.ly-budget = w13.ly-budget + segmentstat.budpersanz. 
            IF lytd-flag THEN 
            DO: 
              w13.lytd-saldo = w13.lytd-saldo + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
              w13.lytd-budget = w13.lytd-budget + segmentstat.budpersanz. 
            END. 
          END.*/ 
        END. 
      END. 
    END. 
    
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH segmentstat WHERE segmentstat.datum GE Pfrom-date 
      AND segmentstat.datum LE Pto-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lastmon = w1.lastmon + segmentstat.zimmeranz. 
      w1.lm-budget = w1.lm-budget + segmentstat.budzimmeranz.  
      IF AVAILABLE w1a THEN 
      DO: 
        w1a.lastmon = w1a.lastmon + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w1a.lm-budget = w1a.lm-budget + segmentstat.budpersanz. 
      END. 
      /*IF AVAILABLE w11 THEN 
      DO: 
        w11.lastmon = w11.lastmon + segmentstat.logis / frate. 
        w11.lm-budget = w11.lm-budget + segmentstat.budlogis. 
      END. 
      IF AVAILABLE w12 THEN 
      DO: 
        w12.lastmon = w12.lastmon + segmentstat.zimmeranz. 
        w12.lm-budget = w12.lm-budget + segmentstat.budzimmeranz. 
      END. 
      IF AVAILABLE w13 THEN 
      DO: 
        w13.lastmon = w13.lastmon + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w13.lm-budget = w13.lm-budget + segmentstat.budpersanz. 
      END.*/  
    END. 

    IF lytoday-flag THEN 
    FOR EACH segmentstat WHERE segmentstat.datum = lytoday
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lytoday = w1.lytoday + segmentstat.zimmeranz.  
      IF AVAILABLE w1a THEN 
        w1a.lytoday = w1a.lytoday + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
      /*IF AVAILABLE w11 THEN 
        w11.lytoday = w11.lytoday + segmentstat.logis / frate.    
      IF AVAILABLE w12 THEN 
        w12.lytoday = w12.lytoday + segmentstat.zimmeranz. 
      IF AVAILABLE w13 THEN 
        w13.lytoday = w13.lytoday + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. */
    END.
     
    /*IF AVAILABLE w11 THEN w11.done = YES. 
    IF AVAILABLE w12 THEN w12.done = YES. 
    IF AVAILABLE w13 THEN w13.done = YES. */
  END.   
  w1.done = YES. 
  IF AVAILABLE w1a THEN w1a.done = YES. 
END. 

PROCEDURE fill-new-rmocc:
  DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 

  DEFINE VARIABLE curr-date       AS DATE. 
  DEFINE VARIABLE datum1          AS DATE. 
  DEFINE VARIABLE datum2          AS DATE. 
  DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
  DEFINE VARIABLE dbudget-flag    AS LOGICAL NO-UNDO.
  DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
  DEFINE VARIABLE frate1          AS DECIMAL NO-UNDO.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1.            /* Room Occ     */
  IF w1.done THEN RETURN.

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 

  FOR EACH genstat WHERE
      genstat.datum GE datum1 AND genstat.datum LE to-date
      AND genstat.resstatus NE 13 /*AND genstat.segmentcode NE 0*/
      /*AND genstat.res-int[1] NE 13*/
      AND genstat.nationnr NE 0
      AND genstat.segmentcode NE 0
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */
      USE-INDEX nat_ix NO-LOCK
      BY genstat.segmentcode:
  
      d-flag = (MONTH(genstat.datum) = MONTH(to-date))
          AND (YEAR(genstat.datum) = YEAR(to-date)).

      IF genstat.datum = to-date THEN 
      DO:         
          w1.tday = w1.tday + 1.
      END. 
      IF MONTH(genstat.datum) EQ MONTH(to-date) AND YEAR(genstat.datum) EQ YEAR(to-date) THEN
      DO:
         w1.saldo = w1.saldo + 1.
      END.
      IF genstat.datum LT from-date THEN 
      DO:
        w1.ytd-saldo = w1.ytd-saldo + 1. 
      END.
      IF ytd-flag THEN 
      DO: 
         w1.ytd-saldo = w1.ytd-saldo + 1. 
      END.

      IF d-flag THEN w1.mon-saldo[DAY(genstat.datum)] 
          = w1.mon-saldo[DAY(genstat.datum)] + 1.
  END.

  FOR EACH segment NO-LOCK: 
 
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 

      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 

      dbudget-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
        AND (YEAR(segmentstat.datum) = YEAR(to-date)).

      IF segmentstat.datum = to-date THEN 
      DO:         
        w1.tbudget = w1.tbudget + segmentstat.budzimmeranz.         
      END.
      IF segmentstat.datum LT from-date THEN 
      DO: 
        w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
      END.
      IF MONTH(segmentstat.datum) EQ MONTH(to-date) AND YEAR(segmentstat.datum) EQ YEAR(to-date) THEN
      DO:
       w1.budget = w1.budget + segmentstat.budzimmeranz.
      END.
      IF ytd-flag THEN 
      DO: 
        w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
      END. 

      IF dbudget-flag THEN w1.mon-budget[DAY(segmentstat.datum)] 
          = w1.mon-budget[DAY(segmentstat.datum)] + segmentstat.budzimmeranz.

    END.
  END.

  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum2 = Ljan1. 
    ELSE datum2 = Lfrom-date. 

    FOR EACH genstat WHERE
      genstat.datum GE datum2 AND genstat.datum LE Lto-date
      AND genstat.resstatus NE 13 /*AND genstat.segmentcode NE 0*/
      /*AND genstat.res-int[1] NE 13*/
      AND genstat.nationnr NE 0
      AND genstat.segmentcode NE 0
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */
      USE-INDEX nat_ix NO-LOCK
      BY genstat.segmentcode:

      IF genstat.datum LT Lfrom-date THEN 
      DO: 
          w1.lytd-saldo = w1.lytd-saldo + 1. 
      END.
      ELSE 
      DO: 
         dlmtd-flag = (MONTH(genstat.datum) = MONTH(to-date)) 
           AND (YEAR(genstat.datum) = YEAR(to-date) - 1).
         IF dlmtd-flag THEN w1.mon-lmtd[DAY(genstat.datum)] 
           = w1.mon-lmtd[DAY(genstat.datum)] + 1.

         w1.lastyr = w1.lastyr + 1. /* LAST year MTD */ 

         IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + 1. 
      END.
    END.  

    FOR EACH segmentstat WHERE segmentstat.datum GE datum2 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
        ASSIGN frate = 1.
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 

        IF segmentstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-budget = w1.lytd-budget + segmentstat.budzimmeranz. 
        END. 
        ELSE DO: 
          w1.ly-budget = w1.ly-budget + segmentstat.budzimmeranz. 

          IF lytd-flag THEN w1.lytd-budget = w1.lytd-budget 
            + segmentstat.budzimmeranz. 
        END.
    END.
  END.

  IF pmtd-flag THEN /* previous MTD */ 
  DO:
    FOR EACH genstat WHERE
      genstat.datum GE Pfrom-date AND genstat.datum LE Pto-date
      AND genstat.resstatus NE 13 /*AND genstat.segmentcode NE 0*/
      /*AND genstat.res-int[1] NE 13*/
      AND genstat.nationnr NE 0
      AND genstat.segmentcode NE 0
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */
      USE-INDEX nat_ix NO-LOCK
      BY genstat.segmentcode:

      w1.lastmon = w1.lastmon + 1. 
    END.

    FOR EACH segmentstat WHERE segmentstat.datum GE Pfrom-date 
      AND segmentstat.datum LE Pto-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lm-budget = w1.lm-budget + segmentstat.budzimmeranz.  
    END.
  END.

  IF lytoday-flag THEN 
  DO:
    FOR EACH genstat WHERE
      genstat.datum = lytoday
      AND genstat.resstatus NE 13 /*AND genstat.segmentcode NE 0*/
      /*AND genstat.res-int[1] NE 13*/
      AND genstat.nationnr NE 0
      AND genstat.segmentcode NE 0
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */
      USE-INDEX nat_ix NO-LOCK
      BY genstat.segmentcode:

      w1.lytoday = w1.lytoday + 1.  
    END.
  END.
  w1.done = YES. 
END.


PROCEDURE fill-gledger: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 

DEFINE BUFFER w11 FOR w1. 
DEFINE BUFFER w12 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 

  FOR EACH uebertrag WHERE uebertrag.datum GE from-date - 1 AND
    uebertrag.datum LE to-date - 1 BY uebertrag.datum:
    w1.mon-saldo[DAY(uebertrag.datum + 1)] = uebertrag.betrag.
  END.
 
  FIND FIRST uebertrag WHERE uebertrag.datum = to-date - 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE uebertrag THEN 
  DO: 
    w1.tday = uebertrag.betrag. 
    w1.done = YES. 
  END. 
END. 

PROCEDURE fill-comproomsnew: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE mm AS INT.
DEFINE VARIABLE d-flag AS LOGICAL NO-UNDO. 

    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    
    IF ytd-flag THEN datum1 = jan1. 
      ELSE datum1 = from-date. 
    mm = MONTH(to-date).
    
    FOR EACH genstat WHERE genstat.datum GE datum1
        AND genstat.datum LE to-date
        AND genstat.zipreis = 0 
        AND genstat.gratis NE 0
        AND genstat.resstatus = 6 NO-LOCK, 
        FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK:
        IF segment.betriebsnr = 0 THEN
        DO:
            d-flag = (MONTH(genstat.datum) = MONTH(to-date)) AND (YEAR(genstat.datum) = YEAR(to-date)).
            IF d-flag THEN                
                w1.mon-saldo[DAY(genstat.datum)] = w1.mon-saldo[DAY(genstat.datum)] + 1.
            IF genstat.datum = to-date THEN
                w1.tday = w1.tday + 1.
            IF MONTH(genstat.datum) = mm THEN
                w1.saldo = w1.saldo + 1.
            
            IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + 1.
        END.                                
    END.

    IF (lytd-flag OR lmtd-flag) THEN 
    DO: 
        IF lytd-flag THEN datum1 = Ljan1. 
            ELSE datum1 = Lfrom-date.

        mm = MONTH(Lto-date).
        FOR EACH genstat WHERE genstat.datum GE datum1
            AND genstat.datum LE Lto-date
            AND genstat.zipreis = 0 
            AND genstat.gratis NE 0
            AND genstat.resstatus = 6 NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK:
            IF segment.betriebsnr = 0 THEN
            DO:
                IF MONTH(genstat.datum) = mm THEN
                    w1.lastyr = w1.lastyr + 1.
                w1.lytd-saldo = w1.lytd-saldo + 1.
            END.                                
        END.
    END.    

    IF pmtd-flag THEN /* previous MTD */ 
    DO:
        mm = MONTH(Pto-date).
        FOR EACH genstat WHERE genstat.datum GE Pfrom-date
            AND genstat.datum LE Pto-date
            AND genstat.zipreis = 0 
            AND genstat.gratis NE 0
            AND genstat.resstatus = 6 NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK:
            IF segment.betriebsnr = 0 THEN
            DO:
                IF MONTH(genstat.datum) = mm THEN
                    w1.lastmon = w1.lastmon + 1.
            END.                                
        END.
    END.
END.

PROCEDURE fill-comprooms: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE d-flag AS LOGICAL NO-UNDO.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  
  FOR EACH segment WHERE segment.betriebsnr = 0 NO-LOCK: /* paying segments */ 
    IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
      OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
      OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
      w1.lm-today = 0.
    ELSE
    DO:
      IF MONTH(to-date) EQ 1 THEN
        curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
      ELSE
        curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
      FIND FIRST segmentstat WHERE segmentstat.datum EQ curr-date
        AND segmentstat.segmentcode = segment.segmentcode 
        AND segmentstat.betriebsnr GT 0 NO-LOCK NO-ERROR.
      IF AVAILABLE segmentstat THEN
      DO:
        frate = 1.
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END.
        w1.lm-today = w1.lm-today + segmentstat.betriebsnr.
      END.
    END.
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segment.segmentcode 
      AND segmentstat.betriebsnr GT 0 NO-LOCK: 

      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
       
      d-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
          AND (YEAR(segmentstat.datum) = YEAR(to-date)).
      IF segmentstat.datum = to-date - 1 THEN 
        w1.yesterday = w1.yesterday + segmentstat.betriebsnr.
      IF segmentstat.datum = to-date THEN 
        w1.tday = w1.tday + segmentstat.betriebsnr. 
 
      IF segmentstat.datum LT from-date THEN 
        w1.ytd-saldo = w1.ytd-saldo + segmentstat.betriebsnr. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + segmentstat.betriebsnr. 
        IF d-flag THEN w1.mon-saldo[DAY(segmentstat.datum)] 
          = w1.mon-saldo[DAY(segmentstat.datum)] 
          + segmentstat.betriebsnr.
        IF ytd-flag THEN 
          w1.ytd-saldo = w1.ytd-saldo + segmentstat.betriebsnr. 
      END. 
    END. 

    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum2 = Ljan1. 
      ELSE datum2 = Lfrom-date. 
      FOR EACH segmentstat WHERE segmentstat.datum GE datum2 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF segmentstat.datum LT Lfrom-date THEN 
          w1.lytd-saldo = w1.lytd-saldo + segmentstat.betriebsnr. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr + segmentstat.betriebsnr. 
          IF lytd-flag THEN 
            w1.lytd-saldo = w1.lytd-saldo + segmentstat.betriebsnr. 
        END. 
      END. 
    END. 
 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH segmentstat WHERE segmentstat.datum GE Pfrom-date 
      AND segmentstat.datum LE Pto-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lastmon = w1.lastmon + segmentstat.betriebsnr. 
    END. 
 
    IF lytoday-flag THEN /* previous MTD */ 
    FOR EACH segmentstat WHERE segmentstat.datum EQ lytoday 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lytoday = w1.lytoday + segmentstat.betriebsnr. 
    END. 
  END. 
  w1.done = YES. 
END. 


PROCEDURE fill-rmocc%: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE BUFFER w11 FOR w1. 
DEFINE BUFFER w12 FOR w1. 
 
  FIND FIRST w11 WHERE w11.main-code = 805 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE w11 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Variable for Room Availablity not defined,",lvCAREA,"")
            + CHR(10)
            + translateExtended ("which is necessary for calculating of room occupancy.",lvCAREA,"").
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
 
  FIND FIRST w12 WHERE w12.main-code = 806 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE w12 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Variable for Occupied Rooms not defined,",lvCAREA,"")
            + CHR(10)
            + translateExtended ("which is necessary for calculating of room occupancy in %.",lvCAREA,"").
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
 
  IF NOT w11.done THEN RUN fill-rmavail(RECID(w11)). 
  /*IF NOT w12.done THEN RUN fill-rmocc(RECID(w12)).*/
  IF NOT w12.done THEN RUN fill-new-rmocc(RECID(w12)).
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF w11.tday NE 0 THEN w1.tday = w12.tday / w11.tday * 100. 
  IF w11.saldo NE 0 THEN w1.saldo = w12.saldo / w11.saldo * 100. 
  IF w11.ytd-saldo NE 0 THEN w1.ytd-saldo = w12.ytd-saldo / w11.ytd-saldo * 100. 
  IF w11.lytd-saldo NE 0 THEN w1.lytd-saldo = w12.lytd-saldo / w11.lytd-saldo 
    * 100. 
  IF w11.lastyr NE 0 THEN w1.lastyr = w12.lastyr / w11.lastyr * 100. 
  IF w11.lastmon NE 0 THEN w1.lastmon = w12.lastmon / w11.lastmon * 100. 
  IF w11.lytoday NE 0 THEN w1.lytoday = w12.lytoday / w11.lytoday * 100. 
  w1.done = YES. 
END. 


PROCEDURE fill-docc%: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE BUFFER w11 FOR w1. 
DEFINE BUFFER w12 FOR w1. 
  FIND FIRST w11 WHERE w11.main-code = 806 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE w11 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Variable for Occupied Rooms not defined,",lvCAREA,"") 
            + CHR(10)
            + translateExtended ("which is necessary for calculating of double room occupancy.",lvCAREA,"").
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
 
  FIND FIRST w12 WHERE w12.main-code = 810 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE w12 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Variable for Occupied Persons not defined,",lvCAREA,"")
            + CHR(10)
            + translateExtended ("which is necessary for calculating of double room occupancy.",lvCAREA,"").
    prog-error = YES. 
    error-nr = - 1. 
    RETURN. 
  END. 
 
  /*`IF NOT w11.done THEN RUN fill-rmocc(RECID(w11)). */
  IF NOT w11.done THEN RUN fill-new-rmocc(RECID(w11)).  
  IF NOT w12.done THEN RUN fill-persocc(RECID(w12)). 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF w11.tday NE 0 THEN w1.tday = (w12.tday - w11.tday) / w11.tday * 100. 
  IF w11.saldo NE 0 THEN w1.saldo = (w12.saldo - w11.saldo) / w11.saldo * 100. 
  IF w11.ytd-saldo NE 0 THEN w1.ytd-saldo 
    = (w12.ytd-saldo - w11.ytd-saldo) / w11.ytd-saldo * 100. 
  IF w11.lytd-saldo NE 0 THEN w1.lytd-saldo 
    = (w12.lytd-saldo - w11.lytd-saldo) / w11.lytd-saldo * 100. 
  IF w11.lastyr NE 0 THEN w1.lastyr 
    = (w12.lastyr - w11.lastyr) / w11.lastyr * 100. 
  IF w11.lastmon NE 0 THEN w1.lastmon 
    = (w12.lastmon - w11.lastmon) / w11.lastmon * 100. 
  IF w11.lytoday NE 0 THEN w1.lytoday
    = (w12.lytoday - w11.lytoday) / w11.lytoday * 100. 
  w1.done = YES. 
END. 

PROCEDURE fill-fbcost: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE VARIABLE cost AS DECIMAL. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST artikel WHERE artikel.artnr = w1.artnr 
    AND artikel.departement = w1.dept NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Article for Cost-variable not found : ",lvCAREA,"") + w1.varname.
    error-nr = -1. 
    RETURN. 
  END. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 AND h-umsatz.datum LE to-date 
    AND h-umsatz.departement = w1.dept NO-LOCK, 
    FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
    AND h-artikel.departement = h-umsatz.departement 
    AND h-artikel.artnrfront = artikel.artnr NO-LOCK: 
    RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
      OUTPUT cost). 
    IF h-umsatz.datum = to-date THEN 
      w1.tday = w1.tday + cost. 
    IF h-umsatz.datum LT from-date THEN 
      w1.ytd-saldo = w1.ytd-saldo + cost. 
    ELSE 
    DO: 
      w1.saldo = w1.saldo + cost. 
      IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + cost. 
    END. 
  END. 
  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum1 = Ljan1. 
    ELSE datum1 = Lfrom-date. 
    FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 
      AND h-umsatz.datum LE Lto-date AND h-umsatz.departement = w1.dept NO-LOCK, 
      FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
      AND h-artikel.departement = h-umsatz.departement 
      AND h-artikel.artnrfront = artikel.artnr NO-LOCK: 
      RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
        OUTPUT cost). 
      IF h-umsatz.datum LT Lfrom-date THEN 
        w1.lytd-saldo = w1.lytd-saldo + cost. 
      ELSE 
      DO: 
        w1.lastyr = w1.lastyr + cost. /* LAST year MTD */ 
        IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + cost. 
      END. 
    END. 
  END. 
  IF pmtd-flag THEN /* previous MTD */ 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE Pfrom-date 
    AND h-umsatz.datum LE Pto-date AND h-umsatz.departement = w1.dept NO-LOCK, 
    FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
    AND h-artikel.departement = h-umsatz.departement 
    AND h-artikel.artnrfront = artikel.artnr NO-LOCK: 
    RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
      OUTPUT cost). 
    w1.lastmon = w1.lastmon + cost. 
  END. 
  IF lytoday-flag THEN 
  FOR EACH h-umsatz WHERE h-umsatz.datum EQ lytoday 
    AND h-umsatz.departement = w1.dept NO-LOCK, 
    FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
    AND h-artikel.departement = h-umsatz.departement 
    AND h-artikel.artnrfront = artikel.artnr NO-LOCK: 
    RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
      OUTPUT cost). 
    w1.lytoday = w1.lytoday + cost. 
  END.   
  w1.done = YES. 
END. 


PROCEDURE fill-sgfb: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER.
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE VARIABLE cost    AS DECIMAL. 
DEFINE VARIABLE sg-dept AS INT.
DEFINE VARIABLE subgr   AS INT.
DEFINE VARIABLE vat     AS DEC.
DEFINE VARIABLE serv    AS DEC.
DEFINE VARIABLE fact    AS DEC.
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 

  ASSIGN
      sg-dept = INT(SUBSTR(w1.s-artnr,1,2))
      subgr = INT(SUBSTR(w1.s-artnr,3)).

  FIND FIRST wgrpdep WHERE wgrpdep.zknr = subgr 
    AND wgrpdep.departement = sg-dept NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE wgrpdep THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("SubGroup not found : ",lvCAREA,"") + w1.varname.
    error-nr = -1. 
    RETURN. 
  END. /**/
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  
  FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 AND h-umsatz.datum LE to-date 
    AND h-umsatz.departement = sg-dept NO-LOCK,
    FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
        AND h-artikel.departement = h-umsatz.departement 
        AND h-artikel.zwkum = subgr
        AND h-artikel.artart = 0 NO-LOCK: 

    /*RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
      OUTPUT cost). */

    RUN calc-servvat.p(h-artikel.departement, h-artikel.artnr, datum, h-artikel.service-code, h-artikel.mwst-code, OUTPUT serv, OUTPUT vat).
            fact = (1.00 + serv + vat).

    IF h-umsatz.datum = to-date THEN 
    DO:
        IF main-nr = 9985 THEN
            w1.tday = w1.tday + h-umsatz.betrag / fact. 
        ELSE IF main-nr = 9986 THEN
            w1.tday = w1.tday + h-umsatz.anzahl.
    END.

    IF MONTH(h-umsatz.datum) = MONTH(to-date) THEN
    DO:
        IF main-nr = 9985 THEN
            w1.saldo = w1.saldo + h-umsatz.betrag / fact. 
        ELSE IF main-nr = 9986 THEN
            w1.saldo = w1.saldo + h-umsatz.anzahl.
    END.
    IF ytd-flag THEN
    DO:
        IF main-nr = 9985 THEN
            w1.ytd-saldo = w1.ytd-saldo + h-umsatz.betrag / fact. 
        ELSE IF main-nr = 9986 THEN
            w1.ytd-saldo = w1.ytd-saldo + h-umsatz.anzahl.
    END.                                                  
  END.
  
  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum1 = Ljan1. 
    ELSE datum1 = Lfrom-date. 
    FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 
        AND h-umsatz.datum LE Lto-date 
        AND h-umsatz.departement = sg-dept NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
            AND h-artikel.departement = h-umsatz.departement 
            AND h-artikel.zwkum = subgr
            AND h-artikel.artart = 0 NO-LOCK: 
        RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
            OUTPUT cost). 
        IF h-umsatz.datum LT Lfrom-date THEN 
            w1.lytd-saldo = w1.lytd-saldo + cost. 
        ELSE 
        DO: 
            w1.lastyr = w1.lastyr + cost. /* LAST year MTD */ 
            IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + cost. 
        END. 
    END. 
  END. 
  IF pmtd-flag THEN /* previous MTD */ 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE Pfrom-date
      AND h-umsatz.datum LE Pto-date 
      AND h-umsatz.departement = sg-dept NO-LOCK,
      FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
        AND h-artikel.departement = h-umsatz.departement 
        AND h-artikel.zwkum = subgr
        AND h-artikel.artart = 0 NO-LOCK: 
        
      RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
          OUTPUT cost). 
      w1.lastmon = w1.lastmon + cost. 
  END. 
  
  IF lytoday-flag THEN 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE lytoday
      AND h-umsatz.departement = sg-dept NO-LOCK,
      FIRST h-artikel WHERE h-artikel.artnr = h-umsatz.artnr 
        AND h-artikel.departement = h-umsatz.departement 
        AND h-artikel.zwkum = subgr
        AND h-artikel.artart = 0 NO-LOCK: 
    
      RUN cal-fbcost(h-umsatz.artnr, h-umsatz.departement, h-umsatz.datum, 
          OUTPUT cost). 
      w1.lytoday = w1.lytoday + cost. 
  END.   
  w1.done = YES. 
END. 


PROCEDURE fill-quantity: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE datum2 AS DATE. 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE d-flag AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST artikel WHERE artikel.artnr = w1.artnr 
    AND artikel.departement = w1.dept NO-LOCK NO-ERROR. 
 
  IF NOT AVAILABLE artikel THEN 
  DO:
      msg-str = msg-str + CHR(2)
            + translateExtended ("No such article number : ",lvCAREA,"") + STRING(w1.artnr)
            + " " + translateExtended ("Dept",lvCAREA,"") + " " + STRING(w1.dept).
      RETURN.
  END. 
  
  IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
    OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
    OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
    w1.lm-today = 0.
  ELSE
  DO:
    IF MONTH(to-date) EQ 1 THEN
      curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
    ELSE
      curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
    FIND FIRST umsatz WHERE umsatz.datum EQ curr-date 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK NO-ERROR.
    IF AVAILABLE umsatz THEN
      w1.lm-today = umsatz.anzahl.
  END.

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  FOR EACH umsatz WHERE umsatz.datum GE datum1 AND umsatz.datum LE to-date 
    AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK: 

    d-flag = (MONTH(umsatz.datum) = MONTH(to-date))
        AND (YEAR(umsatz.datum) = YEAR(to-date)).
    IF umsatz.datum = to-date - 1 THEN 
      w1.yesterday = w1.yesterday + umsatz.anzahl. 
    
    IF umsatz.datum = to-date THEN 
      w1.tday = w1.tday + umsatz.anzahl. 
    
    IF umsatz.datum LT from-date THEN 
      w1.ytd-saldo = w1.ytd-saldo + umsatz.anzahl. 
    ELSE 
    DO: 
      w1.saldo = w1.saldo + umsatz.anzahl. 
      IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + umsatz.anzahl. 
      IF d-flag THEN w1.mon-saldo[DAY(umsatz.datum)] 
        = w1.mon-saldo[DAY(umsatz.datum)] + umsatz.anzahl.
    END. 
  END. 
  IF lytd-flag OR lmtd-flag THEN 
  DO: 
    IF lytd-flag THEN datum2 = Ljan1. 
    ELSE datum2 = Lfrom-date. 
    FOR EACH umsatz WHERE umsatz.datum GE datum2 AND umsatz.datum LE Lto-date 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK: 
      IF umsatz.datum LT Lfrom-date THEN 
        w1.lytd-saldo = w1.lytd-saldo + umsatz.anzahl. 
      ELSE 
      DO: 
        dlmtd-flag = (MONTH(umsatz.datum) = MONTH(to-date)) 
          AND (YEAR(umsatz.datum) = YEAR(to-date) - 1).
        IF dlmtd-flag THEN w1.mon-lmtd[DAY(umsatz.datum)] 
          = w1.mon-lmtd[DAY(umsatz.datum)] + umsatz.anzahl.
        w1.lastyr = w1.lastyr + umsatz.anzahl. /* LAST year MTD */ 
        IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + umsatz.anzahl. 
      END. 
    END. 
  END. 
  IF pmtd-flag THEN /* previous MTD */ 
  FOR EACH umsatz WHERE umsatz.datum GE Pfrom-date 
    AND umsatz.datum LE Pto-date 
    AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK: 
    w1.lastmon = w1.lastmon + umsatz.anzahl. 
  END. 
  IF lytoday-flag THEN 
  DO:
    FIND FIRST umsatz WHERE umsatz.datum EQ lytoday 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE umsatz THEN w1.lastmon = w1.lastmon + umsatz.anzahl. 
  END. 
  w1.done = YES. 
END. 

PROCEDURE fill-revenue: 
DEFINE INPUT PARAMETER rec-w1   AS INTEGER. 
DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE serv            AS DECIMAL. 
DEFINE VARIABLE vat             AS DECIMAL. 
DEFINE VARIABLE vat2            AS DECIMAL.
DEFINE VARIABLE fact            AS DECIMAL. 
DEFINE VARIABLE n-betrag        AS DECIMAL.
DEFINE VARIABLE n-serv          AS DECIMAL. 
DEFINE VARIABLE n-tax           AS DECIMAL. 
DEFINE VARIABLE ly-betrag       AS DECIMAL. 
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dbudget-flag    AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.

DEFINE VARIABLE yes-serv        AS DECIMAL. 
DEFINE VARIABLE yes-vat         AS DECIMAL. 
DEFINE VARIABLE yes-vat2        AS DECIMAL. 
DEFINE VARIABLE yes-fact        AS DECIMAL. 
DEFINE VARIABLE yes-betrag      AS DECIMAL. 
DEFINE VARIABLE date1           AS DATE.
DEFINE VARIABLE date2           AS DATE.
DEFINE VARIABLE temp-date2      AS DATE.
DEFINE VARIABLE temp-curr-date  AS DATE.
DEFINE BUFFER   ubuff           FOR umsatz.
DEFINE BUFFER   buff-umsatz     FOR umsatz.

DEFINE VARIABLE tot-betrag    AS DECIMAL.
DEFINE VARIABLE st-date         AS INT INIT 0.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
  FIND FIRST artikel WHERE artikel.artnr = w1.artnr 
    AND artikel.departement = w1.dept NO-LOCK NO-ERROR.
  IF NOT AVAILABLE artikel THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("No such article number : ",lvCAREA,"") + STRING(w1.artnr)
            + " " + translateExtended ("Dept",lvCAREA,"") + " " + STRING(w1.dept).
    RETURN.
  END.
  /*FT last month today*/
  IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
  OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
  OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
  DO:
    st-date = 1.
    curr-date = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1.  /*FT 010413*/
    /*MTcurr-date = DATE(MONTH(to-date) - 1, DAY(to-date) - 1, YEAR(to-date) - 1).*/
    w1.lm-today = 0.
  END.
  ELSE
  DO:
    st-date = 2.
    IF MONTH(to-date) EQ 1 THEN
      curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
    ELSE
      curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
  END.
      
  FOR EACH buff-umsatz WHERE buff-umsatz.datum GE DATE(MONTH(curr-date),1,YEAR(curr-date))
    AND buff-umsatz.datum LE curr-date
    AND buff-umsatz.artnr = w1.artnr AND buff-umsatz.departement = w1.dept NO-LOCK:
    /*RUN calc-servvat.p(buff-umsatz.departement, buff-umsatz.artnr, buff-umsatz.datum, 
                        artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).*/
     RUN calc-servtaxesbl.p(1, buff-umsatz.artnr, buff-umsatz.departement,
                           buff-umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
    fact = 1.00 + serv + vat + vat2.
    n-betrag = 0. 
    IF foreign-flag THEN 
    DO: 
      RUN find-exrate(curr-date). 
      IF AVAILABLE exrate THEN frate = exrate.betrag. 
    END. 
    ASSIGN
      n-betrag = buff-umsatz.betrag / (fact * frate)
      n-serv   = n-betrag * serv
      n-tax    = n-betrag * vat.
    IF price-decimal = 0 THEN
      ASSIGN
        n-betrag = ROUND(n-betrag, 0)
        n-serv = ROUND(n-serv, 0)
        n-tax = ROUND(n-tax, 0). 
    IF buff-umsatz.datum = curr-date AND st-date = 2 THEN
      ASSIGN
        w1.lm-today = w1.lm-today + n-betrag
        w1.lm-today-serv = w1.lm-today-serv + n-serv
        w1.lm-today-tax = w1.lm-today-tax + n-tax. 
    w1.lm-mtd = w1.lm-mtd + n-betrag. 
  END.
  
  /*geral ambil nilai awal - akhir tahun to-date E9DE63*/
  IF budget-all THEN 
  DO:
    date2      = DATE(12, 31, YEAR(to-date)).

    IF ytd-flag THEN ASSIGN date1 = jan1.
    ELSE date1 = from-date.

    DO temp-curr-date = date1 TO date2:
 
     FIND FIRST budget WHERE budget.artnr = w1.artnr 
     AND budget.departement = w1.dept 
     AND budget.datum = temp-curr-date NO-LOCK NO-ERROR.
     
     IF AVAILABLE budget THEN
     DO:
         IF temp-curr-date GE DATE(MONTH(to-date), 1, YEAR(to-date)) 
             AND temp-curr-date LE DATE((MONTH(to-date ) + 1), 1, YEAR(to-date)) - 1 THEN
         DO:
            w1.month-budget = w1.month-budget + budget.betrag.
         END.
         w1.year-budget = w1.year-budget + budget.betrag.
     END.
    END.
  END.
  /*end geral*/

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 

  DO curr-date = datum1 TO to-date:
    ASSIGN
        serv = 0
        vat  = 0
    .
    FIND FIRST umsatz WHERE umsatz.datum = curr-date 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE umsatz THEN
    /*RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
             artikel.mwst-code, OUTPUT serv, OUTPUT vat).*/

      RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                             umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
    
    fact = 1.00 + serv + vat + vat2.

    d-flag = AVAILABLE umsatz AND (MONTH(umsatz.datum) = MONTH(to-date))
      AND (YEAR(umsatz.datum) = YEAR(to-date)).
    
    n-betrag = 0. 
    IF AVAILABLE umsatz THEN 
    DO: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(curr-date). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      ASSIGN
        n-betrag = umsatz.betrag / (fact * frate) 
        n-serv   = n-betrag * serv
        n-tax    = n-betrag * vat.

      IF umsatz.artnr = 100 THEN DO:
          ASSIGN tot-betrag = tot-betrag + n-betrag.
      END.
      IF price-decimal = 0 THEN 
      DO:
        ASSIGN 
          n-betrag = ROUND(n-betrag, 0)
          n-serv = ROUND(n-serv, 0)
          n-tax = ROUND(n-tax, 0).
      END.
    END. 


    IF budget-flag THEN FIND FIRST budget WHERE budget.artnr = w1.artnr 
      AND budget.departement = w1.dept 
      AND budget.datum = curr-date NO-LOCK NO-ERROR.

    dbudget-flag = AVAILABLE budget AND (MONTH(budget.datum) = MONTH(to-date))
      AND (YEAR(budget.datum) = YEAR(to-date)).
    IF dbudget-flag THEN w1.mon-budget[DAY(budget.datum)] = w1.mon-budget[DAY(budget.datum)] + budget.betrag.

    IF d-flag THEN
    DO:
       w1.mon-serv[DAY(umsatz.datum)] = w1.mon-serv[DAY(umsatz.datum)] + n-serv.
       w1.mon-tax[DAY(umsatz.datum)]  = w1.mon-tax[DAY(umsatz.datum)] + n-tax.
    END.

    
    ly-betrag = 0.
    IF curr-date = to-date THEN 
    DO: 
      ASSIGN
        serv = 0
        vat  = 0.
      IF AVAILABLE umsatz THEN
      DO:
        ASSIGN
          w1.tday = w1.tday + n-betrag
          w1.tday-serv = w1.tday-serv + n-serv 
          w1.tday-tax = w1.tday-tax + n-tax.
      END.
      IF AVAILABLE budget THEN w1.tbudget = w1.tbudget + budget.betrag. 
    END. 

    IF curr-date = to-date THEN
    DO:
      FIND FIRST buff-umsatz WHERE buff-umsatz.datum = curr-date - 1 
        AND buff-umsatz.artnr = w1.artnr AND buff-umsatz.departement = w1.dept NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE buff-umsatz THEN
      DO:
        /*RUN calc-servvat.p(buff-umsatz.departement, buff-umsatz.artnr, buff-umsatz.datum, 
            artikel.service-code, artikel.mwst-code, OUTPUT yes-serv, OUTPUT yes-vat).*/

        RUN calc-servtaxesbl.p(1, buff-umsatz.artnr, buff-umsatz.departement,
                               buff-umsatz.datum, OUTPUT yes-serv, OUTPUT yes-vat, OUTPUT yes-vat2, OUTPUT fact).
        yes-fact = 1.00 + yes-serv + yes-vat + yes-vat2. 
        yes-betrag = 0. 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(curr-date - 1). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        yes-betrag = buff-umsatz.betrag / (yes-fact * frate). 
        IF price-decimal = 0 THEN yes-betrag = ROUND(yes-betrag, 0). 
        w1.yesterday = w1.yesterday + yes-betrag. 
      END.
    END. 

    IF curr-date LE to-date THEN
    DO:
      IF AVAILABLE umsatz THEN
      DO:
        ASSIGN
          w1.ytd-serv = w1.ytd-serv + n-serv
          w1.ytd-tax  = w1.ytd-tax  + n-tax.
      END.
    END.

    /*
    IF d-flag THEN
    DO:
      ASSIGN
        w1.mtd-serv = w1.mtd-serv + n-serv
        w1.mtd-tax  = w1.mtd-tax  + n-tax.
    END.*/
    
    IF curr-date LT from-date THEN 
    DO: 
      IF AVAILABLE umsatz THEN w1.ytd-saldo = w1.ytd-saldo + n-betrag. 
      IF AVAILABLE budget THEN w1.ytd-budget = w1.ytd-budget + budget.betrag. 
    END. 
    ELSE 
    DO: 
      IF AVAILABLE umsatz THEN 
      DO: 
        w1.saldo = w1.saldo + n-betrag. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + n-betrag. 
        IF d-flag THEN w1.mon-saldo[DAY(umsatz.datum)] 
          = w1.mon-saldo[DAY(umsatz.datum)] + n-betrag.

        ASSIGN
            w1.mtd-serv = w1.mtd-serv + n-serv
            w1.mtd-tax  = w1.mtd-tax  + n-tax.
      END. 
      IF AVAILABLE budget THEN 
      DO: 
        w1.budget = w1.budget + budget.betrag. 
        IF ytd-flag THEN w1.ytd-budget = w1.ytd-budget + budget.betrag. 
        /*IF dbudget-flag AND AVAILABLE umsatz THEN w1.mon-budget[DAY(umsatz.datum)] 
          = w1.mon-budget[DAY(umsatz.datum)] + budget.betrag.*/
      END. 
    END. 
  END. 
 
  IF lytd-flag OR lmtd-flag THEN 
  DO:

    IF lytd-flag THEN datum1 = Ljan1. 
    ELSE datum1 = Lfrom-date. 
    
    DO curr-date = datum1 TO Lto-date: 
      ASSIGN
        serv = 0
        vat  = 0.
      FIND FIRST umsatz WHERE umsatz.datum = curr-date 
        AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE umsatz THEN
        /*RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
                           artikel.mwst-code, OUTPUT serv, OUTPUT vat).*/
          RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                                 umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
      fact = 1.00 + serv + vat + vat2.
    
      n-betrag = 0. 
      IF AVAILABLE umsatz THEN 
      DO: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(curr-date). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        ASSIGN                                                     
          n-betrag = umsatz.betrag / (fact * frate)
          n-serv   = n-betrag * serv
          n-tax    = n-betrag * vat. 
        IF price-decimal = 0 THEN
        DO: 
          ASSIGN
            n-betrag = round(n-betrag, 0)
            n-serv = ROUND(n-serv, 0)
            n-tax = ROUND(n-tax, 0). 
        END.
      END. 
      IF budget-flag THEN FIND FIRST budget WHERE budget.artnr = w1.artnr 
        AND budget.departement = w1.dept 
        AND budget.datum = curr-date NO-LOCK NO-ERROR. 

      IF curr-date LT Lfrom-date THEN 
      DO: 
        IF AVAILABLE umsatz THEN 
            ASSIGN 
                w1.lytd-saldo = w1.lytd-saldo + n-betrag
                w1.lytd-serv  = w1.lytd-serv + n-serv
                w1.lytd-tax   = w1.lytd-tax + n-tax. 
        IF AVAILABLE budget THEN w1.lytd-budget = w1.lytd-budget + budget.betrag. 
      END. 
      ELSE 
      DO: 
        IF AVAILABLE umsatz THEN 
        DO: 
          dlmtd-flag = AVAILABLE umsatz AND (MONTH(umsatz.datum) = MONTH(to-date)) 
            AND (YEAR(umsatz.datum) = YEAR(to-date) - 1).
          IF dlmtd-flag THEN DO:
              ASSIGN
                w1.mon-lmtd[DAY(umsatz.datum)] = w1.mon-lmtd[DAY(umsatz.datum)] + n-betrag
                w1.lastyr                      = w1.lastyr + n-betrag /* LAST year MTD */ 
                w1.lmtd-serv                   = w1.lmtd-serv + n-serv
                w1.lmtd-tax                    = w1.lmtd-tax  + n-tax.
          END.
             

          IF (DAY(umsatz.datum) = DAY(to-date)) 
            AND (MONTH(umsatz.datum) = MONTH(to-date)) 
            AND (YEAR(umsatz.datum) = YEAR(to-date) - 1) THEN DO:
               ASSIGN
                   w1.lytoday-serv = w1.lytoday-serv + n-serv
                   w1.lytoday-tax = w1.lytoday-tax + n-tax. 
          END.

          
          IF lytd-flag THEN 
              ASSIGN 
                    w1.lytd-saldo = w1.lytd-saldo + n-betrag
                    w1.lytd-serv = w1.lytd-serv + n-serv
                    w1.lytd-tax = w1.lytd-tax + n-tax. 
        END. 
        IF AVAILABLE budget THEN 
        DO: 
          w1.ly-budget = w1.ly-budget + budget.betrag. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-budget = w1.lytd-budget + budget.betrag. 
        END. 
      END. 
    END. 
  END. 
 
  IF pmtd-flag THEN /* previous MTD */ 
  DO curr-date = Pfrom-date TO Pto-date: 
    ASSIGN
      serv = 0
      vat  = 0.
    FIND FIRST umsatz WHERE umsatz.datum = curr-date 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE umsatz THEN
      RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                             umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
    fact = 1.00 + serv + vat + vat2.
    n-betrag = 0. 
    IF AVAILABLE umsatz THEN 
    DO: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(curr-date). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      ASSIGN                                                     
        n-betrag = umsatz.betrag / (fact * frate)
        n-serv   = n-betrag * serv
        n-tax    = n-betrag * vat. 
      IF price-decimal = 0 THEN
      DO: 
        ASSIGN
          n-betrag = round(n-betrag, 0)
          n-serv = ROUND(n-serv, 0)
          n-tax = ROUND(n-tax, 0). 
      END.
    END. 
    IF budget-flag THEN FIND FIRST budget WHERE budget.artnr = w1.artnr 
      AND budget.departement = w1.dept 
      AND budget.datum = curr-date NO-LOCK NO-ERROR. 
    IF AVAILABLE umsatz THEN
    DO: 
      w1.lastmon = w1.lastmon + n-betrag.
      w1.pmtd-serv = w1.pmtd-serv + n-serv.
      w1.pmtd-tax = w1.pmtd-tax + n-tax.
    END.
    IF AVAILABLE budget THEN w1.lm-budget = w1.lm-budget + budget.betrag. 
  END. 
 
  IF lytoday-flag THEN 
  DO curr-date = lytoday TO lytoday: 
    ASSIGN
      serv = 0
      vat  = 0.
    FIND FIRST umsatz WHERE umsatz.datum = curr-date 
      AND umsatz.artnr = w1.artnr AND umsatz.departement = w1.dept NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE umsatz THEN
    RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                             umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
    fact = 1.00 + serv + vat + vat2.
    n-betrag = 0. 
    IF AVAILABLE umsatz THEN 
    DO: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(curr-date). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END.
      n-betrag = umsatz.betrag / (fact * frate). 
      IF price-decimal = 0 THEN n-betrag = round(n-betrag, 0).
    END. 
    IF budget-flag THEN FIND FIRST budget WHERE budget.artnr = w1.artnr 
      AND budget.departement = w1.dept 
      AND budget.datum = curr-date NO-LOCK NO-ERROR. 
    IF AVAILABLE umsatz THEN w1.lytoday = w1.lytoday + n-betrag. 
  END. 
  w1.done = YES. 
END.

PROCEDURE fill-persocc: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 

DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE datum2          AS DATE. 
DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE ly-currdate     AS DATE.
DEFINE VARIABLE d-flag          AS LOGICAL.
DEFINE VARIABLE dbudget-flag    AS LOGICAL.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
DEFINE VARIABLE frate1          AS DECIMAL NO-UNDO.

DEFINE BUFFER w11 FOR w1. 
DEFINE BUFFER w753 FOR w1. 
DEFINE BUFFER w754 FOR w1. 
DEFINE BUFFER w755 FOR w1. 
  
  /*FIND FIRST w11 WHERE w11.main-code = 806 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. */
 
  FIND FIRST w753 WHERE w753.main-code = 753 AND NOT w753.done NO-ERROR. 
  FIND FIRST w754 WHERE w754.main-code = 754 AND NOT w754.done NO-ERROR. 
  FIND FIRST w755 WHERE w755.main-code = 755 AND NOT w755.done NO-ERROR. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  IF lytd-flag THEN datum2 = Ljan1. 
  ELSE datum2 = Lfrom-date. 

  
  FOR EACH segment NO-LOCK: /*>>>>>*/
    IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
      OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
      OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
    DO:
      IF AVAILABLE w1   THEN w1.lm-today = 0.
      IF AVAILABLE w753 THEN w753.lm-today = 0.
      /*IF AVAILABLE w11  THEN w11.lm-today = 0.*/
    END.
    ELSE
    DO:
      IF MONTH(to-date) EQ 1 THEN
        curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
      ELSE
        curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
      FIND FIRST segmentstat WHERE segmentstat.datum EQ curr-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK NO-ERROR.
      IF AVAILABLE segmentstat THEN
      DO:
        frate = 1.
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END.
        w1.lm-today = w1.lm-today + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        IF AVAILABLE w753 THEN 
          w753.lm-today = w753.lm-today + segmentstat.persanz.
        /*IF AVAILABLE w11 THEN 
          w11.lm-today = w11.lm-today + segmentstat.zimmeranz. */
      END.
    END.

    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 

      d-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
          AND (YEAR(segmentstat.datum) = YEAR(to-date)).
      dbudget-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
          AND (YEAR(segmentstat.datum) = YEAR(to-date)).
      /*FT*/
      IF segmentstat.datum = to-date - 1 THEN
      DO:
        w1.yesterday = w1.yesterday + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        IF AVAILABLE w753 THEN 
          w753.yesterday = w753.yesterday + segmentstat.persanz.
        /*IF AVAILABLE w11 THEN 
          w11.yesterday = w11.yesterday + segmentstat.zimmeranz.*/ 
      END.
      /*FT*/
      IF segmentstat.datum = to-date THEN 
      DO: 
        RELEASE segmbuff.
        IF lytd-flag AND segmentstat.datum = to-date THEN
        DO:
          IF MONTH(to-date) = 2 AND DAY(to-date) = 29 THEN .
          ELSE
          DO:
            ly-currdate = DATE(MONTH(to-date), DAY(to-date), YEAR(to-date) - 1).      
            FIND FIRST segmbuff WHERE segmbuff.datum = ly-currdate 
              AND segmbuff.segmentcode = segment.segmentcode 
              NO-LOCK NO-ERROR. 
          END.
        END.

        w1.tday = w1.tday + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w1.tbudget = w1.tbudget + segmentstat.budpersanz. 
        /*IF AVAILABLE w11 THEN 
        DO: 
          w11.tday = w11.tday + segmentstat.zimmeranz. 
          w11.tbudget = w11.tbudget + segmentstat.budzimmeranz.
        END.*/ 
        IF AVAILABLE w753 THEN 
          w753.tday = w753.tday + segmentstat.persanz. 
        IF AVAILABLE w754 THEN 
          w754.tday = w754.tday + segmentstat.kind1. 
        IF AVAILABLE w755 THEN 
          w755.tday = w755.tday + segmentstat.kind2. 
      END. 

      IF segmentstat.datum LE Lfr-date THEN 
      DO: 
        w1.lm-ytd = w1.lm-ytd + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        /*IF AVAILABLE w11 THEN 
          w11.lm-ytd = w11.lm-ytd + segmentstat.zimmeranz.*/ 
        IF AVAILABLE w753 THEN 
          w753.lm-ytd = w753.lm-ytd + segmentstat.persanz. 
        IF AVAILABLE w754 THEN 
          w754.lm-ytd = w754.lm-ytd + segmentstat.kind1. 
        IF AVAILABLE w755 THEN 
          w755.lm-ytd = w755.lm-ytd + segmentstat.kind2. 
      END. 
 
      IF segmentstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        w1.ytd-budget = w1.ytd-budget + segmentstat.budpersanz. 
        /*IF AVAILABLE w11 THEN 
        DO: 
          w11.ytd-saldo = w11.ytd-saldo + segmentstat.zimmeranz. 
          w11.ytd-budget = w11.ytd-budget + segmentstat.budzimmeranz. 
        END.*/ 
        IF AVAILABLE w753 THEN
          w753.ytd-saldo = w753.ytd-saldo + segmentstat.persanz. 
        IF AVAILABLE w754 THEN 
          w754.ytd-saldo = w754.ytd-saldo + segmentstat.kind1. 
        IF AVAILABLE w755 THEN 
          w755.ytd-saldo = w755.ytd-saldo + segmentstat.kind2.
      END. 
      ELSE 
      DO: 
        ASSIGN
          w1.saldo = w1.saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis
          w1.budget = w1.budget + segmentstat.budpersanz
        . 
        IF d-flag THEN w1.mon-saldo[DAY(segmentstat.datum)] 
          = w1.mon-saldo[DAY(segmentstat.datum)]+ segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis.
        IF dbudget-flag THEN w1.mon-budget[DAY(segmentstat.datum)] 
          = w1.mon-budget[DAY(segmentstat.datum)]+ segmentstat.budpersanz.

        /*IF AVAILABLE w11 THEN 
        DO: 
          ASSIGN
            w11.saldo = w11.saldo + segmentstat.zimmeranz
            w11.budget = w11.budget + segmentstat.budzimmeranz
          . 
          IF d-flag THEN w11.mon-saldo[DAY(segmentstat.datum)] 
            = w11.mon-saldo[DAY(segmentstat.datum)] + segmentstat.zimmeranz.
          IF dbudget-flag THEN w11.mon-budget[DAY(segmentstat.datum)] 
            = w11.mon-budget[DAY(segmentstat.datum)]+ segmentstat.budzimmeranz.
        END. */

        IF AVAILABLE w753 THEN 
        DO: 
          w753.saldo = w753.saldo + segmentstat.persanz. 
          IF d-flag THEN w753.mon-saldo[DAY(segmentstat.datum)] 
            = w753.mon-saldo[DAY(segmentstat.datum)] + segmentstat.persanz.
        END. 

        IF AVAILABLE w754 THEN 
        DO: 
          w754.saldo = w754.saldo + segmentstat.kind1. 
          IF d-flag THEN w754.mon-saldo[DAY(segmentstat.datum)] 
            = w754.mon-saldo[DAY(segmentstat.datum)] + segmentstat.kind1.
        END. 

        IF AVAILABLE w755 THEN 
        DO: 
          w755.saldo = w755.saldo + segmentstat.kind2. 
          IF d-flag THEN w755.mon-saldo[DAY(segmentstat.datum)] 
            = w755.mon-saldo[DAY(segmentstat.datum)] + segmentstat.kind2.
        END. 
 
        IF ytd-flag THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.ytd-budget = w1.ytd-budget + segmentstat.budpersanz. 
          /*IF AVAILABLE w11 THEN 
          DO: 
            w11.ytd-saldo = w11.ytd-saldo + segmentstat.zimmeranz. 
            w11.ytd-budget = w11.ytd-budget + segmentstat.budzimmeranz. 
          END.*/  
          IF AVAILABLE w753 THEN 
            w753.ytd-saldo = w753.ytd-saldo + segmentstat.persanz.
          IF AVAILABLE w754 THEN 
            w754.ytd-saldo = w754.ytd-saldo + segmentstat.kind1.
          IF AVAILABLE w755 THEN 
            w755.ytd-saldo = w755.ytd-saldo + segmentstat.kind2.
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      FOR EACH segmentstat WHERE segmentstat.datum GE datum2 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF segmentstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo + segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.lytd-budget = w1.lytd-budget + segmentstat.budpersanz. 
          /*IF AVAILABLE w11 THEN 
          DO: 
            w11.lytd-saldo = w11.lytd-saldo + segmentstat.zimmeranz. 
            w11.lytd-budget = w11.lytd-budget + segmentstat.budzimmeranz. 
          END. */
          IF AVAILABLE w753 THEN 
            w753.lytd-saldo = w753.lytd-saldo + segmentstat.persanz. 
          IF AVAILABLE w754 THEN 
            w754.lytd-saldo = w754.lytd-saldo + segmentstat.kind1.
          IF AVAILABLE w755 THEN 
            w755.lytd-saldo = w755.lytd-saldo + segmentstat.kind2. 
        END. 
        ELSE 
        DO:
          dlmtd-flag = (MONTH(segmentstat.datum) = MONTH(to-date)) 
            AND (YEAR(segmentstat.datum) = YEAR(to-date) - 1).
          IF dlmtd-flag THEN w1.mon-lmtd[DAY(segmentstat.datum)] 
            = w1.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.persanz
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis.
          w1.lastyr = w1.lastyr + segmentstat.persanz /* LAST year MTD */ 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
          w1.ly-budget = w1.ly-budget + segmentstat.budpersanz. 
          /*IF AVAILABLE w11 THEN 
          DO: 
            IF dlmtd-flag THEN w11.mon-lmtd[DAY(segmentstat.datum)] 
              = w11.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.zimmeranz.
            w11.lastyr = w11.lastyr + segmentstat.zimmeranz. 
            w11.ly-budget = w11.ly-budget + segmentstat.budzimmeranz. 
          END. */
          IF AVAILABLE w753 THEN 
          DO: 
            IF dlmtd-flag THEN w753.mon-lmtd[DAY(segmentstat.datum)] 
              = w753.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.persanz. 
            w753.lastyr = w753.lastyr + segmentstat.persanz. 
          END. 
          IF AVAILABLE w754 THEN 
          DO: 
            IF dlmtd-flag THEN w754.mon-lmtd[DAY(segmentstat.datum)] 
              = w754.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.kind1.
            w754.lastyr = w754.lastyr + segmentstat.kind1. 
          END. 
          IF AVAILABLE w755 THEN 
          DO: 
            IF dlmtd-flag THEN w755.mon-lmtd[DAY(segmentstat.datum)] 
              = w755.mon-lmtd[DAY(segmentstat.datum)] + segmentstat.kind2.
            w755.lastyr = w755.lastyr + segmentstat.kind2. 
          END. 
 
          IF lytd-flag THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + segmentstat.persanz 
              + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
            w1.lytd-budget = w1.lytd-budget + segmentstat.budpersanz. 
            /*IF AVAILABLE w11 THEN 
            DO: 
              w11.lytd-saldo = w11.lytd-saldo + segmentstat.zimmeranz. 
              w11.lytd-budget = w11.lytd-budget + segmentstat.budzimmeranz. 
            END. */
            IF AVAILABLE w753 THEN 
              w753.lytd-saldo = w753.lytd-saldo + segmentstat.persanz. 
            IF AVAILABLE w754 THEN 
              w754.lytd-saldo = w754.lytd-saldo + segmentstat.kind1.
            IF AVAILABLE w755 THEN 
              w755.lytd-saldo = w755.lytd-saldo + segmentstat.kind2. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH segmentstat WHERE segmentstat.datum GE Pfrom-date 
      AND segmentstat.datum LE Pto-date 
      AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(segmentstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lastmon = w1.lastmon + segmentstat.persanz 
        + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
      w1.lm-budget = w1.lm-budget + segmentstat.budpersanz. 
      /*IF AVAILABLE w11 THEN 
      DO: 
        w11.lastmon = w11.lastmon + segmentstat.zimmeranz. 
        w11.lm-budget = w11.lm-budget + segmentstat.budzimmeranz. 
      END.*/ 
      IF AVAILABLE w753 THEN 
         w753.lastmon = w753.lastmon + segmentstat.persanz. 
      IF AVAILABLE w754 THEN 
        w754.lastmon = w754.lastmon + segmentstat.kind1. 
      IF AVAILABLE w755 THEN 
        w755.lastmon = w755.lastmon + segmentstat.kind2. 
    END. 
    IF lytoday-flag THEN 
    DO:
      FIND FIRST segmentstat WHERE segmentstat.datum EQ lytoday
        AND segmentstat.segmentcode = segment.segmentcode NO-LOCK NO-ERROR.
      IF AVAILABLE segmentstat THEN
      DO:
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        w1.lytoday = w1.lytoday + segmentstat.persanz 
          + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
        /*IF AVAILABLE w11 THEN 
          w11.lytoday = w11.lytoday + segmentstat.zimmeranz. */
        IF AVAILABLE w753 THEN 
          w753.lytoday = w753.lytoday + segmentstat.persanz. 
        IF AVAILABLE w754 THEN 
          w754.lytoday = w754.lytoday + segmentstat.kind1. 
        IF AVAILABLE w755 THEN 
          w755.lytoday = w755.lytoday + segmentstat.kind2. 
      END. 
    END. 
  END. 
  w1.done = YES. 
  /*IF AVAILABLE w11 THEN w11.done = YES. */
  IF AVAILABLE w753 THEN w753.done = YES. 
  IF AVAILABLE w754 THEN w754.done = YES. 
  IF AVAILABLE w755 THEN w755.done = YES. 
END. 


PROCEDURE fill-avrgrate: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE BUFFER w11 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST w11 WHERE w11.main-code = 842 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. 
 
  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = "avrgrate" NO-LOCK: 
      IF zinrstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zinrstat.argtumsatz. 
        IF AVAILABLE w11 THEN w11.tday = w11.tday 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF ytd-flag THEN w11.ytd-saldo = w11.ytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = "avrgrate" NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr 
              + zinrstat.logisumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
            IF lytd-flag THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = "avrgrate" NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      IF AVAILABLE w11 THEN 
        w11.lastmon = w11.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz. 
    END. 
    IF lytoday-flag THEN 
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday
        AND zinrstat.zinr = "avrgrate" NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN
      DO:
        w1.lytoday = zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
          w11.lytoday = zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END.
    END.
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
END. 

PROCEDURE fill-avrgLrate: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE BUFFER w11 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST w11 WHERE w11.main-code = 46 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
      IF zinrstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zinrstat.argtumsatz. 
        IF AVAILABLE w11 THEN w11.tday = w11.tday 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF ytd-flag THEN w11.ytd-saldo = w11.ytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr 
              + zinrstat.logisumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
            IF lytd-flag THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      IF AVAILABLE w11 THEN 
        w11.lastmon = w11.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz. 
    END. 
    IF lytoday-flag THEN
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday 
        AND zinrstat.zinr = "avrgLrate" NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN
      DO:
        w1.lytoday = zinrstat.argtumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.lytoday = zinrstat.logisumsatz / zinrstat.zimmeranz. 
      END. 
    END.
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
END. 

PROCEDURE fill-avrglodge: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE BUFFER w11 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST w11 WHERE w11.main-code = 811 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. 
 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = "avrgrate" NO-LOCK: 
      IF zinrstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zinrstat.logisumsatz. 
        IF AVAILABLE w11 THEN w11.tday = w11.tday 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF ytd-flag THEN w11.ytd-saldo = w11.ytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = "avrgrate" NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr 
              + zinrstat.argtumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
            IF lytd-flag THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = "avrgrate" NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(zinrstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      w1.lastmon = w1.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      IF AVAILABLE w11 THEN 
        w11.lastmon = w11.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz. 
    END. 
    IF lytoday-flag THEN
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday 
        AND zinrstat.zinr = "avrgrate" NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN
      DO:
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(zinrstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        w1.lytoday = zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.lytoday = zinrstat.argtumsatz / zinrstat.zimmeranz. 
      END.
    END.
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
END. 

PROCEDURE fill-nation: 
DEFINE INPUT PARAMETER rec-w1  AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER. 
DEFINE VARIABLE mm             AS INTEGER.
DEFINE VARIABLE natnr           AS INTEGER. 
DEFINE VARIABLE datum1         AS DATE. 
DEFINE VARIABLE curr-date      AS DATE. 
DEFINE VARIABLE ly-currdate    AS DATE.
DEFINE VARIABLE ny-currdate    AS DATE.
DEFINE VARIABLE njan1          AS DATE.
DEFINE VARIABLE nmth1          AS DATE.
DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE dbudget-flag   AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.

FIND FIRST w1 WHERE RECID(w1) = rec-w1.
natnr = w1.artnr.

  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    mm = MONTH(to-date).
    /*saldo*/

    FOR EACH genstat WHERE genstat.resident = natnr 
      AND genstat.datum GE datum1 
      AND genstat.datum LE to-date 
      AND genstat.resstatus NE 13 
      /*AND genstat.gratis EQ 0 */
      AND genstat.segmentcode NE 0 
      AND genstat.resident NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES NO-LOCK:

      frate = 1.
      
      d-flag = (MONTH(genstat.datum) = MONTH(to-date))
                AND (YEAR(genstat.datum) = YEAR(to-date)).

      IF genstat.datum = to-date THEN
      DO:
        IF main-nr = 8814 THEN
          w1.tday = w1.tday + genstat.erwachs + 
                    genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 8813 THEN
          w1.tday = w1.tday + 1.
        IF main-nr = 8092 THEN
          w1.tday = w1.tday + genstat.logis.
      END.
      
      IF MONTH(genstat.datum) = mm THEN
      DO:
        IF main-nr = 8814 THEN
        DO:
          IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + genstat.erwachs + 
                genstat.kind1 + genstat.kind2 + genstat.gratis.
          w1.saldo = w1.saldo + genstat.erwachs + 
                     genstat.kind1 + genstat.kind2 + genstat.gratis.
        END.
        IF main-nr = 8813 THEN
        DO:
          w1.saldo = w1.saldo + 1.
          IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + 1.
        END.
        IF main-nr = 8092 THEN
        DO:
          w1.saldo = w1.saldo + genstat.logis.
          IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + genstat.logis.
        END.
      END.
      

      IF main-nr = 8814 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.erwachs + 
                   genstat.kind1 + genstat.kind2 + genstat.gratis.
      IF main-nr = 8813 THEN
        w1.ytd-saldo = w1.ytd-saldo + 1.
      IF main-nr = 8092 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.logis.
    END.
    
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date.
      mm = MONTH(Lto-date).
      FOR EACH genstat WHERE genstat.resident = natnr 
        AND genstat.datum GE datum1 
        AND genstat.datum LE Lto-date 
        AND genstat.resstatus NE 13 
        /*AND genstat.gratis EQ 0 */
        AND genstat.segmentcode NE 0 
        AND genstat.resident NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES NO-LOCK:

        dlmtd-flag = (MONTH(genstat.datum) = MONTH(Lto-date)) 
                     AND (YEAR(genstat.datum) = YEAR(Lto-date)).

        IF genstat.datum = Lto-date THEN
        DO:
          IF main-nr = 8814 THEN
            w1.lytoday = w1.lytoday + genstat.erwachs + 
                         genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 8813 THEN
            w1.lytoday = w1.lytoday + 1.
          IF main-nr = 8092 THEN
            w1.lytoday = w1.lytoday + genstat.logis.
        END.

        IF MONTH(genstat.datum) = mm THEN
        DO:
          IF main-nr = 8814 THEN
            w1.lastyr = w1.lastyr + genstat.erwachs + 
                        genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 8813 THEN
            w1.lastyr = w1.lastyr + 1.
          IF main-nr = 8092 THEN
            w1.lastyr = w1.lastyr + genstat.logis.
        END.

        IF main-nr = 8814 THEN
          w1.lytd-saldo = w1.lytd-saldo + genstat.erwachs + 
                          genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 8813 THEN
          w1.lytd-saldo = w1.lytd-saldo + 1.
        IF main-nr = 8092 THEN
          w1.lytd-saldo = w1.lytd-saldo + genstat.logis.
      END.
    END.
  END. 
END. 

PROCEDURE fill-competitor: 
DEFINE INPUT PARAMETER rec-w1  AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER. 

DEFINE VARIABLE mm             AS INTEGER.
DEFINE VARIABLE compnr         AS INTEGER. 
DEFINE VARIABLE datum1         AS DATE. 
DEFINE VARIABLE curr-date      AS DATE. 
DEFINE VARIABLE ly-currdate    AS DATE.
DEFINE VARIABLE ny-currdate    AS DATE.
DEFINE VARIABLE njan1          AS DATE.
DEFINE VARIABLE nmth1          AS DATE.
DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE dbudget-flag   AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.

FIND FIRST w1 WHERE RECID(w1) = rec-w1.
compnr = w1.artnr.

  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    mm = MONTH(to-date).
    
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = "Competitor"
      AND zinrstat.betriebsnr = compnr NO-LOCK:

      frate = 1.
      
      d-flag = (MONTH(zinrstat.datum) = MONTH(to-date))
                AND (YEAR(zinrstat.datum) = YEAR(to-date)).

      IF zinrstat.datum = to-date THEN
      DO:
        IF main-nr = 9981 THEN
          w1.tday = w1.tday + zinrstat.zimmeranz.
        IF main-nr = 9982 THEN
          w1.tday = w1.tday + zinrstat.personen.
        IF main-nr = 9983 THEN
          w1.tday = w1.tday + INT(zinrstat.argtumsatz).
        IF main-nr = 9984 THEN
          w1.tday = w1.tday + zinrstat.logisumsatz.
      END.
      
      IF MONTH(zinrstat.datum) = mm THEN
      DO:
        IF main-nr = 9981 THEN
        DO:
          w1.saldo = w1.saldo + zinrstat.zimmeranz.
          IF d-flag THEN 
            w1.mon-saldo[DAY(zinrstat.datum)] 
              = w1.mon-saldo[DAY(zinrstat.datum)] + zinrstat.zimmeranz.
        END.
        ELSE IF main-nr = 9982 THEN
        DO:
          w1.saldo = w1.saldo + zinrstat.personen.
          IF d-flag THEN 
            w1.mon-saldo[DAY(zinrstat.datum)] 
              = w1.mon-saldo[DAY(zinrstat.datum)] + zinrstat.personen.
        END.
        ELSE IF main-nr = 9983 THEN
        DO:
          w1.saldo = w1.saldo + INT(zinrstat.argtumsatz).
          IF d-flag THEN 
            w1.mon-saldo[DAY(zinrstat.datum)] 
              = w1.mon-saldo[DAY(zinrstat.datum)] + INT(zinrstat.argtumsatz).
        END.
        ELSE IF main-nr = 9984 THEN
        DO:
          w1.saldo = w1.saldo + zinrstat.logisumsatz.
          IF d-flag THEN 
            w1.mon-saldo[DAY(zinrstat.datum)] 
              = w1.mon-saldo[DAY(zinrstat.datum)] + zinrstat.logisumsatz.
        END.
      END.

      IF main-nr = 9981 THEN
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz.
      ELSE IF main-nr = 9982 THEN
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.personen.
      ELSE IF main-nr = 9983 THEN
        w1.ytd-saldo = w1.ytd-saldo + INT(zinrstat.argtumsatz).
      ELSE IF main-nr = 9984 THEN
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.logisumsatz.
    END.

    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date.
      mm = MONTH(Lto-date).

      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = "Competitor"
        AND zinrstat.betriebsnr = compnr NO-LOCK:

        dlmtd-flag = (MONTH(zinrstat.datum) = MONTH(Lto-date)) 
                     AND (YEAR(zinrstat.datum) = YEAR(Lto-date)).

        IF zinrstat.datum = Lto-date THEN
        DO:
          IF main-nr = 9981 THEN
          w1.lytoday = w1.lytoday + zinrstat.zimmeranz.
          IF main-nr = 9982 THEN
            w1.lytoday = w1.lytoday + zinrstat.personen.
          IF main-nr = 9983 THEN
            w1.lytoday = w1.lytoday + INT(zinrstat.argtumsatz).
          IF main-nr = 9984 THEN
            w1.lytoday = w1.lytoday + zinrstat.logisumsatz.
        END.

        IF MONTH(zinrstat.datum) = mm THEN
        DO:
          IF main-nr = 9981 THEN
            w1.lastyr = w1.lastyr + zinrstat.zimmeranz.
          IF main-nr = 9982 THEN
            w1.lastyr = w1.lastyr + zinrstat.personen.
          IF main-nr = 9983 THEN
            w1.lastyr = w1.lastyr + INT(zinrstat.argtumsatz).
          IF main-nr = 9984 THEN
            w1.lastyr = w1.lastyr + zinrstat.logisumsatz.
        END.

        IF main-nr = 9981 THEN
          w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz.
        ELSE IF main-nr = 9982 THEN
          w1.lytd-saldo = w1.lytd-saldo + zinrstat.personen.
        ELSE IF main-nr = 9983 THEN
          w1.lytd-saldo = w1.lytd-saldo + INT(zinrstat.argtumsatz).
        ELSE IF main-nr = 9984 THEN
          w1.lytd-saldo = w1.lytd-saldo + zinrstat.logisumsatz.
      END.
    END.
  END. 
END. 

/*PROCEDURE fill-segment: 
DEFINE INPUT PARAMETER rec-w1  AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER. 
DEFINE VARIABLE mm             AS INTEGER.
DEFINE VARIABLE segm           AS INTEGER. 
DEFINE VARIABLE datum1         AS DATE. 
DEFINE VARIABLE curr-date      AS DATE. 
DEFINE VARIABLE ly-currdate    AS DATE.
DEFINE VARIABLE ny-currdate    AS DATE.
DEFINE VARIABLE njan1          AS DATE.
DEFINE VARIABLE nmth1          AS DATE.
DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE dbudget-flag   AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.
DEFINE VARIABLE black-list    AS INTEGER NO-UNDO. 

DEFINE BUFFER segmbuffny FOR segmentstat.
IF MONTH(to-date) = 2 AND DAY(to-date) = 29 THEN
  ny-currdate = DATE(MONTH(to-date), 28, YEAR(to-date) + 1).
ELSE
  ny-currdate = DATE(MONTH(to-date), DAY(to-date), YEAR(to-date) + 1).

ASSIGN
  njan1 = DATE(1,1,YEAR(to-date) + 1)
  nmth1 = DATE(MONTH(to-date),1, YEAR(to-date) + 1).

FIND FIRST htparam WHERE paramnr = 709 NO-LOCK NO-ERROR. 
black-list = htparam.finteger. 

FIND FIRST w1 WHERE RECID(w1) = rec-w1.
segm = w1.artnr.

FIND FIRST segmbuffny WHERE segmbuffny.datum = ny-currdate 
        AND segmbuffny.segmentcode = segm NO-LOCK NO-ERROR.     
IF AVAILABLE segmbuffny THEN    
DO:
  IF main-nr = 92 THEN    
    w1.ny-budget = segmbuffny.budlogis.
  IF main-nr = 813 THEN
     w1.ny-budget = segmbuffny.budzimmeranz.
  IF main-nr = 814 THEN
     w1.ny-budget = segmbuffny.budpersanz.
END.

FOR EACH segmbuffny WHERE segmbuffny.datum GE njan1 AND 
  segmbuffny.datum LE ny-currdate AND 
  segmbuffny.segmentcode = segm NO-LOCK:
  IF main-nr = 92 THEN    
    w1.nytd-budget = w1.nytd-budget + segmbuffny.budlogis.
  IF main-nr = 813 THEN
    w1.nytd-budget = w1.nytd-budget + segmbuffny.budzimmeranz.
  IF main-nr = 814 THEN
    w1.nytd-budget = w1.nytd-budget + segmbuffny.budpersanz.
END.

FOR EACH segmbuffny WHERE segmbuffny.datum GE nmth1 AND 
  segmbuffny.datum LE ny-currdate AND 
  segmbuffny.segmentcode = segm NO-LOCK:
  IF main-nr = 92 THEN    
    w1.nmtd-budget = w1.nmtd-budget + segmbuffny.budlogis.
  IF main-nr = 813 THEN
    w1.nmtd-budget = w1.nmtd-budget + segmbuffny.budzimmeranz.
  IF main-nr = 814 THEN
    w1.nmtd-budget = w1.nmtd-budget + segmbuffny.budpersanz.
END.

/*yesterday*/
FIND FIRST segmentstat WHERE segmentstat.datum = to-date - 1 
  AND segmentstat.segmentcode = segm NO-LOCK NO-ERROR.     
IF AVAILABLE segmentstat THEN
DO:
  frate = 1.
  IF foreign-flag THEN 
  DO: 
    RUN find-exrate(segmentstat.datum). 
    IF AVAILABLE exrate THEN frate = exrate.betrag. 
  END. 
  IF main-nr = 92 THEN
    w1.yesterday = segmentstat.logis / frate. 
  ELSE IF main-nr = 813 THEN
    w1.yesterday = segmentstat.zimmeranz. 
  ELSE IF main-nr = 814 THEN
    w1.yesterday = segmentstat.persanz 
      + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
END.

/*last month today*/
IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
  OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
  OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
  w1.lm-today = 0.
ELSE
DO:
  IF MONTH(to-date) EQ 1 THEN
    curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
  ELSE
    curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
  FIND FIRST segmentstat WHERE segmentstat.datum = curr-date 
    AND segmentstat.segmentcode = segm NO-LOCK NO-ERROR.     
  IF AVAILABLE segmentstat THEN
  DO:
    frate = 1.
    IF foreign-flag THEN 
    DO: 
      RUN find-exrate(segmentstat.datum). 
      IF AVAILABLE exrate THEN frate = exrate.betrag. 
    END. 
    IF main-nr = 92 THEN
      w1.lm-today = segmentstat.logis / frate. 
    ELSE IF main-nr = 813 THEN
      w1.lm-today = segmentstat.zimmeranz. 
    ELSE IF main-nr = 814 THEN
      w1.lm-today = segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
  END.
END.

  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    mm = MONTH(to-date).
    /*saldo*/

    FOR EACH genstat WHERE genstat.segmentcode = segm 
      AND genstat.datum GE datum1 
      AND genstat.datum LE to-date 
      AND genstat.resstatus NE 13 
      /*AND genstat.gratis EQ 0 */
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES NO-LOCK:

      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(genstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 

      d-flag = (MONTH(genstat.datum) = MONTH(to-date))
                AND (YEAR(genstat.datum) = YEAR(to-date)).

      IF genstat.datum = to-date THEN
      DO:
        IF main-nr = 814 THEN
          w1.tday = w1.tday + genstat.erwachs + 
                    genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 813 THEN
          w1.tday = w1.tday + 1.
        IF main-nr = 92 THEN
          w1.tday = w1.tday + genstat.logis.
        IF main-nr = 756 THEN
            w1.tday = w1.tday + genstat.erwachs.
        ELSE IF main-nr = 757 THEN
            w1.tday = w1.tday + genstat.kind1.
        ELSE IF main-nr = 758 THEN
            w1.tday = w1.tday + genstat.kind2.
      END.
      
      IF MONTH(genstat.datum) = mm THEN
      DO:
        IF main-nr = 814 THEN
        DO:
          IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + genstat.erwachs + 
                genstat.kind1 + genstat.kind2 + genstat.gratis.
          /*w1.saldo = w1.saldo + genstat.erwachs + 
                     genstat.kind1 + genstat.kind2 + genstat.gratis.*/
        END.
        IF main-nr = 813 THEN
        DO:
          /*w1.saldo = w1.saldo + 1.*/
          IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + 1.
        END.
        IF main-nr = 92 THEN
        DO:
          w1.saldo = w1.saldo + genstat.logis.
          IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + genstat.logis.
        END.
        IF main-nr = 756 THEN
        DO:
            IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + genstat.erwachs.
            /*w1.saldo = w1.saldo + genstat.erwachs.*/
        END.
        ELSE IF main-nr = 757 THEN
        DO:
            IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + genstat.kind1.
            /*w1.saldo = w1.saldo + genstat.kind1.*/
        END.
        ELSE IF main-nr = 758 THEN
        DO:
            IF d-flag THEN 
            w1.mon-saldo[DAY(genstat.datum)] 
              = w1.mon-saldo[DAY(genstat.datum)] + genstat.kind2.
            /*w1.saldo = w1.saldo + genstat.kind2.*/
        END.
      END.
      
      /*MG Adjust with Desktop version FD2FC2*/
      IF genstat.datum GE from-date THEN
      DO:
        IF main-nr = 814 THEN
          w1.saldo = w1.saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 813 THEN
          w1.saldo = w1.saldo + 1.
        /*IF main-nr = 92 THEN
          w1.saldo = w1.saldo + genstat.logis.*/
        IF main-nr = 756 THEN
          w1.saldo = w1.saldo + genstat.erwachs.
        ELSE IF main-nr = 757 THEN
          w1.saldo = w1.saldo + genstat.kind1.
        ELSE IF main-nr = 758 THEN
          w1.saldo = w1.saldo + genstat.kind2.
      END.

      IF main-nr = 814 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.erwachs + 
                   genstat.kind1 + genstat.kind2 + genstat.gratis.
      IF main-nr = 813 THEN
        w1.ytd-saldo = w1.ytd-saldo + 1.
      IF main-nr = 92 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.logis.
      IF main-nr = 756 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.erwachs.
      ELSE IF main-nr = 757 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.kind1.
      ELSE IF main-nr = 758 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.kind2.
    END.
    
    /*budget*/
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segm NO-LOCK: 

      dbudget-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
      AND (YEAR(segmentstat.datum) = YEAR(to-date)).

      IF segmentstat.datum = to-date THEN
      DO:
        IF main-nr = 814 THEN
          w1.tbudget = w1.tbudget + segmentstat.budpersanz. 
        IF main-nr = 813 THEN
          w1.tbudget = w1.tbudget + segmentstat.budzimmeranz. 
        IF main-nr = 92 THEN
          w1.tbudget = w1.tbudget + segmentstat.budlogis.
      END.
      IF MONTH(segmentstat.datum) = mm THEN
      DO:
        IF main-nr = 814 THEN
        DO:
          IF dbudget-flag THEN 
            w1.mon-budget[DAY(segmentstat.datum)] 
              = w1.mon-budget[DAY(segmentstat.datum)] + segmentstat.budpersanz.
          w1.budget = w1.budget + segmentstat.budpersanz. 
        END.
          
        IF main-nr = 813 THEN
        DO:
          IF dbudget-flag THEN 
            w1.mon-budget[DAY(segmentstat.datum)] 
              = w1.mon-budget[DAY(segmentstat.datum)] + segmentstat.budzimmeranz.
          w1.budget = w1.budget + segmentstat.budzimmeranz. 
        END.
          
        IF main-nr = 92 THEN
        DO:
          IF dbudget-flag THEN 
            w1.mon-budget[DAY(segmentstat.datum)] 
              = w1.mon-budget[DAY(segmentstat.datum)] + segmentstat.budlogis.
          w1.budget = w1.budget + segmentstat.budlogis.
        END.
      END.

      IF main-nr = 814 THEN
        w1.ytd-budget = w1.ytd-budget + segmentstat.budpersanz. 
      IF main-nr = 813 THEN
        w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
      IF main-nr = 92 THEN
        w1.ytd-budget = w1.ytd-budget + segmentstat.budlogis.
    END.

    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date.
      mm = MONTH(Lto-date).
      FOR EACH genstat WHERE genstat.segmentcode = segm 
        AND genstat.datum GE datum1 
        AND genstat.datum LE Lto-date 
        AND genstat.resstatus NE 13 
        /*AND genstat.gratis EQ 0 */
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES NO-LOCK:

        frate = 1.
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(genstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 

        dlmtd-flag = (MONTH(genstat.datum) = MONTH(Lto-date)) 
                     AND (YEAR(genstat.datum) = YEAR(Lto-date)).

        IF genstat.datum = Lto-date THEN
        DO:
          IF main-nr = 814 THEN
            w1.lytoday = w1.lytoday + genstat.erwachs + 
                         genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 813 THEN
            w1.lytoday = w1.lytoday + 1.
          IF main-nr = 92 THEN
            w1.lytoday = w1.lytoday + genstat.logis.
        END.

        IF MONTH(genstat.datum) = mm THEN
        DO:
          IF main-nr = 814 THEN
            w1.lastyr = w1.lastyr + genstat.erwachs + 
                        genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 813 THEN
            w1.lastyr = w1.lastyr + 1.
          IF main-nr = 92 THEN
            w1.lastyr = w1.lastyr + genstat.logis.
        END.

        IF main-nr = 814 THEN
          w1.lytd-saldo = w1.lytd-saldo + genstat.erwachs + 
                          genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 813 THEN
          w1.lytd-saldo = w1.lytd-saldo + 1.
        IF main-nr = 92 THEN
          w1.lytd-saldo = w1.lytd-saldo + genstat.logis.
      END.
      /*last year budget*/
      FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segm NO-LOCK: 
        IF segmentstat.datum = to-date THEN
      
        IF MONTH(segmentstat.datum) = mm THEN
        DO:
          IF main-nr = 814 THEN
            w1.ly-budget = w1.ly-budget + segmentstat.budpersanz. 
          IF main-nr = 813 THEN
            w1.ly-budget = w1.ly-budget + segmentstat.budzimmeranz. 
          IF main-nr = 92 THEN
            w1.ly-budget = w1.ly-budget + segmentstat.budlogis.
        END.

        IF main-nr = 814 THEN
          w1.lytd-budget = w1.lytd-budget + segmentstat.budpersanz. 
        IF main-nr = 813 THEN
          w1.lytd-budget = w1.lytd-budget + segmentstat.budzimmeranz. 
        IF main-nr = 92 THEN
          w1.lytd-budget = w1.lytd-budget + segmentstat.budlogis.
      END.
    END.
    IF pmtd-flag THEN
    FOR EACH genstat WHERE genstat.segmentcode = segm 
      AND genstat.datum GE Pfrom-date
      AND genstat.datum LE Pto-date 
      AND genstat.resstatus NE 13 
      /*AND genstat.gratis EQ 0 */
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES NO-LOCK:
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(genstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF main-nr = 814 THEN
        w1.lastmon = w1.lastmon + genstat.erwachs + 
                     genstat.kind1 + genstat.kind2 + genstat.gratis.
      IF main-nr = 813 THEN
        w1.lastmon = w1.lastmon + 1.
      IF main-nr = 92 THEN
        w1.lastmon = w1.lastmon + genstat.logis.
    END.
  END. 
END.*/

PROCEDURE fill-segment: 
DEFINE INPUT PARAMETER rec-w1  AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER. 
DEFINE VARIABLE mm             AS INTEGER.
DEFINE VARIABLE segm           AS INTEGER. 
DEFINE VARIABLE datum1         AS DATE. 
DEFINE VARIABLE curr-date      AS DATE. 
DEFINE VARIABLE ly-currdate    AS DATE.
DEFINE VARIABLE ny-currdate    AS DATE.
DEFINE VARIABLE njan1          AS DATE.
DEFINE VARIABLE nmth1          AS DATE.
DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE dbudget-flag   AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.
 DEFINE VARIABLE black-list    AS INTEGER NO-UNDO. 

DEFINE BUFFER segmbuffny FOR segmentstat.
IF MONTH(to-date) = 2 AND DAY(to-date) = 29 THEN
  ny-currdate = DATE(MONTH(to-date), 28, YEAR(to-date) + 1).
ELSE
  ny-currdate = DATE(MONTH(to-date), DAY(to-date), YEAR(to-date) + 1).

ASSIGN
  njan1 = DATE(1,1,YEAR(to-date) + 1)
  nmth1 = DATE(MONTH(to-date),1, YEAR(to-date) + 1).

FIND FIRST htparam WHERE paramnr = 709 NO-LOCK NO-ERROR. 
black-list = htparam.finteger. 

FIND FIRST w1 WHERE RECID(w1) = rec-w1.
segm = w1.artnr.

FIND FIRST segmbuffny WHERE segmbuffny.datum = ny-currdate 
        AND segmbuffny.segmentcode = segm NO-LOCK NO-ERROR.     
IF AVAILABLE segmbuffny THEN    
DO:
  IF main-nr = 92 THEN    
    w1.ny-budget = segmbuffny.budlogis.
  IF main-nr = 813 THEN
     w1.ny-budget = segmbuffny.budzimmeranz.
  IF main-nr = 814 THEN
     w1.ny-budget = segmbuffny.budpersanz.
END.

FOR EACH segmbuffny WHERE segmbuffny.datum GE njan1 AND 
  segmbuffny.datum LE ny-currdate AND 
  segmbuffny.segmentcode = segm NO-LOCK:
  IF main-nr = 92 THEN    
    w1.nytd-budget = w1.nytd-budget + segmbuffny.budlogis.
  IF main-nr = 813 THEN
    w1.nytd-budget = w1.nytd-budget + segmbuffny.budzimmeranz.
  IF main-nr = 814 THEN
    w1.nytd-budget = w1.nytd-budget + segmbuffny.budpersanz.
END.

FOR EACH segmbuffny WHERE segmbuffny.datum GE nmth1 AND 
  segmbuffny.datum LE ny-currdate AND 
  segmbuffny.segmentcode = segm NO-LOCK:
  IF main-nr = 92 THEN    
    w1.nmtd-budget = w1.nmtd-budget + segmbuffny.budlogis.
  IF main-nr = 813 THEN
    w1.nmtd-budget = w1.nmtd-budget + segmbuffny.budzimmeranz.
  IF main-nr = 814 THEN
    w1.nmtd-budget = w1.nmtd-budget + segmbuffny.budpersanz.
END.

/*yesterday*/
FIND FIRST segmentstat WHERE segmentstat.datum = to-date - 1 
  AND segmentstat.segmentcode = segm NO-LOCK NO-ERROR.     
IF AVAILABLE segmentstat THEN
DO:
  frate = 1.
  IF foreign-flag THEN 
  DO: 
    RUN find-exrate(segmentstat.datum). 
    IF AVAILABLE exrate THEN frate = exrate.betrag. 
  END. 
  IF main-nr = 92 THEN
    w1.yesterday = segmentstat.logis / frate. 
  ELSE IF main-nr = 813 THEN
    w1.yesterday = segmentstat.zimmeranz. 
  ELSE IF main-nr = 814 THEN
    w1.yesterday = segmentstat.persanz 
      + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 

  IF main-nr = 9007 THEN DO: /*ITA 180917*/
      FIND FIRST zinrstat WHERE zinrstat.datum = segmbuffny.datum
          AND zinrstat.zinr = "SEGM" 
          AND zinrstat.betriebsnr = segmbuffny.segmentcode NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN ASSIGN w1.yesterday = zinrstat.logisumsatz / frate.
  END.
END.

/*last month today*/
IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
  OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
  OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
  w1.lm-today = 0.
ELSE
DO:
  IF MONTH(to-date) EQ 1 THEN
    curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
  ELSE
    curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
  FIND FIRST segmentstat WHERE segmentstat.datum = curr-date 
    AND segmentstat.segmentcode = segm NO-LOCK NO-ERROR.     
  IF AVAILABLE segmentstat THEN
  DO:
    frate = 1.
    IF foreign-flag THEN 
    DO: 
      RUN find-exrate(segmentstat.datum). 
      IF AVAILABLE exrate THEN frate = exrate.betrag. 
    END. 
    IF main-nr = 92 THEN
      w1.lm-today = segmentstat.logis / frate. 
    ELSE IF main-nr = 813 THEN
      w1.lm-today = segmentstat.zimmeranz. 
    ELSE IF main-nr = 814 THEN
      w1.lm-today = segmentstat.persanz 
            + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 

    IF main-nr = 9007 THEN DO: /*ITA 180917*/
          FIND FIRST zinrstat WHERE zinrstat.datum = segmbuffny.datum
              AND zinrstat.zinr = "SEGM" 
              AND zinrstat.betriebsnr = segmbuffny.segmentcode NO-LOCK NO-ERROR.
          IF AVAILABLE zinrstat THEN ASSIGN w1.lm-today = zinrstat.logisumsatz / frate.
     END.
  END.
END.

  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    mm = MONTH(to-date).
    /*saldo*/

    FOR EACH genstat WHERE genstat.segmentcode = segm 
      AND genstat.datum GE datum1 
      AND genstat.datum LE to-date 
      AND genstat.resstatus NE 13 
      /*AND genstat.gratis EQ 0 */
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES NO-LOCK:

      frate = 1.
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(genstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 

      d-flag = (MONTH(genstat.datum) = MONTH(to-date))
                AND (YEAR(genstat.datum) = YEAR(to-date)).

      IF genstat.datum = to-date THEN
      DO:
        IF main-nr = 814 THEN
          w1.tday = w1.tday + genstat.erwachs + 
                    genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 813 THEN
          w1.tday = w1.tday + 1.
        IF main-nr = 92 THEN
          w1.tday = w1.tday + genstat.logis.
        IF main-nr = 756 THEN
            w1.tday = w1.tday + genstat.erwachs.
        ELSE IF main-nr = 757 THEN
            w1.tday = w1.tday + genstat.kind1.
        ELSE IF main-nr = 758 THEN
            w1.tday = w1.tday + genstat.kind2.
      END.
      
      IF MONTH(genstat.datum) = mm THEN
      DO:
        IF main-nr = 814 AND d-flag THEN
          w1.mon-saldo[DAY(genstat.datum)] 
            = w1.mon-saldo[DAY(genstat.datum)] + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 813 AND d-flag THEN
          w1.mon-saldo[DAY(genstat.datum)] = w1.mon-saldo[DAY(genstat.datum)] + 1.
        IF main-nr = 92 AND d-flag THEN
          w1.mon-saldo[DAY(genstat.datum)] = w1.mon-saldo[DAY(genstat.datum)] + genstat.logis.
        IF main-nr = 756 AND d-flag THEN
          w1.mon-saldo[DAY(genstat.datum)] = w1.mon-saldo[DAY(genstat.datum)] + genstat.erwachs.
        ELSE IF main-nr = 757 AND d-flag THEN
          w1.mon-saldo[DAY(genstat.datum)] = w1.mon-saldo[DAY(genstat.datum)] + genstat.kind1.
        ELSE IF main-nr = 758 AND d-flag THEN
          w1.mon-saldo[DAY(genstat.datum)] = w1.mon-saldo[DAY(genstat.datum)] + genstat.kind2.
      END.

      IF genstat.datum GE from-date THEN
      DO:
        IF main-nr = 814 THEN
          w1.saldo = w1.saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 813 THEN
          w1.saldo = w1.saldo + 1.
        IF main-nr = 92 THEN
          w1.saldo = w1.saldo + genstat.logis.
        IF main-nr = 756 THEN
          w1.saldo = w1.saldo + genstat.erwachs.
        ELSE IF main-nr = 757 THEN
          w1.saldo = w1.saldo + genstat.kind1.
        ELSE IF main-nr = 758 THEN
          w1.saldo = w1.saldo + genstat.kind2.
      END.

      IF main-nr = 814 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.erwachs + 
                   genstat.kind1 + genstat.kind2 + genstat.gratis.
      IF main-nr = 813 THEN
        w1.ytd-saldo = w1.ytd-saldo + 1.
      IF main-nr = 92 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.logis.
      IF main-nr = 756 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.erwachs.
      ELSE IF main-nr = 757 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.kind1.
      ELSE IF main-nr = 758 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.kind2.
    END.

    /*ITA 180917 segment Other Revenue*/
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE to-date AND zinrstat.zinr = "SEGM"
        AND zinrstat.betriebsnr = segm NO-LOCK, 
        FIRST segment WHERE segment.segmentcode = zinrstat.betriebsnr 
        AND segment.segmentcode NE black-list AND segment.segmentgrup LE 99 
        NO-LOCK BY segment.segmentgrup BY segment.segmentcode:
         d-flag = (MONTH(zinrstat.datum) = MONTH(to-date))
                   AND (YEAR(zinrstat.datum) = YEAR(to-date)).
         frate = 1.
         IF foreign-flag THEN 
         DO: 
            RUN find-exrate(genstat.datum). 
            IF AVAILABLE exrate THEN frate = exrate.betrag. 
         END. 

         IF main-nr = 9007 THEN DO:
            IF zinrstat.datum = to-date THEN w1.tday = w1.tday + zinrstat.logisumsatz.
            IF MONTH(zinrstat.datum) = MONTH(to-date) AND d-flag THEN
                w1.mon-saldo[DAY(zinrstat.datum)] = w1.mon-saldo[DAY(zinrstat.datum)] + zinrstat.logisumsatz.
            IF zinrstat.datum GE from-date THEN w1.saldo = w1.saldo + zinrstat.logisumsatz.

            ASSIGN w1.ytd-saldo = w1.ytd-saldo + zinrstat.logisumsatz.
         END.
    END.
    /*end*/
    
    /*budget*/
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
      AND segmentstat.datum LE to-date 
      AND segmentstat.segmentcode = segm NO-LOCK: 

      dbudget-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
      AND (YEAR(segmentstat.datum) = YEAR(to-date)).

      IF segmentstat.datum = to-date THEN
      DO:
        IF main-nr = 814 THEN
          w1.tbudget = w1.tbudget + segmentstat.budpersanz. 
        IF main-nr = 813 THEN
          w1.tbudget = w1.tbudget + segmentstat.budzimmeranz. 
        IF main-nr = 92 THEN
          w1.tbudget = w1.tbudget + segmentstat.budlogis.
      END.

      IF MONTH(segmentstat.datum) = mm THEN
      DO:
        IF main-nr = 814 AND dbudget-flag THEN
          w1.mon-budget[DAY(segmentstat.datum)] 
            = w1.mon-budget[DAY(segmentstat.datum)] + segmentstat.budpersanz.
        IF main-nr = 813 AND dbudget-flag THEN
          w1.mon-budget[DAY(segmentstat.datum)] 
            = w1.mon-budget[DAY(segmentstat.datum)] + segmentstat.budzimmeranz.
        IF main-nr = 92 AND dbudget-flag THEN
          w1.mon-budget[DAY(segmentstat.datum)] 
            = w1.mon-budget[DAY(segmentstat.datum)] + segmentstat.budlogis.
      END.

      IF segmentstat.datum GE from-date THEN
      DO:
        IF main-nr = 814 THEN
          w1.budget = w1.budget + segmentstat.budpersanz. 
        IF main-nr = 813 THEN
          w1.budget = w1.budget + segmentstat.budzimmeranz. 
        IF main-nr = 92 THEN
          w1.budget = w1.budget + segmentstat.budlogis.
      END.

      IF main-nr = 814 THEN
        w1.ytd-budget = w1.ytd-budget + segmentstat.budpersanz. 
      IF main-nr = 813 THEN
        w1.ytd-budget = w1.ytd-budget + segmentstat.budzimmeranz. 
      IF main-nr = 92 THEN
        w1.ytd-budget = w1.ytd-budget + segmentstat.budlogis.
    END.

    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date.
      mm = MONTH(Lto-date).
        
      FOR EACH genstat WHERE genstat.segmentcode = segm 
        AND genstat.datum GE datum1 
        AND genstat.datum LE Lto-date 
        AND genstat.resstatus NE 13 
        /*AND genstat.gratis EQ 0 */
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES NO-LOCK:

        frate = 1.
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(genstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 

        dlmtd-flag = (MONTH(genstat.datum) = MONTH(Lto-date)) 
                     AND (YEAR(genstat.datum) = YEAR(Lto-date)).

        IF genstat.datum = Lto-date THEN
        DO:
          IF main-nr = 814 THEN
            w1.lytoday = w1.lytoday + genstat.erwachs + 
                         genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 813 THEN
            w1.lytoday = w1.lytoday + 1.
          IF main-nr = 92 THEN
            w1.lytoday = w1.lytoday + genstat.logis.
        END.

        IF MONTH(genstat.datum) = mm THEN
        DO:
          IF main-nr = 814 THEN
            w1.lastyr = w1.lastyr + genstat.erwachs + 
                        genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 813 THEN
            w1.lastyr = w1.lastyr + 1.
          IF main-nr = 92 THEN
            w1.lastyr = w1.lastyr + genstat.logis.
        END.

        IF main-nr = 814 THEN
          w1.lytd-saldo = w1.lytd-saldo + genstat.erwachs + 
                          genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 813 THEN
          w1.lytd-saldo = w1.lytd-saldo + 1.
        IF main-nr = 92 THEN
          w1.lytd-saldo = w1.lytd-saldo + genstat.logis.
      END.

      /*ITA 180917 Last Year segment Other Revenue*/
        FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
            AND zinrstat.datum LE Lto-date AND zinrstat.zinr = "SEGM"
            AND zinrstat.betriebsnr = segm NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = zinrstat.betriebsnr 
            AND segment.segmentcode NE black-list AND segment.segmentgrup LE 99 
            NO-LOCK BY segment.segmentgrup BY segment.segmentcode:
             frate = 1.
             IF foreign-flag THEN 
             DO: 
              RUN find-exrate(zinrstat.datum). 
              IF AVAILABLE exrate THEN frate = exrate.betrag. 
             END. 
    
             dlmtd-flag = (MONTH(zinrstat.datum) = MONTH(Lto-date)) 
                         AND (YEAR(zinrstat.datum) = YEAR(Lto-date)).

             IF main-nr = 9007 THEN DO:
                IF zinrstat.datum = Lto-date THEN w1.lytoday = w1.lytoday + zinrstat.logisumsatz.
                IF MONTH(zinrstat.datum) = mm THEN w1.lastyr = w1.lastyr + zinrstat.logisumsatz.
                ASSIGN w1.lytd-saldo = w1.lytd-saldo + zinrstat.logisumsatz.
             END.
        END.
      /*end*/

      /*last year budget*/
      FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
        AND segmentstat.datum LE Lto-date 
        AND segmentstat.segmentcode = segm NO-LOCK: 
        
        IF MONTH(segmentstat.datum) = mm THEN
        DO:
          IF main-nr = 814 THEN
            w1.ly-budget = w1.ly-budget + segmentstat.budpersanz. 
          IF main-nr = 813 THEN
            w1.ly-budget = w1.ly-budget + segmentstat.budzimmeranz. 
          IF main-nr = 92 THEN
            w1.ly-budget = w1.ly-budget + segmentstat.budlogis.
        END.

        IF main-nr = 814 THEN
          w1.lytd-budget = w1.lytd-budget + segmentstat.budpersanz. 
        IF main-nr = 813 THEN
          w1.lytd-budget = w1.lytd-budget + segmentstat.budzimmeranz. 
        IF main-nr = 92 THEN
          w1.lytd-budget = w1.lytd-budget + segmentstat.budlogis.
      END.
    END.
    
    IF pmtd-flag THEN DO:
        FOR EACH genstat WHERE genstat.segmentcode = segm 
          AND genstat.datum GE Pfrom-date
          AND genstat.datum LE Pto-date 
          AND genstat.resstatus NE 13 
          /*AND genstat.gratis EQ 0 */
          AND genstat.segmentcode NE 0 
          AND genstat.nationnr NE 0
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] EQ YES NO-LOCK:
          IF foreign-flag THEN 
          DO: 
            RUN find-exrate(genstat.datum). 
            IF AVAILABLE exrate THEN frate = exrate.betrag. 
          END. 
          IF main-nr = 814 THEN
            w1.lastmon = w1.lastmon + genstat.erwachs + 
                         genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 813 THEN
            w1.lastmon = w1.lastmon + 1.
          IF main-nr = 92 THEN
            w1.lastmon = w1.lastmon + genstat.logis.
        END.

        /*ITA 180917 Last month segment Other Revenue*/
        FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
            AND zinrstat.datum LE Pto-date AND zinrstat.zinr = "SEGM"
            AND zinrstat.betriebsnr = segm NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = zinrstat.betriebsnr 
            AND segment.segmentcode NE black-list AND segment.segmentgrup LE 99 
            NO-LOCK BY segment.segmentgrup BY segment.segmentcode:
             frate = 1.
             IF foreign-flag THEN 
             DO: 
              RUN find-exrate(genstat.datum). 
              IF AVAILABLE exrate THEN frate = exrate.betrag. 
             END. 
    
             IF main-nr = 9007 THEN w1.lastmon = w1.lastmon + zinrstat.logisumsatz.
        END.
      /*end*/

    END.
  END. 
END.

PROCEDURE fill-rmcatstat: 
DEFINE INPUT PARAMETER rec-w1   AS INTEGER. 
DEFINE INPUT PARAMETER main-nr  AS INTEGER. 
DEFINE VARIABLE zikatno         AS INTEGER. 
DEFINE VARIABLE datum1          AS DATE. 
 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    zikatno = w1.artnr. 

    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH zkstat WHERE zkstat.datum GE datum1 
      AND zkstat.datum LE to-date AND zkstat.zikatnr = zikatno NO-LOCK: 
      IF zkstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zkstat.zimmeranz
          - zkstat.betriebsnr + zkstat.arrangement-art[1].
      END. 
      IF zkstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo + zkstat.zimmeranz
          - zkstat.betriebsnr + zkstat.arrangement-art[1].
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zkstat.zimmeranz
          - zkstat.betriebsnr + zkstat.arrangement-art[1].
        IF ytd-flag THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + zkstat.zimmeranz 
            - zkstat.betriebsnr + zkstat.arrangement-art[1].
        END. 
      END. 
    END. 
    
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zkstat WHERE zkstat.datum GE datum1 
        AND zkstat.datum LE Lto-date AND zkstat.zikatnr = zikatno NO-LOCK: 
        IF zkstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo + zkstat.zimmeranz
            - zkstat.betriebsnr + zkstat.arrangement-art[1].
        END. 
        ELSE 
        DO: /* LAST year MTD */ 
          w1.lastyr = w1.lastyr + zkstat.zimmeranz
            - zkstat.betriebsnr + zkstat.arrangement-art[1].
          IF lytd-flag THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + zkstat.zimmeranz
              - zkstat.betriebsnr + zkstat.arrangement-art[1].
          END. 
        END. 
      END. 
    END.     
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zkstat WHERE zkstat.datum GE Pfrom-date AND zkstat.datum 
      LE Pto-date AND zkstat.zikatnr = zikatno NO-LOCK: 
      w1.lastmon = w1.lastmon + zkstat.zimmeranz
        - zkstat.betriebsnr + zkstat.arrangement-art[1].
    END.  
    IF lytoday-flag THEN  
    DO:
      FIND FIRST zkstat WHERE zkstat.datum EQ lytoday  
        AND zkstat.zikatnr = zikatno NO-LOCK NO-ERROR.
      IF AVAILABLE zkstat THEN w1.lytoday = zkstat.zimmeranz
        - zkstat.betriebsnr + zkstat.arrangement-art[1].
    END.  
    w1.done = YES. 
END. 



PROCEDURE fill-zinrstat: 
DEFINE INPUT PARAMETER rec-w1  AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER. 
DEFINE VARIABLE rmno   AS INTEGER. 
DEFINE VARIABLE mm     AS INTEGER.
DEFINE VARIABLE s-rmno AS CHAR. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE VARIABLE d-flag AS LOGICAL NO-UNDO.
DEFINE BUFFER w11 FOR w1. 
DEFINE BUFFER w12 FOR w1. 
DEFINE BUFFER w13 FOR w1. 
 
  IF main-nr = 800 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    ASSIGN
        rmno = w1.artnr. 
        s-rmno = w1.s-artnr.
    FIND FIRST w12 WHERE w12.main-code = 180 AND w12.artnr = rmno AND w12.s-artnr = s-rmno NO-ERROR. 
    FIND FIRST w13 WHERE w13.main-code = 181 AND w13.artnr = rmno AND w13.s-artnr = s-rmno NO-ERROR. 
  END. 
  ELSE IF main-nr = 180 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    ASSIGN
      rmno     = w1.artnr
      s-rmno = w1.s-artnr.
    FIND FIRST w11 WHERE w11.main-code = 800 AND w11.artnr = rmno AND w11.s-artnr = s-rmno NO-ERROR. 
    FIND FIRST w13 WHERE w13.main-code = 181 AND w13.artnr = rmno AND w13.s-artnr = s-rmno NO-ERROR. 
  END. 
  ELSE IF main-nr = 181 THEN 
  DO: 
    FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
    IF w1.done THEN RETURN. 
    ASSIGN
      rmno     = w1.artnr
      s-rmno = w1.s-artnr
    .
    FIND FIRST w11 WHERE w11.main-code = 800 AND w11.artnr = rmno AND w11.s-artnr = s-rmno NO-ERROR. 
    FIND FIRST w12 WHERE w12.main-code = 180 AND w12.artnr = rmno AND w12.s-artnr = s-rmno NO-ERROR. 
  END. 
 
  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = s-rmno NO-LOCK: 

      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(zinrstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 

      d-flag = (MONTH(zinrstat.datum) = MONTH(to-date))
                AND (YEAR(zinrstat.datum) = YEAR(to-date)).

      /*FD September 07, 2021 => Ticket No: 1D4AFA - Room Revenue Per Date*/
      IF d-flag THEN
      DO:
        IF main-nr = 800 THEN
        DO:
          w1.mon-saldo[DAY(zinrstat.datum)] = w1.mon-saldo[DAY(zinrstat.datum)] + zinrstat.logisumsatz / frate.
          IF AVAILABLE w12 THEN w12.mon-saldo[DAY(zinrstat.datum)] = w12.mon-saldo[DAY(zinrstat.datum)] + zinrstat.zimmeranz. 
          IF AVAILABLE w13 THEN w13.mon-saldo[DAY(zinrstat.datum)] = w13.mon-saldo[DAY(zinrstat.datum)] + zinrstat.personen.
        END.
        ELSE IF main-nr = 180 THEN
        DO:
          w1.mon-saldo[DAY(zinrstat.datum)] = w1.mon-saldo[DAY(zinrstat.datum)] + zinrstat.zimmeranz.
          IF AVAILABLE w11 THEN w11.mon-saldo[DAY(zinrstat.datum)] = w11.mon-saldo[DAY(zinrstat.datum)] + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w13 THEN w13.mon-saldo[DAY(zinrstat.datum)] = w13.mon-saldo[DAY(zinrstat.datum)] + zinrstat.personen.
        END.
        ELSE IF main-nr = 181 THEN
        DO:
          w1.mon-saldo[DAY(zinrstat.datum)] = w1.mon-saldo[DAY(zinrstat.datum)] + zinrstat.personen.
          IF AVAILABLE w11 THEN w11.mon-saldo[DAY(zinrstat.datum)] = w11.mon-saldo[DAY(zinrstat.datum)] + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN w12.mon-saldo[DAY(zinrstat.datum)] = w12.mon-saldo[DAY(zinrstat.datum)] + zinrstat.zimmeranz.
        END.
      END.

      IF zinrstat.datum = to-date THEN 
      DO: 
        IF main-nr = 800 THEN 
        DO: 
          w1.tday = w1.tday + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN w12.tday = w12.tday + zinrstat.zimmeranz. 
          IF AVAILABLE w13 THEN w13.tday = w13.tday + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 180 THEN 
        DO: 
          w1.tday = w1.tday + zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.tday = w11.tday + zinrstat.logisumsatz 
            / frate. 
          IF AVAILABLE w13 THEN w13.tday = w13.tday + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 181 THEN 
        DO: 
          w1.tday = w1.tday + zinrstat.personen. 
          IF AVAILABLE w11 THEN w11.tday = w11.tday + zinrstat.logisumsatz 
            / frate. 
          IF AVAILABLE w12 THEN w12.tday = w12.tday + zinrstat.zimmeranz. 
        END. 
      END. 
 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        IF main-nr = 800 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN 
            w12.ytd-saldo = w12.ytd-saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w13 THEN 
            w13.ytd-saldo = w13.ytd-saldo + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 180 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
            w11.ytd-saldo = w11.ytd-saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w13 THEN 
            w13.ytd-saldo = w13.ytd-saldo + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 181 THEN 
        DO: 
          w1.ytd-saldo = w1.ytd-saldo + zinrstat.personen. 
          IF AVAILABLE w11 THEN 
            w11.ytd-saldo = w11.ytd-saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN 
            w12.ytd-saldo = w12.ytd-saldo + zinrstat.zimmeranz. 
        END. 
      END. 
      ELSE 
      DO: 
        IF main-nr = 800 THEN 
        DO: 
          w1.saldo = w1.saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN 
            w12.saldo = w12.saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w13 THEN 
            w13.saldo = w13.saldo + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 180 THEN 
        DO: 
          w1.saldo = w1.saldo + zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
            w11.saldo = w11.saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w13 THEN 
            w13.saldo = w13.saldo + zinrstat.personen. 
        END. 
        ELSE IF main-nr = 181 THEN 
        DO: 
          w1.saldo = w1.saldo + zinrstat.personen. 
          IF AVAILABLE w11 THEN 
            w11.saldo = w11.saldo + zinrstat.logisumsatz / frate. 
          IF AVAILABLE w12 THEN 
            w12.saldo = w12.saldo + zinrstat.zimmeranz. 
        END. 
 
        IF ytd-flag THEN 
        DO: 
          IF main-nr = 800 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.ytd-saldo = w12.ytd-saldo + zinrstat.zimmeranz. 
            IF AVAILABLE w13 THEN 
              w13.ytd-saldo = w13.ytd-saldo + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 180 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
            IF AVAILABLE w11 THEN 
              w11.ytd-saldo = w11.ytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w13 THEN 
              w13.ytd-saldo = w13.ytd-saldo + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 181 THEN 
          DO: 
            w1.ytd-saldo = w1.ytd-saldo + zinrstat.personen. 
            IF AVAILABLE w11 THEN 
              w11.ytd-saldo = w11.ytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.ytd-saldo = w12.ytd-saldo + zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = s-rmno NO-LOCK: 
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(zinrstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          IF main-nr = 800 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.lytd-saldo = w12.lytd-saldo + zinrstat.zimmeranz. 
            IF AVAILABLE w13 THEN 
              w13.lytd-saldo = w13.lytd-saldo + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 180 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
            IF AVAILABLE w11 THEN 
              w11.lytd-saldo = w11.lytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w13 THEN 
              w13.lytd-saldo = w13.lytd-saldo + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 181 THEN 
          DO: 
            w1.lytd-saldo = w1.lytd-saldo + zinrstat.personen. 
            IF AVAILABLE w11 THEN 
              w11.lytd-saldo = w11.lytd-saldo + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.lytd-saldo = w12.lytd-saldo + zinrstat.zimmeranz. 
          END. 
        END. 
        ELSE 
        DO: /* LAST year MTD */ 
          IF main-nr = 800 THEN 
          DO: 
            w1.lastyr = w1.lastyr + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.lastyr = w12.lastyr + zinrstat.zimmeranz. 
            IF AVAILABLE w13 THEN 
              w13.lastyr = w13.lastyr + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 180 THEN 
          DO: 
            w1.lastyr = w1.lastyr + zinrstat.zimmeranz. 
            IF AVAILABLE w11 THEN 
              w11.lastyr = w11.lastyr + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w13 THEN 
              w13.lastyr = w13.lastyr + zinrstat.personen. 
          END. 
          ELSE IF main-nr = 181 THEN 
          DO: 
            w1.lastyr = w1.lastyr + zinrstat.personen. 
            IF AVAILABLE w11 THEN 
              w11.lastyr = w11.lastyr + zinrstat.logisumsatz / frate. 
            IF AVAILABLE w12 THEN 
              w12.lastyr = w12.lastyr + zinrstat.zimmeranz. 
          END. 
 
          IF lytd-flag THEN 
          DO: 
            IF main-nr = 800 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + zinrstat.logisumsatz / frate. 
              IF AVAILABLE w12 THEN 
                w12.lytd-saldo = w12.lytd-saldo + zinrstat.zimmeranz. 
              IF AVAILABLE w13 THEN 
                w13.lytd-saldo = w13.lytd-saldo + zinrstat.personen. 
            END. 
            ELSE IF main-nr = 180 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
              IF AVAILABLE w11 THEN 
                w11.lytd-saldo = w11.lytd-saldo + zinrstat.logisumsatz / frate. 
              IF AVAILABLE w13 THEN 
                w13.lytd-saldo = w13.lytd-saldo + zinrstat.personen. 
            END. 
            ELSE IF main-nr = 181 THEN 
            DO: 
              w1.lytd-saldo = w1.lytd-saldo + zinrstat.personen. 
              IF AVAILABLE w11 THEN 
                w11.lytd-saldo = w11.lytd-saldo + zinrstat.logisumsatz / frate. 
              IF AVAILABLE w12 THEN 
                w12.lytd-saldo = w12.lytd-saldo + zinrstat.zimmeranz. 
            END. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = s-rmno NO-LOCK: 
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(zinrstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF main-nr = 800 THEN 
      DO: 
        w1.lastmon = w1.lastmon + zinrstat.logisumsatz / frate. 
        IF AVAILABLE w12 THEN 
          w12.lastmon = w12.lastmon + zinrstat.zimmeranz. 
        IF AVAILABLE w13 THEN 
          w13.lastmon = w13.lastmon + zinrstat.personen. 
      END. 
      ELSE IF main-nr = 180 THEN 
      DO: 
        w1.lastmon = w1.lastmon + zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
          w11.lastmon = w11.lastmon + zinrstat.logisumsatz / frate. 
        IF AVAILABLE w13 THEN 
          w13.lastmon = w13.lastmon + zinrstat.personen. 
      END. 
      ELSE IF main-nr = 181 THEN 
      DO: 
        w1.lastmon = w1.lastmon + zinrstat.personen. 
        IF AVAILABLE w11 THEN 
          w11.lastmon = w11.lastmon + zinrstat.logisumsatz / frate. 
        IF AVAILABLE w12 THEN 
          w12.lastmon = w12.lastmon + zinrstat.zimmeranz. 
      END. 
    END. 
    IF lytoday-flag THEN 
    FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday 
      AND zinrstat.zinr = s-rmno NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN
    DO:
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(zinrstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF main-nr = 800 THEN 
      DO: 
        w1.lytoday = zinrstat.logisumsatz / frate. 
        IF AVAILABLE w12 THEN w12.lytoday = zinrstat.zimmeranz. 
        IF AVAILABLE w13 THEN w13.lytoday = zinrstat.personen. 
      END. 
      ELSE IF main-nr = 180 THEN 
      DO: 
        w1.lytoday = zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.lytoday = zinrstat.logisumsatz / frate. 
        IF AVAILABLE w13 THEN w13.lytoday = zinrstat.personen. 
      END. 
      ELSE IF main-nr = 181 THEN 
      DO: 
        w1.lytoday = zinrstat.personen. 
        IF AVAILABLE w11 THEN w11.lytoday = zinrstat.logisumsatz / frate. 
        IF AVAILABLE w12 THEN w12.lytoday = zinrstat.zimmeranz. 
      END. 
    END. 
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
  IF AVAILABLE w12 THEN w12.done = YES. 
  IF AVAILABLE w13 THEN w13.done = YES. 
END. 

PROCEDURE find-exrate: 
DEFINE INPUT PARAMETER curr-date AS DATE NO-UNDO. 
  IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
    AND exrate.datum = curr-date NO-LOCK NO-ERROR. 
  ELSE FIND FIRST exrate WHERE exrate.datum = curr-date NO-LOCK NO-ERROR. 
END. 

PROCEDURE cal-fbcost: 
  DEFINE INPUT PARAMETER artnr AS INTEGER. 
  DEFINE INPUT PARAMETER dept AS INTEGER. 
  DEFINE INPUT PARAMETER datum AS DATE. 
  DEFINE OUTPUT PARAMETER cost AS DECIMAL INITIAL 0. 
  FIND FIRST h-cost WHERE h-cost.artnr = artnr 
    AND h-cost.departement = dept AND h-cost.datum = datum 
    AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
    cost = h-cost.anzahl * h-cost.betrag. 
  ELSE 
  DO: 
    FOR EACH h-journal WHERE h-journal.artnr = artnr 
      AND h-journal.departement = dept 
      AND h-journal.bill-datum EQ datum NO-LOCK: 
      cost = cost + h-journal.betrag * h-artikel.prozent / 100. 
    END. 
  END. 
END. 

PROCEDURE fill-wig:
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1        AS DATE. 
DEFINE VARIABLE curr-date     AS DATE. 
DEFINE VARIABLE wig-gastnr    AS INT.
DEFINE VARIABLE d-flag        AS LOGICAL.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
  
  FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK. 
  wig-gastnr = htparam.fint.

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH genstat WHERE genstat.datum GE datum1
      AND genstat.datum LE to-date 
      AND genstat.gastnrmember GT 0
      AND genstat.gastnr = wig-gastnr
      AND genstat.zinr NE "" 
      AND genstat.resstatus NE 13 NO-LOCK USE-INDEX gastnrmember_ix
      BY genstat.datum:
      d-flag = (MONTH(genstat.datum) = MONTH(to-date)) AND (YEAR(genstat.datum) = YEAR(to-date)).
      IF d-flag THEN
        w1.mon-saldo[DAY(genstat.datum)] = w1.mon-saldo[DAY(genstat.datum)] + 1.
      IF genstat.datum = to-date THEN
        w1.tday = w1.tday + 1.
      IF genstat.datum LT from-date THEN
        w1.ytd-saldo = w1.ytd-saldo + 1.
      ELSE
      DO:
        w1.saldo = w1.saldo + 1.
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + 1.
      END.
    END.
  END.
END.

PROCEDURE fill-new-wig:
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1        AS DATE. 
DEFINE VARIABLE curr-date     AS DATE. 
DEFINE VARIABLE wig-gastnr    AS INT.
DEFINE VARIABLE ci-date       AS DATE.
DEFINE VARIABLE datum         AS DATE.
DEFINE VARIABLE walk-in       AS INTEGER.
DEFINE VARIABLE wi-grp        AS INTEGER.
DEFINE VARIABLE d-flag        AS LOGICAL.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
  ci-date = htparam.fdate.
  
  FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK. 
  wig-gastnr = htparam.fint.

  FIND FIRST htparam WHERE paramnr = 48 NO-LOCK. 
  FIND FIRST segment WHERE segment.segmentcode = htparam.finteger 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE segment THEN 
  DO:
    ASSIGN
     walk-in = htparam.finteger
     wi-grp  = segment.segmentgrup
     .  
  END.

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 

  DO datum = datum1 TO to-date:
    IF datum GE ci-date THEN
    DO:
      FOR EACH res-line WHERE res-line.active-flag = 1 AND 
          res-line.resstatus NE 12 NO-LOCK BY res-line.zinr: 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
          NO-LOCK.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
          NO-LOCK.
        IF segment.segmentcode = walk-in AND segment.segmentgrup NE 0 THEN
        DO: 
          d-flag = (MONTH(datum) = MONTH(to-date)) AND (YEAR(datum) = YEAR(to-date)).
          IF d-flag THEN
            w1.mon-saldo[DAY(datum)] = w1.mon-saldo[DAY(datum)] + res-line.zimmeranz.
          
          IF datum = to-date THEN w1.tday = w1.tday + res-line.zimmeranz.
          IF datum GE DATE(MONTH(to-date), 1, YEAR(to-date)) THEN w1.saldo = w1.saldo + res-line.zimmeranz.
          IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + res-line.zimmeranz.
        END.
      END.  
    END.
    ELSE IF datum LT ci-date THEN
    DO:
      FOR EACH genstat WHERE genstat.datum EQ datum
        AND genstat.gastnrmember GT 0
        AND genstat.zinr NE "" 
        AND genstat.resstatus NE 13 NO-LOCK USE-INDEX gastnrmember_ix, 
        FIRST zinrstat WHERE zinrstat.datum = genstat.datum 
            AND zinrstat.zinr = genstat.zinr NO-LOCK :

        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
          NO-LOCK.
        IF AVAILABLE segment THEN
        DO:
           IF segment.segmentcode = walk-in THEN 
           DO:
             d-flag = (MONTH(genstat.datum) = MONTH(to-date)) AND (YEAR(genstat.datum) = YEAR(to-date)).
             IF d-flag THEN w1.mon-saldo[DAY(genstat.datum)] = w1.mon-saldo[DAY(genstat.datum)] + 1.

             IF genstat.datum = to-date THEN w1.tday = w1.tday + 1.
             IF datum GE DATE(MONTH(to-date), 1, YEAR(to-date)) THEN w1.saldo = w1.saldo + 1.
             IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + 1.
           END.
        END.
      END.
    END.
  END.
  END.

PROCEDURE fill-cover-shift1:
    DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
    DEFINE VARIABLE datum1        AS DATE. 
    DEFINE VARIABLE curr-date     AS DATE. 
    DEFINE VARIABLE curr-i        AS INT. 
    DEFINE VARIABLE curr-rechnr   AS INTEGER.
    DEFINE VARIABLE billnr        AS INTEGER.
    DEFINE VARIABLE i             AS INTEGER.
    DEFINE VARIABLE found         AS LOGICAL.
    DEFINE BUFFER hbuff FOR h-umsatz.
    
      FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
      IF ytd-flag THEN datum1 = jan1. 
      ELSE datum1 = from-date. 

      FOR EACH h-bill-line WHERE h-bill-line.bill-datum GE datum1
          AND h-bill-line.bill-datum LE to-date
          AND h-bill-line.departement = w1.dept NO-LOCK BY h-bill-line.rechnr
          BY h-bill-line.sysdate DESC BY h-bill-line.zeit: 
           
          IF h-bill-line.artnr NE 0 THEN DO: 
              FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
                      AND h-artikel.departement = h-bill-line.departement
                      AND h-artikel.artart GT 0 NO-LOCK NO-ERROR.
              IF AVAILABLE h-artikel THEN DO:
                  IF curr-rechnr NE h-bill-line.rechnr THEN DO:
                      FIND FIRST h-bill WHERE h-bill.rechnr = h-bill-line.rechnr 
                          AND h-bill.departement = h-bill-line.departement NO-LOCK NO-ERROR.
                      IF AVAILABLE h-bill THEN DO:
                           
                          IF h-bill-line.bill-datum = to-date THEN DO:
                              IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2013 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2014 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2015 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2016 THEN w1.tday = w1.tday + h-bill.belegung. 
                          END.
                          ELSE IF h-bill-line.bill-datum GE from-date THEN DO:
                                  IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2013 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2014 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2015 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2016 THEN w1.saldo = w1.saldo + h-bill.belegung.                               
                          END.
    
                          IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2013 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2014 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2015 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2016 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                                                              
                      END.
                  END.
                  ASSIGN curr-rechnr = h-bill-line.rechnr.
              END.              
          END.
          ELSE IF h-bill-line.artnr = 0 THEN DO: 
                ASSIGN 
                  i      = 0 
                  found  = no
                  billnr = 0.  
                
               
                DO WHILE NOT found: 
                    i = i + 1. 
                    if substr(h-bill-line.bezeich, i, 1) = "*" then found = yes. 
                end. 
                billnr = INTEGER(SUBSTR(h-bill-line.bezeich, i + 1, LENGTH(h-bill-line.bezeich) - i)).
                                                          
                IF billnr NE 0 THEN DO:
                   FIND FIRST bill WHERE bill.rechnr = billnr NO-LOCK NO-ERROR. 
                   IF AVAILABLE bill AND bill.zinr NE " " THEN DO: 
                       FIND FIRST h-bill WHERE h-bill.rechnr = h-bill-line.rechnr 
                          AND h-bill.departement = h-bill-line.departement NO-LOCK NO-ERROR.
                      IF AVAILABLE h-bill THEN DO:
                          IF h-bill-line.bill-datum = to-date THEN DO:
                              IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2009 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2010 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2011 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2012 THEN w1.tday = w1.tday + h-bill.belegung. 
                          END.
                          ELSE IF h-bill-line.bill-datum GE from-date THEN DO:
                                  IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2009 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2010 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2011 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2012 THEN w1.saldo = w1.saldo + h-bill.belegung.                               
                          END.
    
                          IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2009 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2010 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2011 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2012 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                      END.
                   END.
               END.
          END.          
      END.
END.

PROCEDURE fill-cover-shift2:
    DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
    DEFINE VARIABLE datum1        AS DATE. 
    DEFINE VARIABLE curr-date     AS DATE. 
    DEFINE VARIABLE curr-i        AS INT. 
    DEFINE VARIABLE curr-rechnr   AS INTEGER.
    DEFINE VARIABLE billnr        AS INTEGER.
    DEFINE VARIABLE i             AS INTEGER.
    DEFINE VARIABLE found         AS LOGICAL.
    DEFINE BUFFER hbuff FOR h-umsatz.
    
      FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
      IF ytd-flag THEN datum1 = jan1. 
      ELSE datum1 = from-date. 
        
       
      FOR EACH h-bill-line WHERE h-bill-line.bill-datum GE datum1
          AND h-bill-line.bill-datum LE to-date
          AND h-bill-line.departement = w1.dept NO-LOCK BY h-bill-line.rechnr
          BY h-bill-line.sysdate DESC BY h-bill-line.zeit: 
           
          IF h-bill-line.artnr NE 0 THEN DO: /*PW*/
              FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
                      AND h-artikel.departement = h-bill-line.departement
                      AND h-artikel.artart GT 0 
                      AND h-artikel.artart NE 11 
                      AND h-artikel.artart NE 12 NO-LOCK NO-ERROR.
              IF AVAILABLE h-artikel THEN DO:
                  IF curr-rechnr NE h-bill-line.rechnr THEN DO:
                      FIND FIRST h-bill WHERE h-bill.rechnr = h-bill-line.rechnr 
                          AND h-bill.departement = h-bill-line.departement NO-LOCK NO-ERROR.
                      IF AVAILABLE h-bill THEN DO:
                           
                          IF h-bill-line.bill-datum = to-date THEN DO:
                              IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2013 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2014 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2015 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2016 THEN w1.tday = w1.tday + h-bill.belegung. 
                          END.
                          ELSE IF h-bill-line.bill-datum GE from-date THEN DO:
                                  IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2013 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2014 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2015 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2016 THEN w1.saldo = w1.saldo + h-bill.belegung.                               
                          END.
    
                          IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2013 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2014 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2015 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2016 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                                                              
                      END.
                  END.
                  ASSIGN curr-rechnr = h-bill-line.rechnr.
              END.              
          END.
          ELSE IF h-bill-line.artnr = 0 THEN DO: /*PH*/
                ASSIGN 
                  i      = 0 
                  found  = no
                  billnr = 0.  
                
               
                DO WHILE NOT found: 
                    i = i + 1. 
                    if substr(h-bill-line.bezeich, i, 1) = "*" then found = yes. 
                end. 
                billnr = INTEGER(SUBSTR(h-bill-line.bezeich, i + 1, LENGTH(h-bill-line.bezeich) - i)).
                                                          
                IF billnr NE 0 THEN DO:
                   FIND FIRST bill WHERE bill.rechnr = billnr NO-LOCK NO-ERROR. 
                   IF AVAILABLE bill AND bill.zinr NE " " THEN DO: 
                       FIND FIRST h-bill WHERE h-bill.rechnr = h-bill-line.rechnr 
                          AND h-bill.departement = h-bill-line.departement NO-LOCK NO-ERROR.
                      IF AVAILABLE h-bill THEN DO:
                          IF h-bill-line.bill-datum = to-date THEN DO:
                              IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2009 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2010 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2011 THEN w1.tday = w1.tday + h-bill.belegung. 
                              IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2012 THEN w1.tday = w1.tday + h-bill.belegung. 
                          END.
                          ELSE IF h-bill-line.bill-datum GE from-date THEN DO:
                                  IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2009 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2010 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2011 THEN w1.saldo = w1.saldo + h-bill.belegung. 
                                  IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2012 THEN w1.saldo = w1.saldo + h-bill.belegung.                               
                          END.
    
                          IF h-bill-line.betriebsnr = 1 THEN IF w1.main-code = 2009 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 2 THEN IF w1.main-code = 2010 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 3 THEN IF w1.main-code = 2011 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                          IF h-bill-line.betriebsnr = 4 THEN IF w1.main-code = 2012 THEN w1.ytd-saldo = w1.ytd-saldo + h-bill.belegung. 
                      END.
                   END.
               END.
          END.          
      END.
END.

PROCEDURE fill-cover-shift:   /*FT 250113*/
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1        AS DATE. 
DEFINE VARIABLE curr-date     AS DATE. 
DEFINE VARIABLE curr-i        AS INT. 
DEFINE BUFFER hbuff FOR h-umsatz.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 AND h-umsatz.datum LE to-date 
    AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept NO-LOCK: 
    IF h-umsatz.epreis = 1 THEN
    DO:
      IF h-umsatz.datum = to-date THEN
      DO:
        IF w1.main-code = 1921 THEN w1.tday = h-umsatz.betrag.
        IF w1.main-code = 1971 THEN w1.tday = h-umsatz.nettobetrag. 
        IF w1.main-code = 1991 THEN w1.tday = h-umsatz.anzahl. 
      END.
      IF h-umsatz.datum GE from-date THEN 
      DO:
        IF w1.main-code = 1921 THEN w1.saldo = w1.saldo + h-umsatz.betrag. 
        IF w1.main-code = 1971 THEN w1.saldo = w1.saldo + h-umsatz.nettobetrag.
        IF w1.main-code = 1991 THEN w1.saldo = w1.saldo + h-umsatz.anzahl.
      END.
      IF w1.main-code = 1921 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.betrag.
      IF w1.main-code = 1971 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.nettobetrag. 
      IF w1.main-code = 1991 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.anzahl. 
    END.
    IF h-umsatz.epreis = 2 THEN
    DO:
      IF h-umsatz.datum = to-date THEN
      DO:
        IF w1.main-code = 1922 THEN w1.tday = h-umsatz.betrag.
        IF w1.main-code = 1972 THEN w1.tday = h-umsatz.nettobetrag. 
        IF w1.main-code = 1992 THEN w1.tday = h-umsatz.anzahl. 
      END.
      IF h-umsatz.datum GE from-date THEN 
      DO:
        IF w1.main-code = 1922 THEN w1.saldo = w1.saldo + h-umsatz.betrag. 
        IF w1.main-code = 1972 THEN w1.saldo = w1.saldo + h-umsatz.nettobetrag.
        IF w1.main-code = 1992 THEN w1.saldo = w1.saldo + h-umsatz.anzahl.
      END.
      IF w1.main-code = 1922 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.betrag.
      IF w1.main-code = 1972 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.nettobetrag. 
      IF w1.main-code = 1992 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.anzahl. 
    END.
    IF h-umsatz.epreis = 3 THEN
    DO:
      IF h-umsatz.datum = to-date THEN
      DO:
        IF w1.main-code = 1923 THEN w1.tday = h-umsatz.betrag.
        IF w1.main-code = 1973 THEN w1.tday = h-umsatz.nettobetrag. 
        IF w1.main-code = 1993 THEN w1.tday = h-umsatz.anzahl. 
      END.
      IF h-umsatz.datum GE from-date THEN 
      DO:
        IF w1.main-code = 1923 THEN w1.saldo = w1.saldo + h-umsatz.betrag. 
        IF w1.main-code = 1973 THEN w1.saldo = w1.saldo + h-umsatz.nettobetrag.
        IF w1.main-code = 1993 THEN w1.saldo = w1.saldo + h-umsatz.anzahl.
      END.
      IF w1.main-code = 1923 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.betrag.
      IF w1.main-code = 1973 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.nettobetrag. 
      IF w1.main-code = 1993 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.anzahl. 
    END.
    IF h-umsatz.epreis = 4 THEN
    DO:
      IF h-umsatz.datum = to-date THEN
      DO:
        IF w1.main-code = 1924 THEN w1.tday = h-umsatz.betrag.
        IF w1.main-code = 1974 THEN w1.tday = h-umsatz.nettobetrag. 
        IF w1.main-code = 1994 THEN w1.tday = h-umsatz.anzahl. 
      END.
      IF h-umsatz.datum GE from-date THEN 
      DO:
        IF w1.main-code = 1924 THEN w1.saldo = w1.saldo + h-umsatz.betrag. 
        IF w1.main-code = 1974 THEN w1.saldo = w1.saldo + h-umsatz.nettobetrag.
        IF w1.main-code = 1994 THEN w1.saldo = w1.saldo + h-umsatz.anzahl.
      END.
      IF w1.main-code = 1924 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.betrag.
      IF w1.main-code = 1974 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.nettobetrag. 
      IF w1.main-code = 1994 THEN w1.ytd-saldo = w1.ytd-saldo + h-umsatz.anzahl. 
    END.
  END.

  IF lytd-flag OR lmtd-flag THEN 
  DO:
    IF lytd-flag THEN datum1 = Ljan1. 
    ELSE datum1 = Lfrom-date. 
    FOR EACH h-umsatz WHERE h-umsatz.datum GE datum1 
      AND h-umsatz.datum LE Lto-date 
      AND h-umsatz.artnr = 0 AND h-umsatz.departement = w1.dept NO-LOCK: 
      IF h-umsatz.epreis = 1 THEN
      DO:
        IF h-umsatz.datum GE Lfrom-date THEN 
        DO:
          IF w1.main-code = 1921 THEN w1.lastyr = w1.lastyr + h-umsatz.betrag. 
          IF w1.main-code = 1971 THEN w1.lastyr = w1.lastyr + h-umsatz.nettobetrag.
          IF w1.main-code = 1991 THEN w1.lastyr = w1.lastyr + h-umsatz.anzahl.
        END.
        IF w1.main-code = 1921 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.betrag.
        IF w1.main-code = 1971 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.nettobetrag. 
        IF w1.main-code = 1991 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.anzahl. 
      END.
      IF h-umsatz.epreis = 2 THEN
      DO:
        IF h-umsatz.datum GE Lfrom-date THEN 
        DO:
          IF w1.main-code = 1922 THEN w1.lastyr = w1.lastyr + h-umsatz.betrag. 
          IF w1.main-code = 1972 THEN w1.lastyr = w1.lastyr + h-umsatz.nettobetrag.
          IF w1.main-code = 1992 THEN w1.lastyr = w1.lastyr + h-umsatz.anzahl.
        END.
        IF w1.main-code = 1922 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.betrag.
        IF w1.main-code = 1972 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.nettobetrag. 
        IF w1.main-code = 1992 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.anzahl. 
      END.
      IF h-umsatz.epreis = 3 THEN
      DO:
        IF h-umsatz.datum GE Lfrom-date THEN 
        DO:
          IF w1.main-code = 1923 THEN w1.lastyr = w1.lastyr + h-umsatz.betrag. 
          IF w1.main-code = 1973 THEN w1.lastyr = w1.lastyr + h-umsatz.nettobetrag.
          IF w1.main-code = 1993 THEN w1.lastyr = w1.lastyr + h-umsatz.anzahl.
        END.
        IF w1.main-code = 1923 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.betrag.
        IF w1.main-code = 1973 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.nettobetrag. 
        IF w1.main-code = 1993 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.anzahl. 
      END.
      IF h-umsatz.epreis = 4 THEN
      DO:
        IF h-umsatz.datum GE Lfrom-date THEN 
        DO:
          IF w1.main-code = 1924 THEN w1.lastyr = w1.lastyr + h-umsatz.betrag. 
          IF w1.main-code = 1974 THEN w1.lastyr = w1.lastyr + h-umsatz.nettobetrag.
          IF w1.main-code = 1994 THEN w1.lastyr = w1.lastyr + h-umsatz.anzahl.
        END.
        IF w1.main-code = 1924 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.betrag.
        IF w1.main-code = 1974 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.nettobetrag. 
        IF w1.main-code = 1994 THEN w1.lytd-saldo = w1.lytd-saldo + h-umsatz.anzahl. 
      END.
    END.
  END.
END. 

PROCEDURE fill-los:
    DEFINE OUTPUT PARAMETER done AS LOGICAL.
    DEFINE VARIABLE datum1        AS DATE. 
    DEFINE VARIABLE datum         AS DATE.
    DEFINE VARIABLE ci-date       AS DATE.
    DEFINE VARIABLE end-date      AS DATE.
    DEFINE VARIABLE start-date    AS DATE.
    DEFINE VARIABLE i             AS INT.
    DEFINE VARIABLE los           AS INT.

    DEFINE VARIABLE mon-saldo1   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo2   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo3   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo4   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo5   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo6   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo7   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo8   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo9   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo10   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo11   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].
    DEFINE VARIABLE mon-saldo12   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].



    FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
    ci-date = htparam.fdate.

    DEFINE BUFFER wlos FOR w1.

    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 


    FIND FIRST wlos WHERE wlos.main-code = 9000 NO-LOCK NO-ERROR.

    FOR EACH res-line WHERE res-line.abreise GE datum1 AND res-line.ankunf LE to-date
        AND res-line.l-zuordnung[3] = 0 AND res-line.zinr NE "" AND res-line.l-zuordnung[1] NE 0
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 99 AND res-line.resstatus NE 10
        AND res-line.resstatus NE 12:

        IF res-line.ankunft = to-date AND res-line.active-flag NE 1 THEN.
        ELSE
        DO:
            IF res-line.abreise = res-line.ankunft THEN end-date = res-line.abreise.
            ELSE end-date = res-line.abreise - 1.

            IF end-date GT to-date THEN end-date = to-date.
            IF res-line.ankunft LT datum1 THEN start-date = datum1.
            ELSE start-date = res-line.ankunft.

            DO datum = start-date TO end-date:
                IF res-line.abreise - datum = 0 THEN los = 1.
                ELSE los = res-line.abreise - datum.
                IF datum = to-date THEN
                    wlos.tday = wlos.tday + los.

                IF MONTH(datum) = MONTH(to-date) AND YEAR(datum) = YEAR(to-date) THEN
                    wlos.mon-saldo[DAY(datum)] = wlos.mon-saldo[DAY(datum)] + los.

                IF MONTH(datum) = 1 THEN
                    mon-saldo1[DAY(datum)] = mon-saldo1[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 2 THEN
                    mon-saldo2[DAY(datum)] = mon-saldo2[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 3 THEN
                    mon-saldo3[DAY(datum)] = mon-saldo3[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 4 THEN
                    mon-saldo4[DAY(datum)] = mon-saldo4[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 5 THEN
                    mon-saldo5[DAY(datum)] = mon-saldo5[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 6 THEN
                    mon-saldo6[DAY(datum)] = mon-saldo6[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 7 THEN
                    mon-saldo7[DAY(datum)] = mon-saldo7[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 8 THEN
                    mon-saldo8[DAY(datum)] = mon-saldo8[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 9 THEN
                    mon-saldo9[DAY(datum)] = mon-saldo9[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 10 THEN
                    mon-saldo10[DAY(datum)] = mon-saldo10[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 11 THEN
                    mon-saldo11[DAY(datum)] = mon-saldo11[DAY(datum)] + los.
                ELSE IF MONTH(datum) = 12 THEN
                    mon-saldo12[DAY(datum)] = mon-saldo12[DAY(datum)] + los.
            END.
        END.    
    END.    

    DO i = 1 TO 31:
        wlos.saldo = wlos.saldo + wlos.mon-saldo[i].
        wlos.ytd-saldo = wlos.ytd-saldo + mon-saldo1[i] + mon-saldo2[i] + mon-saldo3[i] + mon-saldo4[i]
            + mon-saldo5[i] + mon-saldo6[i] + mon-saldo7[i] + mon-saldo8[i] + mon-saldo9[i] + mon-saldo10[i]
            + mon-saldo11[i] + mon-saldo12[i].
    END.

    done = YES.
END.

PROCEDURE fill-pax-cover-shift:   /*FT 201116*/
DEFINE OUTPUT PARAMETER done AS LOGICAL.
DEFINE VARIABLE datum1        AS DATE. 

DEFINE VARIABLE disc-art1   AS INTEGER NO-UNDO. 
DEFINE VARIABLE disc-art2   AS INTEGER NO-UNDO. 
DEFINE VARIABLE disc-art3   AS INTEGER NO-UNDO.

DEFINE BUFFER buff FOR h-bill-line.
DEFINE BUFFER art-buff FOR h-artikel.
DEFINE BUFFER wspc FOR w1.

DEFINE VARIABLE shift AS INT INIT 0.
DEFINE VARIABLE temp1 AS CHAR.
DEFINE VARIABLE temp2 AS CHAR.

DEFINE VARIABLE do-it AS LOGICAL INIT YES.

RUN htpint.p(557, OUTPUT disc-art1).
RUN htpint.p(596, OUTPUT disc-art2).

FOR EACH queasy WHERE queasy.key = 5 AND queasy.number3 NE 0 NO-LOCK BY queasy.number1:
    CREATE shift-list.
    ASSIGN
        shift-list.shift = queasy.number3
        temp1 = STRING(queasy.number1,"9999")
        temp2 = STRING(queasy.number2,"9999")
        shift-list.ftime = (INT(SUBSTR(temp1,1,2)) * 3600) + (INT(SUBSTR(temp1,3,2)) * 60)
        shift-list.ttime = (INT(SUBSTR(temp2,1,2)) * 3600) + (INT(SUBSTR(temp2,3,2)) * 60).
END.
    
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    
    EMPTY TEMP-TABLE t-list.

    FOR EACH h-bill-line WHERE h-bill-line.bill-datum GE datum1
        AND h-bill-line.bill-datum LE to-date
        AND h-bill-line.artnr GT 0 
        AND h-bill-line.artnr NE disc-art1 
        AND h-bill-line.artnr NE disc-art2 
        AND h-bill-line.artnr NE disc-art3 
        AND h-bill-line.zeit GE 0 
        AND h-bill-line.epreis GT 0 NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr 
           AND h-artikel.departement = h-bill-line.departement 
           AND h-artikel.artart = 0 AND h-artikel.artart NE 11
           AND h-artikel.artart NE 12 NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
           AND artikel.departement = h-artikel.departement NO-LOCK,
        FIRST h-bill WHERE h-bill.rechnr = h-bill-line.rechnr
           AND h-bill.departement = h-bill-line.departement NO-LOCK
        BY h-bill-line.departement BY h-bill-line.betriebsnr 
        BY h-bill-line.rechnr BY h-bill-line.bill-datum:

        do-it = YES.

        FOR EACH buff WHERE buff.rechnr = h-bill-line.rechnr 
          AND buff.departement = h-bill-line.departement NO-LOCK,
          FIRST art-buff WHERE art-buff.artnr = buff.artnr 
            AND art-buff.departement = buff.departement NO-LOCK 
            BY art-buff.artart:
          IF art-buff.artart = 11 OR art-buff.artart = 12 THEN
          DO:
              do-it = NO.
              LEAVE.
          END.      
        END.

        IF do-it THEN
        DO:
            shift = 0.
            FIND FIRST shift-list WHERE shift-list.ftime LE h-bill-line.zeit AND 
                shift-list.ttime GE h-bill-line.zeit NO-LOCK NO-ERROR.
            IF AVAILABLE shift-list THEN
                shift = shift-list.shift.
            
            FIND FIRST t-list WHERE t-list.dept = h-bill-line.departement
               AND t-list.datum = h-bill-line.bill-datum 
               AND t-list.shift = h-bill-line.betriebsnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE t-list THEN
            DO:
               CREATE t-list.
               ASSIGN
                   t-list.datum = h-bill-line.bill-datum 
                   t-list.dept  = h-bill-line.departement
                   t-list.shift = h-bill-line.betriebsnr
               .
            END.
        
            FIND FIRST t-rechnr WHERE t-rechnr.rechnr = h-bill-line.rechnr 
               AND t-rechnr.dept  = h-bill-line.departement 
               AND t-rechnr.datum = h-bill-line.bill-datum 
               AND t-rechnr.shift = shift NO-LOCK NO-ERROR.
            IF NOT AVAILABLE t-rechnr THEN
            DO:
               CREATE t-rechnr.
               ASSIGN
                   t-rechnr.rechnr = h-bill-line.rechnr 
                   t-rechnr.dept   = h-bill-line.departement
                   t-rechnr.datum  = h-bill-line.bill-datum
                   t-rechnr.shift  = shift
               .
            END.
        
            IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 AND NOT t-rechnr.found-food THEN 
            DO:
                /*IF h-bill-line.betriebsnr NE 0 THEN*/
                t-rechnr.found-food = YES.
                t-list.pax-food = t-list.pax-food + h-bill.belegung.
            END.
        
            IF artikel.umsatzart = 6 AND NOT t-rechnr.found-bev THEN 
            DO:
                /*IF h-bill-line.betriebsnr NE 0 THEN*/
                t-rechnr.found-bev = YES.
                t-list.pax-bev = t-list.pax-bev + h-bill.belegung.
            END.
        END.    
    END.     
    
    done = YES.
    
    FOR EACH t-list BY t-list.dept BY t-list.shift BY t-list.datum:
        FIND FIRST wspc WHERE wspc.main-code = 1995 AND INT(SUBSTR(wspc.s-artnr,1,2)) = t-list.dept
            AND INT(SUBSTR(wspc.s-artnr,3)) = t-list.shift NO-LOCK NO-ERROR.
        IF AVAILABLE wspc THEN
        DO:
            IF t-list.datum = to-date THEN
                wspc.tday = wspc.tday + t-list.pax-food.
            IF MONTH(t-list.datum) = MONTH(to-date) THEN
                wspc.saldo = wspc.saldo + t-list.pax-food.
             wspc.ytd-saldo = wspc.ytd-saldo + t-list.pax-food.
        END.
    
        FIND FIRST wspc WHERE wspc.main-code = 1996 AND INT(SUBSTR(wspc.s-artnr,1,2)) = t-list.dept
            AND INT(SUBSTR(wspc.s-artnr,3)) = t-list.shift NO-LOCK NO-ERROR.
        IF AVAILABLE wspc THEN
        DO:
            IF t-list.datum = to-date THEN
                wspc.tday = wspc.tday + t-list.pax-bev.
            IF MONTH(t-list.datum) = MONTH(to-date) THEN
                wspc.saldo = wspc.saldo + t-list.pax-bev.
             wspc.ytd-saldo = wspc.ytd-saldo + t-list.pax-bev.
        END.
    END.    
END.    

PROCEDURE fill-pax-cover-shift1:   
  DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
  DEFINE VARIABLE datum1        AS DATE. 
  DEFINE VARIABLE endkum        AS INTEGER.
  DEFINE VARIABLE artnrfront    AS INTEGER.
  DEFINE VARIABLE compli-flag   AS LOGICAL INITIAL NO.
  DEFINE VARIABLE vat           AS DECIMAL. 
  DEFINE VARIABLE vat2          AS DECIMAL. 
  DEFINE VARIABLE service       AS DECIMAL.
  DEFINE VARIABLE fact          AS DECIMAL. 
  DEFINE VARIABLE netto         AS DECIMAL.
  DEFINE VARIABLE curr-rechnr   AS INTEGER.
  DEFINE VARIABLE curr-dept     AS INTEGER.
  DEFINE VARIABLE temp-time     AS INTEGER.
  DEFINE VARIABLE d-flag        AS LOGICAL.

  DEF VAR counter AS INTEGER.

  DEFINE BUFFER btemp-rechnr FOR temp-rechnr.
  DEFINE BUFFER bh-artikel   FOR h-artikel.
  DEFINE BUFFER bh-bill-line FOR h-bill-line.
  
  FIND FIRST w1 WHERE RECID(w1) = rec-w1.

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
     
  /*EMPTY TEMP-TABLE t-rechnr.
  EMPTY TEMP-TABLE temp-rechnr.*/
  curr-rechnr = 0.

  FIND FIRST temp-rechnr NO-ERROR.
  IF NOT AVAILABLE temp-rechnr THEN
  DO:             
    FOR EACH h-bill-line WHERE h-bill-line.bill-datum GE datum1
      AND h-bill-line.bill-datum LE to-date
      AND h-bill-line.artnr GT 0 
      /*AND h-bill-line.departement = 1*/ NO-LOCK,
      FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr 
         AND h-artikel.departement = h-bill-line.departement NO-LOCK,
      FIRST h-bill WHERE h-bill.rechnr = h-bill-line.rechnr
         AND h-bill.departement = h-bill-line.departement NO-LOCK
     BY h-bill-line.bill-datum BY h-bill-line.departement  BY h-bill-line.rechnr  
      BY h-bill-line.betriebsnr:
    
      IF curr-rechnr NE h-bill-line.rechnr THEN
      DO:
         CREATE temp-rechnr.                                
         ASSIGN temp-rechnr.rechnr      = h-bill-line.rechnr    
                temp-rechnr.shift       = h-bill-line.betriebsnr
                temp-rechnr.dept        = h-bill-line.departement
                temp-rechnr.datum       = h-bill-line.bill-datum
                temp-rechnr.belegung    = h-bill.belegung
                temp-rechnr.artnrfront  = h-artikel.artnrfront
                temp-rechnr.tischnr     = h-bill-line.tischnr
                temp-rechnr.betrag      = h-bill-line.betrag
                temp-rechnr.artnr       = h-bill-line.artnr
                temp-rechnr.artart      = h-artikel.artart
                temp-rechnr.resnr       = h-bill.resnr
                temp-rechnr.reslinnr    = h-bill.reslinnr
                curr-rechnr             = h-bill-line.rechnr
                curr-dept               = h-bill-line.departement.

         FOR EACH bh-bill-line WHERE bh-bill-line.rechnr = h-bill-line.rechnr AND bh-bill-line.departement = h-bill-line.departement NO-LOCK ,
             FIRST bh-artikel WHERE bh-artikel.artnr = bh-bill-line.artnr AND bh-artikel.departement = bh-bill-line.departement 
             AND bh-artikel.artart GE 11 AND bh-artikel.artart LE 12 NO-LOCK BY bh-artikel.artart DESC:
             ASSIGN temp-rechnr.compli-flag = YES.
             LEAVE.
         END.
      END.

      FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront AND artikel.departement = h-artikel.departement NO-LOCK NO-ERROR.
      IF AVAILABLE artikel THEN
      DO:
         IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN
         DO:
           ASSIGN temp-rechnr.f-pax = h-bill.belegung
                  temp-rechnr.f-qty = temp-rechnr.f-qty + h-bill-line.anzahl.
         END.
         ELSE IF artikel.umsatzart = 6 THEN
         DO:
           ASSIGN temp-rechnr.b-pax = h-bill.belegung
                  temp-rechnr.b-qty = temp-rechnr.b-qty + h-bill-line.anzahl.
         END.
      END.              
    END.
  END.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1.
  
  FOR EACH temp-rechnr WHERE temp-rechnr.dept = w1.dept NO-LOCK:           
      IF (w1.main-code = 192 OR w1.main-code = 197 OR w1.main-code = 1995 OR w1.main-code = 1996) THEN
      DO:
        IF NOT temp-rechnr.compli-flag THEN
        DO:
          IF w1.main-code = 192 OR w1.main-code = 1995 THEN /*P-COVER & FP-COVER*/
          DO:
             IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.f-pax. 
             IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.f-pax. 
             IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.f-pax. 

             d-flag = (MONTH(temp-rechnr.datum) = MONTH(to-date)) AND (YEAR(temp-rechnr.datum) = YEAR(to-date)).
             IF d-flag THEN
             DO:
               w1.mon-saldo[DAY(temp-rechnr.datum)] = w1.mon-saldo[DAY(temp-rechnr.datum)] + temp-rechnr.f-pax.
             END.
          END.
          IF w1.main-code = 197 OR w1.main-code = 1996 THEN /*$B-COVER & BP-COVER*/
          DO:
             IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.b-pax. 
             IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.b-pax. 
             IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.b-pax. 

             d-flag = (MONTH(temp-rechnr.datum) = MONTH(to-date)) AND (YEAR(temp-rechnr.datum) = YEAR(to-date)).
             IF d-flag THEN
             DO:
               w1.mon-saldo[DAY(temp-rechnr.datum)] = w1.mon-saldo[DAY(temp-rechnr.datum)] + temp-rechnr.b-pax.
             END. 
          END.   
        END.
      END.
      /*geral G-total daily sales 0ADD87*/
      ELSE IF w1.main-code = 2028 THEN
      DO:
        IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.belegung. 
        IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 

        d-flag = (MONTH(temp-rechnr.datum) = MONTH(to-date)) AND (YEAR(temp-rechnr.datum) = YEAR(to-date)).
        IF d-flag THEN
        DO:
          w1.mon-saldo[DAY(temp-rechnr.datum)] = w1.mon-saldo[DAY(temp-rechnr.datum)] + temp-rechnr.belegung.
        END.
      END.
      /*R-total daily sales*/
      ELSE IF w1.main-code = 552 THEN
      DO:
        IF NOT temp-rechnr.compli-flag THEN
        DO: 
          IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.belegung. 
          IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
          IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 

          d-flag = (MONTH(temp-rechnr.datum) = MONTH(to-date)) AND (YEAR(temp-rechnr.datum) = YEAR(to-date)).
          IF d-flag THEN
          DO:
            w1.mon-saldo[DAY(temp-rechnr.datum)] = w1.mon-saldo[DAY(temp-rechnr.datum)] + temp-rechnr.belegung.
          END.
        END.
      END.
      /*gerald tot-bill daily sales 72AF1A*/
      ELSE IF w1.main-code = 2029 THEN
      DO:
        IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + 1. 
        IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + 1. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + 1. 

        d-flag = (MONTH(temp-rechnr.datum) = MONTH(to-date)) AND (YEAR(temp-rechnr.datum) = YEAR(to-date)).
        IF d-flag THEN
        DO:
          w1.mon-saldo[DAY(temp-rechnr.datum)] = w1.mon-saldo[DAY(temp-rechnr.datum)] + 1.
        END.
      END.
      /*gerald pax-table daily sales 72AF1A*/
      ELSE IF w1.main-code = 2031 AND w1.tischnr = temp-rechnr.tischnr THEN
      DO:
        IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.belegung. 
        IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 

        d-flag = (MONTH(temp-rechnr.datum) = MONTH(to-date)) AND (YEAR(temp-rechnr.datum) = YEAR(to-date)).
        IF d-flag THEN
        DO:
          w1.mon-saldo[DAY(temp-rechnr.datum)] = w1.mon-saldo[DAY(temp-rechnr.datum)] + temp-rechnr.belegung.
        END.
      END.

      /*$FP-COVER 1 2 3 4 & $BP-COVER 1 2 3 4*/
    ELSE IF (w1.main-code GE 2020 AND w1.main-code LE 2027) THEN
    DO:
      IF NOT temp-rechnr.compli-flag THEN
      DO:
         IF temp-rechnr.shift = 1 THEN
         DO:
           IF temp-rechnr.datum = to-date THEN
           DO:
             IF w1.main-code = 2020 THEN w1.tday = w1.tday + temp-rechnr.f-pax.
             IF w1.main-code = 2024 THEN w1.tday = w1.tday + temp-rechnr.b-pax.
           END.
           IF MONTH(temp-rechnr.datum) EQ MONTH(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN
           DO:
             IF w1.main-code = 2020 THEN w1.saldo = w1.saldo + temp-rechnr.f-pax.
             IF w1.main-code = 2024 THEN w1.saldo = w1.saldo + temp-rechnr.b-pax. 
           END.
           IF ytd-flag THEN
           DO:
             IF w1.main-code = 2020 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.f-pax.
             IF w1.main-code = 2024 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.b-pax.
           END.
         END.
         IF temp-rechnr.shift = 2 THEN
         DO:
           IF temp-rechnr.datum = to-date THEN
           DO:
             IF w1.main-code = 2021 THEN w1.tday = w1.tday + temp-rechnr.f-pax.
             IF w1.main-code = 2025 THEN w1.tday = w1.tday + temp-rechnr.b-pax.
           END.
           IF MONTH(temp-rechnr.datum) EQ MONTH(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN
           DO:
             IF w1.main-code = 2021 THEN w1.saldo = w1.saldo + temp-rechnr.f-pax.
             IF w1.main-code = 2025 THEN w1.saldo = w1.saldo + temp-rechnr.b-pax.
           END.
           IF ytd-flag THEN
           DO:
             IF w1.main-code = 2021 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.f-pax.
             IF w1.main-code = 2025 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.b-pax.
           END.
         END.
         IF temp-rechnr.shift = 3 THEN
         DO:
           IF temp-rechnr.datum = to-date THEN
           DO:
             IF w1.main-code = 2022 THEN w1.tday = w1.tday + temp-rechnr.f-pax.
             IF w1.main-code = 2026 THEN w1.tday = w1.tday + temp-rechnr.b-pax.
           END.
           IF MONTH(temp-rechnr.datum) EQ MONTH(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN
           DO:
             IF w1.main-code = 2022 THEN w1.saldo = w1.saldo + temp-rechnr.f-pax.
             IF w1.main-code = 2026 THEN w1.saldo = w1.saldo + temp-rechnr.b-pax.
           END.
           IF ytd-flag THEN
           DO:
             IF w1.main-code = 2022 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.f-pax.
             IF w1.main-code = 2026 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.b-pax.
           END.
         END.
         IF temp-rechnr.shift = 4 THEN
         DO:
           IF temp-rechnr.datum = to-date THEN
           DO:
             IF w1.main-code = 2023 THEN w1.tday = w1.tday + temp-rechnr.f-pax.
             IF w1.main-code = 2027 THEN w1.tday = w1.tday + temp-rechnr.b-pax. 
           END.
           IF MONTH(temp-rechnr.datum) EQ MONTH(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN
           DO:
             IF w1.main-code = 2023 THEN w1.saldo = w1.saldo + temp-rechnr.f-pax.
             IF w1.main-code = 2027 THEN w1.saldo = w1.saldo + temp-rechnr.b-pax. 
           END.
           IF ytd-flag THEN
           DO:
             IF w1.main-code = 2023 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.f-pax.
             IF w1.main-code = 2027 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.b-pax. 
           END. 
         END.
      END.                       
    END.
    ELSE IF (w1.main-code GE 2001 AND w1.main-code LE 2004)
        OR (w1.main-code GE 2032 AND w1.main-code LE 2051) THEN
    DO:
      FIND FIRST res-line WHERE res-line.resnr EQ temp-rechnr.resnr AND res-line.reslinnr eq temp-rechnr.reslinnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO: 
        IF temp-rechnr.datum = to-date THEN /*PI-Cover*/
        DO:
          IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2001 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2002 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2003 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2004 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
        END.
        IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN 
        DO:
          IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2001 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2002 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2003 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2004 THEN w1.saldo = w1.saldo + temp-rechnr.belegung.                               
        END.
        ELSE
        DO:
          IF ytd-flag THEN
          DO:
            IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2001 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
            IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2002 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
            IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2003 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
            IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2004 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
          END.
        END.

        IF temp-rechnr.compli-flag = YES THEN
        DO:
           IF temp-rechnr.datum = to-date THEN /*PC-COVER*/
           DO:
             IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2032 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2033 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2034 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2035 THEN w1.tday = w1 .tday + temp-rechnr.belegung.
           END.
           IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN 
           DO:
             IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2032 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2033 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2034 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2035 THEN w1.saldo = w1.saldo + temp-rechnr.belegung.                               
           END.
           
           ELSE
           DO:
             IF ytd-flag THEN
             DO:
               IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2032 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
               IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2033 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
               IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2034 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
               IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2035 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung.
             END.
           END.
        END.
      
        FIND FIRST artikel WHERE artikel.departement = temp-rechnr.dept AND artikel.artnr = temp-rechnr.artnrfront NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN
        DO:
           /*RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement, temp-rechnr.datum, 
                                   OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).*/
           netto = temp-rechnr.betrag / (1 + vat + vat2 + service). 
      
           IF temp-rechnr.datum = to-date THEN /*Rev-Inhouse*/
           DO:
             IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2044 THEN w1.tday = w1.tday + netto. 
             IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2045 THEN w1.tday = w1.tday + netto. 
             IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2046 THEN w1.tday = w1.tday + netto. 
             IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2047 THEN w1.tday = w1 .tday + netto.
           END.
           IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN 
           DO:
             IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2044 THEN w1.saldo = w1.saldo + netto. 
             IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2045 THEN w1.saldo = w1.saldo + netto. 
             IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2046 THEN w1.saldo = w1.saldo + netto. 
             IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2047 THEN w1.saldo = w1.saldo + netto.                               
           END.
           
           ELSE 
           DO:
             IF ytd-flag THEN
             DO:
               IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2044 THEN w1.ytd-saldo = w1.ytd-saldo + netto. 
               IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2045 THEN w1.ytd-saldo = w1.ytd-saldo + netto. 
               IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2046 THEN w1.ytd-saldo = w1.ytd-saldo + netto. 
               IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2047 THEN w1.ytd-saldo = w1.ytd-saldo + netto.
             END.
           END.
        END.
      END.
      ELSE IF NOT AVAILABLE res-line THEN
      DO:
        IF temp-rechnr.datum = to-date THEN /*PO-Cover*/
        DO:
          IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2036 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2037 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2038 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2039 THEN w1.tday = w1 .tday + temp-rechnr.belegung.
        END.
        IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN 
        DO:
          IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2036 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2037 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2038 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
          IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2039 THEN w1.saldo = w1.saldo + temp-rechnr.belegung.                               
        END.
        
        ELSE
        DO:
          IF ytd-flag THEN
          DO:
            IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2036 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
            IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2037 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
            IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2038 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
            IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2039 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
          END.
        END.
      
        IF temp-rechnr.compli-flag = YES THEN
        DO:
           IF temp-rechnr.datum = to-date THEN /*PCO-Cover*/
           DO:
             IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2040 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2041 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2042 THEN w1.tday = w1.tday + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2043 THEN w1.tday = w1 .tday + temp-rechnr.belegung.
           END.
           IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN 
           DO:
             IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2040 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2041 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2042 THEN w1.saldo = w1.saldo + temp-rechnr.belegung. 
             IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2043 THEN w1.saldo = w1.saldo + temp-rechnr.belegung.                               
           END.
           
           ELSE 
           DO:
             IF ytd-flag THEN
             DO:
               IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2040 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
               IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2041 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
               IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2042 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
               IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2043 THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.belegung. 
             END.
           END.
        END.
      
        FIND FIRST artikel WHERE artikel.departement = temp-rechnr.dept AND artikel.artnr = temp-rechnr.artnrfront NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN
        DO:
           /*RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement, temp-rechnr.datum, 
                                   OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).*/
           netto = temp-rechnr.betrag / (1 + vat + vat2 + service). 
      
           IF temp-rechnr.datum = to-date THEN /*Rev-Outsider*/
           DO:
             IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2048 THEN w1.tday = w1.tday + netto. 
             IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2049 THEN w1.tday = w1.tday + netto. 
             IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2050 THEN w1.tday = w1.tday + netto. 
             IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2051 THEN w1.tday = w1 .tday + netto.
           END.
           IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN 
           DO:
             IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2048 THEN w1.saldo = w1.saldo + netto. 
             IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2049 THEN w1.saldo = w1.saldo + netto. 
             IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2050 THEN w1.saldo = w1.saldo + netto. 
             IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2051 THEN w1.saldo = w1.saldo + netto.                               
           END.
           
           ELSE
           DO:
             IF ytd-flag THEN
             DO:
               IF temp-rechnr.shift = 1 THEN IF w1.main-code = 2048 THEN w1.ytd-saldo = w1.ytd-saldo + netto. 
               IF temp-rechnr.shift = 2 THEN IF w1.main-code = 2049 THEN w1.ytd-saldo = w1.ytd-saldo + netto. 
               IF temp-rechnr.shift = 3 THEN IF w1.main-code = 2050 THEN w1.ytd-saldo = w1.ytd-saldo + netto. 
               IF temp-rechnr.shift = 4 THEN IF w1.main-code = 2051 THEN w1.ytd-saldo = w1.ytd-saldo + netto.
             END.
           END.
        END.
      END.
    END.
    ELSE IF (w1.main-code GE 2052 AND w1.main-code LE 2055) THEN
    DO:
       IF w1.main-code = 2052 OR w1.main-code = 2053 THEN
       DO:
          IF NOT temp-rechnr.compli-flag THEN
          DO:
            IF w1.main-code = 2052 THEN /*RQTY-FOOD*/
            DO:
               IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.f-qty. 
               IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.f-qty. 
               IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.f-qty. 
            END.
            IF w1.main-code = 2053 THEN /*RQTY-BEV*/
            DO:
               IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.b-qty. 
               IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.b-qty. 
               IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.b-qty. 
            END.    
          END.
       END.
       ELSE IF w1.main-code = 2054 OR w1.main-code = 2055 THEN
       DO:
         IF w1.main-code = 2054 THEN /*GQTY-FOOD*/
         DO:
            IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.f-qty. 
            IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.f-qty. 
            IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.f-qty. 
         END.
         IF w1.main-code = 2055 THEN /*GQTY-BEV*/
         DO:
            IF temp-rechnr.datum = to-date THEN w1.tday = w1.tday + temp-rechnr.b-qty. 
            IF month(temp-rechnr.datum) EQ month(to-date) AND YEAR(temp-rechnr.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + temp-rechnr.b-qty. 
            IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + temp-rechnr.b-qty. 
         END.       
       END.
    END.
  END.
END.   

PROCEDURE fill-fb-flash:   
  DEFINE INPUT PARAMETER rec-w1   AS INTEGER. 
  DEFINE VARIABLE datum1          AS DATE. 
  DEFINE VARIABLE d-flag          AS LOGICAL.
  DEFINE VARIABLE f-eknr          AS INTEGER NO-UNDO. 
  DEFINE VARIABLE b-eknr          AS INTEGER NO-UNDO. 
  DEFINE VARIABLE fl-eknr         AS INTEGER NO-UNDO. 
  DEFINE VARIABLE bl-eknr         AS INTEGER NO-UNDO.
  DEFINE VARIABLE ldry            AS INTEGER NO-UNDO. 
  DEFINE VARIABLE dstore          AS INTEGER NO-UNDO.
  DEFINE VARIABLE main-storage    AS INTEGER INITIAL 1 NO-UNDO.
  DEFINE VARIABLE warenwert       AS DECIMAL.
  DEFINE VARIABLE stornground     AS CHAR.
  DEFINE VARIABLE double-currency AS LOGICAL NO-UNDO INITIAL NO.
  DEFINE VARIABLE foreign-nr      AS INTEGER NO-UNDO INITIAL 0. 
  DEFINE VARIABLE exchg-rate      AS DECIMAL NO-UNDO INITIAL 1.
  DEFINE VARIABLE curr-datum      AS DATE    NO-UNDO INITIAL ?.
  DEFINE VARIABLE rate            AS DECIMAL      NO-UNDO INITIAL 1. 
  DEFINE VARIABLE cost            AS DECIMAL      NO-UNDO.  

  DEFINE BUFFER h-art     FOR h-artikel. 
  DEFINE BUFFER gl-acc1   FOR gl-acct. 

  FIND FIRST w1 WHERE RECID(w1) = rec-w1.

  EMPTY TEMP-TABLE s-list.

  FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
  ldry = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
  dstore = htparam.finteger. 

  FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency flag */ 
  IF htparam.flogical THEN 
  DO: 
    double-currency = YES. 
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN 
    DO: 
      foreign-nr = waehrung.waehrungsnr. 
      exchg-rate = waehrung.ankauf / waehrung.einheit. 
    END. 
    ELSE exchg-rate = 1. 
  END.

  /* sales */ 
  FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
  f-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
  b-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  
  /* cost, see paramgroup 21 */ 
  FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
  fl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
  bl-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 

  warenwert = 0.
  IF w1.main-code = 2056 THEN   /*FB-Direct*/
  DO:
    FOR EACH l-op WHERE l-op.op-art = 1 AND l-op.pos GT 0 
      AND l-op.loeschflag LE 1 AND l-op.lager-nr NE main-storage
      AND l-op.datum GE datum1 AND l-op.datum LE to-date NO-LOCK, 
      FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum = w1.dept NO-LOCK: 
      
      FIND FIRST s-list WHERE s-list.flag = w1.dept NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
        CREATE s-list.
        ASSIGN s-list.datum  = l-op.datum
               s-list.flag   = w1.dept.
      END.

      s-list.betrag = s-list.betrag + l-op.warenwert.
    END. 

    FOR EACH s-list WHERE s-list.flag = w1.dept:
      IF s-list.datum = to-date THEN w1.tday = w1.tday + s-list.betrag. 
      IF month(s-list.datum) EQ month(to-date) AND YEAR(s-list.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + s-list.betrag. 
      IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + s-list.betrag. 

      d-flag = (MONTH(s-list.datum) = MONTH(to-date)) AND (YEAR(s-list.datum) = YEAR(to-date)).
      IF d-flag THEN
      DO:
        w1.mon-saldo[DAY(s-list.datum)] = w1.mon-saldo[DAY(s-list.datum)] + s-list.betrag.
      END.
    END.
  END.
  IF w1.main-code = 2057 THEN  /*FB-Transfer*/
  DO:
    FOR EACH l-op WHERE l-op.op-art = 4 
      AND l-op.loeschflag LE 1 AND l-op.herkunftflag = 1 
      AND l-op.datum GE datum1 
      AND l-op.datum LE to-date NO-LOCK, 
      FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum = w1.dept NO-LOCK: 
      
      FIND FIRST s-list WHERE s-list.flag = w1.dept NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
        CREATE s-list.
        ASSIGN s-list.datum  = l-op.datum
               s-list.flag   = w1.dept.
      END.

      IF l-op.lager-nr NE main-storage THEN 
      DO:
        s-list.betrag = s-list.betrag - l-op.warenwert.
      END.
      IF l-op.pos NE main-storage THEN 
      DO: 
        s-list.betrag = s-list.betrag + l-op.warenwert.
      END.
    END. 

    FOR EACH s-list WHERE s-list.flag = w1.dept:
      IF s-list.datum = to-date THEN w1.tday = w1.tday + s-list.betrag. 
      IF month(s-list.datum) EQ month(to-date) AND YEAR(s-list.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + s-list.betrag. 
      IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + s-list.betrag. 

      d-flag = (MONTH(s-list.datum) = MONTH(to-date)) AND (YEAR(s-list.datum) = YEAR(to-date)).
      IF d-flag THEN
      DO:
        w1.mon-saldo[DAY(s-list.datum)] = w1.mon-saldo[DAY(s-list.datum)] + s-list.betrag.
      END.
    END.
  END.
  IF w1.main-code = 2058 THEN /*FB-Cost-Alloc*/
  DO:
    IF w1.dept = fl-eknr THEN
     DO:
       FIND FIRST htparam WHERE paramnr = 272 NO-LOCK NO-ERROR. 
       IF AVAILABLE htparam THEN stornground = htparam.fchar. 
    END.
    ELSE IF w1.dept = bl-eknr THEN
    DO:
       FIND FIRST htparam WHERE paramnr = 275 NO-LOCK NO-ERROR. 
       IF AVAILABLE htparam THEN stornground = htparam.fchar. 
    END.

    FOR EACH l-op WHERE l-op.op-art = 3 AND l-op.loeschflag LE 1 
        AND l-op.datum GE datum1 AND l-op.datum LE to-date 
        AND l-op.stornogrund = stornground  NO-LOCK, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND (l-artikel.endkum = fl-eknr OR l-artikel.endkum = bl-eknr) NO-LOCK: 
     
        IF l-op.stornogrund = stornogrund THEN
        DO:
          FIND FIRST s-list WHERE s-list.flag = w1.dept NO-ERROR.
          IF NOT AVAILABLE s-list THEN
          DO:
            CREATE s-list.
            ASSIGN s-list.datum  = l-op.datum
                   s-list.flag   = w1.dept.
          END.
          
          s-list.betrag = s-list.betrag + l-op.warenwert.
        END.
    END.

    FOR EACH s-list WHERE s-list.flag = w1.dept:
      IF s-list.datum = to-date THEN w1.tday = w1.tday + s-list.betrag. 
      IF month(s-list.datum) EQ month(to-date) AND YEAR(s-list.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + s-list.betrag. 
      IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + s-list.betrag. 

      d-flag = (MONTH(s-list.datum) = MONTH(to-date)) AND (YEAR(s-list.datum) = YEAR(to-date)).
      IF d-flag THEN
      DO:
        w1.mon-saldo[DAY(s-list.datum)] = w1.mon-saldo[DAY(s-list.datum)] + s-list.betrag.
      END.
    END.
  END.
  IF w1.main-code = 2059 THEN  /*FB-Compliment*/
  DO:
    FOR EACH h-compli WHERE h-compli.datum GE datum1 
        AND h-compli.datum LE to-date AND h-compli.departement NE ldry 
        AND h-compli.departement NE dstore AND h-compli.betriebsnr = 0 NO-LOCK, 
        FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK 
        BY h-compli.datum BY h-compli.rechnr: 

        cost = 0. 

        IF double-currency AND curr-datum NE h-compli.datum THEN 
        DO: 
            curr-datum = h-compli.datum. 
            IF foreign-nr NE 0 THEN 
                FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
                AND exrate.datum = curr-datum NO-LOCK NO-ERROR. 
            ELSE 
                FIND FIRST exrate WHERE exrate.datum = curr-datum 
                    NO-LOCK NO-ERROR. 
                IF AVAILABLE exrate THEN rate = exrate.betrag. 
                ELSE rate = exchg-rate. 
        END. 

        FIND FIRST h-artikel WHERE h-artikel.artnr = h-compli.artnr 
            AND h-artikel.departement = h-compli.departement NO-LOCK. 

        IF w1.dept = fl-eknr THEN
        DO:
          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
            AND artikel.departement = h-compli.departement NO-LOCK. 
          IF AVAILABLE artikel THEN
          DO:
             IF artikel.endkum = fl-eknr OR artikel.umsatzart = 3
                 OR artikel.umsatzart = 5 THEN
             DO:
                FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
                    AND h-cost.departement = h-compli.departement 
                    AND h-cost.datum = h-compli.datum 
                    AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
                IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
                    cost = h-compli.anzahl * h-cost.betrag. 
                ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
                    cost = h-compli.anzahl * h-compli.epreis * h-artikel.prozent / 100 * rate. 
             END.
          END.  
        END.
        ELSE IF w1.dept = bl-eknr THEN
        DO:
          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
            AND artikel.departement = h-compli.departement NO-LOCK. 
          IF AVAILABLE artikel THEN
          DO:
             IF artikel.endkum = bl-eknr OR artikel.umsatzart = 6 THEN
             DO:
                FIND FIRST h-cost WHERE h-cost.artnr = h-compli.artnr 
                    AND h-cost.departement = h-compli.departement 
                    AND h-cost.datum = h-compli.datum 
                    AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
                IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
                    cost = h-compli.anzahl * h-cost.betrag. 
                ELSE IF NOT AVAILABLE h-cost OR (AVAILABLE h-cost AND h-cost.betrag = 0) THEN 
                    cost = h-compli.anzahl * h-compli.epreis * h-artikel.prozent / 100 * rate. 
             END.
          END.    
        END.

        FIND FIRST s-list WHERE s-list.flag = w1.dept NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list.
          ASSIGN s-list.datum  = h-compli.datum
                 s-list.flag   = w1.dept.
        END.
        
        s-list.betrag = s-list.betrag + cost.
    END.

    FOR EACH s-list WHERE s-list.flag = w1.dept:
      IF s-list.datum = to-date THEN w1.tday = w1.tday + s-list.betrag. 
      IF month(s-list.datum) EQ month(to-date) AND YEAR(s-list.datum) EQ YEAR(to-date) THEN w1.saldo = w1.saldo + s-list.betrag. 
      IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + s-list.betrag. 

      d-flag = (MONTH(s-list.datum) = MONTH(to-date)) AND (YEAR(s-list.datum) = YEAR(to-date)).
      IF d-flag THEN
      DO:
        w1.mon-saldo[DAY(s-list.datum)] = w1.mon-saldo[DAY(s-list.datum)] + s-list.betrag.
      END.
    END.
  END.
END.

PROCEDURE fill-fbstat:   /*FT 041817*/
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1        AS DATE. 
DEFINE VARIABLE fbdept        AS INTEGER.
DEFINE VARIABLE shift         AS INT INIT 0.
DEFINE VARIABLE do-it         AS LOGICAL INIT YES.

DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.

DEFINE BUFFER wf1 FOR w1.
DEFINE BUFFER wf2 FOR w1.
DEFINE BUFFER wf3 FOR w1.
DEFINE BUFFER wf4 FOR w1.

DEFINE BUFFER wb1 FOR w1.
DEFINE BUFFER wb2 FOR w1.
DEFINE BUFFER wb3 FOR w1.
DEFINE BUFFER wb4 FOR w1.

DEFINE BUFFER wo1 FOR w1.
DEFINE BUFFER wo2 FOR w1.
DEFINE BUFFER wo3 FOR w1.
DEFINE BUFFER wo4 FOR w1.

DEFINE VARIABLE mm AS INT.
DEFINE VARIABLE yy AS INT.


FIND FIRST w1 WHERE RECID(w1) = rec-w1 NO-LOCK NO-ERROR.
fbdept = INT(SUBSTR(w1.s-artnr,1,2)).

FIND FIRST fbstat-dept WHERE fbstat-dept.dept = fbdept NO-LOCK NO-ERROR.
IF AVAILABLE fbstat-dept THEN
    do-it = NO.

IF do-it THEN
DO:
    CREATE fbstat-dept.
    ASSIGN
        fbstat-dept.dept = fbdept.

    FIND FIRST wf1 WHERE wf1.main-code = 1997 AND INT(SUBSTR(wf1.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wf1.s-artnr,3)) = 1 NO-LOCK NO-ERROR.
    FIND FIRST wf2 WHERE wf2.main-code = 1997 AND INT(SUBSTR(wf2.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wf2.s-artnr,3)) = 2 NO-LOCK NO-ERROR.
    FIND FIRST wf3 WHERE wf3.main-code = 1997 AND INT(SUBSTR(wf3.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wf3.s-artnr,3)) = 3 NO-LOCK NO-ERROR.
    FIND FIRST wf4 WHERE wf4.main-code = 1997 AND INT(SUBSTR(wf4.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wf4.s-artnr,3)) = 4 NO-LOCK NO-ERROR.

    FIND FIRST wb1 WHERE wb1.main-code = 1998 AND INT(SUBSTR(wb1.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wb1.s-artnr,3)) = 1 NO-LOCK NO-ERROR.
    FIND FIRST wb2 WHERE wb2.main-code = 1998 AND INT(SUBSTR(wb2.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wb2.s-artnr,3)) = 2 NO-LOCK NO-ERROR.
    FIND FIRST wb3 WHERE wb3.main-code = 1998 AND INT(SUBSTR(wb3.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wb3.s-artnr,3)) = 3 NO-LOCK NO-ERROR.
    FIND FIRST wb4 WHERE wb4.main-code = 1998 AND INT(SUBSTR(wb4.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wb4.s-artnr,3)) = 4 NO-LOCK NO-ERROR.

    FIND FIRST wo1 WHERE wb1.main-code = 1999 AND INT(SUBSTR(wo1.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wo1.s-artnr,3)) = 1 NO-LOCK NO-ERROR.
    FIND FIRST wo2 WHERE wo2.main-code = 1999 AND INT(SUBSTR(wo2.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wo2.s-artnr,3)) = 2 NO-LOCK NO-ERROR.
    FIND FIRST wo3 WHERE wo3.main-code = 1999 AND INT(SUBSTR(wo3.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wo3.s-artnr,3)) = 3 NO-LOCK NO-ERROR.
    FIND FIRST wo4 WHERE wo4.main-code = 1999 AND INT(SUBSTR(wo4.s-artnr,1,2)) = fbdept
        AND INT(SUBSTR(wo4.s-artnr,3)) = 4 NO-LOCK NO-ERROR.

    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 

    ASSIGN
        mm = MONTH(to-date)
        yy = YEAR(to-date)
    .

    FOR EACH fbstat WHERE fbstat.datum GE datum1 AND 
        fbstat.datum LE to-date AND fbstat.departement = fbdept:

        d-flag = AVAILABLE zinrstat AND (MONTH(zinrstat.datum) = MONTH(to-date))
            AND (YEAR(zinrstat.datum) = YEAR(to-date)).

        IF fbstat.datum = to-date THEN
        DO:
            IF AVAILABLE wf1 THEN wf1.tday = wf1.tday + fbstat.food-wpax[1] + fbstat.food-gpax[1].
            IF AVAILABLE wf2 THEN wf2.tday = wf2.tday + fbstat.food-wpax[2] + fbstat.food-gpax[2].
            IF AVAILABLE wf3 THEN wf3.tday = wf3.tday + fbstat.food-wpax[3] + fbstat.food-gpax[3].
            IF AVAILABLE wf4 THEN wf4.tday = wf4.tday + fbstat.food-wpax[4] + fbstat.food-gpax[4].

            IF AVAILABLE wb1 THEN wb1.tday = wb1.tday + fbstat.bev-wpax[1] + fbstat.bev-gpax[1].
            IF AVAILABLE wb2 THEN wb2.tday = wb2.tday + fbstat.bev-wpax[2] + fbstat.bev-gpax[2].
            IF AVAILABLE wb3 THEN wb3.tday = wb3.tday + fbstat.bev-wpax[3] + fbstat.bev-gpax[3].
            IF AVAILABLE wb4 THEN wb4.tday = wb4.tday + fbstat.bev-wpax[4] + fbstat.bev-gpax[4].

            IF AVAILABLE wo1 THEN wo1.tday = wo1.tday + fbstat.other-wpax[1] + fbstat.other-gpax[1].
            IF AVAILABLE wo2 THEN wo2.tday = wo2.tday + fbstat.other-wpax[2] + fbstat.other-gpax[2].
            IF AVAILABLE wo3 THEN wo3.tday = wo3.tday + fbstat.other-wpax[3] + fbstat.other-gpax[3].
            IF AVAILABLE wo4 THEN wo4.tday = wo4.tday + fbstat.other-wpax[4] + fbstat.other-gpax[4].
        END.

        IF MONTH(fbstat.datum) = mm THEN
        DO:
            IF AVAILABLE wf1 THEN wf1.saldo = wf1.saldo + fbstat.food-wpax[1] + fbstat.food-gpax[1].
            IF AVAILABLE wf2 THEN wf2.saldo = wf2.saldo + fbstat.food-wpax[2] + fbstat.food-gpax[2].
            IF AVAILABLE wf3 THEN wf3.saldo = wf3.saldo + fbstat.food-wpax[3] + fbstat.food-gpax[3].
            IF AVAILABLE wf4 THEN wf4.saldo = wf4.saldo + fbstat.food-wpax[4] + fbstat.food-gpax[4].

            IF AVAILABLE wb1 THEN wb1.saldo = wb1.saldo + fbstat.bev-wpax[1] + fbstat.bev-gpax[1].
            IF AVAILABLE wb2 THEN wb2.saldo = wb2.saldo + fbstat.bev-wpax[2] + fbstat.bev-gpax[2].
            IF AVAILABLE wb3 THEN wb3.saldo = wb3.saldo + fbstat.bev-wpax[3] + fbstat.bev-gpax[3].
            IF AVAILABLE wb4 THEN wb4.saldo = wb4.saldo + fbstat.bev-wpax[4] + fbstat.bev-gpax[4].

            IF AVAILABLE wo1 THEN wo1.saldo = wo1.saldo + fbstat.other-wpax[1] + fbstat.other-gpax[1].
            IF AVAILABLE wo2 THEN wo2.saldo = wo2.saldo + fbstat.other-wpax[2] + fbstat.other-gpax[2].
            IF AVAILABLE wo3 THEN wo3.saldo = wo3.saldo + fbstat.other-wpax[3] + fbstat.other-gpax[3].
            IF AVAILABLE wo4 THEN wo4.saldo = wo4.saldo + fbstat.other-wpax[4] + fbstat.other-gpax[4].
        END.

        IF MONTH(fbstat.datum) = mm AND YEAR(fbstat.datum) = yy THEN
        DO:
            IF AVAILABLE wf1 THEN wf1.mon-saldo[DAY(fbstat.datum)] = wf1.mon-saldo[DAY(fbstat.datum)] + fbstat.food-wpax[1] + fbstat.food-gpax[1].
            IF AVAILABLE wf2 THEN wf2.mon-saldo[DAY(fbstat.datum)] = wf2.mon-saldo[DAY(fbstat.datum)] + fbstat.food-wpax[2] + fbstat.food-gpax[2].
            IF AVAILABLE wf3 THEN wf3.mon-saldo[DAY(fbstat.datum)] = wf3.mon-saldo[DAY(fbstat.datum)] + fbstat.food-wpax[3] + fbstat.food-gpax[3].
            IF AVAILABLE wf4 THEN wf4.mon-saldo[DAY(fbstat.datum)] = wf4.mon-saldo[DAY(fbstat.datum)] + fbstat.food-wpax[4] + fbstat.food-gpax[4].

            IF AVAILABLE wb1 THEN wb1.mon-saldo[DAY(fbstat.datum)] = wb1.mon-saldo[DAY(fbstat.datum)] + fbstat.bev-wpax[1] + fbstat.bev-gpax[1].
            IF AVAILABLE wb2 THEN wb2.mon-saldo[DAY(fbstat.datum)] = wb2.mon-saldo[DAY(fbstat.datum)] + fbstat.bev-wpax[2] + fbstat.bev-gpax[2].
            IF AVAILABLE wb3 THEN wb3.mon-saldo[DAY(fbstat.datum)] = wb3.mon-saldo[DAY(fbstat.datum)] + fbstat.bev-wpax[3] + fbstat.bev-gpax[3].
            IF AVAILABLE wb4 THEN wb4.mon-saldo[DAY(fbstat.datum)] = wb4.mon-saldo[DAY(fbstat.datum)] + fbstat.bev-wpax[4] + fbstat.bev-gpax[4].

            IF AVAILABLE wo1 THEN wo1.mon-saldo[DAY(fbstat.datum)] = wo1.mon-saldo[DAY(fbstat.datum)] + fbstat.other-wpax[1] + fbstat.other-gpax[1].
            IF AVAILABLE wo2 THEN wo2.mon-saldo[DAY(fbstat.datum)] = wo2.mon-saldo[DAY(fbstat.datum)] + fbstat.other-wpax[2] + fbstat.other-gpax[2].
            IF AVAILABLE wo3 THEN wo3.mon-saldo[DAY(fbstat.datum)] = wo3.mon-saldo[DAY(fbstat.datum)] + fbstat.other-wpax[3] + fbstat.other-gpax[3].
            IF AVAILABLE wo4 THEN wo4.mon-saldo[DAY(fbstat.datum)] = wo4.mon-saldo[DAY(fbstat.datum)] + fbstat.other-wpax[4] + fbstat.other-gpax[4].

        END.

        IF AVAILABLE wf1 THEN wf1.ytd-saldo = wf1.ytd-saldo + fbstat.food-wpax[1] + fbstat.food-gpax[1].
        IF AVAILABLE wf2 THEN wf2.ytd-saldo = wf2.ytd-saldo + fbstat.food-wpax[2] + fbstat.food-gpax[2].
        IF AVAILABLE wf3 THEN wf3.ytd-saldo = wf3.ytd-saldo + fbstat.food-wpax[3] + fbstat.food-gpax[3].
        IF AVAILABLE wf4 THEN wf4.ytd-saldo = wf4.ytd-saldo + fbstat.food-wpax[4] + fbstat.food-gpax[4].

        IF AVAILABLE wb1 THEN wb1.ytd-saldo = wb1.ytd-saldo + fbstat.bev-wpax[1] + fbstat.bev-gpax[1].
        IF AVAILABLE wb2 THEN wb2.ytd-saldo = wb2.ytd-saldo + fbstat.bev-wpax[2] + fbstat.bev-gpax[2].
        IF AVAILABLE wb3 THEN wb3.ytd-saldo = wb3.ytd-saldo + fbstat.bev-wpax[3] + fbstat.bev-gpax[3].
        IF AVAILABLE wb4 THEN wb4.ytd-saldo = wb4.ytd-saldo + fbstat.bev-wpax[4] + fbstat.bev-gpax[4].

        IF AVAILABLE wo1 THEN wo1.ytd-saldo = wo1.ytd-saldo + fbstat.other-wpax[1] + fbstat.other-gpax[1].
        IF AVAILABLE wo2 THEN wo2.ytd-saldo = wo2.ytd-saldo + fbstat.other-wpax[2] + fbstat.other-gpax[2].
        IF AVAILABLE wo3 THEN wo3.ytd-saldo = wo3.ytd-saldo + fbstat.other-wpax[3] + fbstat.other-gpax[3].
        IF AVAILABLE wo4 THEN wo4.ytd-saldo = wo4.ytd-saldo + fbstat.other-wpax[4] + fbstat.other-gpax[4].
    END.   
END.
END.

PROCEDURE fill-rmstat: 
DEFINE INPUT PARAMETER rec-w1   AS INTEGER. 
DEFINE INPUT PARAMETER key-word AS CHAR. 

DEFINE VARIABLE datum1     AS DATE. 
DEFINE VARIABLE curr-date  AS DATE. 
DEFINE VARIABLE d-flag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag AS LOGICAL NO-UNDO.

  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
  /*last month today*/
  IF (DAY(to-date) EQ 31 AND MONTH(to-date) NE 8 AND MONTH(to-date) NE 1)
    OR (DAY(to-date) EQ 30 AND MONTH(to-date) EQ 3)
    OR (DAY(DATE(3,1,YEAR(to-date)) - 1) EQ 28 AND MONTH(to-date) EQ 3 AND DAY(to-date) EQ 29) THEN
    w1.lm-today = 0.
  ELSE
  DO:
    IF MONTH(to-date) EQ 1 THEN
      curr-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
    ELSE
      curr-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)).
    FIND FIRST zinrstat WHERE zinrstat.datum = curr-date 
      AND zinrstat.zinr = key-word NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN
      w1.lm-today = zinrstat.zimmeranz.
  END.
  /*end last month today*/

  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 
  DO: 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = key-word NO-LOCK: 

      d-flag = (MONTH(zinrstat.datum) = MONTH(to-date))
               AND (YEAR(zinrstat.datum) = YEAR(to-date)).
      IF d-flag THEN w1.mon-saldo[DAY(zinrstat.datum)] 
        = w1.mon-saldo[DAY(zinrstat.datum)] + zinrstat.zimmeranz. 
      
      IF zinrstat.datum = to-date - 1  THEN w1.yesterday = w1.yesterday + zinrstat.zimmeranz. 
      IF zinrstat.datum = to-date THEN w1.tday = w1.tday + zinrstat.zimmeranz. 
      IF zinrstat.datum LT from-date THEN 
        w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo + zinrstat.zimmeranz. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = key-word NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
          w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
        ELSE 
        DO:
          dlmtd-flag = (MONTH(zinrstat.datum) = MONTH(to-date)) 
            AND (YEAR(zinrstat.datum) = YEAR(to-date) - 1).
          IF dlmtd-flag THEN w1.mon-lmtd[DAY(zinrstat.datum)] 
            = w1.mon-lmtd[DAY(zinrstat.datum)] + zinrstat.zimmeranz. 
          w1.lastyr = w1.lastyr + zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo + zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.zimmeranz. 
    END. 
    IF lytoday-flag THEN
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday 
        AND zinrstat.zinr = key-word NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN w1.lytoday = zinrstat.zimmeranz. 
    END.   
  END. 
  w1.done = YES. 
END. 

PROCEDURE fill-avrgLlodge: 
DEFINE INPUT PARAMETER rec-w1 AS INTEGER. 
DEFINE VARIABLE datum1 AS DATE. 
DEFINE BUFFER w11 FOR w1. 
 
  FIND FIRST w1 WHERE RECID(w1) = rec-w1. 
  IF w1.done THEN RETURN. 
 
  FIND FIRST w11 WHERE w11.main-code = 812 NO-ERROR. 
  IF AVAILABLE w11 AND w11.done THEN release w11. 
 
  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
      IF zinrstat.datum = to-date THEN 
      DO: 
        w1.tday = w1.tday + zinrstat.logisumsatz. 
        IF AVAILABLE w11 THEN w11.tday = w11.tday 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      END. 
      IF zinrstat.datum LT from-date THEN 
      DO: 
        w1.ytd-saldo = w1.ytd-saldo 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.ytd-saldo = w11.ytd-saldo 
          + zinrstat.argtumsatz / zinrstat.zimmeranz. 
      END. 
      ELSE 
      DO: 
        w1.saldo = w1.saldo + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF ytd-flag THEN w1.ytd-saldo = w1.ytd-saldo 
          + zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN 
        DO: 
          w11.saldo = w11.saldo + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          IF ytd-flag THEN w11.ytd-saldo = w11.ytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        END. 
      END. 
    END. 
    IF lytd-flag OR lmtd-flag THEN 
    DO: 
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
        AND zinrstat.datum LE Lto-date 
        AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
        IF zinrstat.datum LT Lfrom-date THEN 
        DO: 
          w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN w11.lytd-saldo = w11.lytd-saldo 
            + zinrstat.argtumsatz / zinrstat.zimmeranz. 
        END. 
        ELSE 
        DO: 
          w1.lastyr = w1.lastyr 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
          IF lytd-flag THEN w1.lytd-saldo = w1.lytd-saldo 
            + zinrstat.logisumsatz / zinrstat.zimmeranz. 
          IF AVAILABLE w11 THEN 
          DO: 
            w11.lastyr = w11.lastyr 
              + zinrstat.argtumsatz / zinrstat.zimmeranz. /* LAST year MTD */ 
            IF lytd-flag THEN w11.lytd-saldo = w11.lytd-saldo 
              + zinrstat.argtumsatz / zinrstat.zimmeranz. 
          END. 
        END. 
      END. 
    END. 
    IF pmtd-flag THEN /* previous MTD */ 
    FOR EACH zinrstat WHERE zinrstat.datum GE Pfrom-date 
      AND zinrstat.datum LE Pto-date 
      AND zinrstat.zinr = "avrgLrate" NO-LOCK: 
      w1.lastmon = w1.lastmon + zinrstat.logisumsatz / zinrstat.zimmeranz. 
      IF AVAILABLE w11 THEN 
        w11.lastmon = w11.lastmon + zinrstat.argtumsatz / zinrstat.zimmeranz. 
    END. 
    IF lytoday-flag THEN
    DO:
      FIND FIRST zinrstat WHERE zinrstat.datum EQ lytoday
        AND zinrstat.zinr = "avrgLrate" NO-LOCK NO-ERROR.
      IF AVAILABLE zinrstat THEN
      DO:
        w1.lytoday = zinrstat.logisumsatz / zinrstat.zimmeranz. 
        IF AVAILABLE w11 THEN w11.lytoday = zinrstat.argtumsatz / zinrstat.zimmeranz. 
      END.
    END.
  END. 
  w1.done = YES. 
  IF AVAILABLE w11 THEN w11.done = YES. 
END. 

PROCEDURE fill-source: 
DEFINE INPUT PARAMETER rec-w1  AS INTEGER. 
DEFINE INPUT PARAMETER main-nr AS INTEGER. 
DEFINE VARIABLE source-nr      AS INTEGER.
DEFINE VARIABLE mm             AS INTEGER.
DEFINE VARIABLE datum1         AS DATE. 
DEFINE VARIABLE curr-date      AS DATE. 
DEFINE VARIABLE ly-currdate    AS DATE. 
DEFINE VARIABLE ny-currdate    AS DATE. 
DEFINE VARIABLE njan1          AS DATE. 
DEFINE VARIABLE nmth1          AS DATE. 
DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.

DEFINE BUFFER sourcebuff   FOR sources.
DEFINE BUFFER sourcebuffny FOR sources.
DEFINE BUFFER genstatbuff  FOR genstat.

DEFINE BUFFER w11  FOR w1. 
DEFINE BUFFER w12  FOR w1. 
DEFINE BUFFER w13  FOR w1. 

FOR EACH tmp-room:
    DELETE tmp-room.
END.

FIND FIRST w1 WHERE RECID(w1) = rec-w1.
source-nr = w1.artnr.

ASSIGN
  njan1 = DATE(1,1,YEAR(to-date) + 1)
  nmth1 = DATE(MONTH(to-date),1, YEAR(to-date) + 1)
  mm    = MONTH(to-date).

IF MONTH(to-date) = 2 AND DAY(to-date) = 29 THEN
  ny-currdate = DATE(MONTH(to-date), 28, YEAR(to-date) + 1).
ELSE
  ny-currdate = DATE(MONTH(to-date), DAY(to-date), YEAR(to-date) + 1).

FIND FIRST sourcebuffny WHERE sourcebuffny.datum = ny-currdate 
  AND sourcebuffny.source-code = source-nr NO-LOCK NO-ERROR.     
IF AVAILABLE sourcebuffny THEN    
DO:
  IF main-nr = 9092 THEN    
    w1.ny-budget = sourcebuffny.budlogis.
  IF main-nr = 9813 THEN
     w1.ny-budget = sourcebuffny.budzimmeranz.
  IF main-nr = 9814 THEN
     w1.ny-budget = sourcebuffny.persanz.
END.

FOR EACH sourcebuffny WHERE sourcebuffny.datum GE njan1 AND 
  sourcebuffny.datum LE ny-currdate AND 
  sourcebuffny.source-code = source-nr NO-LOCK:
  IF main-nr = 9092 THEN    
    w1.nytd-budget = w1.nytd-budget + sourcebuffny.budlogis.
  IF main-nr = 9813 THEN
    w1.nytd-budget = w1.nytd-budget + sourcebuffny.budzimmeranz.
  IF main-nr = 9814 THEN
    w1.nytd-budget = w1.nytd-budget + sourcebuffny.budpersanz.
END.

FOR EACH sourcebuffny WHERE sourcebuffny.datum GE nmth1 AND 
  sourcebuffny.datum LE ny-currdate AND 
  sourcebuffny.source-code = source-nr NO-LOCK:
  IF main-nr = 9092 THEN    
    w1.nmtd-budget = w1.nmtd-budget + sourcebuffny.budlogis.
  IF main-nr = 9813 THEN
    w1.nmtd-budget = w1.nmtd-budget + sourcebuffny.budzimmeranz.
  IF main-nr = 9814 THEN
    w1.nmtd-budget = w1.nmtd-budget + sourcebuffny.budpersanz.
END.

FIND FIRST sources WHERE sources.datum = to-date - 1 
  AND sources.source-code = source-nr NO-LOCK NO-ERROR.     
IF AVAILABLE sources THEN
DO:
  IF main-nr = 9092 THEN
    w1.yesterday = sources.logis / frate. 
  ELSE IF main-nr = 9813 THEN
    w1.yesterday = sources.zimmeranz. 
  ELSE IF main-nr = 9814 THEN
    w1.yesterday = sources.persanz. 
END.

  DO: 
    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    FOR EACH genstat WHERE 
      genstat.datum GE datum1 AND genstat.datum LE to-date
      AND genstat.resstatus NE 13 
      AND genstat.nationnr NE 0
      AND genstat.segmentcode NE 0
      AND genstat.source EQ source-nr
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES NO-LOCK:
      ASSIGN
        frate  = 1
        d-flag = (MONTH(genstat.datum) = MONTH(to-date))
                 AND (YEAR(genstat.datum) = YEAR(to-date)).
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(genstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END.   
      IF genstat.datum EQ to-date THEN 
      DO: 
        FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
          AND tmp-room.zinr EQ genstat.zinr 
          AND tmp-room.flag = 1 NO-ERROR.
        IF NOT AVAILABLE tmp-room THEN
        DO:
          IF main-nr = 9813 THEN 
             w1.tday = w1.tday + 1.
          CREATE tmp-room.
          ASSIGN tmp-room.gastnr = genstat.gastnr
                 tmp-room.zinr = genstat.zinr
                 tmp-room.flag = 1.
        END.
        IF main-nr = 9814 THEN 
          w1.tday = w1.tday + genstat.erwachs 
                    + genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 9092 THEN
          w1.tday = w1.tday + genstat.logis / frate.
      END.
      IF MONTH(genstat.datum) = mm THEN
      DO:
        IF main-nr = 9092 THEN
        DO:
          IF d-flag THEN w1.mon-saldo[DAY(genstat.datum)] 
            = w1.mon-saldo[DAY(genstat.datum)] + genstat.logis / frate.
          w1.saldo = w1.saldo + genstat.logis / frate.
        END.
        IF main-nr = 9814 THEN 
        DO:
          IF d-flag THEN w1.mon-saldo[DAY(genstat.datum)] 
            = w1.mon-saldo[DAY(genstat.datum)] + genstat.erwachs +
              genstat.kind1 + genstat.kind2 + genstat.gratis.
          w1.saldo = w1.saldo + genstat.erwachs +
                     genstat.kind1 + genstat.kind2 + genstat.gratis.
        END.
        IF main-nr = 9813 THEN 
        DO:
          IF d-flag THEN w1.mon-saldo[DAY(genstat.datum)] 
            = w1.mon-saldo[DAY(genstat.datum)] + 1.
          w1.saldo = w1.saldo + 1.
        END.                                       
      END.
      IF main-nr = 9092 THEN
        w1.ytd-saldo = w1.ytd-saldo + genstat.logis / frate.
      IF main-nr = 9814 THEN 
        w1.ytd-saldo = w1.ytd-saldo + genstat.erwachs 
                  + genstat.kind1 + genstat.kind2 + genstat.gratis.
      IF main-nr = 9813 THEN 
        w1.ytd-saldo = w1.ytd-saldo + 1.
    END.

    FOR EACH tmp-room:
      DELETE tmp-room.
    END.
    IF lytd-flag OR lmtd-flag THEN
    DO:
      mm = MONTH(Lto-date).
      IF lytd-flag THEN datum1 = Ljan1. 
      ELSE datum1 = Lfrom-date. 
      FOR EACH genstat WHERE 
        genstat.datum GE datum1 AND genstat.datum LE Lto-date
        AND genstat.resstatus NE 13 
        AND genstat.nationnr NE 0
        AND genstat.segmentcode NE 0
        AND genstat.source EQ source-nr
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES NO-LOCK:
        dlmtd-flag = (MONTH(genstat.datum) = MONTH(Lto-date)) 
          AND (YEAR(genstat.datum) = YEAR(Lto-date)).
        IF foreign-flag THEN 
        DO: 
          RUN find-exrate(genstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
        END. 
        IF genstat.datum EQ Lto-date THEN 
        DO: 
          FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
            AND tmp-room.zinr EQ genstat.zinr 
            AND tmp-room.flag = 1 NO-ERROR.
          IF NOT AVAILABLE tmp-room THEN
          DO:
            IF main-nr = 9813 THEN 
              w1.lytoday = w1.lytoday + 1.
            CREATE tmp-room.
            ASSIGN tmp-room.gastnr = genstat.gastnr
                   tmp-room.zinr = genstat.zinr
                   tmp-room.flag = 1.
          END.
          IF main-nr = 9814 THEN 
            w1.lytoday = w1.lytoday + genstat.erwachs +
                         genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 9092 THEN
            w1.lytoday = w1.lytoday + genstat.logis / frate.
        END.
        IF MONTH(genstat.datum) = mm THEN
        DO:
          IF main-nr = 9092 THEN
            w1.lastyr = w1.lastyr + genstat.logis / frate.
          IF main-nr = 9814 THEN 
            w1.lastyr = w1.lastyr + genstat.erwachs +
                     genstat.kind1 + genstat.kind2 + genstat.gratis.
          IF main-nr = 9813 THEN 
            w1.lastyr = w1.lastyr + 1.
        END.
        IF main-nr = 9092 THEN
          w1.lytd-saldo = w1.lytd-saldo + genstat.logis / frate.
        IF main-nr = 9814 THEN 
          w1.lytd-saldo = w1.lytd-saldo + genstat.erwachs + 
                          genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF main-nr = 9813 THEN 
          w1.lytd-saldo = w1.lytd-saldo + 1.
      END.
    END.
    IF pmtd-flag THEN
    FOR EACH genstat WHERE 
      genstat.datum GE Pfrom-date AND genstat.datum LE Pto-date
      AND genstat.resstatus NE 13 
      AND genstat.nationnr NE 0
      AND genstat.segmentcode NE 0
      AND genstat.source EQ source-nr
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES NO-LOCK:
      IF foreign-flag THEN 
      DO: 
        RUN find-exrate(genstat.datum). 
        IF AVAILABLE exrate THEN frate = exrate.betrag. 
      END. 
      IF main-nr = 9092 THEN
        w1.lastmon = w1.lastmon + genstat.logis / frate.
      IF main-nr = 9814 THEN 
        w1.lastmon = w1.lastmon + genstat.erwachs + 
                     genstat.kind1 + genstat.kind2 + genstat.gratis.
      IF main-nr = 9813 THEN 
        w1.lastmon = w1.lastmon + 1.
    END.
  END. 
END.

PROCEDURE fill-value1: 
DEFINE INPUT PARAMETER recid1-w1 AS INTEGER. 
DEFINE INPUT PARAMETER recid2-w1 AS INTEGER. 
DEFINE INPUT PARAMETER val-sign AS INTEGER. 
DEFINE VARIABLE sign1 AS INTEGER. 
DEFINE BUFFER parent FOR w1. 
DEFINE BUFFER child FOR w1. 
DEFINE BUFFER curr-child FOR w1. 
DEFINE BUFFER curr-w2 FOR w2. 
DEFINE VARIABLE texte AS CHAR. 
DEFINE VARIABLE n AS INTEGER. 
  FIND FIRST parent WHERE RECID(parent) = recid1-w1. 
  FIND FIRST child WHERE RECID(child) = recid2-w1. 
  DO: 
    parent.tday = parent.tday + val-sign * child.tday. 
    parent.tbudget = parent.tbudget + val-sign * child.tbudget. 
 
    parent.saldo = parent.saldo + val-sign * child.saldo. 
    parent.budget = parent.budget + val-sign * child.budget. 
 
    parent.lytoday = parent.lytoday + val-sign * child.lytoday. 

    parent.lastmon = parent.lastmon + val-sign * child.lastmon. 
    parent.lm-budget = parent.lm-budget + val-sign * child.lm-budget. 
 
    parent.lastyr = parent.lastyr + val-sign * child.lastyr. 
    parent.ly-budget = parent.ly-budget + val-sign * child.ly-budget. 
 
    parent.ytd-saldo = parent.ytd-saldo + val-sign * child.ytd-saldo. 
    parent.ytd-budget = parent.ytd-budget + val-sign * child.ytd-budget. 
 
    parent.lytd-saldo = parent.lytd-saldo + val-sign * child.lytd-saldo. 
    parent.lytd-budget = parent.lytd-budget + val-sign * child.lytd-budget. 
  END. 
END. 

DEFINE VARIABLE prev-param AS CHAR.
DEFINE VARIABLE k          AS INT.
DEFINE VARIABLE j          AS INT.
DEFINE VARIABLE curr-row   AS INT.
DEFINE VARIABLE curr-col   AS INT.
DEFINE VARIABLE htl-no     AS CHAR.
DEFINE VARIABLE cell-value AS CHAR.
DEFINE STREAM s1.
DEF VAR ChCol       AS CHAR EXTENT 26 INITIAL
    ["A","B","C","D","E","F","G","H","I","J","K","L","M",
     "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"].

DEFINE VARIABLE dayname AS CHAR FORMAT "x(12)" EXTENT 7 INITIAL 
  ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]. 

FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
    RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 

OS-DELETE VALUE ("/usr1/vhp/tmp/outputFO_" + htl-no + ".txt").
OUTPUT STREAM s1 TO VALUE("/usr1/vhp/tmp/outputFO_" + htl-no + ".txt") APPEND UNBUFFERED.

/*OS-DELETE VALUE ("C:\e1-vhp\outputFO_" + htl-no + ".txt").
OUTPUT STREAM s1 TO VALUE("C:\e1-vhp\outputFO_" + htl-no + ".txt") APPEND UNBUFFERED.*/

FOR EACH parameters WHERE progname = "FO-macro"
    AND parameters.SECTION = STRING(briefnr) NO-LOCK BY parameters.varname:
    IF prev-param NE parameters.varname THEN
    DO:
        RUN convert-varname(parameters.varname, OUTPUT curr-row, OUTPUT curr-col).
        prev-param = parameters.varname.

        IF parameters.vtype NE 0 THEN
        DO:
            FIND FIRST w1 WHERE w1.varname = parameters.vstring NO-LOCK NO-ERROR.
            IF parameters.vtype GE 9150 AND parameters.vtype LE 9180 THEN 
            DO:

                k = 0.
                DO j = 9150 TO 9180:
                    k = k + 1.
                    IF parameters.vtype = j THEN
                    DO: 
                        cell-value = TRIM(STRING(w1.mon-saldo[k],"->>>>>>>>>>>9.99")).
                        LEAVE.
                    END.
                END.
            END.
            ELSE IF parameters.vtype GE 8120 AND parameters.vtype LE 8150 THEN 
            DO:
                k = 0.
                DO j = 8120 TO 8150:
                    k = k + 1.
                    IF parameters.vtype = j THEN
                    DO: 
                        cell-value = TRIM(STRING(w1.mon-lmtd[k],"->>>>>>>>>>>9.99")).
                        LEAVE.
                    END.
                END.
            END.
            ELSE IF parameters.vtype GE 9119 AND parameters.vtype LE 9149 THEN
            DO:
                k = 0.
                DO j = 9119 TO 9149:
                    k = k + 1.
                    IF parameters.vtype = j THEN
                    DO: 
                        cell-value = TRIM(STRING(w1.mon-budget[k],"->>>>>>>>>>>9.99")).
                        LEAVE.
                    END.
                END.  
            END.
            /*MG E478DD*/
            ELSE IF parameters.vtype GE 9231 AND parameters.vtype LE 9261 THEN
            DO:
              k = 0.
              DO j = 9231 TO 9261:
                k = k + 1.
                IF parameters.vtype = j THEN
                DO: 
                  cell-value = TRIM(STRING(w1.mon-serv[k],"->>>>>>>>>>>9.99")).
                  LEAVE.
                END.
              END.  
            END.
            ELSE IF parameters.vtype GE 9262 AND parameters.vtype LE 9292 THEN
            DO:
              k = 0.
              DO j = 9262 TO 9292:
                k = k + 1.
                IF parameters.vtype = j THEN
                DO: 
                  cell-value = TRIM(STRING(w1.mon-tax[k],"->>>>>>>>>>>9.99")).
                  LEAVE.
                END.
              END.  
            END.
            /*end MG*/
            ELSE IF parameters.vtype = 9197 THEN 
            DO:
                cell-value = TRIM(STRING(w1.ny-budget,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 9196 THEN 
            DO:
                cell-value = TRIM(STRING(w1.nmtd-budget,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 9195 THEN /*nytd-budget for rev by segment & room by segment*/
            DO:
                cell-value = TRIM(STRING(w1.nytd-budget,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 9199 THEN  /* YESTERDAY */ 
            DO: 
                cell-value = TRIM(STRING(w1.yesterday,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9198 THEN  /* last month today */ 
            DO: 
                cell-value = TRIM(STRING(w1.lm-today,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 9194 THEN  /* today-serv */ 
            DO: 
                cell-value = TRIM(STRING(w1.tday-serv,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9193 THEN  /* today-tax */ 
            DO: 
                cell-value = TRIM(STRING(w1.tday-tax,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9192 THEN  /* mtd-serv */ 
            DO: 
                cell-value = TRIM(STRING(w1.mtd-serv,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9191 THEN  /* mtd-tax */ 
            DO: 
                cell-value = TRIM(STRING(w1.mtd-tax,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9190 THEN  /* ytd-serv */ 
            DO: 
                cell-value = TRIM(STRING(w1.ytd-serv,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9189 THEN  /* ytd-tax */ 
            DO: 
                cell-value = TRIM(STRING(w1.ytd-tax,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 9188 THEN  /* lm-today-serv */ 
            DO: 
                cell-value = TRIM(STRING(w1.lm-today-serv,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9187 THEN  /* lm-today-tax */ 
            DO: 
                cell-value = TRIM(STRING(w1.lm-today-tax,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9186 THEN  /* pmtd-serv */ 
            DO: 
                cell-value = TRIM(STRING(w1.pmtd-serv,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9185 THEN  /* pmtd-tax */ 
            DO: 
                cell-value = TRIM(STRING(w1.pmtd-serv,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9184 THEN  /* lmtd-serv */ 
            DO:
                cell-value = TRIM(STRING(w1.lmtd-serv,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9183 THEN  /* lmtd-tax */ 
            DO: 
                cell-value = TRIM(STRING(w1.lmtd-tax,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 9182 THEN  /* FT 300113 lm-mtd */ 
            DO: 
                cell-value = TRIM(STRING(w1.lm-mtd,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 9181 THEN  /* FT 060313 lm-ytd */ 
            DO: 
                cell-value = TRIM(STRING(w1.lm-ytd,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 93 THEN  /* TODAY */ 
            DO: 
                cell-value = TRIM(STRING(w1.tday,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 94 THEN  /* Month TO DATE */ 
            DO: 
                cell-value = TRIM(STRING(w1.saldo,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 96 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lastmon,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 95 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.ytd-saldo,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 185 THEN  /* LAST YEAR TODAY */ 
            DO: 
                cell-value = TRIM(STRING(w1.lytoday,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 196 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lastyr,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 815 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lytd-saldo,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 816 THEN                               
            DO: 
                cell-value = TRIM(STRING(w1.tbudget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 817 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 819 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lm-budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 679 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.ly-budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 827 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.ly-budget,"->>>>>>>>>>>9.99")).
            END. 
             ELSE IF parameters.vtype = 843 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lytd-budget,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 828 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lytd-budget,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 818 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.ytd-budget,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 820 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.tday - w1.tbudget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 821 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.saldo - w1.budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 822 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lastmon - w1.lm-budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 2065 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lastyr - w1.ly-budget,"->>>>>>>>>>>9.99")).
            END.
            ELSE IF parameters.vtype = 2066 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.ytd-saldo - w1.ytd-budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 2067 THEN 
            DO: 
                RUN convert-diff(w1.saldo, w1.budget,OUTPUT cell-value). 
            END. 
            ELSE IF parameters.vtype = 2068 THEN 
            DO: 
                RUN convert-diff(w1.lastmon, w1.lm-budget, OUTPUT cell-value). 
            END. 
            ELSE IF parameters.vtype = 2069 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lastyr - w1.ly-budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 2043 THEN 
            DO: 
                RUN convert-diff(w1.ytd-saldo, w1.ytd-budget, OUTPUT cell-value). 
            END.
            ELSE IF parameters.vtype = 2044 THEN 
            DO:
                cell-value = TRIM(STRING(w1.lytd-saldo,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 2045 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lytd-budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 2046 THEN 
            DO: 
                cell-value = TRIM(STRING(w1.lytd-saldo - w1.lytd-budget,"->>>>>>>>>>>9.99")).
            END. 
            ELSE IF parameters.vtype = 2047 THEN 
            DO: 
                RUN convert-diff(w1.lytd-saldo, w1.lytd-budget, OUTPUT cell-value). 
            END.
        END.
        ELSE
        DO:
            IF parameters.vstring = "$exrate" THEN
            DO:
                cell-value = ch.
            END.
            ELSE IF parameters.vstring = "$weekday" THEN
            DO:
                cell-value = dayname[weekday(to-date)]. 
            END.
            ELSE IF parameters.vstring = "$today" THEN
            DO:
                cell-value = STRING(DAY(TODAY),"99") + "/" + STRING(MONTH(TODAY),"99") + "/" + STRING(YEAR(TODAY),"9999").
            END.
            ELSE IF parameters.vstring = "$to-date" THEN
            DO:
                cell-value = STRING(DAY(to-date),"99") + "/" + STRING(MONTH(to-date),"99") + "/" + STRING(YEAR(to-date),"9999").
            END.
            ELSE IF parameters.vstring = "$month-str" THEN
            DO:
                cell-value = month-str[MONTH(to-date)].
            END.
            ELSE IF parameters.vstring = "$to-date1" THEN
            DO:
                cell-value = STRING(DAY(to-date),"99") + "-" + month-str[MONTH(to-date)] + "-" + STRING(YEAR(to-date),"9999").
            END.
        END.
        
        CREATE stream-list.
        ASSIGN
            stream-list.crow = curr-row
            stream-list.ccol = curr-col
            stream-list.cval = cell-value
        .
    END.
END.

FOR EACH stream-list NO-LOCK BY stream-list.ccol BY stream-list.crow:
    IF stream-list.cval NE "" THEN
        PUT STREAM s1 UNFORMATTED 
            STRING(stream-list.crow) ";" STRING(stream-list.ccol) ";" stream-list.cval SKIP.
    ELSE
        PUT STREAM s1 UNFORMATTED 
            STRING(stream-list.crow) ";" STRING(stream-list.ccol) ";" "''" SKIP.
END.

OUTPUT STREAM s1 CLOSE.


/*OS-COMMAND SILENT VALUE ("C:\e1-vhp\PHP\PHP.exe c:\e1-vhp\PHP-script\write-sheet.php C:\e1-vhp\outputFO_" + htl-no + ".txt " + link).*/
/*OS-COMMAND SILENT VALUE ("c:\e1-vhp\PHP-script\write-sheet.php C:\e1-vhp\outputFO_" + htl-no + ".txt " + link).*/

OS-COMMAND SILENT VALUE ("php /usr1/vhp/php-script/write-sheet.php /usr1/vhp/tmp/outputFO_" + htl-no + ".txt " + link).
/*OS-DELETE VALUE ("/usr1/vhp/tmp/outputFO_" + htl-no + ".txt").*/

PROCEDURE convert-varname:
    DEFINE INPUT PARAMETER str AS CHARACTER.
    DEFINE OUTPUT PARAMETER crow AS INTEGER.
    DEFINE OUTPUT PARAMETER ccol AS INTEGER.

    DEFINE VARIABLE loop-str AS INTEGER INIT 0.
    DEFINE VARIABLE loop-col AS INTEGER INIT 0.
    DEFINE VARIABLE found AS LOGICAL INIT NO.

    DEFINE VARIABLE str-col AS CHARACTER.
    DEFINE VARIABLE str-row AS CHARACTER.

    DO loop-str = 1 TO LENGTH(str):
        found = NO.
        DO loop-col = 1 TO 26:
            IF SUBSTR(str,loop-str,1) = chcol[loop-col] THEN
            DO:
                found = YES.
                LEAVE.
            END.
        END.
        IF found THEN str-col = str-col + SUBSTR(str,loop-str,1).
        ELSE str-row = str-row + SUBSTR(str,loop-str,1).
    END.

    RUN get-columnno(INPUT str-col, OUTPUT ccol).
    crow = INT(str-row).
END.

PROCEDURE get-columnNo:
DEF INPUT PARAMETER last-column AS CHAR.
DEF OUTPUT PARAMETER ind        AS INTEGER INITIAL 1.
DEF VAR i                       AS INTEGER.
DEF VAR ind1                    AS INTEGER.
DEF VAR ind2                    AS INTEGER. 
  IF LENGTH(last-column) = 2 THEN   /*FT130513*/
  DO:
    DO i = 1 TO 26:
      IF chCol[i] = SUBSTRING(last-column,1,1) THEN
      DO:
        ind1 = i * 26.
        LEAVE.
      END.    
    END.
    DO i = 1 TO 26:
      IF chCol[i] = SUBSTRING(last-column,2,1) THEN 
      DO:
        ind2 = i.
        LEAVE.
      END.    
    END.
    ind = ind1 + ind2.
  END.
  ELSE 
    DO i = 1 TO 26:
      IF chCol[i] = last-column THEN
      DO:
        ind = i.
        LEAVE.
      END.
    END.
END.

 
PROCEDURE convert-diff: 
DEFINE INPUT PARAMETER v1 AS DECIMAL. 
DEFINE INPUT PARAMETER v2 AS DECIMAL. 
DEFINE OUTPUT PARAMETER s AS CHAR FORMAT "x(20)" INITIAL "". 
DEFINE VARIABLE balance AS DECIMAL. 
DEFINE VARIABLE b AS DECIMAL. 
DEFINE VARIABLE rs AS CHAR FORMAT "x(7)". 
    
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


