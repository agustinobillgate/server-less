DEFINE TEMP-TABLE s-rezlin 
  FIELD pos         AS INTEGER 
  FIELD artnr       LIKE l-artikel.artnr                 COLUMN-LABEL "     ArtNo" 
  FIELD bezeich     AS CHAR FORMAT "x(36)"               COLUMN-LABEL "Description" 
  FIELD s-unit      AS CHAR FORMAT "x(8)"                COLUMN-LABEL "R-Unit"
  FIELD masseinheit LIKE l-artikel.masseinheit           COLUMN-LABEL "Unit" 
  FIELD menge       LIKE h-rezlin.menge                  COLUMN-LABEL "Quantity" 
  FIELD cost        AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Cost" 
  FIELD vk-preis    AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Avrg Price" 
  FIELD inhalt      AS DECIMAL FORMAT ">>>,>>9.99"       COLUMN-LABEL "Content" 
  FIELD lostfact    LIKE h-rezlin.lostfact 
  FIELD recipe-flag AS LOGICAL INITIAL NO. 

DEFINE INPUT PARAMETER TABLE FOR s-rezlin.
DEFINE INPUT PARAMETER h-artnr    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER h-bezeich  AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER katbezeich AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER katnr      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER portion    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER cost-percent      AS DECIMAL NO-UNDO. /*bernatd FA7A78 2024*/
DEFINE INPUT PARAMETER poten-sell-price AS DECIMAL NO-UNDO. /*bernatd  FA7A78 2024*/

DEF OUTPUT PARAMETER r-recid    AS INTEGER INITIAL 0.
DEFINE VARIABLE curr-pos AS INTEGER INITIAL 0. 
DEFINE BUFFER b-rezept FOR h-rezept.

RUN create-new-recipe.

/*start bernatd FA7A78*/
CREATE queasy. /*bernatd 2024*/
ASSIGN
    queasy.KEY     = 252
    queasy.number1 = h-artnr
    queasy.date1   = TODAY
    queasy.deci1   = cost-percent
    queasy.deci2   = poten-sell-price.

FIND CURRENT queasy NO-LOCK.
/*end bernatd 2024*/

PROCEDURE create-new-recipe: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  create h-rezept. 
  r-recid = RECID(h-rezept). 
  h-rezept.artnrrezept = h-artnr. 
  h-rezept.bezeich = h-bezeich. 
  j = length(h-rezept.bezeich) + 1. 
  DO i = j TO 24: 
    h-rezept.bezeich = h-rezept.bezeich + " ". 
  END. 
  ASSIGN
    /*h-rezept.bezeich        = h-rezept.bezeich + katbezeich*/
    h-rezept.kategorie      = katnr 
    h-rezept.datumanlage    = TODAY 
    h-rezept.portion        = portion.

  /*ITA 300418*/
  FIND FIRST b-rezept NO-LOCK NO-ERROR.
  IF AVAILABLE b-rezept THEN DO:
      IF NUM-ENTRIES(b-rezept.bezeich, ";") GT 1 THEN 
          ASSIGN h-rezept.bezeich = h-rezept.bezeich + ";" + katbezeich.
      ELSE ASSIGN h-rezept.bezeich = h-rezept.bezeich + katbezeich.
  END.
  ELSE ASSIGN h-rezept.bezeich = h-rezept.bezeich + ";" + katbezeich.

  FIND CURRENT h-rezept NO-LOCK. 
  FOR EACH s-rezlin NO-LOCK: 
    create h-rezlin. 
    ASSIGN
      h-rezlin.artnrrezept  = h-artnr
      h-rezlin.artnrlager   = s-rezlin.artnr 
      h-rezlin.menge        = s-rezlin.menge
      h-rezlin.lostfact     = s-rezlin.lostfact 
      h-rezlin.recipe-flag  = s-rezlin.recipe-flag
    . 
    FIND CURRENT h-rezlin NO-LOCK. 
  END. 
  FOR EACH s-rezlin: 
    delete s-rezlin. 
  END. 
  curr-pos = 0. 
END. 
