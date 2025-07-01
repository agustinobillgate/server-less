
DEFINE TEMP-TABLE s-list 
  FIELD rmcat       AS CHAR FORMAT "x(6)" 
  FIELD bezeich     AS CHAR FORMAT "x(40)" 
  FIELD nat         AS CHAR FORMAT "x(24)" 
  FIELD anz         AS INTEGER FORMAT ">>9" 
  FIELD adult       AS INTEGER FORMAT ">>9" 
  FIELD proz        AS DECIMAL FORMAT ">>9.99" 
  FIELD child       AS INTEGER FORMAT ">>9". 
 
 DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS INTEGER 
  FIELD nr         AS INTEGER   FORMAT ">,>>>" /*sis 181113 before ">>9"*/
  FIELD vip        AS CHAR      FORMAT "x(4)" 
  FIELD resnr      AS INTEGER   FORMAT ">>>>>>>" 
  FIELD name       AS CHAR      FORMAT "x(30)" 
  FIELD groupname  AS CHAR      FORMAT "x(24)" 
  FIELD rmno       AS CHAR      FORMAT "x(4)"
  FIELD qty        AS INTEGER   FORMAT ">>>>>9" /*MT 12/06/13 */
  FIELD arrive     AS CHARACTER FORMAT "x(10)" 
  FIELD depart     AS CHARACTER FORMAT "x(10)" 
  FIELD rmcat      AS CHAR      FORMAT "x(6)" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR 
  FIELD a          AS INTEGER   FORMAT "9" 
  FIELD c          AS INTEGER   FORMAT "9" 
  FIELD co         AS INTEGER   FORMAT ">>" 
  FIELD pax        AS CHAR      FORMAT "x(6)" 
  FIELD nat        AS CHAR      FORMAT "x(4)" 
  FIELD nation     AS CHAR 
  FIELD argt       AS CHAR      FORMAT "x(7)" 
  FIELD company    AS CHAR      FORMAT "x(30)" 
  FIELD flight     AS CHAR      FORMAT "x(6)" 
  FIELD etd        AS CHAR      FORMAT "99:99" 
  FIELD outstand   AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
  FIELD bemerk     AS CHAR      FORMAT "x(2000)"
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
  FIELD email      AS CHAR      FORMAT "x(24)"
  FIELD email-adr  AS CHAR      FORMAT "x(40)" /*ITA 150813*/ /*ITA 190813*/
  FIELD tot-night  AS INT       
  FIELD ratecode   AS CHAR      FORMAT "x(10)"
  FIELD full-name  AS CHAR      
                                
  FIELD address    AS CHAR      FORMAT "x(100)"
  FIELD memberno   AS CHAR      FORMAT "x(20)"
  FIELD membertype AS CHAR      FORMAT "x(20)"
.

DEFINE TEMP-TABLE t-cl-list 
  FIELD flag       AS INTEGER 
  FIELD nr         AS INTEGER   FORMAT ">,>>>" /*sis 181113 before ">>9"*/
  FIELD vip        AS CHAR      FORMAT "x(4)" 
  FIELD resnr      AS INTEGER   FORMAT ">>>>>>>" 
  FIELD name       AS CHAR      FORMAT "x(30)" 
  FIELD groupname  AS CHAR      FORMAT "x(24)" 
  FIELD rmno       AS CHAR      FORMAT "x(4)"
  FIELD qty        AS INTEGER   FORMAT ">>>>>9" /*MT 12/06/13 */
  FIELD arrive     AS CHARACTER FORMAT "x(10)" 
  FIELD depart     AS CHARACTER FORMAT "x(10)" 
  FIELD rmcat      AS CHAR      FORMAT "x(6)" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR 
  FIELD a          AS INTEGER   FORMAT "9" 
  FIELD c          AS INTEGER   FORMAT "9" 
  FIELD co         AS INTEGER   FORMAT ">>" 
  FIELD pax        AS CHAR      FORMAT "x(6)" 
  FIELD nat        AS CHAR      FORMAT "x(4)" 
  FIELD nation     AS CHAR 
  FIELD argt       AS CHAR      FORMAT "x(7)" 
  FIELD company    AS CHAR      FORMAT "x(30)" 
  FIELD flight     AS CHAR      FORMAT "x(6)" 
  FIELD etd        AS CHAR      FORMAT "99:99" 
  FIELD outstand   AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
  FIELD bemerk     AS CHAR      FORMAT "x(2000)"
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
  FIELD email      AS CHAR      FORMAT "x(24)"
  FIELD email-adr  AS CHAR      FORMAT "x(40)" /*ITA 150813*/ /*ITA 190813*/
  FIELD tot-night  AS INT       
  FIELD ratecode   AS CHAR      FORMAT "x(10)"
  FIELD full-name  AS CHAR                                      
  FIELD address    AS CHAR      FORMAT "x(100)"
  FIELD memberno   AS CHAR      FORMAT "x(20)"
  FIELD membertype AS CHAR      FORMAT "x(20)"

  FIELD phonenum          AS CHARACTER
  FIELD str-outstand      AS CHARACTER
  FIELD night             AS INTEGER /*FD*/
.


DEFINE INPUT PARAMETER tot-rm AS INTEGER INITIAL 0.
DEFINE INPUT PARAMETER tot-a AS INTEGER INITIAL 0.
DEFINE INPUT PARAMETER tot-c AS INTEGER INITIAL 0.
DEFINE INPUT PARAMETER tot-co AS INTEGER INITIAL 0.
DEFINE INPUT PARAMETER TABLE FOR cl-list.
DEFINE INPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-cl-list.

/*FD September 15, 2020*/
FOR EACH t-cl-list:
    DELETE t-cl-list.
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

    t-cl-list.str-outstand = STRING(cl-list.outstand, "->>>,>>>,>>9.99").
    t-cl-list.night = DATE(cl-list.depart) - DATE(cl-list.arrive).
END.

CREATE t-cl-list.
CREATE t-cl-list.
ASSIGN                       
    t-cl-list.NAME           = "SUMMARY"
    t-cl-list.memberno       = "Room Type"
    t-cl-list.membertype     = "Nation"
    t-cl-list.vip            = " Qty"
    t-cl-list.rmcat          = " Adult"
    t-cl-list.ratecode       = "       (%)"
    t-cl-list.pax            = " Child"
.

FOR EACH s-list:
    CREATE t-cl-list.
    ASSIGN
        t-cl-list.memberno     = s-list.bezeich
        t-cl-list.membertype   = s-list.nat
        t-cl-list.vip          = STRING(s-list.anz, ">>>9")        
        t-cl-list.rmcat        = STRING(s-list.adult, ">>,>>9")   
        t-cl-list.ratecode     = STRING(s-list.proz, "    >>9.99")     
        t-cl-list.pax          = STRING(s-list.child, ">>,>>9")
    .
END.

CREATE t-cl-list.
CREATE t-cl-list.
ASSIGN                       
    t-cl-list.memberno       = "T O T A L"
    t-cl-list.membertype     = ""
    t-cl-list.vip            = STRING(tot-rm, ">>>9")
    t-cl-list.rmcat          = STRING(tot-a + tot-co, ">>,>>9")
    t-cl-list.ratecode       = "    100.00"
    t-cl-list.pax            = STRING(tot-c, ">>,>>9")
. 
/*End FD*/
