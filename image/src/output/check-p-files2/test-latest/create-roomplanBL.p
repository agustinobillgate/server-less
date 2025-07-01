DEFINE TEMP-TABLE na-list 
  FIELD reihenfolge AS INTEGER 
  FIELD flag        AS INTEGER 
  FIELD bezeich     LIKE nightaudit.bezeichnung 
  FIELD anz         AS INTEGER FORMAT ">>,>>9". 

DEFINE INPUT-OUTPUT  PARAMETER TABLE FOR na-list.
DEFINE INPUT         PARAMETER ci-date  AS DATE.
DEFINE OUTPUT        PARAMETER i        AS INTEGER.


RUN create-roomplan.


/* SY 04 June 2016 */
RUN check-co-guestbill.

PROCEDURE create-roomplan: 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE beg-datum AS DATE. 
DEFINE VARIABLE end-datum AS DATE. 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 
 
  FIND FIRST na-list WHERE na-list.reihenfolge = 2. 
  FOR EACH res-line WHERE res-line.gastnr GT 0 AND 
    res-line.resstatus GE 1 AND res-line.resstatus LE 4 
    AND res-line.ankunft GE ci-date AND res-line.active-flag = 0 
    USE-INDEX gnrank_ix NO-LOCK: 
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE zimmer OR (AVAILABLE zimmer AND zimmer.sleeping) THEN 
    DO: 
      j = res-line.resstatus. 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
      beg-datum = res-line.ankunft. 
      end-datum = res-line.abreise - 1. 
      DO curr-date = beg-datum TO end-datum: 
        DO TRANSACTION:
          FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr 
            AND resplan.datum = curr-date NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE resplan THEN 
          DO: 
            i = i + 1. 
            na-list.anz = na-list.anz + 1. 
            CREATE resplan. 
            ASSIGN
              resplan.datum = curr-date
              resplan.zikatnr = zimkateg.zikatnr
            . 
          END. 
          anz = resplan.anzzim[j] + res-line.zimmeranz. 
          FIND CURRENT resplan EXCLUSIVE-LOCK. 
          resplan.anzzim[j] = anz. 
          FIND CURRENT resplan NO-LOCK. 
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
    res-line.abreise GT ci-date AND 
    (res-line.resstatus EQ 6 OR res-line.resstatus EQ 13) NO-LOCK, 
    FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
    IF zimmer.sleeping THEN 
    DO: 
      j = res-line.resstatus. 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
      beg-datum = ci-date. 
      end-datum = res-line.abreise - 1. 
      DO curr-date = beg-datum TO end-datum: 
        DO TRANSACTION:
          FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr 
            AND resplan.datum = curr-date NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE resplan THEN 
          DO: 
            i = i + 1. 
            na-list.anz = na-list.anz + 1. 
            CREATE resplan. 
            ASSIGN
              resplan.datum = curr-date
              resplan.zikatnr = zimkateg.zikatnr
            . 
          END. 
          anz = resplan.anzzim[j] + res-line.zimmeranz. 
          FIND CURRENT resplan EXCLUSIVE-LOCK. 
          resplan.anzzim[j] = anz. 
          FIND CURRENT resplan NO-LOCK. 
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
END. 

/* SY 04 June 2016 */
PROCEDURE check-co-guestbill:
DEF BUFFER bbuff FOR bill.
   FIND FIRST bill WHERE bill.resnr GT 0 AND bill.reslinnr GT 0
       AND bill.flag = 0 AND bill.saldo = 0 NO-LOCK NO-ERROR.
   DO WHILE AVAILABLE bill:
       FIND FIRST res-line WHERE res-line.resnr = bill.resnr
           AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
       IF NOT AVAILABLE res-line THEN
       DO:
           FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
               EXCLUSIVE-LOCK.
           bbuff.flag = 1.
           FIND CURRENT bbuff NO-LOCK.
           RELEASE bbuff.
       END.
       ELSE IF res-line.active-flag = 2 THEN
       DO:
           FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
               EXCLUSIVE-LOCK.
           bbuff.flag = 1.
           FIND CURRENT bbuff NO-LOCK.
           RELEASE bbuff.
       END.
       FIND NEXT bill WHERE bill.resnr GT 0 AND bill.reslinnr GT 0
          AND bill.flag = 0 AND bill.saldo = 0 NO-LOCK NO-ERROR.
   END.
   FOR EACH res-line WHERE res-line.active-flag = 1
       AND res-line.l-zuordnung[3] = 0 NO-LOCK:
       FIND FIRST bill WHERE bill.resnr = res-line.resnr 
           AND bill.parent-nr = res-line.reslinnr NO-LOCK NO-ERROR.
       DO WHILE AVAILABLE bill:
           IF bill.zinr NE res-line.zinr THEN
           DO:
               FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                   EXCLUSIVE-LOCK.
               bbuff.zinr = res-line.zinr.
               FIND CURRENT bbuff NO-LOCK.
               RELEASE bbuff.
           END.
           FIND NEXT bill WHERE bill.resnr = res-line.resnr 
              AND bill.parent-nr = res-line.reslinnr NO-LOCK NO-ERROR.
       END.   
   END.
END.
