
DEFINE TEMP-TABLE output-list
    FIELD company   AS CHAR FORMAT "x(30)" LABEL "Company Name"
    FIELD booker    AS CHAR FORMAT "x(30)" LABEL "Contact Person"
    FIELD datum     LIKE bk-stat.datum     LABEL "Date"
    FIELD room      LIKE bk-stat.room      LABEL "Venue"
    FIELD resnr     LIKE bk-stat.resnr     LABEL "RevNo"
    FIELD sales     AS CHAR FORMAT "x(10)" LABEL "Sales"
    FIELD cmid      AS CHAR FORMAT "x(10)" LABEL "ConventionManager"
    FIELD rm-rev    LIKE bk-stat.rm-rev    LABEL "RoomRevenue"
    FIELD fb-rev    LIKE bk-stat.fb-rev    LABEL "F&B Revenue"
    FIELD other-rev LIKE bk-stat.other-rev LABEL "OtherRevenue"
    FIELD tot-rev   AS DECIMAL FORMAT " >>>,>>>,>>>" LABEL "TotalRevenue"
    . 

DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE troomrev    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE tfbrev      AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE tothrev     AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE ttrev       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".

RUN create-list.

PROCEDURE create-list: 
  DEF VAR other-rev AS DECIMAL FORMAT "->>>,>>>,>>9.99".

  ASSIGN
      troomrev = 0
      tfbrev   = 0
      tothrev  = 0
      ttrev    = 0.
  FOR EACH output-list: 
      DELETE output-list. 
  END. 
    
  FOR EACH bk-stat WHERE bk-stat.datum GE from-date 
      AND bk-stat.datum LE to-date NO-LOCK,
      FIRST bk-veran WHERE bk-veran.veran-nr = bk-stat.resnr NO-LOCK,
      FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK :

      IF AVAILABLE bk-stat THEN
      DO:
          CREATE output-list.
          ASSIGN 
            output-list.company   = guest.NAME
            output-list.datum     = bk-stat.datum
            output-list.room      = bk-stat.room
            output-list.resnr     = bk-stat.resnr
            output-list.rm-rev    = bk-stat.rm-rev
            output-list.fb-rev    = bk-stat.fb-rev
            output-list.other-rev = bk-stat.other-rev
            output-list.tot-rev   = bk-stat.rm-rev + bk-stat.fb-rev + bk-stat.other-rev.

            /*Gerald 020320*/
            FIND FIRST bk-func WHERE bk-func.veran-nr = bk-veran.veran-nr NO-LOCK NO-ERROR.
            IF AVAILABLE bk-func THEN
                output-list.booker    = bk-func.kontaktperson[1].

            FIND FIRST bediener WHERE bediener.userinit = bk-stat.salesid NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
                output-list.sales = bediener.username.
            
            FIND FIRST bediener WHERE bediener.userinit = guest.phonetik2 NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
                output-list.cmid = bediener.username.
     END.
     END.
END. 
