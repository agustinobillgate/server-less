/*FT 080514 perbaikan tamplian browse*/
DEFINE TEMP-TABLE str-list 
  FIELD nebenstelle AS CHAR FORMAT "x(6)"
  FIELD zero-rate   AS LOGICAL INITIAL NO 
  FIELD local       AS DECIMAL 
  FIELD ldist       AS DECIMAL 
  FIELD ovsea       AS DECIMAL 
  FIELD s           AS CHAR FORMAT "x(135)". 

DEFINE TEMP-TABLE cost-list 
  FIELD num    AS INTEGER FORMAT "9999" 
  FIELD name   AS CHAR   FORMAT "x(24)". 


DEFINE INPUT-OUTPUT PARAMETER TABLE FOR cost-list.
DEFINE INPUT        PARAMETER sorttype      AS INTEGER.
DEFINE INPUT        PARAMETER cost-center   AS INTEGER.
DEFINE INPUT        PARAMETER to-cc         AS INTEGER.
DEFINE INPUT        PARAMETER price-decimal AS INTEGER.
DEFINE INPUT        PARAMETER from-date     AS DATE.
DEFINE INPUT        PARAMETER to-date       AS DATE.
DEFINE INPUT        PARAMETER double-currency AS LOGICAL.

DEFINE OUTPUT       PARAMETER stattype     AS INTEGER.
DEFINE OUTPUT       PARAMETER TABLE FOR str-list.

DEFINE VARIABLE amount1 AS DECIMAL. 
DEFINE VARIABLE amount2 AS DECIMAL. 
DEFINE VARIABLE t-local AS DECIMAL. 
DEFINE VARIABLE t-ldist AS DECIMAL. 
DEFINE VARIABLE t-ovsea AS DECIMAL.
DEFINE VARIABLE curr-bezeich AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE last-sort   AS INTEGER INITIAL 2.
DEFINE VARIABLE prstr AS CHAR FORMAT "x(3)" EXTENT 2 INITIAL ["NO", "YES"]. 


IF sorttype = 0 THEN RUN create-list. 
ELSE RUN create-list1.


PROCEDURE create-list: 
DEFINE VARIABLE last-dept   AS INTEGER INITIAL 0. 
DEFINE VARIABLE last-ext    AS CHAR. 
DEFINE VARIABLE ext-amt1    AS DECIMAL. 
DEFINE VARIABLE ext-amt2    AS DECIMAL. 
DEFINE VARIABLE dept-amt1   AS DECIMAL. 
DEFINE VARIABLE dept-amt2   AS DECIMAL. 
DEFINE VARIABLE ext-local   AS DECIMAL. 
DEFINE VARIABLE ext-ldist   AS DECIMAL. 
DEFINE VARIABLE ext-ovsea   AS DECIMAL. 
DEFINE VARIABLE dept-local  AS DECIMAL. 
DEFINE VARIABLE dept-ldist  AS DECIMAL. 
DEFINE VARIABLE dept-ovsea  AS DECIMAL. 
DEFINE VARIABLE from-cost   AS INTEGER. 
DEFINE VARIABLE to-cost     AS INTEGER. 
DEFINE VARIABLE i           AS INTEGER. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  IF cost-center = 0 THEN 
  DO: 
    from-cost = 0. 
    to-cost = 9999. 
  END. 
  ELSE 
  DO: 
    from-cost = cost-center. 
    IF to-cc LT cost-center THEN to-cost = cost-center. 
    ELSE to-cost = to-cc. 
  END. 
 
  amount1 = 0. 
  amount2 = 0. 
  t-local = 0. 
  t-ldist = 0. 
  t-ovsea = 0. 
 
  IF last-sort = 2 THEN /* BY Extension */ 
  DO: 
    FOR EACH nebenst WHERE nebenst.departement NE 0 NO-LOCK, 
      FIRST cost-list WHERE cost-list.num = nebenst.departement 
      AND cost-list.num GE from-cost AND cost-list.num LE to-cost NO-LOCK 
      BY nebenst.departement BY nebenst.nebenstelle: 
      
      IF nebenst.nebstart = 0 OR nebenst.nebstart = 1 THEN stattype = 1. 
      ELSE stattype = 0. 
 
      IF last-dept NE cost-list.num THEN 
      DO: 
        IF last-dept NE 0 THEN 
        DO: 
          create str-list. 
          str-list.local = dept-local. 
          str-list.ldist = dept-ldist. 
          str-list.ovsea = dept-ovsea. 
          DO i = 1 TO 19: 
            str-list.s = str-list.s + " ". 
          END. 
          str-list.s = str-list.s 
            + STRING(("TOTAL DEPT - " + STRING(last-dept,"9999")), "x(40)"). 
          IF price-decimal = 0 THEN 
          DO: 
            IF dept-amt1 LE 999999999 THEN 
              str-list.s = str-list.s + STRING(dept-amt1,    ">,>>>,>>>,>>9"). 
            ELSE str-list.s = str-list.s + STRING(dept-amt1, ">>>>>>>>>>>>9"). 
          END. 
          ELSE 
          str-list.s = str-list.s + STRING(dept-amt1,   ">>,>>>,>>9.99"). 
          IF double-currency OR price-decimal NE 0 THEN 
            str-list.s = str-list.s + STRING(dept-amt2,   ">>,>>>,>>9.99"). 
          ELSE 
          DO: 
            IF dept-amt2 LE 999999999 THEN 
              str-list.s = str-list.s + STRING(dept-amt2,    ">>,>>,>>>,>>9"). 
            ELSE str-list.s = str-list.s + STRING(dept-amt2, ">>>>>>>>>>>>9"). 
          END. 
          create str-list. 
        END. 
        create str-list. 
        DO i = 1 TO 19: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s 
          + STRING(STRING(cost-list.num,"9999") + " - " 
          + cost-list.name, "x(24)"). 
        last-dept = cost-list.num. 
        dept-amt1 = 0. 
        dept-amt2 = 0. 
        dept-local = 0. 
        dept-ldist = 0. 
        dept-ovsea = 0. 
      END. 
 
/** Print Total per extension **/ 
      last-ext = "". 
      ext-amt1 = 0. 
      ext-amt2 = 0. 
      ext-local = 0. 
      ext-ldist = 0. 
      ext-ovsea = 0. 
 
      FOR EACH calls WHERE calls.key = 1 /*AND calls.buchflag = stattype */
        AND calls.nebenstelle = nebenst.nebenstelle 
        AND calls.datum GE from-date AND calls.datum LE to-date 
        AND calls.zeit GE 0 
        /* Dzikri - 32213C : Remove indexing for faster results
        USE-INDEX key-book-nebst_ix 
         */
        NO-LOCK BY calls.nebenstelle 
        BY calls.datum descending BY calls.zeit descending: 
/* 
        FIND FIRST s-list WHERE s-list.ext = calls.nebenstelle NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
            CREATE s-list. 
            s-list.ext = calls.nebenstelle. 
        END. 
        s-list.s2 = s-list.s2 + calls.pabxbetrag. 
*/ 
        
        IF last-ext = "" THEN last-ext = calls.nebenstelle. 
        IF last-ext NE calls.nebenstelle THEN 
        DO: 
          create str-list. 
          str-list.local = ext-local. 
          str-list.ldist = ext-ldist. 
          str-list.ovsea = ext-ovsea. 
          DO i = 1 TO 19: 
            str-list.s = str-list.s + " ". 
          END. 
          str-list.s = str-list.s 
            + STRING(("TOTAL EXT. - " + last-ext), "x(40)"). 
          IF price-decimal = 0 THEN 
          DO: 
            IF ext-amt1 LE 999999999 THEN 
              str-list.s = str-list.s + STRING(ext-amt1,    ">,>>>,>>>,>>9"). 
            ELSE str-list.s = str-list.s + STRING(ext-amt1, ">>>>>>>>>>>>9"). 
          END. 
          ELSE 
          str-list.s = str-list.s + STRING(ext-amt1,        ">>,>>>,>>9.99"). 
          IF double-currency OR price-decimal NE 0 THEN 
            str-list.s = str-list.s + STRING(ext-amt2,      ">>,>>>,>>9.99"). 
          ELSE 
          DO: 
            IF ext-amt2 LE 999999999 THEN 
              str-list.s = str-list.s + STRING(ext-amt2,    ">,>>>,>>>,>>9"). 
            ELSE str-list.s = str-list.s + STRING(ext-amt2, ">>>>>>>>>>>>9"). 
          END. 
          create str-list. 
          last-ext = calls.nebenstelle. 
          ASSIGN
            ext-amt1  = 0 
            ext-amt2  = 0 
            ext-local = 0 
            ext-ldist = 0 
            ext-ovsea = 0
          . 
        END. 
        ext-amt1 = ext-amt1 + calls.pabxbetrag. 
        ext-amt2 = ext-amt2 + calls.gastbetrag. 
        dept-amt1 = dept-amt1 + calls.pabxbetrag. 
        dept-amt2 = dept-amt2 + calls.gastbetrag. 
 
        IF SUBSTR(calls.rufnummer,1,1) NE "0" THEN 
        DO: 
          ext-local = ext-local + calls.pabxbetrag. 
          dept-local = dept-local + calls.pabxbetrag. 
        END. 
        ELSE IF SUBSTR(calls.rufnummer,1,2) EQ "00" THEN 
        DO: 
          ext-ovsea = ext-ovsea + calls.pabxbetrag. 
          dept-ovsea = dept-ovsea + calls.pabxbetrag. 
        END. 
        ELSE DO: 
          ext-ldist = ext-ldist + calls.pabxbetrag. 
          dept-ldist = dept-ldist + calls.pabxbetrag. 
        END. 
 
        RUN create-record. 
 
      END. 
      IF last-ext NE "" THEN 
      DO: 
        create str-list. 
        str-list.local = ext-local. 
        str-list.ldist = ext-ldist. 
        str-list.ovsea = ext-ovsea. 
        DO i = 1 TO 19: 
          str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s 
          + STRING(("TOTAL EXT. - " + last-ext), "x(40)"). 
        IF price-decimal = 0 THEN 
        DO: 
          IF ext-amt1 LE 999999999 THEN 
            str-list.s = str-list.s + STRING(ext-amt1,    ">,>>>,>>>,>>9"). 
          ELSE str-list.s = str-list.s + STRING(ext-amt1, ">>>>>>>>>>>>9"). 
        END. 
        ELSE str-list.s = str-list.s + STRING(ext-amt1,   ">>,>>>,>>9.99"). 
        IF double-currency OR price-decimal NE 0 THEN 
         str-list.s = str-list.s + STRING(ext-amt2,       ">>,>>>,>>9.99"). 
        ELSE 
        DO: 
          IF ext-amt2 LE 999999999 THEN 
            str-list.s = str-list.s + STRING(ext-amt2,    ">,>>>,>>>,>>9"). 
          ELSE str-list.s = str-list.s + STRING(ext-amt2, ">>>>>>>>>>>>9"). 
        END. 
        create str-list. 
      END. 
    END. 
  END. 
  create str-list. 
  str-list.local = dept-local. 
  str-list.ldist = dept-ldist. 
  str-list.ovsea = dept-ovsea. 
  DO i = 1 TO 19: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s 
    + STRING(("TOTAL DEPT - " + STRING(last-dept,"9999")), "x(40)"). 
  IF price-decimal = 0 THEN 
  DO: 
    IF dept-amt1 LE 999999999 THEN 
      str-list.s = str-list.s + STRING(dept-amt1,    ">,>>>,>>>,>>9"). 
    ELSE str-list.s = str-list.s + STRING(dept-amt1, ">>>>>>>>>>>>9"). 
  END. 
  ELSE str-list.s = str-list.s + STRING(dept-amt1,   ">>,>>>,>>9.99"). 
  IF double-currency OR price-decimal NE 0 THEN 
    str-list.s = str-list.s + STRING(dept-amt2,      ">>,>>>,>>9.99"). 
  ELSE 
  DO: 
    IF dept-amt2 LE 999999999 THEN 
      str-list.s = str-list.s + STRING(dept-amt2,    ">,>>>,>>>,>>9"). 
    ELSE str-list.s = str-list.s + STRING(dept-amt2, ">>>>>>>>>>>>9"). 
  END. 
  create str-list. 
 
  create str-list. 
  str-list.local = t-local. 
  str-list.ldist = t-ldist. 
  str-list.ovsea = t-ovsea. 
  DO i = 1 TO 19: 
    str-list.s = str-list.s + " ". 
  END. 
  str-list.s = str-list.s + STRING("GRAND TOTAL", "x(40)"). 
  IF price-decimal = 0 THEN 
  DO: 
    IF amount1 LE 999999999 THEN 
       str-list.s = str-list.s + STRING(amount1,   ">,>>>,>>>,>>9"). 
    ELSE str-list.s = str-list.s + STRING(amount1, ">>??>>>>>>>>9"). 
  END. 
  ELSE str-list.s = str-list.s + STRING(amount1,   ">>,>>>,>>9.99"). 
 
  IF double-currency OR price-decimal NE 0 THEN 
   str-list.s = str-list.s + STRING(amount2,       ">>,>>>,>>9.99"). 
  ELSE 
  DO: 
    IF amount2 LE 999999999 THEN 
       str-list.s = str-list.s + STRING(amount2,   ">,>>>,>>>,>>9"). 
    ELSE str-list.s = str-list.s + STRING(amount2, ">>>>>>>>>>>>9"). 
  END.
END. 

PROCEDURE create-list1: 
DEFINE VARIABLE last-dept   AS INTEGER INITIAL 0. 
DEFINE VARIABLE last-ext    AS CHAR. 
DEFINE VARIABLE ext-amt1    AS DECIMAL. 
DEFINE VARIABLE ext-amt2    AS DECIMAL. 
DEFINE VARIABLE dept-amt1   AS DECIMAL. 
DEFINE VARIABLE dept-amt2   AS DECIMAL. 
DEFINE VARIABLE ext-local   AS DECIMAL. 
DEFINE VARIABLE ext-ldist   AS DECIMAL. 
DEFINE VARIABLE ext-ovsea   AS DECIMAL. 
DEFINE VARIABLE dept-local  AS DECIMAL. 
DEFINE VARIABLE dept-ldist  AS DECIMAL. 
DEFINE VARIABLE dept-ovsea  AS DECIMAL. 
DEFINE VARIABLE from-cost   AS INTEGER. 
DEFINE VARIABLE to-cost     AS INTEGER. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE usr-amt1    AS DECIMAL.
DEFINE VARIABLE usr-amt2    AS DECIMAL.
DEFINE VARIABLE it-exist    AS LOGICAL INITIAL NO.
DEFINE VARIABLE dept-exist  AS LOGICAL INITIAL NO.
DEFINE VARIABLE temp-no     AS INTEGER FORMAT ">>>9".
DEFINE VARIABLE curr-user   AS CHAR INITIAL "Not defined".
DEFINE VARIABLE do-it       AS LOGICAL.

  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  IF cost-center = 0 THEN 
  DO: 
    from-cost = 0. 
    to-cost = 9999. 
  END. 
  ELSE 
  DO: 
    from-cost = cost-center. 
    IF to-cc LT cost-center THEN to-cost = cost-center. 
    ELSE to-cost = to-cc. 
  END. 
 
  ASSIGN
    amount1    = 0
    amount2    = 0 
    t-local    = 0 
    t-ldist    = 0 
    t-ovsea    = 0 
    ext-local  = 0 
    ext-ldist  = 0 
    ext-ovsea  = 0 
    ext-amt1   = 0
    ext-amt2   = 0
  .

  FOR EACH calls WHERE calls.KEY = 1
    AND calls.datum GE from-date AND calls.datum LE to-date
    AND calls.zeit GE 0 NO-LOCK BY calls.aufschlag BY calls.datum DESCENDING
    BY calls.zeit DESCENDING:
    FIND FIRST nebenst WHERE nebenst.nebenstelle = calls.nebenstelle
        NO-LOCK NO-ERROR.
    do-it = AVAILABLE nebenst 
      AND nebenst.departement GE from-cost 
      AND nebenst.departement LE to-cost.
    IF do-it THEN
    DO:
      FIND FIRST bediener WHERE bediener.nr = INTEGER(calls.aufschlag)
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE bediener.
    END.
    IF do-it THEN
    DO:
      IF AVAILABLE bediener THEN curr-bezeich = bediener.username.
      ELSE curr-bezeich = "Unknown".
      
      IF curr-user = "not defined" THEN curr-user = curr-bezeich.
      IF curr-user NE curr-bezeich THEN
      DO:
        CREATE str-list.
        str-list.s = FILL(" ", 19).
        str-list.s = str-list.s + STRING(("TOTAL USER - " + curr-user), "x(40)").
        IF price-decimal = 0 THEN
        DO:
          IF ext-amt1 LE 999999999 THEN
             str-list.s = str-list.s + STRING(ext-amt1,   ">,>>>,>>>,>>9"). 
          ELSE str-list.s = str-list.s + STRING(ext-amt1, ">>>>>>>>>>>>9").
        END.
        ELSE str-list.s = str-list.s + STRING(ext-amt1,   ">>,>>>,>>9.99"). 
        IF double-currency OR price-decimal NE 0 THEN 
          str-list.s = str-list.s + STRING(ext-amt2,      ">>,>>>,>>9.99"). 
        ELSE 
        DO: 
          IF ext-amt2 LE 999999999 THEN 
            str-list.s = str-list.s + STRING(ext-amt2,    ">,>>>,>>>,>>9"). 
          ELSE str-list.s = str-list.s + STRING(ext-amt2, ">>>>>>>>>>>>9"). 
        END. 
        CREATE str-list.
        ASSIGN
            curr-user = curr-bezeich
            dept-local = 0
            dept-ldist = 0 
            dept-ovsea = 0 
            ext-amt1   = 0
            ext-amt2   = 0.
      END.
      RUN create-record.
      ASSIGN
        ext-amt1 = ext-amt1 + calls.pabxbetrag
        ext-amt2 = ext-amt2 + calls.gastbetrag 
      . 
      IF SUBSTR(calls.rufnummer,1,1) NE "0" THEN 
      DO: 
        dept-local = dept-local + calls.pabxbetrag. 
      END. 
      ELSE IF SUBSTR(calls.rufnummer,1,2) EQ "00" THEN 
      DO: 
        dept-ovsea = dept-ovsea + calls.pabxbetrag. 
      END. 
      ELSE DO: 
        dept-ldist = dept-ldist + calls.pabxbetrag. 
      END. 
    END.
  END.
      
  CREATE str-list.
  str-list.s = FILL(" ", 19).
  str-list.s = str-list.s + STRING(("TOTAL USER - " + curr-user), "x(40)").
  IF price-decimal = 0 THEN
  DO:
    IF ext-amt1 LE 999999999 THEN
       str-list.s = str-list.s + STRING(ext-amt1,   ">,>>>,>>>,>>9"). 
    ELSE str-list.s = str-list.s + STRING(ext-amt1, ">>>>>>>>>>>>9").
  END.
END. 


PROCEDURE create-record: 
DEFINE VARIABLE i AS INTEGER. 
  IF calls.betriebsnr = 0 THEN i = 1. 
  ELSE i = 2. 
 
  create str-list. 
  str-list.zero-rate = (calls.pabxbetrag = 0 AND calls.gastbetrag = 0). 
 
  str-list.s = STRING(calls.nebenstelle, "x(6)") 
    + STRING(calls.datum) 
    + STRING(calls.zeit, "HH:MM") 
    + STRING(calls.rufnummer, "x(24)") 
    + STRING(calls.satz-id, "x(16)"). 
  IF double-currency THEN 
  DO: 
    IF calls.leitung GE 10000 THEN
    str-list.s = str-list.s + STRING(calls.pabxbetrag, ">,>>>,>>>,>>9") 
      + STRING(calls.gastbetrag, ">>,>>>,>>9.99") 
      + STRING(calls.dauer, "HH:MM:SS") 
      + STRING(calls.zinr, "x(6)") 
      + STRING(calls.impulse, ">>>>>9") 
      + STRING(STRING(calls.leitung), "x(4)") 
      + prstr[i] 
      + STRING(calls.sequence,">>>>>>9"). 
    ELSE
    str-list.s = str-list.s + STRING(calls.pabxbetrag, ">,>>>,>>>,>>9") 
      + STRING(calls.gastbetrag, ">>,>>>,>>9.99") 
      + STRING(calls.dauer, "HH:MM:SS") 
      + STRING(calls.zinr, "x(6)") 
      + STRING(calls.impulse, ">>>>>9") 
      + STRING(calls.leitung, ">>>>") 
      + prstr[i] 
      + STRING(calls.sequence,">>>>>>9"). 
  END. 
  ELSE 
  DO: 
    IF price-decimal = 0 THEN 
      str-list.s = str-list.s + STRING(calls.pabxbetrag,    ">,>>>,>>>,>>9") 
      + STRING(calls.gastbetrag, ">,>>>,>>>,>>9"). 
    ELSE str-list.s = str-list.s + STRING(calls.pabxbetrag, ">>,>>>,>>9.99") 
      + STRING(calls.gastbetrag, ">>,>>>,>>9.99"). 
    IF calls.leitung GE 10000 THEN
    str-list.s = str-list.s 
      + STRING(calls.dauer, "HH:MM:SS") 
      + STRING(calls.zinr, "x(6)") 
      + STRING(calls.impulse, ">>>>>9") 
      + STRING(STRING(calls.leitung), "x(4)") 
      + prstr[i] 
      + STRING(calls.sequence,">>>>>>9"). 
    ELSE
    str-list.s = str-list.s 
      + STRING(calls.dauer, "HH:MM:SS") 
      + STRING(calls.zinr, "x(6)") 
      + STRING(calls.impulse, ">>>>>9") 
      + STRING(calls.leitung, ">>>>") 
      + prstr[i] 
      + STRING(calls.sequence,">>>>>>9"). 
  END. 
  IF sorttype = 1 THEN
  DO:
      IF AVAILABLE bediener THEN
          str-list.s = str-list.s + " " + bediener.username.
  END.
      
  amount1 = amount1 + calls.pabxbetrag. 
  amount2 = amount2 + calls.gastbetrag. 
 
  IF SUBSTR(calls.rufnummer,1,1) NE "0" THEN 
    t-local = t-local + calls.pabxbetrag. 
  ELSE IF SUBSTR(calls.rufnummer,1,2) EQ "00" THEN 
    t-ovsea = t-ovsea + calls.pabxbetrag. 
  ELSE t-ldist = t-ldist + calls.pabxbetrag. 
 
END. 
 

