DEFINE TEMP-TABLE output-list
    FIELD counter     AS INTEGER
    FIELD segmentcode AS INTEGER
    FIELD datum       AS DATE
    FIELD str-datum   AS CHAR
    FIELD segment     AS CHAR
    FIELD room        AS INTEGER
    FIELD revenue     AS DECIMAL
    FIELD avrg-rev    AS DECIMAL
    FIELD str-room    AS CHAR
    FIELD str-revenue AS CHAR
    FIELD str-avrg    AS CHAR
    FIELD check-flag   AS LOGICAL
.

DEFINE TEMP-TABLE output-list1
    FIELD counter     AS INTEGER
    FIELD segmentcode AS INTEGER
    FIELD segment     AS CHAR
    FIELD room        AS INTEGER EXTENT 12
    FIELD revenue     AS DECIMAL EXTENT 12
    FIELD avrg-rev    AS DECIMAL EXTENT 12
    FIELD check-flag  AS LOGICAL
.

DEFINE INPUT PARAMETER sum-month AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER fr-date   AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER to-date   AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER to-year   AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER ex-tent   AS LOGICAL NO-UNDO. /*william F4BC9C*/
DEFINE INPUT PARAMETER ex-comp   AS LOGICAL NO-UNDO. /*william F4BC9C*/
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
DEFINE OUTPUT PARAMETER TABLE FOR output-list1.

DEFINE VARIABLE black-list AS INTEGER. 
DEFINE VARIABLE counter    AS INTEGER.
DEFINE VARIABLE ci-date    AS DATE    NO-UNDO.
DEFINE VARIABLE curr-date  AS DATE    NO-UNDO.
DEFINE VARIABLE tot-rm     AS DECIMAL NO-UNDO.
DEFINE VARIABLE trm        AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-rev    AS DECIMAL NO-UNDO.
DEFINE VARIABLE trev       AS DECIMAL NO-UNDO.


DEFINE VARIABLE trev1       AS DECIMAL NO-UNDO EXTENT 12.
DEFINE VARIABLE trm1        AS DECIMAL NO-UNDO EXTENT 12.
DEFINE VARIABLE loopi       AS INTEGER NO-UNDO.

DEFINE BUFFER boutput FOR output-list.
DEFINE BUFFER boutput1 FOR output-list1.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN ci-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
ASSIGN black-list = htparam.finteger. 

IF sum-month = NO THEN DO:
    IF fr-date LT ci-date THEN RUN create-browse.
    ELSE RUN create-browse1.
    
    FOR EACH output-list WHERE output-list.check-flag  = YES BY output-list.datum BY output-list.segmentcode: /* Naufal Afthar - AD7A8A*/
    
        IF curr-date = ? THEN DO:
              CREATE boutput.
              ASSIGN counter             = counter + 1
                     boutput.counter     = counter  
                     boutput.segment     = STRING(output-list.datum, "99/99/9999")
              .
        END.
        ELSE IF curr-date NE ? AND curr-date NE output-list.datum THEN DO:
              CREATE boutput.
              ASSIGN counter             = counter + 1
                     boutput.counter     = counter                 
                     boutput.datum       = curr-date
                     boutput.str-datum   = STRING(curr-date, "99/99/9999")
                     boutput.segment     = "TOTAL"
                     boutput.room        = tot-rm
                     boutput.revenue     = tot-rev
                     boutput.avrg-rev    = tot-rev / tot-rm
                     tot-rm              = 0 
                     tot-rev             = 0 
                     boutput.str-room     = STRING(boutput.room, ">>>,>>9")
                     boutput.str-revenue  = STRING(boutput.revenue, "->>>,>>>,>>>,>>9.99")
                     boutput.str-avrg     = STRING(boutput.avrg-rev, "->>>,>>>,>>>,>>9.99")     
                  .      
    
              CREATE boutput.
              ASSIGN counter             = counter + 1
                     boutput.counter     = counter.
    
              CREATE boutput.
              ASSIGN counter             = counter + 1
                     boutput.counter     = counter  
                     boutput.segment     = STRING(output-list.datum, "99/99/9999")
              .
        END.
        IF output-list.room NE 0 AND output-list.room NE ? THEN
        DO:
            output-list.avrg-rev     = output-list.revenue / output-list.room.
        END.
        ASSIGN counter                  = counter + 1
               output-list.counter      = counter  
               /* output-list.avrg-rev     = output-list.revenue / output-list.room */
               output-list.str-room     = STRING(output-list.room, ">>>,>>9")
               output-list.str-revenue  = STRING(output-list.revenue, "->>>,>>>,>>>,>>9.99")
               output-list.str-avrg     = STRING(output-list.avrg-rev, "->>>,>>>,>>>,>>9.99")           
               curr-date                = output-list.datum
               tot-rm                   = tot-rm + output-list.room
               tot-rev                  = tot-rev + output-list.revenue
               trm                      = trm + output-list.room
               trev                     = trev + output-list.revenue
               output-list.check-flag   = NO
         .
    END.
    
    CREATE boutput.
    ASSIGN counter             = counter + 1
           boutput.counter     = counter                 
           boutput.datum       = curr-date
           boutput.str-datum   = STRING(curr-date, "99/99/9999")
           boutput.segment     = "TOTAL"
           boutput.room        = tot-rm
           boutput.revenue     = tot-rev
           boutput.avrg-rev    = tot-rev / tot-rm
           tot-rm              = 0 
           tot-rev             = 0 
           boutput.str-room     = STRING(boutput.room, ">>>,>>9")
           boutput.str-revenue  = STRING(boutput.revenue, "->>>,>>>,>>>,>>9.99")
           boutput.str-avrg     = STRING(boutput.avrg-rev, "->>>,>>>,>>>,>>9.99")   
      .         
    
    CREATE boutput.
    ASSIGN counter             = counter + 1
           boutput.counter     = counter                        
           boutput.segment     = "Grand TOTAL"
           boutput.room        = trm
           boutput.revenue     = trev
           boutput.avrg-rev    = trev / trm
           boutput.str-room     = STRING(boutput.room, ">>>,>>9")
           boutput.str-revenue  = STRING(boutput.revenue, "->>>,>>>,>>>,>>9.99")
           boutput.str-avrg     = STRING(boutput.avrg-rev, "->>>,>>>,>>>,>>9.99")   
      .
END.
ELSE IF sum-month = YES THEN DO:
    IF to-year LE YEAR(ci-date) THEN RUN create-browse2.
    ELSE RUN create-browse3.


    FOR EACH output-list1 WHERE output-list1.check-flag  = YES BY output-list.segmentcode: /* Naufal Afthar - AD7A8A*/
        
        DO loopi = 1 TO 12:
            ASSIGN counter                   = counter + 1
                   output-list1.counter      = counter  
                   output-list1.avrg-rev[loopi]     = output-list1.revenue[loopi] / output-list1.room[loopi]
                   trm1[loopi]                      = trm1[loopi] + output-list1.room[loopi]
                   trev1[loopi]                     = trev1[loopi] + output-list1.revenue[loopi]
             .
            IF output-list1.avrg-rev[loopi] = ? THEN ASSIGN output-list1.avrg-rev[loopi] = 0.
        END.
        ASSIGN output-list1.check-flag = NO.
    END.
    
    CREATE boutput1.
    ASSIGN counter                     = counter + 1
           boutput1.counter            = counter                        
           boutput1.segment            = "TOTAL"
     .

    DO loopi = 1 TO 12:
          ASSIGN
               boutput1.room[loopi]        = trm1[loopi]
               boutput1.revenue[loopi]     = trev1[loopi]
               boutput1.avrg-rev[loopi]    = trev1[loopi] / trm1[loopi]           
          .
          IF boutput1.avrg-rev[loopi] = ? THEN ASSIGN boutput1.avrg-rev[loopi] = 0.

    END.
END.


PROCEDURE create-browse:
    DEFINE VARIABLE datum            AS DATE.
    DEFINE VARIABLE datum1           AS DATE. 
    DEFINE VARIABLE datum2           AS DATE. 
    DEFINE VARIABLE tdate            AS DATE.
    DEFINE VARIABLE fdate            AS DATE.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VAR tot-vat               AS DECIMAL INITIAL 0.
    DEFINE VAR tot-service           AS DECIMAL INITIAL 0.

    IF to-date LT (ci-date - 1) THEN tdate = to-date. 
    ELSE tdate = ci-date - 1. 
    
    FOR EACH genstat WHERE genstat.datum GE fr-date 
           AND genstat.datum LE tdate
           AND genstat.segmentcode NE 0
           AND genstat.nationnr NE 0
           AND genstat.zinr NE ""
           AND genstat.res-logic[2] EQ YES 
           AND genstat.resstatus NE 13
           NO-LOCK USE-INDEX gastnrmember_ix, 
           FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode
           AND segment.segmentcode NE black-list BY genstat.segmentcode:  
    
         FIND FIRST output-list WHERE output-list.segmentcode = genstat.segmentcode
             AND output-list.datum = genstat.datum NO-ERROR.
         IF NOT AVAILABLE output-list THEN DO:
             CREATE output-list.
             ASSIGN output-list.segmentcode = genstat.segmentcode
                    output-list.datum       = genstat.datum
                    output-list.segment     = segment.bezeich
                    output-list.check-flag   = YES
              .
         END.
         ASSIGN output-list.room    = output-list.room + 1
                output-list.revenue = output-list.revenue + genstat.logis.            
    END.

    ASSIGN fdate = tdate + 1.
    IF to-date GE ci-date THEN DO:
        FOR EACH res-line WHERE ((res-line.resstatus LE 13 
            AND res-line.resstatus NE 4
            /*AND res-line.resstatus NE 8*/
            AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12 
            AND res-line.active-flag LE 1 
            AND NOT (res-line.ankunft GT to-date) 
            AND NOT (res-line.abreise LT fdate))) OR
            (res-line.resstatus = 8 AND res-line.active-flag = 2
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK 
            USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending: 
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                AND segment.segmentcode NE black-list NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN DO:
                IF ex-tent THEN  /*william F4BC9C*/
                DO:
                    IF res-line.resstatus EQ 3 THEN NEXT.
                END.              
                IF ex-comp THEN  /*william F4BC9C*/
                DO:
                    IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN NEXT.
                END.
                IF (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND NOT ex-tent)) /*william F4BC9C*/
                AND res-line.resstatus NE 4 /*AND (res-line.abreise GT res-line.ankunft OR (res-line.ankunft LE res-line.abreise OR dayuse-flag))*/
                AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                DO:
                  datum1 = fdate. 
                  IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
                  datum2 = to-date. 
                  IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.
    
                  DO datum = datum1 TO datum2:
                     ASSIGN 
                         net-lodg      = 0
                         curr-i        = curr-i + 1.

                     IF datum = res-line.abreise THEN .
                     ELSE DO:
                        ASSIGN net-lodg      = 0
                               tot-breakfast = 0
                               tot-lunch     = 0
                               tot-dinner    = 0
                               tot-other     = 0
                               tot-rmrev     = 0
                               tot-vat       = 0
                               tot-service   = 0
                          . 

                        RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, fr-date,
                                                 OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                 OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                 OUTPUT tot-dinner, OUTPUT tot-other,
                                                 OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                 OUTPUT tot-service).  

                         FIND FIRST output-list WHERE output-list.segmentcode = reservation.segmentcode
                             AND output-list.datum = datum NO-ERROR.
                         IF NOT AVAILABLE output-list THEN DO:
                             CREATE output-list.
                             ASSIGN output-list.segmentcode = reservation.segmentcode
                                    output-list.datum       = datum
                                    output-list.segment     = segment.bezeich
                                    output-list.check-flag   = YES
                              .
                         END.
                         ASSIGN output-list.room    = output-list.room + res-line.zimmeranz.
                                output-list.revenue = output-list.revenue + net-lodg.      

                     END.   
                  END.
                END.
            END.              
        END.
    END.
END.

PROCEDURE create-browse1:
    DEFINE VARIABLE datum            AS DATE.
    DEFINE VARIABLE datum1           AS DATE. 
    DEFINE VARIABLE datum2           AS DATE. 
    DEFINE VARIABLE tdate            AS DATE.
    DEFINE VARIABLE fdate            AS DATE.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VAR tot-vat               AS DECIMAL INITIAL 0.
    DEFINE VAR tot-service           AS DECIMAL INITIAL 0.

    
    FOR EACH res-line WHERE (res-line.resstatus LE 13 
        AND res-line.resstatus NE 4
        /*AND res-line.resstatus NE 8*/
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT fr-date)) OR
        (res-line.resstatus = 8 AND res-line.active-flag = 2
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK 
        USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending: 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            AND segment.segmentcode NE black-list NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN DO:
            IF ex-tent THEN  /*william F4BC9C*/
            DO:
                IF res-line.resstatus EQ 3 THEN NEXT.
            END.              
            IF ex-comp THEN  /*william F4BC9C*/
            DO:
                IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN NEXT.
            END.
            IF (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND NOT ex-tent)) /*william F4BC9C*/
            AND res-line.resstatus NE 4 /*AND (res-line.abreise GT res-line.ankunft OR (res-line.ankunft LE res-line.abreise OR dayuse-flag))*/
            AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
            DO:
              datum1 = fr-date. 
              IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
              datum2 = to-date. 
              IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

              DO datum = datum1 TO datum2:
                 ASSIGN 
                     net-lodg      = 0
                     curr-i        = curr-i + 1.

                 IF datum = res-line.abreise THEN .
                 ELSE DO:
                    ASSIGN net-lodg      = 0
                           tot-breakfast = 0
                           tot-lunch     = 0
                           tot-dinner    = 0
                           tot-other     = 0
                           tot-rmrev     = 0
                           tot-vat       = 0
                           tot-service   = 0
                      . 

                    RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, fr-date,
                                             OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                             OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                             OUTPUT tot-dinner, OUTPUT tot-other,
                                             OUTPUT tot-rmrev, OUTPUT tot-vat,
                                             OUTPUT tot-service).  

                     FIND FIRST output-list WHERE output-list.segmentcode = reservation.segmentcode
                         AND output-list.datum = datum NO-ERROR.
                     IF NOT AVAILABLE output-list THEN DO:
                         CREATE output-list.
                         ASSIGN output-list.segmentcode = reservation.segmentcode
                                output-list.datum       = datum
                                output-list.segment     = segment.bezeich
                                output-list.check-flag   = YES
                          .
                     END.
                     ASSIGN output-list.room    = output-list.room + res-line.zimmeranz.
                            output-list.revenue = output-list.revenue + net-lodg.      

                 END.   
              END.
           END.
        END.              
    END.
END.


PROCEDURE create-browse2:
    DEFINE VARIABLE datum            AS DATE.
    DEFINE VARIABLE datum1           AS DATE. 
    DEFINE VARIABLE datum2           AS DATE. 
    DEFINE VARIABLE tdate            AS DATE.
    DEFINE VARIABLE fdate            AS DATE.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VAR tot-vat               AS DECIMAL INITIAL 0.
    DEFINE VAR tot-service           AS DECIMAL INITIAL 0.
    DEFINE VARIABLE frdate           AS DATE NO-UNDO.
    DEFINE VARIABLE todate           AS DATE NO-UNDO.

    
    ASSIGN frdate   = DATE(1,1, to-year)
           todate   = DATE(12,31, to-year)
           tdate    = ci-date - 1.
    
    FOR EACH genstat WHERE genstat.datum GE frdate 
           AND genstat.datum LE tdate
           AND genstat.segmentcode NE 0
           AND genstat.nationnr NE 0
           AND genstat.zinr NE ""
           AND genstat.res-logic[2] EQ YES 
           AND genstat.resstatus NE 13
           NO-LOCK USE-INDEX gastnrmember_ix, 
           FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode
           AND segment.segmentcode NE black-list BY genstat.segmentcode:  
    
         FIND FIRST output-list1 WHERE output-list1.segmentcode = genstat.segmentcode NO-ERROR.
         IF NOT AVAILABLE output-list1 THEN DO:
             CREATE output-list1.
             ASSIGN output-list1.segmentcode = genstat.segmentcode                    
                    output-list1.segment     = segment.bezeich
                    output-list1.check-flag   = YES
              .
         END.
         ASSIGN output-list1.room[MONTH(genstat.datum)] = output-list1.room[MONTH(genstat.datum)] + 1
                output-list1.revenue[MONTH(genstat.datum)] = output-list1.revenue[MONTH(genstat.datum)] + genstat.logis.            
    END.


    ASSIGN fdate = tdate + 1.
    IF to-date GE ci-date THEN DO:
        FOR EACH res-line WHERE ((res-line.resstatus LE 13 
            AND res-line.resstatus NE 4
            /*AND res-line.resstatus NE 8*/
            AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12 
            AND res-line.active-flag LE 1 
            AND NOT (res-line.ankunft GT todate) 
            AND NOT (res-line.abreise LT fdate))) OR
            (res-line.resstatus = 8 AND res-line.active-flag = 2
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK 
            USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending: 
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
                AND segment.segmentcode NE black-list NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN DO:
                IF ex-tent THEN  /*william F4BC9C*/
                DO:
                    IF res-line.resstatus EQ 3 THEN NEXT.
                END.              
                IF ex-comp THEN  /*william F4BC9C*/
                DO:
                    IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN NEXT.
                END.
                IF (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND NOT ex-tent)) /*william F4BC9C*/
                AND res-line.resstatus NE 4 /*AND (res-line.abreise GT res-line.ankunft OR (res-line.ankunft LE res-line.abreise OR dayuse-flag))*/
                AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
                DO:
                  datum1 = fdate. 
                  IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
                  datum2 = todate. 
                  IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.
    
                  DO datum = datum1 TO datum2:
                     ASSIGN 
                         net-lodg      = 0
                         curr-i        = curr-i + 1.

                     IF datum = res-line.abreise THEN .
                     ELSE DO:
                        ASSIGN net-lodg      = 0
                               tot-breakfast = 0
                               tot-lunch     = 0
                               tot-dinner    = 0
                               tot-other     = 0
                               tot-rmrev     = 0
                               tot-vat       = 0
                               tot-service   = 0
                          . 

                        RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, fr-date,
                                                 OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                 OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                 OUTPUT tot-dinner, OUTPUT tot-other,
                                                 OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                 OUTPUT tot-service).  
                         
                         FIND FIRST output-list1 WHERE output-list1.segmentcode = reservation.segmentcode NO-ERROR.
                         IF NOT AVAILABLE output-list1 THEN DO:
                             CREATE output-list1.
                             ASSIGN output-list1.segmentcode = reservation.segmentcode
                                    output-list1.segment     = segment.bezeich
                                    output-list1.check-flag   = YES
                              .
                         END.
                         ASSIGN output-list1.room[MONTH(datum)] = output-list1.room[MONTH(datum)] + res-line.zimmeranz.
                                output-list1.revenue[MONTH(datum)] = output-list1.revenue[MONTH(datum)] + net-lodg.      

                     END.   
                  END.
                END.
            END.              
        END.
    END.
END.

PROCEDURE create-browse3:
    DEFINE VARIABLE datum            AS DATE.
    DEFINE VARIABLE datum1           AS DATE. 
    DEFINE VARIABLE datum2           AS DATE. 
    DEFINE VARIABLE tdate            AS DATE.
    DEFINE VARIABLE fdate            AS DATE.
    DEFINE VARIABLE tot-breakfast    AS DECIMAL.
    DEFINE VARIABLE tot-Lunch        AS DECIMAL.
    DEFINE VARIABLE tot-dinner       AS DECIMAL.
    DEFINE VARIABLE tot-Other        AS DECIMAL.
    DEFINE VARIABLE curr-i           AS INTEGER.
    DEFINE VARIABLE net-lodg         AS DECIMAL.
    DEFINE VARIABLE Fnet-lodg        AS DECIMAL.
    DEFINE VARIABLE tot-rmrev        AS DECIMAL INITIAL 0.
    DEFINE VAR tot-vat               AS DECIMAL INITIAL 0.
    DEFINE VAR tot-service           AS DECIMAL INITIAL 0.
    DEFINE VARIABLE frdate           AS DATE NO-UNDO.
    DEFINE VARIABLE todate           AS DATE NO-UNDO.

    
    ASSIGN frdate   = DATE(1,1, to-year)
           todate   = DATE(12,31, to-year)
    .

    
    FOR EACH res-line WHERE ((res-line.resstatus LE 13 
        AND res-line.resstatus NE 4
        /*AND res-line.resstatus NE 8*/
        AND res-line.resstatus NE 9 
        AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 12 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT todate) 
        AND NOT (res-line.abreise LT frdate))) OR
        (res-line.resstatus = 8 AND res-line.active-flag = 2
        AND res-line.ankunft = ci-date AND res-line.abreise = ci-date)
        AND res-line.gastnr GT 0 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK 
        USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending: 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            AND segment.segmentcode NE black-list NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN DO:
            IF ex-tent THEN  /*william F4BC9C*/
            DO:
                IF res-line.resstatus EQ 3 THEN NEXT.
            END.              
            IF ex-comp THEN  /*william F4BC9C*/
            DO:
                IF res-line.erwachs = 0 AND res-line.gratis GT 0 AND res-line.zipreis = 0 THEN NEXT.
            END.
            IF (res-line.resstatus NE 3 OR (res-line.resstatus = 3 AND NOT ex-tent)) /*william F4BC9C*/
            AND res-line.resstatus NE 4 /*AND (res-line.abreise GT res-line.ankunft OR (res-line.ankunft LE res-line.abreise OR dayuse-flag))*/
            AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN
            DO:
              datum1 = frdate. 
              IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
              datum2 = todate. 
              IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

              DO datum = datum1 TO datum2:
                 ASSIGN 
                     net-lodg      = 0
                     curr-i        = curr-i + 1.

                 IF datum = res-line.abreise THEN .
                 ELSE DO:
                    ASSIGN net-lodg      = 0
                           tot-breakfast = 0
                           tot-lunch     = 0
                           tot-dinner    = 0
                           tot-other     = 0
                           tot-rmrev     = 0
                           tot-vat       = 0
                           tot-service   = 0
                      . 

                    RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, fr-date,
                                             OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                             OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                             OUTPUT tot-dinner, OUTPUT tot-other,
                                             OUTPUT tot-rmrev, OUTPUT tot-vat,
                                             OUTPUT tot-service).  

                     FIND FIRST output-list1 WHERE output-list1.segmentcode = reservation.segmentcode NO-ERROR.
                     IF NOT AVAILABLE output-list1 THEN DO:
                         CREATE output-list1.
                         ASSIGN output-list1.segmentcode = reservation.segmentcode
                                output-list1.segment     = segment.bezeich
                                output-list1.check-flag   = YES
                          .
                     END.
                     ASSIGN output-list1.room[MONTH(datum)]    = output-list1.room[MONTH(datum)] + res-line.zimmeranz.
                            output-list1.revenue[MONTH(datum)] = output-list1.revenue[MONTH(datum)] + net-lodg.      

                 END.   
              END.
            END.
        END.              
    END.
END.


