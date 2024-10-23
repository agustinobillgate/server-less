
DEFINE TEMP-TABLE output-list 
    FIELD STR AS CHAR
    FIELD cperson AS CHAR
    FIELD tevent  AS CHAR
    FIELD venue   AS CHAR
    FIELD pax     AS CHAR
  .

DEFINE TEMP-TABLE t-out
    FIELD rsv-date  AS CHAR     FORMAT "x(8)"   COLUMN-LABEL "RsvDate"
    FIELD b-date    AS CHAR     FORMAT "x(8)"   COLUMN-LABEL "Date"
    FIELD rsv-no    AS CHAR     FORMAT "x(8)"   COLUMN-LABEL "RsvNo" 
    FIELD resline   AS CHAR     FORMAT "x(3)"   COLUMN-LABEL "ResLine" 
    FIELD engager   AS CHAR     FORMAT "x(32)"  COLUMN-LABEL "Engager"
    FIELD cperson   AS CHAR     FORMAT "x(24)"  COLUMN-LABEL "Contact Person" /*ITA 240314*/
    FIELD tevent    AS CHAR     FORMAT "x(18)"  COLUMN-LABEL "Event"  /*ITA 240314*/
    FIELD venue     AS CHAR     FORMAT "x(12)"  COLUMN-LABEL "Venue"  /*ITA 240314*/
    FIELD pax       AS CHAR     FORMAT "x(5)"   COLUMN-LABEL "Pax"   /*ITA 240314*/
    FIELD reason    AS CHAR     FORMAT "x(62)"  COLUMN-LABEL "Reason"    
    FIELD id        AS CHAR     FORMAT "x(3)"   COLUMN-LABEL "ID" /* geral 29/11/2019 */
    FIELD room-rev  AS CHAR     FORMAT "x(19)"  COLUMN-LABEL "Room Revenue"
    FIELD fb-rev    AS CHAR     FORMAT "x(15)"  COLUMN-LABEL "F&B Revenue"
    FIELD other-rev AS CHAR     FORMAT "x(15)"  COLUMN-LABEL "Other Revenue"
    FIELD tot-rev   AS CHAR     FORMAT "x(19)"  COLUMN-LABEL "Total Revenue"
    FIELD f-empty   AS CHAR     FORMAT "x(1)"   COLUMN-LABEL ""
.

DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER curr-select1   AS INT.
DEF OUTPUT PARAMETER TABLE FOR output-list.
DEF OUTPUT PARAMETER TABLE FOR t-out.

RUN journal-list.

PROCEDURE journal-list: 
  DEFINE VARIABLE other-revenue AS DECIMAL FORMAT "->>>,>>>,>>9.99".
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  FOR EACH t-out: 
    DELETE t-out. 
  END. 
  FOR EACH b-storno WHERE b-storno.datum GE from-date AND b-storno.datum LE to-date AND 
    b-storno.grund[18] NE "" NO-LOCK, 
    FIRST bk-func WHERE bk-func.veran-nr = b-storno.bankettnr NO-LOCK,
    FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK,
    FIRST guest WHERE guest.gastnr = b-storno.gastnr NO-LOCK:
    IF AVAILABLE bk-veran THEN
    DO:
        other-revenue = 0.
        curr-select1 = int(b-storno.bankettnr).
        FOR EACH bk-rart WHERE bk-rart.veran-nr = bk-func.veran-nr AND
                bk-rart.veran-seite = bk-func.veran-seite NO-LOCK:
                other-revenue = other-revenue + (bk-rart.preis * anzahl).
        END.
    END.
    IF AVAILABLE guest THEN 
    DO:
        CREATE output-list. 
        STR = STRING(bk-veran.kontaktfirst,"99/99/99")+
              STRING(b-storno.datum,"99/99/99") + 
              STRING(b-storno.bankettnr,">>>>>>>>") + 
              STRING(b-storno.breslinnr,">>>") + 
              STRING(guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma,"x(32)") + 
              STRING(b-storno.grund[18],"x(62)") + 
              STRING(b-storno.usercode,"x(3)") /* geral 29/11/2019*/ + 
              STRING(bk-func.rpreis[1], "->>>,>>>,>>>,>>9.99") + 
              STRING((bk-func.rpreis[7] * bk-func.rpersonen[1]), "->>>,>>>,>>9.99") +
              STRING(other-revenue, "->>>,>>>,>>9.99") + 
              STRING((bk-func.rpreis[1] + (bk-func.rpreis[7] * bk-func.rpersonen[1]) + other-revenue), "->>>,>>>,>>>,>>9.99")
            .
        /*ITA 240314*/
          ASSIGN 
              output-list.pax       = STRING(bk-func.personen, ">,>>>")
              output-list.venue     = STRING(bk-func.raeume[1],"x(12)")
              output-list.cperson   = STRING(bk-func.v-kontaktperson[1],"x(32)")
              output-list.tevent    = STRING(bk-func.zweck[1],"x(18)")
          .
    END.     
  END. 
  FOR EACH output-list:
    CREATE t-out.
    ASSIGN
        t-out.rsv-date  = SUBSTRING(STR,1,8)
        t-out.b-date    = SUBSTRING(STR,9,8)
        t-out.rsv-no    = SUBSTRING(STR,17,8)
        t-out.resline   = SUBSTRING(STR,25,3)
        t-out.engager   = SUBSTRING(STR,28,32)
        t-out.reason    = SUBSTRING(STR,60,62)
        /* geral 29/11/2019*/
        t-out.id        = SUBSTRING(STR,122,3) 
        t-out.room-rev  = SUBSTRING(str,125,19)
        t-out.fb-rev    = SUBSTRING(str,144,15)  
        t-out.other-rev = SUBSTRING(str,159,15) 
        t-out.tot-rev   = SUBSTRING(str,174,19)
        t-out.pax       = output-list.pax
        t-out.venue     = output-list.venue
        t-out.cperson   = output-list.cperson

    .
  END.
END. 
