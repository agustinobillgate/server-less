
DEFINE TEMP-TABLE s-list
  FIELD rmcat AS CHAR FORMAT "x(6)"
  FIELD bezeich AS CHAR FORMAT "x(24)"
  FIELD nat   AS CHAR FORMAT "x(24)"
  FIELD anz   AS INTEGER FORMAT ">>9"
  FIELD adult AS INTEGER FORMAT ">>9"
  FIELD proz  AS DECIMAL FORMAT ">>9.99"
  FIELD child AS INTEGER FORMAT ">>9".

DEFINE TEMP-TABLE t-list
  FIELD gastnr  AS INTEGER
  FIELD company AS CHAR
  FIELD counter AS CHAR
  FIELD int-counter AS INTEGER INITIAL 0
  FIELD anzahl      AS INTEGER INITIAL 0
  FIELD erwachs     AS INTEGER INITIAL 0
  FIELD kind        AS INTEGER INITIAL 0.

DEFINE TEMP-TABLE cl-list
  FIELD ci-id      AS CHAR      /*MT 04/09/13 */
  FIELD stat-flag  AS CHAR FORMAT "x(1)" INITIAL " "
  FIELD datum      AS DATE FORMAT "99/99/99"
  FIELD flag       AS INTEGER
  FIELD nr         AS INTEGER FORMAT ">,>>>"
  FIELD vip        AS CHAR FORMAT "x(4)"
  FIELD gastnr     AS INTEGER INITIAL 0
  FIELD resnr      AS INTEGER FORMAT ">>>>>>>"
  FIELD name       AS CHAR FORMAT "x(24)"
  FIELD groupname  AS CHAR FORMAT "x(24)"
  FIELD zimmeranz  AS INTEGER
  FIELD rmno       LIKE res-line.zinr /*MT 24/07/12 */
  FIELD qty        AS INTEGER FORMAT ">>9"
  FIELD zipreis    AS CHAR    FORMAT "x(15)"
  FIELD arrival    AS CHAR    FORMAT "x(10)"
  FIELD depart     AS CHAR    FORMAT "x(10)"
  FIELD rmcat      AS CHAR    FORMAT "x(6)"
  FIELD kurzbez    AS CHAR
  FIELD bezeich    AS CHAR
  FIELD a          AS INTEGER FORMAT "9"
  FIELD c          AS INTEGER FORMAT "9"
  FIELD co         AS INTEGER FORMAT ">>"
  FIELD pax        AS CHAR FORMAT "x(6)"
  FIELD nat        AS CHAR FORMAT "x(4)"
  FIELD nation     AS CHAR
  FIELD argt       AS CHAR FORMAT "x(7)"
  FIELD company    AS CHAR FORMAT "x(30)"
  FIELD flight     AS CHAR FORMAT "x(6)"
  FIELD etd        AS CHAR FORMAT "99:99"
  FIELD stay       AS INTEGER
  FIELD segment    AS CHARACTER FORMAT "x(16)" /*sis 070814*/
  FIELD rate-code  AS CHARACTER FORMAT "x(7)" /*sis 070814*/
  FIELD eta        AS CHARACTER FORMAT "99:99" /*sis 070814*/
  FIELD Email      LIKE guest.email-adr
  FIELD bemerk     AS CHAR FORMAT "x(2000)"
  /*naufal Add Remarks 2000 Char*/                              
  FIELD bemerk01   AS CHAR      FORMAT "x(255)"
  FIELD bemerk02   AS CHAR      FORMAT "x(255)"
  FIELD bemerk03   AS CHAR      FORMAT "x(255)"
  FIELD bemerk04   AS CHAR      FORMAT "x(255)"
  FIELD bemerk05   AS CHAR      FORMAT "x(255)"
  FIELD bemerk06   AS CHAR      FORMAT "x(255)"
  FIELD bemerk07   AS CHAR      FORMAT "x(255)"
  FIELD bemerk08   AS CHAR      FORMAT "x(255)"
  /*end naufal*/
  FIELD spreq      AS CHAR
  FIELD memberno   AS CHAR      FORMAT "x(20)"   
  FIELD resdate    AS CHAR      FORMAT "x(10)"
  FIELD sob        AS CHAR      FORMAT "x(25)" 
  /*FD*/
  FIELD created-by AS CHARACTER
  FIELD ci-time    AS CHARACTER
  /*End FD*/
.

DEFINE TEMP-TABLE t-cl-list
  FIELD ci-id      AS CHAR      /*MT 04/09/13 */
  FIELD stat-flag  AS CHAR FORMAT "x(1)" INITIAL " "
  FIELD datum      AS DATE FORMAT "99/99/99"
  FIELD flag       AS INTEGER
  FIELD nr         AS INTEGER FORMAT ">,>>>"
  FIELD vip        AS CHAR FORMAT "x(4)"
  FIELD gastnr     AS INTEGER INITIAL 0
  FIELD resnr      AS INTEGER FORMAT ">>>>>>>"
  FIELD name       AS CHAR FORMAT "x(24)"
  FIELD groupname  AS CHAR FORMAT "x(24)"
  FIELD zimmeranz  AS INTEGER
  FIELD rmno       LIKE res-line.zinr /*MT 24/07/12 */
  FIELD qty        AS INTEGER FORMAT ">>9"
  FIELD zipreis    AS CHAR    FORMAT "x(15)"
  FIELD arrival    AS CHAR    FORMAT "x(10)"
  FIELD depart     AS CHAR    FORMAT "x(10)"
  FIELD rmcat      AS CHAR    FORMAT "x(6)"
  FIELD kurzbez    AS CHAR
  FIELD bezeich    AS CHAR
  FIELD a          AS INTEGER FORMAT "9"
  FIELD c          AS INTEGER FORMAT "9"
  FIELD co         AS INTEGER FORMAT ">>"
  FIELD pax        AS CHAR FORMAT "x(6)"
  FIELD nat        AS CHAR FORMAT "x(4)"
  FIELD nation     AS CHAR
  FIELD argt       AS CHAR FORMAT "x(7)"
  FIELD company    AS CHAR FORMAT "x(30)"
  FIELD flight     AS CHAR FORMAT "x(6)"
  FIELD etd        AS CHAR FORMAT "99:99"
  FIELD stay       AS INTEGER
  FIELD segment    AS CHARACTER FORMAT "x(16)" /*sis 070814*/
  FIELD rate-code  AS CHARACTER FORMAT "x(7)" /*sis 070814*/
  FIELD eta        AS CHARACTER FORMAT "99:99" /*sis 070814*/
  FIELD Email      LIKE guest.email-adr
  FIELD bemerk     AS CHAR FORMAT "x(2000)"
  /*naufal Add Remarks 2000 Char*/                              
  FIELD bemerk01   AS CHAR      FORMAT "x(255)"
  FIELD bemerk02   AS CHAR      FORMAT "x(255)"
  FIELD bemerk03   AS CHAR      FORMAT "x(255)"
  FIELD bemerk04   AS CHAR      FORMAT "x(255)"
  FIELD bemerk05   AS CHAR      FORMAT "x(255)"
  FIELD bemerk06   AS CHAR      FORMAT "x(255)"
  FIELD bemerk07   AS CHAR      FORMAT "x(255)"
  FIELD bemerk08   AS CHAR      FORMAT "x(255)"
  /*end naufal*/
  FIELD spreq      AS CHAR
  FIELD memberno   AS CHAR      FORMAT "x(20)"   
  FIELD resdate    AS CHAR      FORMAT "x(10)"
  FIELD sob        AS CHAR      FORMAT "x(25)" 
  /*FD*/
  FIELD created-by AS CHARACTER
  FIELD ci-time    AS CHARACTER
  /*End FD*/

  FIELD phonenum        AS CHARACTER
  FIELD member-typ      AS CHARACTER
  FIELD repeat-guest    AS CHARACTER FORMAT "x(1)"
  FIELD night           AS INTEGER. /*FD*/

DEFINE INPUT PARAMETER tot-rm AS INTEGER INITIAL 0.
DEFINE INPUT PARAMETER tot-a  AS INTEGER INITIAL 0.
DEFINE INPUT PARAMETER tot-c  AS INTEGER INITIAL 0.
DEFINE INPUT PARAMETER tot-co AS INTEGER INITIAL 0.
DEFINE INPUT PARAMETER total-flag AS LOGICAL.
DEFINE INPUT PARAMETER TABLE FOR cl-list.
DEFINE INPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-cl-list.

DEFINE VARIABLE found AS LOGICAL INIT NO.
DEFINE VARIABLE loopi AS INT.
DEFINE VARIABLE counter-str AS CHAR.
DEFINE VARIABLE tot-troom  AS INTEGER.
DEFINE VARIABLE tot-trsv   AS INTEGER.
DEFINE VARIABLE tot-tadult AS INTEGER.
DEFINE VARIABLE tot-tkind  AS INTEGER.

/*FD September 10, 2020*/
FOR EACH t-cl-list:
    DELETE t-cl-list.
END.

FOR EACH t-list:
  DELETE t-list.
END.

FOR EACH cl-list:
    CREATE t-cl-list.
    BUFFER-COPY cl-list TO t-cl-list.
    IF NUM-ENTRIES(cl-list.company, ";") GT 1 THEN
        ASSIGN
        t-cl-list.company = ENTRY(1, cl-list.company, ";")
        t-cl-list.phonenum = ENTRY(2, cl-list.company, ";").
    ELSE
        t-cl-list.company = cl-list.company.

    IF NUM-ENTRIES(cl-list.memberno, ";") GT 1 THEN /*FD*/
    DO:
        ASSIGN
            t-cl-list.member-typ = ENTRY(2, cl-list.memberno, ";")
            t-cl-list.memberno = ENTRY(1, cl-list.memberno, ";").              
    END.
    ELSE t-cl-list.memberno = cl-list.memberno.

    IF t-cl-list.stay GT 1 THEN t-cl-list.repeat-guest = "*".

    ASSIGN t-cl-list.night = DATE(cl-list.depart) - DATE(cl-list.arrival).
END.

CREATE t-cl-list.
CREATE t-cl-list.
ASSIGN                       
    t-cl-list.NAME           = "SUMMARY"
    t-cl-list.memberno       = "Room Type"
    t-cl-list.member-typ     = "Nation"
    t-cl-list.vip            = " Qty"
    t-cl-list.argt           = "  Adult"
    t-cl-list.rmcat          = "   (%)"
    t-cl-list.rate-code      = "     Child"
.

FOR EACH s-list:
    CREATE t-cl-list.
    ASSIGN                     
        t-cl-list.memberno     = s-list.bezeich
        t-cl-list.member-typ   = s-list.nat
        t-cl-list.vip          = STRING(s-list.anz, ">>>9")
        t-cl-list.argt         = STRING(s-list.adult, "  >>>>9")
        t-cl-list.rmcat        = STRING(s-list.proz, ">>9.99")
        t-cl-list.rate-code    = STRING(s-list.child, "     >>>>9")
    .
END.

CREATE t-cl-list.
ASSIGN
    t-cl-list.memberno         = "T O T A L"
    t-cl-list.member-typ       = ""
    t-cl-list.vip              = STRING(tot-rm, ">>>9")
    t-cl-list.argt             = STRING(tot-a + tot-co, "  >>>>9")
    t-cl-list.rmcat            = "100.00"
    t-cl-list.rate-code        = STRING(tot-c,"     >>>>9")
.              

FOR EACH t-cl-list BY t-cl-list.datum BY t-cl-list.nr:
  IF total-flag AND t-cl-list.gastnr > 0 THEN
  DO:
    FIND FIRST t-list WHERE t-list.gastnr = t-cl-list.gastnr NO-ERROR.
    IF NOT AVAILABLE t-list THEN
    DO:
      CREATE t-list.
      ASSIGN
      t-list.gastnr  = t-cl-list.gastnr
      t-list.company = t-cl-list.company.
    END.
    ASSIGN
        t-list.anzahl  = t-list.anzahl + t-cl-list.zimmeranz
        t-list.erwachs = t-list.erwachs + t-cl-list.zimmeranz * t-cl-list.a
        t-list.kind    = t-list.kind + t-cl-list.zimmeranz * t-cl-list.c.
    found = NO.
    DO loopi = 1 TO NUM-ENTRIES(t-list.counter,";"):
        counter-str = ENTRY(loopi,t-list.counter,";").
        IF INT(counter-str) = t-cl-list.resnr THEN found = YES.
    END.
    IF NOT found THEN
        t-list.counter = t-list.counter + STRING(t-cl-list.resnr) + ";". 
  END.
END.

IF total-flag THEN
DO:
    CREATE t-cl-list.
    CREATE t-cl-list.
    ASSIGN                            
        t-cl-list.memberno       = "Reserve Name"
        t-cl-list.member-typ     = "               Rooms"
        t-cl-list.argt           = " TotRsv"
        t-cl-list.rmcat          = " Adult"
        t-cl-list.rate-code      = "     Child"
    .

    FOR EACH t-list:
        IF NUM-ENTRIES(t-list.counter,";") GE 2 THEN
            t-list.int-counter = NUM-ENTRIES(t-list.counter,";") - 1.
        ELSE t-list.int-counter = 0.
    END.

    FOR EACH t-list:
        CREATE t-cl-list.
        ASSIGN
            t-cl-list.rmno           = "#"
            t-cl-list.memberno       = t-list.company
            t-cl-list.member-typ     = STRING(t-list.anzahl, "                >>>9")
            t-cl-list.argt           = STRING(t-list.int-counter, "    >>9")
            t-cl-list.rmcat          = STRING(t-list.erwachs, "   >>9")
            t-cl-list.rate-code      = STRING(t-list.kind, "       >>9")
        .
    END.

    FOR EACH t-list:
        ASSIGN
            tot-troom = tot-troom + t-list.anzahl
            tot-trsv  = tot-trsv + t-list.int-counter
            tot-tadult = tot-tadult + t-list.erwachs
            tot-tkind = tot-tkind + t-list.kind
        .
    END.
    CREATE t-cl-list.
    ASSIGN
        t-cl-list.rmno           = "#"
        t-cl-list.memberno       = "T O T A L"
        t-cl-list.member-typ     = STRING(tot-troom, "                >>>9")
        t-cl-list.argt           = STRING(tot-trsv, "    >>9")
        t-cl-list.rmcat          = STRING(tot-tadult, "   >>9")     
        t-cl-list.rate-code      = STRING(tot-tkind, "       >>9")    
    .           
END. 
