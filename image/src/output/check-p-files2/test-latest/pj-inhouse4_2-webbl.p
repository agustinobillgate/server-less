DEFINE TEMP-TABLE inhouse-guest-list 
    FIELD flag          AS INTEGER 
    FIELD karteityp     AS INTEGER 
    FIELD nr            AS INTEGER   FORMAT ">>>9" 
    FIELD vip           AS CHAR      FORMAT "x(5)" 
    FIELD resnr         AS INTEGER   FORMAT ">>>>>9" 
    FIELD firstname     AS CHAR      FORMAT "x(32)" 
    FIELD lastname      AS CHAR      FORMAT "x(32)" 
    FIELD birthdate     AS CHAR      FORMAT "x(10)"
    FIELD groupname     AS CHAR      FORMAT "x(24)" 
    FIELD rmno          AS CHAR	  
    FIELD qty           AS INTEGER   FORMAT ">>9" 
    FIELD arrive        AS DATE 
    FIELD depart        AS DATE 
    FIELD rmcat         AS CHAR      FORMAT "x(6)" 
    FIELD ratecode      AS CHAR      FORMAT "x(15)"
    FIELD zipreis       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"
    FIELD kurzbez       AS CHAR 
    FIELD bezeich       AS CHAR 
    FIELD a             AS INTEGER   FORMAT "9" 
    FIELD c             AS INTEGER   FORMAT "9" 
    FIELD co            AS INTEGER   FORMAT ">9" 
    FIELD pax           AS CHAR      FORMAT "x(6)" 
    FIELD nat           AS CHAR      FORMAT "x(3)" 
    FIELD nation        AS CHAR 
    FIELD argt          AS CHAR      FORMAT "x(6)" 
    FIELD company       AS CHAR      FORMAT "x(18)" 
    FIELD flight        AS CHAR      FORMAT "x(6)" 
    FIELD etd           AS CHAR      FORMAT "99:99" 
    FIELD paym          AS INTEGER   FORMAT ">>9" 
    FIELD segm          AS CHAR      FORMAT "x(12)"
    FIELD telefon       AS CHAR      FORMAT "x(24)" 
    FIELD mobil-tel     AS CHAR      FORMAT "x(16)" 
    FIELD created       AS DATE      FORMAT "99/99/99"
    FIELD createid      AS CHAR      FORMAT "x(4)" /* Malik Serverless : FIELD createID -> FIELD createid */
    FIELD bemerk        AS CHAR      FORMAT "x(100)"
    FIELD bemerk1       AS CHAR      FORMAT "x(32)" 
    FIELD ci-time       AS CHAR
    FIELD curr          AS CHAR      FORMAT "x(4)"
    FIELD inhousedate   AS DATE
    FIELD sob           AS CHAR      FORMAT "x(25)" 
    FIELD gastnr        AS INTEGER
    FIELD lodging       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD breakfast     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD lunch         AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD dinner        AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
    FIELD otherev       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"       
    FIELD rechnr        AS INT            
    FIELD memberno      AS CHAR      FORMAT "x(15)"     
    FIELD membertype    AS CHAR      FORMAT "x(20)"     
    FIELD email         AS CHAR      FORMAT "x(30)"  
    FIELD localreg      AS CHAR      FORMAT "x(20)"  
    FIELD c-zipreis     AS CHAR      FORMAT "x(18)"
    FIELD c-lodging     AS CHAR     FORMAT "x(18)"
    FIELD c-breakfast   AS CHAR     FORMAT "x(18)"     
    FIELD c-lunch       AS CHAR     FORMAT "x(18)"    
    FIELD c-dinner      AS CHAR     FORMAT "x(18)"    
    FIELD c-otherev     AS CHAR     FORMAT "x(18)"
    FIELD c-a           AS CHAR  
    FIELD c-c           AS CHAR  
    FIELD c-co          AS CHAR  
    FIELD c-rechnr      AS CHAR  
    FIELD c-resnr       AS CHAR  
    FIELD night         AS CHAR     FORMAT "x(5)"
    FIELD city          AS CHAR     FORMAT "x(32)" 
    FIELD keycard       AS CHAR     FORMAT "x(6)"  
    FIELD co-time       AS CHAR                                     
    FIELD pay-art       AS CHAR     FORMAT "x(20)"
    FIELD etage         AS INTEGER
    FIELD zinr-bez      AS CHAR     /*Gerald 7E2311*/
    FIELD flag-guest    AS INTEGER  /*Gerald 7E2311*/
    .      

DEFINE TEMP-TABLE output-list 
    FIELD flag          AS INTEGER 
    FIELD karteityp     AS INTEGER 
    FIELD nr            AS INTEGER   FORMAT ">>>9" 
    FIELD vip           AS CHAR      FORMAT "x(5)" 
    FIELD resnr         AS INTEGER   FORMAT ">>>>>9" 
    FIELD firstname     AS CHAR      FORMAT "x(32)" 
    FIELD lastname      AS CHAR      FORMAT "x(32)" 
    FIELD birthdate     AS CHAR      FORMAT "x(10)"
    FIELD groupname     AS CHAR      FORMAT "x(24)" 
    FIELD rmno          AS CHAR	  
    FIELD qty           AS INTEGER   FORMAT ">>9" 
    FIELD arrive        AS DATE 
    FIELD depart        AS DATE 
    FIELD rmcat         AS CHAR      FORMAT "x(6)" 
    FIELD ratecode      AS CHAR      FORMAT "x(15)"
    FIELD zipreis       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"
    FIELD kurzbez       AS CHAR 
    FIELD bezeich       AS CHAR 
    FIELD a             AS INTEGER   FORMAT "9" 
    FIELD c             AS INTEGER   FORMAT "9" 
    FIELD co            AS INTEGER   FORMAT ">9" 
    FIELD pax           AS CHAR      FORMAT "x(6)" 
    FIELD nat           AS CHAR      FORMAT "x(3)" 
    FIELD nation        AS CHAR 
    FIELD argt          AS CHAR      FORMAT "x(6)" 
    FIELD company       AS CHAR      FORMAT "x(18)" 
    FIELD flight        AS CHAR      FORMAT "x(6)" 
    FIELD etd           AS CHAR      FORMAT "99:99" 
    FIELD paym          AS INTEGER   FORMAT ">>9" 
    FIELD segm          AS CHAR      FORMAT "x(12)"
    FIELD telefon       AS CHAR      FORMAT "x(24)" 
    FIELD mobil-tel     AS CHAR      FORMAT "x(16)" 
    FIELD created       AS DATE      FORMAT "99/99/99"
    FIELD createid      AS CHAR      FORMAT "x(4)" /* Malik Serverless : FIELD createID -> FIELD createid */
    FIELD bemerk        AS CHAR      FORMAT "x(100)"
    FIELD bemerk1       AS CHAR      FORMAT "x(32)" 
    FIELD ci-time       AS CHAR
    FIELD curr          AS CHAR      FORMAT "x(4)"
    FIELD inhousedate   AS DATE
    FIELD sob           AS CHAR      FORMAT "x(25)" 
    FIELD gastnr        AS INTEGER
    FIELD lodging       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD breakfast     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD lunch         AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD dinner        AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
    FIELD otherev       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"       
    FIELD rechnr        AS INT            
    FIELD memberno      AS CHAR      FORMAT "x(15)"     
    FIELD membertype    AS CHAR      FORMAT "x(20)"     
    FIELD email         AS CHAR      FORMAT "x(30)"  
    FIELD localreg      AS CHAR      FORMAT "x(20)"  
    FIELD c-zipreis     AS CHAR      FORMAT "x(18)"
    FIELD c-lodging     AS CHAR     FORMAT "x(18)"
    FIELD c-breakfast   AS CHAR     FORMAT "x(18)"     
    FIELD c-lunch       AS CHAR     FORMAT "x(18)"    
    FIELD c-dinner      AS CHAR     FORMAT "x(18)"    
    FIELD c-otherev     AS CHAR     FORMAT "x(18)"
    FIELD c-a           AS CHAR  
    FIELD c-c           AS CHAR  
    FIELD c-co          AS CHAR  
    FIELD c-rechnr      AS CHAR  
    FIELD c-resnr       AS CHAR  
    FIELD night         AS CHAR     FORMAT "x(5)"
    FIELD city          AS CHAR     FORMAT "x(32)" 
    FIELD keycard       AS CHAR     FORMAT "x(6)"  
    FIELD co-time       AS CHAR                                     
    FIELD pay-art       AS CHAR     FORMAT "x(20)" 
    FIELD etage         AS INTEGER
    FIELD zinr-bez      AS CHAR     /*Gerald 7E2311*/
    FIELD flag-guest    AS INTEGER  /*Gerald 7E2311*/
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


DEFINE TEMP-TABLE zikat-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD zikatnr  AS INTEGER 
    FIELD kurzbez  AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(32)"
.

DEFINE TEMP-TABLE t-buff-queasy LIKE queasy.

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
DEFINE TEMP-TABLE summary-list4 /*bernatd*/
    FIELD argt         AS CHAR
    FIELD rm-qty       AS INTEGER
    FIELD pax          AS INTEGER
   /*FIELD bfast        AS DECIMAL*/
.

DEFINE TEMP-TABLE sum-list
    FIELD curr      AS CHAR FORMAT "x(4)"
    FIELD zipreis   AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD lodging   AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD bfast     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD lunch     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD dinner    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD other     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
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
  FIELD argt       AS CHAR      FORMAT "x(6)"
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
DEFINE INPUT PARAMETER idFlag          AS CHAR.
DEFINE INPUT PARAMETER exc-compli      AS LOGICAL. /*Bernatd 9D155B 2025*/


DEFINE VARIABLE curr-date       AS DATE.
DEFINE VARIABLE curr-gastnr     AS INT.

DEFINE VARIABLE str    AS CHAR NO-UNDO.
DEFINE VARIABLE htl-no AS CHAR NO-UNDO.
DEFINE STREAM s1.

DEFINE VARIABLE tdate   AS CHAR NO-UNDO.
DEFINE VARIABLE crdate  AS CHAR NO-UNDO.
DEFINE VARIABLE cgdate  AS CHAR NO-UNDO.
DEFINE VARIABLE counter AS INTEGER NO-UNDO.
DEFINE VARIABLE company AS CHAR NO-UNDO.

DEFINE VARIABLE tot-payrm   AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-rm      AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-a       AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-c       AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-co      AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-avail   AS INTEGER INITIAL 0.  
DEFINE VARIABLE inactive    AS INTEGER INITIAL 0.  
DEFINE VARIABLE tot-keycard AS INTEGER INITIAL 0.
DEFINE VARIABLE bemerk      AS CHAR.
DEFINE VARIABLE bemerk1     AS CHAR.
DEFINE VARIABLE bezeich     AS CHAR. 

DEFINE VARIABLE tot-qty         AS INTEGER.
DEFINE VARIABLE tot-rev         AS DECIMAL.
DEFINE VARIABLE ct              AS INTEGER.
DEFINE VARIABLE tmp-rmcat       AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-nat         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-adult         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-proz         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-child         AS CHAR. /* Malik Serverless 258 */


DEFINE VARIABLE tmp-flag        AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-vip         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-firstname         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-lastname         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-birthdate         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-groupname         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-rmno         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-qty         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-arrive         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-depart         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-rmcat-que         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-ratecode         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-kurzbez         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-pax         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-nat-que         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-nation         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-argt         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-company         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-flight         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-etd         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-segm         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-telefon         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-mobil-tel         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-created         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-createid         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-ci-time         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-curr         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-sob         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-memberno         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-membertype         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-email         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-localreg         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-zipreis         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-lodging         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-breakfast         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-lunch         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-dinner         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-otherev         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-a         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-c         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-co         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-rechnr         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-c-resnr         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-night         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-city         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-keycard         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-co-time         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-pay-art         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-zinr-bez         AS CHAR. /* Malik Serverless 258 */
DEFINE VARIABLE tmp-bezeich         AS CHAR.
DEFINE VARIABLE tmp-currency        AS CHAR.
DEFINE VARIABLE tmp-segment         AS CHAR.
DEFINE VARIABLE tmp-sum-curr            AS CHAR.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.


/*************************************** PROCCESS ***************************************/
CREATE queasy.
ASSIGN queasy.KEY      = 285
       queasy.char1    = "Inhouse List"
       queasy.number1  = 1
       queasy.number2  = INT(idFlag).
RELEASE queasy.

CREATE queasy.
ASSIGN queasy.KEY      = 285
       queasy.char1    = "Inhouse List Sum"
       queasy.number1  = 1
       queasy.number2  = INT(idFlag).
RELEASE queasy.


DEFINE VARIABLE curr-time AS INTEGER.
ASSIGN curr-time = TIME.

RUN htpdate.p(87, OUTPUT curr-date).

FOR EACH zimkateg NO-LOCK BY zimkateg.kurzbez: 
    CREATE zikat-list. 
    ASSIGN 
      zikat-list.zikatnr = zimkateg.zikatnr 
      zikat-list.kurzbez = zimkateg.kurzbez 
      zikat-list.bezeich = zimkateg.bezeichnung. /* Malik Serverless : zimkateg.bezeich -> zimkateg.bezeichnung */
END. 
FOR EACH zikat-list:
    zikat-list.selected = YES.
END.


FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
  RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 


RUN pj-inhouse4-btn-go_5-cldbl.p
    (1, from-date, to-date, curr-date, curr-gastnr, froom, troom, exc-depart,
    incl-gcomment, incl-rsvcomment, "PJ-inhouse2", disp-accompany,exc-compli, INPUT TABLE zikat-list,
    OUTPUT tot-payrm, OUTPUT tot-rm, OUTPUT tot-a, OUTPUT tot-c,
    OUTPUT tot-co, OUTPUT tot-avail, OUTPUT inactive, OUTPUT tot-keycard,
    OUTPUT TABLE output-list, OUTPUT TABLE s-list, OUTPUT TABLE t-buff-queasy).



IF sorttype EQ 1 OR sorttype EQ 3 THEN /* By RoomNo */
DO:
    IF sorttype EQ 1 THEN
    DO:
        FOR EACH output-list NO-LOCK BY output-list.nr:
            counter = counter + 1.
            ASSIGN output-list.nr = counter.
    
            CREATE inhouse-guest-list.
            BUFFER-COPY output-list TO inhouse-guest-list.
        END.
    END.
    ELSE
    DO:
        FOR EACH output-list NO-LOCK BY output-list.etage BY output-list.rmno:
            counter = counter + 1.
            ASSIGN output-list.nr = counter.
    
            CREATE inhouse-guest-list.
            BUFFER-COPY output-list TO inhouse-guest-list.
        END.
    END.
END.
ELSE /* By Compnay */
DO:
    DEFINE BUFFER bufflist FOR output-list.

    FOR EACH output-list BY output-list.company:
        IF company NE output-list.company THEN
        DO:
            company = output-list.company.
            CREATE inhouse-guest-list.
            inhouse-guest-list.rmcat = output-list.company.

            FOR EACH bufflist WHERE bufflist.company EQ company:
                counter = counter + 1.
                CREATE inhouse-guest-list.
                BUFFER-COPY bufflist TO inhouse-guest-list.
                inhouse-guest-list.nr = counter.
            END.   
            CREATE inhouse-guest-list.
        END.
    END.
END.

/*summary*/

FOR EACH sum-list:
    DELETE sum-list.
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

FOR EACH summary-list4:
    DELETE summary-list4.
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


     FIND FIRST summary-list4 WHERE summary-list4.argt = tmplist.argt NO-ERROR.
     IF NOT AVAILABLE summary-list4 THEN
     DO:
         CREATE summary-list4.
         ASSIGN
            summary-list4.argt   = tmplist.argt.
     END.
     ASSIGN
         summary-list4.rm-qty = summary-list4.rm-qty + tmplist.qty
         summary-list4.pax    = summary-list4.pax + tmplist.a + tmplist.co.
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

/*end*/

/* Malik serverless */
FOR EACH inhouse-guest-list:

    IF inhouse-guest-list.bezeich = ? THEN bezeich = "".
    ELSE bezeich = inhouse-guest-list.bezeich.
    IF inhouse-guest-list.bemerk = ? THEN bemerk = "".
    ELSE bemerk = inhouse-guest-list.bemerk.
    IF inhouse-guest-list.bemerk1 = ? THEN bemerk1 = "".
    ELSE bemerk1 = inhouse-guest-list.bemerk1.

    ASSIGN bezeich = REPLACE(bezeich, CHR(10),"")
           bezeich = REPLACE(bezeich, CHR(13),"")
           bemerk  = REPLACE(bemerk, CHR(10),"")
           bemerk  = REPLACE(bemerk, CHR(13),"")
           bemerk  = REPLACE(bemerk, "|","")
           counter          = counter + 1
           .

    RUN add-html(bezeich,OUTPUT bezeich).
    RUN clean-html(bezeich,OUTPUT bezeich).

    RUN add-html(bemerk,OUTPUT bemerk).
    RUN clean-html(bemerk,OUTPUT bemerk).
    
    RUN add-html(bemerk1,OUTPUT bemerk1).
    RUN clean-html(bemerk1,OUTPUT bemerk1).

    /* Malik Serverless for case 258 */
    IF inhouse-guest-list.flag NE ? THEN 
    DO:
        tmp-flag = STRING(inhouse-guest-list.flag).
    END.
    ELSE
    DO:
        tmp-flag = "".
    END.

    IF inhouse-guest-list.vip NE ? THEN 
    DO:
        tmp-vip = inhouse-guest-list.vip.
    END.
    ELSE
    DO:
        tmp-vip = "".
    END.
    
    IF inhouse-guest-list.firstname NE ? THEN 
    DO:
        tmp-firstname = inhouse-guest-list.firstname.
    END.
    ELSE
    DO:
        tmp-firstname = "".
    END.

    IF inhouse-guest-list.lastname NE ? THEN 
    DO:
        tmp-lastname = inhouse-guest-list.lastname.
    END.
    ELSE
    DO:
        tmp-lastname = "".
    END.

    IF inhouse-guest-list.birthdate NE ? THEN 
    DO:
        tmp-birthdate = inhouse-guest-list.birthdate.
    END.
    ELSE
    DO:
        tmp-birthdate = "".
    END.

    IF inhouse-guest-list.groupname NE ? THEN 
    DO:
        tmp-groupname = inhouse-guest-list.groupname.
    END.
    ELSE
    DO:
        tmp-groupname = "".
    END.

    IF inhouse-guest-list.rmno NE ? THEN 
    DO:
        tmp-rmno = inhouse-guest-list.rmno.
    END.
    ELSE
    DO:
        tmp-rmno = "".
    END.

    IF inhouse-guest-list.qty NE ? THEN 
    DO:
        tmp-qty = STRING(inhouse-guest-list.qty).
    END.
    ELSE
    DO:
        tmp-qty = "".
    END.

    IF inhouse-guest-list.arrive NE ? THEN 
    DO:
        tmp-arrive = STRING(inhouse-guest-list.arrive).
    END.
    ELSE
    DO:
        tmp-arrive = "".
    END.

    IF inhouse-guest-list.depart NE ? THEN 
    DO:
        tmp-depart = STRING(inhouse-guest-list.depart).
    END.
    ELSE
    DO:
        tmp-depart = "".
    END.

    IF inhouse-guest-list.rmcat NE ? THEN 
    DO:
        tmp-rmcat-que = inhouse-guest-list.rmcat.
    END.
    ELSE
    DO:
        tmp-rmcat-que = "".
    END.

    IF inhouse-guest-list.ratecode NE ? THEN 
    DO:
        tmp-ratecode = inhouse-guest-list.ratecode.
    END.
    ELSE
    DO:
        tmp-ratecode = "".
    END.

    IF inhouse-guest-list.kurzbez NE ? THEN 
    DO:
        tmp-kurzbez = inhouse-guest-list.kurzbez.
    END.
    ELSE
    DO:
        tmp-kurzbez = "".
    END.

    IF inhouse-guest-list.pax NE ? THEN 
    DO:
        tmp-pax = inhouse-guest-list.pax.
    END.
    ELSE
    DO:
        tmp-pax = "".
    END.

    IF inhouse-guest-list.nat NE ? THEN 
    DO:
        tmp-nat-que = inhouse-guest-list.nat.
    END.
    ELSE
    DO:
        tmp-nat-que = "".
    END.

    IF inhouse-guest-list.nation NE ? THEN 
    DO:
        tmp-nation = inhouse-guest-list.nation.
    END.
    ELSE
    DO:
        tmp-nation = "".
    END.

    IF inhouse-guest-list.argt NE ? THEN 
    DO:
        tmp-argt = inhouse-guest-list.argt.
    END.
    ELSE
    DO:
        tmp-argt = "".
    END.

    IF inhouse-guest-list.company NE ? THEN 
    DO:
        tmp-company = inhouse-guest-list.company.
    END.
    ELSE
    DO:
        tmp-company = "".
    END.

    IF inhouse-guest-list.flight NE ? THEN 
    DO:
        tmp-flight = inhouse-guest-list.flight.
    END.
    ELSE
    DO:
        tmp-flight = "".
    END.

    IF inhouse-guest-list.etd NE ? THEN 
    DO:
        tmp-etd = inhouse-guest-list.etd.
    END.
    ELSE
    DO:
        tmp-etd = "".
    END.

    IF inhouse-guest-list.segm NE ? THEN 
    DO:
        tmp-segm = inhouse-guest-list.segm.
    END.
    ELSE
    DO:
        tmp-segm = "".
    END.

    IF inhouse-guest-list.telefon NE ? THEN 
    DO:
        tmp-telefon = inhouse-guest-list.telefon.
    END.
    ELSE
    DO:
        tmp-telefon = "".
    END.

    IF inhouse-guest-list.mobil-tel NE ? THEN 
    DO:
        tmp-mobil-tel = inhouse-guest-list.mobil-tel.
    END.
    ELSE
    DO:
        tmp-mobil-tel = "".
    END.

    IF inhouse-guest-list.created NE ? THEN 
    DO:
        tmp-created = STRING(inhouse-guest-list.created).
    END.
    ELSE
    DO:
        tmp-created = "".
    END.

    IF inhouse-guest-list.createid NE ? THEN 
    DO:
        tmp-createid = inhouse-guest-list.createid.
    END.
    ELSE
    DO:
        tmp-createid = "".
    END.

    IF inhouse-guest-list.ci-time NE ? THEN 
    DO:
        tmp-ci-time = inhouse-guest-list.ci-time.
    END.
    ELSE
    DO:
        tmp-ci-time = "".
    END.

    IF inhouse-guest-list.curr NE ? THEN 
    DO:
        tmp-curr = inhouse-guest-list.curr.
    END.
    ELSE
    DO:
        tmp-curr = "".
    END.

    IF inhouse-guest-list.sob NE ? THEN 
    DO:
        tmp-sob = inhouse-guest-list.sob.
    END.
    ELSE
    DO:
        tmp-sob = "".
    END.

    IF inhouse-guest-list.memberno NE ? THEN 
    DO:
        tmp-memberno = inhouse-guest-list.memberno.
    END.
    ELSE
    DO:
        tmp-memberno = "".
    END.

    IF inhouse-guest-list.membertype NE ? THEN 
    DO:
        tmp-membertype = inhouse-guest-list.membertype.
    END.
    ELSE
    DO:
        tmp-membertype = "".
    END.

    IF inhouse-guest-list.email NE ? THEN 
    DO:
        tmp-email = inhouse-guest-list.email.
    END.
    ELSE
    DO:
        tmp-email = "".
    END.

    IF inhouse-guest-list.localreg NE ? THEN 
    DO:
        tmp-localreg = inhouse-guest-list.localreg.
    END.
    ELSE
    DO:
        tmp-localreg = "".
    END.

    IF inhouse-guest-list.c-zipreis NE ? THEN 
    DO:
        tmp-c-zipreis = inhouse-guest-list.c-zipreis.
    END.
    ELSE
    DO:
        tmp-c-zipreis = "".
    END.

    IF inhouse-guest-list.c-lodging NE ? THEN 
    DO:
        tmp-c-lodging = inhouse-guest-list.c-lodging.
    END.
    ELSE
    DO:
        tmp-c-lodging = "".
    END.

    IF inhouse-guest-list.c-breakfast NE ? THEN 
    DO:
        tmp-c-breakfast = inhouse-guest-list.c-breakfast.
    END.
    ELSE
    DO:
        tmp-c-breakfast = "".
    END.

    IF inhouse-guest-list.c-lunch NE ? THEN 
    DO:
        tmp-c-lunch = inhouse-guest-list.c-lunch.
    END.
    ELSE
    DO:
        tmp-c-lunch = "".
    END.

    IF inhouse-guest-list.c-dinner NE ? THEN 
    DO:
        tmp-c-dinner = inhouse-guest-list.c-dinner.
    END.
    ELSE
    DO:
        tmp-c-dinner = "".
    END.

    IF inhouse-guest-list.c-otherev NE ? THEN 
    DO:
        tmp-c-otherev = inhouse-guest-list.c-otherev.
    END.
    ELSE
    DO:
        tmp-c-otherev = "".
    END.

    IF inhouse-guest-list.c-a NE ? THEN 
    DO:
        tmp-c-a = inhouse-guest-list.c-a.
    END.
    ELSE
    DO:
        tmp-c-a = "".
    END.

    IF inhouse-guest-list.c-c NE ? THEN 
    DO:
        tmp-c-c = inhouse-guest-list.c-c.
    END.
    ELSE
    DO:
        tmp-c-c = "".
    END.

    IF inhouse-guest-list.c-co NE ? THEN 
    DO:
        tmp-c-co = inhouse-guest-list.c-co.
    END.
    ELSE
    DO:
        tmp-c-co = "".
    END.

    IF inhouse-guest-list.c-rechnr NE ? THEN 
    DO:
        tmp-c-rechnr = inhouse-guest-list.c-rechnr.
    END.
    ELSE
    DO:
        tmp-c-rechnr = "".
    END.

    IF inhouse-guest-list.c-resnr NE ? THEN 
    DO:
        tmp-c-resnr = inhouse-guest-list.c-resnr.
    END.
    ELSE
    DO:
        tmp-c-resnr = "".
    END.

    IF inhouse-guest-list.night NE ? THEN 
    DO:
        tmp-night = inhouse-guest-list.night.
    END.
    ELSE
    DO:
        tmp-night = "".
    END.

    IF inhouse-guest-list.city NE ? THEN 
    DO:
        tmp-city = inhouse-guest-list.city.
    END.
    ELSE
    DO:
        tmp-city = "".
    END.

    IF inhouse-guest-list.keycard NE ? THEN 
    DO:
        tmp-keycard = inhouse-guest-list.keycard.
    END.
    ELSE
    DO:
        tmp-keycard = "".
    END.

    IF inhouse-guest-list.co-time NE ? THEN 
    DO:
        tmp-co-time = inhouse-guest-list.co-time.
    END.
    ELSE
    DO:
        tmp-co-time = "".
    END.

    IF inhouse-guest-list.pay-art NE ? THEN 
    DO:
        tmp-pay-art = inhouse-guest-list.pay-art.
    END.
    ELSE
    DO:
        tmp-pay-art = "".
    END.

    IF inhouse-guest-list.zinr-bez NE ? THEN 
    DO:
        tmp-zinr-bez = inhouse-guest-list.zinr-bez.
    END.
    ELSE
    DO:
        tmp-zinr-bez = "".
    END.
    /* END Malik */

    /*Start Bernatd 7DA94E*/
    IF tmp-vip MATCHES "*|*" THEN tmp-vip = REPLACE(tmp-vip,"|","&").
    ELSE tmp-vip = tmp-vip.

    IF tmp-firstname MATCHES "*|*" THEN tmp-firstname = REPLACE(tmp-firstname,"|","&").
    ELSE tmp-firstname = tmp-firstname.

    IF tmp-lastname MATCHES "*|*" THEN tmp-lastname = REPLACE(tmp-lastname,"|","&").
    ELSE tmp-lastname = tmp-lastname.

    IF tmp-groupname MATCHES "*|*" THEN tmp-groupname = REPLACE(tmp-groupname,"|"," ").
    ELSE tmp-groupname = tmp-groupname.

    IF tmp-birthdate MATCHES "*|*" THEN tmp-birthdate = REPLACE(tmp-birthdate,"|"," ").
    ELSE tmp-birthdate = tmp-birthdate.

    IF tmp-rmno MATCHES "*|*" THEN tmp-rmno = REPLACE(tmp-rmno,"|"," ").
    ELSE tmp-rmno = tmp-rmno.

    IF tmp-rmcat-que MATCHES "*|*" THEN tmp-rmcat-que = REPLACE(tmp-rmcat-que,"|"," ").
    ELSE tmp-rmcat-que = tmp-rmcat-que.

    IF tmp-ratecode MATCHES "*|*" THEN tmp-ratecode = REPLACE(tmp-ratecode,"|"," ").
    ELSE tmp-ratecode = tmp-ratecode.

    IF tmp-kurzbez MATCHES "*|*" THEN tmp-kurzbez = REPLACE(tmp-kurzbez,"|"," ").
    ELSE tmp-kurzbez = tmp-kurzbez.

    IF tmp-pax MATCHES "*|*" THEN tmp-pax  = REPLACE(tmp-pax ,"|"," ").
    ELSE tmp-pax  = tmp-pax.

    IF tmp-nat-que MATCHES "*|*" THEN tmp-nat-que  = REPLACE(tmp-nat-que ,"|"," ").
    ELSE tmp-nat-que  = tmp-nat-que.

    IF tmp-nation MATCHES "*|*" THEN tmp-nation  = REPLACE(tmp-nation ,"|"," ").
    ELSE tmp-nation  = tmp-nation.

    IF tmp-argt MATCHES "*|*" THEN tmp-argt  = REPLACE(tmp-argt ,"|"," ").
    ELSE tmp-argt  = tmp-argt.

    IF tmp-company MATCHES "*|*" THEN tmp-company  = REPLACE(tmp-company ,"|"," ").
    ELSE tmp-company  = tmp-company.

    IF tmp-flight MATCHES "*|*" THEN tmp-flight  = REPLACE(tmp-flight ,"|"," ").
    ELSE tmp-flight  = tmp-flight.

    IF tmp-etd MATCHES "*|*" THEN tmp-etd  = REPLACE(tmp-etd ,"|"," ").
    ELSE tmp-etd  = tmp-etd.

    IF tmp-segm MATCHES "*|*" THEN tmp-segm  = REPLACE(tmp-segm ,"|"," ").
    ELSE tmp-segm  = tmp-segm.

    IF tmp-telefon MATCHES "*|*" THEN tmp-telefon  = REPLACE(tmp-telefon ,"|"," ").
    ELSE tmp-telefon  = tmp-telefon.

    IF tmp-mobil-tel MATCHES "*|*" THEN tmp-mobil-tel  = REPLACE(tmp-mobil-tel ,"|"," ").
    ELSE tmp-mobil-tel  = tmp-mobil-tel.

    IF tmp-createid MATCHES "*|*" THEN tmp-createid  = REPLACE(tmp-createid ,"|"," ").
    ELSE tmp-createid  = tmp-createid.

    IF tmp-ci-time MATCHES "*|*" THEN tmp-ci-time  = REPLACE(tmp-ci-time ,"|"," ").
    ELSE tmp-ci-time  = tmp-ci-time.

    IF tmp-curr MATCHES "*|*" THEN tmp-curr  = REPLACE(tmp-curr ,"|"," ").
    ELSE tmp-curr  = tmp-curr.

    IF tmp-sob MATCHES "*|*" THEN tmp-sob  = REPLACE(tmp-sob ,"|"," ").
    ELSE tmp-sob  = tmp-sob.

    IF tmp-memberno MATCHES "*|*" THEN tmp-memberno  = REPLACE(tmp-memberno ,"|"," ").
    ELSE tmp-memberno  = tmp-memberno.

    IF tmp-membertype MATCHES "*|*" THEN tmp-membertype = REPLACE(tmp-membertype,"|"," ").
    ELSE tmp-membertype = tmp-membertype.

    IF tmp-email MATCHES "*|*" THEN tmp-email = REPLACE(tmp-email,"|"," ").
    ELSE tmp-email = tmp-email.

    IF tmp-localreg MATCHES "*|*" THEN tmp-localreg = REPLACE(tmp-localreg,"|"," ").
    ELSE tmp-localreg = tmp-localreg.

    IF tmp-c-zipreis MATCHES "*|*" THEN tmp-c-zipreis = REPLACE(tmp-c-zipreis,"|"," ").
    ELSE tmp-c-zipreis = tmp-c-zipreis.

    IF tmp-c-lodging MATCHES "*|*" THEN tmp-c-lodging = REPLACE(tmp-c-lodging,"|"," ").
    ELSE tmp-c-lodging = tmp-c-lodging.

    IF tmp-c-breakfast MATCHES "*|*" THEN tmp-c-breakfast = REPLACE(tmp-c-breakfast,"|"," ").
    ELSE tmp-c-breakfast = tmp-c-breakfast.

    IF tmp-c-lunch MATCHES "*|*" THEN tmp-c-lunch = REPLACE(tmp-c-lunch,"|"," ").
    ELSE tmp-c-lunch = tmp-c-lunch.

    IF tmp-c-dinner MATCHES "*|*" THEN tmp-c-dinner = REPLACE(tmp-c-dinner,"|"," ").
    ELSE tmp-c-dinner = tmp-c-dinner.

    IF tmp-c-otherev MATCHES "*|*" THEN tmp-c-otherev = REPLACE(tmp-c-otherev,"|"," ").
    ELSE tmp-c-otherev = tmp-c-otherev.

    IF tmp-c-a MATCHES "*|*" THEN tmp-c-a = REPLACE(tmp-c-a,"|"," ").
    ELSE tmp-c-a = tmp-c-a.

    IF tmp-c-c MATCHES "*|*" THEN tmp-c-c = REPLACE(tmp-c-c,"|"," ").
    ELSE tmp-c-c = tmp-c-c.

    IF tmp-c-co MATCHES "*|*" THEN tmp-c-co = REPLACE(tmp-c-co,"|"," ").
    ELSE tmp-c-co = tmp-c-co.

    IF tmp-c-rechnr MATCHES "*|*" THEN tmp-c-rechnr = REPLACE(tmp-c-rechnr,"|"," ").
    ELSE tmp-c-rechnr = tmp-c-rechnr.
    
    IF tmp-c-resnr MATCHES "*|*" THEN tmp-c-resnr = REPLACE(tmp-c-resnr,"|"," ").
    ELSE tmp-c-resnr = tmp-c-resnr.

    IF tmp-night MATCHES "*|*" THEN tmp-night = REPLACE(tmp-night,"|"," ").
    ELSE tmp-night = tmp-night.

    IF tmp-city MATCHES "*|*" THEN tmp-city = REPLACE(tmp-city,"|"," ").
    ELSE tmp-city = tmp-city.

    IF tmp-keycard MATCHES "*|*" THEN tmp-keycard = REPLACE(tmp-keycard,"|"," ").
    ELSE tmp-keycard = tmp-keycard.

    IF tmp-co-time MATCHES "*|*" THEN tmp-co-time = REPLACE(tmp-co-time,"|"," ").
    ELSE tmp-co-time = tmp-co-time.

    IF tmp-pay-art MATCHES "*|*" THEN tmp-pay-art = REPLACE(tmp-pay-art,"|"," ").
    ELSE tmp-pay-art = tmp-pay-art.

    IF tmp-zinr-bez MATCHES "*|*" THEN tmp-zinr-bez   = REPLACE(tmp-zinr-bez  ,"|"," ").
    ELSE tmp-zinr-bez   = tmp-zinr-bez.

    IF tmp-zinr-bez MATCHES "*|*" THEN tmp-zinr-bez   = REPLACE(tmp-zinr-bez  ,"|"," ").
    ELSE tmp-zinr-bez   = tmp-zinr-bez.
    /*END Bernatd 7DA94E*/

    CREATE queasy.
    ASSIGN queasy.KEY   = 280
           queasy.char1 = "Inhouse List"
           queasy.number2 = INT(idFlag)
           queasy.char3 = STRING(bezeich)                                + "|" +
                          STRING(bemerk)                                 + "|" +
                          STRING(bemerk1)                                  
           queasy.char2 = tmp-flag                               + "|" +  /* 1 malik serverless 258*/
                          STRING(inhouse-guest-list.karteityp)   + "|" +  /*2*/
                          STRING(inhouse-guest-list.nr)          + "|" +  /*3*/
                          tmp-vip                                + "|" +  /*4*/
                          STRING(inhouse-guest-list.resnr)       + "|" +  /*5*/
                          tmp-firstname                          + "|" +  /*6*/
                          tmp-lastname                           + "|" +  /*7*/
                          tmp-birthdate                          + "|" +  /*8*/
                          tmp-groupname                          + "|" +  /*9*/
                          tmp-rmno                               + "|" +  /*10*/
                          tmp-qty                                + "|" +  /*11*/
                          tmp-arrive                             + "|" +  /*12*/
                          tmp-depart                             + "|" +  /*13*/
                          tmp-rmcat-que                              + "|" +  /*14*/
                          tmp-ratecode                           + "|" +  /*15*/
                          STRING(inhouse-guest-list.zipreis)     + "|" +  /*16*/
                          tmp-kurzbez                            + "|" +  /*17*/
                          STRING(inhouse-guest-list.a)           + "|" +  /*18*/
                          STRING(inhouse-guest-list.c)           + "|" +  /*19*/
                          STRING(inhouse-guest-list.co)          + "|" +  /*20*/
                          tmp-pax                                + "|" +  /*21*/
                          tmp-nat-que                                + "|" +  /*22*/
                          tmp-nation                             + "|" +  /*23*/
                          tmp-argt                               + "|" +  /*24*/
                          tmp-company                            + "|" +  /*25*/
                          tmp-flight                             + "|" +  /*26*/
                          tmp-etd                                + "|" +  /*27*/
                          STRING(inhouse-guest-list.paym)        + "|" +  /*28*/
                          tmp-segm                               + "|" +  /*29*/
                          tmp-telefon                            + "|" +  /*30*/
                          tmp-mobil-tel                          + "|" +  /*31*/
                          tmp-created     + "|" +  /*32*/
                          tmp-createid                           + "|" +  /*33 (Malik serverless : inhouse-guest-list.createID -> inhouse-guest-list.createid) */ 
                          tmp-ci-time                            + "|" +  /*34*/
                          tmp-curr                               + "|" +  /*35*/
                          STRING(inhouse-guest-list.inhousedate) + "|" +  /*36*/
                          tmp-sob                                + "|" +  /*37*/
                          STRING(inhouse-guest-list.gastnr)      + "|" +  /*38*/
                          STRING(inhouse-guest-list.lodging)     + "|" +  /*39*/
                          STRING(inhouse-guest-list.breakfast)   + "|" +  /*40*/
                          STRING(inhouse-guest-list.lunch)       + "|" +  /*41*/
                          STRING(inhouse-guest-list.dinner)      + "|" +  /*42*/
                          STRING(inhouse-guest-list.otherev)     + "|" +  /*43*/
                          STRING(inhouse-guest-list.rechnr)      + "|" +  /*44*/
                          tmp-memberno            + "|" +  /*45*/
                          tmp-membertype          + "|" +  /*46*/
                          tmp-email               + "|" +  /*47*/
                          tmp-localreg            + "|" +  /*48*/
                          tmp-c-zipreis           + "|" +  /*49*/
                          tmp-c-lodging           + "|" +  /*50*/
                          tmp-c-breakfast         + "|" +  /*51*/
                          tmp-c-lunch             + "|" +  /*52*/
                          tmp-c-dinner            + "|" +  /*53*/
                          tmp-c-otherev           + "|" +  /*54*/
                          tmp-c-a                 + "|" +  /*55*/
                          tmp-c-c                 + "|" +  /*56*/
                          tmp-c-co                + "|" +  /*57*/
                          tmp-c-rechnr            + "|" +  /*58*/
                          tmp-c-resnr             + "|" +  /*59*/
                          tmp-night               + "|" +  /*60*/
                          tmp-city                + "|" +  /*61*/
                          tmp-keycard             + "|" +  /*62*/
                          tmp-co-time             + "|" +  /*63*/
                          tmp-pay-art             + "|" +  /*64*/
                          STRING(inhouse-guest-list.etage)       + "|" +  /*65*/
                          tmp-zinr-bez            + "|" +  /*66*/
                          STRING(inhouse-guest-list.flag-guest)           /*67*/
            queasy.number1 = counter.


         
    RELEASE queasy.         
    
END.
/* END Malik */

/* commment for serverless
FIND FIRST inhouse-guest-list NO-ERROR.
DO WHILE AVAILABLE inhouse-guest-list:

    IF inhouse-guest-list.bezeich = ? THEN bezeich = "".
    ELSE bezeich = inhouse-guest-list.bezeich.
    IF inhouse-guest-list.bemerk = ? THEN bemerk = "".
    ELSE bemerk = inhouse-guest-list.bemerk.
    IF inhouse-guest-list.bemerk1 = ? THEN bemerk1 = "".
    ELSE bemerk1 = inhouse-guest-list.bemerk1.

    ASSIGN bezeich = REPLACE(bezeich, CHR(10),"")
           bezeich = REPLACE(bezeich, CHR(13),"")
           bemerk  = REPLACE(bemerk, CHR(10),"")
           bemerk  = REPLACE(bemerk, CHR(13),"")
           bemerk  = REPLACE(bemerk, "|","")
           counter          = counter + 1
           .

    RUN add-html(bezeich,OUTPUT bezeich).
    RUN clean-html(bezeich,OUTPUT bezeich).

    RUN add-html(bemerk,OUTPUT bemerk).
    RUN clean-html(bemerk,OUTPUT bemerk).
    
    RUN add-html(bemerk1,OUTPUT bemerk1).
    RUN clean-html(bemerk1,OUTPUT bemerk1).

    CREATE queasy.
    ASSIGN queasy.KEY   = 280
           queasy.char1 = "Inhouse List"
           queasy.number2 = INT(idFlag)
           queasy.char3 = STRING(bezeich)                                + "|" +
                          STRING(bemerk)                                 + "|" +
                          STRING(bemerk1)                                  
           queasy.char2 = STRING(inhouse-guest-list.flag)        + "|" +  /*1*/
                          STRING(inhouse-guest-list.karteityp)   + "|" +  /*2*/
                          STRING(inhouse-guest-list.nr)          + "|" +  /*3*/
                          inhouse-guest-list.vip                 + "|" +  /*4*/
                          STRING(inhouse-guest-list.resnr)       + "|" +  /*5*/
                          inhouse-guest-list.firstname           + "|" +  /*6*/
                          inhouse-guest-list.lastname            + "|" +  /*7*/
                          inhouse-guest-list.birthdate           + "|" +  /*8*/
                          inhouse-guest-list.groupname           + "|" +  /*9*/
                          inhouse-guest-list.rmno                + "|" +  /*10*/
                          STRING(inhouse-guest-list.qty)         + "|" +  /*11*/
                          STRING(inhouse-guest-list.arrive)      + "|" +  /*12*/
                          STRING(inhouse-guest-list.depart)      + "|" +  /*13*/
                          inhouse-guest-list.rmcat               + "|" +  /*14*/
                          inhouse-guest-list.ratecode            + "|" +  /*15*/
                          STRING(inhouse-guest-list.zipreis)     + "|" +  /*16*/
                          inhouse-guest-list.kurzbez             + "|" +  /*17*/
                          STRING(inhouse-guest-list.a)           + "|" +  /*18*/
                          STRING(inhouse-guest-list.c)           + "|" +  /*19*/
                          STRING(inhouse-guest-list.co)          + "|" +  /*20*/
                          inhouse-guest-list.pax                 + "|" +  /*21*/
                          inhouse-guest-list.nat                 + "|" +  /*22*/
                          inhouse-guest-list.nation              + "|" +  /*23*/
                          inhouse-guest-list.argt                + "|" +  /*24*/
                          inhouse-guest-list.company             + "|" +  /*25*/
                          inhouse-guest-list.flight              + "|" +  /*26*/
                          inhouse-guest-list.etd                 + "|" +  /*27*/
                          STRING(inhouse-guest-list.paym)        + "|" +  /*28*/
                          inhouse-guest-list.segm                + "|" +  /*29*/
                          inhouse-guest-list.telefon             + "|" +  /*30*/
                          inhouse-guest-list.mobil-tel           + "|" +  /*31*/
                          STRING(inhouse-guest-list.created)     + "|" +  /*32*/
                          inhouse-guest-list.createid            + "|" +  /*33 (Malik serverless : inhouse-guest-list.createID -> inhouse-guest-list.createid) */ 
                          inhouse-guest-list.ci-time             + "|" +  /*34*/
                          inhouse-guest-list.curr                + "|" +  /*35*/
                          STRING(inhouse-guest-list.inhousedate) + "|" +  /*36*/
                          inhouse-guest-list.sob                 + "|" +  /*37*/
                          STRING(inhouse-guest-list.gastnr)      + "|" +  /*38*/
                          STRING(inhouse-guest-list.lodging)     + "|" +  /*39*/
                          STRING(inhouse-guest-list.breakfast)   + "|" +  /*40*/
                          STRING(inhouse-guest-list.lunch)       + "|" +  /*41*/
                          STRING(inhouse-guest-list.dinner)      + "|" +  /*42*/
                          STRING(inhouse-guest-list.otherev)     + "|" +  /*43*/
                          STRING(inhouse-guest-list.rechnr)      + "|" +  /*44*/
                          inhouse-guest-list.memberno            + "|" +  /*45*/
                          inhouse-guest-list.membertype          + "|" +  /*46*/
                          inhouse-guest-list.email               + "|" +  /*47*/
                          inhouse-guest-list.localreg            + "|" +  /*48*/
                          inhouse-guest-list.c-zipreis           + "|" +  /*49*/
                          inhouse-guest-list.c-lodging           + "|" +  /*50*/
                          inhouse-guest-list.c-breakfast         + "|" +  /*51*/
                          inhouse-guest-list.c-lunch             + "|" +  /*52*/
                          inhouse-guest-list.c-dinner            + "|" +  /*53*/
                          inhouse-guest-list.c-otherev           + "|" +  /*54*/
                          inhouse-guest-list.c-a                 + "|" +  /*55*/
                          inhouse-guest-list.c-c                 + "|" +  /*56*/
                          inhouse-guest-list.c-co                + "|" +  /*57*/
                          inhouse-guest-list.c-rechnr            + "|" +  /*58*/
                          inhouse-guest-list.c-resnr             + "|" +  /*59*/
                          inhouse-guest-list.night               + "|" +  /*60*/
                          inhouse-guest-list.city                + "|" +  /*61*/
                          inhouse-guest-list.keycard             + "|" +  /*62*/
                          inhouse-guest-list.co-time             + "|" +  /*63*/
                          inhouse-guest-list.pay-art             + "|" +  /*64*/
                          STRING(inhouse-guest-list.etage)       + "|" +  /*65*/
                          inhouse-guest-list.zinr-bez            + "|" +  /*66*/
                          STRING(inhouse-guest-list.flag-guest)           /*67*/
            queasy.number1 = counter.
    FIND NEXT inhouse-guest-list NO-ERROR.
END.
*/

FIND FIRST queasy WHERE queasy.KEY = 280
    AND queasy.char1 = "Inhouse List Sum" 
    AND queasy.number2 = INT(idFlag) NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN DO:
    FOR EACH summary-roomtype NO-LOCK:  
        /* Malik Serverless for case 258 */
        IF summary-roomtype.rmcat NE ? THEN 
        DO:
            tmp-rmcat = summary-roomtype.rmcat.
        END.
        ELSE
        DO:
            tmp-rmcat = "".
        END.
        IF summary-roomtype.bezeich NE ? THEN 
        DO:
            tmp-bezeich = summary-roomtype.bezeich.
        END.
        ELSE
        DO:
            tmp-bezeich = "".
        END.
        /* END Malik */
        
        /*bernatd CE55BE*/
        IF tmp-rmcat MATCHES "*|*" THEN tmp-rmcat   = REPLACE(tmp-rmcat  ,"|"," ").
        ELSE tmp-rmcat   = tmp-rmcat.
        IF tmp-bezeich MATCHES "*|*" THEN tmp-bezeich = REPLACE(tmp-bezeich,"|"," ").
        ELSE tmp-bezeich = tmp-bezeich.
        /*end bernatd*/
        
        ct = ct + 1.
        CREATE queasy.
        ASSIGN queasy.KEY       = 280
               queasy.char1     = "Inhouse List Sum"
               queasy.number1   = ct  
               queasy.number2   = INT(idFlag)
               queasy.char3     = "roomtype"  
               queasy.char2     = tmp-rmcat                                 + "|" +    /* malik serverless cse 258 : summary-roomtype.rmcat -> tmp-rmcat */ 
               tmp-bezeich                               + "|" +    /*1*/  
                                  STRING(summary-roomtype.anz)              + "|" +    /*2*/  
                                  STRING(summary-roomtype.proz-qty)         + "|" +    /*3*/  
                                  STRING(summary-roomtype.rev)              + "|" +    /*4*/  
                                  STRING(summary-roomtype.proz-rev)         + "|" +    /*5*/  
                                  STRING(summary-roomtype.arr)              .          /*6*/                                
            
    END.     

    ct = 0.
    FOR EACH summary-nation NO-LOCK:
        /* Malik Serverless for case 258 */
        IF summary-nation.nat NE ? THEN
        DO:
            tmp-nat = summary-nation.nat.
        END.
        ELSE
        DO:
            tmp-nat = "".
        END.

        IF summary-nation.adult NE ? THEN
        DO:
            tmp-adult = summary-nation.adult.
        END.
        ELSE
        DO:
            tmp-adult = "".
        END.

        IF summary-nation.proz NE ? THEN
        DO:
            tmp-proz = summary-nation.proz.
        END.
        ELSE
        DO:
            tmp-proz = "".
        END.

        IF summary-nation.child NE ? THEN
        DO:
            tmp-child = summary-nation.child.
        END.
        ELSE
        DO:
            tmp-child = "".
        END.
        /* END Malik */

        /*start bernatd*/
        IF tmp-nat MATCHES "*|*" THEN tmp-nat = REPLACE(tmp-nat,"|","&").
        ELSE tmp-nat = tmp-nat.
        IF tmp-adult MATCHES "*|*" THEN tmp-adult = REPLACE(tmp-adult,"|","&").
        ELSE tmp-adult = tmp-adult.
        IF tmp-proz MATCHES "*|*" THEN tmp-proz = REPLACE(tmp-proz,"|","&").
        ELSE tmp-proz = tmp-proz.
        IF tmp-child MATCHES "*|*" THEN tmp-child = REPLACE(tmp-child,"|","&").
        ELSE tmp-child = tmp-child.
        /*end bernatd*/

        ct = ct + 1.
        CREATE queasy.
        ASSIGN queasy.KEY       = 280
               queasy.char1     = "Inhouse List Sum"
               queasy.number1   = ct  
               queasy.number2   = INT(idFlag)
               queasy.char3     = "nation"
               queasy.char2     = tmp-nat           + "|" + /* Malik serverless 258 : summary-nation.nat -> tmp-nat */
                                  tmp-adult         + "|" +
                                  tmp-proz          + "|" +
                                  tmp-child         . 
    END.

    ct = 0.
    FOR EACH summary-revenue NO-LOCK:
        ct = ct + 1.

        IF summary-revenue.currency MATCHES "*|*" THEN tmp-currency = REPLACE(summary-revenue.currency,"|"," ").
        ELSE tmp-currency = summary-revenue.currency.

        CREATE queasy.
        ASSIGN queasy.KEY       = 280
               queasy.char1     = "Inhouse List Sum"
               queasy.number1   = ct  
               queasy.number2   = INT(idFlag)
               queasy.char3     = "revenue"
               queasy.char2     =  summary-revenue.currency             + "|" +    
                                   STRING(summary-revenue.room-rate)    + "|" + 
                                   STRING(summary-revenue.lodging)      + "|" + 
                                   STRING(summary-revenue.b-amount)     + "|" + 
                                   STRING(summary-revenue.l-amount)     + "|" + 
                                   STRING(summary-revenue.d-amount)     + "|" + 
                                   STRING(summary-revenue.o-amount).
    END.                                               
    
    ct = 0.
    FOR EACH summary-segment NO-LOCK:
        ct = ct + 1.

        IF summary-segment.segment MATCHES "*|*" THEN tmp-segment = REPLACE(summary-segment.segment,"|"," ").
        ELSE tmp-segment = summary-segment.segment.

        CREATE queasy.
        ASSIGN queasy.KEY       = 280
               queasy.char1     = "Inhouse List Sum"
               queasy.number1   = ct  
               queasy.number2   = INT(idFlag)
               queasy.char3     = "segment"
               queasy.char2     = STRING(summary-segment.segmcode)          + "|" +
                                  summary-segment.segment                   + "|" +
                                  STRING(summary-segment.anzahl)            + "|" +
                                  STRING(summary-segment.proz-qty)          + "|" +
                                  STRING(summary-segment.rev)               + "|" +
                                  STRING(summary-segment.proz-rev)          + "|" +
                                  STRING(summary-segment.arr)               . 
    END.

    ct = 0.
    FOR EACH summary-list4 NO-LOCK:
        ct = ct + 1.
        CREATE queasy.
        ASSIGN queasy.KEY       = 280
               queasy.char1     = "Inhouse List Sum"
               queasy.number1   = ct   
               queasy.number2   = INT(idFlag)    
               queasy.char3     = "summary-list4"
               queasy.char2     = summary-list4.argt                   + "|" +
                                  STRING(summary-list4.rm-qty)         + "|" +
                                  STRING(summary-list4.pax).
    END.

    ct = 0.
    FOR EACH sum-list NO-LOCK:
        ct = ct + 1.

        IF sum-list.curr MATCHES "*|*" THEN tmp-sum-curr = REPLACE(sum-list.curr,"|"," ").
        ELSE tmp-sum-curr = sum-list.curr.

        CREATE queasy.
        ASSIGN queasy.KEY       = 280
               queasy.char1     = "Inhouse List Sum"
               queasy.number1   = ct  
               queasy.number2   = INT(idFlag)
               queasy.char3     = "summary"
               queasy.char2     = sum-list.curr                     + "|" +
                                  STRING(sum-list.zipreis)          + "|" +
                                  STRING(sum-list.lodging)          + "|" +
                                  STRING(sum-list.bfast)            + "|" +
                                  STRING(sum-list.lunch)            + "|" +
                                  STRING(sum-list.dinner)           + "|" + 
                                  STRING(sum-list.other).  
    END.                                                   
    
    /*
    ct = ct + 1.
    CREATE queasy.
    ASSIGN queasy.KEY       = 280
           queasy.char1     = "Inhouse List Sum"
           queasy.number1   = ct  
           queasy.number2   = INT(idFlag)
           queasy.char3     = "total"
           queasy.char2     = STRING(tot-payrm)             + "|" +
                              STRING(tot-rm)                + "|" +
                              STRING(tot-a)                 + "|" +
                              STRING(tot-c)                 + "|" +
                              STRING(tot-co)                + "|" +
                              STRING(tot-avail)             + "|" + 
                              STRING(inactive)              + "|" +
                              STRING(tot-keycard).*/

END.

FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "Inhouse List"
    AND bqueasy.number2 = INT(idFlag) NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.

FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "Inhouse List Sum"
    AND bqueasy.number2 = INT(idFlag) NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
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

PROCEDURE add-html:
    DEFINE INPUT  PARAMETER pcString  AS CHARACTER   NO-UNDO.
    DEFINE OUTPUT PARAMETER pcCleaned AS CHARACTER   NO-UNDO.

    DEFINE VARIABLE iHtmlTagBegins AS INTEGER     NO-UNDO.
    DEFINE VARIABLE iHtmlTagEnds   AS INTEGER     NO-UNDO.
    DEFINE VARIABLE lHtmlTagActive AS LOGICAL     NO-UNDO.

    DEFINE VARIABLE i AS INTEGER     NO-UNDO.

    DO i = 1 TO LENGTH(pcString):
        IF lHtmlTagActive = FALSE AND SUBSTRING(pcString, i, 1) = ">" THEN DO:
            iHtmlTagBegins = i.
            lHtmlTagActive = TRUE.
        END.

        IF lHtmlTagActive AND SUBSTRING(pcString, i, 1) = "<" THEN DO:
            iHtmlTagEnds = i.
            lHtmlTagActive = FALSE.

            SUBSTRING(pcString, i,1) = " " + SUBSTRING(pcString, i,1).
       END.
    END.
    pcCleaned = pcString.
END PROCEDURE.

PROCEDURE clean-html:
    DEFINE INPUT  PARAMETER pcString  AS CHARACTER   NO-UNDO.
    DEFINE OUTPUT PARAMETER pcCleaned AS CHARACTER   NO-UNDO.

    DEFINE VARIABLE iHtmlTagBegins AS INTEGER     NO-UNDO.
    DEFINE VARIABLE iHtmlTagEnds   AS INTEGER     NO-UNDO.
    DEFINE VARIABLE lHtmlTagActive AS LOGICAL     NO-UNDO.

    DEFINE VARIABLE i AS INTEGER     NO-UNDO.

    DO i = 1 TO LENGTH(pcString):
        IF lHtmlTagActive = FALSE AND SUBSTRING(pcString, i, 1) = "<" THEN DO:
            iHtmlTagBegins = i.
            lHtmlTagActive = TRUE.
        END.

        IF lHtmlTagActive AND SUBSTRING(pcString, i, 1) = ">" THEN DO:
            iHtmlTagEnds = i.
            lHtmlTagActive = FALSE.

            SUBSTRING(pcString, iHtmlTagBegins, iHtmlTagEnds - iHtmlTagBegins + 1) = FILL("|", iHtmlTagEnds - iHtmlTagBegins).
        END.
    END.

    pcCleaned = REPLACE(pcString, "|", "").

END PROCEDURE.
