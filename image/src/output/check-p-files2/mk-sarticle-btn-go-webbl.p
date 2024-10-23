DEFINE TEMP-TABLE l-art 
    FIELD artnr        AS INT  
    FIELD zwkum        AS INT
    FIELD endkum       AS INT
    FIELD bezeich      AS char
    FIELD jahrgang     AS INT
    FIELD min-bestand  AS DECIMAL
    FIELD lieferfrist  AS INT
    FIELD inhalt       AS DEC
    FIELD lief-einheit AS DEC
    FIELD masseinheit  AS char
    FIELD herkunft     AS char
    FIELD erfass-art   AS LOGICAL
    FIELD bestellt     AS LOGICAL
    FIELD fibukonto    AS char
    FIELD alkoholgrad  AS DECIMAL
    FIELD traubensorte AS char
    FIELD lief-nr1     AS INT
    FIELD lief-nr2     AS INT
    FIELD lief-nr3     AS INT
    FIELD letz-eingang AS date
    FIELD letz-ausgang AS date
    FIELD anzverbrauch AS DECIMAL
    FIELD ek-aktuell   AS DECIMAL
    FIELD ek-letzter   AS DECIMAL
    FIELD wert-verbrau AS DECIMAL
    FIELD vk-preis     AS DECIMAL
    FIELD lief-artnr   AS CHAR EXTENT 3
    FIELD betriebsnr   AS INT
    .

DEFINE TEMP-TABLE tt-artnr
    FIELD curr-i   AS INTEGER
    FIELD ss-artnr AS INTEGER
.
DEFINE TEMP-TABLE tt-content
    FIELD curr-i     AS INTEGER
    FIELD ss-content AS INTEGER
.

DEFINE INPUT PARAMETER pvILanguage  AS INT      NO-UNDO.
DEFINE INPUT PARAMETER artnr        AS INT      NO-UNDO.
DEFINE INPUT PARAMETER dml-art      AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER bez-aend     AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER s-unit       AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER zwkum        AS INT      NO-UNDO.
DEFINE INPUT PARAMETER endkum       AS INT      NO-UNDO.
DEFINE INPUT PARAMETER bezeich      AS char     NO-UNDO.
DEFINE INPUT PARAMETER jahrgang     AS INT      NO-UNDO.
DEFINE INPUT PARAMETER min-bestand  AS DECIMAL  NO-UNDO.
DEFINE INPUT PARAMETER lieferfrist  AS INT      NO-UNDO.
DEFINE INPUT PARAMETER inhalt       AS DECIMAL  NO-UNDO.
DEFINE INPUT PARAMETER lief-einheit AS DECIMAL  NO-UNDO.
DEFINE INPUT PARAMETER masseinheit  AS char     NO-UNDO.
DEFINE INPUT PARAMETER herkunft     AS char     NO-UNDO.
DEFINE INPUT PARAMETER erfass-art   AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER bestellt     AS LOGICAL  NO-UNDO. 
DEFINE INPUT PARAMETER fibukonto    AS char     NO-UNDO.
DEFINE INPUT PARAMETER alkoholgrad  AS DECIMAL  NO-UNDO.
DEFINE INPUT PARAMETER traubensorte AS char     NO-UNDO.
DEFINE INPUT PARAMETER lief-nr1     AS INT      NO-UNDO.
DEFINE INPUT PARAMETER lief-nr2     AS INT      NO-UNDO.
DEFINE INPUT PARAMETER lief-nr3     AS INT      NO-UNDO.
DEFINE INPUT PARAMETER letz-eingang AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER letz-ausgang AS date     NO-UNDO.
DEFINE INPUT PARAMETER anzverbrauch AS DEC      NO-UNDO.
DEFINE INPUT PARAMETER ek-aktuell   AS DEC      NO-UNDO.
DEFINE INPUT PARAMETER ek-letzter   AS DEC      NO-UNDO.
DEFINE INPUT PARAMETER wert-verbrau AS DEC      NO-UNDO.
DEFINE INPUT PARAMETER vk-preis     AS DEC      NO-UNDO.
DEFINE INPUT PARAMETER lief-artnr1  AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER lief-artnr2  AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER lief-artnr3  AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER betriebsnr   AS INT      NO-UNDO.

DEFINE INPUT PARAMETER tartnr-curr-i1 AS INT NO-UNDO.
DEFINE INPUT PARAMETER tartnr-curr-i2 AS INT NO-UNDO.
DEFINE INPUT PARAMETER tartnr-curr-i3 AS INT NO-UNDO.
DEFINE INPUT PARAMETER sartnr1 AS INT NO-UNDO.
DEFINE INPUT PARAMETER sartnr2 AS INT NO-UNDO.
DEFINE INPUT PARAMETER sartnr3 AS INT NO-UNDO.

DEFINE INPUT PARAMETER tcontent-curr-i1 AS INT NO-UNDO.
DEFINE INPUT PARAMETER tcontent-curr-i2 AS INT NO-UNDO.
DEFINE INPUT PARAMETER tcontent-curr-i3 AS INT NO-UNDO.
DEFINE INPUT PARAMETER scontent1 AS INT NO-UNDO.
DEFINE INPUT PARAMETER scontent2 AS INT NO-UNDO.
DEFINE INPUT PARAMETER scontent3 AS INT NO-UNDO.

DEFINE OUTPUT PARAMETER sss-artnr   AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER sss-cont    AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER str-msg     AS CHAR     NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER created     AS LOGICAL  NO-UNDO INIT NO.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "mk-sarticle". 

DEFINE VAR ss-artnr     AS INT      NO-UNDO EXTENT 3.
DEFINE VAR ss-content   AS INT      NO-UNDO EXTENT 3.

CREATE l-art.
ASSIGN                  
    l-art.artnr         = artnr
    l-art.zwkum         = zwkum       
    l-art.endkum        = endkum      
    l-art.bezeich       = bezeich     
    l-art.jahrgang      = jahrgang    
    l-art.min-bestand   = min-bestand 
    l-art.lieferfrist   = lieferfrist 
    l-art.inhalt        = inhalt      
    l-art.lief-einheit  = lief-einheit
    l-art.masseinheit   = masseinheit 
    l-art.herkunft      = herkunft    
    l-art.erfass-art    = erfass-art  
    l-art.bestellt      = bestellt    
    l-art.fibukonto     = fibukonto   
    l-art.alkoholgrad   = alkoholgrad 
    l-art.traubensorte  = traubensorte
    l-art.lief-nr1      = lief-nr1    
    l-art.lief-nr2      = lief-nr2    
    l-art.lief-nr3      = lief-nr3    
    l-art.letz-eingang  = letz-eingang
    l-art.letz-ausgang  = letz-ausgang
    l-art.anzverbrauch  = anzverbrauch
    l-art.ek-aktuell    = ek-aktuell  
    l-art.ek-letzter    = ek-letzter  
    l-art.wert-verbrau  = wert-verbrau
    l-art.vk-preis      = vk-preis    
    l-art.lief-artnr[1] = lief-artnr1 
    l-art.lief-artnr[2] = lief-artnr2 
    l-art.lief-artnr[3] = lief-artnr3 
    l-art.betriebsnr    = betriebsnr.

CREATE tt-artnr.
ASSIGN 
    tt-artnr.curr-i   = tartnr-curr-i1
    tt-artnr.ss-artnr = sartnr1.
CREATE tt-artnr.
ASSIGN 
    tt-artnr.curr-i   = tartnr-curr-i2
    tt-artnr.ss-artnr = sartnr2.
CREATE tt-artnr.
ASSIGN 
    tt-artnr.curr-i   = tartnr-curr-i3
    tt-artnr.ss-artnr = sartnr3.

CREATE tt-content.
ASSIGN 
    tt-content.curr-i     = tcontent-curr-i1 
    tt-content.ss-content = scontent1.        
CREATE tt-content.
ASSIGN 
    tt-content.curr-i     = tcontent-curr-i2 
    tt-content.ss-content = scontent2. 
CREATE tt-content.
ASSIGN 
    tt-content.curr-i     = tcontent-curr-i3 
    tt-content.ss-content = scontent3. 


RUN mk-sarticle-btn-gobl.p (pvILanguage, TABLE tt-artnr, TABLE tt-content, 
                            artnr, dml-art, fibukonto, bez-aend, s-unit, INPUT TABLE l-art,
                            OUTPUT sss-artnr, OUTPUT sss-cont,OUTPUT str-msg, OUTPUT created).
