
DEFINE TEMP-TABLE t-kontline2   LIKE kontline.
DEFINE TEMP-TABLE t-counters    LIKE counters.

DEFINE INPUT PARAMETER curr-mode    AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER gastnr       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER zikatnr1     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER argt         AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER comments     AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER kontcode     AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER ankunft      AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER abreise      AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER zikatnr      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER zimmeranz    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER erwachs      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER kind1        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER overbooking  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER ruecktage    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER rueckdatum   AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER kontignr     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER ansprech     AS CHAR    NO-UNDO.


DEFINE OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO.
  
  FOR EACH t-kontline2:
      DELETE t-kontline2.
  END.

  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.

  IF curr-mode = "new" THEN 
  DO: 
    RUN next-counterbl.p(10, OUTPUT TABLE t-counters).
    FIND FIRST t-counters.
    CREATE t-kontline2.
    ASSIGN
        t-kontline2.kontcode        = kontcode
        t-kontline2.ankunft         = ankunft 
        t-kontline2.abreise         = abreise 
        t-kontline2.zikatnr         = zikatnr 
        t-kontline2.arrangement     = argt 
        t-kontline2.zimmeranz       = zimmeranz 
        t-kontline2.erwachs         = erwachs 
        t-kontline2.kind1           = kind1 
        t-kontline2.overbooking     = overbooking 
        t-kontline2.ruecktage       = ruecktage 
        t-kontline2.rueckdatum      = rueckdatum 
        t-kontline2.kontignr        = t-counters.counter
        t-kontline2.bemerk          = comments
        t-kontline2.gastnr          = gastnr
        t-kontline2.useridanlage    = ""
        t-kontline2.ansprech        = ansprech.
  END. 
  IF curr-mode = "chg" THEN
  DO: 
      CREATE t-kontline2.
      ASSIGN
      t-kontline2.kontcode        = kontcode
      t-kontline2.ankunft         = ankunft 
      t-kontline2.abreise         = abreise 
      t-kontline2.zikatnr         = zikatnr 
      t-kontline2.arrangement     = argt 
      t-kontline2.zimmeranz       = zimmeranz 
      t-kontline2.erwachs         = erwachs 
      t-kontline2.kind1           = kind1 
      t-kontline2.overbooking     = overbooking 
      t-kontline2.ruecktage       = ruecktage 
      t-kontline2.rueckdatum      = rueckdatum 
      t-kontline2.kontignr        = kontignr
      t-kontline2.arrangement     = argt
      t-kontline2.bemerk          = comments
      t-kontline2.gastnr          = gastnr
      t-kontline2.bediener-nr     = bediener.nr
      t-kontline2.ansprech        = ansprech.
  END.
  ASSIGN t-kontline2.zikatnr = zikatnr1. 
  IF curr-mode = "new" THEN t-kontline2.bediener-nr = bediener.nr. 
  IF curr-mode = "chg" THEN t-kontline2.useridanlage = bediener.userinit. 
  
  IF curr-mode = "new" THEN
  RUN write-kontlinebl.p(2, INPUT TABLE t-kontline2, OUTPUT success-flag).

  ELSE IF curr-mode = "chg" THEN 
  RUN write-kontlinebl.p(1, INPUT TABLE t-kontline2, OUTPUT success-flag).
