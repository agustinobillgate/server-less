
DEFINE TEMP-TABLE na-list 
  FIELD reihenfolge AS INTEGER 
  FIELD flag AS INTEGER 
  FIELD anz AS INTEGER 
  FIELD bezeich LIKE nightaudit.bezeichnung. 

DEF INPUT  PARAMETER case-type     AS INTEGER.
DEF INPUT  PARAMETER pvILanguage   AS INTEGER      NO-UNDO.
DEF OUTPUT PARAMETER mn-stopped    AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER stop-it       AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER arrival-guest AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER msg-str       AS CHAR.
DEF OUTPUT PARAMETER mess-str      AS CHAR.
DEF OUTPUT PARAMETER crm-license   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER banquet-license AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR na-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mn-start".

DEFINE VARIABLE ci-date             AS DATE.
DEFINE VARIABLE new-contrate        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE contcode            AS CHAR NO-UNDO.
DEFINE VARIABLE created-date        AS DATE NO-UNDO.

DEFINE VARIABLE wd-array AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 985 no-lock.  /* License Banquet */ 
IF htparam.flogical THEN ASSIGN banquet-license = YES.

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs AS INTEGER, 
     INPUT kind1 AS INTEGER, 
     INPUT kind2 AS INTEGER). 
  DEF VAR rate AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN 
      rate = rate + katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. 

IF case-type = 1 THEN
DO:
    FIND FIRST htparam WHERE paramnr = 105 NO-LOCK. /* LAST midnight */ 
    IF htparam.fdate GE TODAY THEN 
    DO:
      mn-stopped = YES.
      RETURN. 
    END.

    RUN check-license-date.
    IF stop-it THEN 
    DO:
      mn-stopped = YES.
      STOP. 
    END.

    RUN check-room-sharers.
    IF stop-it THEN
    DO:
      mn-stopped = YES.
      RETURN. 
    END.

    FIND FIRST htparam WHERE htparam.paramnr = 208 NO-LOCK.
    IF NOT htparam.flogical THEN
    DO:
      mess-str = translateExtended ("Checking Opened Master Bill.",lvCAREA,""). 

      FOR EACH bill WHERE bill.flag = 0 AND bill.resnr GT 0 AND bill.reslinnr = 0
        NO-LOCK:
        FIND FIRST res-line WHERE res-line.resnr = bill.resnr
          AND res-line.active-flag LE 1
          AND res-line.resstatus NE 8
          AND res-line.resstatus NE 9
          AND res-line.resstatus NE 10 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE res-line THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK.
            msg-str = msg-str + CHR(2)
                    + translateExtended ("Opened master bill found but all guests checked-out:",lvCAREA,"")
                    + " " + STRING(bill.rechnr) + " - " + guest.NAME
                    + CHR(10)
                    + translateExtended ("Midnight Program stopped.",lvCAREA,"").
            mn-stopped = YES.
            RETURN.
        END.
      END.
    END.

    /*checking roomRate*/
    RUN check-room-rate.
    IF stop-it THEN
    DO:
      mn-stopped = YES.
      RETURN. 
    END.

    RUN check-today-arrival-guest.
    IF stop-it THEN RETURN. 
    ELSE case-type = 2.
END.

IF case-type = 2 THEN
DO:
    RUN midnite-prog.
    FIND FIRST htparam WHERE htparam.paramnr = 1459 NO-LOCK. /* CRM license */
    IF htparam.paramgr = 99 AND htparam.flogical THEN crm-license = YES.
    /*MTRUN chg-sysdates.*/
END.


/***********************************************************/
PROCEDURE check-license-date: 
  FIND FIRST htparam WHERE paramnr = 976 NO-LOCK. 
  IF htparam.fdate NE ? THEN 
  DO: 
    IF htparam.fdate LT today THEN 
    DO: 
      stop-it = YES. 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Your License was valid until",lvCAREA,"") + " "
              + STRING(htparam.fdate) + " " + translateExtended ("only.",lvCAREA,"")
              + CHR(10)
              + translateExtended ("Please contact your next Our Technical Support for further information.",lvCAREA,"").
    END. 
  END. 
  ELSE stop-it = YES.

  IF stop-it THEN 
  DO:
    FIND FIRST htparam WHERE htparam.paramnr = 999 NO-LOCK. 
    IF htparam.flogical THEN 
    DO TRANSACTION: 
      FIND FIRST htparam WHERE htparam.paramnr = 996 EXCLUSIVE-LOCK. 
      htparam.fchar = "". 
      FIND CURRENT htparam NO-LOCK. 
    END. 
  END. 
END. 

PROCEDURE check-today-arrival-guest:
DEFINE VARIABLE answer AS LOGICAL INITIAL NO NO-UNDO.
    FIND FIRST res-line WHERE res-line.active-flag = 0
        AND (res-line.resstatus LE 2 OR res-line.resstatus = 5
        OR res-line.resstatus = 11)
        AND res-line.ankunft = ci-date NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        msg-str = msg-str + CHR(2) + "&Q"
                + translateExtended ("Today's arrival guest(s) record found.",lvCAREA,"")
                + CHR(10)
                + translateExtended ("Are you sure you want to proceed the Midnight Program?",lvCAREA,"").
        arrival-guest = YES.
        stop-it = YES.
        RETURN.
    END.
END.

PROCEDURE check-room-sharers:
DEF BUFFER rbuff FOR res-line.
    FOR EACH res-line WHERE res-line.active-flag = 1 AND res-line.resstatus = 13
        AND res-line.l-zuordnung[3] = 0 NO-LOCK:
        FIND FIRST rbuff WHERE rbuff.active-flag = 1 AND rbuff.zinr = res-line.zinr
            AND rbuff.resstatus = 6 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE rbuff THEN
        DO:
            msg-str = msg-str + CHR(2)
                    + translateExtended ("Difference Rate between Reservation and Fixed Rate found. The Night Audit process not posibble.",lvCAREA,"").
            stop-it = YES.
            RETURN.
        END.
    END.
END.

PROCEDURE check-room-rate:
    DEF BUFFER rbuff FOR res-line.
    DEFINE VARIABLE cdate AS DATE NO-UNDO.

    FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
    cdate = htparam.fdate.

    FOR EACH res-line WHERE res-line.active-flag = 1 AND res-line.resstatus = 6
        AND res-line.l-zuordnung[3] = 0 NO-LOCK:

        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
            AND reslin-queasy.resnr = res-line.resnr 
            AND reslin-queasy.reslinnr = res-line.reslinnr 
            AND cdate GE reslin-queasy.date1 
            AND cdate LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy AND res-line.zipreis NE reslin-queasy.deci1 THEN DO:
            msg-str = msg-str + CHR(2)
                    + translateExtended ("Different Rate found! Night Audit process not possible.",lvCAREA,"").
            stop-it = YES.
            RETURN.
        END.
    END.
END.



/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */

PROCEDURE midnite-prog:

  RUN reorg-prog.
  RUN check-cancelled-res-line.
  RUN check-delete-res-line.
  RUN check-cekout-res-line.

  
  DO TRANSACTION: 

    FIND FIRST htparam WHERE paramnr = 105 EXCLUSIVE-LOCK. /* LAST midnight */ 
    IF htparam.fdate LT TODAY THEN htparam.fdate = htparam.fdate + 1. 
/*  ELSE htparam.fdate = htparam.fdate + 1.  */ 
    ci-date = htparam.fdate. 
    FIND CURRENT htparam NO-LOCK. 
 
    FIND FIRST htparam WHERE paramnr = 87 EXCLUSIVE-LOCK.   /* ci-date */ 
    htparam.fdate = ci-date. 
    FIND CURRENT htparam NO-LOCK. 
  END. 
 
  /*MT
  FOR EACH na-list: 
    DELETE na-list. 
  END.
  
/* no-show list   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 1. 
  na-list.bezeich = translateExtended ("Process Noshow List",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN noshow. 
 
/* Extend Departure DATE   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 2. 
  na-list.bezeich = translateExtended ("Extending Departure Date",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN extend-departure. 
 
/* CRM online questionnair   ********/ 
  FIND FIRST htparam WHERE htparam.paramnr = 1459 NO-LOCK. /* CRM license */
  IF htparam.paramgr = 99 AND htparam.flogical THEN
  DO:
    CREATE na-list. 
    na-list.reihenfolge = 2. 
    na-list.bezeich = translateExtended ("CRM questionnair - C/O Guests",lvCAREA,""). 
    na-list.flag = 2. 
    OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
    RUN CRM-checkout. 
  END.

/* Early Checkout   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 2. 
  na-list.bezeich = translateExtended ("Early Checkout",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN early-checkout. 


  /* UPDATE HouseKeeping Status   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 3. 
  na-list.bezeich = translateExtended ("Updating Room Status",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN update-zistatus. 
 

  /* Correct bill.datum   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 4. 
  na-list.bezeich = translateExtended ("Correcting bill date",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN fix-bill-datum. 
  
/* Delete old bills   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 4. 
  na-list.bezeich = translateExtended ("Deleting old bills",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-bills. 
 
/* Delete old billjournals   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 5. 
  na-list.bezeich = "Deleting old bill journals". 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-billjournal. 
 
/* Delete old Reservation   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 6. 
  na-list.bezeich = translateExtended ("Deleting old reservations",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-res. 
 
/* Delete old Resplan AND zimplan   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 7. 
  na-list.bezeich = translateExtended ("Deleting old roomplans",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-roomplan. 
 
/* Delete old paid debts   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 8. 
  na-list.bezeich = translateExtended ("Deleting old paid debts",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-debt. 
 
/* Delete old paid A/P ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 8. 
  na-list.bezeich = translateExtended ("Deleting old paid A/P",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-ap. 
 
/* Delete old Rest Bills   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 9. 
  na-list.bezeich = translateExtended ("Deleting old restaurant bills",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-rbill. 
 
/* Delete old rest bill journals   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 10. 
  na-list.bezeich = translateExtended ("Deleting old rest.journals",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-rjournal. 
 
/* Delete old kitchen bon records  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 11. 
  na-list.bezeich = translateExtended ("Deleting old rest.journals",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-bons. 
 
/* Delete old kitchen bon records  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 11. 
  na-list.bezeich = translateExtended ("Deleting old outlet turnovers",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-outlet-umsatz. 
 
/* Delete old calls   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 12. 
  na-list.bezeich = translateExtended ("Deleting old calls",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-calls. 
 
/* Delete old l-order & l-orderhdr   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 13. 
  na-list.bezeich = translateExtended ("Deleting old purchase orders",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-po. 
 
/* Delete old stock movings  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 14. 
  na-list.bezeich = translateExtended ("Close direct purchase records",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-l-op. 
 
/* Delete old zinrstat  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 15. 
  na-list.bezeich = translateExtended ("Deleting old room number statistics",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat1. 
 
/* Delete old zkstat  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 16. 
  na-list.bezeich = translateExtended ("Deleting old room catagory statistics",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat2. 
 
/* Delete old sources  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 17. 
  na-list.bezeich = translateExtended ("Deleting old source statistics",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat3. 
 
/* Delete old segmentstat  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 18. 
  na-list.bezeich = translateExtended ("Deleting old segment statistics",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat4. 
 
/* Delete old market segment statistic  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 18. 
  na-list.bezeich = translateExtended ("Deleting old market segment statistics",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat41. 
 
/* Delete old nationstat  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 19. 
  na-list.bezeich = translateExtended ("Deleting old nation statistics",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat5. 
 
/* Delete old umsatz  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 20. 
  na-list.bezeich = translateExtended ("Deleting old turnover statistics",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat6. 
 
/* Delete old h-umsatz ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 21. 
  na-list.bezeich = translateExtended ("Deleting old restaurant turnover statistics",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat7. 
 
/* Delete old h-cost ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 22. 
  na-list.bezeich = translateExtended ("Deleting old F&B Costs",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat8. 
 
/* Delete old exchange rates ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 23. 
  na-list.bezeich = translateExtended ("Deleting old Exchange Rates",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-stat9. 
 
/* Delete NOT used allotments ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 24. 
  na-list.bezeich = translateExtended ("Deleting expired allotments",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-allotment. 
 
/* Delete old DML-list ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 25. 
  na-list.bezeich = translateExtended ("Deleting old DML-Articles",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-dml. 
 
/* Delete old OLD Interface Records ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 26. 
  na-list.bezeich = translateExtended ("Deleting old Interface Records",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-interface. 
 
/* Delete old OLD nitehist records ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 27. 
  na-list.bezeich = translateExtended ("Deleting old nithist Records",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-nitehist. 
 
/* CREATE Banquet history, AND delete old Banquet Reservation   ********/ 
  FIND FIRST htparam WHERE paramnr = 985 no-lock.  /* License Banquet */ 
  IF htparam.flogical THEN 
  DO: 
    CREATE na-list. 
    na-list.reihenfolge = 28. 
    na-list.bezeich = translateExtended ("Banquet Reservations",lvCAREA,""). 
    na-list.flag = 2. 
    OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
    RUN nt-bahistory.p. 
    RUN del-old-bares. 
  END. 
 
/* Move reslin-queasy.char1 OF Reservation Changes TO char3 ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 29. 
  na-list.bezeich = translateExtended ("Updating logfile records",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN update-logfile-records. 
 
/* Delete old h-compliment ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 30. 
  na-list.bezeich = translateExtended ("Deleting old F&B Compliments",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-hcompli. 
 
/* Delete old work order ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 31. 
  na-list.bezeich = translateExtended ("Deleting old Work Order Records",lvCAREA,""). 
  na-list.flag = 2. 
  OPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge descending. 
  RUN del-old-workorder. 

  /* Club Software */ 
  FIND FIRST htparam WHERE htparam.paramnr = 1114 NO-LOCK. 
  IF htparam.flogical THEN RUN clclosing.p. 
 
  FIND FIRST htparam WHERE paramnr = 592 NO-LOCK. 
  IF htparam.flogical THEN RETURN. 
  DO TRANSACTION: 
    FIND CURRENT htparam EXCLUSIVE-LOCK. 
    htparam.flogical = YES. 
    FIND CURRENT htparam NO-LOCK. 
    FIND FIRST htparam WHERE paramnr = 592 EXCLUSIVE-LOCK. 
    htparam.fchar = "Midnight Program". 
    htparam.fdate = today. 
    htparam.finteger = time. 
    htparam.flogical = NO. 
    FIND CURRENT htparam NO-LOCK. 
  END. 
  */
END. 

PROCEDURE check-cancelled-res-line:
DEF BUFFER rbuff FOR res-line.
  FIND FIRST res-line WHERE res-line.resstatus = 9
      AND res-line.active-flag = 0 NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE res-line:
      DO TRANSACTION:
          FIND FIRST rbuff WHERE RECID(rbuff) = RECID(res-line).
          ASSIGN rbuff.active-flag = 2.
          FIND CURRENT rbuff NO-LOCK.
          RELEASE rbuff.
      END.
    FIND NEXT res-line WHERE res-line.resstatus = 9
        AND res-line.active-flag = 0 NO-ERROR.
  END.
END.

/*ITA 120816 check delete resline*/
PROCEDURE check-delete-res-line:
  DEF BUFFER rbuff FOR res-line.
  
  FIND FIRST res-line WHERE res-line.resstatus = 99
      AND res-line.active-flag LT 2 NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE res-line:
      DO TRANSACTION:
          FIND FIRST rbuff WHERE RECID(rbuff) = RECID(res-line).
          ASSIGN rbuff.active-flag = 2.
          FIND CURRENT rbuff NO-LOCK.
          RELEASE rbuff.

          CREATE res-history.
          ASSIGN
              res-history.datum = TODAY
              res-history.zeit  = TIME
              res-history.aenderung = "Delete ResLine: ResNo " + STRING(res-line.resnr) + " No " 
                                      + STRING(res-line.reslinnr) + " - Change ActiveFlag was " 
                                      + STRING(res-line.active-flag) + "To 2" 
              res-history.action = "Reservation".

          FIND CURRENT res-history NO-LOCK. 
          RELEASE res-history. 
      END.
      
      FIND NEXT res-line WHERE res-line.resstatus = 99
          AND res-line.active-flag LT 2 NO-LOCK NO-ERROR.
  END.
END.

PROCEDURE check-cekout-res-line:
  DEF BUFFER rbuff FOR res-line.
  FIND FIRST res-line WHERE res-line.resstatus = 8
      AND res-line.active-flag LT 2 NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE res-line:
      DO TRANSACTION:
          FIND FIRST rbuff WHERE RECID(rbuff) = RECID(res-line).
          ASSIGN rbuff.active-flag = 2.
          FIND CURRENT rbuff NO-LOCK.
          RELEASE rbuff.
      END.
    FIND NEXT res-line WHERE res-line.resstatus = 8
      AND res-line.active-flag LT 2 NO-ERROR.
  END.
END.

PROCEDURE reorg-prog: 
  FIND FIRST htparam WHERE paramnr = 87 no-lock.   /* ci-date */ 
  ci-date = htparam.fdate. 
 
  FOR EACH na-list:
      DELETE na-list.
  END.
 
/* Delete resplan AND roomplan  ********/ 
  CREATE na-list.
  na-list.reihenfolge = 1.
  na-list.bezeich = "Deleting Roomplan Records".
  na-list.flag = 3.
  /*MTOPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge.*/
  RUN del-roomplan.
 
/* CREATE resplan AND roomplan   ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 2. 
  na-list.bezeich = "Creating Roomplan records". 
  na-list.flag = 3. 
  /*MTOPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge. */
  RUN create-roomplan. 
 
/* UPDATE room status  ********/ 
  CREATE na-list. 
  na-list.reihenfolge = 3. 
  na-list.bezeich = "Updating Room Status". 
  na-list.flag = 3. 
  /*MTOPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge. */
  RUN update-rmstatus. 
  /*MTOPEN QUERY q1 FOR EACH na-list NO-LOCK BY na-list.reihenfolge. */

  /*update roomrate
  RUN rm-charge.*/
END. 


PROCEDURE rm-charge: 

DEFINE VARIABLE double-currency     AS LOGICAL INITIAL NO. 
DEFINE VARIABLE master-exist        AS LOGICAL. 
DEFINE VARIABLE exchg-rate          AS DECIMAL INITIAL 1. 

DEFINE VARIABLE price-decimal       AS INTEGER. 
DEFINE VARIABLE user-init           AS CHAR FORMAT "x(2)". 
DEFINE VARIABLE ct                  AS CHAR         NO-UNDO.
DEFINE VARIABLE st1                 AS CHAR         NO-UNDO.
DEFINE VARIABLE st2                 AS CHAR         NO-UNDO.
DEFINE VARIABLE segment-flag        AS LOGICAL      NO-UNDO.
DEFINE VARIABLE bonus           AS LOGICAL. 
DEFINE VARIABLE roomrate        AS DECIMAL. 
DEFINE VARIABLE cid             AS CHAR FORMAT "x(2)" INITIAL "  ". 
DEFINE VARIABLE cdate           AS CHAR FORMAT "x(8)" INITIAL "        ". 
DEFINE VARIABLE argt            AS CHAR. 
DEFINE VARIABLE c               AS CHAR. 

DEFINE VARIABLE pax             AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE n               AS INTEGER              NO-UNDO. 

DEFINE BUFFER rbuff             FOR res-line.
DEFINE BUFFER rline FOR res-line.




FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 104 NO-LOCK. 
user-init = htparam.fchar. 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
IF htparam.flogical OR DOUBLE-CURRENCY THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
END. 
 



  FIND FIRST res-line WHERE res-line.active-flag = 1 
    AND res-line.resstatus NE 12 
    AND (res-line.erwachs NE 0 OR res-line.kind1 NE 0 OR res-line.kind2 NE 0)
    AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 

  DO WHILE AVAILABLE res-line: 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK. 
    FIND FIRST arrangement WHERE arrangement.arrangement 
      = res-line.arrangement NO-LOCK. 
    FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr 
      AND artikel.departement = 0 NO-LOCK. 

    n = 0.
    IF res-line.zimmer-wunsch MATCHES ("*DATE,*") THEN
    n = INDEX(res-line.zimmer-wunsch,"Date,").
    IF n > 0 THEN
    DO:
      c = SUBSTR(res-line.zimmer-wunsch, n + 5, 8).
      created-date = DATE(INTEGER(SUBSTR(c,5,2)), INTEGER(SUBSTR(c,7,2)),
        INTEGER(SUBSTR(c,1,4))).
    END.
    ELSE created-date = reservation.resdat.

/* SY 24/02/2014 */   
    ASSIGN 
        contcode     = ""
        segment-flag = NO
    .
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
      AND reslin-queasy.resnr = res-line.resnr 
      AND reslin-queasy.reslinnr = res-line.reslinnr 
      AND reslin-queasy.date1 GE ci-date 
      AND reslin-queasy.date1 LE ci-date NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy AND reslin-queasy.char2 NE "" THEN
    DO TRANSACTION:
      ASSIGN 
          segment-flag = YES
          contcode     = reslin-queasy.char2
          ct           = res-line.zimmer-wunsch
      .
      FIND FIRST rline WHERE RECID(rline) = RECID(res-line).
      IF NOT ct MATCHES ("*$CODE$*") THEN
        rline.zimmer-wunsch = ct + "$CODE$" + contcode + ";".
      ELSE
      ASSIGN
        st1                 = SUBSTR(ct,1, INDEX(ct,"$CODE$") - 1)
        st2                 = SUBSTR(ct, LENGTH(st1) + 1)
        st2                 = SUBSTR(st2,INDEX(st2,";") + 1)
        ct                  = st1 + "$CODE$" + contcode + ";" + st2
        rline.zimmer-wunsch = TRIM(ct)
      .
      FIND CURRENT rline NO-LOCK.
    END.
    ELSE
    DO:
      FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE guest-pr THEN contcode = guest-pr.CODE.
      ct = res-line.zimmer-wunsch.
      IF ct MATCHES("*$CODE$*") THEN
      DO:
        ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
        contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
      END.
    END.
    
    IF segment-flag = YES AND (contcode NE "") THEN
    DO:
      FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = contcode 
        NO-LOCK NO-ERROR.
      IF AVAILABLE queasy AND ENTRY(1, queasy.char3, ";") NE "" THEN
      DO:
        FIND FIRST segment WHERE segment.bezeich = ENTRY(1, queasy.char3, ";")
          NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN
        DO TRANSACTION:
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr.
          reservation.segmentcode = segment.segmentcode.
          FIND CURRENT reservation NO-LOCK.
        END.
      END.
    END.

    RUN check-bonus(OUTPUT bonus). 

    DO: 
      roomrate = res-line.zipreis. 
      argt = res-line.arrangement. 
      pax = res-line.erwachs. 
      IF bonus THEN roomrate = 0. 
      ELSE 
      DO:
        IF new-contrate THEN RUN new-update-zipreis (INPUT-OUTPUT roomrate, 
          INPUT-OUTPUT argt, INPUT-OUTPUT pax). 
        ELSE RUN update-zipreis (INPUT-OUTPUT roomrate, INPUT-OUTPUT argt, 
          INPUT-OUTPUT pax). 
      END.
      
      /*MESSAGE res-line.resnr res-line.reslinnr res-line.zipreis roomrate
          reslin-queasy.date1 bill-date VIEW-AS ALERT-BOX INFO.*/

      IF (res-line.zipreis NE roomrate) OR (res-line.arrangement NE argt) 
        OR (res-line.erwachs NE pax) THEN 
      DO TRANSACTION: 
        cid = "  ". 
        cdate = "        ". 
        IF TRIM(res-line.changed-id) NE "" THEN 
        DO: 
          cid = res-line.changed-id. 
          cdate = STRING(res-line.changed). 
        END. 
        CREATE reslin-queasy. 
        ASSIGN
          reslin-queasy.key = "ResChanges"
          reslin-queasy.resnr = res-line.resnr 
          reslin-queasy.reslinnr = res-line.reslinnr
          reslin-queasy.date2 = TODAY
          reslin-queasy.number2 = TIME 
        . 
        reslin-queasy.char3 = STRING(res-line.ankunft) + ";" 
                        + STRING(res-line.ankunft) + ";" 
                        + STRING(res-line.abreise) + ";" 
                        + STRING(res-line.abreise) + ";" 
                        + STRING(res-line.zimmeranz) + ";" 
                        + STRING(res-line.zimmeranz) + ";" 
                        + STRING(res-line.erwachs) + ";" 
                        + STRING(pax) + ";" 
                        + STRING(res-line.kind1) + ";" 
                        + STRING(res-line.kind1) + ";" 
                        + STRING(res-line.gratis) + ";" 
                        + STRING(res-line.gratis) + ";" 
                        + STRING(res-line.zikatnr) + ";" 
                        + STRING(res-line.zikatnr) + ";" 
                        + STRING(res-line.zinr) + ";" 
                        + STRING(res-line.zinr) + ";" 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(argt) + ";" 
                        + STRING(res-line.zipreis) + ";" 
                        + STRING(roomrate) + ";" 
                        + STRING(cid) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(cdate) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(res-line.NAME) + ";" 
                        + STRING(res-line.NAME) + ";". 
        IF res-line.was-status = 0 THEN 
          reslin-queasy.char3 = reslin-queasy.char3 + STRING(" NO") + ";"
                        + STRING("YES") + ";". 
        ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";" 
                        + STRING("YES") + ";". 
        FIND CURRENT reslin-queasy NO-LOCK.
        RELEASE reslin-queasy. 
 
        FIND FIRST rbuff WHERE RECID(rbuff) = RECID(res-line) EXCLUSIVE-LOCK.
        rbuff.zipreis = roomrate. 
        IF argt NE rbuff.arrangement THEN rbuff.arrangement = argt. 
        IF pax NE rbuff.erwachs THEN rbuff.erwachs = pax. 
        FIND CURRENT rbuff NO-LOCK. 
      END. 
    END. 
      
    FIND NEXT res-line WHERE res-line.active-flag = 1 
      AND res-line.resstatus NE 12 
      AND (res-line.erwachs NE 0 OR res-line.kind1 NE 0 OR res-line.kind2 NE 0)
      AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
  END. 
END. 
 
PROCEDURE check-bonus: 
DEFINE OUTPUT PARAMETER bonus AS LOGICAL INITIAL NO. 
DEFINE VARIABLE bonus-array AS LOGICAL EXTENT 999 INITIAL NO. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE stay AS INTEGER. 
DEFINE VARIABLE pay AS INTEGER. 
DEFINE VARIABLE num-bonus AS INTEGER INITIAL 0. 
DEF VAR curr-zikatnr AS INTEGER. 
DEF BUFFER rmcat FOR zimkateg. 
 
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
    AND reslin-queasy.resnr = res-line.resnr 
    AND reslin-queasy.reslinnr = res-line.reslinnr 
    AND ci-date GE reslin-queasy.date1 
    AND ci-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
  IF AVAILABLE reslin-queasy THEN RETURN. 
 
  IF NOT AVAILABLE guest-pr THEN RETURN. 
  
  IF res-line.l-zuordnung[1] NE 0 THEN 
  DO: 
    FIND FIRST rmcat WHERE rmcat.zikatnr = res-line.l-zuordnung[1] 
      NO-LOCK. 
    curr-zikatnr = rmcat.zikatnr. 
  END. 
  ELSE curr-zikatnr = res-line.zikatnr. 
 
  IF new-contrate THEN
  DO:
    /*MMESSAGE "minus program ratecode-compli.p" VIEW-AS ALERT-BOX INFO.
    TRUN ratecode-compli.p(res-line.resnr, res-line.reslinnr, contcode, 
      curr-zikatnr, bill-date, OUTPUT bonus).*/
    RETURN.
  END.

  FIND FIRST arrangement WHERE arrangement.arrangement 
    = res-line.arrangement NO-LOCK. 
  
/*
  FIND FIRST pricecod WHERE pricecod.code = contcode 
    AND pricecod.marknr = res-line.reserve-int 
    AND pricecod.argtnr = arrangement.argtnr 
    AND pricecod.zikatnr = curr-zikatnr 
    AND bill-date GE pricecod.startperiode 
    AND bill-date LE pricecod.endperiode NO-LOCK NO-ERROR. 
 
  IF NOT AVAILABLE pricecod THEN RETURN. 
*/

  j = 1. 
  DO i = 1 TO 4: 
    stay = INTEGER(SUBSTR(options, j, 2)). 
    pay  = INTEGER(SUBSTR(options, j + 2, 2)). 
    IF (stay - pay) GT 0 THEN 
    DO: 
      n = num-bonus + pay  + 1. 
      DO k = n TO stay: 
        bonus-array[k] = YES. 
      END. 
      num-bonus = stay - pay. 
    END. 
     j = j + 4. 
  END. 
  n = ci-date - res-line.ankunft + 1. 
  IF n GE 1 THEN bonus = bonus-array[n]. 
END. 
 
PROCEDURE new-update-zipreis: 
DEFINE INPUT-OUTPUT PARAMETER roomrate  AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER argt      AS CHAR. 
DEFINE INPUT-OUTPUT PARAMETER pax       AS INTEGER. 
DEFINE VARIABLE rm-rate         AS DECIMAL. 
DEFINE VARIABLE add-it          AS LOGICAL INITIAL NO. 
DEFINE VARIABLE qty             AS INTEGER. 
DEFINE VARIABLE it-exist        AS LOGICAL INITIAL NO. /* YES->usr prog exists */ 
DEFINE VARIABLE argt-defined    AS LOGICAL. 
DEFINE VARIABLE exrate1         AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL INITIAL 1. 
DEFINE VARIABLE child1          AS INTEGER              NO-UNDO. 
DEFINE VARIABLE fix-rate        AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE post-date       AS DATE                 NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER              NO-UNDO. 
DEFINE VARIABLE w-day           AS INTEGER              NO-UNDO. 
DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
DEFINE BUFFER w1                FOR waehrung. 
 
  rm-rate = roomrate. 
 
  ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*").
  kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").
  IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
  ELSE curr-zikatnr = res-line.zikatnr. 
  
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
    AND reslin-queasy.resnr = res-line.resnr 
    AND reslin-queasy.reslinnr = res-line.reslinnr 
    AND ci-date GE reslin-queasy.date1 
    AND ci-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE reslin-queasy AND res-line.abreise LE ci-date THEN
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
    AND reslin-queasy.resnr = res-line.resnr 
    AND reslin-queasy.reslinnr = res-line.reslinnr 
    AND (res-line.abreise - 1) GE reslin-queasy.date1 
    AND (res-line.abreise - 1) LE reslin-queasy.date2 NO-LOCK NO-ERROR. 

  IF AVAILABLE reslin-queasy THEN /* fixed rate */
  DO: 
    roomrate = reslin-queasy.deci1. 
    IF reslin-queasy.char1 NE "" AND reslin-queasy.char1 NE argt THEN 
      argt = reslin-queasy.char1. 
 
    IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
    /*MTRUN usr-prog1(INPUT-OUTPUT roomrate, OUTPUT it-exist). */

    RETURN. 
  END. 
  ELSE 
  DO: 
    /*MTRUN usr-prog1(INPUT-OUTPUT roomrate, OUTPUT it-exist). */
    IF it-exist THEN RETURN. 
  END. 
 
  FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
  FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR. 
  IF AVAILABLE guest-pr THEN 
  DO: 
    post-date = ci-date. 
    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = 
      res-line.reserve-int NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.logi3 THEN post-date = res-line.ankunft. 

    RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
      res-line.reslinnr, contcode, created-date, post-date, res-line.ankunft,
      res-line.abreise, res-line.reserve-int, arrangement.argtnr,
      curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
      res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
      OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).

/* SY 05 AUG 2015 */
    IF rm-rate LE 0.01 THEN rm-rate = 0.

/** additional fix cost e.g. extra beds **/ 
    FIND FIRST fixleist WHERE fixleist.resnr = res-line.resnr 
      AND fixleist.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE fixleist: 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
        AND reslin-queasy.char1 = contcode 
        AND reslin-queasy.number1 = res-line.reserve-int 
        AND reslin-queasy.number2 = arrangement.argtnr 
        AND reslin-queasy.reslinnr = res-line.zikatnr 
        AND reslin-queasy.number3 = fixleist.artnr 
        AND reslin-queasy.resnr = fixleist.departement 
        AND post-date GE reslin-queasy.date1 
        AND post-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        FIND CURRENT fixleist EXCLUSIVE-LOCK. 
        fixleist.betrag = reslin-queasy.deci1. 
        FIND CURRENT fixleist NO-LOCK. 
      END. 
      FIND NEXT fixleist WHERE fixleist.resnr = res-line.resnr 
        AND fixleist.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
    END. 
    roomrate = rm-rate. 
    /*MTRUN usr-prog2(INPUT-OUTPUT roomrate). */
    RETURN. 
  END. /* IF AVAILABLE guest-pr */ 
  ELSE /* publish rate */ 
  DO: 
  DEF VAR publish-rate AS DECIMAL INITIAL 0 NO-UNDO. 
    w-day = wd-array[WEEKDAY(ci-date - 1)]. 
    FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE (ci-date - 1) 
      AND katpreis.endperiode GE (ci-date - 1) 
      AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE katpreis THEN 
    FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE (ci-date - 1) 
      AND katpreis.endperiode GE (ci-date - 1) 
      AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE katpreis THEN RETURN. 
    IF res-line.zipreis NE get-rackrate(res-line.erwachs, 
       res-line.kind1, res-line.kind2) THEN RETURN. 

    w-day = wd-array[WEEKDAY(ci-date)]. 
    FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE ci-date 
      AND katpreis.endperiode GE ci-date 
      AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE katpreis THEN 
    FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE ci-date 
      AND katpreis.endperiode GE ci-date 
      AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE katpreis THEN 
    DO: 
      publish-rate = get-rackrate(res-line.erwachs, res-line.kind1, 
        res-line.kind2). 
      IF publish-rate = 0 THEN RETURN. 
/*
      CREATE reslin-queasy. 
      ASSIGN 
        reslin-queasy.key = "arrangement" 
        reslin-queasy.resnr = res-line.resnr 
        reslin-queasy.reslinnr = res-line.reslinnr 
        reslin-queasy.date1 = bill-date - 1 
        reslin-queasy.date2 = bill-date - 1 
        reslin-queasy.deci1 = roomrate 
        reslin-queasy.char1 = res-line.arrangement 
        reslin-queasy.number3 = res-line.erwachs 
      . 
      FIND CURRENT reslin-queasy NO-LOCK. 
*/
      roomrate = publish-rate. 
    END. 
  END. 
END.  

PROCEDURE update-zipreis: 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER argt AS CHAR. 
DEFINE INPUT-OUTPUT PARAMETER pax AS INTEGER. 
DEFINE VARIABLE rm-rate AS DECIMAL. 
DEFINE buffer resline FOR res-line. 
DEFINE VARIABLE add-it AS LOGICAL INITIAL NO. 
DEFINE VARIABLE qty AS INTEGER. 
DEFINE VARIABLE it-exist AS LOGICAL INITIAL NO. /* YES IF user program exists */ 
DEFINE VARIABLE argt-defined AS LOGICAL. 
DEFINE VARIABLE exrate1 AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2 AS DECIMAL INITIAL 1. 
DEFINE VARIABLE child1 AS INTEGER NO-UNDO. 
DEFINE VARIABLE fix-rate AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE post-date AS DATE NO-UNDO. 
DEFINE VARIABLE curr-zikatnr AS INTEGER NO-UNDO. 
DEFINE VARIABLE w-day AS INTEGER NO-UNDO. 
DEFINE buffer w1 FOR waehrung. 

rm-rate = roomrate. 

IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
ELSE curr-zikatnr = res-line.zikatnr. 

/*  DO NOT USE !!! 
FIND FIRST htparam WHERE paramnr = 264 NO-LOCK. 
IF htparam.flogical THEN return. /* NO change, roomrate fixed FOR whole stay */ 
ELSE 
*/ 
DO: 
FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
  AND reslin-queasy.resnr = res-line.resnr 
  AND reslin-queasy.reslinnr = res-line.reslinnr 
  AND ci-date GE reslin-queasy.date1 
  AND ci-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
IF AVAILABLE reslin-queasy THEN 
DO: 
  roomrate = reslin-queasy.deci1. 
  IF reslin-queasy.char1 NE "" AND reslin-queasy.char1 NE argt THEN 
    argt = reslin-queasy.char1. 

  IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
  /*MTRUN usr-prog1(INPUT-OUTPUT roomrate, OUTPUT it-exist). */

  RETURN. 
END. 
ELSE 
    DO: 
      /*MTRUN usr-prog1(INPUT-OUTPUT roomrate, OUTPUT it-exist). */
      IF it-exist THEN RETURN. 
    END. 
 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK. 
    FIND FIRST arrangement WHERE arrangement.arrangement 
      = res-line.arrangement NO-LOCK. 
    IF AVAILABLE guest-pr THEN 
    DO: 
      post-date = ci-date. 
      FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = 
        res-line.reserve-int NO-LOCK NO-ERROR. 
      IF AVAILABLE queasy AND queasy.logi3 THEN post-date = res-line.ankunft. 
      FIND FIRST pricecod WHERE pricecod.code = contcode 
        AND pricecod.marknr = res-line.reserve-int 
        AND pricecod.argtnr = arrangement.argtnr 
        AND pricecod.zikatnr = curr-zikatnr 
        AND post-date GE pricecod.startperiode 
        AND post-date LE pricecod.endperiode NO-LOCK NO-ERROR. 
      IF AVAILABLE pricecod THEN 
      DO: 
        IF res-line.kind1 LE pricecod.betriebsnr THEN child1 = 0. 
        ELSE child1 = res-line.kind1 - pricecod.betriebsnr. 
        rm-rate = pricecod.perspreis[res-line.erwachs] 
          + pricecod.kindpreis[1] * child1 
          + pricecod.kindpreis[2] * res-line.kind2. 
 
/** additional charges IF argt-line price NOT included IN basic room rate **/ 
        FIND FIRST w1 WHERE w1.waehrungsnr = arrangement.betriebsnr NO-LOCK 
          NO-ERROR. 
        IF AVAILABLE w1 THEN exrate1 = w1.ankauf / w1.einheit. 
        IF res-line.reserve-dec NE 0 THEN 
          ex2 = ex2 / res-line.reserve-dec. 
        ELSE 
        DO: 
          FIND FIRST w1 WHERE w1.waehrungsnr = res-line.betriebsnr NO-LOCK 
            NO-ERROR. 
          IF AVAILABLE w1 THEN ex2 = (w1.ankauf / w1.einheit). 
        END. 
        FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
          AND NOT argt-line.kind1 AND NOT argt-line.kind2: 
          add-it = NO. 
          IF argt-line.vt-percnt = 0 THEN 
          DO: 
            IF argt-line.betriebsnr = 0 THEN qty = res-line.erwachs. 
            ELSE qty = argt-line.betriebsnr. 
          END. 
          ELSE IF argt-line.vt-percnt = 1 THEN qty = child1. 
          ELSE IF argt-line.vt-percnt = 2 THEN qty = res-line.kind2. 
 
          IF qty GT 0 THEN 
          DO: 
            IF argt-line.fakt-modus = 1 THEN add-it = YES. 
            ELSE IF argt-line.fakt-modus = 2 THEN 
            DO: 
              IF res-line.ankunft EQ post-date THEN add-it = YES. 
            END. 
            ELSE IF argt-line.fakt-modus = 3 THEN 
            DO: 
              IF (res-line.ankunft + 1) EQ post-date THEN add-it = YES. 
            END. 
            ELSE IF argt-line.fakt-modus = 4 
              AND day(post-date) = 1 THEN add-it = YES. 
            ELSE IF argt-line.fakt-modus = 5 
              AND day(post-date + 1) = 1 THEN add-it = YES. 
            ELSE IF argt-line.fakt-modus = 6 THEN 
              IF (res-line.ankunft + (argt-line.intervall - 1)) GE post-date 
              THEN add-it = YES. 
          END. 
          IF add-it THEN 
          DO: 
            argt-defined = NO. 
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
              AND reslin-queasy.char1 = "" 
              AND reslin-queasy.number1 = argt-line.departement 
              AND reslin-queasy.number2 = argt-line.argtnr 
              AND reslin-queasy.resnr = res-line.resnr 
              AND reslin-queasy.reslinnr = res-line.reslinnr 
              AND reslin-queasy.number3 = argt-line.argt-artnr 
              AND post-date GE reslin-queasy.date1 
              AND post-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
            IF AVAILABLE reslin-queasy THEN 
            DO: 
              argt-defined = YES. 
              IF argt-line.vt-percnt = 0 THEN 
                rm-rate = rm-rate + reslin-queasy.deci1 * qty. 
              ELSE IF argt-line.vt-percnt = 1 THEN 
                rm-rate = rm-rate + reslin-queasy.deci2 * qty. 
              ELSE IF argt-line.vt-percnt = 2 THEN 
                rm-rate = rm-rate + reslin-queasy.deci3 * qty. 
            END. 
            IF NOT argt-defined THEN 
            DO: 
              FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
                AND reslin-queasy.char1 = pricecod.code 
                AND reslin-queasy.number1 = pricecod.marknr 
                AND reslin-queasy.number2 = pricecod.argtnr 
                AND reslin-queasy.reslinnr = pricecod.zikatnr 
                AND reslin-queasy.number3 = argt-line.argt-artnr 
                AND reslin-queasy.resnr = argt-line.departement 
                AND post-date GE reslin-queasy.date1 
                AND post-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
              IF AVAILABLE reslin-queasy THEN 
              DO: 
                IF argt-line.vt-percnt = 0 THEN 
                  rm-rate = rm-rate + reslin-queasy.deci1 * qty. 
                ELSE IF argt-line.vt-percnt = 1 THEN 
                  rm-rate = rm-rate + reslin-queasy.deci2 * qty. 
                ELSE IF argt-line.vt-percnt = 2 THEN 
                  rm-rate = rm-rate + reslin-queasy.deci3 * qty. 
              END. 
              ELSE rm-rate = rm-rate + argt-line.betrag * qty * exrate1 / ex2. 
            END. 
          END. 
        END. 
/** additional fix cost e.g. extra beds **/ 
        FIND FIRST fixleist WHERE fixleist.resnr = res-line.resnr 
          AND fixleist.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
        DO WHILE AVAILABLE fixleist: 
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
            AND reslin-queasy.char1 = pricecod.code 
            AND reslin-queasy.number1 = pricecod.marknr 
            AND reslin-queasy.number2 = pricecod.argtnr 
            AND reslin-queasy.reslinnr = pricecod.zikatnr 
            AND reslin-queasy.number3 = fixleist.artnr 
            AND reslin-queasy.resnr = fixleist.departement 
            AND post-date GE reslin-queasy.date1 
            AND post-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy THEN 
          DO: 
            FIND CURRENT fixleist EXCLUSIVE-LOCK. 
            fixleist.betrag = reslin-queasy.deci1. 
            FIND CURRENT fixleist NO-LOCK. 
          END. 
          FIND NEXT fixleist WHERE fixleist.resnr = res-line.resnr 
            AND fixleist.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
        END. 
      END. 
      ELSE 
      DO: 
        FIND FIRST pricegrp WHERE pricegrp.code = contcode 
          AND pricegrp.argtnr = arrangement.argtnr 
          AND ci-date GE pricegrp.startperiode 
          AND ci-date LE pricegrp.endperiode NO-LOCK NO-ERROR. 
        IF AVAILABLE pricegrp THEN 
          rm-rate = pricegrp.perspreis[res-line.erwachs]. 
        IF res-line.kind1 EQ 1 OR res-line.kind1 = 2 THEN 
          rm-rate = rm-rate + pricecod.kindpreis[res-line.kind1]. 
      END. 
      roomrate = rm-rate. 
      /*MTRUN usr-prog2(INPUT-OUTPUT roomrate). */
      RETURN. 
    END. /* IF AVAILABLE guest-pr */ 
    ELSE /* publish rate */ 
    DO: 
    DEF VAR publish-rate AS DECIMAL INITIAL 0 NO-UNDO. 
      w-day = wd-array[WEEKDAY(ci-date - 1)]. 
      FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
        AND katpreis.argtnr = arrangement.argtnr 
        AND katpreis.startperiode LE (ci-date - 1) 
        AND katpreis.endperiode GE (ci-date - 1) 
        AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE katpreis THEN 
      FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
        AND katpreis.argtnr = arrangement.argtnr 
        AND katpreis.startperiode LE (ci-date - 1) 
        AND katpreis.endperiode GE (ci-date - 1) 
        AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE katpreis THEN RETURN. 
      IF res-line.zipreis NE get-rackrate(res-line.erwachs, 
         res-line.kind1, res-line.kind2) THEN RETURN. 
 
      w-day = wd-array[WEEKDAY(ci-date)]. 
      FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
        AND katpreis.argtnr = arrangement.argtnr 
        AND katpreis.startperiode LE ci-date 
        AND katpreis.endperiode GE ci-date 
        AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE katpreis THEN 
      FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
        AND katpreis.argtnr = arrangement.argtnr 
        AND katpreis.startperiode LE ci-date 
        AND katpreis.endperiode GE ci-date 
        AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE katpreis THEN 
      DO: 
        publish-rate = get-rackrate(res-line.erwachs, res-line.kind1, res-line.kind2). 
        IF publish-rate = 0 THEN RETURN. 
        roomrate = publish-rate. 
      END. 
    END. 
  END. 
END. 


PROCEDURE del-roomplan: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
  /*MTmess-str = translateExtended ("Deleted records",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST resplan WHERE resplan.datum GE ci-date NO-LOCK NO-ERROR. 
  FIND FIRST na-list WHERE na-list.reihenfolge = 1. 
  DO WHILE AVAILABLE resplan: 
    DO TRANSACTION: 
      i = i + 1. 
      na-list.anz = na-list.anz + 1. 
      /*MTmess-str = translateExtended ("Deleted records",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
      FIND CURRENT resplan EXCLUSIVE-LOCK. 
      delete resplan. 
      RELEASE resplan.
    END. 
    FIND NEXT resplan WHERE resplan.datum GE ci-date NO-LOCK NO-ERROR. 
  END. 
  FIND FIRST zimplan WHERE zimplan.datum GE ci-date NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE zimplan: 
    DO TRANSACTION: 
      i = i + 1. 
      na-list.anz = na-list.anz + 1. 
      /*MTmess-str = translateExtended ("Deleted records",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
      FIND CURRENT zimplan EXCLUSIVE-LOCK. 
        delete zimplan. 
    END. 
    FIND NEXT zimplan WHERE zimplan.datum GE ci-date NO-LOCK NO-ERROR. 
  END. 
  /*MTPAUSE 0. */
END. 



PROCEDURE create-roomplan: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE beg-datum AS DATE. 
DEFINE VARIABLE end-datum AS DATE. 
DEFINE VARIABLE curr-date AS DATE. 
  FIND FIRST na-list WHERE na-list.reihenfolge = 2. 
  /*MTmess-str = translateExtended ("Created records",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FOR EACH res-line WHERE res-line.active-flag = 0 AND 
    res-line.resstatus NE 11 AND res-line.ankunft GE ci-date NO-LOCK: 
    j = res-line.resstatus. 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
      NO-ERROR. 
    beg-datum = res-line.ankunft. 
    end-datum = res-line.abreise - 1. 
    IF AVAILABLE zimkateg THEN 
    DO curr-date = beg-datum TO end-datum: 
      DO TRANSACTION:
        FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr 
          AND resplan.datum = curr-date NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resplan THEN 
        DO: 
          i = i + 1. 
          na-list.anz = na-list.anz + 1. 
          /*MTmess-str = translateExtended ("Created records",lvCAREA,"") + " " + STRING(i). 
          DISP mess-str WITH FRAME frame1. */
          CREATE resplan. 
          ASSIGN
            resplan.datum = curr-date
            resplan.zikatnr = zimkateg.zikatnr
            resplan.anzzim[j] = res-line.zimmeranz. 
          . 
        END. 
        ELSE IF AVAILABLE resplan THEN
        DO:
            FIND CURRENT resplan EXCLUSIVE-LOCK. 
            resplan.anzzim[j] = resplan.anzzim[j] + res-line.zimmeranz.  
            FIND CURRENT resplan NO-LOCK. 
            RELEASE resplan.
        END.               
      END.
    END. 

    IF res-line.zinr NE "" THEN 
    DO curr-date = beg-datum TO end-datum: 
      DO TRANSACTION:
        FIND FIRST zimplan WHERE zimplan.datum = curr-date 
          AND zimplan.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE zimplan THEN 
        DO: 
          i = i + 1. 
          na-list.anz = na-list.anz + 1. 
          /*MTmess-str = translateExtended ("Created records",lvCAREA,"") + " " + STRING(i). */
          CREATE zimplan. 
          ASSIGN
            zimplan.datum = curr-date
            zimplan.zinr = res-line.zinr 
            zimplan.res-recid = RECID(res-line)
            zimplan.gastnrmember = res-line.gastnrmember 
            zimplan.bemerk = res-line.bemerk 
            zimplan.resstatus = res-line.resstatus
            zimplan.name = res-line.name
          . 
          FIND CURRENT zimplan NO-LOCK. 
        END.
      END.
    END. 
  END. 
 
  FOR EACH res-line WHERE res-line.active-flag = 1 AND 
    res-line.abreise GT ci-date AND res-line.resstatus NE 12 NO-LOCK: 
    j = res-line.resstatus. 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
      NO-ERROR. 
    beg-datum = ci-date. 
    end-datum = res-line.abreise - 1. 
    IF AVAILABLE zimkateg THEN 
    DO curr-date = beg-datum TO end-datum: 
      DO TRANSACTION:
        FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr 
          AND resplan.datum = curr-date NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resplan THEN 
        DO: 
          i = i + 1. 
          na-list.anz = na-list.anz + 1. 
          /*MTmess-str = translateExtended ("Created records",lvCAREA,"") + " " + STRING(i). 
          DISP mess-str WITH FRAME frame1. */
          CREATE resplan. 
          ASSIGN
            resplan.datum = curr-date
            resplan.zikatnr = zimkateg.zikatnr
            resplan.anzzim[j] = res-line.zimmeranz. 
          . 
        END.
        ELSE IF AVAILABLE resplan THEN
        DO:
            FIND CURRENT resplan EXCLUSIVE-LOCK. 
            resplan.anzzim[j] = resplan.anzzim[j] + res-line.zimmeranz. 
            FIND CURRENT resplan NO-LOCK. 
            RELEASE resplan.
        END.
      END.
    END. 

    IF res-line.resstatus EQ 6 THEN 
    DO: 
      DO curr-date = beg-datum TO end-datum: 
        DO TRANSACTION:
          FIND FIRST zimplan WHERE zimplan.datum = curr-date 
            AND zimplan.zinr = res-line.zinr NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE zimplan THEN 
          DO: 
            i = i + 1. 
            na-list.anz = na-list.anz + 1. 
            /*MTmess-str = translateExtended ("Created records",lvCAREA,"") + " " + STRING(i). */
            CREATE zimplan.
            ASSIGN
              zimplan.datum = curr-date
              zimplan.zinr = res-line.zinr 
              zimplan.res-recid = RECID(res-line) 
              zimplan.gastnrmember = res-line.gastnrmember
              zimplan.bemerk = res-line.bemerk
              zimplan.resstatus = res-line.resstatus 
              zimplan.name = res-line.name
            . 
            FIND CURRENT zimplan NO-LOCK. 
          END.
        END.
      END. 
    END. 
  END. 
  /*MTPAUSE 0. */
END. 



PROCEDURE update-rmstatus: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
DEFINE VARIABLE ci-date AS DATE. 
  
  FIND FIRST htparam WHERE paramnr = 87 no-lock.   /* ci-date */ 
  ci-date = htparam.fdate. 
  /*MTmess-str = translateExtended ("Updating Room Status",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST na-list WHERE na-list.reihenfolge = 3. 
  
  FIND FIRST zimmer NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE zimmer: 
    IF zimmer.personal = YES THEN
    DO TRANSACTION:
      FIND CURRENT zimmer EXCLUSIVE-LOCK.
      zimmer.personal = NO.
      FIND CURRENT zimmer NO-LOCK.
    END.
    IF zimmer.zistatus = 0 OR zimmer.zistatus = 1 OR zimmer.zistatus = 2 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO TRANSACTION: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        /*MTmess-str = translateExtended ("Updating Room Status",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        IF res-line.abreise = ci-date THEN zimmer.zistatus = 3. 
        ELSE zimmer.zistatus = 5. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
    END. 
    ELSE IF zimmer.zistatus = 3 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line AND res-line.abreise GT ci-date THEN 
      DO TRANSACTION: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        /*MTmess-str = translateExtended ("Updating Room Status",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 5. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
      ELSE IF NOT AVAILABLE res-line THEN 
      DO TRANSACTION: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        /*MTmess-str = translateExtended ("Updating Room Status",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 1. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
    END. 
    ELSE IF zimmer.zistatus = 4 OR zimmer.zistatus = 5 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line AND res-line.abreise EQ ci-date THEN 
      DO TRANSACTION: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        /*MTmess-str = translateExtended ("Updating Room Status",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 3. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
      ELSE IF NOT AVAILABLE res-line THEN 
      DO TRANSACTION: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        /*MTmess-str = translateExtended ("Updating Room Status",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        zimmer.zistatus = 1. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
      END. 
    END. 
    IF zimmer.zistatus = 6 
    THEN DO: 
      FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
        AND res-line.active-flag = 1 AND res-line.resstatus = 6 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO TRANSACTION: 
        i = i + 1. 
        na-list.anz = na-list.anz + 1. 
        /*MTmess-str = translateExtended ("Updating Room Status",lvCAREA,"") + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
        FIND CURRENT zimmer EXCLUSIVE-LOCK. 
        IF res-line.abreise = ci-date THEN zimmer.zistatus = 3. 
        ELSE zimmer.zistatus = 5. 
        zimmer.bediener-nr-stat = 0. 
        FIND CURRENT zimmer NO-LOCK. 
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
          EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE outorder THEN delete outorder. 
      END. 
    END. 
    FIND NEXT zimmer NO-LOCK NO-ERROR. 
  END. 
 
  FOR EACH zimkateg: 
    i = 0. 
    FOR EACH zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr NO-LOCK: 
      i = i + 1. 
    END. 
    zimkateg.maxzimanz = i. 
  END. 
 
  /*MTPAUSE 0. */
END. 
