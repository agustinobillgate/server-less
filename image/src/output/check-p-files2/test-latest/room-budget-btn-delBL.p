
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST rmbudget WHERE RECID(rmbudget) = rec-id.
FIND CURRENT rmbudget EXCLUSIVE-LOCK. 
DELETE rmbudget.
RELEASE rmbudget.
