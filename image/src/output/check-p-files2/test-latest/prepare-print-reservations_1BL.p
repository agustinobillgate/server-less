
DEF TEMP-TABLE t-list LIKE res-line
    FIELD bed-setup AS CHAR
    FIELD str-zipreis AS CHAR FORMAT "x(17)"
    FIELD mstr AS CHAR FORMAT "x(2)"
    FIELD zimkateg-kurzbez AS CHAR
    FIELD sharer-no AS INTEGER.                 /* 14/02/23 Rulita | 10E4B1 Req print lnl[RAMADA BY WYDHAM SUNSET ROAD]*/

DEF TEMP-TABLE t-guest LIKE guest.
DEF TEMP-TABLE t-reservation LIKE reservation.
DEF BUFFER bresline FOR res-line.               /* 14/02/23 Rulita | 10E4B1 Req print lnl[RAMADA BY WYDHAM SUNSET ROAD]*/

DEF INPUT  PARAMETER lresnr AS INT.
DEF INPUT  PARAMETER ta-gastnr  AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-guest.
DEF OUTPUT PARAMETER TABLE FOR t-reservation.
DEF OUTPUT PARAMETER TABLE FOR t-list.

FIND FIRST guest WHERE guest.gastnr = ta-gastnr NO-LOCK.
CREATE t-guest.
BUFFER-COPY guest TO t-guest.

FIND FIRST reservation WHERE reservation.resnr = lresnr NO-LOCK. 
CREATE t-reservation.
BUFFER-COPY reservation TO t-reservation.

FOR EACH res-line WHERE res-line.gastnr = ta-gastnr 
    AND res-line.resnr = lresnr AND res-line.resstatus NE 12 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
    NO-LOCK BY res-line.zinr BY res-line.l-zuordnung[3] 
    BY res-line.resstatus BY res-line.name: 

    CREATE t-list.
    BUFFER-COPY res-line TO t-list.
    t-list.zimkateg-kurzbez = zimkateg.kurzbez.

    t-list.bed-setup = "". 
    IF res-line.setup NE 0 THEN 
    DO: 
      FIND FIRST paramtext WHERE paramtext.txtnr = res-line.setup + 9200 
        NO-LOCK. 
          t-list.bed-setup = SUBSTR(paramtext.notes,1,1). 
    END. 

    IF res-line.zipreis LE 9999999 THEN 
        t-list.str-zipreis = STRING(res-line.zipreis, ">,>>>,>>9.99"). 
    ELSE t-list.str-zipreis = STRING(res-line.zipreis, ">>>>,>>>,>>9"). 

    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
      NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN
        t-list.str-zipreis = t-list.str-zipreis + STRING(waehrung.wabkurz, " x(4)"). 
    ELSE t-list.str-zipreis = t-list.str-zipreis + STRING("", " x(4)").

    FIND FIRST messages WHERE messages.resnr = res-line.resnr 
      AND messages.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE messages THEN t-list.mstr = "M ". 
    ELSE t-list.mstr = "  ".

    /* 14/02/23 Rulita | 10E4B1 Req print lnl[RAMADA BY WYDHAM SUNSET ROAD]*/
    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN DO:
        FIND FIRST bresline WHERE bresline.reslinnr NE res-line.reslinnr
            AND bresline.kontakt-nr EQ res-line.reslinnr
            AND (bresline.resstatus EQ 11 OR bresline.resstatus EQ 13) NO-LOCK NO-ERROR.
        IF AVAILABLE bresline THEN ASSIGN t-list.sharer-no = bresline.kontakt-nr.
    END.
    ELSE ASSIGN t-list.sharer-no = res-line.kontakt-nr.
END.
