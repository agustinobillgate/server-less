DEFINE TEMP-TABLE rest-article-list
    FIELD dept-no           AS INTEGER
    FIELD dept-name         AS CHARACTER
    FIELD artnr             AS INTEGER
    FIELD art-desc          AS CHARACTER
    FIELD main-group        AS INTEGER
    FIELD sub-group         AS INTEGER
    FIELD main-group-desc   AS CHARACTER
    FIELD sub-group-desc    AS CHARACTER
    FIELD art-type          AS INTEGER
    FIELD price             AS DECIMAL
    FIELD cost%             AS DECIMAL
    FIELD fo-artnr          AS INTEGER
    FIELD foart-desc        AS CHARACTER
    FIELD recipe-no         AS INTEGER
    FIELD recipe-desc       AS CHARACTER
    FIELD kp-no             AS INTEGER
    FIELD kp-desc           AS CHARACTER
    FIELD active-art        AS LOGICAL
    .

DEFINE TEMP-TABLE rest-maingroup-list
    FIELD maingroup-no          AS INTEGER
    FIELD maingroup-desc        AS CHARACTER
    FIELD new-maingroup-no      AS INTEGER
    FIELD new-maingroup-desc    AS CHARACTER
    FIELD fibukonto             AS CHARACTER
    FIELD betriebsnr            AS INTEGER
    .

DEFINE TEMP-TABLE rest-subgroup-list
    FIELD dept-no               AS INTEGER
    FIELD dept-name             AS CHARACTER
    FIELD subgroup-no           AS INTEGER
    FIELD subgroup-desc         AS CHARACTER
    FIELD subgroup-prior        AS INTEGER
    FIELD subgroup-bgcol        AS INTEGER
    FIELD new-subgroup-no       AS INTEGER
    FIELD new-subgroup-desc     AS CHARACTER
    FIELD fibukonto             AS CHARACTER
    FIELD betriebsnr            AS INTEGER
    .

DEFINE INPUT PARAMETER TABLE FOR rest-article-list.
DEFINE INPUT PARAMETER TABLE FOR rest-maingroup-list.
DEFINE INPUT PARAMETER TABLE FOR rest-subgroup-list.
DEFINE OUTPUT PARAMETER artnr     AS INTEGER.
DEFINE OUTPUT PARAMETER dept      AS CHARACTER.
DEFINE OUTPUT PARAMETER art-desc1 AS CHARACTER.
DEFINE OUTPUT PARAMETER art-desc2 AS CHARACTER.
DEFINE OUTPUT PARAMETER maingroup AS INTEGER.
DEFINE OUTPUT PARAMETER subgroup  AS INTEGER.
DEFINE OUTPUT PARAMETER fl-flag   AS INTEGER INIT 0.

DEFINE BUFFER b-article-list FOR rest-article-list.
DEFINE BUFFER b-maingroup-list FOR rest-maingroup-list.
DEFINE BUFFER b-subgroup-list FOR rest-subgroup-list.
DEFINE BUFFER b-wgrpgen FOR wgrpgen.
DEFINE BUFFER b-wgrpdep FOR wgrpdep.
DEFINE BUFFER b-artikel FOR h-artikel.

RUN cek-artikel.
IF fl-flag EQ 1 OR fl-flag EQ 2 OR fl-flag = 3 /*OR fl-flag = 4*/ THEN RETURN.

RUN import-artikel.

PROCEDURE cek-artikel:
  FOR EACH b-article-list:
    FIND FIRST b-maingroup-list WHERE (b-maingroup-list.maingroup-desc EQ b-article-list.main-group-desc)
        OR (b-maingroup-list.new-maingroup-desc EQ b-article-list.main-group-desc) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE b-maingroup-list THEN
    DO:
       ASSIGN artnr   = b-article-list.artnr
              dept    = b-article-list.dept-name
              fl-flag = 1.
       RETURN.
    END.
    FIND FIRST b-subgroup-list WHERE (b-subgroup-list.subgroup-desc EQ b-article-list.sub-group-desc)
        OR (b-subgroup-list.new-subgroup-desc EQ b-article-list.sub-group-desc) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE b-subgroup-list THEN
    DO:
       ASSIGN artnr   = b-article-list.artnr
              dept    = b-article-list.dept-name
              fl-flag = 2.
       RETURN.
    END.
    FIND FIRST rest-article-list WHERE rest-article-list.dept-no = b-article-list.dept-no
        AND rest-article-list.artnr = b-article-list.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE rest-article-list THEN
    DO:
       IF rest-article-list.art-desc NE b-article-list.art-desc THEN
       DO:
         ASSIGN
          art-desc1 = b-article-list.art-desc
          art-desc2 = rest-article-list.art-desc
          dept      = b-article-list.dept-name
          fl-flag   = 3.
         RETURN.
       END.
    END.
  END.          

  /*FOR EACH rest-maingroup-list:
      FIND FIRST b-maingroup-list WHERE b-maingroup-list.new-maingroup-no EQ rest-maingroup-list.maingroup-no NO-LOCK NO-ERROR.
      IF AVAILABLE b-maingroup-list THEN
      DO:
         ASSIGN maingroup = b-maingroup-list.new-maingroup-no
                fl-flag    = 3.
         RETURN.
      END.
  END.

  FOR EACH rest-subgroup-list:
      FIND FIRST b-subgroup-list WHERE b-subgroup-list.new-subgroup-no EQ rest-subgroup-list.subgroup-no
          AND b-subgroup-list.dept-no EQ rest-subgroup-list.dept-no NO-LOCK NO-ERROR.
      IF AVAILABLE b-subgroup-list THEN
      DO:
         ASSIGN subgroup = b-subgroup-list.new-subgroup-no
                dept     = b-subgroup-list.dept-name
                fl-flag   = 4.   
         RETURN.
      END.
  END.*/
END.

PROCEDURE import-artikel:
  FOR EACH h-artikel:
    FIND FIRST rest-article-list WHERE rest-article-list.artnr = h-artikel.artnr
        AND rest-article-list.dept-no = h-artikel.departement NO-LOCK NO-ERROR.
    IF AVAILABLE rest-article-list THEN
    DO:
      ASSIGN h-artikel.activeflag = rest-article-list.active-art.
    END.
  
    FIND FIRST rest-maingroup-list WHERE rest-maingroup-list.maingroup-no = h-artikel.endkum NO-LOCK NO-ERROR.
    IF AVAILABLE rest-maingroup-list THEN
    DO:
       ASSIGN h-artikel.endkum = rest-maingroup-list.new-maingroup-no.
    END.
  
    FIND FIRST rest-subgroup-list WHERE rest-subgroup-list.subgroup-no = h-artikel.zwkum
        AND rest-subgroup-list.dept-no = h-artikel.departement NO-LOCK NO-ERROR.
    IF AVAILABLE rest-subgroup-list THEN
    DO:
       ASSIGN h-artikel.zwkum = rest-subgroup-list.new-subgroup-no.
    END.
  END.
  
  FOR EACH rest-maingroup-list:
    FIND FIRST wgrpgen WHERE wgrpgen.eknr = rest-maingroup-list.maingroup-no NO-ERROR.
    IF AVAILABLE wgrpgen THEN
    DO:
       ASSIGN rest-maingroup-list.fibukonto  = wgrpgen.fibukonto
              rest-maingroup-list.betriebsnr = wgrpgen.betriebsnr.
       DELETE wgrpgen.
    END.
    IF NOT AVAILABLE wgrpgen THEN
    DO:
      ASSIGN rest-maingroup-list.fibukonto   = ""
              rest-maingroup-list.betriebsnr = 0.
    END.

    FIND FIRST b-wgrpgen WHERE b-wgrpgen.eknr = rest-maingroup-list.new-maingroup-no NO-ERROR.
    IF NOT AVAILABLE b-wgrpgen THEN
    DO:
      CREATE b-wgrpgen.
      ASSIGN b-wgrpgen.eknr         = rest-maingroup-list.new-maingroup-no
             b-wgrpgen.bezeich      = rest-maingroup-list.new-maingroup-desc
             b-wgrpgen.fibukonto    = rest-maingroup-list.fibukonto
             b-wgrpgen.betriebsnr   = rest-maingroup-list.betriebsnr.
    END.
    IF AVAILABLE b-wgrpgen THEN
    DO:
       ASSIGN b-wgrpgen.bezeich = rest-maingroup-list.new-maingroup-desc.
    END.

  END.
  
  FOR EACH rest-subgroup-list:
    FIND FIRST wgrpdep WHERE wgrpdep.zknr = rest-subgroup-list.subgroup-no
        AND wgrpdep.departement = rest-subgroup-list.dept-no NO-ERROR.
    IF AVAILABLE wgrpdep THEN
    DO:
       ASSIGN rest-subgroup-list.fibukonto  = wgrpdep.fibukonto
              rest-subgroup-list.betriebsnr = wgrpdep.betriebsnr.
       DELETE wgrpdep.
    END.
    IF NOT AVAILABLE wgrpdep THEN
    DO:
       ASSIGN rest-subgroup-list.fibukonto  = ""
              rest-subgroup-list.betriebsnr = 0.
    END.

    FIND FIRST b-wgrpdep WHERE b-wgrpdep.zknr = rest-subgroup-list.new-subgroup-no
        AND b-wgrpdep.departement = rest-subgroup-list.dept-no NO-ERROR.
    IF NOT AVAILABLE b-wgrpdep THEN
    DO:
    CREATE b-wgrpdep.
    ASSIGN b-wgrpdep.zknr         = rest-subgroup-list.new-subgroup-no
           b-wgrpdep.bezeich      = rest-subgroup-list.new-subgroup-desc
           b-wgrpdep.departement  = rest-subgroup-list.dept-no
           b-wgrpdep.fibukonto    = rest-subgroup-list.fibukonto
           b-wgrpdep.betriebsnr   = rest-subgroup-list.betriebsnr.
    END.
    IF AVAILABLE b-wgrpdep THEN
    DO:
       ASSIGN b-wgrpdep.bezeich = rest-subgroup-list.new-subgroup-desc.
    END.
  END.
  
  FOR EACH rest-article-list NO-LOCK:
    FIND FIRST h-artikel WHERE h-artikel.artnr = rest-article-list.artnr
        AND h-artikel.departement = rest-article-list.dept-no NO-ERROR.
    IF NOT AVAILABLE h-artikel THEN
    DO:        
       CREATE h-artikel.
       ASSIGN h-artikel.departement  = rest-article-list.dept-no
              h-artikel.artnr        = rest-article-list.artnr
              h-artikel.bezeich      = rest-article-list.art-desc
              h-artikel.epreis1      = rest-article-list.price
              h-artikel.autosaldo    = NO
              h-artikel.bezaendern   = NO
              h-artikel.prozent      = rest-article-list.cost%
              h-artikel.bondruckernr = rest-article-list.kp-no
              h-artikel.aenderwunsch = NO
              h-artikel.artnrfront   = rest-article-list.fo-artnr
              h-artikel.artnrrezept  = rest-article-list.recipe-no
              h-artikel.activeflag   = rest-article-list.active-art
              h-artikel.betriebsnr   = 0.
           .

      FIND FIRST wgrpgen WHERE wgrpgen.bezeich = rest-article-list.main-group-desc NO-LOCK NO-ERROR.
      IF AVAILABLE wgrpgen THEN
      DO:
         h-artikel.endkum = wgrpgen.eknr.

         FIND FIRST b-artikel WHERE b-artikel.endkum = wgrpgen.eknr AND b-artikel.mwst-code NE 0
             AND b-artikel.service-code NE 0 NO-LOCK NO-ERROR.
         IF AVAILABLE b-artikel THEN
            ASSIGN h-artikel.mwst-code = b-artikel.mwst-code
                   h-artikel.service-code = b-artikel.service-code.
      END.
  
      FIND FIRST wgrpdep WHERE wgrpdep.bezeich = rest-article-list.sub-group-desc
          AND wgrpdep.departement = rest-article-list.dept-no NO-LOCK NO-ERROR.
      IF AVAILABLE wgrpdep THEN
      DO:
         h-artikel.zwkum = wgrpdep.zknr.                            
      END.
    END.
    ELSE IF AVAILABLE h-artikel THEN
    DO:
       IF LENGTH(STRING(rest-article-list.artnr)) GT 6 THEN
       DO:
          ASSIGN 
              h-artikel.epreis1 = rest-article-list.price                 
              h-artikel.activeflag = rest-article-list.active-art
              h-artikel.bezeich = rest-article-list.art-desc /*FDL: 258C16*/
              .

          IF h-artikel.mwst-code EQ 0 AND h-artikel.service-code EQ 0 THEN
          DO:
             FIND FIRST b-artikel WHERE b-artikel.endkum = h-artikel.endkum
                 AND b-artikel.mwst-code NE 0
                 AND b-artikel.service-code NE 0 NO-LOCK NO-ERROR.
             IF AVAILABLE b-artikel THEN
                ASSIGN h-artikel.mwst-code = b-artikel.mwst-code
                       h-artikel.service-code = b-artikel.service-code.
          END.
       END.
    END.
  END.
END.
