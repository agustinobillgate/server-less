DEFINE TEMP-TABLE output-list
    FIELD gastnr        AS INTEGER                  
    FIELD rsvname       AS CHARACTER        /*Modified by gerald 23012020*/ 
    FIELD guestname     AS CHARACTER        /*Add By Gerald 23012020*/      
    FIELD resno         AS INTEGER
    FIELD reslinnr      AS INTEGER
    FIELD rm-type       AS CHAR
    FIELD create-date   AS DATE
    FIELD cidate        AS DATE
    FIELD codate        AS DATE
    FIELD room-night    AS INTEGER    
    FIELD lead          AS DECIMAL   
    FIELD argt          AS CHAR 
    FIELD currency      AS CHAR
    FIELD rmrate        AS DECIMAL
    FIELD lodging       AS DECIMAL
    FIELD avg-rmrate    AS DECIMAL
    FIELD avg-lodging   AS DECIMAL
    FIELD rmrate1       AS DECIMAL
    FIELD lodging1      AS DECIMAL
    FIELD segment       AS CHAR
    FIELD nation        AS CHAR
    FIELD rm-night      AS INTEGER
    
    FIELD c-resno       AS CHAR
    FIELD c-rmnight     AS CHAR    
    FIELD c-lead        AS CHAR
    FIELD c-rmrate      AS CHAR
    FIELD c-lodging     AS CHAR
    FIELD c-avgrmrate   AS CHAR
    FIELD c-avglodging  AS CHAR
    FIELD c-rmrate1     AS CHAR
    FIELD c-lodging1    AS CHAR
     
    FIELD adult         AS INTEGER
    FIELD child         AS INTEGER
    FIELD infant        AS INTEGER
    FIELD comp          AS INTEGER
    FIELD compchild     AS INTEGER

    FIELD avrg-lead     AS DECIMAL
    FIELD avrg-los      AS DECIMAL  
    FIELD pos           AS INTEGER
    FIELD tot-reserv    AS INTEGER
    /*ragung 304E71*/
    FIELD contcode      AS CHAR
    FIELD sourcecode    AS CHAR
    /*end*/

    FIELD check-flag    AS LOGICAL
    FIELD check-flag1    AS LOGICAL
    FIELD check-flag2    AS LOGICAL

    /*bernatd */
    FIELD tot-rate         AS CHAR
    FIELD tot-avg-rate     AS CHAR
    FIELD tot-rate1        AS CHAR
    FIELD tot-lodging      AS CHAR
    FIELD tot-avg-lodging  AS CHAR
    FIELD tot-lodging1     AS CHAR
    .  

DEFINE TEMP-TABLE tot-list
    FIELD gastnr    AS INTEGER
    FIELD t-lead    AS DECIMAL
    FIELD t-los     AS DECIMAL
    FIELD t-reserv  AS INTEGER
 .

DEFINE INPUT PARAMETER fromdate    AS DATE NO-UNDO.
DEFINE INPUT PARAMETER todate      AS DATE NO-UNDO.
DEFINE INPUT PARAMETER from-rsv    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER to-rsv      AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER exclude     AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER rm-sharer   AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER check-cdate AS LOGICAL NO-UNDO. /*Ragung 75D77B*/
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE BUFFER t-guest FOR guest.

DEFINE VARIABLE pax           AS INTEGER NO-UNDO. 
DEFINE VARIABLE ci-date       AS DATE    NO-UNDO.
DEFINE VARIABLE local-curr    AS DECIMAL NO-UNDO.
DEFINE VARIABLE foreign-curr  AS DECIMAL NO-UNDO.
DEFINE VARIABLE curr-foreign  AS INTEGER NO-UNDO.
DEFINE VARIABLE fixed-rate    AS LOGICAL NO-UNDO.
DEFINE BUFFER bguest FOR guest.
DEFINE BUFFER waehrung1 FOR waehrung.
DEFINE BUFFER boutput FOR output-list.
DEFINE BUFFER tguest FOR guest.

DEFINE VARIABLE new-contrate        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE wd-array AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE VARIABLE bill-date       AS DATE NO-UNDO. 
DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE contcode        AS CHAR.  
DEFINE VARIABLE ct              AS CHAR.  
DEFINE VARIABLE curr-zikatnr    AS INTEGER              NO-UNDO. 
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rm-rate         AS DECIMAL. 
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE it-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE bonus-array     AS LOGICAL EXTENT 999 INITIAL NO. 
DEFINE VARIABLE w-day           AS INTEGER              NO-UNDO. 
DEFINE VARIABLE rack-rate       AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE counter         AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE datacount       AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE totaldatacount  AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE tmp-date        AS DATE                 NO-UNDO.        /* Rulita 071124 | Fixing date calculate for serverless program */
DEFINE VARIABLE curr-lead-days  AS INTEGER              NO-UNDO.        /* Rulita 201124 | Fixing for serverless program */

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR. 
ASSIGN ci-date = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung1 WHERE waehrung1.wabkurz = htparam.fchar NO-LOCK NO-ERROR.
IF AVAILABLE waehrung1 THEN local-curr = waehrung1.ankauf.

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung1 WHERE waehrung1.wabkurz = htparam.fchar NO-LOCK NO-ERROR.
IF AVAILABLE waehrung1 THEN 
    ASSIGN 
        foreign-curr = waehrung1.ankauf
        curr-foreign = waehrung1.waehrungsnr.

FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs  AS INTEGER, 
     INPUT kind1    AS INTEGER, 
     INPUT kind2    AS INTEGER). 
  DEF VAR rate AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN 
      rate = rate + katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. 

/*IF fromdate LT ci-date THEN RUN create-browse.
ELSE RUN create-browse1.*/
IF fromdate LT ci-date THEN
DO:
    RUN create-browse.
END.
ELSE IF fromdate LT ci-date AND exclude = YES THEN
DO:
    RUN create-browse-exclude.
END.
ELSE IF fromdate GE ci-date AND exclude = YES THEN
DO:
    RUN create-browse-exclude1.
END.
ELSE IF fromdate LT ci-date AND rm-sharer = YES THEN
DO:
    RUN create-browse-rm-sharer.
END.
ELSE IF fromdate GE ci-date AND rm-sharer = YES THEN
DO:
    RUN create-browse-rm-sharer1.
END.
ELSE
DO:
    RUN create-browse1.
END.



FOR EACH output-list WHERE output-list.check-flag   = YES:

    IF output-list.resno    = 0 THEN output-list.c-resno    = " ".
    ELSE output-list.c-resno = STRING(output-list.resno, ">>>>>>>>9").

    IF output-list.room-night  = 0 THEN output-list.c-rmnight  = " ".
    ELSE output-list.c-rmnight = STRING(output-list.room-night, ">>>9").

    IF output-list.lead     = 0 THEN output-list.c-lead     = " ".
    ELSE output-list.c-lead = STRING(output-list.lead, "->,>>>9.99").

    IF output-list.rmrate   = 0 THEN output-list.c-rmrate   = " ".
    ELSE output-list.c-rmrate     = STRING(output-list.rmrate, "->>>,>>>,>>>,>>9.99").

    IF output-list.lodging  = 0 THEN output-list.c-lodging  = " ".
    ELSE output-list.c-lodging    = STRING(output-list.lodging, "->>>,>>>,>>>,>>9.99").

    IF output-list.rmrate1  = 0 THEN output-list.c-rmrate1  = " ".
    ELSE output-list.c-rmrate1    = STRING(output-list.rmrate1, "->>>,>>>,>>>,>>9.99").

    IF output-list.lodging1 = 0 THEN output-list.c-lodging1 = " ".
    ELSE output-list.c-lodging1   = STRING(output-list.lodging1, "->>>,>>>,>>>,>>9.99").

    IF output-list.avg-rmrate  = 0 THEN output-list.c-avgrmrate  = " ".
    ELSE output-list.c-avgrmrate    = STRING(output-list.avg-rmrate, "->>>,>>>,>>>,>>9.99").
    
    IF output-list.avrg-lead = ? THEN ASSIGN output-list.avrg-lead = 0.
    IF output-list.avrg-los = ? THEN ASSIGN output-list.avrg-los = 0.

    /*bernatd 918F24 2025*/
    IF output-list.rmrate   = 0 THEN output-list.tot-rate   = " ".
    ELSE output-list.tot-rate     = STRING(output-list.rmrate, "->>>,>>>,>>>,>>9.99").

    IF output-list.lodging  = 0 THEN output-list.tot-lodging  = " ".
    ELSE output-list.tot-lodging    = STRING(output-list.lodging, "->>>,>>>,>>>,>>9.99").
    
    IF output-list.avg-rmrate  = 0 THEN output-list.tot-avg-rate  = " ".
    ELSE output-list.tot-avg-rate    = STRING(output-list.avg-rmrate, "->>>,>>>,>>>,>>9.99").

    IF output-list.avg-lodging  = 0 THEN output-list.tot-avg-lodging  = " ".
    ELSE output-list.tot-avg-lodging    = STRING(output-list.avg-lodging, "->>>,>>>,>>>,>>9.99").

    IF output-list.rmrate1  = 0 THEN output-list.tot-rate1  = " ".
    ELSE output-list.tot-rate1    = STRING(output-list.rmrate1, "->>>,>>>,>>>,>>9.99").

    IF output-list.lodging1 = 0 THEN output-list.tot-lodging1 = " ".
    ELSE output-list.tot-lodging1   = STRING(output-list.lodging1, "->>>,>>>,>>>,>>9.99").

    ASSIGN output-list.check-flag = NO.

END.


PROCEDURE create-browse:
    DEFINE VARIABLE datum            AS DATE NO-UNDO.
    DEFINE VARIABLE datum2           AS DATE NO-UNDO.
    DEFINE VARIABLE datum3           AS DATE NO-UNDO.
    DEFINE VARIABLE datum4           AS DATE NO-UNDO.
    DEFINE VARIABLE ldatum           AS DATE NO-UNDO.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.
    
    DEFINE VARIABLE tot-lead         AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrlodging   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-los          AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-rmnight      AS INTEGER INITIAL 0.

    DEFINE VARIABLE tot-adult         AS INTEGER.
    DEFINE VARIABLE tot-child         AS INTEGER.
    DEFINE VARIABLE tot-infant        AS INTEGER.
    DEFINE VARIABLE tot-comp          AS INTEGER.
    DEFINE VARIABLE tot-compchild     AS INTEGER.

    DEFINE VARIABLE t-gastnr        AS INTEGER.
    DEFINE VARIABLE t-lead          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging1      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrlodging    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglead      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglos       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-los           AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-rmnight       AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-adult         AS INTEGER.
    DEFINE VARIABLE t-child         AS INTEGER.
    DEFINE VARIABLE t-infant        AS INTEGER.
    DEFINE VARIABLE t-comp          AS INTEGER.
    DEFINE VARIABLE t-compchild     AS INTEGER.
    DEFINE VARIABLE tot-avrglead    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrglos     AS DECIMAL INITIAL 0.

    DEFINE VARIABLE t-rmrate        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate1       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrgrmrate    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrgrmrate  AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rsv         AS DECIMAL INITIAL 0.

    /*bernatd */
     DEFINE VARIABLE t-roomrate     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avg-rmrate   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-roomrate1    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-roomrate   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avg-rmrate AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-roomrate1  AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodg         AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avg-lodg     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodg1        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodg       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avg-lodg   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodg1      AS DECIMAL INITIAL 0.


    ASSIGN datum = fromdate.
    IF todate LT (ci-date - 1) THEN datum2 = todate.
    ELSE datum2 = ci-date - 1.

    IF check-cdate THEN
    DO:
        /*history*/
        FOR EACH genstat WHERE genstat.res-logic[2] 
              AND genstat.zinr NE " " NO-LOCK,
              FIRST reservation WHERE reservation.resnr = genstat.resnr
                AND reservation.resdat GE fromdate
                AND reservation.resdat LE todate NO-LOCK,  /*Add By Gerald 23012020*/   
              FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK BY genstat.gastnr:  /*Modified by gerald 23012020*/ 

            IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                FIND FIRST tguest WHERE tguest.gastnr = genstat.gastnr
                    AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tguest THEN NEXT.
            END.
                                                                                               
            FIND FIRST output-list WHERE output-list.gastnr = genstat.gastnr
                AND output-list.resno = genstat.resnr
                AND output-list.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF NOT AVAILABLE output-list THEN DO:
                CREATE output-list.
                ASSIGN output-list.gastnr       = genstat.gastnr
                       output-list.rsvname      = reservation.NAME              /*Add by gerald 23012020*/ 
                       output-list.guestname    = guest.NAME                    /*Modified By Gerald 23012020*/      
                       output-list.resno        = genstat.resnr 
                       output-list.reslinnr     = genstat.res-int[1]
                       output-list.cidate       = genstat.res-date[1] 
                       output-list.codate       = genstat.res-date[2]
                       output-list.room-night   = genstat.res-date[2] - genstat.res-date[1] 
                       output-list.rm-night     = genstat.res-date[2] - genstat.res-date[1]  
                       output-list.argt         = genstat.argt
                       output-list.rmrate       = genstat.zipreis 
                       output-list.lodging      = genstat.logis
                       output-list.adult        = genstat.erwachs 
                       output-list.child        = genstat.kind1
                       output-list.infant       = genstat.kind2 
                       output-list.comp         = genstat.gratis
                       output-list.compchild    = genstat.kind3
                       output-list.check-flag   = YES
                       output-list.check-flag1  = YES
                       output-list.check-flag2  = YES
                       output-list.tot-rate     = STRING(output-list.room-night * output-list.rmrate,"->>>,>>>,>>>,>>9.99") /*bernatd */   
                    .         
                       
                FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE bguest THEN DO: 
                    FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                END.
                    
                FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 

                /*ragung*/
                FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                /*end*/
                
                /*FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.*/
                IF AVAILABLE reservation THEN 
                    ASSIGN 
                        output-list.create-date = reservation.resdat
                        output-list.lead        = genstat.res-date[1] - reservation.resdat. 
    
                FIND FIRST res-line WHERE res-line.resnr = genstat.resnr 
                    AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                    AND reslin-queasy.resnr = genstat.resnr 
                    AND reslin-queasy.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy THEN 
                DO: 
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = genstat.zipreis.
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.                      
                END.             
            END.
            ELSE DO:
                ASSIGN
                   output-list.rmrate       = output-list.rmrate + genstat.zipreis 
                   output-list.lodging      = output-list.lodging + genstat.logis.              
            END.
        END.
    
        FOR EACH output-list WHERE output-list.check-flag2  = YES BY output-list.rsvname BY output-list.create-date:

            /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
            /* ASSIGN
                output-list.rmrate1      = output-list.rmrate / foreign-curr
                output-list.lodging1     = output-list.lodging / foreign-curr
                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                output-list.avg-lodging  = output-list.lodging / output-list.room-night
            .
            IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
            IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */
            
            /*bernatd */
            ASSIGN
            output-list.tot-avg-rate = STRING(DECIMAL(output-list.tot-rate) / output-list.room-night,"->>>,>>>,>>>,>>9.99") 
            output-list.tot-rate1    = STRING(DECIMAL(output-list.tot-rate) / foreign-curr,"->>>,>>>,>>>,>>9.99").

            IF foreign-curr NE 0 THEN
            DO:
                ASSIGN
                    output-list.rmrate1      = output-list.rmrate / foreign-curr
                    output-list.lodging1     = output-list.lodging / foreign-curr
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.rmrate1      = 0
                    output-list.lodging1     = 0
                .
            END.

            IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN 
            DO:
                ASSIGN 
                    output-list.avg-rmrate = output-list.rmrate / output-list.room-night
                    output-list.avg-lodging = output-list.lodging / output-list.room-night
                .
            END.
            ELSE
            DO: 
                ASSIGN
                    output-list.avg-rmrate = output-list.rmrate
                    output-list.avg-lodging = output-list.lodging
                .
            END.
            /* End Rulita */

            ASSIGN
                tot-lead                 = tot-lead + output-list.lead
                tot-lodging              = tot-lodging + output-list.lodging
                tot-lodging1             = tot-lodging1 + output-list.lodging1
                tot-los                  = tot-los + output-list.room-night 
                tot-rmnight              = tot-rmnight + output-list.rm-night 
                /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                tot-avrlodging           = tot-avrlodging + output-list.lodging
                tot-adult                = tot-adult + output-list.adult
                tot-child                = tot-child + output-list.child
                tot-infant               = tot-infant + output-list.infant
                tot-comp                 = tot-comp + output-list.comp
                tot-compchild            = tot-compchild + output-list.compchild
             .
    
            
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tot-list THEN DO:
                CREATE tot-list.
                ASSIGN tot-list.gastnr = output-list.gastnr.
            END.

            ASSIGN tot-list.t-lead          = tot-list.t-lead + output-list.lead
                   tot-list.t-los           = tot-list.t-los + output-list.room-night
                   tot-list.t-reserv        = tot-list.t-reserv + 1
                   output-list.check-flag2  = NO
            .

        END.
        
        
        /*forecast*/
        datum2 = datum2 + 1.
        FOR EACH res-line WHERE ((res-line.resstatus LE 13 
            AND res-line.resstatus NE 4
            AND res-line.resstatus NE 8
            AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12 
            AND res-line.active-flag LE 1)) 
            OR (res-line.resstatus = 8 AND res-line.active-flag = 2
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] = 0 USE-INDEX gnrank_ix NO-LOCK,
            FIRST reservation WHERE reservation.resnr = res-line.resnr
            AND reservation.resdat GE fromdate 
            AND reservation.resdat LE todate NO-LOCK BY reservation.resdat BY res-line.resnr DESCENDING: 
                
                /* Rulita 130324 | Fixing for serverless */
                FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.

                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember                     /*Modified by gerald 23012020*/ 
                     NO-LOCK NO-ERROR.               
                IF AVAILABLE guest THEN DO:

                    IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                        FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                            AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tguest THEN NEXT.
                    END.

                    FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                        AND output-list.resno = res-line.resnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN DO:
                        CREATE output-list.
                        ASSIGN output-list.gastnr       = res-line.gastnr
                               output-list.rsvname      = reservation.NAME          /*Add by gerald 23012020*/ 
                               output-list.guestname    = guest.NAME                /*Modified By Gerald 23012020*/        
                               output-list.resno        = res-line.resnr 
                               output-list.reslinnr     = res-line.reslinnr
                               output-list.cidate       = res-line.ankunft 
                               output-list.codate       = res-line.abreise
                               output-list.room-night   = res-line.abreise - res-line.ankunft 
                               output-list.rm-night     = res-line.abreise - res-line.ankunft 
                               output-list.argt         = res-line.arrangement           
                               output-list.rmrate       = res-line.zipreis
                               output-list.create-date  = reservation.resdat
                               curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 201124 | Fixing for serverless */
                               output-list.lead         = curr-lead-days
                               output-list.adult        = res-line.erwachs 
                               output-list.child        = res-line.kind1
                               output-list.infant       = res-line.kind2 
                               output-list.comp         = res-line.gratis
                               output-list.compchild    = res-line.l-zuordnung[4]
                               output-list.check-flag   = YES
                               output-list.check-flag1  = YES
                               output-list.check-flag2  = YES
                            . 

                        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE bguest THEN DO: 
                            FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                        END.
                        
                        
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 

                        /*ragung*/
                        FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                        IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                        /*end*/
                        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO: 
                            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                        END. 

                        /*bernatd */
                        DO ldatum = res-line.ankunft TO res-line.abreise - 1:
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                ASSIGN output-list.tot-rate = STRING(DECIMAL(output-list.tot-rate) + reslin-queasy.deci1,"->>>,>>>,>>>,>>9.99"). 
                            END.

                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                  OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                  OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                  OUTPUT tot-dinner, OUTPUT tot-other,
                                                  OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                  OUTPUT tot-service).

                             ASSIGN output-list.tot-lodging = STRING(DECIMAL(output-list.tot-lodging) + net-lodg,"->>>,>>>,>>>,>>9.99"). 
                        END.
        
                        datum3 = datum2.
                        IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                        datum4 = todate. 
                        IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
        
                        DO ldatum = datum3 TO datum4:
                            pax         = res-line.erwachs. 
                            net-lodg    = 0.
                            curr-i      = curr-i + 1.
        
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                fixed-rate = YES. 
                                IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                                ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                            END.
                             
                            IF NOT fixed-rate THEN DO:
                                FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest-pr THEN 
                                DO: 
                                    contcode = guest-pr.CODE.  
                                    ct = res-line.zimmer-wunsch.  
                                    IF ct MATCHES("*$CODE$*") THEN  
                                    DO:  
                                        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
                                        ASSIGN output-list.contcode = contcode.  /*ragung*/
                                    END.  
                                    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                    ELSE curr-zikatnr = res-line.zikatnr. 
                                    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                                    IF AVAILABLE queasy AND queasy.logi3 THEN 
                                       bill-date = res-line.ankunft. 
                        
                                    IF new-contrate THEN 
                                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                      res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                    ELSE
                                    DO:
                                      RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                        guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                        res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                        res-line.erwachs, res-line.kind1, res-line.kind2,
                                        res-line.reserve-dec, res-line.betriebsnr, 
                                        OUTPUT rm-rate, OUTPUT rate-found).
                                      /* Rulita 130324 | Fixing for serverless */
                                      /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                      IF it-exist THEN rate-found = YES.
                                      IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                    END. 
                                    ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                                END.    
                                w-day = wd-array[WEEKDAY(bill-date)]. 
                                IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                                DO: 
                                  rm-rate = res-line.zipreis. 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day 
                                    NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) = rm-rate 
                                  THEN rack-rate = YES. 
                                END. 
                                ELSE IF rack-rate THEN 
                                DO: 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) > 0 
                                  THEN 
                                    rm-rate = get-rackrate(res-line.erwachs, 
                                      res-line.kind1, res-line.kind2). 
                                END. /* if rack-rate   */ 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.
             /*ragung*/     ELSE DO:
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*end*/
                                END.  
                            END.
        
                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                      OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                      OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                      OUTPUT tot-dinner, OUTPUT tot-other,
                                                      OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                      OUTPUT tot-service).
                             ASSIGN output-list.lodging = output-list.lodging + net-lodg.
                        END.
                        IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                        ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.
                        
                        /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                         .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */

                        /*bernatd */
                        ASSIGN
                            output-list.tot-avg-rate = STRING(DECIMAL(output-list.tot-rate) / output-list.room-night,"->>>,>>>,>>>,>>9.99")
                            output-list.tot-rate1    = STRING(DECIMAL(output-list.tot-rate) / foreign-curr,"->>>,>>>,>>>,>>9.99")
                            output-list.tot-avg-lodging  = STRING(DECIMAL(output-list.tot-lodging) / output-list.room-night,"->>>,>>>,>>>,>>9.99")
                            output-list.tot-lodging1 =  STRING(DECIMAL(output-list.tot-lodging) / foreign-curr,"->>>,>>>,>>>,>>9.99").
                        
                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN
                        DO:
                            ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        END.
                        ELSE
                        DO:
                            ASSIGN output-list.lodging1 = 0.
                        END.
                        
                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            output-list.avg-rmrate = output-list.rmrate / output-list.room-night.
                            output-list.avg-lodging = output-list.lodging / output-list.room-night.
                        END.
                        ELSE 
                        DO:
                             ASSIGN 
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .
                        END.
                        /* End Rulita */
    
                        ASSIGN
                            tot-lead                 = tot-lead + output-list.lead
                            tot-lodging              = tot-lodging + output-list.lodging
                            tot-lodging1             = tot-lodging1 + output-list.lodging1
                            tot-los                  = tot-los + output-list.room-night
                            tot-rmnight              = tot-rmnight + output-list.rm-night
                            /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                            tot-avrlodging           = tot-avrlodging + output-list.lodging
                            tot-adult                = tot-adult + output-list.adult
                            tot-child                = tot-child + output-list.child
                            tot-infant               = tot-infant + output-list.infant
                            tot-comp                 = tot-comp + output-list.comp
                            tot-compchild            = tot-compchild + output-list.compchild.
    
                        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tot-list THEN DO:
                            CREATE tot-list.
                            ASSIGN tot-list.gastnr = output-list.gastnr.
                        END.
                        ASSIGN tot-list.t-lead      = tot-list.t-lead + output-list.lead
                               tot-list.t-los       = tot-list.t-los + output-list.room-night
                               tot-list.t-reserv    = tot-list.t-reserv + 1
                        .
    
                    END.
                END.                       
            END.
        
    
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.rsvname BY output-list.create-date:
            ASSIGN counter = counter + 1.
    
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate  = t-avrgrmrate / t-rmnight
                    boutput.tot-rate        = STRING(t-roomrate,"->>>,>>>,>>>,>>9.99")    /*bernatd */       
                    boutput.tot-rate1       = STRING(t-roomrate1,"->>>,>>>,>>>,>>9.99")                
                    boutput.tot-avg-rate    = STRING(t-avg-rmrate / t-rmnight,"->>>,>>>,>>>,>>9.99")
                    boutput.tot-lodging     = STRING(t-lodg ,"->>>,>>>,>>>,>>9.99")
                    boutput.tot-avg-lodging = STRING(t-avg-lodg  / t-rmnight ,"->>>,>>>,>>>,>>9.99")
                    boutput.tot-lodging1    = STRING(t-lodg1 ,"->>>,>>>,>>>,>>9.99")
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
    
                FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
    
            END.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
                
                /* Rulita 180225 | Fixing serverless issue git 100 */
                IF output-list.lead / tot-list.t-lead NE ? 
                AND output-list.lead / tot-list.t-lead NE 0 THEN 
                DO:
                    IF tot-list.t-reserv NE ? AND tot-list.t-reserv NE 0 THEN 
                    DO:
                        ASSIGN t-avrglead = t-avrglead + (output-list.lead / tot-list.t-reserv).
                    END.
                    ELSE
                    DO:
                        ASSIGN t-avrglead = t-avrglead + 0.
                    END.

                    ASSIGN tot-avrglead = tot-avrglead + output-list.lead.
                END. 
    
                IF output-list.room-night / tot-list.t-reserv NE ?
                AND output-list.room-night / tot-list.t-reserv NE 0 THEN
                DO:
                    IF tot-list.t-reserv NE ? AND tot-list.t-reserv NE 0 THEN 
                    DO:
                        ASSIGN t-avrglos = t-avrglos + (output-list.room-night / tot-list.t-reserv).
                    END.
                    ELSE
                    DO:
                        ASSIGN t-avrglos = t-avrglos + 0.
                    END.

                    ASSIGN tot-avrglos = tot-avrglos + output-list.room-night.
                END. 
                /* End Rulita */
            END.
    
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild 
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                /*bernatd */
                tot-roomrate            = tot-roomrate   + DECIMAL(output-list.tot-rate)
                tot-roomrate1           = tot-roomrate1  + DECIMAL(output-list.tot-rate1)
                tot-avg-rmrate          = tot-avg-rmrate + DECIMAL(output-list.avg-rmrate)
                tot-lodg                = tot-lodg       + DECIMAL(output-list.tot-lodging)
                tot-avg-lodg            = tot-avg-lodg   + DECIMAL(output-list.tot-avg-lodging)
                tot-lodg1               = tot-lodg1      + DECIMAL(output-list.tot-lodging1)
                output-list.check-flag1 = NO
            .
        END.
    
        CREATE output-list.
        ASSIGN 
            counter                 = counter + 1
            output-list.pos         = counter
            output-list.gastnr      = t-gastnr
            output-list.rsvname     = "T O T A L"
            output-list.lead        = t-lead
            output-list.lodging     = t-lodging
            output-list.lodging1    = t-lodging1
            output-list.room-night  = t-los
            output-list.rm-night    = t-rmnight
            output-list.avg-lodging = t-avrlodging / t-rmnight
            output-list.adult       = t-adult 
            output-list.child       = t-child 
            output-list.infant      = t-infant 
            output-list.comp        = t-comp 
            output-list.compchild   = t-compchild 
            output-list.avrg-lead   = t-avrglead
            output-list.avrg-los    = t-avrglos      
            output-list.rmrate      = t-rmrate                
            output-list.rmrate1     = t-rmrate1               
            output-list.avg-rmrate  = t-avrgrmrate / t-rmnight
            /*bernatd */
            output-list.tot-rate    = STRING(t-roomrate,"->>>,>>>,>>>,>>9.99")               
            output-list.tot-rate1   = STRING(t-roomrate1,"->>>,>>>,>>>,>>9.99") 
            output-list.tot-avg-rate = STRING(t-avg-rmrate / t-rmnight,"->>>,>>>,>>>,>>9.99")       
            output-list.tot-lodging = STRING(t-lodg,"->>>,>>>,>>>,>>9.99")
            output-list.tot-avg-lodging = STRING(t-avg-lodg / t-rmnight,"->>>,>>>,>>>,>>9.99")
            output-list.tot-lodging1 = STRING(t-lodg1,"->>>,>>>,>>>,>>9.99")
            output-list.check-flag   = YES
         .

        FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE tot-list THEN ASSIGN output-list.tot-reserv = tot-list.t-reserv.
        
        FOR EACH tot-list NO-LOCK:
            ASSIGN tot-rsv = tot-rsv + tot-list.t-reserv.
        END.
        
        CREATE output-list.
        ASSIGN 
            counter                 = counter + 1
            output-list.pos         = counter
            output-list.gastnr      = 999999999
            output-list.rsvname     = "Grand T O T A L"
            output-list.lead        = tot-lead
            output-list.lodging     = tot-lodging
            output-list.lodging1    = tot-lodging1
            output-list.room-night  = tot-los
            output-list.rm-night    = tot-rmnight
            output-list.avg-lodging = tot-avrlodging / tot-rmnight
            output-list.adult       = tot-adult 
            output-list.child       = tot-child 
            output-list.infant      = tot-infant 
            output-list.comp        = tot-comp 
            output-list.compchild   = tot-compchild 
            output-list.avrg-lead   = tot-avrglead / tot-rsv
            output-list.avrg-los    = tot-avrglos / tot-rsv
            output-list.rmrate      = tot-rmrate                
            output-list.rmrate1     = tot-rmrate1               
            output-list.avg-rmrate  = tot-avrgrmrate / tot-rmnight
            output-list.tot-reserv  = tot-rsv
            /*bernatd */
            output-list.tot-rate        = STRING(tot-roomrate,"->>>,>>>,>>>,>>9.99")                       
            output-list.tot-rate1       = STRING(tot-roomrate1,"->>>,>>>,>>>,>>9.99")                      
            output-list.tot-avg-rate    = STRING(tot-avg-rmrate / tot-rmnight,"->>>,>>>,>>>,>>9.99") 
            output-list.tot-lodging     = STRING(tot-lodg,"->>>,>>>,>>>,>>9.99")                       
            output-list.tot-avg-lodging = STRING(tot-avg-lodg / tot-rmnight,"->>>,>>>,>>>,>>9.99") 
            output-list.tot-lodging1    = STRING(tot-lodg1,"->>>,>>>,>>>,>>9.99")
            output-list.check-flag   = YES
            .
    END.
    ELSE 
    DO:
        
        /*history*/
        FOR EACH genstat WHERE genstat.res-date[1] GE datum 
              AND genstat.res-date[1] LE datum2
              AND genstat.res-logic[2] 
              AND genstat.zinr NE " " NO-LOCK,
              FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK BY genstat.gastnr:  /*Modified by gerald 23012020*/ 

            IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                FIND FIRST tguest WHERE tguest.gastnr = genstat.gastnr
                    AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tguest THEN NEXT.
            END.
                                                                                               
            FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.  /*Add By Gerald 23012020*/   
            FIND FIRST output-list WHERE output-list.gastnr = genstat.gastnr
                AND output-list.resno = genstat.resnr
                AND output-list.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF NOT AVAILABLE output-list THEN DO:
                CREATE output-list.
                ASSIGN output-list.gastnr       = genstat.gastnr
                       output-list.rsvname      = reservation.NAME              /*Add by gerald 23012020*/ 
                       output-list.guestname    = guest.NAME                    /*Modified By Gerald 23012020*/      
                       output-list.resno        = genstat.resnr 
                       output-list.reslinnr     = genstat.res-int[1]
                       output-list.cidate       = genstat.res-date[1] 
                       output-list.codate       = genstat.res-date[2]
                       output-list.room-night   = genstat.res-date[2] - genstat.res-date[1] 
                       output-list.rm-night     = genstat.res-date[2] - genstat.res-date[1]  
                       output-list.argt         = genstat.argt
                       output-list.rmrate       = genstat.zipreis 
                       output-list.lodging      = genstat.logis
                       output-list.adult        = genstat.erwachs 
                       output-list.child        = genstat.kind1
                       output-list.infant       = genstat.kind2 
                       output-list.comp         = genstat.gratis
                       output-list.compchild    = genstat.kind3
                       output-list.check-flag   = YES
                       output-list.check-flag1  = YES
                       output-list.check-flag2  = YES
                    .                 
                       
                FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE bguest THEN DO: 
                    FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                END.
                    
                FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segment = segment.bezeich.

                /*ragung*/
                FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                /*end*/
        
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                
                /*FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.*/
                IF AVAILABLE reservation THEN 
                    ASSIGN 
                        output-list.create-date = reservation.resdat
                        output-list.lead        = genstat.res-date[1] - reservation.resdat. 
    
                FIND FIRST res-line WHERE res-line.resnr = genstat.resnr 
                    AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                    AND reslin-queasy.resnr = genstat.resnr 
                    AND reslin-queasy.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy THEN 
                DO: 
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = genstat.zipreis.
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.                      
                END.             
            END.
            ELSE DO:
                ASSIGN
                   output-list.rmrate       = output-list.rmrate + genstat.zipreis 
                   output-list.lodging      = output-list.lodging + genstat.logis.              
            END.
        END.
    
        FOR EACH output-list WHERE output-list.check-flag2  = YES:

            /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
            /* ASSIGN
                output-list.rmrate1      = output-list.rmrate / foreign-curr
                output-list.lodging1     = output-list.lodging / foreign-curr
                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                output-list.avg-lodging  = output-list.lodging / output-list.room-night
            .
            IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
            IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */

            IF foreign-curr NE ? AND foreign-curr NE 0 THEN
            DO:
                ASSIGN
                    output-list.rmrate1      = output-list.rmrate / foreign-curr
                    output-list.lodging1     = output-list.lodging / foreign-curr
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.rmrate1      = 0
                    output-list.lodging1     = 0
                .
            END.

            IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN 
            DO:
                ASSIGN 
                    output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                    output-list.avg-lodging  = output-list.lodging / output-list.room-night
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.avg-rmrate = output-list.rmrate
                    output-list.avg-lodging  = output-list.lodging
                .
            END.
            /* End Rulita */
    
            ASSIGN
                tot-lead                 = tot-lead + output-list.lead
                tot-lodging              = tot-lodging + output-list.lodging
                tot-lodging1             = tot-lodging1 + output-list.lodging1
                tot-los                  = tot-los + output-list.room-night 
                tot-rmnight              = tot-rmnight + output-list.rm-night 
                /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                tot-avrlodging           = tot-avrlodging + output-list.lodging
                tot-adult                = tot-adult + output-list.adult
                tot-child                = tot-child + output-list.child
                tot-infant               = tot-infant + output-list.infant
                tot-comp                 = tot-comp + output-list.comp
                tot-compchild            = tot-compchild + output-list.compchild
             .
    
            
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tot-list THEN DO:
                CREATE tot-list.
                ASSIGN tot-list.gastnr = output-list.gastnr.
            END.
            ASSIGN tot-list.t-lead          = tot-list.t-lead + output-list.lead
                   tot-list.t-los           = tot-list.t-los + output-list.room-night
                   tot-list.t-reserv        = tot-list.t-reserv + 1
                   output-list.check-flag2  = NO
            .
    
        END.
    
        
        /*forecast*/
        datum2 = datum2 + 1.
        IF todate GE ci-date THEN DO:
        FOR EACH res-line WHERE ((res-line.resstatus LE 13 
            AND res-line.resstatus NE 4
            AND res-line.resstatus NE 8
            AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12 
            AND res-line.active-flag LE 1 
            AND res-line.ankunft GE fromdate
            AND res-line.ankunft LE todate)) OR (res-line.resstatus = 8 AND res-line.active-flag = 2
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK 
            USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending:
                
                /* Rulita 130324 | Fixing for serverless */
                FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
 
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember                     /*Modified by gerald 23012020*/ 
                   NO-LOCK NO-ERROR.               
                IF AVAILABLE guest THEN DO:

                    IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                        FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                            AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tguest THEN NEXT.
                    END.

                    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
                    FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                        AND output-list.resno = res-line.resnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN DO:
                        CREATE output-list.
                        ASSIGN output-list.gastnr       = res-line.gastnr
                               output-list.rsvname      = reservation.NAME          /*Add by gerald 23012020*/ 
                               output-list.guestname    = guest.NAME                /*Modified By Gerald 23012020*/        
                               output-list.resno        = res-line.resnr 
                               output-list.reslinnr     = res-line.reslinnr
                               output-list.cidate       = res-line.ankunft 
                               output-list.codate       = res-line.abreise
                               output-list.room-night   = res-line.abreise - res-line.ankunft 
                               output-list.rm-night     = res-line.abreise - res-line.ankunft 
                               output-list.argt         = res-line.arrangement           
                               output-list.rmrate       = res-line.zipreis
                               output-list.create-date  = reservation.resdat
                               curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 201124 | Fixing for serverless */
                               output-list.lead         = curr-lead-days
                               output-list.adult        = res-line.erwachs 
                               output-list.child        = res-line.kind1
                               output-list.infant       = res-line.kind2 
                               output-list.comp         = res-line.gratis
                               output-list.compchild    = res-line.l-zuordnung[4]
                               output-list.check-flag   = YES
                               output-list.check-flag1  = YES
                               output-list.check-flag2  = YES
                            . 
        
                        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE bguest THEN DO: 
                            FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                        END.
                        
                        
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE segment THEN output-list.segment = segment.bezeich.

                        /*ragung*/
                        FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                        IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                        /*end*/
        
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO: 
                            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                        END. 
        
                        datum3 = datum2.
                        IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                        datum4 = todate. 
                        IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
        
                        DO ldatum = datum3 TO datum4:
                            pax         = res-line.erwachs. 
                            net-lodg    = 0.
                            curr-i      = curr-i + 1.
        
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                fixed-rate = YES. 
                                IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                                ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                            END.
                             
                            IF NOT fixed-rate THEN DO:
                                FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest-pr THEN 
                                DO: 
                                    contcode = guest-pr.CODE.  
                                    ct = res-line.zimmer-wunsch.  
                                    IF ct MATCHES("*$CODE$*") THEN  
                                    DO:  
                                        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1). 
                                        ASSIGN output-list.contcode = contcode.  /*ragung*/
                                    END.  
                                    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                    ELSE curr-zikatnr = res-line.zikatnr. 
                                    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                                    IF AVAILABLE queasy AND queasy.logi3 THEN 
                                       bill-date = res-line.ankunft. 
                        
                                    IF new-contrate THEN 
                                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                      res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                    ELSE
                                    DO:
                                      RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                        guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                        res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                        res-line.erwachs, res-line.kind1, res-line.kind2,
                                        res-line.reserve-dec, res-line.betriebsnr, 
                                        OUTPUT rm-rate, OUTPUT rate-found).
                                      /* Rulita 130324 | Fixing for serverless */
                                      /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                      IF it-exist THEN rate-found = YES.
                                      IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                    END. 
                                    ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                                END.    
                                w-day = wd-array[WEEKDAY(bill-date)]. 
                                IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                                DO: 
                                  rm-rate = res-line.zipreis. 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day 
                                    NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) = rm-rate 
                                  THEN rack-rate = YES. 
                                END. 
                                ELSE IF rack-rate THEN 
                                DO: 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) > 0 
                                  THEN 
                                    rm-rate = get-rackrate(res-line.erwachs, 
                                      res-line.kind1, res-line.kind2). 
                                END. /* if rack-rate   */ 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.
             /*ragung*/     ELSE DO:
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*end*/
                                END.  
                            END.
        
                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                      OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                      OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                      OUTPUT tot-dinner, OUTPUT tot-other,
                                                      OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                      OUTPUT tot-service).
                             ASSIGN output-list.lodging = output-list.lodging + net-lodg.
                        END.
                        IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                        ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.
                        
                        /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                         .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */

                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        ELSE ASSIGN output-list.lodging1 = 0.

                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            ASSIGN
                                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                                output-list.avg-lodging  = output-list.lodging / output-list.room-night
                            .
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .
                        END.
                        /* End Rulita */
    
                        ASSIGN
                            tot-lead                 = tot-lead + output-list.lead
                            tot-lodging              = tot-lodging + output-list.lodging
                            tot-lodging1             = tot-lodging1 + output-list.lodging1
                            tot-los                  = tot-los + output-list.room-night
                            tot-rmnight              = tot-rmnight + output-list.rm-night
                            /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                            tot-avrlodging           = tot-avrlodging + output-list.lodging
                            tot-adult                = tot-adult + output-list.adult
                            tot-child                = tot-child + output-list.child
                            tot-infant               = tot-infant + output-list.infant
                            tot-comp                 = tot-comp + output-list.comp
                            tot-compchild            = tot-compchild + output-list.compchild.
    
                        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tot-list THEN DO:
                            CREATE tot-list.
                            ASSIGN tot-list.gastnr = output-list.gastnr.
                        END.
                        ASSIGN tot-list.t-lead      = tot-list.t-lead + output-list.lead
                               tot-list.t-los       = tot-list.t-los + output-list.room-night
                               tot-list.t-reserv    = tot-list.t-reserv + 1
                        .
    
                    END.
                END.                       
            END.
        END.
    
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.gastnr:
            ASSIGN counter = counter + 1.
    
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate  = t-avrgrmrate / t-rmnight
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
    
                FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
    
            END.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
                
                /* Rulita 180225 | Fixing serverless issue git 100 */
                IF output-list.lead NE 0 AND output-list.lead NE ? THEN 
                DO:
                    IF output-list.lead / tot-list.t-lead NE ? THEN 
                        ASSIGN
                            t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                            tot-avrglead          = tot-avrglead + output-list.lead
                    .
                END.
    
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .

                IF output-list.lead / tot-list.t-lead NE ? THEN 
                    ASSIGN
                        t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                        tot-avrglead          = tot-avrglead + output-list.lead
                 .
    
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
    
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild 
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1  = NO
            .
    
        END.
    
        CREATE output-list.
        ASSIGN 
            counter                 = counter + 1
            output-list.pos         = counter
            output-list.gastnr      = t-gastnr
            output-list.rsvname     = "T O T A L"
            output-list.lead        = t-lead
            output-list.lodging     = t-lodging
            output-list.lodging1    = t-lodging1
            output-list.room-night  = t-los
            output-list.rm-night    = t-rmnight
            output-list.avg-lodging = t-avrlodging / t-rmnight
            output-list.adult       = t-adult 
            output-list.child       = t-child 
            output-list.infant      = t-infant 
            output-list.comp        = t-comp 
            output-list.compchild   = t-compchild 
            output-list.avrg-lead   = t-avrglead
            output-list.avrg-los    = t-avrglos      
            output-list.rmrate      = t-rmrate                
            output-list.rmrate1     = t-rmrate1               
            output-list.avg-rmrate  = t-avrgrmrate / t-rmnight
            output-list.check-flag   = YES
         .

        FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE tot-list THEN ASSIGN output-list.tot-reserv = tot-list.t-reserv.
        
        FOR EACH tot-list NO-LOCK:
            ASSIGN tot-rsv = tot-rsv + tot-list.t-reserv.
        END.
        
        CREATE output-list.
        ASSIGN 
            counter                 = counter + 1
            output-list.pos         = counter
            output-list.gastnr      = 999999999
            output-list.rsvname     = "Grand T O T A L"
            output-list.lead        = tot-lead
            output-list.lodging     = tot-lodging
            output-list.lodging1    = tot-lodging1
            output-list.room-night  = tot-los
            output-list.rm-night    = tot-rmnight
            output-list.avg-lodging = tot-avrlodging / tot-rmnight
            output-list.adult       = tot-adult 
            output-list.child       = tot-child 
            output-list.infant      = tot-infant 
            output-list.comp        = tot-comp 
            output-list.compchild   = tot-compchild 
            output-list.avrg-lead   = tot-avrglead / tot-rsv
            output-list.avrg-los    = tot-avrglos / tot-rsv
            output-list.rmrate      = tot-rmrate                
            output-list.rmrate1     = tot-rmrate1               
            output-list.avg-rmrate  = tot-avrgrmrate / tot-rmnight
            output-list.tot-reserv  = tot-rsv
            output-list.check-flag   = YES
            .
    END.
END.

PROCEDURE create-browse1:
    DEFINE VARIABLE datum            AS DATE NO-UNDO.
    DEFINE VARIABLE datum2           AS DATE NO-UNDO.
    DEFINE VARIABLE datum3           AS DATE NO-UNDO.
    DEFINE VARIABLE datum4           AS DATE NO-UNDO.
    DEFINE VARIABLE ldatum           AS DATE NO-UNDO.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.

    DEFINE VARIABLE tot-lead         AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrlodging   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-los          AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-rmnight      AS INTEGER INITIAL 0.

    DEFINE VARIABLE tot-adult         AS INTEGER.
    DEFINE VARIABLE tot-child         AS INTEGER.
    DEFINE VARIABLE tot-infant        AS INTEGER.
    DEFINE VARIABLE tot-comp          AS INTEGER.
    DEFINE VARIABLE tot-compchild     AS INTEGER.


    DEFINE VARIABLE t-gastnr        AS INTEGER.
    DEFINE VARIABLE t-lead          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging1      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrlodging    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglead      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglos       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-los           AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-rmnight       AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-adult         AS INTEGER.
    DEFINE VARIABLE t-child         AS INTEGER.
    DEFINE VARIABLE t-infant        AS INTEGER.
    DEFINE VARIABLE t-comp          AS INTEGER.
    DEFINE VARIABLE t-compchild     AS INTEGER.
    DEFINE VARIABLE tot-avrglead    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrglos     AS DECIMAL INITIAL 0.

    DEFINE VARIABLE t-rmrate        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate1       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrgrmrate    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrgrmrate  AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rsv         AS DECIMAL INITIAL 0.
    
    IF check-cdate THEN
    DO:
        FOR EACH res-line WHERE (res-line.active-flag LE 1 
        AND res-line.resstatus LE 13 
        AND res-line.resstatus NE 4 
        AND res-line.resstatus NE 12) OR 
        (res-line.active-flag = 2 AND res-line.resstatus = 8
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK,
        FIRST reservation WHERE reservation.resnr = res-line.resnr
        AND reservation.resdat GE fromdate 
        AND reservation.resdat LE todate NO-LOCK BY reservation.resdat BY res-line.resnr:
        
          ASSIGN
          curr-i        = 0
          tot-breakfast = 0
          tot-lunch     = 0
          tot-dinner    = 0
          tot-other     = 0
          ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*")
          kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").

          /* ITA 09/04/2025 | Fixing for serverless */
         FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
        
         FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember                     /*Modified by gerald 23012020*/ 
              NO-LOCK NO-ERROR.            
         IF AVAILABLE guest THEN DO:
             IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                    AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tguest THEN NEXT.
            END.

             FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr  
                 AND output-list.resno = res-line.resnr
                 AND output-list.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
             IF NOT AVAILABLE output-list THEN DO:
                 CREATE output-list.
                 ASSIGN output-list.gastnr       = res-line.gastnr 
                        output-list.rsvname      = reservation.NAME      /*Modified by gerald 23012020*/ 
                        output-list.guestname    = guest.NAME            /*Add By Gerald 23012020*/            
                        output-list.resno        = res-line.resnr
                        output-list.reslinnr     = res-line.reslinnr
                        output-list.cidate       = res-line.ankunft 
                        output-list.codate       = res-line.abreise
                        output-list.room-night   = res-line.abreise - res-line.ankunft 
                        output-list.rm-night     = res-line.abreise - res-line.ankunft 
                        output-list.argt         = res-line.arrangement           
                        /*output-list.rmrate       = res-line.zipreis */
                        output-list.create-date  = reservation.resdat
                        /* output-list.lead         = res-line.ankunft - reservation.resdat */
                        curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 161224 | Fixing for serverless 299 */
                        output-list.lead         = curr-lead-days
                        output-list.adult        = res-line.erwachs 
                        output-list.child        = res-line.kind1
                        output-list.infant       = res-line.kind2 
                        output-list.comp         = res-line.gratis
                        output-list.compchild    = res-line.l-zuordnung[4]
                        output-list.check-flag   = YES
                        output-list.check-flag1  = YES
                        output-list.check-flag2  = YES
                     . 
        
        
                 FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                 IF AVAILABLE bguest THEN DO: 
                     FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                     IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.                       
                 END.

                 /*ragung*/
                 FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                 IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                 /*end*/

                 FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                 IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                 FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                 IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
        
                 FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                     AND reslin-queasy.resnr = res-line.resnr 
                     AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                 IF AVAILABLE reslin-queasy THEN 
                 DO: 
                     FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                     IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                 END. 
        
                 datum3 = fromdate.
                 IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                 datum4 = todate. 
                 IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
                
                 tmp-date = res-line.abreise - 1.                              /* Rulita 071124 | Fixing date calculate for serverless program */
                 /*DO ldatum = datum3 TO datum4:*/
                 /* DO ldatum = res-line.ankunft TO res-line.abreise - 1: */    /* Rulita 071124 | Fixing date calculate for serverless program */
                 DO ldatum = res-line.ankunft TO tmp-date:
                     pax         = res-line.erwachs. 
                     net-lodg    = 0.
                     curr-i      = curr-i + 1.
        
                     FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                       AND reslin-queasy.resnr = res-line.resnr 
                       AND reslin-queasy.reslinnr = res-line.reslinnr 
                       AND reslin-queasy.date1 LE ldatum 
                       AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                     IF AVAILABLE reslin-queasy THEN DO:
                         fixed-rate = YES. 
                         IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                         ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                     END.
        
                     IF NOT fixed-rate THEN DO:
                         FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                         IF AVAILABLE guest-pr THEN 
                         DO: 
                             contcode = guest-pr.CODE.  
                             ct = res-line.zimmer-wunsch.  
                             IF ct MATCHES("*$CODE$*") THEN  
                             DO:  
                                 ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                 contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
                                 ASSIGN output-list.contcode = contcode.  /*ragung*/
                             END.  
                             IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                             ELSE curr-zikatnr = res-line.zikatnr. 
                             FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                               = res-line.reserve-int NO-LOCK NO-ERROR. 
                             IF AVAILABLE queasy AND queasy.logi3 THEN 
                                bill-date = res-line.ankunft. 
        
                             IF new-contrate THEN 
                             RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                               res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                               res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                               curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                               res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                               OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                             ELSE
                             DO:
                               RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                 guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                 res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                 res-line.erwachs, res-line.kind1, res-line.kind2,
                                 res-line.reserve-dec, res-line.betriebsnr, 
                                 OUTPUT rm-rate, OUTPUT rate-found).
                                 /* Rulita 130324 | Fixing for serverless */
                                 /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                               IF it-exist THEN rate-found = YES.
                               IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                             END. 
                             ASSIGN output-list.rmrate = output-list.rmrate + rm-rate.                   
                         END.    
                         w-day = wd-array[WEEKDAY(bill-date)]. 
                         IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                         DO: 
                           rm-rate = res-line.zipreis. 
                           FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                             AND katpreis.argtnr = arrangement.argtnr 
                             AND katpreis.startperiode LE bill-date 
                             AND katpreis.endperiode GE bill-date 
                             AND katpreis.betriebsnr = w-day 
                             NO-LOCK NO-ERROR. 
                           IF NOT AVAILABLE katpreis THEN 
                           FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                             AND katpreis.argtnr = arrangement.argtnr 
                             AND katpreis.startperiode LE bill-date 
                             AND katpreis.endperiode GE bill-date 
                             AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                           IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                             res-line.kind1, res-line.kind2) = rm-rate 
                           THEN rack-rate = YES. 
                         END. 
                         ELSE IF rack-rate THEN 
                         DO: 
                           FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                             AND katpreis.argtnr = arrangement.argtnr 
                             AND katpreis.startperiode LE bill-date 
                             AND katpreis.endperiode GE bill-date 
                             AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                           IF NOT AVAILABLE katpreis THEN 
                           FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                             AND katpreis.argtnr = arrangement.argtnr 
                             AND katpreis.startperiode LE bill-date 
                             AND katpreis.endperiode GE bill-date 
                             AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                           IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                             res-line.kind1, res-line.kind2) > 0 
                           THEN 
                             rm-rate = get-rackrate(res-line.erwachs, 
                               res-line.kind1, res-line.kind2). 
                         END. /* if rack-rate   */ 
                         ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                     END.
      /*ragung*/     ELSE DO:
                         ct = res-line.zimmer-wunsch.  
                         IF ct MATCHES("*$CODE$*") THEN  
                         DO:  
                             ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                             contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                             ASSIGN output-list.contcode = contcode.  /*end*/
                         END.  
                     END.
        
                      RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                               OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                               OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                               OUTPUT tot-dinner, OUTPUT tot-other,
                                               OUTPUT tot-rmrev, OUTPUT tot-vat,
                                               OUTPUT tot-service).
                      ASSIGN output-list.lodging = output-list.lodging + net-lodg.                         
                 END.
        
                 IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                 ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.

                 /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                 /* ASSIGN 
                    output-list.lodging1     = output-list.lodging / foreign-curr
                    output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                    output-list.avg-lodging  = output-list.lodging / output-list.room-night
                .
                IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */

                IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                ELSE ASSIGN output-list.lodging1 = 0.
                
                IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                DO:
                    ASSIGN
                        output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                        output-list.avg-lodging  = output-list.lodging / output-list.room-night
                    .
                END.
                ELSE
                DO:
                    ASSIGN
                        output-list.avg-rmrate = output-list.rmrate
                        output-list.avg-lodging  = output-list.lodging
                    .
                END.
                /* End Rulita */
        
                 ASSIGN
                     tot-lead                 = tot-lead + output-list.lead
                     tot-lodging              = tot-lodging + output-list.lodging
                     tot-lodging1             = tot-lodging1 + output-list.lodging1
                     tot-los                  = tot-los + output-list.room-night
                     tot-rmnight              = tot-rmnight + output-list.rm-night
                     /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                     tot-avrlodging           = tot-avrlodging + output-list.lodging
                     tot-adult                = tot-adult + output-list.adult
                     tot-child                = tot-child + output-list.child
                     tot-infant               = tot-infant + output-list.infant
                     tot-comp                 = tot-comp + output-list.comp
                     tot-compchild            = tot-compchild + output-list.compchild.
        
        
                 FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                 IF NOT AVAILABLE tot-list THEN DO:
                     CREATE tot-list.
                     ASSIGN tot-list.gastnr = output-list.gastnr.
                 END.
                 ASSIGN tot-list.t-lead     = tot-list.t-lead + output-list.lead
                        tot-list.t-los      = tot-list.t-los + output-list.room-night
                        tot-list.t-reserv   = tot-list.t-reserv + 1
                 .
             END.
         END.                
        END.

        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.rsvname BY output-list.create-date:
            ASSIGN counter  = counter + 1.
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate = t-avrgrmrate / t-rmnight
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
                 FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                 IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
            END.
            
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
            
                IF output-list.lead / tot-list.t-lead NE ? THEN 
                    ASSIGN
                        t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                        tot-avrglead          = tot-avrglead + output-list.lead
                 .
            
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
            
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild  
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1  = NO
            .
        END.
    END.
    ELSE
    DO:
        FOR EACH res-line WHERE (res-line.active-flag LE 1 
        AND res-line.resstatus LE 13 
        AND res-line.resstatus NE 4 
        AND res-line.resstatus NE 12
        AND res-line.ankunft GE fromdate
        AND res-line.ankunft LE todate) OR 
        (res-line.active-flag = 2 AND res-line.resstatus = 8
         AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK BY res-line.resnr:
            
             ASSIGN
             curr-i        = 0
             tot-breakfast = 0
             tot-lunch     = 0
             tot-dinner    = 0
             tot-other     = 0
             ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*")
             kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").

              /* ITA 09/04/2025 | Fixing for serverless */
            FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
            
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember                     /*Modified by gerald 23012020*/ 
               NO-LOCK NO-ERROR.            
            IF AVAILABLE guest THEN DO:

                IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                    FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                        AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE tguest THEN NEXT.
                END.

                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
                FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr  
                    AND output-list.resno = res-line.resnr
                    AND output-list.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE output-list THEN DO:
                    CREATE output-list.
                    ASSIGN output-list.gastnr       = res-line.gastnr 
                           output-list.rsvname      = reservation.NAME      /*Modified by gerald 23012020*/ 
                           output-list.guestname    = guest.NAME            /*Add By Gerald 23012020*/            
                           output-list.resno        = res-line.resnr
                           output-list.reslinnr     = res-line.reslinnr
                           output-list.cidate       = res-line.ankunft 
                           output-list.codate       = res-line.abreise
                           output-list.room-night   = res-line.abreise - res-line.ankunft 
                           output-list.rm-night     = res-line.abreise - res-line.ankunft 
                           output-list.argt         = res-line.arrangement           
                           /*output-list.rmrate       = res-line.zipreis */
                           output-list.create-date  = reservation.resdat
                           /* output-list.lead         = res-line.ankunft - reservation.resdat */
                           curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 161224 | Fixing for serverless 299 */
                           output-list.lead         = curr-lead-days
                           output-list.adult        = res-line.erwachs 
                           output-list.child        = res-line.kind1
                           output-list.infant       = res-line.kind2 
                           output-list.comp         = res-line.gratis
                           output-list.compchild    = res-line.l-zuordnung[4]
                           output-list.check-flag   = YES
                           output-list.check-flag1  = YES
                           output-list.check-flag2  = YES
                        . 
        
                    
                    FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE bguest THEN DO: 
                        FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                        IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.                       
                    END.

                    /*ragung*/
                    FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                    IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                    /*end*/

                    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                    IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                        
                    FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                        AND reslin-queasy.resnr = res-line.resnr 
                        AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE reslin-queasy THEN 
                    DO: 
                        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                    END. 
                    
                    datum3 = fromdate.
                    IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                    datum4 = todate. 
                    IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
                    
                    tmp-date = res-line.abreise - 1.                               /* Rulita 071124 | Fixing date calculate for serverless program */
                    /*DO ldatum = datum3 TO datum4:*/
                    /* DO ldatum = res-line.ankunft TO res-line.abreise - 1: */     /* Rulita 071124 | Fixing date calculate for serverless program */
                    DO ldatum = res-line.ankunft TO tmp-date:
                        pax         = res-line.erwachs. 
                        net-lodg    = 0.
                        curr-i      = curr-i + 1.
        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                          AND reslin-queasy.resnr = res-line.resnr 
                          AND reslin-queasy.reslinnr = res-line.reslinnr 
                          AND reslin-queasy.date1 LE ldatum 
                          AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN DO:
                            fixed-rate = YES. 
                            IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                            ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                        END.
                         
                        IF NOT fixed-rate THEN DO:
                            FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                            IF AVAILABLE guest-pr THEN 
                            DO: 
                                contcode = guest-pr.CODE.  
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*ragung*/
                                END.  
                                IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                ELSE curr-zikatnr = res-line.zikatnr. 
                                FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                  = res-line.reserve-int NO-LOCK NO-ERROR. 
                                IF AVAILABLE queasy AND queasy.logi3 THEN 
                                   bill-date = res-line.ankunft. 
                    
                                IF new-contrate THEN 
                                RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                  res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                  res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                  curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                  res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                  OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                ELSE
                                DO:
                                  RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                    guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                    res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                    res-line.erwachs, res-line.kind1, res-line.kind2,
                                    res-line.reserve-dec, res-line.betriebsnr, 
                                    OUTPUT rm-rate, OUTPUT rate-found).
                                    /* Rulita 130324 | Fixing for serverless */
                                    /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                  IF it-exist THEN rate-found = YES.
                                  IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                END. 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate.
                            END.    
                            w-day = wd-array[WEEKDAY(bill-date)]. 
                            IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                            DO: 
                              rm-rate = res-line.zipreis. 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = w-day 
                                NO-LOCK NO-ERROR. 
                              IF NOT AVAILABLE katpreis THEN 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                              IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                res-line.kind1, res-line.kind2) = rm-rate 
                              THEN rack-rate = YES. 
                            END. 
                            ELSE IF rack-rate THEN 
                            DO: 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                              IF NOT AVAILABLE katpreis THEN 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                              IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                res-line.kind1, res-line.kind2) > 0 
                              THEN 
                                rm-rate = get-rackrate(res-line.erwachs, 
                                  res-line.kind1, res-line.kind2). 
                            END. /* if rack-rate   */ 
                            ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                        END.
         /*ragung*/     ELSE DO:
                            ct = res-line.zimmer-wunsch.  
                            IF ct MATCHES("*$CODE$*") THEN  
                            DO:  
                                ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                ASSIGN output-list.contcode = contcode.  /*end*/
                            END.  
                        END.
        
                         RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                  OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                  OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                  OUTPUT tot-dinner, OUTPUT tot-other,
                                                  OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                  OUTPUT tot-service).
                         ASSIGN output-list.lodging = output-list.lodging + net-lodg.                         
                    END.
                    
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                    ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.

                    /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                    /* ASSIGN 
                        output-list.lodging1     = output-list.lodging / foreign-curr
                        output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                        output-list.avg-lodging  = output-list.lodging / output-list.room-night
                    .
                    IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                    IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */
                    
                    IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                    ELSE ASSIGN output-list.lodging1 = 0.
                    
                    IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                    DO:
                        ASSIGN
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                    END.
                    ELSE 
                    DO:
                        ASSIGN
                            output-list.avg-rmrate = output-list.rmrate
                            output-list.avg-lodging  = output-list.lodging
                        .
                    END.
                    /* End Rulita */
        
                    ASSIGN
                        tot-lead                 = tot-lead + output-list.lead
                        tot-lodging              = tot-lodging + output-list.lodging
                        tot-lodging1             = tot-lodging1 + output-list.lodging1
                        tot-los                  = tot-los + output-list.room-night
                        tot-rmnight              = tot-rmnight + output-list.rm-night
                        /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                        tot-avrlodging           = tot-avrlodging + output-list.lodging
                        tot-adult                = tot-adult + output-list.adult
                        tot-child                = tot-child + output-list.child
                        tot-infant               = tot-infant + output-list.infant
                        tot-comp                 = tot-comp + output-list.comp
                        tot-compchild            = tot-compchild + output-list.compchild.
        
        
                    FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE tot-list THEN DO:
                        CREATE tot-list.
                        ASSIGN tot-list.gastnr = output-list.gastnr.
                    END.
                    ASSIGN tot-list.t-lead     = tot-list.t-lead + output-list.lead
                           tot-list.t-los      = tot-list.t-los + output-list.room-night
                           tot-list.t-reserv   = tot-list.t-reserv + 1
                    .
                END.
            END.                
        END.   
        
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.gastnr:
            ASSIGN counter  = counter + 1.
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.resno       = datacount
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    counter             = counter + 1
                    totaldatacount      = totaldatacount + datacount
                    datacount           = 0
                    boutput.check-flag  = YES
                 .
    
                 /* Rulita 180225 | Fixing serverless issue git 100 */
                IF t-rmnight NE ? AND t-rmnight NE 0 THEN
                DO:
                    IF t-avrlodging NE ? AND t-avrlodging NE 0 THEN
                    DO:
                        boutput.avg-lodging = t-avrlodging / t-rmnight.
                    END.
                    
                    IF t-avrgrmrate NE ? AND t-avrgrmrate NE 0 THEN
                    DO:
                        boutput.avg-rmrate = t-avrgrmrate / t-rmnight.
                    END.
                END.
    
                FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
            END.
            datacount           = datacount + 1.
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
            
                IF output-list.lead / tot-list.t-lead NE ? THEN 
                    ASSIGN
                        t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                        tot-avrglead          = tot-avrglead + output-list.lead
                 .
            
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
            
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild  
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1 = NO
            .
        END.
    END.

    CREATE output-list.
    ASSIGN 
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = t-gastnr
        output-list.rsvname     = "T O T A L"
        output-list.resno       = datacount
        output-list.lead        = t-lead
        output-list.lodging     = t-lodging
        output-list.lodging1    = t-lodging1
        output-list.room-night  = t-los
        output-list.rm-night    = t-rmnight
        output-list.avg-lodging = t-avrlodging / t-rmnight
        output-list.adult       = t-adult 
        output-list.child       = t-child 
        output-list.infant      = t-infant 
        output-list.comp        = t-comp 
        output-list.compchild   = t-compchild 
        output-list.avrg-lead   = t-avrglead
        output-list.avrg-los    = t-avrglos    
        output-list.rmrate      = t-rmrate                
        output-list.rmrate1     = t-rmrate1               
        output-list.avg-rmrate  = t-avrgrmrate / t-rmnight
        totaldatacount          = totaldatacount + datacount
        datacount               = 0
        output-list.check-flag  = YES
     .
    FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE tot-list THEN ASSIGN output-list.tot-reserv = tot-list.t-reserv.

    FOR EACH tot-list NO-LOCK:
        ASSIGN tot-rsv = tot-rsv + tot-list.t-reserv.
    END.
    
    CREATE output-list.
    ASSIGN 
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = 999999999
        output-list.rsvname     = "Grand T O T A L"
        output-list.resno       = totaldatacount
        output-list.lead        = tot-lead
        output-list.lodging     = tot-lodging
        output-list.lodging1    = tot-lodging1
        output-list.room-night  = tot-los
        output-list.rm-night    = tot-rmnight
        output-list.avg-lodging = tot-avrlodging / tot-rmnight
        output-list.adult       = tot-adult 
        output-list.child       = tot-child 
        output-list.infant      = tot-infant 
        output-list.comp        = tot-comp 
        output-list.compchild   = tot-compchild
        output-list.avrg-lead   = tot-avrglead / tot-rsv
        output-list.avrg-los    = tot-avrglos / tot-rsv
        output-list.rmrate      = tot-rmrate                
        output-list.rmrate1     = tot-rmrate1               
        output-list.avg-rmrate  = tot-avrgrmrate / tot-rmnight
        output-list.tot-reserv  = tot-rsv
        totaldatacount          = 0
        output-list.check-flag  = YES
     .
END.


PROCEDURE create-browse-exclude:
    DEFINE VARIABLE datum            AS DATE NO-UNDO.
    DEFINE VARIABLE datum2           AS DATE NO-UNDO.
    DEFINE VARIABLE datum3           AS DATE NO-UNDO.
    DEFINE VARIABLE datum4           AS DATE NO-UNDO.
    DEFINE VARIABLE ldatum           AS DATE NO-UNDO.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.
    
    DEFINE VARIABLE tot-lead         AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrlodging   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-los          AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-rmnight      AS INTEGER INITIAL 0.

    DEFINE VARIABLE tot-adult         AS INTEGER.
    DEFINE VARIABLE tot-child         AS INTEGER.
    DEFINE VARIABLE tot-infant        AS INTEGER.
    DEFINE VARIABLE tot-comp          AS INTEGER.
    DEFINE VARIABLE tot-compchild     AS INTEGER.

    DEFINE VARIABLE t-gastnr        AS INTEGER.
    DEFINE VARIABLE t-lead          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging1      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrlodging    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglead      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglos       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-los           AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-rmnight       AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-adult         AS INTEGER.
    DEFINE VARIABLE t-child         AS INTEGER.
    DEFINE VARIABLE t-infant        AS INTEGER.
    DEFINE VARIABLE t-comp          AS INTEGER.
    DEFINE VARIABLE t-compchild     AS INTEGER.
    DEFINE VARIABLE tot-avrglead    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrglos     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate1       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrgrmrate    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrgrmrate  AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rsv         AS DECIMAL INITIAL 0.


    ASSIGN datum = fromdate.
    IF todate LT (ci-date - 1) THEN datum2 = todate.
    ELSE datum2 = ci-date - 1.
    
    IF check-cdate THEN
    DO:
       /*history*/
        FOR EACH genstat WHERE genstat.res-logic[2] 
              AND genstat.zinr NE " " NO-LOCK,
    
            /*FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.NAME GE from-rsv AND guest.NAME LE to-rsv NO-LOCK BY genstat.gastnr:  */        
            FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK BY genstat.gastnr:           /*Modified By Gerald 23012020*/
            
            IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                FIND FIRST tguest WHERE tguest.gastnr = genstat.gastnr
                    AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tguest THEN NEXT.
            END.

            FIND FIRST reservation WHERE reservation.resdat GE fromdate
                AND reservation.resdat LE todate
                AND reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
            FIND FIRST output-list WHERE output-list.gastnr = genstat.gastnr
                AND output-list.resno = genstat.resnr
                AND output-list.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF NOT AVAILABLE output-list THEN DO:
                CREATE output-list.
                ASSIGN output-list.gastnr       = genstat.gastnr
                       output-list.rsvname      = reservation.NAME          /*Add by gerald 23012020*/ 
                       output-list.guestname    = guest.NAME                /*Modified By Gerald 23012020*/        
                       output-list.resno        = genstat.resnr 
                       output-list.reslinnr     = genstat.res-int[1]
                       output-list.cidate       = genstat.res-date[1] 
                       output-list.codate       = genstat.res-date[2]
                       output-list.room-night   = genstat.res-date[2] - genstat.res-date[1] 
                       output-list.rm-night     = genstat.res-date[2] - genstat.res-date[1]  
                       output-list.argt         = genstat.argt
                       output-list.rmrate       = genstat.zipreis 
                       output-list.lodging      = genstat.logis
                       output-list.adult        = genstat.erwachs 
                       output-list.child        = genstat.kind1
                       output-list.infant       = genstat.kind2 
                       output-list.comp         = genstat.gratis
                       output-list.compchild    = genstat.kind3
                       output-list.check-flag   = YES
                       output-list.check-flag1  = YES
                       output-list.check-flag2  = YES
                    .   
                            
                       
                FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE bguest THEN DO: 
                    FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                END.
                    
                FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
                    
                /*ragung*/
                FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                /*end*/
        
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                
                /*FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.*/
                IF AVAILABLE reservation THEN 
                    ASSIGN 
                        output-list.create-date = reservation.resdat
                        output-list.lead        = genstat.res-date[1] - reservation.resdat. 
    
                FIND FIRST res-line WHERE res-line.resnr = genstat.resnr 
                    AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                    AND reslin-queasy.resnr = genstat.resnr 
                    AND reslin-queasy.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy THEN 
                DO: 
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = genstat.zipreis.
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.                      
                END.             
            END.
            ELSE DO:
                ASSIGN
                   output-list.rmrate       = output-list.rmrate + genstat.zipreis 
                   output-list.lodging      = output-list.lodging + genstat.logis.              
            END.
        END.
    
        FOR EACH output-list WHERE output-list.check-flag2  = YES BY output-list.create-date:
            /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
            /* ASSIGN
                output-list.rmrate1      = output-list.rmrate / foreign-curr
                output-list.lodging1     = output-list.lodging / foreign-curr
                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                output-list.avg-lodging  = output-list.lodging / output-list.room-night
             .
            IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
            IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */

            IF foreign-curr NE ? AND foreign-curr NE 0 THEN
            DO:
                ASSIGN
                    output-list.rmrate1      = output-list.rmrate / foreign-curr
                    output-list.lodging1     = output-list.lodging / foreign-curr
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.rmrate1      = 0
                    output-list.lodging1     = 0
                .
            END.

            IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
            DO:
                ASSIGN
                    output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                    output-list.avg-lodging  = output-list.lodging / output-list.room-night
                .
            END.
            ELSE 
            DO:
                ASSIGN
                    output-list.avg-rmrate = output-list.rmrate
                    output-list.avg-lodging  = output-list.lodging
                .
            END.
            /* End Rulita */
    
            ASSIGN
                tot-lead                 = tot-lead + output-list.lead
                tot-lodging              = tot-lodging + output-list.lodging
                tot-lodging1             = tot-lodging1 + output-list.lodging1
                tot-los                  = tot-los + output-list.room-night 
                tot-rmnight              = tot-rmnight + output-list.rm-night 
                /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                tot-avrlodging           = tot-avrlodging + output-list.lodging
                tot-adult                = tot-adult + output-list.adult
                tot-child                = tot-child + output-list.child
                tot-infant               = tot-infant + output-list.infant
                tot-comp                 = tot-comp + output-list.comp
                tot-compchild            = tot-compchild + output-list.compchild.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tot-list THEN DO:
                CREATE tot-list.
                ASSIGN tot-list.gastnr = output-list.gastnr.
            END.
            ASSIGN tot-list.t-lead          = tot-list.t-lead + output-list.lead
                   tot-list.t-los           = tot-list.t-los + output-list.room-night
                   tot-list.t-reserv        = tot-list.t-reserv + 1
                   output-list.check-flag2  = NO
            .
        END.
    
        
        /*forecast*/
        datum2 = datum2 + 1.
        FOR EACH res-line WHERE ((res-line.resstatus LE 13 
            AND res-line.resstatus NE 4
            AND res-line.resstatus NE 8
            AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12 
            AND res-line.active-flag LE 1)) 
            OR (res-line.resstatus = 8 AND res-line.active-flag = 2
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] GT 1 NO-LOCK 
            USE-INDEX gnrank_ix,
            reservation WHERE reservation.resdat GE fromdate 
            AND reservation.resdat LE todate
            AND reservation.resnr = res-line.resnr NO-LOCK
            BY res-line.resnr BY res-line.reslinnr descending:
                
                /* Rulita 130324 | Fixing for serverless */
                FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
 
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:

                    IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                        FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                            AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tguest THEN NEXT.
                    END.
                  
                    FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                        AND output-list.resno = res-line.resnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN DO:
                        CREATE output-list.
                        ASSIGN output-list.gastnr       = res-line.gastnr
                               output-list.rsvname      = reservation.NAME
                               output-list.guestname    = guest.NAME                  
                               output-list.resno        = res-line.resnr 
                               output-list.reslinnr     = res-line.reslinnr
                               output-list.cidate       = res-line.ankunft 
                               output-list.codate       = res-line.abreise
                               output-list.room-night   = res-line.abreise - res-line.ankunft 
                               output-list.rm-night     = res-line.abreise - res-line.ankunft 
                               output-list.argt         = res-line.arrangement           
                               output-list.rmrate       = res-line.zipreis
                               output-list.create-date  = reservation.resdat
                               curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 161224 | Fixing for serverless 299 */
                               output-list.lead         = curr-lead-days
                               output-list.adult        = res-line.erwachs 
                               output-list.child        = res-line.kind1
                               output-list.infant       = res-line.kind2 
                               output-list.comp         = res-line.gratis
                               output-list.compchild    = res-line.l-zuordnung[4]
                               output-list.check-flag   = YES
                               output-list.check-flag1  = YES
                               output-list.check-flag2  = YES
                            . 
        
                        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE bguest THEN DO: 
                            FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                        END.
                        
                        
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE segment THEN output-list.segment = segment.bezeich.

                        /*ragung*/
                        FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                        IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                        /*end*/
        
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO: 
                            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                        END. 
        
                        datum3 = datum2.
                        IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                        datum4 = todate. 
                        IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
        
                        DO ldatum = datum3 TO datum4:
                            pax         = res-line.erwachs. 
                            net-lodg    = 0.
                            curr-i      = curr-i + 1.
        
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                fixed-rate = YES. 
                                IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                                ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                            END.
                             
                            IF NOT fixed-rate THEN DO:
                                FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest-pr THEN 
                                DO: 
                                    contcode = guest-pr.CODE.  
                                    ct = res-line.zimmer-wunsch.  
                                    IF ct MATCHES("*$CODE$*") THEN  
                                    DO:  
                                        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
                                        ASSIGN output-list.contcode = contcode.  /*ragung*/
                                    END.  
                                    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                    ELSE curr-zikatnr = res-line.zikatnr. 
                                    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                                    IF AVAILABLE queasy AND queasy.logi3 THEN 
                                       bill-date = res-line.ankunft. 
                        
                                    IF new-contrate THEN 
                                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                      res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                    ELSE
                                    DO:
                                      RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                        guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                        res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                        res-line.erwachs, res-line.kind1, res-line.kind2,
                                        res-line.reserve-dec, res-line.betriebsnr, 
                                        OUTPUT rm-rate, OUTPUT rate-found).
                                      /* Rulita 130324 | Fixing for serverless */
                                      /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                      IF it-exist THEN rate-found = YES.
                                      IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                    END. 
                                    ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                                END.    
                                w-day = wd-array[WEEKDAY(bill-date)]. 
                                IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                                DO: 
                                  rm-rate = res-line.zipreis. 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day 
                                    NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) = rm-rate 
                                  THEN rack-rate = YES. 
                                END. 
                                ELSE IF rack-rate THEN 
                                DO: 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) > 0 
                                  THEN 
                                    rm-rate = get-rackrate(res-line.erwachs, 
                                      res-line.kind1, res-line.kind2). 
                                END. /* if rack-rate   */ 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.
             /*ragung*/     ELSE DO:
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*end*/
                                END.  
                            END.
        
                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                      OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                      OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                      OUTPUT tot-dinner, OUTPUT tot-other,
                                                      OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                      OUTPUT tot-service).
                             ASSIGN output-list.lodging = output-list.lodging + net-lodg.
                        END.
                        IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                        ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.

                        /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */
                        
                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        ELSE ASSIGN output-list.lodging1 = 0.
                            
                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            ASSIGN
                                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                                output-list.avg-lodging  = output-list.lodging / output-list.room-night
                            .
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .
                        END.
                        /* End Rulita */
                        
                        ASSIGN
                            tot-lead                 = tot-lead + output-list.lead
                            tot-lodging              = tot-lodging + output-list.lodging
                            tot-lodging1             = tot-lodging1 + output-list.lodging1
                            tot-los                  = tot-los + output-list.room-night
                            tot-rmnight              = tot-rmnight + output-list.rm-night
                            /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                            tot-avrlodging           = tot-avrlodging + output-list.lodging
                            tot-adult                = tot-adult + output-list.adult
                            tot-child                = tot-child + output-list.child
                            tot-infant               = tot-infant + output-list.infant
                            tot-comp                 = tot-comp + output-list.comp
                            tot-compchild            = tot-compchild + output-list.compchild
                        .
    
                        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tot-list THEN DO:
                            CREATE tot-list.
                            ASSIGN tot-list.gastnr = output-list.gastnr.
                        END.
                        ASSIGN tot-list.t-lead  = tot-list.t-lead + output-list.lead
                               tot-list.t-los   = tot-list.t-los + output-list.room-night
                               tot-list.t-reserv    = tot-list.t-reserv + 1
                        .
                    END.
                END.                       
            END.
    
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.rsvname BY output-list.create-date BY output-list.gastnr:
            ASSIGN counter = counter + 1.
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate = t-avrgrmrate / t-rmnight
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
                 FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                 IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
            END.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
    
                IF output-list.lead / tot-list.t-lead NE ? THEN 
                    ASSIGN
                        t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                        tot-avrglead          = tot-avrglead + output-list.lead
                 .
    
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
    
    
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild   
                t-avrglos               = t-avrglos    + output-list.avrg-los 
                tot-avrglos             = tot-avrglos   + output-list.avrg-los
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1 = NO
            .
    
        END. 
    END.
    ELSE
    DO:
        /*history*/
        FOR EACH genstat WHERE genstat.res-date[1] GE datum 
              AND genstat.res-date[1] LE datum2
              AND genstat.res-logic[2] 
              AND genstat.zinr NE " " NO-LOCK,
    
            /*FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.NAME GE from-rsv AND guest.NAME LE to-rsv NO-LOCK BY genstat.gastnr:  */        
            FIRST guest WHERE guest.gastnr = genstat.gastnrmember  NO-LOCK BY genstat.gastnr:           /*Modified By Gerald 23012020*/
            
            IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                FIND FIRST tguest WHERE tguest.gastnr = genstat.gastnr
                    AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tguest THEN NEXT.
            END.

            FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
            FIND FIRST output-list WHERE output-list.gastnr = genstat.gastnr
                AND output-list.resno = genstat.resnr
                AND output-list.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF NOT AVAILABLE output-list THEN DO:
                CREATE output-list.
                ASSIGN output-list.gastnr       = genstat.gastnr
                       output-list.rsvname      = reservation.NAME          /*Add by gerald 23012020*/ 
                       output-list.guestname    = guest.NAME                /*Modified By Gerald 23012020*/        
                       output-list.resno        = genstat.resnr 
                       output-list.reslinnr     = genstat.res-int[1]
                       output-list.cidate       = genstat.res-date[1] 
                       output-list.codate       = genstat.res-date[2]
                       output-list.room-night   = genstat.res-date[2] - genstat.res-date[1] 
                       output-list.rm-night     = genstat.res-date[2] - genstat.res-date[1]  
                       output-list.argt         = genstat.argt
                       output-list.rmrate       = genstat.zipreis 
                       output-list.lodging      = genstat.logis
                       output-list.adult        = genstat.erwachs 
                       output-list.child        = genstat.kind1
                       output-list.infant       = genstat.kind2 
                       output-list.comp         = genstat.gratis
                       output-list.compchild    = genstat.kind3
                       output-list.check-flag   = YES
                       output-list.check-flag1  = YES
                       output-list.check-flag2  = YES
                    .   
                            
                       
                FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE bguest THEN DO: 
                    FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                END.
                    
                FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
                
                /*ragung*/
                FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                /*end*/
        
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                
                /*FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.*/
                IF AVAILABLE reservation THEN 
                    ASSIGN 
                        output-list.create-date = reservation.resdat
                        output-list.lead        = genstat.res-date[1] - reservation.resdat. 
    
                FIND FIRST res-line WHERE res-line.resnr = genstat.resnr 
                    AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                    AND reslin-queasy.resnr = genstat.resnr 
                    AND reslin-queasy.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy THEN 
                DO: 
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = genstat.zipreis.
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.                      
                END.             
            END.
            ELSE DO:
                ASSIGN
                   output-list.rmrate       = output-list.rmrate + genstat.zipreis 
                   output-list.lodging      = output-list.lodging + genstat.logis.              
            END.
        END.
    
        FOR EACH output-list WHERE output-list.check-flag2  = YES:
            /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
            /* ASSIGN
                output-list.rmrate1      = output-list.rmrate / foreign-curr
                output-list.lodging1     = output-list.lodging / foreign-curr
                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                output-list.avg-lodging  = output-list.lodging / output-list.room-night
             .
            IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
            IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */

            IF foreign-curr NE ? AND foreign-curr NE 0 THEN
            DO:
                ASSIGN
                    output-list.rmrate1      = output-list.rmrate / foreign-curr
                    output-list.lodging1     = output-list.lodging / foreign-curr
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.rmrate1      = 0
                    output-list.lodging1     = 0
                .
            END.

            IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
            DO:
                ASSIGN
                    output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                    output-list.avg-lodging  = output-list.lodging / output-list.room-night
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.avg-rmrate = output-list.rmrate
                    output-list.avg-lodging  = output-list.lodging
                .
            END.
            /* End Rulita */
    
            ASSIGN
                tot-lead                 = tot-lead + output-list.lead
                tot-lodging              = tot-lodging + output-list.lodging
                tot-lodging1             = tot-lodging1 + output-list.lodging1
                tot-los                  = tot-los + output-list.room-night 
                tot-rmnight              = tot-rmnight + output-list.rm-night 
                /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                tot-avrlodging           = tot-avrlodging + output-list.lodging
                tot-adult                = tot-adult + output-list.adult
                tot-child                = tot-child + output-list.child
                tot-infant               = tot-infant + output-list.infant
                tot-comp                 = tot-comp + output-list.comp
                tot-compchild            = tot-compchild + output-list.compchild.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tot-list THEN DO:
                CREATE tot-list.
                ASSIGN tot-list.gastnr = output-list.gastnr.
            END.
            ASSIGN tot-list.t-lead          = tot-list.t-lead + output-list.lead
                   tot-list.t-los           = tot-list.t-los + output-list.room-night
                   tot-list.t-reserv        = tot-list.t-reserv + 1
                   output-list.check-flag2  = NO
            .
        END.
    
        
        /*forecast*/
        datum2 = datum2 + 1.
        IF todate GE ci-date THEN DO:
        FOR EACH res-line WHERE ((res-line.resstatus LE 13 
            AND res-line.resstatus NE 4
            AND res-line.resstatus NE 8
            AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12 
            AND res-line.active-flag LE 1 
            AND res-line.ankunft GE fromdate
            AND res-line.ankunft LE todate)) OR (res-line.resstatus = 8 AND res-line.active-flag = 2
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] GT 1 NO-LOCK 
            USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending:
                
                /* Rulita 130324 | Fixing for serverless */
                FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
 
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember
                    NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:

                    IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                        FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                            AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tguest THEN NEXT.
                    END.

                    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
                    FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                        AND output-list.resno = res-line.resnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN DO:
                        CREATE output-list.
                        ASSIGN output-list.gastnr       = res-line.gastnr
                               output-list.rsvname      = reservation.NAME
                               output-list.guestname    = guest.NAME                  
                               output-list.resno        = res-line.resnr 
                               output-list.reslinnr     = res-line.reslinnr
                               output-list.cidate       = res-line.ankunft 
                               output-list.codate       = res-line.abreise
                               output-list.room-night   = res-line.abreise - res-line.ankunft 
                               output-list.rm-night     = res-line.abreise - res-line.ankunft 
                               output-list.argt         = res-line.arrangement           
                               output-list.rmrate       = res-line.zipreis
                               output-list.create-date  = reservation.resdat
                               curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 161224 | Fixing for serverless 299 */
                               output-list.lead         = curr-lead-days
                               output-list.adult        = res-line.erwachs 
                               output-list.child        = res-line.kind1
                               output-list.infant       = res-line.kind2 
                               output-list.comp         = res-line.gratis
                               output-list.compchild    = res-line.l-zuordnung[4]
                               output-list.check-flag   = YES
                               output-list.check-flag1  = YES
                               output-list.check-flag2  = YES
                            . 
        
                        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE bguest THEN DO: 
                            FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                        END.
                        
                        /*ragung*/
                        FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                        IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                        /*end*/

                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO: 
                            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                        END. 
        
                        datum3 = datum2.
                        IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                        datum4 = todate. 
                        IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
        
                        DO ldatum = datum3 TO datum4:
                            pax         = res-line.erwachs. 
                            net-lodg    = 0.
                            curr-i      = curr-i + 1.
        
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                fixed-rate = YES. 
                                IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                                ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                            END.
                             
                            IF NOT fixed-rate THEN DO:
                                FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest-pr THEN 
                                DO: 
                                    contcode = guest-pr.CODE.  
                                    ct = res-line.zimmer-wunsch.  
                                    IF ct MATCHES("*$CODE$*") THEN  
                                    DO:  
                                        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
                                        ASSIGN output-list.contcode = contcode.  /*ragung*/
                                    END.  
                                    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                    ELSE curr-zikatnr = res-line.zikatnr. 
                                    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                                    IF AVAILABLE queasy AND queasy.logi3 THEN 
                                       bill-date = res-line.ankunft. 
                        
                                    IF new-contrate THEN 
                                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                      res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                    ELSE
                                    DO:
                                      RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                        guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                        res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                        res-line.erwachs, res-line.kind1, res-line.kind2,
                                        res-line.reserve-dec, res-line.betriebsnr, 
                                        OUTPUT rm-rate, OUTPUT rate-found).
                                      /* Rulita 130324 | Fixing for serverless */
                                      /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                      IF it-exist THEN rate-found = YES.
                                      IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                    END. 
                                    ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                                END.    
                                w-day = wd-array[WEEKDAY(bill-date)]. 
                                IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                                DO: 
                                  rm-rate = res-line.zipreis. 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day 
                                    NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) = rm-rate 
                                  THEN rack-rate = YES. 
                                END. 
                                ELSE IF rack-rate THEN 
                                DO: 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) > 0 
                                  THEN 
                                    rm-rate = get-rackrate(res-line.erwachs, 
                                      res-line.kind1, res-line.kind2). 
                                END. /* if rack-rate   */ 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.
             /*ragung*/     ELSE DO:
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*end*/
                                END.  
                            END.
        
                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                      OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                      OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                      OUTPUT tot-dinner, OUTPUT tot-other,
                                                      OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                      OUTPUT tot-service).
                             ASSIGN output-list.lodging = output-list.lodging + net-lodg.
                        END.
                        IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                        ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.

                        /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging.*/
                        
                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        ELSE ASSIGN output-list.lodging1 = 0.
                            
                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            ASSIGN
                                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                                output-list.avg-lodging  = output-list.lodging / output-list.room-night
                            .
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .
                        END.
                        /* End Rulita */
                        
                        ASSIGN
                            tot-lead                 = tot-lead + output-list.lead
                            tot-lodging              = tot-lodging + output-list.lodging
                            tot-lodging1             = tot-lodging1 + output-list.lodging1
                            tot-los                  = tot-los + output-list.room-night
                            tot-rmnight              = tot-rmnight + output-list.rm-night
                            /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                            tot-avrlodging           = tot-avrlodging + output-list.lodging
                            tot-adult                = tot-adult + output-list.adult
                            tot-child                = tot-child + output-list.child
                            tot-infant               = tot-infant + output-list.infant
                            tot-comp                 = tot-comp + output-list.comp
                            tot-compchild            = tot-compchild + output-list.compchild
                        .
    
                        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tot-list THEN DO:
                            CREATE tot-list.
                            ASSIGN tot-list.gastnr = output-list.gastnr.
                        END.
                        ASSIGN tot-list.t-lead  = tot-list.t-lead + output-list.lead
                               tot-list.t-los   = tot-list.t-los + output-list.room-night
                               tot-list.t-reserv    = tot-list.t-reserv + 1
                        .
                    END.
                END.                       
            END.
        END.
    
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.gastnr:
            ASSIGN counter = counter + 1.
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate = t-avrgrmrate / t-rmnight
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
                 FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                 IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
            END.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
    
                IF output-list.lead / tot-list.t-lead NE ? THEN 
                    ASSIGN
                        t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                        tot-avrglead          = tot-avrglead + output-list.lead
                 .
    
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
    
    
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild   
                t-avrglos               = t-avrglos    + output-list.avrg-los 
                tot-avrglos             = tot-avrglos   + output-list.avrg-los
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1 = NO
            .
        END.
    END.

    CREATE output-list.
    ASSIGN 
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = t-gastnr
        output-list.rsvname     = "T O T A L"
        output-list.lead        = t-lead
        output-list.lodging     = t-lodging
        output-list.lodging1    = t-lodging1
        output-list.room-night  = t-los
        output-list.rm-night    = t-rmnight
        output-list.avg-lodging = t-avrlodging / t-rmnight
        output-list.adult       = t-adult 
        output-list.child       = t-child 
        output-list.infant      = t-infant 
        output-list.comp        = t-comp 
        output-list.compchild   = t-compchild 
        output-list.avrg-lead   = t-avrglead
        output-list.avrg-los    = t-avrglos
        output-list.rmrate      = t-rmrate                
        output-list.rmrate1     = t-rmrate1               
        output-list.avg-rmrate  = t-avrgrmrate / t-rmnight
        output-list.check-flag   = YES
    .

    FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE tot-list THEN ASSIGN output-list.tot-reserv = tot-list.t-reserv.

    FOR EACH tot-list NO-LOCK:
        ASSIGN tot-rsv = tot-rsv + tot-list.t-reserv.
    END.
    
    CREATE output-list.
    ASSIGN 
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = 999999999
        output-list.rsvname     = "Grand T O T A L"
        output-list.lead        = tot-lead
        output-list.lodging     = tot-lodging
        output-list.lodging1    = tot-lodging1
        output-list.room-night  = tot-los
        output-list.rm-night    = tot-rmnight
        output-list.avg-lodging = tot-avrlodging / tot-rmnight
        output-list.adult       = tot-adult 
        output-list.child       = tot-child 
        output-list.infant      = tot-infant 
        output-list.comp        = tot-comp 
        output-list.compchild   = tot-compchild 
        output-list.avrg-lead   = tot-avrglead / tot-rsv
        output-list.avrg-los    = tot-avrglos / tot-rsv
        output-list.rmrate      = tot-rmrate                
        output-list.rmrate1     = tot-rmrate1               
        output-list.avg-rmrate  = tot-avrgrmrate / tot-rmnight
        output-list.tot-reserv  = tot-rsv
        output-list.check-flag   = YES
      . 
END.

PROCEDURE create-browse-exclude1:
    DEFINE VARIABLE datum            AS DATE NO-UNDO.
    DEFINE VARIABLE datum2           AS DATE NO-UNDO.
    DEFINE VARIABLE datum3           AS DATE NO-UNDO.
    DEFINE VARIABLE datum4           AS DATE NO-UNDO.
    DEFINE VARIABLE ldatum           AS DATE NO-UNDO.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.

    DEFINE VARIABLE tot-lead         AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrlodging   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-los          AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-rmnight      AS INTEGER INITIAL 0.

    DEFINE VARIABLE tot-adult         AS INTEGER.
    DEFINE VARIABLE tot-child         AS INTEGER.
    DEFINE VARIABLE tot-infant        AS INTEGER.
    DEFINE VARIABLE tot-comp          AS INTEGER.
    DEFINE VARIABLE tot-compchild     AS INTEGER.

    DEFINE VARIABLE t-gastnr        AS INTEGER.
    DEFINE VARIABLE t-lead          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging1      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrlodging    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglead      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglos       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-los           AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-rmnight       AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-adult         AS INTEGER.
    DEFINE VARIABLE t-child         AS INTEGER.
    DEFINE VARIABLE t-infant        AS INTEGER.
    DEFINE VARIABLE t-comp          AS INTEGER.
    DEFINE VARIABLE t-compchild     AS INTEGER.
    DEFINE VARIABLE tot-avrglead    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrglos     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate1       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrgrmrate    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrgrmrate  AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rsv         AS DECIMAL INITIAL 0.

    IF check-cdate THEN
    DO:    
        FOR EACH res-line WHERE (res-line.active-flag LE 1 
            AND res-line.resstatus LE 13 
            AND res-line.resstatus NE 4 
            AND res-line.resstatus NE 12) 
            OR (res-line.active-flag = 2 AND res-line.resstatus = 8
             AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] GT 1 
            USE-INDEX gnrank_ix NO-LOCK,
            FIRST reservation WHERE reservation.resdat GE fromdate
            AND reservation.resdat LE todate
            AND reservation.resnr = res-line.resnr NO-LOCK BY res-line.resnr:
                
                ASSIGN
                 curr-i        = 0
                 tot-breakfast = 0
                 tot-lunch     = 0
                 tot-dinner    = 0
                 tot-other     = 0
                 ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*")
                 kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").

                 /* ITA 09/04/2025 | Fixing for serverless */
                FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
                
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:

                    IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                        FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                            AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tguest THEN NEXT.
                    END.

                    FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                        AND output-list.resno = res-line.resnr
                        AND output-list.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN DO:
                        CREATE output-list.
                        ASSIGN output-list.gastnr       = res-line.gastnr
                               output-list.rsvname      = reservation.NAME          /*Modified by gerald 23012020*/ 
                               output-list.guestname    = guest.NAME                /*Add By Gerald 23012020*/        
                               output-list.resno        = res-line.resnr
                               output-list.reslinnr     = res-line.reslinnr
                               output-list.cidate       = res-line.ankunft 
                               output-list.codate       = res-line.abreise
                               output-list.room-night   = res-line.abreise - res-line.ankunft 
                               output-list.rm-night     = res-line.abreise - res-line.ankunft 
                               output-list.argt         = res-line.arrangement           
                               /*output-list.rmrate       = res-line.zipreis */
                               output-list.create-date  = reservation.resdat
                               curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 161224 | Fixing for serverless 299 */
                               output-list.lead         = curr-lead-days
                               output-list.adult        = res-line.erwachs 
                               output-list.child        = res-line.kind1
                               output-list.infant       = res-line.kind2 
                               output-list.comp         = res-line.gratis
                               output-list.compchild    = res-line.l-zuordnung[4]
                               output-list.check-flag   = YES
                               output-list.check-flag1  = YES
                               output-list.check-flag2  = YES
                            . 
        
                        
                        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE bguest THEN DO: 
                            FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.                       
                        END.

                        /*ragung*/
                        FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                        IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                        /*end*/
                        
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO: 
                            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                        END. 
                        
                        datum3 = fromdate.
                        IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                        datum4 = todate. 
                        IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
                        
                        tmp-date = res-line.abreise - 1.                               /* Rulita 071124 | Fixing date calculate for serverless program */
                        /*DO ldatum = datum3 TO datum4:*/
                        /* DO ldatum = res-line.ankunft TO res-line.abreise - 1: */     /* Rulita 071124 | Fixing date calculate for serverless program */
                        DO ldatum = res-line.ankunft TO tmp-date:       
                            pax         = res-line.erwachs. 
                            net-lodg    = 0.
                            curr-i      = curr-i + 1.
    
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                fixed-rate = YES. 
                                IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                                ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                            END.
                             
                            IF NOT fixed-rate THEN DO:
                                FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest-pr THEN 
                                DO: 
                                    contcode = guest-pr.CODE.  
                                    ct = res-line.zimmer-wunsch.  
                                    IF ct MATCHES("*$CODE$*") THEN  
                                    DO:  
                                        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1). 
                                        ASSIGN output-list.contcode = contcode.  /*ragung*/
                                    END.  
                                    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                    ELSE curr-zikatnr = res-line.zikatnr. 
                                    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                                    IF AVAILABLE queasy AND queasy.logi3 THEN 
                                       bill-date = res-line.ankunft. 
                        
                                    IF new-contrate THEN 
                                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                      res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                    ELSE
                                    DO:
                                      RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                        guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                        res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                        res-line.erwachs, res-line.kind1, res-line.kind2,
                                        res-line.reserve-dec, res-line.betriebsnr, 
                                        OUTPUT rm-rate, OUTPUT rate-found).
                                      /* Rulita 130324 | Fixing for serverless */
                                      /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                      IF it-exist THEN rate-found = YES.
                                      IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                    END. 
                                    ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                                END.    
                                w-day = wd-array[WEEKDAY(bill-date)]. 
                                IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                                DO: 
                                  rm-rate = res-line.zipreis. 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day 
                                    NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) = rm-rate 
                                  THEN rack-rate = YES. 
                                END. 
                                ELSE IF rack-rate THEN 
                                DO: 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) > 0 
                                  THEN 
                                    rm-rate = get-rackrate(res-line.erwachs, 
                                      res-line.kind1, res-line.kind2). 
                                END. /* if rack-rate   */ 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.
             /*ragung*/     ELSE DO:
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*end*/
                                END.  
                            END.
    
                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                      OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                      OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                      OUTPUT tot-dinner, OUTPUT tot-other,
                                                      OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                      OUTPUT tot-service).
                             ASSIGN output-list.lodging = output-list.lodging + net-lodg.                         
                        END.
                        
                        IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                        ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.

                        ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging.

                        /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging.*/
                        
                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        ELSE ASSIGN output-list.lodging1 = 0.
                            
                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            ASSIGN
                                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                                output-list.avg-lodging  = output-list.lodging / output-list.room-night
                            .
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .

                        END.
                        /* End Rulita */

                        ASSIGN
                            tot-lead                 = tot-lead + output-list.lead
                            tot-lodging              = tot-lodging + output-list.lodging
                            tot-lodging1             = tot-lodging1 + output-list.lodging1
                            tot-los                  = tot-los + output-list.room-night
                            tot-rmnight              = tot-rmnight + output-list.rm-night
                            /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                            tot-avrlodging           = tot-avrlodging + output-list.lodging
                            tot-adult                = tot-adult + output-list.adult
                            tot-child                = tot-child + output-list.child
                            tot-infant               = tot-infant + output-list.infant
                            tot-comp                 = tot-comp + output-list.comp
                            tot-compchild            = tot-compchild + output-list.compchild.
    
                        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tot-list THEN DO:
                            CREATE tot-list.
                            ASSIGN tot-list.gastnr = output-list.gastnr.
                        END.
                        ASSIGN tot-list.t-lead  = tot-list.t-lead + output-list.lead
                               tot-list.t-los   = tot-list.t-los + output-list.room-night
                               tot-list.t-reserv    = tot-list.t-reserv + 1
                        .
                    END.
                END.              
        END.
    
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.create-date BY output-list.gastnr:
            ASSIGN counter = counter + 1.
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate = t-avrgrmrate / t-rmnight
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
                 FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                 IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
            END.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
                
                /* Rulita 180225 | Fixing serverless issue git 100 */
                IF output-list.lead NE 0 AND output-list.lead NE ? THEN 
                DO:
                    IF output-list.lead / tot-list.t-lead NE ? THEN 
                        ASSIGN
                            t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                            tot-avrglead          = tot-avrglead + output-list.lead
                    .
                END. 
    
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
    
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild    
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1 = NO
            .
    
        END.
    END.
    ELSE
    DO:    
        FOR EACH res-line WHERE (res-line.active-flag LE 1 
            AND res-line.resstatus LE 13 
            AND res-line.resstatus NE 4 
            AND res-line.resstatus NE 12
            AND res-line.ankunft GE fromdate
            AND res-line.ankunft LE todate) OR 
            (res-line.active-flag = 2 AND res-line.resstatus = 8
             AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] GT 1 
            USE-INDEX gnrank_ix NO-LOCK BY res-line.resnr:
                
                ASSIGN
                 curr-i        = 0
                 tot-breakfast = 0
                 tot-lunch     = 0
                 tot-dinner    = 0
                 tot-other     = 0
                 ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*")
                 kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").

                 /* ITA 09/04/2025 | Fixing for serverless */
                FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
                
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN DO:

                    IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                        FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                            AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tguest THEN NEXT.
                    END.

                    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
                    FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                        AND output-list.resno = res-line.resnr
                        AND output-list.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN DO:
                        CREATE output-list.
                        ASSIGN output-list.gastnr       = res-line.gastnr
                               output-list.rsvname      = reservation.NAME          /*Modified by gerald 23012020*/ 
                               output-list.guestname    = guest.NAME                /*Add By Gerald 23012020*/        
                               output-list.resno        = res-line.resnr
                               output-list.reslinnr     = res-line.reslinnr
                               output-list.cidate       = res-line.ankunft 
                               output-list.codate       = res-line.abreise
                               output-list.room-night   = res-line.abreise - res-line.ankunft 
                               output-list.rm-night     = res-line.abreise - res-line.ankunft 
                               output-list.argt         = res-line.arrangement           
                               /*output-list.rmrate       = res-line.zipreis */
                               output-list.create-date  = reservation.resdat
                               curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 161224 | Fixing for serverless 299 */
                               output-list.lead         = curr-lead-days
                               output-list.adult        = res-line.erwachs 
                               output-list.child        = res-line.kind1
                               output-list.infant       = res-line.kind2 
                               output-list.comp         = res-line.gratis
                               output-list.compchild    = res-line.l-zuordnung[4]
                               output-list.check-flag   = YES
                               output-list.check-flag1  = YES
                               output-list.check-flag2  = YES
                            . 
        
                        
                        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE bguest THEN DO: 
                            FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.                       
                        END.
                        
                        /*ragung*/
                        FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                        IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                        /*end*/

                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO: 
                            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                        END. 
                        
                        datum3 = fromdate.
                        IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                        datum4 = todate. 
                        IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
                        
                        tmp-date = res-line.abreise - 1.                               /* Rulita 071124 | Fixing date calculate for serverless program */
                        /*DO ldatum = datum3 TO datum4:*/
                        /* DO ldatum = res-line.ankunft TO res-line.abreise - 1: */     /* Rulita 071124 | Fixing date calculate for serverless program */
                        DO ldatum = res-line.ankunft TO tmp-date:
                            pax         = res-line.erwachs. 
                            net-lodg    = 0.
                            curr-i      = curr-i + 1.
    
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                fixed-rate = YES. 
                                IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                                ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                            END.
                             
                            IF NOT fixed-rate THEN DO:
                                FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest-pr THEN 
                                DO: 
                                    contcode = guest-pr.CODE.  
                                    ct = res-line.zimmer-wunsch.  
                                    IF ct MATCHES("*$CODE$*") THEN  
                                    DO:  
                                        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                        ASSIGN output-list.contcode = contcode.  /*ragung*/
                                    END.  
                                    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                    ELSE curr-zikatnr = res-line.zikatnr. 
                                    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                                    IF AVAILABLE queasy AND queasy.logi3 THEN 
                                       bill-date = res-line.ankunft. 
                        
                                    IF new-contrate THEN 
                                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                      res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                    ELSE
                                    DO:
                                      RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                        guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                        res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                        res-line.erwachs, res-line.kind1, res-line.kind2,
                                        res-line.reserve-dec, res-line.betriebsnr, 
                                        OUTPUT rm-rate, OUTPUT rate-found).
                                      /* Rulita 130324 | Fixing for serverless */
                                      /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                      IF it-exist THEN rate-found = YES.
                                      IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                    END. 
                                    ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                                END.    
                                w-day = wd-array[WEEKDAY(bill-date)]. 
                                IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                                DO: 
                                  rm-rate = res-line.zipreis. 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day 
                                    NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) = rm-rate 
                                  THEN rack-rate = YES. 
                                END. 
                                ELSE IF rack-rate THEN 
                                DO: 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) > 0 
                                  THEN 
                                    rm-rate = get-rackrate(res-line.erwachs, 
                                      res-line.kind1, res-line.kind2). 
                                END. /* if rack-rate   */ 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.
             /*ragung*/     ELSE DO:
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*end*/
                                END.  
                            END.

                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                      OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                      OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                      OUTPUT tot-dinner, OUTPUT tot-other,
                                                      OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                      OUTPUT tot-service).
                             ASSIGN output-list.lodging = output-list.lodging + net-lodg.                         
                        END.
                        
                        IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                        ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.

                        /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging.*/
                        
                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        ELSE ASSIGN output-list.lodging1 = 0.
                            
                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            ASSIGN
                                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                                output-list.avg-lodging  = output-list.lodging / output-list.room-night
                            .
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .

                        END.
                        /* End Rulita */

                        ASSIGN
                            tot-lead                 = tot-lead + output-list.lead
                            tot-lodging              = tot-lodging + output-list.lodging
                            tot-lodging1             = tot-lodging1 + output-list.lodging1
                            tot-los                  = tot-los + output-list.room-night
                            tot-rmnight              = tot-rmnight + output-list.rm-night
                            /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                            tot-avrlodging           = tot-avrlodging + output-list.lodging
                            tot-adult                = tot-adult + output-list.adult
                            tot-child                = tot-child + output-list.child
                            tot-infant               = tot-infant + output-list.infant
                            tot-comp                 = tot-comp + output-list.comp
                            tot-compchild            = tot-compchild + output-list.compchild.
    
                        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tot-list THEN DO:
                            CREATE tot-list.
                            ASSIGN tot-list.gastnr = output-list.gastnr.
                        END.
                        ASSIGN tot-list.t-lead  = tot-list.t-lead + output-list.lead
                               tot-list.t-los   = tot-list.t-los + output-list.room-night
                               tot-list.t-reserv    = tot-list.t-reserv + 1
                        .
                    END.
                END.              
        END.
    
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.gastnr:
            ASSIGN counter = counter + 1.
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate = t-avrgrmrate / t-rmnight
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
                 FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                 IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
            END.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
    
                IF output-list.lead / tot-list.t-lead NE ? THEN 
                    ASSIGN
                        t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                        tot-avrglead          = tot-avrglead + output-list.lead
                 .
    
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
    
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild    
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1 = NO
            .
        END. 
    END.

    
    
    CREATE output-list.
    ASSIGN 
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = t-gastnr
        output-list.rsvname     = "T O T A L"
        output-list.lead        = t-lead
        output-list.lodging     = t-lodging
        output-list.lodging1    = t-lodging1
        output-list.room-night  = t-los
        output-list.rm-night    = t-rmnight
        output-list.avg-lodging = t-avrlodging / t-rmnight
        output-list.adult       = t-adult 
        output-list.child       = t-child 
        output-list.infant      = t-infant 
        output-list.comp        = t-comp 
        output-list.compchild   = t-compchild 
        output-list.avrg-lead   = t-avrglead
        output-list.avrg-los    = t-avrglos   
        output-list.rmrate      = t-rmrate                
        output-list.rmrate1     = t-rmrate1               
        output-list.avg-rmrate  = t-avrgrmrate / t-rmnight
        output-list.check-flag   = YES
    .

    FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE tot-list THEN ASSIGN output-list.tot-reserv = tot-list.t-reserv.

    FOR EACH tot-list NO-LOCK:
        ASSIGN tot-rsv = tot-rsv + tot-list.t-reserv.
    END.
    
    CREATE output-list.                         /*ini titik*/
    ASSIGN 
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = 999999999
        output-list.rsvname     = "Grand T O T A L"
        output-list.lead        = tot-lead
        output-list.lodging     = tot-lodging
        output-list.lodging1    = tot-lodging1
        output-list.room-night  = tot-los
        output-list.rm-night    = tot-rmnight
        output-list.avg-lodging = tot-avrlodging / tot-rmnight
        output-list.adult       = tot-adult 
        output-list.child       = tot-child 
        output-list.infant      = tot-infant 
        output-list.comp        = tot-comp 
        output-list.compchild   = tot-compchild
        output-list.avrg-lead   = tot-avrglead / tot-rsv
        output-list.avrg-los    = tot-avrglos / tot-rsv
        output-list.rmrate      = tot-rmrate                
        output-list.rmrate1     = tot-rmrate1               
        output-list.avg-rmrate  = tot-avrgrmrate / tot-rmnight
        output-list.tot-reserv  = tot-rsv
        output-list.check-flag   = YES
    . 
END.


PROCEDURE create-browse-rm-sharer:
    DEFINE VARIABLE datum            AS DATE NO-UNDO.
    DEFINE VARIABLE datum2           AS DATE NO-UNDO.
    DEFINE VARIABLE datum3           AS DATE NO-UNDO.
    DEFINE VARIABLE datum4           AS DATE NO-UNDO.
    DEFINE VARIABLE ldatum           AS DATE NO-UNDO.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.
    
    DEFINE VARIABLE tot-lead         AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrlodging   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-los          AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-rmnight      AS INTEGER INITIAL 0.

    DEFINE VARIABLE tot-adult         AS INTEGER.
    DEFINE VARIABLE tot-child         AS INTEGER.
    DEFINE VARIABLE tot-infant        AS INTEGER.
    DEFINE VARIABLE tot-comp          AS INTEGER.
    DEFINE VARIABLE tot-compchild     AS INTEGER.

    DEFINE VARIABLE t-gastnr        AS INTEGER.
    DEFINE VARIABLE t-lead          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging1      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrlodging    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglead      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglos       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-los           AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-rmnight       AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-adult         AS INTEGER.
    DEFINE VARIABLE t-child         AS INTEGER.
    DEFINE VARIABLE t-infant        AS INTEGER.
    DEFINE VARIABLE t-comp          AS INTEGER.
    DEFINE VARIABLE t-compchild     AS INTEGER.
    DEFINE VARIABLE tot-avrglead    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrglos     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate1       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrgrmrate    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrgrmrate  AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rsv         AS DECIMAL INITIAL 0.


    ASSIGN datum = fromdate.
    IF todate LT (ci-date - 1) THEN datum2 = todate.
    ELSE datum2 = ci-date - 1.

    IF check-cdate THEN
    DO:
        /*history*/
        FOR EACH genstat WHERE genstat.res-date[1] GE datum 
              AND genstat.res-date[1] LE datum2
              AND genstat.res-logic[2] 
              AND genstat.zinr NE " " AND genstat.resstatus NE 13 NO-LOCK,
            /*FIRST guest WHERE guest.gastnr = genstat.gastnr
                AND guest.NAME GE from-rsv AND guest.NAME LE to-rsv NO-LOCK BY genstat.gastnr:*/
            FIRST reservation WHERE reservation.resdat GE fromdate
                AND reservation.resdat LE todate
                AND reservation.gastnr = genstat.gastnr NO-LOCK,
            FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK BY genstat.gastnr:       /*Modified By Gerald 23012020*/

            IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                FIND FIRST tguest WHERE tguest.gastnr = genstat.gastnr
                    AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tguest THEN NEXT.
            END.

            FIND FIRST output-list WHERE output-list.gastnr = genstat.gastnr
                AND output-list.resno = genstat.resnr
                AND output-list.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF NOT AVAILABLE output-list THEN DO:
                CREATE output-list.
                ASSIGN output-list.gastnr       = genstat.gastnr
                       output-list.rsvname      = reservation.NAME              /*Modified by gerald 23012020*/ 
                       output-list.guestname    = guest.NAME                    /*Add By Gerald 23012020*/      
                       output-list.resno        = genstat.resnr 
                       output-list.reslinnr     = genstat.res-int[1]
                       output-list.cidate       = genstat.res-date[1] 
                       output-list.codate       = genstat.res-date[2]
                       output-list.room-night   = genstat.res-date[2] - genstat.res-date[1] 
                       output-list.rm-night     = genstat.res-date[2] - genstat.res-date[1]  
                       output-list.argt         = genstat.argt
                       output-list.rmrate       = genstat.zipreis 
                       output-list.lodging      = genstat.logis
                       output-list.adult        = genstat.erwachs 
                       output-list.child        = genstat.kind1
                       output-list.infant       = genstat.kind2 
                       output-list.comp         = genstat.gratis
                       output-list.compchild    = genstat.kind3
                       output-list.check-flag   = YES
                       output-list.check-flag1  = YES
                       output-list.check-flag2  = YES
                    .   
                            
                       
                FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE bguest THEN DO: 
                    FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                END.
                    
                FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segment = segment.bezeich.

                /*ragung*/
                FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                /*end*/
        
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                
                /*FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.*/
                IF AVAILABLE reservation THEN 
                    ASSIGN 
                        output-list.create-date = reservation.resdat
                        output-list.lead        = genstat.res-date[1] - reservation.resdat. 
    
                FIND FIRST res-line WHERE res-line.resnr = genstat.resnr 
                    AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                    AND reslin-queasy.resnr = genstat.resnr 
                    AND reslin-queasy.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy THEN 
                DO: 
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = genstat.zipreis.
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.                      
                END.             
            END.
            ELSE DO:
                ASSIGN
                   output-list.rmrate       = output-list.rmrate + genstat.zipreis 
                   output-list.lodging      = output-list.lodging + genstat.logis.              
            END.
        END.
    
        FOR EACH output-list WHERE output-list.check-flag2  = YES BY output-list.create-date:
            /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
            /* ASSIGN
                output-list.rmrate1      = output-list.rmrate / foreign-curr
                output-list.lodging1     = output-list.lodging / foreign-curr
                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                output-list.avg-lodging  = output-list.lodging / output-list.room-night
             .
            IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
            IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */

            IF foreign-curr NE ? AND foreign-curr NE 0 THEN
            DO:
                ASSIGN
                    output-list.rmrate1      = output-list.rmrate / foreign-curr
                    output-list.lodging1     = output-list.lodging / foreign-curr
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.rmrate1      = 0
                    output-list.lodging1     = 0
                .
            END.

            IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
            DO:
                ASSIGN
                    output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                    output-list.avg-lodging  = output-list.lodging / output-list.room-night
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.avg-rmrate = output-list.rmrate
                    output-list.avg-lodging  = output-list.lodging
                .
            END.
            /* End Rulita */

            ASSIGN
                tot-lead                 = tot-lead + output-list.lead
                tot-lodging              = tot-lodging + output-list.lodging
                tot-lodging1             = tot-lodging1 + output-list.lodging1
                tot-los                  = tot-los + output-list.room-night 
                tot-rmnight              = tot-rmnight + output-list.rm-night 
                /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                tot-avrlodging           = tot-avrlodging + output-list.lodging
                tot-adult                = tot-adult + output-list.adult
                tot-child                = tot-child + output-list.child
                tot-infant               = tot-infant + output-list.infant
                tot-comp                 = tot-comp + output-list.comp
                tot-compchild            = tot-compchild + output-list.compchild.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tot-list THEN DO:
                CREATE tot-list.
                ASSIGN tot-list.gastnr = output-list.gastnr.
            END.
            ASSIGN tot-list.t-lead          = tot-list.t-lead + output-list.lead
                   tot-list.t-los           = tot-list.t-los + output-list.room-night
                   tot-list.t-reserv        = tot-list.t-reserv + 1
                   output-list.check-flag2  = NO
            .
        END.
    
        
        /*forecast*/
        datum2 = datum2 + 1.
        FOR EACH res-line WHERE ((res-line.resstatus NE 11
            AND res-line.resstatus NE 13
            AND res-line.active-flag LE 1 )) 
            OR (res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND res-line.active-flag = 2
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK 
            USE-INDEX gnrank_ix,
            FIRST reservation WHERE reservation.resdat GE fromdate
                AND reservation.resdat LE todate
                AND reservation.resnr = res-line.resnr NO-LOCK 
            BY res-line.resnr BY res-line.reslinnr descending:
                
                /* Rulita 130324 | Fixing for serverless */
                FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
 
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember                     /*Modified by gerald 23012020*/ 
                    NO-LOCK NO-ERROR.             
                IF AVAILABLE guest THEN DO:

                    IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                        FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                            AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tguest THEN NEXT.
                    END.

                    FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                        AND output-list.resno = res-line.resnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN DO:
                        CREATE output-list.
                        ASSIGN output-list.gastnr       = res-line.gastnr
                               output-list.rsvname      = reservation.NAME      /*Add by gerald 23012020*/ 
                               output-list.guestname    = guest.NAME            /*Modified By Gerald 23012020*/            
                               output-list.resno        = res-line.resnr 
                               output-list.reslinnr     = res-line.reslinnr
                               output-list.cidate       = res-line.ankunft 
                               output-list.codate       = res-line.abreise
                               output-list.room-night   = res-line.abreise - res-line.ankunft 
                               output-list.rm-night     = res-line.abreise - res-line.ankunft 
                               output-list.argt         = res-line.arrangement           
                               output-list.rmrate       = res-line.zipreis
                               output-list.create-date  = reservation.resdat
                               curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 201124 | Fixing for serverless */
                               output-list.lead         = curr-lead-days
                               output-list.adult        = res-line.erwachs 
                               output-list.child        = res-line.kind1
                               output-list.infant       = res-line.kind2 
                               output-list.comp         = res-line.gratis
                               output-list.compchild    = res-line.l-zuordnung[4]
                               output-list.check-flag   = YES
                               output-list.check-flag1  = YES
                               output-list.check-flag2  = YES
                            . 
        
                        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE bguest THEN DO: 
                            FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                        END.
                        
                        /*ragung*/
                        FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                        IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                        /*end*/
                        
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO: 
                            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                        END. 
        
                        datum3 = datum2.
                        IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                        datum4 = todate. 
                        IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
        
                        DO ldatum = datum3 TO datum4:
                            pax         = res-line.erwachs. 
                            net-lodg    = 0.
                            curr-i      = curr-i + 1.
        
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                fixed-rate = YES. 
                                IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                                ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                            END.
                             
                            IF NOT fixed-rate THEN DO:
                                FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest-pr THEN 
                                DO: 
                                    contcode = guest-pr.CODE.  
                                    ct = res-line.zimmer-wunsch.  
                                    IF ct MATCHES("*$CODE$*") THEN  
                                    DO:  
                                        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1). 
                                        ASSIGN output-list.contcode = contcode.  /*ragung*/
                                    END.  
                                    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                    ELSE curr-zikatnr = res-line.zikatnr. 
                                    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                                    IF AVAILABLE queasy AND queasy.logi3 THEN 
                                       bill-date = res-line.ankunft. 
                        
                                    IF new-contrate THEN 
                                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                      res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                    ELSE
                                    DO:
                                      RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                        guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                        res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                        res-line.erwachs, res-line.kind1, res-line.kind2,
                                        res-line.reserve-dec, res-line.betriebsnr, 
                                        OUTPUT rm-rate, OUTPUT rate-found).
                                      /* Rulita 130324 | Fixing for serverless */
                                      /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                      IF it-exist THEN rate-found = YES.
                                      IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                    END. 
                                    ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                                END.    
                                w-day = wd-array[WEEKDAY(bill-date)]. 
                                IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                                DO: 
                                  rm-rate = res-line.zipreis. 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day 
                                    NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) = rm-rate 
                                  THEN rack-rate = YES. 
                                END. 
                                ELSE IF rack-rate THEN 
                                DO: 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) > 0 
                                  THEN 
                                    rm-rate = get-rackrate(res-line.erwachs, 
                                      res-line.kind1, res-line.kind2). 
                                END. /* if rack-rate   */ 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.
             /*ragung*/     ELSE DO:
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*end*/
                                END.  
                            END.
        
                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                      OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                      OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                      OUTPUT tot-dinner, OUTPUT tot-other,
                                                      OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                      OUTPUT tot-service).
                             ASSIGN output-list.lodging = output-list.lodging + net-lodg.
                        END.
                        IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                        ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.
                        
                        /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging.*/
                        
                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        ELSE ASSIGN output-list.lodging1 = 0.
                            
                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            ASSIGN
                                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                                output-list.avg-lodging  = output-list.lodging / output-list.room-night
                            .
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .

                        END.
                        /* End Rulita */

                        ASSIGN
                            tot-lead                 = tot-lead + output-list.lead
                            tot-lodging              = tot-lodging + output-list.lodging
                            tot-lodging1             = tot-lodging1 + output-list.lodging1
                            tot-los                  = tot-los + output-list.room-night
                            tot-rmnight              = tot-rmnight + output-list.rm-night
                            /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                            tot-avrlodging           = tot-avrlodging + output-list.lodging
                            tot-adult                = tot-adult + output-list.adult
                            tot-child                = tot-child + output-list.child
                            tot-infant               = tot-infant + output-list.infant
                            tot-comp                 = tot-comp + output-list.comp
                            tot-compchild            = tot-compchild + output-list.compchild.
    
                        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tot-list THEN DO:
                            CREATE tot-list.
                            ASSIGN tot-list.gastnr = output-list.gastnr.
                        END.
                        ASSIGN tot-list.t-lead  = tot-list.t-lead + output-list.lead
                               tot-list.t-los   = tot-list.t-los + output-list.room-night
                               tot-list.t-reserv    = tot-list.t-reserv + 1
                        .
                    END.
                END.                       
            END.
        
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.create-date BY output-list.gastnr:
            ASSIGN counter  = counter + 1.
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate = t-avrgrmrate / t-rmnight
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
                 FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                 IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
            END.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
    
                IF output-list.lead / tot-list.t-lead NE ? THEN 
                    ASSIGN
                        t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                        tot-avrglead          = tot-avrglead + output-list.lead
                 .
    
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
    
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild   
                t-avrglos               = t-avrglos    + output-list.avrg-los 
                tot-avrglos             = tot-avrglos    + output-list.avrg-los 
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1  = NO
            .
    
        END.
    END.
    ELSE
    DO:
        /*history*/
        FOR EACH genstat WHERE genstat.res-date[1] GE datum 
              AND genstat.res-date[1] LE datum2
              AND genstat.res-logic[2] 
              AND genstat.zinr NE " " AND genstat.resstatus NE 13 NO-LOCK,
            /*FIRST guest WHERE guest.gastnr = genstat.gastnr
                AND guest.NAME GE from-rsv AND guest.NAME LE to-rsv NO-LOCK BY genstat.gastnr:*/
            FIRST guest WHERE guest.gastnr = genstat.gastnrmember
                 NO-LOCK BY genstat.gastnr:       /*Modified By Gerald 23012020*/

            IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                FIND FIRST tguest WHERE tguest.gastnr = genstat.gastnr
                    AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tguest THEN NEXT.
            END.
            
            FIND FIRST reservation WHERE reservation.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
            FIND FIRST output-list WHERE output-list.gastnr = genstat.gastnr
                AND output-list.resno = genstat.resnr
                AND output-list.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF NOT AVAILABLE output-list THEN DO:
                CREATE output-list.
                ASSIGN output-list.gastnr       = genstat.gastnr
                       output-list.rsvname      = reservation.NAME              /*Modified by gerald 23012020*/ 
                       output-list.guestname    = guest.NAME                    /*Add By Gerald 23012020*/      
                       output-list.resno        = genstat.resnr 
                       output-list.reslinnr     = genstat.res-int[1]
                       output-list.cidate       = genstat.res-date[1] 
                       output-list.codate       = genstat.res-date[2]
                       output-list.room-night   = genstat.res-date[2] - genstat.res-date[1] 
                       output-list.rm-night     = genstat.res-date[2] - genstat.res-date[1]  
                       output-list.argt         = genstat.argt
                       output-list.rmrate       = genstat.zipreis 
                       output-list.lodging      = genstat.logis
                       output-list.adult        = genstat.erwachs 
                       output-list.child        = genstat.kind1
                       output-list.infant       = genstat.kind2 
                       output-list.comp         = genstat.gratis
                       output-list.compchild    = genstat.kind3
                       output-list.check-flag   = YES
                       output-list.check-flag1  = YES
                       output-list.check-flag2  = YES
                    .   
                            
                       
                FIND FIRST bguest WHERE bguest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE bguest THEN DO: 
                    FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                    IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                END.
                    
                /*ragung*/
                FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                /*end*/

                FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                
                /*FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.*/
                IF AVAILABLE reservation THEN 
                    ASSIGN 
                        output-list.create-date = reservation.resdat
                        output-list.lead        = genstat.res-date[1] - reservation.resdat. 
    
                FIND FIRST res-line WHERE res-line.resnr = genstat.resnr 
                    AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
                FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                    AND reslin-queasy.resnr = genstat.resnr 
                    AND reslin-queasy.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR. 
                IF AVAILABLE reslin-queasy THEN 
                DO: 
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = genstat.zipreis.
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.                      
                END.             
            END.
            ELSE DO:
                ASSIGN
                   output-list.rmrate       = output-list.rmrate + genstat.zipreis 
                   output-list.lodging      = output-list.lodging + genstat.logis.              
            END.
        END.
    
        FOR EACH output-list WHERE output-list.check-flag2  = YES:
            /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
            /* ASSIGN
                output-list.rmrate1      = output-list.rmrate / foreign-curr
                output-list.lodging1     = output-list.lodging / foreign-curr
                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                output-list.avg-lodging  = output-list.lodging / output-list.room-night
             .
            IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
            IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging. */

            IF foreign-curr NE ? AND foreign-curr NE 0 THEN
            DO:
                ASSIGN
                    output-list.rmrate1      = output-list.rmrate / foreign-curr
                    output-list.lodging1     = output-list.lodging / foreign-curr
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.rmrate1      = 0
                    output-list.lodging1     = 0
                .
            END.

            IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
            DO:
                ASSIGN
                    output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                    output-list.avg-lodging  = output-list.lodging / output-list.room-night
                .
            END.
            ELSE
            DO:
                ASSIGN
                    output-list.avg-rmrate = output-list.rmrate
                    output-list.avg-lodging  = output-list.lodging
                .
            END.
            /* End Rulita */
            ASSIGN
                tot-lead                 = tot-lead + output-list.lead
                tot-lodging              = tot-lodging + output-list.lodging
                tot-lodging1             = tot-lodging1 + output-list.lodging1
                tot-los                  = tot-los + output-list.room-night 
                tot-rmnight              = tot-rmnight + output-list.rm-night 
                /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                tot-avrlodging           = tot-avrlodging + output-list.lodging
                tot-adult                = tot-adult + output-list.adult
                tot-child                = tot-child + output-list.child
                tot-infant               = tot-infant + output-list.infant
                tot-comp                 = tot-comp + output-list.comp
                tot-compchild            = tot-compchild + output-list.compchild.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE tot-list THEN DO:
                CREATE tot-list.
                ASSIGN tot-list.gastnr = output-list.gastnr.
            END.
            ASSIGN tot-list.t-lead      = tot-list.t-lead + output-list.lead
                   tot-list.t-los       = tot-list.t-los + output-list.room-night
                   tot-list.t-reserv    = tot-list.t-reserv + 1
                   output-list.check-flag2  = NO
            .
        END.
    
        
        /*forecast*/
        datum2 = datum2 + 1.
        IF todate GE ci-date THEN DO:
        FOR EACH res-line WHERE ((res-line.resstatus NE 11 AND res-line.resstatus NE 13
            AND res-line.active-flag LE 1 
            AND res-line.ankunft GE fromdate
            AND res-line.ankunft LE todate)) 
            OR (res-line.resstatus NE 11 AND res-line.resstatus NE 13
            AND res-line.active-flag = 2
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK 
            USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending:
                
                /* Rulita 130324 | Fixing for serverless */
                FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
 
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember                     /*Modified by gerald 23012020*/ 
                    NO-LOCK NO-ERROR.             
                IF AVAILABLE guest THEN DO:

                    IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                        FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                            AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tguest THEN NEXT.
                    END.

                    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
                    FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                        AND output-list.resno = res-line.resnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE output-list THEN DO:
                        CREATE output-list.
                        ASSIGN output-list.gastnr       = res-line.gastnr
                               output-list.rsvname      = reservation.NAME      /*Add by gerald 23012020*/ 
                               output-list.guestname    = guest.NAME            /*Modified By Gerald 23012020*/            
                               output-list.resno        = res-line.resnr 
                               output-list.reslinnr     = res-line.reslinnr
                               output-list.cidate       = res-line.ankunft 
                               output-list.codate       = res-line.abreise
                               output-list.room-night   = res-line.abreise - res-line.ankunft 
                               output-list.rm-night     = res-line.abreise - res-line.ankunft 
                               output-list.argt         = res-line.arrangement           
                               output-list.rmrate       = res-line.zipreis
                               output-list.create-date  = reservation.resdat
                               curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 201124 | Fixing for serverless */
                               output-list.lead         = curr-lead-days
                               output-list.adult        = res-line.erwachs 
                               output-list.child        = res-line.kind1
                               output-list.infant       = res-line.kind2 
                               output-list.comp         = res-line.gratis
                               output-list.compchild    = res-line.l-zuordnung[4]
                               output-list.check-flag   = YES
                               output-list.check-flag1  = YES
                               output-list.check-flag2  = YES
                            . 
        
                        FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE bguest THEN DO: 
                            FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                            IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.
                        END.
                        
                        /*ragung*/
                        FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                        IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                        /*end*/
                        
                        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                        IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
        
                        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                        IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                        
                        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                            AND reslin-queasy.resnr = res-line.resnr 
                            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN 
                        DO: 
                            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                        END. 
        
                        datum3 = datum2.
                        IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                        datum4 = todate. 
                        IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
        
                        DO ldatum = datum3 TO datum4:
                            pax         = res-line.erwachs. 
                            net-lodg    = 0.
                            curr-i      = curr-i + 1.
        
                            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                              AND reslin-queasy.resnr = res-line.resnr 
                              AND reslin-queasy.reslinnr = res-line.reslinnr 
                              AND reslin-queasy.date1 LE ldatum 
                              AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                            IF AVAILABLE reslin-queasy THEN DO:
                                fixed-rate = YES. 
                                IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                                ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                            END.
                             
                            IF NOT fixed-rate THEN DO:
                                FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest-pr THEN 
                                DO: 
                                    contcode = guest-pr.CODE.  
                                    ct = res-line.zimmer-wunsch.  
                                    IF ct MATCHES("*$CODE$*") THEN  
                                    DO:  
                                        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1). 
                                        ASSIGN output-list.contcode = contcode.  /*ragung*/
                                    END.  
                                    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                    ELSE curr-zikatnr = res-line.zikatnr. 
                                    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                      = res-line.reserve-int NO-LOCK NO-ERROR. 
                                    IF AVAILABLE queasy AND queasy.logi3 THEN 
                                       bill-date = res-line.ankunft. 
                        
                                    IF new-contrate THEN 
                                    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                      res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                    ELSE
                                    DO:
                                      RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                        guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                        res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                        res-line.erwachs, res-line.kind1, res-line.kind2,
                                        res-line.reserve-dec, res-line.betriebsnr, 
                                        OUTPUT rm-rate, OUTPUT rate-found).
                                      /* Rulita 130324 | Fixing for serverless */
                                      /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                      IF it-exist THEN rate-found = YES.
                                      IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                    END. 
                                    ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                                END.    
                                w-day = wd-array[WEEKDAY(bill-date)]. 
                                IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                                DO: 
                                  rm-rate = res-line.zipreis. 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day 
                                    NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) = rm-rate 
                                  THEN rack-rate = YES. 
                                END. 
                                ELSE IF rack-rate THEN 
                                DO: 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                                  IF NOT AVAILABLE katpreis THEN 
                                  FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                    AND katpreis.argtnr = arrangement.argtnr 
                                    AND katpreis.startperiode LE bill-date 
                                    AND katpreis.endperiode GE bill-date 
                                    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                                  IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                    res-line.kind1, res-line.kind2) > 0 
                                  THEN 
                                    rm-rate = get-rackrate(res-line.erwachs, 
                                      res-line.kind1, res-line.kind2). 
                                END. /* if rack-rate   */ 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.
             /*ragung*/     ELSE DO:
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                    ASSIGN output-list.contcode = contcode.  /*end*/
                                END.  
                            END.
        
                             RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                      OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                      OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                      OUTPUT tot-dinner, OUTPUT tot-other,
                                                      OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                      OUTPUT tot-service).
                             ASSIGN output-list.lodging = output-list.lodging + net-lodg.
                        END.
                        IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                        ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.

                        /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging.*/
                        
                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        ELSE ASSIGN output-list.lodging1 = 0.
                            
                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            ASSIGN
                                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                                output-list.avg-lodging  = output-list.lodging / output-list.room-night
                            .
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .

                        END.
                        /* End Rulita */

                        ASSIGN
                            tot-lead                 = tot-lead + output-list.lead
                            tot-lodging              = tot-lodging + output-list.lodging
                            tot-lodging1             = tot-lodging1 + output-list.lodging1
                            tot-los                  = tot-los + output-list.room-night
                            tot-rmnight              = tot-rmnight + output-list.rm-night
                            /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                            tot-avrlodging           = tot-avrlodging + output-list.lodging
                            tot-adult                = tot-adult + output-list.adult
                            tot-child                = tot-child + output-list.child
                            tot-infant               = tot-infant + output-list.infant
                            tot-comp                 = tot-comp + output-list.comp
                            tot-compchild            = tot-compchild + output-list.compchild.
    
                        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE tot-list THEN DO:
                            CREATE tot-list.
                            ASSIGN tot-list.gastnr = output-list.gastnr.
                        END.
                        ASSIGN tot-list.t-lead  = tot-list.t-lead + output-list.lead
                               tot-list.t-los   = tot-list.t-los + output-list.room-night
                               tot-list.t-reserv    = tot-list.t-reserv + 1
                        .
                    END.
                END.                       
            END.
        END.
        
        FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.gastnr:
            ASSIGN counter  = counter + 1.
            IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
                CREATE boutput.
                ASSIGN 
                    boutput.gastnr      = t-gastnr
                    boutput.rsvname     = "T O T A L"
                    boutput.lead        = t-lead
                    boutput.lodging     = t-lodging
                    boutput.lodging1    = t-lodging1
                    boutput.room-night  = t-los
                    boutput.rm-night    = t-rmnight
                    boutput.avg-lodging = t-avrlodging / t-rmnight
                    boutput.adult       = t-adult 
                    boutput.child       = t-child 
                    boutput.infant      = t-infant 
                    boutput.comp        = t-comp 
                    boutput.compchild   = t-compchild 
                    boutput.avrg-lead   = t-avrglead
                    boutput.avrg-los    = t-avrglos
                    boutput.pos         = counter
                    boutput.rmrate      = t-rmrate                
                    boutput.rmrate1     = t-rmrate1               
                    boutput.avg-rmrate = t-avrgrmrate / t-rmnight
                    t-rmrate            = 0
                    t-rmrate1           = 0
                    t-avrgrmrate        = 0
                    t-lead              = 0
                    t-lodging           = 0
                    t-lodging1          = 0
                    t-avrlodging        = 0
                    t-los               = 0
                    t-rmnight           = 0
                    t-adult             = 0
                    t-child             = 0
                    t-infant            = 0
                    t-comp              = 0
                    t-compchild         = 0 
                    t-avrglead          = 0
                    t-avrglos           = 0
                    counter             = counter + 1
                    boutput.check-flag  = YES
                 .
                 FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
                 IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
            END.
    
            FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE tot-list THEN DO:
                ASSIGN
                    output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                    output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                    .           
    
                IF output-list.lead / tot-list.t-lead NE ? THEN 
                    ASSIGN
                        t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                        tot-avrglead          = tot-avrglead + output-list.lead
                 .
    
                IF output-list.room-night / tot-list.t-reserv NE ? THEN
                    ASSIGN
                        t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                        tot-avrglos           = tot-avrglos  + output-list.room-night
                   .
            END.
    
            ASSIGN 
                output-list.pos         = counter
                t-gastnr                = output-list.gastnr
                t-lead                  = t-lead       + output-list.lead       
                t-lodging               = t-lodging    + output-list.lodging    
                t-lodging1              = t-lodging1   + output-list.lodging1   
                /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
                t-avrlodging            = t-avrlodging + output-list.lodging 
                t-los                   = t-los        + output-list.room-night   
                t-rmnight               = t-rmnight    + output-list.rm-night
                t-adult                 = t-adult      + output-list.adult      
                t-child                 = t-child      + output-list.child      
                t-infant                = t-infant     + output-list.infant     
                t-comp                  = t-comp       + output-list.comp       
                t-compchild             = t-compchild  + output-list.compchild   
                t-avrglos               = t-avrglos    + output-list.avrg-los 
                tot-avrglos             = tot-avrglos    + output-list.avrg-los 
                t-rmrate                = t-rmrate      + output-list.rmrate
                t-rmrate1               = t-rmrate1     + output-list.rmrate1
                /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
                t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
                tot-rmrate              = tot-rmrate    + output-list.rmrate
                tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
                /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
                tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
                output-list.check-flag1 = NO
            .
        END.
    END.

    CREATE output-list.
    ASSIGN 
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = t-gastnr
        output-list.rsvname     = "T O T A L"
        output-list.lead        = t-lead
        output-list.lodging     = t-lodging
        output-list.lodging1    = t-lodging1
        output-list.room-night  = t-los
        output-list.rm-night    = t-rmnight
        output-list.avg-lodging = t-avrlodging / t-rmnight
        output-list.adult       = t-adult 
        output-list.child       = t-child 
        output-list.infant      = t-infant 
        output-list.comp        = t-comp 
        output-list.compchild   = t-compchild 
        output-list.avrg-lead   = t-avrglead
        output-list.avrg-los    = t-avrglos  
        output-list.rmrate      = t-rmrate                
        output-list.rmrate1     = t-rmrate1               
        output-list.avg-rmrate = t-avrgrmrate / t-rmnight
        output-list.check-flag   = YES
.

    FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE tot-list THEN ASSIGN output-list.tot-reserv = tot-list.t-reserv.

    FOR EACH tot-list NO-LOCK:
        ASSIGN tot-rsv = tot-rsv + tot-list.t-reserv.
    END.
    
    CREATE output-list.
    ASSIGN
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = 999999999
        output-list.rsvname     = "Grand T O T A L"
        output-list.lead        = tot-lead
        output-list.lodging     = tot-lodging
        output-list.lodging1    = tot-lodging1
        output-list.room-night  = tot-los
        output-list.rm-night    = tot-rmnight
        output-list.avg-lodging = tot-avrlodging / tot-rmnight
        output-list.adult       = tot-adult 
        output-list.child       = tot-child 
        output-list.infant      = tot-infant 
        output-list.comp        = tot-comp 
        output-list.compchild   = tot-compchild 
        output-list.avrg-lead   = tot-avrglead / tot-rsv
        output-list.avrg-los    = tot-avrglos / tot-rsv
        output-list.rmrate      = tot-rmrate                
        output-list.rmrate1     = tot-rmrate1               
        output-list.avg-rmrate  = tot-avrgrmrate / tot-rmnight
        output-list.tot-reserv  = tot-rsv
        output-list.check-flag   = YES
    .
END.

PROCEDURE create-browse-rm-sharer1:
    DEFINE VARIABLE datum            AS DATE NO-UNDO.
    DEFINE VARIABLE datum2           AS DATE NO-UNDO.
    DEFINE VARIABLE datum3           AS DATE NO-UNDO.
    DEFINE VARIABLE datum4           AS DATE NO-UNDO.
    DEFINE VARIABLE ldatum           AS DATE NO-UNDO.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-vat          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-service      AS DECIMAL INITIAL 0.

    DEFINE VARIABLE tot-lead         AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-lodging1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrlodging   AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-los          AS INTEGER INITIAL 0.
    DEFINE VARIABLE tot-rmnight      AS INTEGER INITIAL 0.

    DEFINE VARIABLE tot-adult         AS INTEGER.
    DEFINE VARIABLE tot-child         AS INTEGER.
    DEFINE VARIABLE tot-infant        AS INTEGER.
    DEFINE VARIABLE tot-comp          AS INTEGER.
    DEFINE VARIABLE tot-compchild     AS INTEGER.

    DEFINE VARIABLE t-gastnr        AS INTEGER.
    DEFINE VARIABLE t-lead          AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-lodging1      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrlodging    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglead      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrglos       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-los           AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-rmnight       AS INTEGER INITIAL 0.
    DEFINE VARIABLE t-adult         AS INTEGER.
    DEFINE VARIABLE t-child         AS INTEGER.
    DEFINE VARIABLE t-infant        AS INTEGER.
    DEFINE VARIABLE t-comp          AS INTEGER.
    DEFINE VARIABLE t-compchild     AS INTEGER.
    DEFINE VARIABLE tot-avrglead    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrglos     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate        AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-rmrate1       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-avrgrmrate    AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate      AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rmrate1     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-avrgrmrate  AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-rsv         AS DECIMAL INITIAL 0.
    
    IF check-cdate THEN
    DO:
      FOR EACH res-line WHERE (res-line.active-flag LE 1 
        AND res-line.resstatus NE 11 AND res-line.resstatus NE 13) 
        OR (res-line.active-flag = 2 AND res-line.resstatus NE 11
        AND res-line.resstatus NE 13
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK,
        FIRST reservation WHERE reservation.resdat GE fromdate
          AND reservation.resdat LE todate
          AND reservation.resnr = res-line.resnr NO-LOCK BY res-line.resnr:
            
            ASSIGN
             curr-i        = 0
             tot-breakfast = 0
             tot-lunch     = 0
             tot-dinner    = 0
             tot-other     = 0
             ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*")
             kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").

             /* ITA 09/04/2025 | Fixing for serverless */
            FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
            
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember                 /*Modified by gerald 23012020*/ 
                NO-LOCK NO-ERROR.       
            IF AVAILABLE guest THEN DO:

                IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                    FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                        AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE tguest THEN NEXT.
                END.

                FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                    AND output-list.resno = res-line.resnr
                    AND output-list.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE output-list THEN DO:
                    CREATE output-list.
                    ASSIGN output-list.gastnr       = res-line.gastnr
                           output-list.rsvname      = reservation.NAME      /*Add by gerald 23012020*/ 
                           output-list.guestname    = guest.NAME            /*Modified By Gerald 23012020*/            
                           output-list.resno        = res-line.resnr
                           output-list.reslinnr     = res-line.reslinnr
                           output-list.cidate       = res-line.ankunft 
                           output-list.codate       = res-line.abreise
                           output-list.room-night   = res-line.abreise - res-line.ankunft 
                           output-list.rm-night     = res-line.abreise - res-line.ankunft 
                           output-list.argt         = res-line.arrangement           
                           /*output-list.rmrate       = res-line.zipreis */
                           output-list.create-date  = reservation.resdat
                           /* output-list.lead         = res-line.ankunft - reservation.resdat */
                           curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 161224 | Fixing for serverless 299 */
                           output-list.lead         = curr-lead-days
                           output-list.adult        = res-line.erwachs 
                           output-list.child        = res-line.kind1
                           output-list.infant       = res-line.kind2 
                           output-list.comp         = res-line.gratis
                           output-list.compchild    = res-line.l-zuordnung[4]
                           output-list.check-flag   = YES
                           output-list.check-flag1  = YES
                           output-list.check-flag2  = YES
                       . 
    
                    
                    FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE bguest THEN DO: 
                        FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                        IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.                       
                    END.

                    /*ragung*/
                    FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                    IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                    /*end*/
                    
                    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                    IF AVAILABLE segment THEN output-list.segment = segment.bezeich.
    
                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                    
                    FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                        AND reslin-queasy.resnr = res-line.resnr 
                        AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE reslin-queasy THEN 
                    DO: 
                        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                    END. 
                    
                    datum3 = fromdate.
                    IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                    datum4 = todate. 
                    IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
                    
                    tmp-date = res-line.abreise - 1.                                /* Rulita 071124 | Fixing date calculate for serverless program */
                    /*DO ldatum = datum3 TO datum4:*/
                    /* DO ldatum = res-line.ankunft TO res-line.abreise - 1: */     /* Rulita 071124 | Fixing date calculate for serverless program */
                    DO ldatum = res-line.ankunft TO tmp-date:
                        pax         = res-line.erwachs. 
                        net-lodg    = 0.
                        curr-i      = curr-i + 1.

                        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                          AND reslin-queasy.resnr = res-line.resnr 
                          AND reslin-queasy.reslinnr = res-line.reslinnr 
                          AND reslin-queasy.date1 LE ldatum 
                          AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN DO:
                            fixed-rate = YES. 
                            IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                            ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                        END.
                         
                        IF NOT fixed-rate THEN DO:
                            FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                            IF AVAILABLE guest-pr THEN 
                            DO: 
                                contcode = guest-pr.CODE.  
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
                                    ASSIGN output-list.contcode = contcode.  /*ragung*/
                                END.  
                                IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                ELSE curr-zikatnr = res-line.zikatnr. 
                                FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                  = res-line.reserve-int NO-LOCK NO-ERROR. 
                                IF AVAILABLE queasy AND queasy.logi3 THEN 
                                   bill-date = res-line.ankunft. 
                    
                                IF new-contrate THEN 
                                RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                  res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                  res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                  curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                  res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                  OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                ELSE
                                DO:
                                  RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                    guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                    res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                    res-line.erwachs, res-line.kind1, res-line.kind2,
                                    res-line.reserve-dec, res-line.betriebsnr, 
                                    OUTPUT rm-rate, OUTPUT rate-found).
                                    /* Rulita 130324 | Fixing for serverless */
                                    /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                  IF it-exist THEN rate-found = YES.
                                  IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                END. 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.    
                            w-day = wd-array[WEEKDAY(bill-date)]. 
                            IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                            DO: 
                              rm-rate = res-line.zipreis. 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = w-day 
                                NO-LOCK NO-ERROR. 
                              IF NOT AVAILABLE katpreis THEN 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                              IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                res-line.kind1, res-line.kind2) = rm-rate 
                              THEN rack-rate = YES. 
                            END. 
                            ELSE IF rack-rate THEN 
                            DO: 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                              IF NOT AVAILABLE katpreis THEN 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                              IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                res-line.kind1, res-line.kind2) > 0 
                              THEN 
                                rm-rate = get-rackrate(res-line.erwachs, 
                                  res-line.kind1, res-line.kind2). 
                            END. /* if rack-rate   */ 
                            ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                        END.
         /*ragung*/     ELSE DO:
                            ct = res-line.zimmer-wunsch.  
                            IF ct MATCHES("*$CODE$*") THEN  
                            DO:  
                                ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                ASSIGN output-list.contcode = contcode.  /*end*/
                            END.  
                        END.

                         RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                  OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                  OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                  OUTPUT tot-dinner, OUTPUT tot-other,
                                                  OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                  OUTPUT tot-service).
                         ASSIGN output-list.lodging = output-list.lodging + net-lodg.                         
                    END.
                    
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                    ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.

                    /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                        /* ASSIGN 
                            output-list.lodging1     = output-list.lodging / foreign-curr
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                        IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                        IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging.*/
                        
                        IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                        ELSE ASSIGN output-list.lodging1 = 0.
                            
                        IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                        DO:
                            ASSIGN
                                output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                                output-list.avg-lodging  = output-list.lodging / output-list.room-night
                            .
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                output-list.avg-rmrate = output-list.rmrate
                                output-list.avg-lodging  = output-list.lodging
                            .

                        END.
                        /* End Rulita */

                    ASSIGN
                        tot-lead                 = tot-lead + output-list.lead
                        tot-lodging              = tot-lodging + output-list.lodging
                        tot-lodging1             = tot-lodging1 + output-list.lodging1
                        tot-los                  = tot-los + output-list.room-night
                        tot-rmnight              = tot-rmnight + output-list.rm-night
                        /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                        tot-avrlodging           = tot-avrlodging + output-list.lodging
                        tot-adult                = tot-adult + output-list.adult
                        tot-child                = tot-child + output-list.child
                        tot-infant               = tot-infant + output-list.infant
                        tot-comp                 = tot-comp + output-list.comp
                        tot-compchild            = tot-compchild + output-list.compchild.

                    FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE tot-list THEN DO:
                        CREATE tot-list.
                        ASSIGN tot-list.gastnr = output-list.gastnr.
                    END.
                    ASSIGN tot-list.t-lead  = tot-list.t-lead + output-list.lead
                           tot-list.t-los   = tot-list.t-los + output-list.room-night
                           tot-list.t-reserv    = tot-list.t-reserv + 1
                           .
                END.
            END.              
      END.

      FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.create-date BY output-list.gastnr:
        ASSIGN counter  = counter + 1.
        IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
            CREATE boutput.
            ASSIGN 
                boutput.gastnr      = t-gastnr
                boutput.rsvname     = "T O T A L"
                boutput.lead        = t-lead
                boutput.lodging     = t-lodging
                boutput.lodging1    = t-lodging1
                boutput.room-night  = t-los
                boutput.rm-night    = t-rmnight
                boutput.avg-lodging = t-avrlodging / t-rmnight
                boutput.adult       = t-adult 
                boutput.child       = t-child 
                boutput.infant      = t-infant 
                boutput.comp        = t-comp 
                boutput.compchild   = t-compchild 
                boutput.avrg-lead   = t-avrglead
                boutput.avrg-los    = t-avrglos
                boutput.pos         = counter
                boutput.rmrate      = t-rmrate                
                boutput.rmrate1     = t-rmrate1               
                boutput.avg-rmrate  = t-avrgrmrate / t-rmnight
                t-rmrate            = 0
                t-rmrate1           = 0
                t-avrgrmrate        = 0
                t-lead              = 0
                t-lodging           = 0
                t-lodging1          = 0
                t-avrlodging        = 0
                t-los               = 0
                t-rmnight           = 0
                t-adult             = 0
                t-child             = 0
                t-infant            = 0
                t-comp              = 0
                t-compchild         = 0 
                t-avrglead          = 0
                t-avrglos           = 0
                counter             = counter + 1
                boutput.check-flag  = YES
             .
             FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
             IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
        END.

        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE tot-list THEN DO:
            ASSIGN
                output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                .           

            IF output-list.lead / tot-list.t-lead NE ? THEN 
                ASSIGN
                    t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                    tot-avrglead          = tot-avrglead + output-list.lead
             .

            IF output-list.room-night / tot-list.t-reserv NE ? THEN
                ASSIGN
                    t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                    tot-avrglos           = tot-avrglos  + output-list.room-night
               .
        END.

        ASSIGN 
            output-list.pos         = counter
            t-gastnr                = output-list.gastnr
            t-lead                  = t-lead       + output-list.lead       
            t-lodging               = t-lodging    + output-list.lodging    
            t-lodging1              = t-lodging1   + output-list.lodging1   
            /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
            t-avrlodging            = t-avrlodging + output-list.lodging 
            t-los                   = t-los        + output-list.room-night   
            t-rmnight               = t-rmnight    + output-list.rm-night
            t-adult                 = t-adult      + output-list.adult      
            t-child                 = t-child      + output-list.child      
            t-infant                = t-infant     + output-list.infant     
            t-comp                  = t-comp       + output-list.comp       
            t-compchild             = t-compchild  + output-list.compchild   
            t-avrglos               = t-avrglos    + output-list.avrg-los 
            tot-avrglos             = tot-avrglos    + output-list.avrg-los 
            t-rmrate                = t-rmrate      + output-list.rmrate
            t-rmrate1               = t-rmrate1     + output-list.rmrate1
            /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
            t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
            tot-rmrate              = tot-rmrate    + output-list.rmrate
            tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
            /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
            tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
            output-list.check-flag1 = NO
        .
      END.
    END.
    ELSE
    DO:
        FOR EACH res-line WHERE (res-line.active-flag LE 1 
        AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 
        AND res-line.ankunft GE fromdate
        AND res-line.ankunft LE todate) OR 
        (res-line.active-flag = 2 AND res-line.resstatus = 11
         AND res-line.resstatus NE 13
         AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 AND res-line.l-zuordnung[3] = 0 
        USE-INDEX gnrank_ix NO-LOCK BY res-line.resnr:
            
            ASSIGN
             curr-i        = 0
             tot-breakfast = 0
             tot-lunch     = 0
             tot-dinner    = 0
             tot-other     = 0
             ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*")
             kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").

             /* ITA 09/04/2025 | Fixing for serverless */
            FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
            
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember                 /*Modified by gerald 23012020*/ 
                 NO-LOCK NO-ERROR.       
            IF AVAILABLE guest THEN DO:

                IF from-rsv NE "" AND to-rsv NE "" THEN DO:
                    FIND FIRST tguest WHERE tguest.gastnr = res-line.gastnr
                        AND tguest.NAME GE from-rsv AND tguest.NAME LE to-rsv NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE tguest THEN NEXT.
                END.

                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
                FIND FIRST output-list WHERE output-list.gastnr = res-line.gastnr
                    AND output-list.resno = res-line.resnr
                    AND output-list.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE output-list THEN DO:
                    CREATE output-list.
                    ASSIGN output-list.gastnr       = res-line.gastnr
                           output-list.rsvname      = reservation.NAME      /*Add by gerald 23012020*/ 
                           output-list.guestname    = guest.NAME            /*Modified By Gerald 23012020*/            
                           output-list.resno        = res-line.resnr
                           output-list.reslinnr     = res-line.reslinnr
                           output-list.cidate       = res-line.ankunft 
                           output-list.codate       = res-line.abreise
                           output-list.room-night   = res-line.abreise - res-line.ankunft 
                           output-list.rm-night     = res-line.abreise - res-line.ankunft 
                           output-list.argt         = res-line.arrangement           
                           /*output-list.rmrate       = res-line.zipreis */
                           output-list.create-date  = reservation.resdat
                           /* output-list.lead         = res-line.ankunft - reservation.resdat */
                           curr-lead-days           = res-line.ankunft - reservation.resdat                 /* Rulita 161224 | Fixing for serverless 299 */
                           output-list.lead         = curr-lead-days
                           output-list.adult        = res-line.erwachs 
                           output-list.child        = res-line.kind1
                           output-list.infant       = res-line.kind2 
                           output-list.comp         = res-line.gratis
                           output-list.compchild    = res-line.l-zuordnung[4]
                           output-list.check-flag   = YES
                           output-list.check-flag1  = YES
                           output-list.check-flag2  = YES
                        . 
    
                    
                    FIND FIRST bguest WHERE bguest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE bguest THEN DO: 
                        FIND FIRST nation WHERE nation.kurzbez = bguest.nation1 NO-LOCK NO-ERROR.
                        IF AVAILABLE nation THEN ASSIGN output-list.nation = nation.bezeich.                       
                    END.
                    
                    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                    IF AVAILABLE segment THEN output-list.segment = segment.bezeich.

                    /*ragung*/
                    FIND FIRST sourccod WHERE Sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
                    IF AVAILABLE sourccod THEN ASSIGN output-list.sourcecode = sourccod.bezeich.
                    /*end*/
    
                    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                    IF AVAILABLE zimkateg THEN ASSIGN output-list.rm-type = zimkateg.kurzbez. 
                    
                    FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
                        AND reslin-queasy.resnr = res-line.resnr 
                        AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE reslin-queasy THEN 
                    DO: 
                        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE waehrung THEN output-list.currency  = waehrung.wabkurz.
                    END. 
                    
                    datum3 = fromdate.
                    IF res-line.ankunft GT datum3 THEN datum3 = res-line.ankunft. 
                    datum4 = todate. 
                    IF res-line.abreise LT datum4 THEN datum4 = res-line.abreise.
                    
                    tmp-date = res-line.abreise - 1.                                /* Rulita 071124 | Fixing date calculate for serverless program */
                    /*DO ldatum = datum3 TO datum4:*/
                    /* DO ldatum = res-line.ankunft TO res-line.abreise - 1: */     /* Rulita 071124 | Fixing date calculate for serverless program */
                    DO ldatum = res-line.ankunft TO tmp-date:       
                        pax         = res-line.erwachs. 
                        net-lodg    = 0.
                        curr-i      = curr-i + 1.

                        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                          AND reslin-queasy.resnr = res-line.resnr 
                          AND reslin-queasy.reslinnr = res-line.reslinnr 
                          AND reslin-queasy.date1 LE ldatum 
                          AND reslin-queasy.date2 GE ldatum NO-LOCK NO-ERROR. 
                        IF AVAILABLE reslin-queasy THEN DO:
                            fixed-rate = YES. 
                            IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
                            ASSIGN output-list.rmrate = output-list.rmrate + reslin-queasy.deci1. 
                        END.
                         
                        IF NOT fixed-rate THEN DO:
                            FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
                            IF AVAILABLE guest-pr THEN 
                            DO: 
                                contcode = guest-pr.CODE.  
                                ct = res-line.zimmer-wunsch.  
                                IF ct MATCHES("*$CODE$*") THEN  
                                DO:  
                                    ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                    contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
                                    ASSIGN output-list.contcode = contcode.  /*ragung*/
                                END.  
                                IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
                                ELSE curr-zikatnr = res-line.zikatnr. 
                                FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                                  = res-line.reserve-int NO-LOCK NO-ERROR. 
                                IF AVAILABLE queasy AND queasy.logi3 THEN 
                                   bill-date = res-line.ankunft. 
                    
                                IF new-contrate THEN 
                                RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                                  res-line.reslinnr, contcode, ?, bill-date, res-line.ankunft,
                                  res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                                  curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                                  res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                                  OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
                                ELSE
                                DO:
                                  RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                                    guest-pr.CODE, bill-date, res-line.ankunft, res-line.abreise, 
                                    res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                                    res-line.erwachs, res-line.kind1, res-line.kind2,
                                    res-line.reserve-dec, res-line.betriebsnr, 
                                    OUTPUT rm-rate, OUTPUT rate-found).
                                    /* Rulita 130324 | Fixing for serverless */
                                    /* RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
                                  IF it-exist THEN rate-found = YES.
                                  IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
                                END. 
                                ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                            END.    
                            w-day = wd-array[WEEKDAY(bill-date)]. 
                            IF (bill-date = ci-date) OR (bill-date = res-line.ankunft) THEN 
                            DO: 
                              rm-rate = res-line.zipreis. 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = w-day 
                                NO-LOCK NO-ERROR. 
                              IF NOT AVAILABLE katpreis THEN 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                              IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                res-line.kind1, res-line.kind2) = rm-rate 
                              THEN rack-rate = YES. 
                            END. 
                            ELSE IF rack-rate THEN 
                            DO: 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
                              IF NOT AVAILABLE katpreis THEN 
                              FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                                AND katpreis.argtnr = arrangement.argtnr 
                                AND katpreis.startperiode LE bill-date 
                                AND katpreis.endperiode GE bill-date 
                                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
                              IF AVAILABLE katpreis AND get-rackrate(res-line.erwachs, 
                                res-line.kind1, res-line.kind2) > 0 
                              THEN 
                                rm-rate = get-rackrate(res-line.erwachs, 
                                  res-line.kind1, res-line.kind2). 
                            END. /* if rack-rate   */ 
                            ASSIGN output-list.rmrate = output-list.rmrate + rm-rate. 
                        END.
         /*ragung*/     ELSE DO:
                            ct = res-line.zimmer-wunsch.  
                            IF ct MATCHES("*$CODE$*") THEN  
                            DO:  
                                ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).  
                                contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).  
                                ASSIGN output-list.contcode = contcode.  /*end*/
                            END.  
                        END.

                         RUN get-room-breakdown.p(RECID(res-line), ldatum, curr-i, fromdate,
                                                  OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                  OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                                  OUTPUT tot-dinner, OUTPUT tot-other,
                                                  OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                  OUTPUT tot-service).
                         ASSIGN output-list.lodging = output-list.lodging + net-lodg.                         
                    END.
                    
                    IF res-line.betriebsnr = curr-foreign THEN ASSIGN output-list.rmrate1 = output-list.rmrate.
                    ELSE ASSIGN output-list.rmrate1      = output-list.rmrate / foreign-curr.
                    /* Rulita 161224 | Fixing serverless error decimal.DivisionByZero issue git 100 */
                    /* ASSIGN 
                        output-list.lodging1     = output-list.lodging / foreign-curr
                        output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                        output-list.avg-lodging  = output-list.lodging / output-list.room-night
                    .
                    IF output-list.avg-rmrate = ? THEN ASSIGN output-list.avg-rmrate = output-list.rmrate.
                    IF output-list.avg-lodging = ? THEN ASSIGN output-list.avg-lodging  = output-list.lodging.*/
                    
                    IF foreign-curr NE ? AND foreign-curr NE 0 THEN ASSIGN output-list.lodging1 = output-list.lodging / foreign-curr.
                    ELSE ASSIGN output-list.lodging1 = 0.
                        
                    IF output-list.room-night NE ? AND output-list.room-night NE 0 THEN
                    DO:
                        ASSIGN
                            output-list.avg-rmrate   = output-list.rmrate / output-list.room-night
                            output-list.avg-lodging  = output-list.lodging / output-list.room-night
                        .
                    END.
                    ELSE
                    DO:
                        ASSIGN
                            output-list.avg-rmrate = output-list.rmrate
                            output-list.avg-lodging  = output-list.lodging
                        .

                    END.
                    /* End Rulita */
                    ASSIGN
                        tot-lead                 = tot-lead + output-list.lead
                        tot-lodging              = tot-lodging + output-list.lodging
                        tot-lodging1             = tot-lodging1 + output-list.lodging1
                        tot-los                  = tot-los + output-list.room-night
                        tot-rmnight              = tot-rmnight + output-list.rm-night
                        /*tot-avrlodging           = tot-avrlodging + output-list.avg-lodging*/
                        tot-avrlodging           = tot-avrlodging + output-list.lodging
                        tot-adult                = tot-adult + output-list.adult
                        tot-child                = tot-child + output-list.child
                        tot-infant               = tot-infant + output-list.infant
                        tot-comp                 = tot-comp + output-list.comp
                        tot-compchild            = tot-compchild + output-list.compchild.

                    FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE tot-list THEN DO:
                        CREATE tot-list.
                        ASSIGN tot-list.gastnr = output-list.gastnr.
                    END.
                    ASSIGN tot-list.t-lead  = tot-list.t-lead + output-list.lead
                           tot-list.t-los   = tot-list.t-los + output-list.room-night
                           tot-list.t-reserv    = tot-list.t-reserv + 1
                           .
                END.
            END.              
        END.

      FOR EACH output-list WHERE output-list.check-flag1  = YES BY output-list.gastnr:
        ASSIGN counter  = counter + 1.
        IF t-gastnr NE 0 AND t-gastnr NE output-list.gastnr THEN DO:
            CREATE boutput.
            ASSIGN 
                boutput.gastnr      = t-gastnr
                boutput.rsvname     = "T O T A L"
                boutput.lead        = t-lead
                boutput.lodging     = t-lodging
                boutput.lodging1    = t-lodging1
                boutput.room-night  = t-los
                boutput.rm-night    = t-rmnight
                boutput.avg-lodging = t-avrlodging / t-rmnight
                boutput.adult       = t-adult 
                boutput.child       = t-child 
                boutput.infant      = t-infant 
                boutput.comp        = t-comp 
                boutput.compchild   = t-compchild 
                boutput.avrg-lead   = t-avrglead
                boutput.avrg-los    = t-avrglos
                boutput.pos         = counter
                boutput.rmrate      = t-rmrate                
                boutput.rmrate1     = t-rmrate1               
                boutput.avg-rmrate  = t-avrgrmrate / t-rmnight
                t-rmrate            = 0
                t-rmrate1           = 0
                t-avrgrmrate        = 0
                t-lead              = 0
                t-lodging           = 0
                t-lodging1          = 0
                t-avrlodging        = 0
                t-los               = 0
                t-rmnight           = 0
                t-adult             = 0
                t-child             = 0
                t-infant            = 0
                t-comp              = 0
                t-compchild         = 0 
                t-avrglead          = 0
                t-avrglos           = 0
                counter             = counter + 1
                boutput.check-flag  = YES
             .
             FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
             IF AVAILABLE tot-list THEN ASSIGN boutput.tot-reserv = tot-list.t-reserv.
        END.

        FIND FIRST tot-list WHERE tot-list.gastnr = output-list.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE tot-list THEN DO:
            ASSIGN
                output-list.avrg-lead = output-list.lead /*/ tot-list.t-lead*/
                output-list.avrg-los  = output-list.room-night /*/ tot-list.t-los*/
                .           

            IF output-list.lead / tot-list.t-lead NE ? THEN 
                ASSIGN
                    t-avrglead            = t-avrglead + (output-list.lead / tot-list.t-reserv)
                    tot-avrglead          = tot-avrglead + output-list.lead
             .

            IF output-list.room-night / tot-list.t-reserv NE ? THEN
                ASSIGN
                    t-avrglos             = t-avrglos    + (output-list.room-night / tot-list.t-reserv)
                    tot-avrglos           = tot-avrglos  + output-list.room-night
               .
        END.

        ASSIGN 
            output-list.pos         = counter
            t-gastnr                = output-list.gastnr
            t-lead                  = t-lead       + output-list.lead       
            t-lodging               = t-lodging    + output-list.lodging    
            t-lodging1              = t-lodging1   + output-list.lodging1   
            /*t-avrlodging            = t-avrlodging + output-list.avg-lodging */
            t-avrlodging            = t-avrlodging + output-list.lodging 
            t-los                   = t-los        + output-list.room-night   
            t-rmnight               = t-rmnight    + output-list.rm-night
            t-adult                 = t-adult      + output-list.adult      
            t-child                 = t-child      + output-list.child      
            t-infant                = t-infant     + output-list.infant     
            t-comp                  = t-comp       + output-list.comp       
            t-compchild             = t-compchild  + output-list.compchild   
            t-avrglos               = t-avrglos    + output-list.avrg-los 
            tot-avrglos             = tot-avrglos    + output-list.avrg-los 
            t-rmrate                = t-rmrate      + output-list.rmrate
            t-rmrate1               = t-rmrate1     + output-list.rmrate1
            /*t-avrgrmrate            = t-avrgrmrate  + output-list.avg-rmrate*/
            t-avrgrmrate            = t-avrgrmrate  + output-list.rmrate
            tot-rmrate              = tot-rmrate    + output-list.rmrate
            tot-rmrate1             = tot-rmrate1   + output-list.rmrate1
            /*tot-avrgrmrate          = tot-avrgrmrate + output-list.avg-rmrate*/
            tot-avrgrmrate          = tot-avrgrmrate + output-list.rmrate
            output-list.check-flag1 = NO
        .

      END.                
    END.   

    CREATE output-list.
    ASSIGN 
        counter                 = counter + 1
        output-list.pos         = counter
        output-list.gastnr      = t-gastnr
        output-list.rsvname     = "T O T A L"
        output-list.lead        = t-lead
        output-list.lodging     = t-lodging
        output-list.lodging1    = t-lodging1
        output-list.room-night  = t-los
        output-list.rm-night    = t-rmnight
        output-list.avg-lodging = t-avrlodging / t-rmnight
        output-list.adult       = t-adult 
        output-list.child       = t-child 
        output-list.infant      = t-infant 
        output-list.comp        = t-comp 
        output-list.compchild   = t-compchild 
        output-list.avrg-lead   = t-avrglead
        output-list.avrg-los    = t-avrglos 
        output-list.rmrate      = t-rmrate                
        output-list.rmrate1     = t-rmrate1               
        output-list.avg-rmrate = t-avrgrmrate / t-rmnight
        output-list.check-flag   = YES
        .

    FIND FIRST tot-list WHERE tot-list.gastnr = t-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE tot-list THEN ASSIGN output-list.tot-reserv = tot-list.t-reserv.

    
  /* CREATE output-list.
    ASSIGN 
        output-list.gastnr      = 999999999
        output-list.rsvname   = "T O T A L"
        output-list.lead        = tot-lead
        output-list.lodging     = tot-lodging
        output-list.lodging1    = tot-lodging1
        output-list.room-night  = tot-los
        output-list.rm-night    = tot-rmnight
        output-list.avg-lodging = tot-avrlodging
        output-list.adult       = tot-adult 
        output-list.child       = tot-child 
        output-list.infant      = tot-infant 
        output-list.comp        = tot-comp 
        output-list.compchild   = tot-compchild.*/
END.






