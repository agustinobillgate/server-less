DEFINE TEMP-TABLE outlist 
  FIELD resnr AS INTEGER 
  FIELD name AS CHAR FORMAT "x(30)" COLUMN-LABEL "Travel Agents" 
  FIELD mnite AS INTEGER FORMAT ">>,>>9" COLUMN-LABEL "MTD RmNite" 
  FIELD pmnite AS INTEGER FORMAT ">>9.9" COLUMN-LABEL "(%)" 
  FIELD ynite AS INTEGER FORMAT ">>,>>9" COLUMN-LABEL "YTD RmNite" 
  FIELD pynite AS INTEGER FORMAT ">>9.9" COLUMN-LABEL "(%)" 
  FIELD mtu AS DECIMAL FORMAT ">>,>>>,>>>,>>9" COLUMN-LABEL "MTD Expect Rev" 
  FIELD pmtu AS INTEGER FORMAT ">>9.9" COLUMN-LABEL "(%)" 
  FIELD ytu AS DECIMAL FORMAT ">>>,>>>,>>>,>>9" COLUMN-LABEL "YTD Expect Rev" 
  FIELD pytu AS INTEGER FORMAT ">>9.9" COLUMN-LABEL "(%)" 
  FIELD wohnort AS CHAR FORMAT "x(36)" COLUMN-LABEL "City - Land"
. 

DEFINE INPUT PARAMETER fdate        AS DATE.
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE INPUT PARAMETER fname        AS CHAR.
DEFINE INPUT PARAMETER tname        AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR outlist.

DEFINE VARIABLE t-mnite             AS INTEGER FORMAT ">>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-ynite             AS INTEGER FORMAT ">>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-mtu               AS DECIMAL FORMAT ">>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-ytu               AS DECIMAL FORMAT " >>>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE gastnr              AS INTEGER INITIAL 0. 
DEFINE VARIABLE rmnite              AS INTEGER. 
DEFINE VARIABLE bdate               AS DATE. 
DEFINE VARIABLE tmpInt              AS INTEGER INITIAL 0 NO-UNDO. /*FT serverless*/
 
  bdate = DATE(1, 1, year(fdate)). 
  t-mnite = 0. 
  t-mtu = 0. 
  t-ynite = 0. 
  t-ytu = 0. 
  IF sorttype = 1 THEN 
  FOR EACH res-line WHERE res-line.active-flag = 2 
    AND res-line.resstatus = 10 AND res-line.ankunft GE bdate 
    AND res-line.ankunft LE fdate 
    AND res-line.resname GE fname AND res-line.resname LE tname 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = res-line.gastnr 
    AND guest.karteityp = 2 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
    BY res-line.resname BY res-line.ankunft BY res-line.name: 
    FIND FIRST outlist WHERE outlist.resnr = res-line.resnr NO-ERROR. 
    IF NOT AVAILABLE outlist THEN 
    DO: 
      create outlist. 
      outlist.resnr = res-line.resnr. 
      outlist.name = guest.name + ", " + guest.anredefirma. 
      outlist.wohnort = guest.wohnort + " " + STRING(guest.plz) 
        + " - " + guest.land. 
      gastnr = res-line.gastnr. 
    END.
    ASSIGN
      tmpInt = res-line.abreise - res-line.ankunft
      rmnite =  tmpInt * res-line.zimmeranz. 
    IF month(res-line.ankunft) = month(fdate) THEN 
    DO: 
      outlist.mnite = outlist.mnite + rmnite. 
      outlist.mtu = outlist.mtu + rmnite * res-line.zipreis. 
      t-mnite = t-mnite + rmnite. 
      t-mtu = t-mtu + rmnite * res-line.zipreis. 
    END. 
    outlist.ynite = outlist.ynite + rmnite. 
    outlist.ytu = outlist.ytu + rmnite * res-line.zipreis. 
    t-ynite = t-ynite + rmnite. 
    t-ytu = t-ytu + rmnite * res-line.zipreis. 
  END. 
  ELSE 
  FOR EACH res-line WHERE res-line.active-flag = 2 
    AND res-line.resstatus = 10 AND res-line.ankunft GE bdate 
    AND res-line.ankunft LE fdate 
    AND res-line.resname GE fname AND res-line.resname LE tname 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = res-line.gastnr 
    AND guest.karteityp = 1 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
    BY res-line.resname BY res-line.ankunft BY res-line.name: 
    FIND FIRST outlist WHERE outlist.resnr = res-line.resnr NO-ERROR. 
    IF NOT AVAILABLE outlist THEN 
    DO: 
      create outlist. 
      outlist.resnr = res-line.resnr. 
      outlist.name = guest.name + ", " + guest.anredefirma. 
      outlist.wohnort = guest.wohnort + " " + STRING(guest.plz) 
        + " - " + guest.land. 
      gastnr = res-line.gastnr. 
    END. 
    ASSIGN
      tmpInt = res-line.abreise - res-line.ankunft
      rmnite = tmpInt * res-line.zimmeranz. 
    IF month(res-line.ankunft) = month(fdate) THEN 
    DO: 
      outlist.mnite = outlist.mnite + rmnite. 
      outlist.mtu = outlist.mtu + rmnite * res-line.zipreis. 
      t-mnite = t-mnite + rmnite. 
      t-mtu = t-mtu + rmnite * res-line.zipreis. 
    END. 
    outlist.ynite = outlist.ynite + rmnite. 
    outlist.ytu = outlist.ytu + rmnite * res-line.zipreis. 
    t-ynite = t-ynite + rmnite. 
    t-ytu = t-ytu + rmnite * res-line.zipreis. 
  END. 
 
  FOR EACH outlist: 
    IF t-mnite NE 0 THEN 
    DO: 
      outlist.pmnite = outlist.mnite / t-mnite * 100. 
      IF t-mtu NE 0 THEN
        outlist.pmtu = outlist.mtu / t-mtu * 100. 
    END. 
    IF t-ynite NE 0 THEN 
    DO: 
      outlist.pynite = outlist.ynite / t-ynite * 100. 
      IF t-ytu NE 0 THEN
        outlist.pytu = outlist.ytu / t-ytu * 100. 
    END. 
  END. 
