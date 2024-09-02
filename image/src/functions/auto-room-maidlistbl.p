DEFINE TEMP-TABLE rmlist
    FIELD flag      AS INTEGER  FORMAT ">>>" 
    FIELD code      AS CHAR     FORMAT "x(3)"     COLUMN-LABEL "Loc"
    FIELD zinr      LIKE zimmer.zinr              COLUMN-LABEL "RmNo"
    FIELD credit    AS INTEGER  FORMAT ">>>"      COLUMN-LABEL "CP"
    FIELD floor     AS INTEGER  FORMAT ">>"       COLUMN-LABEL "FL"
    FIELD gname     AS CHAR     FORMAT "x(32)"    COLUMN-LABEL "Main Guest Name" 
    FIELD pic       AS CHAR     FORMAT "x(12)"    COLUMN-LABEL "Person in Charge"
    FIELD bemerk    AS CHAR     FORMAT "x(50)"    COLUMN-LABEL "Remarks"
    FIELD rstat     AS CHAR     FORMAT "x(20)"    COLUMN-LABEL "Room Status" 
    FIELD ankunft   AS DATE     FORMAT "99/99/99" COLUMN-LABEL "Arrival" 
    FIELD abreise   AS DATE     FORMAT "99/99/99" COLUMN-LABEL "Departure" 
    FIELD kbezeich  AS CHAR     FORMAT "x(12)"    COLUMN-LABEL "Description" 
    FIELD nation    AS CHAR     FORMAT "x(3)"     COLUMN-LABEL "Nat" 
    FIELD paxnr     AS INTEGER  FORMAT ">>>"      COLUMN-LABEL "No"
    .

DEFINE TEMP-TABLE temp-loc
    FIELD t-loc AS CHARACTER.

DEF INPUT PARAMETER loc-combo AS CHAR    NO-UNDO.
DEF INPUT PARAMETER stat1     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER stat2     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER stat3     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER stat4     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER fr-floor  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER to-floor  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER pax       AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR rmlist.

DEFINE VARIABLE credit      AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE resbemerk   AS CHAR NO-UNDO.
DEFINE VARIABLE count-i     AS INTEGER.

RUN create-rmlist.    
RUN create-browse.

PROCEDURE create-rmlist:
    RUN hk-rmboy-rmlist_1bl.p (loc-combo,
    stat1, stat2, stat3, stat4,fr-floor, to-floor, 
    OUTPUT credit, OUTPUT TABLE rmlist).
END.

PROCEDURE create-browse:
    DEFINE VARIABLE each-credit AS DECIMAL INITIAL 0 NO-UNDO.
    DEFINE VARIABLE n           AS INTEGER INITIAL 1 NO-UNDO.
    DEFINE VARIABLE pnt         AS DECIMAL INITIAL 0 NO-UNDO.
    each-credit = credit / pax. 
    DEFINE VARIABLE pers-str AS CHAR FORMAT "x(12)" NO-UNDO. 

    pers-str = "Person".

    FOR EACH rmlist WHERE rmlist.zinr NE '' 
        NO-LOCK BY rmlist.floor BY rmlist.zinr:
        pnt = pnt + rmlist.credit.
        IF (pnt GT each-credit) AND (n LT pax) THEN
        DO:
          n = n + 1.
          pnt = 0.
        END.
        ASSIGN 
            rmlist.pic   = pers-str  + " " + STRING(n, ">>9")
            rmlist.paxnr = n
        .

        resbemerk = rmlist.bemerk.
        resbemerk = REPLACE(resbemerk,CHR(10),"").
        resbemerk = REPLACE(resbemerk,CHR(13),"").
        resbemerk = REPLACE(resbemerk,"~n","").
        resbemerk = REPLACE(resbemerk,"\n","").
        resbemerk = REPLACE(resbemerk,"~r","").
        resbemerk = REPLACE(resbemerk,"~r~n","").
        resbemerk = REPLACE(resbemerk,"&nbsp;"," ").
        resbemerk = REPLACE(resbemerk,"</p>","</p></p>").
        resbemerk = REPLACE(resbemerk,"</p>",CHR(13)).
        resbemerk = REPLACE(resbemerk,"<BR>",CHR(13)).
        resbemerk = REPLACE(resbemerk,CHR(10) + CHR(13),"").

        IF LENGTH(resbemerk) LT 3 THEN resbemerk = REPLACE(resbemerk,CHR(32),"").
        IF LENGTH(resbemerk) LT 3 THEN resbemerk = "".
        IF LENGTH(resbemerk) EQ ? THEN resbemerk = "".

        DO count-i = 0 TO 31:
            IF resbemerk MATCHES CHR(count-i) THEN resbemerk = REPLACE(resbemerk,CHR(count-i),"").
        END.
        DO count-i = 127 TO 255:
            IF resbemerk MATCHES CHR(count-i) THEN resbemerk = REPLACE(resbemerk,CHR(count-i),"").
        END.
        rmlist.bemerk = resbemerk.
    END.
END.
