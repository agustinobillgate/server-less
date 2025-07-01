
DEFINE TEMP-TABLE pr-list 
    FIELD cstr    AS CHAR FORMAT "x(1)" EXTENT 2 INITIAL ["", "*"] 
    FIELD prcode  AS CHAR 
    FIELD rmcat   AS CHAR FORMAT "x(10)"  LABEL "RmCat " /*"x(6)" wen 070819*/
    FIELD argt    AS CHAR FORMAT "x(27)" LABEL "Arrangement" 
    FIELD zikatnr AS INTEGER 
    FIELD argtnr  AS INTEGER 
    FIELD i-typ   AS INTEGER INIT 0
    FIELD flag    AS INTEGER INITIAL 0  /* 0 = NOT selected */ 
.
DEFINE TEMP-TABLE prbuff    LIKE pr-list.
DEFINE TEMP-TABLE t-prtable LIKE prtable. 

DEF INPUT PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER select-mode AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER prcode      AS CHAR             NO-UNDO.
DEF INPUT PARAMETER market-no   AS INTEGER          NO-UNDO.

DEF INPUT PARAMETER TABLE  FOR prbuff.
DEF INPUT PARAMETER TABLE  FOR pr-list.

DEF OUTPUT PARAMETER msg-str    AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER error-flag AS LOGICAL INIT YES NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ratecode-admin".
DEF VAR chcode  AS CHAR NO-UNDO. /*Naufal - add variable to store child ratecode*/

FIND FIRST prbuff NO-ERROR.
IF select-mode = 0 THEN RUN check-deselect.
ELSE RUN check-select.
IF error-flag THEN RETURN.

RUN update-select-list.

PROCEDURE check-deselect:
  IF prbuff.flag = 0 THEN 
  DO: 
    msg-str =translateExtended ("Product was not selected",lvCAREA,"").
    RETURN. 
  END. 
  FIND FIRST ratecode WHERE ratecode.argtnr = prbuff.argtnr 
      AND ratecode.zikatnr = prbuff.zikatnr 
      AND ratecode.code = prbuff.prcode 
      AND ratecode.marknr = market-no NO-LOCK NO-ERROR. 
  IF AVAILABLE ratecode THEN 
  DO: 
    msg-str = translateExtended ("Rates exist with Code = ",lvCAREA,"") + ratecode.code 
        + ", deselecting not possible.".
    RETURN. 
  END. 
  FIND FIRST pr-list WHERE pr-list.zikatnr = prbuff.zikatnr
      AND pr-list.argtnr = prbuff.argtnr NO-ERROR.
  IF AVAILABLE pr-list THEN
    ASSIGN pr-list.flag = 0.

  /*Naufal - add auto-deselect rmtype for child when parent select rmtype*/
  FOR EACH queasy WHERE queasy.KEY EQ 2 AND NOT queasy.logi2
    AND NUM-ENTRIES(queasy.char3, ";") GT 2
    AND ENTRY(2, queasy.char3, ";") EQ prcode NO-LOCK:
    
    FIND FIRST pr-list WHERE pr-list.zikatnr = prbuff.zikatnr 
        AND pr-list.argtnr = prbuff.argtnr NO-ERROR.
    IF AVAILABLE pr-list THEN
        ASSIGN pr-list.flag = 0.
  END.
  /*end*/
  error-flag = NO.
END.

PROCEDURE check-select:
  IF prbuff.flag = 1 THEN 
  DO: 
    msg-str = translateExtended ("Product has been selected",lvCAREA,"").
    RETURN.
  END. 
  FIND FIRST pr-list WHERE pr-list.zikatnr = prbuff.zikatnr 
    AND pr-list.argtnr = prbuff.argtnr NO-ERROR.
  IF AVAILABLE pr-list THEN
    ASSIGN pr-list.flag = 1.

  /*Naufal - add auto-select rmtype for child when parent select rmtype*/
  FOR EACH queasy WHERE queasy.KEY EQ 2 AND NOT queasy.logi2
    AND NUM-ENTRIES(queasy.char3, ";") GT 2
    AND ENTRY(2, queasy.char3, ";") EQ prcode NO-LOCK:
    
    FIND FIRST pr-list WHERE pr-list.zikatnr = prbuff.zikatnr 
        AND pr-list.argtnr = prbuff.argtnr.
    ASSIGN pr-list.flag = 1.
  END.
  /*end*/
  error-flag = NO.
END.

PROCEDURE update-select-list: 
DEFINE VARIABLE i       AS INTEGER NO-UNDO. 
DEFINE VARIABLE i-fact  AS INTEGER NO-UNDO.
DEFINE BUFFER prtable0  FOR prtable.
DEFINE BUFFER qbuff18   FOR queasy.
DEFINE BUFFER wbuff     FOR waehrung.

  FIND FIRST prtable0 WHERE prtable0.marknr = market-no 
    AND prtable0.prcode = "" NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE prtable0 THEN
  DO:
    msg-str = translateExtended ("prtable record not available for market segment",lvCAREA,"")
      + " " + STRING(market-no).
    error-flag = YES.
    RETURN.
  END.

  FIND FIRST prtable WHERE prtable.prcode = prcode
    /*AND prtable.nr = market-no*/ AND prtable.marknr = market-no EXCLUSIVE-LOCK NO-ERROR.
  IF NOT AVAILABLE prtable THEN 
  DO: 
    CREATE prtable. 
    ASSIGN
      prtable.prcode = prcode 
      prtable.nr     = market-no
      prtable.marknr = market-no
    .
  END. 
    
  DO i = 1 TO 99: 
      ASSIGN
        prtable.product[i] = 0 
        prtable.zikatnr[i] = prtable0.zikatnr[i]
        prtable.argtnr[i]  = prtable0.argtnr[i]
      . 
  END. 
  i = 0. 
  FOR EACH pr-list WHERE pr-list.flag = 1 BY pr-list.argtnr: 
      ASSIGN
          i      = i + 1
          i-fact = 0
      . 
/* SY 28/07/2014 
   assume total number of rmtype never GE 90
*/
      /* FD Comment => ORIGINAL
      IF pr-list.zikatnr LT 10 THEN i-fact = 90.
          prtable.product[i] = (i-fact + pr-list.zikatnr) * 1000 
                             + pr-list.argtnr. 
      */

      /*FD August 18, 2022 => Ticket FAF793*/
      IF pr-list.argtnr LE 999 THEN
      DO:
          IF pr-list.zikatnr LT 10 THEN i-fact = 90.
          prtable.product[i] = (i-fact + pr-list.zikatnr) * 1000 
                             + pr-list.argtnr. 
      END.
      ELSE
      DO:
          IF pr-list.zikatnr LT 10 THEN i-fact = 90.
          prtable.product[i] = (i-fact + pr-list.zikatnr) * 10000 
                             + pr-list.argtnr. 
      END.

/*
      IF pr-list.argtnr LT 100 THEN 
        prtable.product[i] = pr-list.zikatnr * 100 + pr-list.argtnr. 
      ELSE prtable.product[i] = pr-list.zikatnr * 1000 + pr-list.argtnr. 
*/  
  END. 
  FIND CURRENT prtable NO-LOCK. 
  RELEASE prtable.

  /*Naufal - add child's rmtype to table*/
  FOR EACH queasy WHERE queasy.KEY EQ 2 AND NOT queasy.logi2
    AND NUM-ENTRIES(queasy.char3, ";") GT 2
    AND ENTRY(2, queasy.char3, ";") EQ prcode NO-LOCK:

    FIND FIRST prtable WHERE prtable.prcode = queasy.char1
        /*AND prtable.nr = market-no*/ AND prtable.marknr = market-no EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE prtable THEN 
    DO: 
        CREATE prtable. 
        ASSIGN
            prtable.prcode = queasy.char1 
            prtable.nr     = market-no
            prtable.marknr = market-no.
    END.

    DO i = 1 TO 99: 
        ASSIGN
            prtable.product[i] = 0 
            prtable.zikatnr[i] = prtable0.zikatnr[i]
            prtable.argtnr[i]  = prtable0.argtnr[i]. 
    END.

    i = 0. 
    FOR EACH pr-list WHERE pr-list.flag = 1 BY pr-list.argtnr: 
        ASSIGN
            i      = i + 1
            i-fact = 0. 
    /* SY 28/07/2014 
       assume total number of rmtype never GE 90
    */
        IF pr-list.zikatnr LT 10 THEN i-fact = 90.
        prtable.product[i] = (i-fact + pr-list.zikatnr) * 1000 
            + pr-list.argtnr. 
    /*
          IF pr-list.argtnr LT 100 THEN 
            prtable.product[i] = pr-list.zikatnr * 100 + pr-list.argtnr. 
          ELSE prtable.product[i] = pr-list.zikatnr * 1000 + pr-list.argtnr. 
    */  
    END. 
    FIND CURRENT prtable NO-LOCK.
    RELEASE prtable.
  END.
  /*end*/
  /*
  FIND FIRST prtable WHERE prtable.prcode = chcode
    AND prtable.nr = market-no EXCLUSIVE-LOCK NO-ERROR.
  IF NOT AVAILABLE prtable THEN 
  DO: 
    CREATE prtable. 
    ASSIGN
      prtable.prcode = chcode 
      prtable.nr     = market-no
      prtable.marknr = market-no
    .
  END. 
    
  DO i = 1 TO 99: 
        ASSIGN
            prtable.product[i] = 0 
            prtable.zikatnr[i] = prtable0.zikatnr[i]
            prtable.argtnr[i]  = prtable0.argtnr[i]. 
  END. 
  i = 0. 
  FOR EACH pr-list WHERE pr-list.flag = 1 BY pr-list.argtnr: 
      ASSIGN
          i      = i + 1
          i-fact = 0
      . 
/* SY 28/07/2014 
   assume total number of rmtype never GE 90
*/
      IF pr-list.zikatnr LT 10 THEN i-fact = 90.
      prtable.product[i] = (i-fact + pr-list.zikatnr) * 1000 
                         + pr-list.argtnr. 
/*
      IF pr-list.argtnr LT 100 THEN 
        prtable.product[i] = pr-list.zikatnr * 100 + pr-list.argtnr. 
      ELSE prtable.product[i] = pr-list.zikatnr * 1000 + pr-list.argtnr. 
*/  
  END. 
  FIND CURRENT prtable NO-LOCK.
  */
  
  FIND FIRST qbuff18 WHERE qbuff18.KEY = 18 
      AND qbuff18.number1 = prtable.nr 
      AND qbuff18.char3 NE "" NO-LOCK NO-ERROR.
  IF AVAILABLE qbuff18 THEN
  DO:
      FIND FIRST wbuff WHERE wbuff.wabkurz = qbuff18.char3 NO-LOCK NO-ERROR.
      IF AVAILABLE wbuff THEN
      DO:
        FIND FIRST queasy WHERE queasy.KEY = 2
          AND queasy.char1 = prcode EXCLUSIVE-LOCK.
        ASSIGN queasy.number1 = wbuff.waehrungsnr.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
      END.
  END.
END. 
