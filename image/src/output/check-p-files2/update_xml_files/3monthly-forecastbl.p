DEFINE TEMP-TABLE output-list
    FIELD datum         AS DATE
    FIELD smonth        AS INTEGER
    FIELD rmSold        AS INTEGER
    FIELD ooo           AS INTEGER
    FIELD comp          AS INTEGER
    FIELD houseUse      AS INTEGER
    FIELD rmRevenue     AS DECIMAL  
    FIELD percent-occ   AS DECIMAL
.

DEFINE TEMP-TABLE output-list1 LIKE output-list
    FIELD counter       AS INTEGER
    FIELD sdate         AS CHAR
    FIELD avrgRevenue   AS DECIMAL.


DEFINE TEMP-TABLE active-rm-list
    FIELD datum     AS DATE
    FIELD zimmeranz AS INTEGER INIT 0
.

DEFINE INPUT PARAMETER fmonth AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER tmonth AS CHAR NO-UNDO.

DEFINE OUTPUT PARAMETE TABLE FOR output-list1.

DEFINE VARIABLE bill-date AS DATE NO-UNDO.
DEFINE VARIABLE fdate     AS DATE NO-UNDO.
DEFINE VARIABLE tdate     AS DATE NO-UNDO.
DEFINE VARIABLE fmm        AS INTEGER NO-UNDO.
DEFINE VARIABLE fyy        AS INTEGER NO-UNDO.
DEFINE VARIABLE tmm        AS INTEGER NO-UNDO.
DEFINE VARIABLE tyy        AS INTEGER NO-UNDO.
DEFINE VARIABLE datum      AS DATE    NO-UNDO.
DEFINE VARIABLE datum1     AS DATE    NO-UNDO.
DEFINE VARIABLE datum2     AS DATE    NO-UNDO.
DEFINE VARIABLE datum3     AS DATE    NO-UNDO.

DEFINE VARIABLE curr-i      AS INTEGER.
DEFINE VARIABLE net-lodg    AS DECIMAL.
DEFINE VARIABLE Fnet-lodg   AS DECIMAL.

DEFINE VAR tot-breakfast    AS DECIMAL.
DEFINE VAR tot-Lunch        AS DECIMAL.
DEFINE VAR tot-dinner       AS DECIMAL.
DEFINE VAR tot-Other        AS DECIMAL.
DEFINE VAR tot-rmrev        AS DECIMAL INITIAL 0.
DEFINE VAR tot-vat          AS DECIMAL INITIAL 0.
DEFINE VAR tot-service      AS DECIMAL INITIAL 0.
DEFINE VARIABLE actual-tot-room AS INTEGER. 

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
ASSIGN bill-date = htparam.fdate.

DEFINE BUFFER boutput FOR output-list.



ASSIGN fmm   = INTEGER(ENTRY(1, fmonth, "/"))
       fyy   = INTEGER(ENTRY(2, fmonth, "/"))
       tmm   = INTEGER(ENTRY(1, tmonth, "/"))
       tyy   = INTEGER(ENTRY(2, tmonth, "/"))
       fdate = DATE(fmm, 1, fyy).
  .

IF tmm + 1 GT 12 THEN
    ASSIGN tdate = DATE(1,1, tyy + 1) - 1.
ELSE ASSIGN tdate = DATE(tmm + 1,1, tyy) - 1.


IF fdate LT bill-date THEN DO:
    
    ASSIGN datum1 = fdate.
    
    IF datum1 LT bill-date THEN DO:
        IF tdate LT (bill-date - 1) THEN datum2 = tdate.
        ELSE datum2 = bill-date - 1.
    END.
    ELSE datum2 = tdate.


    FOR EACH genstat WHERE genstat.datum GE datum1 
         AND genstat.datum LE datum2 
         AND genstat.resstatus NE 13
         AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
         AND genstat.zinr NE "" USE-INDEX date_ix NO-LOCK:

         FIND FIRST output-list WHERE output-list.datum = genstat.datum NO-ERROR.
         IF NOT AVAILABLE output-list THEN DO:
             CREATE output-list.
             ASSIGN output-list.datum  = genstat.datum
                    output-list.smonth = MONTH(genstat.datum)
             .
         END.

         ASSIGN output-list.rmSold = output-list.rmSold + 1
                output-list.rmRevenue = output-list.rmRevenue + genstat.logis
          .

         FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
         IF AVAILABLE segment AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) THEN DO:
             IF segment.betriebsnr = 1 THEN ASSIGN output-list.comp = output-list.comp + 1.
             ELSE IF segment.betriebsnr = 2 THEN ASSIGN output-list.houseUse = output-list.houseUse + 1.
         END.
         ELSE DO:
             IF genstat.zipreis = 0 AND genstat.gratis NE 0
                     AND genstat.resstatus = 6
                     AND genstat.res-logic[2] THEN ASSIGN output-list.comp = output-list.comp + 1.
         END.
    END.

    IF tdate GE bill-date THEN DO:
         FOR EACH res-line WHERE ((res-line.resstatus LE 13 
             AND res-line.resstatus NE 4
             AND res-line.resstatus NE 8
             AND res-line.resstatus NE 9 
             AND res-line.resstatus NE 10 
             AND res-line.resstatus NE 12 
             AND res-line.resstatus NE 3
             AND res-line.resstatus NE 13
             AND res-line.resstatus NE 11
             AND res-line.active-flag LE 1 
             AND NOT (res-line.ankunft GT tdate) 
             AND NOT (res-line.abreise LT bill-date))) OR
             ((res-line.active-flag = 2 AND res-line.resstatus = 8
             AND res-line.ankunft = bill-date AND res-line.abreise = bill-date) OR 
             (res-line.active-flag = 2 AND res-line.resstatus = 8 
             AND res-line.abreise = bill-date))
             AND res-line.gastnr GT 0 
             AND res-line.l-zuordnung[3] = 0 NO-LOCK 
             USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending: 
             FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
                 NO-ERROR.

             datum1 = bill-date.
             IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
             datum2 = tdate. 
             IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

             DO datum3 = datum1 TO datum2:
                 IF datum3 = res-line.abreise THEN .
                 ELSE DO:
                     FIND FIRST output-list WHERE output-list.datum = datum3 NO-ERROR.
                     IF NOT AVAILABLE output-list THEN DO:
                         CREATE output-list.
                         ASSIGN output-list.datum  = datum3
                                output-list.smonth = MONTH(datum3)
                         .
                     END.
    
                     ASSIGN net-lodg      = 0
                            Fnet-lodg     = 0
                            tot-breakfast = 0
                            tot-lunch     = 0
                            tot-dinner    = 0
                            tot-other     = 0
                      . 
                     
                     IF res-line.zipreis GT 0 THEN
                         RUN get-room-breakdown.p(RECID(res-line), datum3, curr-i, bill-date,
                                                  OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                  OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                  OUTPUT tot-dinner, OUTPUT tot-other,
                                                  OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                  OUTPUT tot-service).   

                     IF net-lodg = ? THEN ASSIGN net-lodg = 0.
                     IF tot-rmrev = ? THEN ASSIGN tot-rmrev = 0.

                     IF res-line.resstatus NE 11 AND res-line.resstatus NE 13
                        AND NOT res-line.zimmerfix THEN
                         ASSIGN output-list.rmSold    = output-list.rmSold + res-line.zimmeranz
                                output-list.rmRevenue = output-list.rmRevenue + net-lodg
                          .
                         
    
                     FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                     IF AVAILABLE segment AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) THEN DO:
                         IF segment.betriebsnr = 1 THEN ASSIGN output-list.comp = output-list.comp + 1.
                         ELSE IF segment.betriebsnr = 2 THEN ASSIGN output-list.houseUse = output-list.houseUse + res-line.zimmeranz.
                     END.
                     ELSE DO:
                         IF res-line.zipreis = 0 AND res-line.gratis NE 0 THEN ASSIGN output-list.comp = output-list.comp + res-line.zimmeranz.
                     END.
                 END.                 
             END.
         END.
    END.
END.
ELSE DO:

        FOR EACH res-line WHERE ((res-line.resstatus LE 13 
             AND res-line.resstatus NE 4
             AND res-line.resstatus NE 8
             AND res-line.resstatus NE 9 
             AND res-line.resstatus NE 10 
             AND res-line.resstatus NE 12 
             AND res-line.resstatus NE 3
             AND res-line.resstatus NE 13
             AND res-line.resstatus NE 11
             AND res-line.active-flag LE 1 
             AND NOT (res-line.ankunft GT tdate) 
             AND NOT (res-line.abreise LT fdate))) OR
             ((res-line.active-flag = 2 AND res-line.resstatus = 8
             AND res-line.ankunft = bill-date AND res-line.abreise = bill-date) OR 
             (res-line.active-flag = 2 AND res-line.resstatus = 8 
             AND res-line.abreise = bill-date))
             AND res-line.gastnr GT 0 
             AND res-line.l-zuordnung[3] = 0 NO-LOCK 
             USE-INDEX gnrank_ix BY res-line.resnr BY res-line.reslinnr descending: 
             FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
                 NO-ERROR.

             datum1 = fdate.
             IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
             datum2 = tdate. 
             IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise.

             DO datum3 = datum1 TO datum2:

                 IF datum3 = res-line.abreise THEN .
                 ELSE DO:
                     FIND FIRST output-list WHERE output-list.datum = datum3 NO-ERROR.
                     IF NOT AVAILABLE output-list THEN DO:
                         CREATE output-list.
                         ASSIGN output-list.datum  = datum3
                                output-list.smonth = MONTH(datum3)
                         .
                     END.
    
                     ASSIGN net-lodg      = 0
                            Fnet-lodg     = 0
                            tot-breakfast = 0
                            tot-lunch     = 0
                            tot-dinner    = 0
                            tot-other     = 0
                            curr-i        = curr-i + 1
                      . 

                     IF res-line.zipreis GT 0 THEN
                         RUN get-room-breakdown.p(RECID(res-line), datum3, curr-i, fdate,
                                                  OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                                  OUTPUT tot-breakfast, OUTPUT tot-lunch,
                                                  OUTPUT tot-dinner, OUTPUT tot-other,
                                                  OUTPUT tot-rmrev, OUTPUT tot-vat,
                                                  OUTPUT tot-service).  

                     IF net-lodg = ? THEN ASSIGN net-lodg = 0.
                     IF tot-rmrev = ? THEN ASSIGN tot-rmrev = 0.
                    
                     IF res-line.resstatus NE 11 AND res-line.resstatus NE 13
                        AND NOT res-line.zimmerfix THEN
                             ASSIGN output-list.rmSold    = output-list.rmSold + res-line.zimmeranz
                                    output-list.rmRevenue = output-list.rmRevenue + net-lodg
                              .
    
                     FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                     IF AVAILABLE segment AND (segment.betriebsnr = 1 OR segment.betriebsnr = 2) THEN DO:
                         IF segment.betriebsnr = 1 THEN ASSIGN output-list.comp = output-list.comp + 1.
                         ELSE IF segment.betriebsnr = 2 THEN ASSIGN output-list.houseUse = output-list.houseUse + res-line.zimmeranz.
                     END.
                     ELSE DO:
                         IF res-line.zipreis = 0 AND res-line.gratis NE 0 THEN ASSIGN output-list.comp = output-list.comp + res-line.zimmeranz.
                     END.
                 END.
             END.
         END.
END.



DO datum = fdate TO tdate:
    IF datum LT bill-date THEN DO:
        FIND FIRST zinrstat WHERE zinrstat.zinr = "ooo" AND zinrstat.datum = datum NO-LOCK NO-ERROR.
        IF AVAILABLE zinrstat THEN DO:
            FIND FIRST output-list WHERE output-list.datum = datum NO-ERROR.
            IF NOT AVAILABLE output-list THEN DO:
                CREATE output-list.
                ASSIGN output-list.datum  = datum
                       output-list.smonth = MONTH(datum)
                .
            END.
            ASSIGN output-list.ooo    = output-list.ooo + zinrstat.zimmeranz.
        END.
    END.
    ELSE DO:
        FOR EACH outorder WHERE outorder.betriebsnr LE 1
            AND datum GE outorder.gespstart AND datum LE outorder.gespende NO-LOCK, 
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping = YES NO-LOCK:
    
            FIND FIRST output-list WHERE output-list.datum = datum NO-ERROR.
            IF NOT AVAILABLE output-list THEN DO:
                CREATE output-list.
                ASSIGN output-list.datum  = datum
                       output-list.smonth = MONTH(datum)
                .
            END.
            ASSIGN output-list.ooo    = output-list.ooo + 1.
        END.
    END.
    
    
    FIND FIRST boutput WHERE boutput.datum = datum NO-LOCK NO-ERROR.
    IF NOT AVAILABLE boutput THEN DO:
        CREATE boutput.
        ASSIGN boutput.datum  = datum
               boutput.smonth = MONTH(datum)
               boutput.rmSold      = 0
               boutput.ooo         = 0
               boutput.comp        = 0
               boutput.houseUse    = 0
               boutput.rmRevenue   = 0               
        .
    END.

END.

DEFINE VARIABLE curr-month AS INTEGER NO-UNDO.
DEFINE VARIABLE  tot-rmSold      AS DECIMAL NO-UNDO.
DEFINE VARIABLE  tot-ooo         AS DECIMAL NO-UNDO.
DEFINE VARIABLE  tot-comp        AS DECIMAL NO-UNDO.
DEFINE VARIABLE  tot-houseUse    AS DECIMAL NO-UNDO.
DEFINE VARIABLE  tot-rmRevenue   AS DECIMAL NO-UNDO.
DEFINE VARIABLE  tot-avrgRevenue AS DECIMAL NO-UNDO.
DEFINE VARIABLE  tot-room        AS INTEGER NO-UNDO.
DEFINE VARIABLE  tot-zinr        AS INTEGER NO-UNDO.

actual-tot-room = 0. 
FOR EACH zimmer WHERE sleeping NO-LOCK: 
    ASSIGN actual-tot-room = actual-tot-room + 1. 
END. 
RUN create-active-room-list.

FOR EACH output-list BY output-list.datum:
    IF curr-month NE 0 AND curr-month NE MONTH(output-list.datum) THEN DO:
        CREATE output-list1.
        ASSIGN counter                  = counter + 1
               output-list1.counter     = counter
               output-list1.sdate       = "T O T A L"
               output-list1.smonth      = curr-month
               output-list1.rmSold      = tot-rmSold
               output-list1.ooo         = tot-ooo
               output-list1.comp        = tot-comp
               output-list1.houseUse    = tot-houseUse
               output-list1.rmRevenue   = tot-rmRevenue
               output-list1.avrgRevenue = output-list1.rmRevenue / output-list1.rmSold 
               output-list1.percent-occ = output-list1.rmSold / tot-zinr * 100
               
               tot-rmSold           = 0   
               tot-ooo              = 0
               tot-comp             = 0
               tot-houseUse         = 0
               tot-rmRevenue        = 0
               tot-avrgRevenue      = 0
               tot-zinr             = 0
          .              
    END.

    RUN get-active-room(datum, OUTPUT tot-room).
    
    CREATE output-list1.
    BUFFER-COPY output-list TO output-list1.
    ASSIGN counter                  = counter + 1
           output-list1.counter     = counter
           output-list1.sdate       = STRING(output-list.datum)
           output-list1.avrgRevenue = output-list.rmRevenue / output-list.rmSold
           output-list1.percent-occ = output-list.rmSold / tot-room * 100
           curr-month               = MONTH(output-list.datum)

           tot-rmSold              = tot-rmSold      + output-list1.rmSold
           tot-ooo                 = tot-ooo         + output-list1.ooo
           tot-comp                = tot-comp        + output-list1.comp
           tot-houseUse            = tot-houseUse    + output-list1.houseUse
           tot-rmRevenue           = tot-rmRevenue   + output-list1.rmRevenue 
           tot-avrgRevenue         = tot-avrgRevenue + output-list1.avrgRevenue
           tot-zinr                = tot-zinr        + tot-room
     .
END.

CREATE output-list1.
ASSIGN counter                  = counter + 1
       output-list1.counter     = counter
       output-list1.sdate       = "T O T A L"
       output-list1.smonth      = curr-month
       output-list1.rmSold      = tot-rmSold
       output-list1.ooo         = tot-ooo
       output-list1.comp        = tot-comp
       output-list1.houseUse    = tot-houseUse
       output-list1.rmRevenue   = tot-rmRevenue
       output-list1.avrgRevenue = output-list1.rmRevenue / output-list1.rmSold 
       output-list1.percent-occ = output-list1.rmSold / tot-zinr * 100
.


PROCEDURE get-active-room:
DEFINE INPUT  PARAMETER curr-datum  AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER active-room AS INTEGER NO-UNDO INIT 0.
  IF curr-datum GE bill-date THEN
  DO:
    active-room = actual-tot-room.
    RETURN.
  END.
  FIND FIRST active-rm-list WHERE active-rm-list.datum = curr-datum
      NO-ERROR.
  IF AVAILABLE active-rm-list THEN active-room = active-rm-list.zimmeranz.
END.


PROCEDURE create-active-room-list:
DEF VAR end-date    AS DATE NO-UNDO.
DEF VAR actual-date AS DATE NO-UNDO INIT ?.

  IF tdate LT bill-date THEN end-date = tdate.
  ELSE end-date = bill-date - 1.

  FOR EACH zkstat WHERE zkstat.datum GE fdate
    AND zkstat.datum LE end-date NO-LOCK BY zkstat.datum:
    IF actual-date NE zkstat.datum THEN
    DO:
      CREATE active-rm-list.
      ASSIGN 
        active-rm-list.datum     = zkstat.datum
        actual-date              = zkstat.datum
      .
    END.
    active-rm-list.zimmeranz = active-rm-list.zimmeranz + zkstat.anz100.
  END.
END.



