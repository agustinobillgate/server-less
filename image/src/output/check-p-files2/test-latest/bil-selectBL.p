DEFINE TEMP-TABLE b1-list
    FIELD zinr       LIKE bill.zinr
    FIELD billnr     LIKE bill.billnr
    FIELD rechnr     LIKE bill.rechnr
    FIELD name       LIKE bill.name
    FIELD saldo      LIKE bill.saldo
    FIELD resnr      LIKE bill.resnr
    FIELD reslinnr   LIKE bill.reslinnr
    FIELD datum      LIKE bill.datum
    FIELD printnr    LIKE bill.printnr
    FIELD vesrcod    LIKE bill.vesrcod
    FIELD rec-id     AS INTEGER
    FIELD fg-col     AS LOGICAL INIT NO
    FIELD resname    AS CHAR FORMAT "x(19)"
    FIELD address    AS CHAR FORMAT "x(19)"
    FIELD city       AS CHAR FORMAT "x(19)"
    FIELD b-comments AS CHAR
    FIELD guest-name AS CHAR            /*ragung penambahan guest name req Web*/
    .


DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER sorttype     AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER zinr         AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER bil-int      AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER curr-gastnr  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER ci-date      AS DATE     NO-UNDO.

DEFINE INPUT PARAMETER gastname     AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER to-name      AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER rechnr       AS INTEGER  NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR b1-list.

DEFINE BUFFER resline     FOR res-line. 
DEFINE BUFFER rline       FOR res-line.
DEFINE BUFFER guestmember FOR guest. 
DEFINE BUFFER mbill       FOR bill.

/* SY 04 June 2016 */
DEFINE VARIABLE actFlag   AS INTEGER NO-UNDO.
ASSIGN actFlag = bil-int + 1. /* = 1 if bill active, 2 if closed bill */

/* SY 07 June 2016 */
DEFINE BUFFER bbuff FOR bill.

/*ITA 130616*/
DEFINE VARIABLE bl-saldo  AS DECIMAL NO-UNDO.
DEFINE BUFFER tbuff FOR bill.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "bil-select". 

IF bil-int = 0 THEN RUN disp-bill-list0.
ELSE RUN disp-bill-list1.


PROCEDURE disp-bill-list0: 
DEFINE VARIABLE to-rechnr AS INTEGER. 
DEFINE VARIABLE fr-name   AS CHAR INITIAL "". 
DEFINE VARIABLE to-name   AS CHAR. 
DEFINE VARIABLE rmno      AS CHAR. 

  IF sorttype = 1 THEN 
  DO: 
    /* SY 07 June 2016 */
    IF bil-int = 0 THEN
    FOR EACH res-line WHERE res-line.active-flag = 1
        AND res-line.zinr = zinr
        AND res-line.resstatus NE 12
        AND res-line.l-zuordnung[3] = 0 NO-LOCK:
      FOR EACH bill WHERE bill.resnr = res-line.resnr
          AND bill.parent-nr = res-line.reslinnr
          AND bill.flag = 0 NO-LOCK:

          ASSIGN bl-saldo = 0.
          FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
                ASSIGN bl-saldo = bl-saldo + bill-line.betrag.
          END.

          IF bill.zinr NE res-line.zinr THEN
          DO:
            FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                EXCLUSIVE-LOCK.
            ASSIGN bbuff.zinr = res-line.zinr.
            FIND CURRENT bbuff NO-LOCK.
            RELEASE bbuff.
          END.
            

          /*ITA 130616*/
          IF bl-saldo NE bill.saldo THEN DO:
                FIND FIRST tbuff WHERE RECID(tbuff) = RECID(bill)
                     EXCLUSIVE-LOCK.
                tbuff.saldo = bl-saldo.
                FIND CURRENT tbuff NO-LOCK.
                RELEASE tbuff.
          END.
      END.
    END.     

    FOR EACH bill WHERE bill.zinr GE zinr AND bill.zinr NE "" 
      AND bill.flag = bil-int NO-LOCK,
      FIRST rline WHERE rline.resnr = bill.resnr 
      AND rline.reslinnr = bill.parent-nr 
      AND rline.active-flag = actFlag /* SY 04 June 2016 */
      NO-LOCK BY bill.zinr BY bill.billnr:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 2 THEN 
  DO: 
    IF curr-gastnr = 0 THEN 
    DO: 
      IF gastname = "" THEN gastname = "a". 
      IF gastname = "*" THEN to-name = "zz". 
      ELSE 
      DO: 
        fr-name = gastname. 
        to-name = chr(asc(SUBSTR(gastname,1,1)) + 1). 
      END. 
      FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
        AND bill.name GE fr-name AND bill.name LE to-name 
        AND bill.billtyp = 0 NO-LOCK,
        FIRST rline WHERE rline.resnr = bill.resnr 
        AND rline.reslinnr = bill.parent-nr 
        AND rline.active-flag = actFlag /* SY 04 June 2016 */
        NO-LOCK BY bill.name BY bill.zinr:
          RUN assign-it.
      END.
      FIND FIRST b1-list NO-ERROR.
      IF NOT AVAILABLE b1-list THEN 
      FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
        AND bill.name GE fr-name AND bill.billtyp = 0 NO-LOCK,
        FIRST rline WHERE rline.resnr = bill.resnr 
        AND rline.reslinnr = bill.parent-nr 
        AND rline.active-flag = actFlag /* SY 04 June 2016 */
        NO-LOCK BY bill.name BY bill.zinr:
          RUN assign-it.
      END.
    END. 
    ELSE
    DO: 
      FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
        AND bill.gastnr = curr-gastnr AND bill.billtyp = 0 
        NO-LOCK USE-INDEX gastnr_index,
        FIRST rline WHERE rline.resnr = bill.resnr 
        AND rline.reslinnr = bill.parent-nr 
        AND rline.active-flag = actFlag /* SY 04 June 2016 */
        NO-LOCK BY bill.name BY bill.zinr descending:
          RUN assign-it.
      END.
    END.
  END. 
  ELSE IF sorttype = 3 THEN 
  DO: 
    to-rechnr = rechnr + 1000. 
    FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
      AND bill.rechnr EQ rechnr NO-LOCK,
      FIRST rline WHERE rline.resnr = bill.resnr 
      AND rline.reslinnr = bill.parent-nr 
      AND rline.active-flag = actFlag /* SY 04 June 2016 */
      NO-LOCK BY bill.rechnr:
        RUN assign-it.
    END.
    FIND FIRST b1-list NO-ERROR.
    IF NOT AVAILABLE b1-list THEN 
    FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
      AND bill.rechnr GE rechnr AND bill.rechnr LE to-rechnr NO-LOCK,
      FIRST rline WHERE rline.resnr = bill.resnr 
      AND rline.reslinnr = bill.parent-nr 
      AND rline.active-flag = actFlag /* SY 04 June 2016 */
      NO-LOCK BY bill.rechnr:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 4 THEN 
  DO: 
    FOR EACH rline WHERE rline.active-flag = 1
      AND rline.resstatus NE 12
      AND rline.abreise = ci-date
      AND rline.l-zuordnung[3] = 0 NO-LOCK BY rline.zinr:
      FOR EACH bill WHERE bill.resnr = rline.resnr
        AND bill.parent-nr = rline.reslinnr 
        AND bill.flag = 0 NO-LOCK BY bill.billnr:
        RUN assign-it.
      END.
    END.
  END. 
END. 


PROCEDURE disp-bill-list1: 
DEFINE VARIABLE to-rechnr  AS INTEGER. 
DEFINE VARIABLE fr-name    AS CHAR INITIAL "". 
DEFINE VARIABLE to-name    AS CHAR. 
DEFINE VARIABLE rmno       AS CHAR.

  IF sorttype = 1 THEN 
  DO: 
    IF zinr NE "" THEN 
    DO: 
      /* SY 07 June 2016 */
      IF bil-int = 0 THEN
      FOR EACH res-line WHERE res-line.active-flag = 1
          AND res-line.zinr = zinr
          AND res-line.resstatus NE 12
          AND res-line.l-zuordnung[3] = 0 NO-LOCK:
        FOR EACH bill WHERE bill.resnr = res-line.resnr
            AND bill.parent-nr = res-line.reslinnr
            AND bill.flag = 0 NO-LOCK:

            ASSIGN bl-saldo = 0.
            FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
                  ASSIGN bl-saldo = bl-saldo + bill-line.betrag.
            END.
            
            IF bill.zinr NE res-line.zinr THEN
            DO:
              FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                EXCLUSIVE-LOCK.
              ASSIGN bbuff.zinr = res-line.zinr.
              FIND CURRENT bbuff NO-LOCK.
              RELEASE bbuff.
            END.
            

            /*ITA 130616*/
            IF bl-saldo NE bill.saldo THEN DO:
                FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                     EXCLUSIVE-LOCK.
                bbuff.saldo = bl-saldo.
                FIND CURRENT bbuff NO-LOCK.
                RELEASE bbuff.
            END.
        END.
      END.      

      FOR EACH bill WHERE bill.zinr = zinr 
        AND bill.flag = bil-int AND bill.rechnr NE 0 NO-LOCK,
        FIRST rline WHERE rline.resnr = bill.resnr 
        AND rline.reslinnr = bill.parent-nr 
        AND rline.active-flag = actFlag /* SY 04 June 2016 */
        NO-LOCK BY bill.rechnr descending:
          RUN assign-it.
      END.
    END.
  END. 
  ELSE IF sorttype = 2 THEN 
  DO: 
    IF curr-gastnr = 0 THEN 
    DO: 
      IF gastname = "" THEN gastname = "a". 
      IF gastname = "*" THEN to-name = "zz". 
      ELSE 
      DO: 
        fr-name = gastname. 
        to-name = CHR(ASC(SUBSTR(gastname,1,1)) + 1). 
      END. 
      FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
        AND bill.name GE gastname AND bill.name LE to-name AND bill.billtyp = 0 
        AND bill.rechnr NE 0 NO-LOCK,
        FIRST rline WHERE rline.resnr = bill.resnr 
        AND rline.reslinnr = bill.parent-nr 
        AND rline.active-flag = actFlag /* SY 04 June 2016 */
        NO-LOCK BY bill.name BY bill.rechnr DESCENDING:
          RUN assign-it.
      END.
      FIND FIRST b1-list NO-ERROR.
      IF NOT AVAILABLE b1-list THEN 
      FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
        AND bill.name GE gastname AND bill.billtyp = 0 
        AND bill.rechnr NE 0 NO-LOCK,
        FIRST rline WHERE rline.resnr = bill.resnr 
        AND rline.reslinnr = bill.parent-nr 
        AND rline.active-flag = actFlag /* SY 04 June 2016 */
        NO-LOCK BY bill.name BY bill.rechnr DESCENDING:
          RUN assign-it.
      END.
    END. 
    ELSE 
    DO: 
      FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
        AND bill.gastnr = curr-gastnr AND bill.billtyp = 0 
        AND bill.rechnr NE 0 NO-LOCK USE-INDEX gastnr_index,
        FIRST rline WHERE rline.resnr = bill.resnr 
        AND rline.reslinnr = bill.parent-nr 
        AND rline.abreise = ci-date NO-LOCK
        BY bill.name BY bill.rechnr descending:
          RUN assign-it.
      END.
    END.
  END. 
  ELSE IF sorttype = 3 THEN 
  DO: 
    IF rechnr NE 0 THEN 
    DO: 
      FOR EACH bill WHERE bill.zinr GT "" AND bill.flag = bil-int 
        AND bill.rechnr EQ rechnr NO-LOCK,
        FIRST rline WHERE rline.resnr = bill.resnr 
        AND rline.reslinnr = bill.parent-nr 
        AND rline.active-flag = actFlag /* SY 04 June 2016 */
        NO-LOCK:
          RUN assign-it.
      END.
    END.
  END. 
  ELSE IF sorttype = 4 THEN 
  DO: 
    FOR EACH rline WHERE rline.active-flag = 2
      AND rline.resstatus EQ 8
      AND rline.abreise = ci-date
      AND rline.l-zuordnung[3] = 0 NO-LOCK BY rline.zinr:
      FOR EACH bill WHERE bill.resnr = rline.resnr
        AND bill.parent-nr = rline.reslinnr 
        AND bill.flag = 1 USE-INDEX resrec_index NO-LOCK BY bill.billnr:
        RUN assign-it.
      END.
    END.
  END. 
END. 


PROCEDURE assign-it:
DEFINE buffer usr FOR bediener. 
    
    /*ITA 130616*/
    ASSIGN bl-saldo = 0.
    /*
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
          ASSIGN bl-saldo = bl-saldo + bill-line.betrag.
    END.
    */
    FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE bill-line:
        bl-saldo = bl-saldo + bill-line.betrag.
        FIND NEXT bill-line WHERE bill-line.rechnr EQ bill.rechnr NO-LOCK NO-ERROR.
    END.

    IF bl-saldo NE bill.saldo THEN DO:
        FIND FIRST tbuff WHERE RECID(tbuff) = RECID(bill)
             EXCLUSIVE-LOCK.
        tbuff.saldo = bl-saldo.
        FIND CURRENT tbuff NO-LOCK.
        RELEASE tbuff.
    END.

    CREATE b1-list.
    ASSIGN
      b1-list.zinr      = bill.zinr
      b1-list.billnr    = bill.billnr
      b1-list.rechnr    = bill.rechnr
      b1-list.name      = bill.name
      b1-list.saldo     = bill.saldo
      b1-list.resnr     = bill.resnr
      b1-list.reslinnr  = bill.reslinnr
      b1-list.datum     = bill.datum
      b1-list.printnr   = bill.printnr
      b1-list.vesrcod   = bill.vesrcod
      b1-list.rec-id    = RECID(bill).

    FIND FIRST mbill WHERE mbill.resnr = bill.resnr
      AND mbill.reslinnr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE mbill THEN
        ASSIGN b1-list.fg-col = YES.


    FIND FIRST usr WHERE usr.userinit = bill.vesrcod NO-LOCK NO-ERROR. 
  IF AVAILABLE usr THEN b1-list.b-comments = translateExtended ("C/O by:",lvCAREA,"") + " " + usr.username + chr(10). 
 
  IF AVAILABLE bill THEN
  DO:
    FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE reservation THEN 
    DO: 
      FIND FIRST resline WHERE resline.resnr = bill.resnr 
        AND resline.reslinnr = bill.parent-nr NO-LOCK NO-ERROR. 
      IF AVAILABLE resline THEN 
      DO: 
        FIND FIRST guestmember WHERE 
          guestmember.gastnr = resline.gastnrmember NO-LOCK. 
        b1-list.resname = guestmember.name + ", " + guestmember.vorname1 
          + " " + guestmember.anrede1. 
        b1-list.guest-name  = guestmember.anrede1 + " " + guestmember.name + ", " + guestmember.vorname1.
        b1-list.address = guestmember.adresse1. 
        b1-list.city = guestmember.wohnort + " " + guestmember.plz. 
        b1-list.b-comments = b1-list.b-comments + translateExtended ("Departure:",lvCAREA,"") + " " + STRING(resline.abreise) + chr(10). 
        IF guestmember.bemerkung NE "" THEN 
          b1-list.b-comments = b1-list.b-comments + guestmember.bemerkung + chr(10). 
        IF reservation.bemerk NE "" THEN 
          b1-list.b-comments = b1-list.b-comments + reservation.bemerk + chr(10). 
        IF resline.bemerk NE "" THEN 
          b1-list.b-comments = b1-list.b-comments + resline.bemerk. 
      END.
    END. 
    ELSE 
    DO: /* res-line deleted, try TO GET the data from history */ 
      IF bill.flag = 1 THEN 
      DO: 
        FIND FIRST history WHERE history.resnr = bill.resnr 
          AND history.reslinnr = bill.parent-nr 
          AND history.zi-wechsel = NO NO-LOCK NO-ERROR. 
        IF AVAILABLE history THEN 
        DO: 
          FIND FIRST guestmember WHERE 
            guestmember.gastnr = history.gastnr NO-LOCK. 
          b1-list.resname = guestmember.name + ", " + guestmember.vorname1 
              + " " + guestmember.anrede1. 
          b1-list.guest-name  = guestmember.anrede1 + " " + guestmember.name + ", " + guestmember.vorname1.
          b1-list.address = guestmember.adresse1. 
          b1-list.city = guestmember.wohnort + " " + guestmember.plz. 
          b1-list.b-comments = b1-list.b-comments + translateExtended ("Departure:",lvCAREA,"") + " " + STRING(history.abreise) 
            + chr(10). 
          b1-list.b-comments = b1-list.b-comments + history.bemerk. 
        END. 
      END. 
    END.
  END.
END.
