DEFINE TEMP-TABLE earlycog-list 
  FIELD datum       AS DATE LABEL "Date" 
  FIELD zinr        LIKE zimmer.zinr LABEL "RmNo" 
  FIELD resname     AS CHAR FORMAT "x(24)" LABEL "Reservation Name"
  FIELD name        AS CHAR FORMAT "x(30)" LABEL "Guest Name" 
  FIELD zimmeranz   AS INTEGER FORMAT ">>>" LABEL "Qty" 
  FIELD pax         AS INTEGER FORMAT ">>>" LABEL "Pax" 
  FIELD ankunft     AS DATE LABEL "Arrival" 
  FIELD abreise     AS DATE LABEL "Departure" 
  FIELD origdate    AS DATE LABEL "OrigDate"
  FIELD zipreis     AS CHAR FORMAT "x(13)" LABEL "    Room Rate" 
  FIELD curr        AS CHAR FORMAT "x(4)" LABEL "Curr" 
  FIELD reason      AS CHAR FORMAT "x(32)" LABEL "C/O Reason"
  FIELD country     AS CHAR FORMAT "x(3)" LABEL "Country"
  FIELD sex         AS CHAR FORMAT "x(1)"  LABEL "S"
  .

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR earlycog-list.

DEFINE WORKFILE cl-list 
  FIELD bezeich AS CHAR FORMAT "x(16)" 
  FIELD zimmeranz AS INTEGER 
  FIELD pax AS INTEGER. 

DEFINE VARIABLE datum   AS DATE. 
DEFINE VARIABLE t-anz   AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-pax   AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-anz AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-pax AS INTEGER INITIAL 0. 
DEFINE VARIABLE n       AS INTEGER.
DEFINE VARIABLE st      AS CHAR.
DEFINE VARIABLE long-digit AS LOGICAL. 

/*************************************************************************************************/
                                       
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FOR EACH earlycog-list: 
    DELETE earlycog-list. 
END. 
FOR EACH cl-list: 
    DELETE cl-list. 
END. 

DO datum = from-date TO to-date: 
    t-anz = 0. 
    t-pax = 0. 
    DO: 
        FOR EACH res-line WHERE res-line.active-flag = 2 
            AND res-line.resstatus EQ 8 
            AND res-line.abreise GE datum
            AND res-line.abreise LE datum 
            AND (res-line.abreise - res-line.ankunft) LT res-line.anztage
            NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK 
            BY res-line.abreise BY res-line.zinr: 

            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember USE-INDEX gastnr_index
                NO-LOCK NO-ERROR.

            CREATE earlycog-list. 
            ASSIGN 
                earlycog-list.datum      = datum 
                earlycog-list.zinr       = res-line.zinr 
                earlycog-list.name       = res-line.name 
                earlycog-list.resname    = reservation.NAME
                earlycog-list.zimmeranz  = res-line.zimmeranz 
                earlycog-list.pax        = res-line.erwachs + res-line.gratis 
                earlycog-list.ankunft    = res-line.ankunft 
                earlycog-list.abreise    = res-line.abreise 
                earlycog-list.origdate   = res-line.ankunft + res-line.anztage
                .

            IF AVAILABLE guest THEN
                ASSIGN
                earlycog-list.sex      = guest.geschlecht
                earlycog-list.country  = guest.land.
        
            IF res-line.zimmer-wunsch MATCHES ("*earlyCO*") THEN
                DO n = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    st = ENTRY(n, res-line.zimmer-wunsch,";").
                    IF SUBSTR(st,1,8) = "earlyCO," THEN
                        earlycog-list.reason = earlycog-list.reason + SUBSTR(st,9) + ";".
                END.

            IF long-digit THEN 
                earlycog-list.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
            ELSE earlycog-list.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 

            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN earlycog-list.curr = waehrung.wabkurz. 
            t-anz = t-anz + 1. 
            t-pax = t-pax + res-line.erwachs + res-line.gratis. 
        END. 

        IF t-anz NE 0 THEN 
        DO: 
            CREATE earlycog-list. 
            earlycog-list.name = "T O T A L". 
            earlycog-list.zimmeranz = t-anz. 
            earlycog-list.pax = t-pax. 
        END. 
    END.
END.