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

DEFINE TEMP-TABLE output-list 
  FIELD ext         AS CHAR FORMAT "x(6)" 
  FIELD datum       AS CHAR FORMAT "x(8)" 
  FIELD zeit        AS CHAR FORMAT "x(5)" 
  FIELD dialed      AS CHAR FORMAT "x(24)"
  FIELD dest        AS CHAR FORMAT "x(16)"
  FIELD pabx-rate   AS CHAR FORMAT "x(13)"
  FIELD guest-rate  AS CHAR FORMAT "x(13)"
  FIELD duration    AS CHAR FORMAT "x(8)" 
  FIELD zinr        AS CHAR FORMAT "x(6)" 
  FIELD pulse       AS CHAR FORMAT "x(5)" 
  FIELD lin         AS CHAR FORMAT "x(4)" 
  FIELD print       AS CHAR FORMAT "x(3)" 
  FIELD ref-no      AS CHAR FORMAT "x(7)" 
  FIELD username    AS CHAR FORMAT "x(32)".

DEFINE TEMP-TABLE print-list
  FIELD flag        AS INTEGER
  FIELD ext         AS CHAR 
  FIELD datum       AS CHAR  
  FIELD zeit        AS CHAR 
  FIELD dialed      AS CHAR 
  FIELD dest        AS CHAR 
  FIELD pabx-rate   AS CHAR 
  FIELD guest-rate  AS CHAR  
  FIELD duration    AS CHAR
  FIELD local       AS DECIMAL 
  FIELD ldist       AS DECIMAL 
  FIELD ovsea       AS DECIMAL .

DEFINE TEMP-TABLE t-parameters LIKE parameters.

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR cost-list.
DEFINE INPUT        PARAMETER sorttype      AS INTEGER.
DEFINE INPUT        PARAMETER cost-center   AS INTEGER.
DEFINE INPUT        PARAMETER to-cc         AS INTEGER.
DEFINE INPUT        PARAMETER price-decimal AS INTEGER.
DEFINE INPUT        PARAMETER from-date     AS DATE.
DEFINE INPUT        PARAMETER to-date       AS DATE.
DEFINE INPUT        PARAMETER double-currency AS LOGICAL.
DEFINE INPUT        PARAMETER pr-summary    AS LOGICAL.

DEFINE OUTPUT       PARAMETER stattype     AS INTEGER.
DEFINE OUTPUT       PARAMETER TABLE FOR output-list.
DEFINE OUTPUT       PARAMETER TABLE FOR print-list.

/*
DEFINE VAR sorttype      AS INTEGER INITIAL 0.
DEFINE VAR cost-center   AS INTEGER INITIAL 0.
DEFINE VAR to-cc         AS INTEGER INITIAL 0.
DEFINE VAR price-decimal AS INTEGER INITIAL 0.
DEFINE VAR from-date     AS DATE INITIAL 1/1/19.
DEFINE VAR to-date       AS DATE INITIAL 1/14/19.
DEFINE VAR double-currency AS LOGICAL INITIAL NO.
DEFINE VAR stattype     AS INTEGER.
DEFINE VAR cost1     AS DECIMAL.
DEFINE VAR cost2     AS DECIMAL.
DEFINE VAR pr-summary AS LOGICAL INIT YES.

FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.num = INTEGER(parameters.varname). 
    cost-list.name = parameters.vstring. 
    IF cost1 GT cost-list.num THEN cost1 = cost-list.num. 
    IF cost2 LT cost-list.num THEN cost2 = cost-list.num. 
END.
*/

DEFINE VARIABLE read-parameter-str1 AS CHAR.
DEFINE VARIABLE read-parameter-str2 AS CHAR.
DEFINE VARIABLE substrTR            AS CHAR.

FOR EACH output-list:
    DELETE output-list.
END.

RUN calls-deptlistbl.p
    (INPUT-OUTPUT TABLE cost-list, sorttype, cost-center, to-cc,
                 price-decimal, from-date, to-date, double-currency,
                 OUTPUT stattype, OUTPUT TABLE str-list).

FOR EACH str-list:
    CREATE output-list.
    ASSIGN 
        output-list.ext         = SUBSTR(str-list.s, 1, 6)   
        output-list.datum       = SUBSTR(str-list.s, 7, 8)   
        output-list.zeit        = SUBSTR(str-list.s, 15, 5)  
        output-list.dialed      = SUBSTR(str-list.s, 20, 24) 
        output-list.dest        = SUBSTR(str-list.s, 44, 16) 
        output-list.pabx-rate   = SUBSTR(str-list.s, 60, 13) 
        output-list.guest-rate  = SUBSTR(str-list.s, 73, 13) 
        output-list.duration    = SUBSTR(str-list.s, 86, 8)  
        output-list.zinr        = SUBSTR(str-list.s, 94, 6)  
        output-list.pulse       = SUBSTR(str-list.s, 100, 6) 
        output-list.lin         = SUBSTR(str-list.s, 106, 4) 
        output-list.print       = SUBSTR(str-list.s, 110, 3) 
        output-list.ref-no      = SUBSTR(str-list.s, 113, 7) 
        output-list.username    = SUBSTR(str-list.s, 120,32) 
        .
END.

FOR EACH str-list WHERE NOT str-list.zero-rate:
  IF sorttype = 0 THEN
  DO:
    IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL DEPT" 
      OR SUBSTR(TRIM(str-list.s),1,5) = "GRAND" THEN 
    DO:
      CREATE print-list.
      ASSIGN 
        print-list.flag = 0
        print-list.ext = "---"
      .
    END.
    IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL EXT." 
      AND NOT pr-summary THEN 
    DO:
      CREATE print-list.
      ASSIGN
        print-list.flag = 0
        print-list.ext = "---".
    END.
    IF NOT pr-summary THEN 
    DO:
      CREATE print-list.
      ASSIGN
        print-list.flag        = 1
        print-list.ext         = SUBSTR(str-list.s, 1, 6)   
        print-list.datum       = SUBSTR(str-list.s, 7, 8)   
        print-list.zeit        = SUBSTR(str-list.s, 15, 5)  
        print-list.dialed      = SUBSTR(str-list.s, 20, 24) 
        print-list.dest        = SUBSTR(str-list.s, 44, 16) 
        print-list.pabx-rate   = SUBSTR(str-list.s, 60, 13) 
        print-list.duration    = SUBSTR(str-list.s, 86, 8).
    END. 
    ELSE IF pr-summary AND (SUBSTR(TRIM(str-list.s),1,5) = "TOTAL" 
      OR SUBSTR(TRIM(str-list.s),1,5) = "GRAND") THEN 
    DO: 
      IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL EXT." THEN 
      DO:
         CREATE print-list.
         ASSIGN 
           print-list.flag = 2
           print-list.ext = SUBSTR(TRIM(str-list.s),14,6).
      END.
      ELSE IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL DEPT" THEN 
      DO: 
        FIND FIRST cost-list WHERE cost-list.num = INTEGER(SUBSTR(TRIM(str-list.s), 14, 4)) NO-LOCK. 
        IF AVAILABLE cost-list THEN
        DO:
          CREATE print-list.
          ASSIGN 
            print-list.flag = 2
            print-list.ext = cost-list.NAME.
        END.
      END.
      ELSE
      DO:
          CREATE print-list.
          ASSIGN
            print-list.flag = 2
            print-list.ext = SUBSTR(str-list.s, 20, 24).
      END.
      ASSIGN
        print-list.local = str-list.local
        print-list.ldist = str-list.ldist
        print-list.ovsea = str-list.ovsea
        print-list.pabx-rate = SUBSTR(str-list.s, 60, 13)
        print-list.guest-rate = SUBSTR(str-list.s, 73, 13).
      IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL DEPT" THEN
      DO:     
        CREATE print-list.
        ASSIGN 
          print-list.flag = 0.
      END.
    END.
  END.
  ELSE /*sorttype ne 0*/
  DO:
    IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL DEPT" 
      OR SUBSTR(TRIM(str-list.s),1,5) = "GRAND" THEN 
    DO:
      CREATE print-list.
      ASSIGN 
        print-list.flag = 0
        print-list.ext = "---".
    END.
    IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL USER" 
      AND NOT pr-summary THEN
    DO:
      CREATE print-list.
      ASSIGN 
        print-list.flag = 0
        print-list.ext = "---".
    END.
    IF NOT pr-summary THEN 
    DO:
      CREATE print-list.
      ASSIGN
        print-list.flag = 1
        print-list.ext         = SUBSTR(str-list.s, 1, 6)   
        print-list.datum       = SUBSTR(str-list.s, 7, 8)   
        print-list.zeit        = SUBSTR(str-list.s, 15, 5)  
        print-list.dialed      = SUBSTR(str-list.s, 20, 24) 
        print-list.dest        = SUBSTR(str-list.s, 44, 16) 
        print-list.pabx-rate   = SUBSTR(str-list.s, 60, 13) 
        print-list.duration    = SUBSTR(str-list.s, 86, 8).
    END. 
    ELSE IF pr-summary AND (SUBSTR(TRIM(str-list.s),1,5) = "TOTAL" 
      OR SUBSTR(TRIM(str-list.s),1,5) = "GRAND") THEN 
    DO: 
      IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL USER" THEN 
      DO:
        CREATE print-list.
        ASSIGN print-list.ext = SUBSTR(TRIM(str-list.s),14, 6).
      END.
      ELSE IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL DEPT" THEN 
      DO:
        ASSIGN
          read-parameter-str1 = "CostCenter"
          read-parameter-str2 = "Name"
          substrTR            = SUBSTR(TRIM(str-list.s), 14, 4).
        RUN read-parametersbl.p(5, read-parameter-str1, read-parameter-str2,
          substrTR, ?, OUTPUT TABLE t-parameters).
        FIND FIRST t-parameters.
        CREATE print-list.
        ASSIGN print-list.ext = t-parameters.vstring.
      END. 
      ELSE
      DO:
        CREATE print-list.
        ASSIGN print-list.ext = SUBSTR(str-list.s, 20, 24).
      END.
      ASSIGN
        print-list.local = str-list.local
        print-list.ldist = str-list.ldist
        print-list.ovsea = str-list.ovsea
        print-list.pabx-rate = SUBSTR(str-list.s, 60, 13)
        print-list.guest-rate = SUBSTR(str-list.s, 73, 13).
      IF SUBSTR(TRIM(str-list.s),1,10) = "TOTAL DEPT" THEN
      DO:     
        CREATE print-list.
        ASSIGN print-list.flag = 0.
      END.
    END. 
  END.
END.

/*FOR EACH output-list:
    DISP output-list.
END.

FOR EACH print-list:
    DISP print-list.ext FORMAT "x(24)" print-list.local print-list.ldist print-list.ovsea.
END.
*/
