DEFINE TEMP-TABLE l-art LIKE l-artikel. 

DEFINE TEMP-TABLE tt-artnr
    FIELD curr-i   AS INTEGER
    FIELD ss-artnr AS INTEGER
.
DEFINE TEMP-TABLE tt-content
    FIELD curr-i     AS INTEGER
    FIELD ss-content AS INTEGER
.

DEFINE INPUT PARAMETER pvILanguage  AS INT      NO-UNDO.

DEFINE INPUT PARAMETER TABLE FOR tt-artnr.
DEFINE INPUT PARAMETER TABLE FOR tt-content.

DEFINE INPUT PARAMETER artnr        AS INT      NO-UNDO.
DEFINE INPUT PARAMETER dml-art      AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER fibukonto    AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER bez-aend     AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER s-unit       AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR l-art.
DEFINE OUTPUT PARAMETER sss-artnr   AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER sss-cont    AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER str-msg     AS CHAR     NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER created     AS LOGICAL  NO-UNDO INIT NO.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "mk-sarticle". 

DEFINE VAR ss-artnr     AS INT      NO-UNDO EXTENT 3.
DEFINE VAR ss-content   AS INT      NO-UNDO EXTENT 3.

DEF BUFFER l-art1 FOR l-artikel. 
FIND FIRST l-art NO-LOCK NO-ERROR.

FOR EACH tt-artnr:
    ss-artnr[tt-artnr.curr-i] = tt-artnr.ss-artnr.
END.
FOR EACH tt-content:
    ss-content[tt-content.curr-i] = tt-content.ss-content.
END.

IF ss-artnr[1] NE 0 THEN 
DO: 
    FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[1] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-art1 OR l-art1.betriebsnr GT 0 THEN
    DO:
        sss-artnr = YES.
        RETURN.
    END.       
    IF ss-content[1] = 0 THEN 
    DO:
        sss-cont = YES.
        RETURN.
    END.               
END. 
IF ss-artnr[2] NE 0 THEN 
DO: 
    FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[2] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-art1 OR l-art1.betriebsnr GT 0 THEN 
    DO:
        sss-artnr = YES.
        RETURN.
    END.       
    IF ss-content[2] = 0 THEN 
    DO:
        sss-cont = YES.
        RETURN.
    END.               
END. 

IF ss-artnr[3] NE 0 THEN 
DO: 
    FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[3] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-art1 OR l-art1.betriebsnr GT 0 THEN 
    DO:
        sss-artnr = YES.
        RETURN.
    END.       
    IF ss-content[3] = 0 THEN 
    DO:
        sss-cont = YES.
        RETURN.
    END.               
END. 

IF artnr = 0 OR l-art.zwkum = 0 OR l-art.endkum = 0 
    OR l-art.inhalt = 0 OR l-art.bezeich = "" THEN 
    str-msg = translateExtended ("Unfilled field(s) detected",lvCAREA,""). 
ELSE 
DO:
    FIND FIRST l-artikel WHERE l-artikel.artnr = artnr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-artikel THEN 
    DO: 
        str-msg = translateExtended ("Article Number ",lvCAREA,"") + STRING(artnr) 
                  + " - " + l-artikel.bezeich + CHR(10) + "already exists". 
        RETURN. 
    END. 
 
    IF l-art.zwkum GE 100 THEN 
    DO: 
        IF SUBSTR(STRING(artnr),2,3) NE STRING(l-art.zwkum,"999") 
            OR SUBSTR(STRING(artnr),1,1) NE STRING(l-art.endkum,"9") THEN 
        DO: 
            str-msg = translateExtended ("Article Number does not match to main group and/or subgroup.",lvCAREA,"").
            RETURN.
        END. 
    END. 
    ELSE 
    DO: 
        IF SUBSTR(STRING(artnr),2,2) NE STRING(l-art.zwkum,"99") 
            OR SUBSTR(STRING(artnr),1,1) NE STRING(l-art.endkum,"9") THEN 
        DO: 
            str-msg = translateExtended ("Article Number does not match to main group and/or subgroup.",lvCAREA,"").
            RETURN. 
        END. 
    END. 
 
    DO: 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-art.zwkum 
                NO-LOCK. 
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
                NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE gl-acct THEN 
                str-msg = "&W" + 
                          translateExtended ("Chart of Account not correctly defined.",
                                             lvCAREA,"").
        END. 
        RUN create-l-artikel. 
        created = YES. 
    END. 
END.


 
PROCEDURE create-l-artikel: 
  DO transaction: 
    CREATE l-artikel. 
    ASSIGN
      l-artikel.artnr = artnr
      l-artikel.fibukonto = fibukonto 
      l-artikel.bezeich = l-art.bezeich 
      l-artikel.zwkum = l-art.zwkum
      l-artikel.endkum = l-art.endkum 
      l-artikel.herkunft = l-art.herkunft + ";" + s-unit + ";" 
      l-artikel.masseinheit = l-art.masseinheit
      l-artikel.inhalt = l-art.inhalt
      l-artikel.traubensort = l-art.traubensort 
      l-artikel.lief-einheit = l-art.lief-einheit 
      l-artikel.min-bestand = l-art.min-bestand
      l-artikel.anzverbrauch = l-art.anzverbrauch 
      l-artikel.lief-nr1 = l-art.lief-nr1
      l-artikel.lief-artnr[1] = l-art.lief-artnr[1]
      l-artikel.lief-nr2 = l-art.lief-nr2
      l-artikel.lief-artnr[2] = l-art.lief-artnr[2]
      l-artikel.lief-nr3 = l-art.lief-nr3 
      l-artikel.lief-artnr[3] = l-art.lief-artnr[3]
      l-artikel.betriebsnr = l-art.betriebsnr
      l-artikel.ek-aktuell = l-art.ek-aktuell 
      l-artikel.ek-letzter = l-art.ek-letzter 
      l-artikel.vk-preis = l-art.vk-preis
      l-artikel.bestellt = dml-art
      l-artikel.jahrgang = l-art.jahrgang 
    .
    IF ss-artnr[1] NE 0 OR ss-artnr[2] NE 0 OR ss-artnr[3] NE 0 THEN 
    DO: 
        CREATE queasy. 
        ASSIGN 
            queasy.KEY = 20 
            queasy.number1 = artnr 
            queasy.deci1 = ss-artnr[1] 
            queasy.deci2 = ss-artnr[2] 
            queasy.deci3 = ss-artnr[3]
            queasy.char3 = STRING(ss-content[1],"999") + ";" 
                + STRING(ss-content[2],"999") + ";" 
                + STRING(ss-content[3],"999") + ";" 
            queasy.date3 = TODAY. 
        RELEASE queasy. 
    END. 
  end. /* transaction */ 
END. 
