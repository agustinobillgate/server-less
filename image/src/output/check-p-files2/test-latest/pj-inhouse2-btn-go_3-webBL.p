DEFINE TEMP-TABLE cl-list 
    FIELD flag        AS INTEGER 
    FIELD karteityp   AS INTEGER 
    FIELD nr          AS INTEGER FORMAT ">>9" 
    FIELD vip         AS CHAR FORMAT "x(5)" 
    FIELD resnr       AS INTEGER FORMAT ">>>>>9" 
    FIELD name        AS CHAR FORMAT "x(24)" 
    FIELD groupname   AS CHAR FORMAT "x(24)" 
    FIELD rmno        AS CHAR FORMAT "x(7)"		/*MT 25/07/12 */
    FIELD qty         AS INTEGER FORMAT ">>9" 
    FIELD arrive      AS DATE 
    FIELD depart      AS DATE 
    FIELD rmcat       AS CHAR FORMAT "x(6)" 
    FIELD ratecode    AS CHAR FORMAT "x(18)"  /* "x(6)" Gerald 270720*/
    FIELD zipreis     AS DECIMAL 
    FIELD kurzbez     AS CHAR 
    FIELD bezeich     AS CHAR 
    FIELD a           AS INTEGER FORMAT "9" 
    FIELD c           AS INTEGER FORMAT "9" 
    FIELD co          AS INTEGER FORMAT ">9" 
    FIELD pax         AS CHAR FORMAT "x(6)" 
    FIELD nat         AS CHAR FORMAT "x(3)" 
    FIELD nation      AS CHAR 
    FIELD argt        AS CHAR FORMAT "x(6)" 
    FIELD company     AS CHAR FORMAT "x(18)" 
    FIELD flight      AS CHAR FORMAT "x(6)" 
    FIELD etd         AS CHAR FORMAT "99:99" 
    FIELD paym        AS INTEGER FORMAT ">>9" 
    FIELD segm        AS CHAR FORMAT "x(12)"
    FIELD telefon     AS CHAR FORMAT "x(24)" /*SIS 31/01/13 */
    FIELD mobil-tel   AS CHAR FORMAT "x(24)" /*SIS 31/01/13 */
    FIELD created     AS DATE FORMAT "99/99/99"
    FIELD createID    AS CHAR FORMAT "x(4)"
    FIELD bemerk      AS CHAR FORMAT "x(16)"
    FIELD bemerk01    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
    FIELD bemerk02    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
    FIELD bemerk03    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
    FIELD bemerk04    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
    FIELD bemerk05    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
    FIELD bemerk06    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
    FIELD bemerk07    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
    FIELD bemerk08    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
    FIELD bemerk1     AS CHAR FORMAT "x(32)" /*IT 200612 add incl-rsvcomment*/
    FIELD ci-time     AS CHAR
    FIELD curr        AS CHAR FORMAT "x(4)"
    FIELD spreq       AS CHAR FORMAT "x(20)"
    FIELD tot-bfast   AS INTEGER
    FIELD local-reg   AS CHARACTER
    FIELD rsv-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/    
    FIELD other-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
    FIELD g-comment   AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
    FIELD zinr-bez    AS CHAR     /*Gerald 7E2311*/
    FIELD flag-guest  AS INTEGER  /*Gerald 7E2311*/
    FIELD etage       AS INTEGER /*FDL April 24, 2023 => 7958BA*/
    FIELD birthdate   AS DATE /*MCH Dec 20, 2024 => 5BB5DC Req Royal Santrian*/
.

DEFINE TEMP-TABLE s-list 
    FIELD rmcat       AS CHAR FORMAT "x(6)" 
    FIELD bezeich     AS CHAR FORMAT "x(24)" 
    FIELD nat         AS CHAR FORMAT "x(24)" 
    FIELD anz         AS INTEGER FORMAT ">>9" 
    FIELD adult       AS INTEGER FORMAT ">>9" 
    FIELD proz        AS DECIMAL FORMAT ">>9.99" 
    FIELD child       AS INTEGER FORMAT ">>9"
    FIELD rmqty       AS INTEGER  FORMAT ">>9"   /*FD Jan 06, 2019*/
.

DEFINE TEMP-TABLE segm-list
    FIELD segmcode AS INTEGER
    FIELD segment  AS CHAR 
    FIELD anzahl   AS INTEGER
.

DEFINE TEMP-TABLE argt-list
    FIELD argt          AS CHAR
    FIELD tot-room      AS INTEGER
    FIELD tot-pax       AS INTEGER
    FIELD tot-breakfast AS INTEGER
.

DEFINE TEMP-TABLE sum-list
    FIELD curr AS CHAR FORMAT "x(4)"
    FIELD zipreis AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
.

DEFINE TEMP-TABLE t-buff-queasy LIKE queasy.

DEFINE TEMP-TABLE output-list 
    FIELD flag        AS INTEGER 
    FIELD karteityp   AS INTEGER 
    FIELD nr          AS INTEGER FORMAT ">>9" 
    FIELD vip         AS CHAR FORMAT "x(5)" 
    FIELD resnr       AS INTEGER FORMAT ">>>>>9" 
    FIELD name        AS CHAR FORMAT "x(24)" 
    FIELD groupname   AS CHAR FORMAT "x(24)" 
    FIELD rmno        AS CHAR FORMAT "x(7)"		/*MT 25/07/12 */
    FIELD qty         AS INTEGER FORMAT ">>9" 
    FIELD arrive      AS DATE 
    FIELD depart      AS DATE 
    FIELD rmcat       AS CHAR FORMAT "x(6)" 
    FIELD ratecode    AS CHAR FORMAT "x(18)"  /* "x(6)" Gerald 270720*/
    FIELD zipreis     AS DECIMAL 
    FIELD kurzbez     AS CHAR 
    FIELD bezeich     AS CHAR 
    FIELD a           AS INTEGER FORMAT "9" 
    FIELD c           AS INTEGER FORMAT "9" 
    FIELD co          AS INTEGER FORMAT ">9" 
    FIELD pax         AS CHAR FORMAT "x(6)" 
    FIELD nat         AS CHAR FORMAT "x(3)" 
    FIELD nation      AS CHAR 
    FIELD argt        AS CHAR FORMAT "x(6)" 
    FIELD company     AS CHAR FORMAT "x(18)" 
    FIELD flight      AS CHAR FORMAT "x(6)" 
    FIELD etd         AS CHAR FORMAT "99:99" 
    FIELD paym        AS INTEGER FORMAT ">>9" 
    FIELD segm        AS CHAR FORMAT "x(12)"
    FIELD telefon     AS CHAR FORMAT "x(24)" /*SIS 31/01/13 */
    FIELD mobil-tel   AS CHAR FORMAT "x(24)" /*SIS 31/01/13 */
    FIELD created     AS DATE FORMAT "99/99/99"
    FIELD createID    AS CHAR FORMAT "x(4)"
    FIELD bemerk      AS CHAR FORMAT "x(16)"
    FIELD bemerk01    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
    FIELD bemerk02    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
    FIELD bemerk03    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
    FIELD bemerk04    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
    FIELD bemerk05    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
    FIELD bemerk06    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
    FIELD bemerk07    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
    FIELD bemerk08    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
    FIELD bemerk1     AS CHAR FORMAT "x(32)" /*IT 200612 add incl-rsvcomment*/
    FIELD ci-time     AS CHAR
    FIELD curr        AS CHAR FORMAT "x(4)"
    FIELD spreq       AS CHAR FORMAT "x(20)"
    FIELD tot-bfast   AS INTEGER
    FIELD local-reg   AS CHARACTER
    FIELD memberno    AS CHAR FORMAT "x(25)"                        
    FIELD membertype  AS CHAR FORMAT "x(25)"       
    FIELD email       AS CHAR FORMAT "x(35)" 
    FIELD ac          AS CHAR FORMAT "x(4)"
    FIELD stay        AS INTEGER /*FD September 08, 2020*/
    FIELD rsv-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/    
    FIELD other-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
    FIELD g-comment   AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
    FIELD zinr-bez    AS CHAR     /*Gerald 7E2311*/
    FIELD flag-guest  AS INTEGER  /*Gerald 7E2311*/
    FIELD etage       AS INTEGER /*FDL April 24, 2023 => 7958BA*/
    FIELD birthdate   AS DATE /*MCH Dec 20, 2024 => 5BB5DC Req Royal Santrian*/
.

DEFINE TEMP-TABLE lnl-sum
  FIELD counter     AS INTEGER
  FIELD summ        AS CHARACTER
  FIELD rm-type     AS CHARACTER
  FIELD qty         AS CHARACTER
  FIELD nation      AS CHARACTER
  FIELD rm-qty      AS CHARACTER
  FIELD adult       AS CHARACTER
  FIELD percent     AS CHARACTER
  FIELD child       AS CHARACTER
.

DEFINE TEMP-TABLE summary-list1
    FIELD summ          AS CHARACTER
    FIELD room-type     AS CHARACTER
    FIELD qty           AS CHARACTER
    FIELD nation        AS CHARACTER
    FIELD rm-qty        AS CHARACTER
    FIELD adult         AS CHARACTER
    FIELD percent       AS CHARACTER
    FIELD child         AS CHARACTER
.

DEFINE TEMP-TABLE summary-list2
    FIELD summ          AS CHARACTER
    FIELD curr          AS CHARACTER
    FIELD room-rate     AS CHARACTER
.

DEFINE TEMP-TABLE summary-list3
    FIELD summ          AS CHARACTER
    FIELD segm-code     AS CHARACTER
    FIELD rm-qty        AS CHARACTER
.

DEFINE TEMP-TABLE summary-list4
    FIELD summ          AS CHARACTER
    FIELD argt          AS CHARACTER
    FIELD rm-qty        AS CHARACTER
    FIELD pax           AS CHARACTER
    FIELD bfast         AS CHARACTER    
.

DEF INPUT PARAMETER sorttype        AS INT.
DEF INPUT PARAMETER datum           AS DATE.
DEF INPUT PARAMETER curr-date       AS DATE.
DEF INPUT PARAMETER curr-gastnr     AS INT.
DEF INPUT PARAMETER froom           AS CHAR.
DEF INPUT PARAMETER troom           AS CHAR.
DEF INPUT PARAMETER exc-depart      AS LOGICAL.
DEF INPUT PARAMETER incl-gcomment   AS LOGICAL.
DEF INPUT PARAMETER incl-rsvcomment AS LOGICAL.
DEF INPUT PARAMETER prog-name       AS CHAR.
DEF INPUT PARAMETER disp-accompany  AS LOGICAL.
DEF INPUT PARAMETER disp-exclinact  AS LOGICAL.
DEF INPUT PARAMETER split-rsv-print AS LOGICAL. /*FDL August 28, 2023 => Req Kayu Manis Group*/
DEF OUTPUT PARAMETER TABLE FOR output-list.
DEF OUTPUT PARAMETER TABLE FOR summary-list1.
DEF OUTPUT PARAMETER TABLE FOR summary-list2.
DEF OUTPUT PARAMETER TABLE FOR summary-list3.
DEF OUTPUT PARAMETER TABLE FOR summary-list4.
DEF OUTPUT PARAMETER TABLE FOR lnl-sum.
DEF OUTPUT PARAMETER TABLE FOR t-buff-queasy.
/* For Testing Output Data
DEF VARIABLE sorttype        AS INT.
DEF VARIABLE datum           AS DATE.
DEF VARIABLE curr-date       AS DATE.
DEF VARIABLE curr-gastnr     AS INT.
DEF VARIABLE froom           LIKE zimmer.zinr.
DEF VARIABLE troom           LIKE zimmer.zinr.
DEF VARIABLE exc-depart      AS LOGICAL.
DEF VARIABLE incl-gcomment   AS LOGICAL.
DEF VARIABLE incl-rsvcomment AS LOGICAL.
DEF VARIABLE prog-name       AS CHAR.
DEF VARIABLE disp-accompany  AS LOGICAL.
DEF VARIABLE disp-exclinact  AS LOGICAL.

ASSIGN
    sorttype        = 1
    datum           = 01/14/19
    curr-date       = 01/14/19
    curr-gastnr     = 0
    froom           = ""
    troom           = "zz"
    exc-depart      = NO
    incl-gcomment   = NO
    incl-rsvcomment = NO
    prog-name       = ""
    disp-accompany  = NO
    disp-exclinact  = NO.
*/
DEFINE VARIABLE tot-payrm      AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-rm         AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-a          AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-c          AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-co         AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-avail      AS INTEGER INITIAL 0.
DEFINE VARIABLE tot-rmqty      AS INTEGER INITIAL 0.   /*FD Jan 06, 2019*/
DEFINE VARIABLE inactive       AS INTEGER INITIAL 0. 

DEFINE VARIABLE curr-company    AS CHAR INIT "" NO-UNDO.
DEFINE VARIABLE outnr           AS INTEGER.

DEFINE VARIABLE qh AS HANDLE.
DEFINE VARIABLE query-string AS CHAR.

RUN create-inhouse-v2.

/******************************************************************************************************/

PROCEDURE create-inhouse-v2:
    DEFINE VARIABLE prog-name AS CHAR NO-UNDO.
    prog-name = "PJ-inhouse2".
    RUN pj-inhouse2-btn-go_3-cldbl.p 
        (sorttype, datum, curr-date, curr-gastnr, froom, troom, exc-depart,
         incl-gcomment, incl-rsvcomment, prog-name, disp-accompany, disp-exclinact,
         split-rsv-print,
         OUTPUT tot-payrm, OUTPUT tot-rm, OUTPUT tot-a, OUTPUT tot-c,
         OUTPUT tot-co, OUTPUT tot-avail, OUTPUT tot-rmqty, OUTPUT inactive,
         OUTPUT TABLE cl-list, OUTPUT TABLE s-list, OUTPUT TABLE t-buff-queasy).
    
    DEFINE BUFFER c-list FOR cl-list.
    
    FOR EACH output-list:
        DELETE output-list.
    END.
    
    FOR EACH sum-list:
        DELETE sum-list.
    END.
    
    FOR EACH segm-list:
        DELETE segm-list.
    END.
    
    FOR EACH argt-list:
        DELETE argt-list.
    END.
    
    FOR EACH summary-list1:
        DELETE summary-list1.
    END.

    FOR EACH summary-list2:
        DELETE summary-list2.
    END.

    FOR EACH summary-list3:
        DELETE summary-list3.
    END.

    FOR EACH summary-list4:
        DELETE summary-list4.
    END.

    FOR EACH lnl-sum:
        DELETE lnl-sum.
    END.

    IF sorttype EQ 1 OR sorttype EQ 3 THEN
    DO:
        outnr = 0.

        /* IF sorttype EQ 1 THEN query-string = "FOR EACH cl-list.".
        ELSE IF sorttype EQ 3 THEN query-string = "FOR EACH cl-list BY cl-list.etage BY cl-list.rmno.".

        CREATE QUERY qh.
        qh:SET-BUFFERS(BUFFER cl-list:handle).
        qh:QUERY-PREPARE(query-string).
        qh:QUERY-OPEN.

        Comment FDL 15 Nov, 2023
        FOR EACH cl-list:
       
        /*FDL 15 Nov, 2023 => Ticket 287722 - changed to dynamic query with query handle*/
        REPEAT:
            qh:GET-NEXT().
            IF NOT AVAILABLE cl-list THEN LEAVE.

            
        END.

        qh:QUERY-CLOSE().
        DELETE OBJECT qh. FT serverless*/
        IF sorttype = 1 THEN
            FOR EACH cl-list:
                RUN create-outList.
            END.
        ELSE IF sorttype = 3 THEN
            FOR EACH cl-list BY cl-list.etage BY cl-list.rmno:
                RUN create-outList.
            END.
    END.
    ELSE 
    DO:
        FOR EACH cl-list BY cl-list.company:
            IF curr-company NE cl-list.company THEN
            DO:
                curr-company = cl-list.company.
                CREATE output-list.
                output-list.rmno = "".
    
                CREATE output-list.
                ASSIGN 
                    output-list.rmno = ""
                    output-list.NAME = CAPS(cl-list.company).            
    
                outnr = 0.
                FOR EACH c-list WHERE c-list.company EQ curr-company:
                    outnr = outnr + 1.
                    CREATE output-list.
                    BUFFER-COPY c-list TO output-list.
                    output-list.nr   = outnr.
    
                    IF NUM-ENTRIES(c-list.telefon,";") GT 1 THEN
                    DO:
                        output-list.memberno = TRIM(STRING(ENTRY(2,c-list.telefon,";"),"x(25)")).                    
                        output-list.telefon  = TRIM(ENTRY(1,c-list.telefon,";")).
                    END.
                                        
                    IF NUM-ENTRIES(c-list.mobil-tel,";") GT 1 THEN
                    DO:
                        output-list.membertype = TRIM(STRING(ENTRY(2,c-list.mobil-tel,";"),"x(26)")).                    
                        output-list.mobil-tel  = TRIM(ENTRY(1,c-list.mobil-tel,";")).
                    END.                    
                        
                    IF NUM-ENTRIES(c-list.curr,";") GT 1 THEN
                    DO: 
                        output-list.email = STRING(ENTRY(2,c-list.curr,";"),"x(40)").                    
                    END.
                    
                    output-list.ac = STRING(c-list.a) + "/" + string(c-list.c).                
                END.
            END.
            FIND FIRST sum-list WHERE sum-list.curr = ENTRY(1,cl-list.curr,";") NO-ERROR.
            IF NOT AVAILABLE sum-list THEN
            DO:
                CREATE sum-list.
                ASSIGN sum-list.curr = ENTRY(1,cl-list.curr,";").
            END.
            ASSIGN sum-list.zipreis = sum-list.zipreis + cl-list.zipreis. 
    
            FIND FIRST segm-list WHERE segm-list.segmcode = cl-list.paym NO-ERROR.
            IF NOT AVAILABLE segm-list THEN
            DO: 
                CREATE segm-list.
                ASSIGN segm-list.segmcode = cl-list.paym
                segm-list.segment = cl-list.segm.
            END.
            ASSIGN segm-list.anzahl = segm-list.anzahl + cl-list.qty.
    
            FIND FIRST argt-list WHERE argt-list.argt = cl-list.argt NO-ERROR.
            IF NOT AVAILABLE argt-list THEN DO:
                CREATE argt-list.
                ASSIGN argt-list.argt = cl-list.argt.
            END.
            ASSIGN 
                argt-list.tot-room      = argt-list.tot-room + 1
                argt-list.tot-pax       = argt-list.tot-pax + cl-list.a
                argt-list.tot-breakfast = argt-list.tot-breakfast + cl-list.tot-bfast.
    
            output-list.stay = cl-list.depart - cl-list.arrive.
        END.
    END.
        
    FOR EACH s-list:            /*Summary 1*/
        CREATE summary-list1.
        ASSIGN 
            summary-list1.summ      = ""
            summary-list1.room-type = s-list.bezeich
            summary-list1.qty       = STRING(s-list.anz,">>>>>")
            summary-list1.nation    = TRIM(s-list.nat)
            summary-list1.rm-qty    = STRING(s-list.rmqty, ">>>>9")
            summary-list1.adult     = STRING(s-list.adult, ">>>>9")       
            summary-list1.percent   = STRING(s-list.proz,  ">>9.99")        
            summary-list1.child     = STRING(s-list.child, ">>>>9")
        .
    END. 

    CREATE summary-list1. /*Break Line*/
       
    CREATE summary-list1.
    ASSIGN 
        summary-list1.summ        = ""
        summary-list1.room-type   = "ROOM AVAILABLE"                                 
        summary-list1.qty         = STRING(tot-avail,">>>>9"). 

    IF inactive NE 0 THEN 
    DO: 
        CREATE summary-list1.
        ASSIGN 
            summary-list1.summ       = ""
            summary-list1.room-type  = "OCCUPIED/INACTIVE"
            summary-list1.qty        = STRING(tot-rm,">>>>9") + "/" + STRING(inactive)
            summary-list1.nation     = ""
            summary-list1.rm-qty     = STRING(tot-rmqty, ">>>>9")
            summary-list1.adult      = STRING(tot-a + tot-co, ">>>>9")
            summary-list1.percent    = "100.00"
            summary-list1.child      = STRING(tot-c,">>>>9")
        .
    END.
    ELSE
    DO:
        CREATE summary-list1.
        ASSIGN            
            summary-list1.summ       = ""
            summary-list1.room-type  = "T O T A L  OCCUPIED"
            summary-list1.qty        = STRING(tot-rm,">>>>9")
            summary-list1.nation     = ""
            summary-list1.rm-qty     = STRING(tot-rmqty, ">>>>9")
            summary-list1.adult      = STRING(tot-a + tot-co, ">>>>9")
            summary-list1.percent    = "100.00"
            summary-list1.child      = STRING(tot-c,">>>>9")
        .
    END.

    CREATE summary-list1.
    ASSIGN 
        summary-list1.summ      = ""
        summary-list1.room-type = "IN PERCENTAGE (%)"
        summary-list1.qty       = STRING(tot-rm / tot-avail * 100,">>9.99")
        summary-list1.nation    = "AVRG GUEST/ROOM"
        summary-list1.rm-qty    = STRING((tot-a + tot-co) / tot-rm, ">>9.99")
    .

    CREATE summary-list1.
    ASSIGN 
        summary-list1.summ      = ""
        summary-list1.room-type = "OCC. PAYING ROOMS"
        summary-list1.qty       = STRING(tot-payrm / tot-avail * 100,">>9.99") + " %".                                                                        
                                                                           
    
    FOR EACH sum-list:
        CREATE summary-list2.
        ASSIGN 
            summary-list2.summ   = ""
            summary-list2.curr   = STRING(sum-list.curr, "x(15)") 
            summary-list2.room-rate = STRING(sum-list.zipreis, "->,>>>,>>>,>>9.99")
        .
    END.
        
    FOR EACH segm-list:
        CREATE summary-list3.
        ASSIGN 
            summary-list3.summ        = ""
            summary-list3.segm-code   = segm-list.segment
            summary-list3.rm-qty      = STRING(segm-list.anzahl, ">>>>9")
            .
    END.
    
    FOR EACH argt-list:
        CREATE summary-list4.
        ASSIGN 
            summary-list4.summ      = ""
            summary-list4.argt      = STRING(argt-list.argt, "x(15)") 
            summary-list4.rm-qty    = STRING(argt-list.tot-room, ">>>>>9") 
            summary-list4.pax       = STRING(argt-list.tot-pax, ">>>>>9") 
            summary-list4.bfast     = STRING(argt-list.tot-breakfast, ">>>>9").
    END.    

    /*FD April 07, 2021 => for LnL
    FOR EACH lnl-sum:
        DELETE lnl-sum.
    END.

    counter = 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.summ    = "SUMM"
        lnl-sum.rm-type = "ROOM TYPE"
        lnl-sum.qty     = "QTY"          
    .

    FOR EACH s-list WHERE s-list.bezeich NE "":
        counter = counter + 1.

        CREATE lnl-sum.
        ASSIGN
            lnl-sum.counter = counter
            lnl-sum.summ    = ""
            lnl-sum.rm-type = s-list.bezeich
            lnl-sum.qty     = STRING(s-list.anz, ">>>")
        .
    END.    

    CREATE lnl-sum.         /*Break Line*/
    lnl-sum.summ    = "".

    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter  
        lnl-sum.rm-type = "NATION"
        lnl-sum.qty     = "RMQTY" 
        lnl-sum.adult   = "ADULT" 
        lnl-sum.percent = "(%)"   
        lnl-sum.child   = "CHILD" 
    .

    FOR EACH s-list WHERE s-list.nat NE "":
        counter = counter + 1.

        CREATE lnl-sum.
        ASSIGN
            lnl-sum.counter = counter
            lnl-sum.rm-type = TRIM(s-list.nat)
            lnl-sum.qty     = STRING(s-list.rmqty, ">>>>9")
            lnl-sum.adult   = STRING(s-list.adult, ">>>>9")
            lnl-sum.percent = STRING(s-list.proz, ">>9.99")
            lnl-sum.child   = STRING(s-list.child, ">>>>9")
        .
    END.             

    CREATE lnl-sum.         /*Break Line*/
    lnl-sum.summ    = "".
    
    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.rm-type = "ROOM AVAILABLE"
        lnl-sum.qty     = STRING(tot-avail, ">>9")
    .

    counter = counter + 1.
    IF inactive NE 0 THEN
    DO:
        CREATE lnl-sum.
        ASSIGN
            lnl-sum.counter = counter
            lnl-sum.rm-type = "OCCUPIED/INACTIVE"
            lnl-sum.qty     = STRING(tot-rm, ">>9") + "/" + STRING(inactive)
        .
    END.
    ELSE
    DO:
        CREATE lnl-sum.
        ASSIGN
            lnl-sum.counter = counter
            lnl-sum.rm-type = "T O T A L  OCCUPIED"
            lnl-sum.qty     = STRING(tot-rm, ">>9")
        .
    END.
    
    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.rm-type = ""
        lnl-sum.qty     = STRING(tot-rmqty, ">>>>9")
        lnl-sum.adult   = STRING(tot-a + tot-co, ">>>>9")
        lnl-sum.percent = "100.00"
        lnl-sum.child   = STRING(tot-c, ">>>>9")
    .

    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.rm-type = "IN PERCENTAGE (%)"
        lnl-sum.qty     = STRING(tot-rm / tot-avail * 100, ">>9.99")
    .
    
    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.rm-type = "AVRG GUEST/ROOM"
        lnl-sum.qty     = STRING((tot-a + tot-co) / tot-rm, ">>9.99")
    .

    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.rm-type = "OCC. PAYING ROOMS"
        lnl-sum.qty     = STRING(tot-payrm / tot-avail * 100,">>9.99") + " %"
    .

    CREATE lnl-sum.         /*Break Line*/
    lnl-sum.summ    = "".

    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.summ    = "SUMM"
        lnl-sum.rm-type = "CURRENCY"
        lnl-sum.qty     = "ROOMRATE"          
    .
    
    FOR EACH sum-list:
        counter = counter + 1.

        CREATE lnl-sum.
        ASSIGN
            lnl-sum.counter = counter
            lnl-sum.summ    = ""
            lnl-sum.rm-type = STRING(sum-list.curr, "x(15)")
            lnl-sum.qty     = STRING(sum-list.zipreis, "->,>>>,>>>,>>9.99")          
        .
    END.

    CREATE lnl-sum.         /*Break Line*/
    lnl-sum.summ    = "".

    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.summ    = "SUMM"
        lnl-sum.rm-type = "SEGMENT"
        lnl-sum.qty     = "RMQTY"          
    .

    FOR EACH segm-list:
        counter = counter + 1.

        CREATE lnl-sum.
        ASSIGN
            lnl-sum.counter = counter
            lnl-sum.summ    = ""
            lnl-sum.rm-type = segm-list.segment
            lnl-sum.qty     = STRING(segm-list.anzahl, ">>9")
        .
    END.

    CREATE lnl-sum.         /*Break Line*/
    lnl-sum.summ    = "".

    counter = counter + 1.
    CREATE lnl-sum.
    ASSIGN
        lnl-sum.counter = counter
        lnl-sum.summ    = "SUMM"
        lnl-sum.rm-type = "ARRANGEMENT"
        lnl-sum.qty     = "RMQTY" 
        lnl-sum.adult   = "PAX"
        lnl-sum.percent = "B-FAST"
    .

    FOR EACH argt-list:
        counter = counter + 1.

        CREATE lnl-sum.
        ASSIGN
            lnl-sum.counter = counter
            lnl-sum.summ    = ""
            lnl-sum.rm-type = STRING(argt-list.argt, "x(15)")
            lnl-sum.qty     = STRING(argt-list.tot-room, ">>>,>>9")
            lnl-sum.adult   = STRING(argt-list.tot-pax, ">>>,>>9")
            lnl-sum.percent = STRING(argt-list.tot-breakfast, ">>,>>9")
        .
    END.
    /*End FD*/*/
END PROCEDURE.

PROCEDURE create-outList:
    outnr = outnr + 1.
    CREATE output-list.
    BUFFER-COPY cl-list TO output-list.        
    output-list.nr = outnr.

    IF NUM-ENTRIES(cl-list.telefon,";") GT 1 THEN
    DO:
        output-list.memberno = TRIM(STRING(ENTRY(2,cl-list.telefon,";"),"x(25)")).           
        output-list.telefon  = TRIM(ENTRY(1,cl-list.telefon,";")).
    END.            
    
    IF NUM-ENTRIES(cl-list.mobil-tel,";") GT 1 THEN
    DO:
        output-list.membertype = TRIM(STRING(ENTRY(2,cl-list.mobil-tel,";"),"x(26)")).            
        output-list.mobil-tel  = TRIM(ENTRY(1,cl-list.mobil-tel,";")).
    END.
                    
    IF NUM-ENTRIES(cl-list.curr,";") GT 1 THEN
    DO: 
        output-list.email = STRING(ENTRY(2,cl-list.curr,";"),"x(40)").            
    END.
    
    output-list.ac = STRING(cl-list.a) + "/" + string(cl-list.c).        

    FIND FIRST sum-list WHERE sum-list.curr = ENTRY(1,cl-list.curr,";") NO-ERROR.
    IF NOT AVAILABLE sum-list THEN
    DO:
        CREATE sum-list.
        ASSIGN sum-list.curr = ENTRY(1,cl-list.curr,";").
    END.
    ASSIGN sum-list.zipreis = sum-list.zipreis + cl-list.zipreis. 

    FIND FIRST segm-list WHERE segm-list.segmcode = cl-list.paym NO-ERROR.
    IF NOT AVAILABLE segm-list THEN
    DO: 
        CREATE segm-list.
        ASSIGN segm-list.segmcode = cl-list.paym
        segm-list.segment = cl-list.segm.
    END.
    ASSIGN segm-list.anzahl = segm-list.anzahl + cl-list.qty.

    FIND FIRST argt-list WHERE argt-list.argt = cl-list.argt NO-ERROR.
    IF NOT AVAILABLE argt-list THEN DO:
        CREATE argt-list.
        ASSIGN argt-list.argt = cl-list.argt.
    END.
    ASSIGN 
        argt-list.tot-room      = argt-list.tot-room + 1
        argt-list.tot-pax       = argt-list.tot-pax + cl-list.a
        argt-list.tot-breakfast = argt-list.tot-breakfast + cl-list.tot-bfast.

    output-list.stay = cl-list.depart - cl-list.arrive.
END.
