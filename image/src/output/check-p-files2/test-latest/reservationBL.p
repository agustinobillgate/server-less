
DEFINE TEMP-TABLE mainres-list 
  FIELD resnr      AS INTEGER FORMAT ">>>>>>9"             LABEL "ResNo" 
  FIELD zimanz     AS INTEGER FORMAT ">>9"                 LABEL "Qty" 
  FIELD ankunft    AS DATE    INITIAL 01/01/2099           LABEL "Arrival" 
  FIELD abreise    AS DATE    INITIAL 01/01/1998           LABEL "Depart" 
  FIELD segm       AS INTEGER FORMAT ">>9"                 LABEL "Seg" 
  FIELD deposit    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Deposit" 
  FIELD until      AS DATE                                 LABEL "DueDate" 
  FIELD paid       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Paid Amount" 
  FIELD id1        AS CHAR    FORMAT "x(3)"                LABEL "ID" 
  FIELD id2        AS CHAR    FORMAT "x(3)"                LABEL "ID" 
  FIELD id2-date   AS DATE                                 LABEL "ChgDate" 
  FIELD groupname  AS CHAR    FORMAT "x(29)"               LABEL "Group Name" 
  FIELD grpflag    AS LOGICAL 
  FIELD bemerk     AS CHAR    FORMAT "x(32)" 
  FIELD voucher    AS CHAR    FORMAT "x(20)"               LABEL "Voucher No"
  FIELD vesrdepot2 AS CHAR
  FIELD arrival    AS LOGICAL INITIAL NO 
  FIELD resident   AS LOGICAL INITIAL NO 
  FIELD arr-today  AS LOGICAL INITIAL NO
  FIELD last-reslinnr AS INTEGER /*FDL - Issue vhpCloud Hotel Pelangi Bogor*/
.

DEF TEMP-TABLE res-list
  FIELD name         LIKE res-line.NAME FORMAT "x(31)" 
  FIELD abreise      LIKE res-line.abreise 
  FIELD zinr         LIKE res-line.zinr 
  FIELD kurzbez      LIKE zimkateg.kurzbez FORMAT "x(5)" 
  FIELD zipreis      LIKE res-line.zipreis FORMAT ">>>,>>>,>>>,>>9.99" 
  FIELD arrangement  LIKE res-line.arrangement COLUMN-LABEL "ArgCode" 
  FIELD erwachs      LIKE res-line.erwachs
  FIELD gratis       LIKE res-line.gratis
  FIELD kind1        LIKE res-line.kind1
  FIELD kind2        LIKE res-line.kind2
  FIELD ankunft      LIKE res-line.ankunft
  FIELD resstatus    LIKE res-line.resstatus
  FIELD kontakt-nr   LIKE res-line.kontakt-nr
  FIELD zimmeranz    LIKE res-line.zimmeranz
  FIELD anztage      LIKE res-line.anztage
  FIELD changed-id   LIKE res-line.changed-id
  FIELD changed      LIKE res-line.changed
  FIELD ratecode     AS CHAR COLUMN-LABEL "RCode" 
  FIELD bemerk       AS CHAR
  FIELD l-zuord3     AS INTEGER 
  FIELD resnr        AS INTEGER
  FIELD reslinnr     AS INTEGER
  FIELD gastnrmember AS INTEGER
  FIELD betrieb-gast AS INTEGER
  FIELD zikatnr      AS INTEGER
  FIELD reserve-int  AS INTEGER
  FIELD kontignr     AS INTEGER
  FIELD karteityp    AS INTEGER
  FIELD allot-flag   AS INTEGER
  FIELD kontcode     AS CHAR
.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER gastNo    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resNo     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR mainres-list.
DEF OUTPUT PARAMETER TABLE FOR res-list.

DEF VAR ci-date AS DATE NO-UNDO.
DEF VAR i       AS INT  NO-UNDO.
DEF VAR str     AS CHAR NO-UNDO.
DEF BUFFER bresline FOR res-line.

DEF VARIABLE res-bemerk AS CHARACTER NO-UNDO.
DEF VARIABLE loopk AS INTEGER NO-UNDO.

RUN htpdate.p (87, OUTPUT ci-date).

CASE case-type:
    WHEN 1 THEN
    DO:
      IF resNo = 0 THEN
      FOR EACH reservation WHERE reservation.gastnr = gastNo
        AND reservation.activeflag = 0 NO-LOCK,
        FIRST res-line WHERE res-line.resnr = reservation.resnr
        AND res-line.active-flag LE 1 NO-LOCK BY reservation.resnr:
        CREATE mainres-list. 
        ASSIGN
          mainres-list.resnr        = reservation.resnr
          mainres-list.deposit      = reservation.depositgef 
          mainres-list.until        = reservation.limitdate 
          mainres-list.paid         = reservation.depositbez + reservation.depositbez2 /* Malik Serverless : depositbez + depositbez2 -> reservation.depositbez + reservation.depositbez2 */
          mainres-list.segm         = reservation.segmentcode 
          mainres-list.groupname    = reservation.groupname
          mainres-list.bemerk       = reservation.bemerk
          mainres-list.id1          = reservation.useridanlage 
          mainres-list.id2          = reservation.useridmutat 
          mainres-list.id2-date     = reservation.mutdat
          mainres-list.grpflag      = reservation.grpflag
          mainres-list.voucher      = reservation.vesrdepot
        . 
        RUN update-mainres. 
      END.
      ELSE
      DO:
        FIND FIRST reservation WHERE reservation.gastnr = gastNo
          AND reservation.resnr = resNo
          AND reservation.activeflag = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE reservation THEN
        DO:
          CREATE mainres-list. 
          ASSIGN
            mainres-list.resnr        = reservation.resnr
            mainres-list.deposit      = reservation.depositgef 
            mainres-list.until        = reservation.limitdate 
            mainres-list.paid         = reservation.depositbez + reservation.depositbez2 /* Malik Serverless : depositbez + depositbez2 -> reservation.depositbez + reservation.depositbez2 */
            mainres-list.segm         = reservation.segmentcode 
            mainres-list.groupname    = reservation.groupname
            mainres-list.bemerk       = reservation.bemerk
            mainres-list.id1          = reservation.useridanlage 
            mainres-list.id2          = reservation.useridmutat 
            mainres-list.id2-date     = reservation.mutdat
            mainres-list.grpflag      = reservation.grpflag
            mainres-list.voucher      = reservation.vesrdepot
          . 
          RUN update-mainres. 
        END.
      END.
    END.
    WHEN 2 THEN
    DO:
      FOR EACH res-line WHERE res-line.resnr = resNo
        AND res-line.active-flag LE 1 AND res-line.resstatus NE 12
        AND res-line.resstatus NE 99 NO-LOCK:
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK.
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember
            NO-LOCK.
        CREATE res-list.
        BUFFER-COPY res-line TO res-list.

        /*FDL August 28, 2023 => Ticket 024948*/
        ASSIGN  
            res-list.bemerk = REPLACE(res-list.bemerk,CHR(10),"").
            res-list.bemerk = REPLACE(res-list.bemerk,CHR(13),"").
            res-list.bemerk = REPLACE(res-list.bemerk,"~n","").
            res-list.bemerk = REPLACE(res-list.bemerk,"\n","").
            res-list.bemerk = REPLACE(res-list.bemerk,"~r","").
            res-list.bemerk = REPLACE(res-list.bemerk,"~r~n","").
            res-list.bemerk = REPLACE(res-list.bemerk,CHR(10) + CHR(13),"").
       
        res-bemerk = "".
        DO loopk = 1 TO LENGTH(res-list.bemerk):
            IF ASC(SUBSTR(res-list.bemerk, loopk, 1)) = 0 THEN.
            ELSE res-bemerk = res-bemerk + SUBSTR(res-list.bemerk, loopk, 1). 
        END.
        ASSIGN res-list.bemerk = res-bemerk.
       
        IF LENGTH(res-list.bemerk) LT 3 THEN res-list.bemerk = REPLACE(res-list.bemerk,CHR(32),"").
        IF LENGTH(res-list.bemerk) EQ ? THEN res-list.bemerk = "".
        /*End FDL*/

        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN res-list.ratecode = SUBSTR(str,7).
        END.

        ASSIGN
          res-list.karteityp = guest.karteityp
          res-list.l-zuord3  = res-line.l-zuordnung[3] 
          res-list.kurzbez   = zimkateg.kurzbez
        .                         

        FIND FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
          AND kontline.betriebsnr = 0 AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE kontline THEN 
        ASSIGN
          res-list.allot-flag = 1
          res-list.kontcode   = kontline.kontcode
        .
        ELSE
        DO:
          FIND FIRST kontline WHERE kontline.kontignr = - res-line.kontignr 
            AND kontline.betriebsnr = 1 AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
          IF AVAILABLE kontline THEN 
          ASSIGN
            res-list.allot-flag = -1
            res-list.kontcode   = kontline.kontcode
          .
        END.
      END.
    END.
    WHEN 3 THEN RUN update-gcfinfo.
END CASE.

PROCEDURE update-mainres: 
  ASSIGN
    mainres-list.ankunft   = 01/01/2099
    mainres-list.abreise   = 01/01/1998 
    mainres-list.zimanz    = 0 
    mainres-list.arrival   = NO 
    mainres-list.arr-today = NO 
    mainres-list.resident  = NO
  . 
  FOR EACH res-line WHERE res-line.resnr = mainres-list.resnr 
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
    AND res-line.resstatus NE 12
    AND res-line.resstatus NE 99 NO-LOCK: 
    IF res-line.resstatus LE 6 THEN
      mainres-list.zimanz   = mainres-list.zimanz + res-line.zimmeranz. 
    IF mainres-list.ankunft > res-line.ankunft THEN 
       mainres-list.ankunft = res-line.ankunft. 
    IF mainres-list.abreise < res-line.abreise THEN 
       mainres-list.abreise = res-line.abreise. 
    IF (res-line.resstatus LE 5 OR res-line.resstatus = 11) THEN 
       mainres-list.arrival = YES. 
    IF mainres-list.arrival = YES AND res-line.ankunft = ci-date THEN 
       mainres-list.arr-today = YES. 
    IF res-line.resstatus = 6 OR res-line.resstatus = 13 THEN 
       mainres-list.resident = YES. 
  END. 

  /*FDL - Issue vhpCloud Hotel Pelangi Bogor*/
  FOR EACH res-line WHERE res-line.resnr = mainres-list.resnr 
      NO-LOCK BY res-line.reslinnr DESC:

      mainres-list.last-reslinnr = res-line.reslinnr.
      LEAVE.
  END.
END. 

PROCEDURE update-gcfinfo: 
DEF VAR ci-date AS DATE NO-UNDO.
  RUN htpdate.p (87, OUTPUT ci-date).
  FOR EACH res-line WHERE res-line.resnr = resNo
    AND res-line.gastnr = gastNo AND res-line.active-flag LE 1
    AND res-line.resstatus NE 12
    AND res-line.resstatus NE 99 NO-LOCK:
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
      EXCLUSIVE-LOCK. 
    IF guest.erste-res = ? THEN guest.erste-res = ci-date. 
    IF guest.naechste-res = ? OR guest.naechste-res LT res-line.ankunft 
      THEN guest.naechste-res = res-line.ankunft. 
    guest.letzte-res = ci-date. 
    RELEASE guest. 
  END. 
END. 
