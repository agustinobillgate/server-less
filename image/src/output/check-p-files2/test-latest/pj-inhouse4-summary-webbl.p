DEFINE TEMP-TABLE inhouse-guest-list 
  FIELD resnr      AS INTEGER   FORMAT ">>>>>9" 
  FIELD qty        AS INTEGER   FORMAT ">>9" 
  FIELD rmcat      AS CHAR      FORMAT "x(6)" 
  FIELD rmno       AS CHAR  
  FIELD nation     AS CHAR 
  FIELD arrive     AS DATE 
  FIELD depart     AS DATE 
  FIELD zipreis    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR  
  FIELD a          AS INTEGER   FORMAT "9" 
  FIELD c          AS INTEGER   FORMAT "9" 
  FIELD co         AS INTEGER   FORMAT ">9" 
  FIELD nat        AS CHAR      FORMAT "x(3)" 
  FIELD lodging    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"  
  FIELD breakfast  AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
  FIELD lunch      AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
  FIELD dinner     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
  FIELD otherev    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD curr       AS CHAR      FORMAT "x(4)"
  FIELD paym       AS INTEGER   FORMAT ">>9" 
  FIELD segm       AS CHAR      FORMAT "x(12)"
  .

DEFINE TEMP-TABLE output-list 
  FIELD resnr      AS INTEGER   FORMAT ">>>>>9" 
  FIELD qty        AS INTEGER   FORMAT ">>9" 
  FIELD rmcat      AS CHAR      FORMAT "x(6)" 
  FIELD rmno       AS CHAR 	 
  FIELD nation     AS CHAR 
  FIELD arrive     AS DATE 
  FIELD depart     AS DATE 
  FIELD zipreis    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR  
  FIELD a          AS INTEGER   FORMAT "9" 
  FIELD c          AS INTEGER   FORMAT "9" 
  FIELD co         AS INTEGER   FORMAT ">9" 
  FIELD nat        AS CHAR      FORMAT "x(3)" 
  FIELD lodging    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"  
  FIELD breakfast  AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
  FIELD lunch      AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
  FIELD dinner     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
  FIELD otherev    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD curr       AS CHAR      FORMAT "x(4)"
  FIELD paym       AS INTEGER   FORMAT ">>9"  
  FIELD segm       AS CHAR      FORMAT "x(12)"
  .  

DEFINE TEMP-TABLE tmplist 
  FIELD resnr      AS INTEGER   FORMAT ">>>>>9" 
  FIELD qty        AS INTEGER   FORMAT ">>9" 
  FIELD rmcat      AS CHAR      FORMAT "x(6)" 
  FIELD rmno       AS CHAR  
  FIELD nation     AS CHAR 
  FIELD arrive     AS DATE 
  FIELD depart     AS DATE 
  FIELD zipreis    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR  
  FIELD a          AS INTEGER   FORMAT "9" 
  FIELD c          AS INTEGER   FORMAT "9" 
  FIELD co         AS INTEGER   FORMAT ">9" 
  FIELD nat        AS CHAR      FORMAT "x(3)" 
  FIELD lodging    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"  
  FIELD breakfast  AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
  FIELD lunch      AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
  FIELD dinner     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
  FIELD otherev    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD curr       AS CHAR      FORMAT "x(4)"
  FIELD paym       AS INTEGER   FORMAT ">>9" 
  FIELD segm       AS CHAR      FORMAT "x(12)"
  .   

DEFINE TEMP-TABLE s-list 
  FIELD rmcat       AS CHAR FORMAT "x(6)" 
  FIELD bezeich     AS CHAR FORMAT "x(24)" 
  FIELD nat         AS CHAR FORMAT "x(24)" 
  FIELD anz         AS INTEGER FORMAT ">>9" 
  FIELD adult       AS INTEGER FORMAT ">>9" 
  FIELD proz        AS DECIMAL FORMAT ">>9.99" 
  FIELD child       AS INTEGER FORMAT ">>9"
  FIELD proz-qty    AS DECIMAL FORMAT ">>9.99"
  FIELD rev         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
  FIELD proz-rev    AS DECIMAL FORMAT ">>9.99"
  FIELD arr         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
 . 

DEFINE TEMP-TABLE summary-roomtype 
    FIELD rmcat       AS CHAR FORMAT "x(6)" 
    FIELD bezeich     AS CHAR FORMAT "x(24)"     
    FIELD anz         AS INTEGER FORMAT ">>9"         
    FIELD proz-qty    AS DECIMAL FORMAT ">>9.99"
    FIELD rev         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD proz-rev    AS DECIMAL FORMAT ">>9.99"
    FIELD arr         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
. 

DEFINE TEMP-TABLE summary-nation     
    FIELD nat         AS CHAR      
    FIELD adult       AS CHAR
    FIELD proz        AS CHAR
    FIELD child       AS CHAR
. 

DEFINE TEMP-TABLE summary-revenue 
    FIELD currency      AS CHAR        
    FIELD room-rate     AS DECIMAL 
    FIELD lodging       AS DECIMAL 
    FIELD b-amount      AS DECIMAL 
    FIELD l-amount      AS DECIMAL
    FIELD d-amount      AS DECIMAL
    FIELD o-amount      AS DECIMAL
 . 

DEFINE TEMP-TABLE summary-segment
    FIELD segmcode  AS INTEGER
    FIELD segment   AS CHAR 
    FIELD anzahl    AS INTEGER
    FIELD proz-qty  AS DECIMAL
    FIELD rev       AS DECIMAL
    FIELD proz-rev  AS DECIMAL
    FIELD arr       AS DECIMAL
.

DEFINE TEMP-TABLE t-buff-queasy LIKE queasy.

DEFINE TEMP-TABLE sum-list
    FIELD curr      AS CHAR FORMAT "x(4)"
    FIELD zipreis   AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD lodging   AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD bfast     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD lunch     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD dinner    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD other     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    .

DEFINE TEMP-TABLE zikat-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD zikatnr  AS INTEGER 
    FIELD kurzbez  AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(32)"
.

DEFINE INPUT PARAMETER sorttype        AS INT.
DEFINE INPUT PARAMETER from-date       AS DATE.
DEFINE INPUT PARAMETER to-date         AS DATE.
DEFINE INPUT PARAMETER froom           AS CHAR.
DEFINE INPUT PARAMETER troom           AS CHAR.
DEFINE INPUT PARAMETER exc-depart      AS LOGICAL.
DEFINE INPUT PARAMETER incl-gcomment   AS LOGICAL.
DEFINE INPUT PARAMETER incl-rsvcomment AS LOGICAL.
DEFINE INPUT PARAMETER disp-accompany  AS LOGICAL.
DEFINE OUTPUT PARAMETER tot-payrm      AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-rm         AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-a          AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-c          AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-co         AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-avail      AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER inactive       AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-keycard    AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER TABLE FOR summary-roomtype.
DEFINE OUTPUT PARAMETER TABLE FOR summary-nation.
DEFINE OUTPUT PARAMETER TABLE FOR summary-revenue.
DEFINE OUTPUT PARAMETER TABLE FOR summary-segment.

DEFINE VARIABLE curr-date       AS DATE.
DEFINE VARIABLE curr-gastnr     AS INT.
DEFINE VARIABLE prog-name       AS CHAR INIT "PJ-inhouse4-summary".
DEFINE VARIABLE tot-qty         AS INTEGER.
DEFINE VARIABLE tot-rev         AS DECIMAL.
DEFINE VARIABLE company         AS CHAR NO-UNDO.
DEFINE VARIABLE counter         AS INTEGER NO-UNDO.

/*************************************** PROCCESS ***************************************/
RUN htpdate.p(87, OUTPUT curr-date).

FOR EACH zimkateg NO-LOCK BY zimkateg.kurzbez: 
    CREATE zikat-list. 
    ASSIGN 
      zikat-list.zikatnr = zimkateg.zikatnr 
      zikat-list.kurzbez = zimkateg.kurzbez 
      zikat-list.bezeich = zimkateg.bezeich. 
END. 
FOR EACH zikat-list:
    zikat-list.selected = YES.
END.

RUN pj-inhouse4-summary-cldbl.p
    (1, from-date, to-date, curr-date, curr-gastnr, froom, troom, exc-depart,
    incl-gcomment, incl-rsvcomment, "PJ-inhouse2", disp-accompany, INPUT TABLE zikat-list,
    OUTPUT tot-payrm, OUTPUT tot-rm, OUTPUT tot-a, OUTPUT tot-c,
    OUTPUT tot-co, OUTPUT tot-avail, OUTPUT inactive, OUTPUT tot-keycard,
    OUTPUT TABLE output-list, OUTPUT TABLE s-list, OUTPUT TABLE t-buff-queasy).

FOR EACH sum-list:
    DELETE sum-list.
END.

FOR EACH inhouse-guest-list:
    DELETE inhouse-guest-list.
END.

FOR EACH summary-roomtype:
    DELETE summary-roomtype.
END.

FOR EACH summary-nation:
    DELETE summary-nation.
END.

FOR EACH summary-revenue:
    DELETE summary-revenue.
END.

FOR EACH summary-segment:
    DELETE summary-segment.
END.



FOR EACH output-list :
    FIND FIRST tmplist WHERE tmplist.resnr EQ output-list.resnr AND tmplist.rmno EQ output-list.rmno NO-ERROR.
    IF NOT AVAILABLE tmplist THEN
    DO:
        CREATE tmplist.
        BUFFER-COPY output-list TO tmplist.
    END.
END.

FOR EACH tmplist WHERE tmplist.rmno GE froom AND tmplist.rmno LE troom:
    FIND FIRST sum-list WHERE sum-list.curr = ENTRY(1,tmplist.curr,";") NO-ERROR.
    IF NOT AVAILABLE sum-list THEN
    DO:
        CREATE sum-list.
        ASSIGN sum-list.curr = ENTRY(1,tmplist.curr,";").
    END.
    
    ASSIGN 
        sum-list.zipreis = sum-list.zipreis + tmplist.zipreis
        sum-list.lodging = sum-list.lodging + tmplist.lodging
        sum-list.bfast = sum-list.bfast + tmplist.breakfast
        sum-list.lunch = sum-list.lunch + tmplist.lunch
        sum-list.dinner = sum-list.dinner + tmplist.dinner
        sum-list.other = sum-list.other + tmplist.otherev
        . 

    FIND FIRST summary-segment WHERE summary-segment.segmcode = tmplist.paym NO-ERROR.
    IF NOT AVAILABLE summary-segment THEN
    DO:
        CREATE summary-segment.
        ASSIGN 
            summary-segment.segmcode = tmplist.paym               
            summary-segment.segment = tmplist.segm
            .
    END.
    ASSIGN 
        summary-segment.anzahl  = summary-segment.anzahl + tmplist.qty
        summary-segment.rev     = summary-segment.rev + tmplist.zipreis
        tot-qty                 = tot-qty + tmplist.qty
        tot-rev                 = tot-rev + tmplist.zipreis
     .
END.


/* Create Summary */
FOR EACH s-list WHERE s-list.rmcat NE "":
    CREATE summary-roomtype.
    ASSIGN 
        summary-roomtype.bezeich    = s-list.bezeich
        summary-roomtype.anz        = s-list.anz
        summary-roomtype.proz-qty   = s-list.proz-qty
        summary-roomtype.rev        = s-list.rev
        summary-roomtype.proz-rev   = s-list.proz-rev
        summary-roomtype.arr        = s-list.arr                
    .
END.

FOR EACH s-list WHERE s-list.nat NE "" :
    CREATE summary-nation.
    IF NUM-ENTRIES(s-list.nat, ";") GT 1 THEN summary-nation.nat = ENTRY(1, s-list.nat, ";").
    ELSE summary-nation.nat = s-list.nat.
   
    ASSIGN
    summary-nation.adult    = STRING(s-list.adult, ">>>>9")
    summary-nation.proz     = STRING(s-list.proz,  ">>9.99")
    summary-nation.child    = STRING(s-list.child, ">>>>9").
END.

CREATE summary-nation.
ASSIGN
    summary-nation.nat      = "T O T A L"
    summary-nation.adult    = STRING(tot-a + tot-co, ">>>>9")
    summary-nation.proz     = "100.00"
    summary-nation.child    = STRING(tot-c,">>>>9")
    .

CREATE summary-nation. /* Breake Line */
CREATE summary-nation.
ASSIGN
    summary-nation.nat      = "ROOM AVAILABLE"
    summary-nation.adult    = STRING(tot-avail, ">>,>>9")
    .

IF inactive NE 0 THEN
DO:
    CREATE summary-nation.
    ASSIGN
        summary-nation.nat      = "OCCUPIED/INACTIVE"
        summary-nation.adult    = STRING(tot-rm, ">>,>>9") + "/" + STRING(inactive)
        .
END.
ELSE
DO:
    CREATE summary-nation.
    ASSIGN
        summary-nation.nat      = "T O T A L  OCCUPIED"
        summary-nation.adult    = STRING(tot-rm, ">>,>>9")
        .
END.

CREATE summary-nation.
ASSIGN
    summary-nation.nat      = "AVRG GUEST/ROOM"
    summary-nation.adult    = STRING((tot-a + tot-co) / tot-rm, ">>,>>9.99")
    .

CREATE summary-nation.
ASSIGN
    summary-nation.nat      = "KEYCARD"
    summary-nation.adult    = STRING(tot-keycard, ">>,>>9")
    .

FOR EACH sum-list:
    CREATE summary-revenue.
    ASSIGN 
           summary-revenue.currency  = sum-list.curr
           summary-revenue.room-rate = sum-list.zipreis
           summary-revenue.lodging   = sum-list.lodging
           summary-revenue.b-amount  = sum-list.bfast 
           summary-revenue.l-amount  = sum-list.lunch
           summary-revenue.d-amount  = sum-list.dinner
           summary-revenue.o-amount  = sum-list.other             
        .
END.

FOR EACH summary-segment:
    ASSIGN 
        summary-segment.proz-qty = (summary-segment.anzahl / tot-qty) * 100
        summary-segment.proz-rev = (summary-segment.rev / tot-rev) * 100
        summary-segment.arr      = (summary-segment.rev / summary-segment.anzahl) 
        .           
END.

