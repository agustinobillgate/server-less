
DEFINE TEMP-TABLE output-list 
  FIELD resstatus AS CHAR COLUMN-LABEL "S" FORMAT "x(1)"
  FIELD compname  LIKE bk-func.veranstalteranschrift[1] COLUMN-LABEL "Company Name" FORMAT "x(40)"
  FIELD EVENT     LIKE bk-func.zweck[1] COLUMN-LABEL "Event" FORMAT "x(25)"
  FIELD pax       AS CHAR COLUMN-LABEL "Pax" FORMAT "x(7)"
  FIELD venue     LIKE bk-raum.raum COLUMN-LABEL "Venue" FORMAT "x(15)"
  FIELD booker    LIKE akt-kont.NAME FORMAT "x(25)" COLUMN-LABEL "Contat Person"
  FIELD DATE      LIKE bk-func.datum COLUMN-LABEL "Date of Event"
  .

DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER TABLE FOR output-list.

RUN event-list.

PROCEDURE event-list: 
DEFINE BUFFER gast FOR guest.
DEFINE VARIABLE resstatus AS CHARACTER.
DEF VAR str-len AS INT.

FOR EACH output-list:
    DELETE output-list.
END.
FOR EACH bk-func WHERE bk-func.bis-datum GE from-date 
    AND bk-func.bis-datum LE to-date AND bk-func.resstatus LE 3 NO-LOCK, 
    FIRST bk-veran WHERE bk-veran.veran-nr = bk-func.veran-nr NO-LOCK BY bk-func.bis-datum: 
    CREATE output-list.
     
        IF bk-func.resstatus EQ 1 THEN
            ASSIGN
            output-list.resstatus = "F".
        ELSE IF bk-func.resstatus EQ 2 THEN
            output-list.resstatus = "T".
        ELSE IF bk-func.resstatus EQ 3 THEN
            output-list.resstatus = "W".                                    
        output-list.compname  = bk-func.adurch.
        output-list.EVENT     = bk-func.zweck[1]. 
        output-list.pax       = string(bk-func.rpersonen[1]).
        output-list.venue     = bk-func.raeume[1]. 
        output-list.booker    = bk-func.v-kontaktperson[1] .
        output-list.DATE      = bk-func.datum .

  END.
END. 
