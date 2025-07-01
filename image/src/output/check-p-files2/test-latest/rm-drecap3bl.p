DEFINE TEMP-TABLE output-list 
  FIELD segNo      AS INTEGER INITIAL 0
  FIELD flag       AS CHAR 
  FIELD STR        AS CHAR
  FIELD yroom      AS CHAR FORMAT "x(6)"
  FIELD proz3      AS CHAR FORMAT "x(6)"
  FIELD ypax       AS CHAR FORMAT "x(6)"
  FIELD yrate      AS CHAR FORMAT "x(13)" 
  FIELD yrev       AS CHAR FORMAT "x(22)"
  FIELD zero-flag  AS LOGICAL INIT NO.

DEFINE TEMP-TABLE dos-list
    FIELD segno AS INTEGER
    FIELD flag AS CHAR
    FIELD guestSegment AS CHARACTER
    FIELD room AS INTEGER
    FIELD proz-rm AS DECIMAL
    FIELD mtd AS INTEGER
    FIELD proz-mtd AS DECIMAL
    FIELD ytd AS INTEGER
    FIELD proz-ytd AS DECIMAL
    FIELD pax AS INTEGER
    FIELD mtd-pax AS INTEGER
    FIELD ytd-pax AS INTEGER
    FIELD avrg-rate AS DECIMAL
    FIELD mtd-avrgrate AS DECIMAL
    FIELD ytd-avrgrate AS DECIMAL
    FIELD room-rev AS DECIMAL
    FIELD mtd-rev AS DECIMAL
    FIELD ytd-rev AS DECIMAL
    FIELD zero-flag AS LOGICAL.

DEF INPUT PARAMETER language-code   AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER opening-date    AS DATE.
DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER fdate           AS DATE.
DEF INPUT PARAMETER tdate           AS DATE.
DEF INPUT PARAMETER segmtype-exist  AS LOGICAL.
DEF INPUT PARAMETER checked-mi-mtd  AS LOGICAL.
DEF INPUT PARAMETER checked-mi-ftd  AS LOGICAL.
DEF INPUT PARAMETER checked-mi-excHU AS LOGICAL.
DEF INPUT PARAMETER checked-mi-excComp AS LOGICAL.
DEF INPUT PARAMETER long-digit      AS LOGICAL. 

DEF OUTPUT PARAMETER TABLE FOR dos-list.


RUN rm-drecap2bl.p
    (language-code, opening-date, from-date, to-date, fdate, tdate,
     segmtype-exist, checked-mi-mtd, checked-mi-ftd,
     checked-mi-excHU, checked-mi-excComp, long-digit,
     OUTPUT TABLE output-list).


FOR EACH output-list:
    CREATE dos-list.
    ASSIGN
        dos-list.segno = INTEGER(SUBSTRING(output-list.str,1,3))
        dos-list.flag = output-list.flag
        dos-list.guestSegment = SUBSTRING(output-list.str,4,16)
        dos-list.room = INTEGER(SUBSTRING(output-list.str,20,3))
        dos-list.proz-rm = DECIMAL(SUBSTRING(output-list.str,23,7))
        dos-list.mtd = INTEGER(SUBSTRING(output-list.str,30,6))
        dos-list.proz-mtd = DECIMAL(SUBSTRING(output-list.str,36,7))
        dos-list.ytd = INTEGER(output-list.yroom)
        dos-list.proz-ytd = DECIMAL(output-list.proz3)
        dos-list.pax = INTEGER(SUBSTRING(output-list.str,43,3))
        dos-list.mtd-pax = INTEGER(SUBSTRING(output-list.str,46,6))
        dos-list.ytd-pax = INTEGER(output-list.ypax)
        dos-list.avrg-rate = DECIMAL(SUBSTRING(output-list.str,52,13))
        dos-list.mtd-avrgrate = DECIMAL(SUBSTRING(output-list.str,65,13))
        dos-list.ytd-avrgrate = DECIMAL(output-list.yrate)
        dos-list.room-rev = DECIMAL(SUBSTRING(output-list.str,78,14))
        dos-list.mtd-rev = DECIMAL(SUBSTRING(output-list.str,92,19))
        dos-list.ytd-rev = DECIMAL(output-list.yrev)
        dos-list.zero-flag = output-list.zero-flag.
END.
