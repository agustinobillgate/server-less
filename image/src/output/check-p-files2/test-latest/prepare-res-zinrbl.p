
DEFINE TEMP-TABLE t-zimkateg   LIKE zimkateg.
DEFINE TEMP-TABLE t-paramtext1 LIKE paramtext.
DEFINE TEMP-TABLE t-paramtext2 LIKE paramtext.
DEFINE TEMP-TABLE t-paramtext3 LIKE paramtext.
DEFINE TEMP-TABLE t-res-line   LIKE res-line.
DEFINE TEMP-TABLE t-zimmer     LIKE zimmer.
DEFINE TEMP-TABLE zimkateg1    LIKE zimkateg. 
DEFINE TEMP-TABLE res-line1    LIKE res-line. 

DEFINE TEMP-TABLE htl-feature 
  FIELD s AS CHAR FORMAT "x(32)" LABEL "Possible Room Features" /*FONT 1 */
  FIELD flag AS INTEGER INITIAL 1. 

DEFINE TEMP-TABLE room-list 
  FIELD i          AS INTEGER 
  FIELD flag       AS LOGICAL INITIAL YES 
  FIELD sleeping   AS LOGICAL INITIAL YES
  FIELD feature    AS CHAR FORMAT "x(16)" EXTENT 99 
  FIELD himmelsr   AS CHAR FORMAT "x(60)" LABEL "Room Features" 
  FIELD build      AS CHAR FORMAT "x(40)" 
  FIELD zikennz    AS CHAR FORMAT "x(1)" COLUMN-LABEL "A" 
  FIELD build-flag AS CHAR FORMAT "x(1)" LABEL "P" 
  FIELD zistat     AS CHAR FORMAT "x(2)" INITIAL "  " LABEL "ST" 
  FIELD infochar   AS CHAR FORMAT "x(2)" LABEL "    " 
  FIELD zinr       LIKE zimmer.zinr LABEL "RmNo" 
  FIELD bezeich    AS CHAR FORMAT "x(24)" LABEL "Description" 
  FIELD etage      AS INTEGER FORMAT ">9" LABEL "Fl" 
  FIELD outlook    AS CHAR FORMAT "x(14)" LABEL "Overlook" 
  FIELD setup      AS CHAR FORMAT "x(14)" LABEL "BedSetup" 
  FIELD name       AS CHAR FORMAT "x(24)" LABEL "MainGuest" 
  FIELD comment    AS CHAR FORMAT "x(32)" LABEL "Guest Comment" 
  FIELD verbindung1 AS CHAR FORMAT "x(6)" LABEL "Connecting"
  FIELD verbindung2 AS CHAR FORMAT "x(6)" LABEL "Connecting"
  FIELD infonum    AS INTEGER FORMAT "9" INITIAL 3 
  FIELD prioritaet AS INTEGER 
  FIELD recid1     AS INTEGER INITIAL 0 
  FIELD recid2     AS INTEGER INITIAL 0
  FIELD infostr    AS CHAR
.

DEF INPUT PARAMETER c-rmcat     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER resnr       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinnr    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER i-setup     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER sharer      AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER ankunft1    AS DATE    NO-UNDO.
DEF INPUT PARAMETER abreise1    AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER ci-date AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-paramtext1.
DEF OUTPUT PARAMETER TABLE FOR t-paramtext2.
DEF OUTPUT PARAMETER TABLE FOR t-paramtext3.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.
DEF OUTPUT PARAMETER TABLE FOR zimkateg1.
DEF OUTPUT PARAMETER TABLE FOR htl-feature.
DEF OUTPUT PARAMETER TABLE FOR room-list.

DEF VARIABLE p-text  AS CHAR NO-UNDO.
DEF VAR int-tzimkategzikatnr AS INTEGER. /*Eko 30 mar 2016*/

RUN htpdate.p (87, OUTPUT ci-date).

RUN read-zimkategbl.p (2, ?, c-rmcat, OUTPUT TABLE t-zimkateg).
FIND FIRST t-zimkateg NO-ERROR.
IF AVAILABLE t-zimkateg THEN int-tzimkategzikatnr = t-zimkateg.zikatnr. /*Eko 30 mar 2016*/

RUN read-res-linebl.p (1, resnr, reslinnr, ?, ?, ?,?,?,?,?,?, 
    OUTPUT TABLE t-res-line).
FIND FIRST t-res-line NO-ERROR.
RUN read-zimkategbl.p (3, ?, ?, OUTPUT TABLE zimkateg1).

RUN read-paramtextbl.p (3, 9201, OUTPUT p-text,
    OUTPUT TABLE t-paramtext1). /* ALL possible bed setup */

RUN read-paramtextbl.p (3, 230, OUTPUT p-text, 
    OUTPUT TABLE t-paramtext2).

IF i-setup GT 0 THEN RUN read-paramtextbl.p (2, (i-setup + 9200), 
   OUTPUT p-text, OUTPUT TABLE t-paramtext3).  /* specific bed setup */

IF sharer THEN 
DO: 
    RUN read-res-linebl.p (4, resnr, ?,?, ?, ?,?,?,?,?,?, 
      OUTPUT TABLE res-line1).
    FOR EACH res-line1 WHERE res-line1.zinr NE "" 
        AND res-line1.resstatus LE 6 
        BY res-line1.zinr: 
      IF res-line1.ankunft LE ankunft1 AND res-line1.abreise GE abreise1 THEN 
      DO: 
        RUN read-zimmerbl.p (1, res-line1.zinr, ?,?, 
            OUTPUT TABLE t-zimmer).
        FIND FIRST t-zimmer.
        RELEASE paramtext.
        IF t-zimmer.zikatnr = int-tzimkategzikatnr THEN /*Eko 30 mar 2016*/
        DO: 
          IF t-zimmer.setup GT 0 THEN 
            FIND FIRST paramtext WHERE paramtext.txtnr 
              = (t-zimmer.setup + 9200) NO-LOCK NO-ERROR.
          CREATE room-list. 
          ASSIGN
            room-list.zinr        = t-zimmer.zinr
            room-list.prioritaet  = t-zimmer.prioritaet 
            room-list.name        = res-line1.name
          . 
          IF AVAILABLE paramtext THEN
             ASSIGN room-list.setup = paramtext.ptexte.
        END. 
      END. 
    END. 
END.
ELSE 
RUN res-zinrbl.p (1, resnr, reslinnr, int-tzimkategzikatnr,  /*Eko 30 mar 2016*/
    ankunft1, abreise1, OUTPUT TABLE room-list, 
    OUTPUT TABLE htl-feature).
