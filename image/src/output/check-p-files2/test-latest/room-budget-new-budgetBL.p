
DEF INPUT PARAMETER fdate            AS DATE.
DEF INPUT PARAMETER tdate            AS DATE.
DEF INPUT PARAMETER anzahl           AS INTEGER.
DEF INPUT PARAMETER logis            AS DECIMAL.
DEF INPUT PARAMETER occrm            AS DECIMAL.
DEF INPUT PARAMETER betrag           AS DECIMAL.
DEF INPUT PARAMETER user-init        AS CHAR.
DEF INPUT PARAMETER zimkateg-zikatnr AS INT.

DEFINE VARIABLE datum  AS DATE.

DO datum = fdate TO tdate: 
    IF datum = tdate THEN
    ASSIGN
      anzahl = occrm
      logis  = betrag
    .
    FIND FIRST rmbudget WHERE rmbudget.datum = datum 
      AND rmbudget.zikatnr = zimkateg-zikatnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE rmbudget THEN 
    DO: 
       CREATE rmbudget. 
       ASSIGN
         rmbudget.datum    = datum 
         rmbudget.zikatnr  = zimkateg-zikatnr
       . 
    END.
    ASSIGN
      rmbudget.zimmeranz = anzahl
      rmbudget.logis     = logis 
      rmbudget.userinit  = user-init
      rmbudget.zeit      = TIME
      occrm              = occrm - anzahl
      betrag             = betrag - logis
    .
END.
