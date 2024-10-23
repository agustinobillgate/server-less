DEFINE TEMP-TABLE disc-list
    FIELD h-artnr       AS INTEGER
    FIELD bezeich       AS CHAR
    FIELD artnr         AS INTEGER
    FIELD mwst          AS INTEGER
    FIELD service       AS INTEGER
    FIELD umsatzart     AS INTEGER INITIAL 0 
    FIELD defaultFlag   AS LOGICAL INITIAL NO
    FIELD amount        AS DECIMAL INITIAL 0
    FIELD netto-amt     AS DECIMAL INITIAL 0
    FIELD service-amt   AS DECIMAL INITIAL 0
    FIELD mwst-amt      AS DECIMAL INITIAL 0
.

DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER disc-value AS DECIMAL.
DEF INPUT PARAMETER procent AS DECIMAL.
DEF INPUT PARAMETER b-billart AS INT.
DEF INPUT PARAMETER b2-billart AS INT.

DEF OUTPUT PARAMETER billart AS INT.
DEF OUTPUT PARAMETER description AS CHAR.
DEF OUTPUT PARAMETER b-artnrfront AS INT.
DEF OUTPUT PARAMETER o-artnrfront AS INT.
DEF OUTPUT PARAMETER TABLE FOR disc-list.

DEFINE VARIABLE b2-artnrfront AS INTEGER. 
DEFINE VARIABLE b2-vcode      AS INTEGER.
DEFINE VARIABLE b-vcode       AS INTEGER.
DEFINE VARIABLE disc-descript AS CHAR. 
DEFINE VARIABLE o-billart     AS INTEGER NO-UNDO. 

RUN get-article.
RUN create-discList.

PROCEDURE get-article: 
DEFINE VARIABLE voucher-art AS INTEGER INITIAL 0. 

  IF disc-value NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE paramnr = 1001 NO-LOCK. 
    voucher-art = htparam.finteger. 
     FIND FIRST h-artikel WHERE h-artikel.artnr = finteger 
      AND h-artikel.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN 
    DO: 
      billart = h-artikel.artnr. 
      description = vhp.h-artikel.bezeich + " " + STRING(disc-value). 
      disc-descript = DESCRIPTION.
    END. 
  END. 
  IF voucher-art NE 0 THEN RETURN. 
  
  FIND FIRST vhp.htparam WHERE paramnr = 557 no-lock. /*rest artnr 4 disc*/ 
  IF finteger NE 0 THEN 
  DO: 
    FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = finteger 
      AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.h-artikel THEN 
    DO: 
      billart = vhp.h-artikel.artnr. 
      IF disc-value = 0 THEN 
      DO:
        IF (procent NE INTEGER(procent)) THEN description = vhp.h-artikel.bezeich 
          + " " + TRIM(STRING(procent,"->>9.99")) + "%". 
        ELSE description = vhp.h-artikel.bezeich + " " 
          + TRIM(STRING(procent,"->>9")) + "%". 
      END.
      ELSE description = vhp.h-artikel.bezeich. 
    END. 
  END. 
  
  FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. 
  IF finteger NE 0 THEN 
  DO: 
    FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = finteger 
      AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.h-artikel THEN 
    ASSIGN
      b-billart    = vhp.h-artikel.artnr 
      b-artnrfront = vhp.h-artikel.artnrfront 
      b-vcode      = vhp.h-artikel.mwst-code
    .
  END. 

  FIND FIRST vhp.htparam WHERE paramnr = 1009 NO-LOCK. 
  IF vhp.htparam.finteger NE 0 THEN 
  DO: 
    FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = finteger 
      AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.h-artikel THEN  
    ASSIGN
      b2-billart    = vhp.h-artikel.artnr
      b2-artnrfront = vhp.h-artikel.artnrfront
      b2-vcode      = vhp.h-artikel.mwst-code
    . 
  END. 

  FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK. 
  IF finteger NE 0 THEN 
  DO: 
    FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = finteger 
      AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.h-artikel THEN 
    DO: 
      o-billart = vhp.h-artikel.artnr. 
      o-artnrfront = vhp.h-artikel.artnrfront. 
    END. 
  END. 
END. 

PROCEDURE create-discList:
DEF VAR zwkum AS INTEGER NO-UNDO.
  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = billart 
      AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR.
  IF NOT AVAILABLE vhp.h-artikel THEN RETURN.
  FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront
      AND vhp.artikel.departement = dept NO-LOCK.
  zwkum = vhp.artikel.zwkum.
  CREATE disc-list.
  ASSIGN
      disc-list.h-artnr     = billart
      disc-list.bezeich     = vhp.h-artikel.bezeich
      disc-list.artnr       = vhp.h-artikel.artnrfront
      disc-list.mwst        = vhp.h-artikel.mwst
      disc-list.service     = vhp.h-artikel.service
      disc-list.umsatzart   = vhp.artikel.umsatzart
      disc-list.defaultFlag = YES
  . 

  IF disc-value NE 0 THEN
    disc-list.bezeich = disc-list.bezeich + " " + STRING(disc-value).
  ELSE
  DO:
    IF (procent NE INTEGER(procent)) THEN disc-list.bezeich = disc-list.bezeich 
      + " " + TRIM(STRING(procent,"->>9.99")) + "%". 
    ELSE disc-list.bezeich = disc-list.bezeich + " " + TRIM(STRING(procent,"->>9")) + "%". 
  END.

  IF b-billart NE 0 THEN
  DO:
      FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = b-billart 
          AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR.
      FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront
          AND vhp.artikel.departement = dept NO-LOCK.
      CREATE disc-list.
      ASSIGN
          disc-list.h-artnr     = vhp.h-artikel.artnr
          disc-list.bezeich     = vhp.h-artikel.bezeich
          disc-list.artnr       = vhp.h-artikel.artnrfront
          disc-list.mwst        = vhp.h-artikel.mwst
          disc-list.service     = vhp.h-artikel.service
          disc-list.umsatzart   = vhp.artikel.umsatzart
          disc-list.defaultFlag = YES
      .
      IF disc-value NE 0 THEN
        disc-list.bezeich = disc-list.bezeich + " " + STRING(disc-value).
      ELSE
      DO:
        IF (procent NE INTEGER(procent)) THEN disc-list.bezeich = disc-list.bezeich 
          + " " + TRIM(STRING(procent,"->>9.99")) + "%". 
        ELSE disc-list.bezeich = disc-list.bezeich + " " + TRIM(STRING(procent,"->>9")) + "%". 
      END.
  END.

  IF b2-billart NE 0 THEN
  DO:
      FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = b2-billart 
          AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR.
      FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront
          AND vhp.artikel.departement = dept NO-LOCK.
      CREATE disc-list.
      ASSIGN
          disc-list.h-artnr     = vhp.h-artikel.artnr
          disc-list.bezeich     = vhp.h-artikel.bezeich
          disc-list.artnr       = vhp.h-artikel.artnrfront
          disc-list.mwst        = vhp.h-artikel.mwst
          disc-list.service     = vhp.h-artikel.service
          disc-list.umsatzart   = vhp.artikel.umsatzart
          disc-list.defaultFlag = YES
      .
      IF disc-value NE 0 THEN
        disc-list.bezeich = disc-list.bezeich + " " + STRING(disc-value).
      ELSE
      DO:
        IF (procent NE INTEGER(procent)) THEN disc-list.bezeich = disc-list.bezeich 
          + " " + TRIM(STRING(procent,"->>9.99")) + "%". 
        ELSE disc-list.bezeich = disc-list.bezeich + " " + TRIM(STRING(procent,"->>9")) + "%". 
      END.
  END.

  IF o-billart NE 0 THEN
  DO:
      FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = o-billart 
          AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR.
      FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront
          AND vhp.artikel.departement = dept NO-LOCK.
      CREATE disc-list.
      ASSIGN
          disc-list.h-artnr     = vhp.h-artikel.artnr
          disc-list.bezeich     = vhp.h-artikel.bezeich
          disc-list.artnr       = vhp.h-artikel.artnrfront
          disc-list.mwst        = vhp.h-artikel.mwst
          disc-list.service     = vhp.h-artikel.service
          disc-list.umsatzart   = vhp.artikel.umsatzart
          disc-list.defaultFlag = YES
      .
      IF disc-value NE 0 THEN
        disc-list.bezeich = disc-list.bezeich + " " + STRING(disc-value).
      ELSE
      DO:
        IF (procent NE INTEGER(procent)) THEN disc-list.bezeich = disc-list.bezeich 
          + " " + TRIM(STRING(procent,"->>9.99")) + "%". 
        ELSE disc-list.bezeich = disc-list.bezeich + " " + TRIM(STRING(procent,"->>9")) + "%". 
      END.
  END.

  FOR EACH vhp.artikel WHERE vhp.artikel.departement = dept
      AND vhp.artikel.zwkum = zwkum NO-LOCK:
      FIND FIRST disc-list WHERE disc-list.artnr = vhp.artikel.artnr NO-ERROR.
      IF NOT AVAILABLE disc-list THEN
      DO:
        FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnrfront = vhp.artikel.artnr 
            AND vhp.h-artikel.departement = dept NO-LOCK NO-ERROR.
        IF AVAILABLE vhp.h-artikel THEN
        DO:
            CREATE disc-list.
            ASSIGN
                disc-list.h-artnr     = vhp.h-artikel.artnr
                disc-list.bezeich     = vhp.h-artikel.bezeich
                disc-list.artnr       = vhp.h-artikel.artnrfront
                disc-list.mwst        = vhp.h-artikel.mwst
                disc-list.service     = vhp.h-artikel.service
                disc-list.umsatzart   = vhp.artikel.umsatzart
                disc-list.defaultFlag = NO
            .
            IF disc-value NE 0 THEN
              disc-list.bezeich = disc-list.bezeich + " " + STRING(disc-value).
            ELSE
            DO:
              IF (procent NE INTEGER(procent)) THEN disc-list.bezeich = disc-list.bezeich 
                + " " + TRIM(STRING(procent,"->>9.99")) + "%". 
              ELSE disc-list.bezeich = disc-list.bezeich + " " + TRIM(STRING(procent,"->>9")) + "%". 
            END.
        END.
      END.
  END.

END.
