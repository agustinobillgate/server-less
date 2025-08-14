\echo . 
\echo Loading Table bk_package 
\copy qcauto.bk_package from '/usr1/dump-qcserverless4-20250812/bk-package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_package__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_package));
\echo Finish Table bk_package 
\echo . 
\echo Loading Table bk_pause 
\copy qcauto.bk_pause from '/usr1/dump-qcserverless4-20250812/bk-pause.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_pause__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_pause));
\echo Finish Table bk_pause 
\echo . 
\echo Loading Table bk_rart 
\copy qcauto.bk_rart from '/usr1/dump-qcserverless4-20250812/bk-rart.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_rart__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_rart));
\echo Finish Table bk_rart 
\echo . 
\echo Loading Table bk_raum 
\copy qcauto.bk_raum from '/usr1/dump-qcserverless4-20250812/bk-raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_raum__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_raum));
\echo Finish Table bk_raum 
\echo . 
\echo Loading Table bk_reser 
\copy qcauto.bk_reser from '/usr1/dump-qcserverless4-20250812/bk-reser.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_reser__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_reser));
\echo Finish Table bk_reser 
\echo . 
\echo Loading Table bk_rset 
\copy qcauto.bk_rset from '/usr1/dump-qcserverless4-20250812/bk-rset.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_rset__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_rset));
\echo Finish Table bk_rset 
\echo . 
\echo Loading Table bk_setup 
\copy qcauto.bk_setup from '/usr1/dump-qcserverless4-20250812/bk-setup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_setup__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_setup));
\echo Finish Table bk_setup 
\echo . 
\echo Loading Table bk_stat 
\copy qcauto.bk_stat from '/usr1/dump-qcserverless4-20250812/bk-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_stat__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_stat));
\echo Finish Table bk_stat 
\echo . 
\echo Loading Table bk_veran 
\copy qcauto.bk_veran from '/usr1/dump-qcserverless4-20250812/bk-veran.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bk_veran__recid_seq', (SELECT MAX(_recid) FROM qcauto.bk_veran));
update qcauto.bk_veran set payment_userinit = array_replace(payment_userinit,NULL,''); 
\echo Finish Table bk_veran 
\echo . 
\echo Loading Table bl_dates 
\copy qcauto.bl_dates from '/usr1/dump-qcserverless4-20250812/bl-dates.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bl_dates__recid_seq', (SELECT MAX(_recid) FROM qcauto.bl_dates));
\echo Finish Table bl_dates 
\echo . 
\echo Loading Table blinehis 
\copy qcauto.blinehis from '/usr1/dump-qcserverless4-20250812/blinehis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.blinehis__recid_seq', (SELECT MAX(_recid) FROM qcauto.blinehis));
\echo Finish Table blinehis 
\echo . 
\echo Loading Table bresline 
\copy qcauto.bresline from '/usr1/dump-qcserverless4-20250812/bresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.bresline__recid_seq', (SELECT MAX(_recid) FROM qcauto.bresline));
update qcauto.bresline set texte = array_replace(texte,NULL,''); 
\echo Finish Table bresline 
\echo . 
\echo Loading Table brief 
\copy qcauto.brief from '/usr1/dump-qcserverless4-20250812/brief.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.brief__recid_seq', (SELECT MAX(_recid) FROM qcauto.brief));
\echo Finish Table brief 
\echo . 
\echo Loading Table brieftmp 
\copy qcauto.brieftmp from '/usr1/dump-qcserverless4-20250812/brieftmp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.brieftmp__recid_seq', (SELECT MAX(_recid) FROM qcauto.brieftmp));
\echo Finish Table brieftmp 
\echo . 
\echo Loading Table briefzei 
\copy qcauto.briefzei from '/usr1/dump-qcserverless4-20250812/briefzei.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.briefzei__recid_seq', (SELECT MAX(_recid) FROM qcauto.briefzei));
\echo Finish Table briefzei 
\echo . 
\echo Loading Table budget 
\copy qcauto.budget from '/usr1/dump-qcserverless4-20250812/budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.budget__recid_seq', (SELECT MAX(_recid) FROM qcauto.budget));
\echo Finish Table budget 
\echo . 
\echo Loading Table calls 
\copy qcauto.calls from '/usr1/dump-qcserverless4-20250812/calls.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.calls__recid_seq', (SELECT MAX(_recid) FROM qcauto.calls));
\echo Finish Table calls 
\echo . 
\echo Loading Table cl_bonus 
\copy qcauto.cl_bonus from '/usr1/dump-qcserverless4-20250812/cl-bonus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_bonus__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_bonus));
\echo Finish Table cl_bonus 
\echo . 
\echo Loading Table cl_book 
\copy qcauto.cl_book from '/usr1/dump-qcserverless4-20250812/cl-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_book__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_book));
\echo Finish Table cl_book 
\echo . 
\echo Loading Table cl_checkin 
\copy qcauto.cl_checkin from '/usr1/dump-qcserverless4-20250812/cl-checkin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_checkin__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_checkin));
\echo Finish Table cl_checkin 
\echo . 
\echo Loading Table cl_class 
\copy qcauto.cl_class from '/usr1/dump-qcserverless4-20250812/cl-class.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_class__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_class));
\echo Finish Table cl_class 
\echo . 
\echo Loading Table cl_enroll 
\copy qcauto.cl_enroll from '/usr1/dump-qcserverless4-20250812/cl-enroll.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_enroll__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_enroll));
\echo Finish Table cl_enroll 
\echo . 
\echo Loading Table cl_free 
\copy qcauto.cl_free from '/usr1/dump-qcserverless4-20250812/cl-free.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_free__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_free));
\echo Finish Table cl_free 
\echo . 
\echo Loading Table cl_histci 
\copy qcauto.cl_histci from '/usr1/dump-qcserverless4-20250812/cl-histci.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_histci__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_histci));
\echo Finish Table cl_histci 
\echo . 
\echo Loading Table cl_histpay 
\copy qcauto.cl_histpay from '/usr1/dump-qcserverless4-20250812/cl-histpay.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_histpay__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_histpay));
\echo Finish Table cl_histpay 
\echo . 
\echo Loading Table cl_histstatus 
\copy qcauto.cl_histstatus from '/usr1/dump-qcserverless4-20250812/cl-histstatus.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_histstatus__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_histstatus));
\echo Finish Table cl_histstatus 
\echo . 
\echo Loading Table cl_histtrain 
\copy qcauto.cl_histtrain from '/usr1/dump-qcserverless4-20250812/cl-histtrain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_histtrain__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_histtrain));
\echo Finish Table cl_histtrain 
\echo . 
\echo Loading Table cl_histvisit 
\copy qcauto.cl_histvisit from '/usr1/dump-qcserverless4-20250812/cl-histvisit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_histvisit__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_histvisit));
\echo Finish Table cl_histvisit 
\echo . 
\echo Loading Table cl_home 
\copy qcauto.cl_home from '/usr1/dump-qcserverless4-20250812/cl-home.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_home__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_home));
\echo Finish Table cl_home 
\echo . 
\echo Loading Table cl_location 
\copy qcauto.cl_location from '/usr1/dump-qcserverless4-20250812/cl-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_location__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_location));
\echo Finish Table cl_location 
\echo . 
\echo Loading Table cl_locker 
\copy qcauto.cl_locker from '/usr1/dump-qcserverless4-20250812/cl-locker.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_locker__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_locker));
\echo Finish Table cl_locker 
\echo . 
\echo Loading Table cl_log 
\copy qcauto.cl_log from '/usr1/dump-qcserverless4-20250812/cl-log.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_log__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_log));
\echo Finish Table cl_log 
\echo . 
\echo Loading Table cl_member 
\copy qcauto.cl_member from '/usr1/dump-qcserverless4-20250812/cl-member.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_member__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_member));
\echo Finish Table cl_member 
\echo . 
\echo Loading Table cl_memtype 
\copy qcauto.cl_memtype from '/usr1/dump-qcserverless4-20250812/cl-memtype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_memtype__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_memtype));
\echo Finish Table cl_memtype 
\echo . 
\echo Loading Table cl_paysched 
\copy qcauto.cl_paysched from '/usr1/dump-qcserverless4-20250812/cl-paysched.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_paysched__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_paysched));
\echo Finish Table cl_paysched 
\echo . 
\echo Loading Table cl_stat 
\copy qcauto.cl_stat from '/usr1/dump-qcserverless4-20250812/cl-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_stat__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_stat));
\echo Finish Table cl_stat 
\echo . 
\echo Loading Table cl_stat1 
\copy qcauto.cl_stat1 from '/usr1/dump-qcserverless4-20250812/cl-stat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_stat1__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_stat1));
\echo Finish Table cl_stat1 
\echo . 
\echo Loading Table cl_towel 
\copy qcauto.cl_towel from '/usr1/dump-qcserverless4-20250812/cl-towel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_towel__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_towel));
\echo Finish Table cl_towel 
\echo . 
\echo Loading Table cl_trainer 
\copy qcauto.cl_trainer from '/usr1/dump-qcserverless4-20250812/cl-trainer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_trainer__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_trainer));
\echo Finish Table cl_trainer 
\echo . 
\echo Loading Table cl_upgrade 
\copy qcauto.cl_upgrade from '/usr1/dump-qcserverless4-20250812/cl-upgrade.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cl_upgrade__recid_seq', (SELECT MAX(_recid) FROM qcauto.cl_upgrade));
\echo Finish Table cl_upgrade 
\echo . 
\echo Loading Table costbudget 
\copy qcauto.costbudget from '/usr1/dump-qcserverless4-20250812/costbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.costbudget__recid_seq', (SELECT MAX(_recid) FROM qcauto.costbudget));
\echo Finish Table costbudget 
\echo . 
\echo Loading Table counters 
\copy qcauto.counters from '/usr1/dump-qcserverless4-20250812/counters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.counters__recid_seq', (SELECT MAX(_recid) FROM qcauto.counters));
\echo Finish Table counters 
\echo . 
\echo Loading Table crm_campaign 
\copy qcauto.crm_campaign from '/usr1/dump-qcserverless4-20250812/crm-campaign.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_campaign__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_campaign));
\echo Finish Table crm_campaign 
\echo . 
\echo Loading Table crm_category 
\copy qcauto.crm_category from '/usr1/dump-qcserverless4-20250812/crm-category.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_category__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_category));
\echo Finish Table crm_category 
\echo . 
\echo Loading Table crm_dept 
\copy qcauto.crm_dept from '/usr1/dump-qcserverless4-20250812/crm-dept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_dept__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_dept));
\echo Finish Table crm_dept 
\echo . 
\echo Loading Table crm_dtl 
\copy qcauto.crm_dtl from '/usr1/dump-qcserverless4-20250812/crm-dtl.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_dtl__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_dtl));
\echo Finish Table crm_dtl 
\echo . 
\echo Loading Table crm_email 
\copy qcauto.crm_email from '/usr1/dump-qcserverless4-20250812/crm-email.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_email__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_email));
\echo Finish Table crm_email 
\echo . 
\echo Loading Table crm_event 
\copy qcauto.crm_event from '/usr1/dump-qcserverless4-20250812/crm-event.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_event__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_event));
\echo Finish Table crm_event 
\echo . 
\echo Loading Table crm_feedhdr 
\copy qcauto.crm_feedhdr from '/usr1/dump-qcserverless4-20250812/crm-feedhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_feedhdr__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_feedhdr));
\echo Finish Table crm_feedhdr 
\echo . 
\echo Loading Table crm_fnlresult 
\copy qcauto.crm_fnlresult from '/usr1/dump-qcserverless4-20250812/crm-fnlresult.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_fnlresult__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_fnlresult));
\echo Finish Table crm_fnlresult 
\echo . 
\echo Loading Table crm_language 
\copy qcauto.crm_language from '/usr1/dump-qcserverless4-20250812/crm-language.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_language__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_language));
\echo Finish Table crm_language 
\echo . 
\echo Loading Table crm_question 
\copy qcauto.crm_question from '/usr1/dump-qcserverless4-20250812/crm-question.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_question__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_question));
\echo Finish Table crm_question 
\echo . 
\echo Loading Table crm_tamplang 
\copy qcauto.crm_tamplang from '/usr1/dump-qcserverless4-20250812/crm-tamplang.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_tamplang__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_tamplang));
\echo Finish Table crm_tamplang 
\echo . 
\echo Loading Table crm_template 
\copy qcauto.crm_template from '/usr1/dump-qcserverless4-20250812/crm-template.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.crm_template__recid_seq', (SELECT MAX(_recid) FROM qcauto.crm_template));
\echo Finish Table crm_template 
\echo . 
\echo Loading Table cross_dtl 
\copy qcauto.cross_dtl from '/usr1/dump-qcserverless4-20250812/cross-DTL.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cross_dtl__recid_seq', (SELECT MAX(_recid) FROM qcauto.cross_dtl));
\echo Finish Table cross_dtl 
\echo . 
\echo Loading Table cross_hdr 
\copy qcauto.cross_hdr from '/usr1/dump-qcserverless4-20250812/cross-HDR.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.cross_hdr__recid_seq', (SELECT MAX(_recid) FROM qcauto.cross_hdr));
\echo Finish Table cross_hdr 
\echo . 
\echo Loading Table debitor 
\copy qcauto.debitor from '/usr1/dump-qcserverless4-20250812/debitor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.debitor__recid_seq', (SELECT MAX(_recid) FROM qcauto.debitor));
\echo Finish Table debitor 
\echo . 
\echo Loading Table debthis 
\copy qcauto.debthis from '/usr1/dump-qcserverless4-20250812/debthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.debthis__recid_seq', (SELECT MAX(_recid) FROM qcauto.debthis));
\echo Finish Table debthis 
\echo . 
\echo Loading Table desttext 
\copy qcauto.desttext from '/usr1/dump-qcserverless4-20250812/desttext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.desttext__recid_seq', (SELECT MAX(_recid) FROM qcauto.desttext));
\echo Finish Table desttext 
\echo . 
\echo Loading Table dml_art 
\copy qcauto.dml_art from '/usr1/dump-qcserverless4-20250812/dml-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.dml_art__recid_seq', (SELECT MAX(_recid) FROM qcauto.dml_art));
\echo Finish Table dml_art 
\echo . 
\echo Loading Table dml_artdep 
\copy qcauto.dml_artdep from '/usr1/dump-qcserverless4-20250812/dml-artdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.dml_artdep__recid_seq', (SELECT MAX(_recid) FROM qcauto.dml_artdep));
\echo Finish Table dml_artdep 
\echo . 
\echo Loading Table dml_rate 
\copy qcauto.dml_rate from '/usr1/dump-qcserverless4-20250812/dml-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.dml_rate__recid_seq', (SELECT MAX(_recid) FROM qcauto.dml_rate));
\echo Finish Table dml_rate 
\echo . 
\echo Loading Table eg_action 
\copy qcauto.eg_action from '/usr1/dump-qcserverless4-20250812/eg-action.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_action__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_action));
\echo Finish Table eg_action 
\echo . 
\echo Loading Table eg_alert 
\copy qcauto.eg_alert from '/usr1/dump-qcserverless4-20250812/eg-Alert.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_alert__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_alert));
\echo Finish Table eg_alert 
\echo . 
\echo Loading Table eg_budget 
\copy qcauto.eg_budget from '/usr1/dump-qcserverless4-20250812/eg-budget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_budget__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_budget));
\echo Finish Table eg_budget 
\echo . 
\echo Loading Table eg_cost 
\copy qcauto.eg_cost from '/usr1/dump-qcserverless4-20250812/eg-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_cost__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_cost));
\echo Finish Table eg_cost 
\echo . 
\echo Loading Table eg_duration 
\copy qcauto.eg_duration from '/usr1/dump-qcserverless4-20250812/eg-Duration.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_duration__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_duration));
\echo Finish Table eg_duration 
\echo . 
\echo Loading Table eg_location 
\copy qcauto.eg_location from '/usr1/dump-qcserverless4-20250812/eg-location.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_location__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_location));
\echo Finish Table eg_location 
\echo . 
\echo Loading Table eg_mainstat 
\copy qcauto.eg_mainstat from '/usr1/dump-qcserverless4-20250812/eg-MainStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_mainstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_mainstat));
\echo Finish Table eg_mainstat 
\echo . 
\echo Loading Table eg_maintain 
\copy qcauto.eg_maintain from '/usr1/dump-qcserverless4-20250812/eg-maintain.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_maintain__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_maintain));
\echo Finish Table eg_maintain 
\echo . 
\echo Loading Table eg_mdetail 
\copy qcauto.eg_mdetail from '/usr1/dump-qcserverless4-20250812/eg-mdetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_mdetail__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_mdetail));
\echo Finish Table eg_mdetail 
\echo . 
\echo Loading Table eg_messageno 
\copy qcauto.eg_messageno from '/usr1/dump-qcserverless4-20250812/eg-MessageNo.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_messageno__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_messageno));
\echo Finish Table eg_messageno 
\echo . 
\echo Loading Table eg_mobilenr 
\copy qcauto.eg_mobilenr from '/usr1/dump-qcserverless4-20250812/eg-mobileNr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_mobilenr__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_mobilenr));
\echo Finish Table eg_mobilenr 
\echo . 
\echo Loading Table eg_moveproperty 
\copy qcauto.eg_moveproperty from '/usr1/dump-qcserverless4-20250812/eg-moveProperty.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_moveproperty__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_moveproperty));
\echo Finish Table eg_moveproperty 
\echo . 
\echo Loading Table eg_property 
\copy qcauto.eg_property from '/usr1/dump-qcserverless4-20250812/eg-property.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_property__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_property));
\echo Finish Table eg_property 
\echo . 
\echo Loading Table eg_propmeter 
\copy qcauto.eg_propmeter from '/usr1/dump-qcserverless4-20250812/eg-propMeter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_propmeter__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_propmeter));
\echo Finish Table eg_propmeter 
\echo . 
\echo Loading Table eg_queasy 
\copy qcauto.eg_queasy from '/usr1/dump-qcserverless4-20250812/eg-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_queasy__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_queasy));
\echo Finish Table eg_queasy 
\echo . 
\echo Loading Table eg_reqdetail 
\copy qcauto.eg_reqdetail from '/usr1/dump-qcserverless4-20250812/eg-reqDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_reqdetail__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_reqdetail));
\echo Finish Table eg_reqdetail 
\echo . 
\echo Loading Table eg_reqif 
\copy qcauto.eg_reqif from '/usr1/dump-qcserverless4-20250812/eg-reqif.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_reqif__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_reqif));
\echo Finish Table eg_reqif 
\echo . 
\echo Loading Table eg_reqstat 
\copy qcauto.eg_reqstat from '/usr1/dump-qcserverless4-20250812/eg-ReqStat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_reqstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_reqstat));
\echo Finish Table eg_reqstat 
\echo . 
\echo Loading Table eg_request 
\copy qcauto.eg_request from '/usr1/dump-qcserverless4-20250812/eg-request.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_request__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_request));
\echo Finish Table eg_request 
\echo . 
\echo Loading Table eg_resources 
\copy qcauto.eg_resources from '/usr1/dump-qcserverless4-20250812/eg-resources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_resources__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_resources));
\echo Finish Table eg_resources 
\echo . 
\echo Loading Table eg_staff 
\copy qcauto.eg_staff from '/usr1/dump-qcserverless4-20250812/eg-staff.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_staff__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_staff));
\echo Finish Table eg_staff 
\echo . 
\echo Loading Table eg_stat 
\copy qcauto.eg_stat from '/usr1/dump-qcserverless4-20250812/eg-stat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_stat__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_stat));
\echo Finish Table eg_stat 
\echo . 
\echo Loading Table eg_subtask 
\copy qcauto.eg_subtask from '/usr1/dump-qcserverless4-20250812/eg-subtask.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_subtask__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_subtask));
\echo Finish Table eg_subtask 
\echo . 
\echo Loading Table eg_vendor 
\copy qcauto.eg_vendor from '/usr1/dump-qcserverless4-20250812/eg-vendor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_vendor__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_vendor));
\echo Finish Table eg_vendor 
\echo . 
\echo Loading Table eg_vperform 
\copy qcauto.eg_vperform from '/usr1/dump-qcserverless4-20250812/eg-vperform.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.eg_vperform__recid_seq', (SELECT MAX(_recid) FROM qcauto.eg_vperform));
\echo Finish Table eg_vperform 
\echo . 
\echo Loading Table ekum 
\copy qcauto.ekum from '/usr1/dump-qcserverless4-20250812/ekum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.ekum__recid_seq', (SELECT MAX(_recid) FROM qcauto.ekum));
\echo Finish Table ekum 
\echo . 
\echo Loading Table employee 
\copy qcauto.employee from '/usr1/dump-qcserverless4-20250812/employee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.employee__recid_seq', (SELECT MAX(_recid) FROM qcauto.employee));
update qcauto.employee set child = array_replace(child,NULL,''); 
\echo Finish Table employee 
\echo . 
\echo Loading Table equiplan 
\copy qcauto.equiplan from '/usr1/dump-qcserverless4-20250812/equiplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.equiplan__recid_seq', (SELECT MAX(_recid) FROM qcauto.equiplan));
\echo Finish Table equiplan 
\echo . 
\echo Loading Table exrate 
\copy qcauto.exrate from '/usr1/dump-qcserverless4-20250812/exrate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.exrate__recid_seq', (SELECT MAX(_recid) FROM qcauto.exrate));
\echo Finish Table exrate 
\echo . 
\echo Loading Table fa_artikel 
\copy qcauto.fa_artikel from '/usr1/dump-qcserverless4-20250812/fa-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_artikel__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_artikel));
\echo Finish Table fa_artikel 
\echo . 
\echo Loading Table fa_counter 
\copy qcauto.fa_counter from '/usr1/dump-qcserverless4-20250812/fa-Counter.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_counter__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_counter));
\echo Finish Table fa_counter 
\echo . 
\echo Loading Table fa_dp 
\copy qcauto.fa_dp from '/usr1/dump-qcserverless4-20250812/fa-DP.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_dp__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_dp));
\echo Finish Table fa_dp 
\echo . 
\echo Loading Table fa_grup 
\copy qcauto.fa_grup from '/usr1/dump-qcserverless4-20250812/fa-grup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_grup__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_grup));
\echo Finish Table fa_grup 
\echo . 
\echo Loading Table fa_kateg 
\copy qcauto.fa_kateg from '/usr1/dump-qcserverless4-20250812/fa-kateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_kateg__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_kateg));
\echo Finish Table fa_kateg 
\echo . 
\echo Loading Table fa_lager 
\copy qcauto.fa_lager from '/usr1/dump-qcserverless4-20250812/fa-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_lager__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_lager));
\echo Finish Table fa_lager 
\echo . 
\echo Loading Table fa_op 
\copy qcauto.fa_op from '/usr1/dump-qcserverless4-20250812/fa-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_op__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_op));
\echo Finish Table fa_op 
\echo . 
\echo Loading Table fa_order 
\copy qcauto.fa_order from '/usr1/dump-qcserverless4-20250812/fa-Order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_order__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_order));
\echo Finish Table fa_order 
\echo . 
\echo Loading Table fa_ordheader 
\copy qcauto.fa_ordheader from '/usr1/dump-qcserverless4-20250812/fa-OrdHeader.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_ordheader__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_ordheader));
\echo Finish Table fa_ordheader 
\echo . 
\echo Loading Table fa_quodetail 
\copy qcauto.fa_quodetail from '/usr1/dump-qcserverless4-20250812/fa-QuoDetail.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_quodetail__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_quodetail));
\echo Finish Table fa_quodetail 
\echo . 
\echo Loading Table fa_quotation 
\copy qcauto.fa_quotation from '/usr1/dump-qcserverless4-20250812/fa-quotation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_quotation__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_quotation));
\echo Finish Table fa_quotation 
\echo . 
\echo Loading Table fa_user 
\copy qcauto.fa_user from '/usr1/dump-qcserverless4-20250812/fa-user.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fa_user__recid_seq', (SELECT MAX(_recid) FROM qcauto.fa_user));
update qcauto.fa_user set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table fa_user 
\echo . 
\echo Loading Table fbstat 
\copy qcauto.fbstat from '/usr1/dump-qcserverless4-20250812/fbstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fbstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.fbstat));
\echo Finish Table fbstat 
\echo . 
\echo Loading Table feiertag 
\copy qcauto.feiertag from '/usr1/dump-qcserverless4-20250812/feiertag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.feiertag__recid_seq', (SELECT MAX(_recid) FROM qcauto.feiertag));
\echo Finish Table feiertag 
\echo . 
\echo Loading Table ffont 
\copy qcauto.ffont from '/usr1/dump-qcserverless4-20250812/ffont.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.ffont__recid_seq', (SELECT MAX(_recid) FROM qcauto.ffont));
\echo Finish Table ffont 
\echo . 
\echo Loading Table fixleist 
\copy qcauto.fixleist from '/usr1/dump-qcserverless4-20250812/fixleist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.fixleist__recid_seq', (SELECT MAX(_recid) FROM qcauto.fixleist));
\echo Finish Table fixleist 
\echo . 
\echo Loading Table gc_giro 
\copy qcauto.gc_giro from '/usr1/dump-qcserverless4-20250812/gc-giro.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gc_giro__recid_seq', (SELECT MAX(_recid) FROM qcauto.gc_giro));
update qcauto.gc_giro set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_giro 
\echo . 
\echo Loading Table gc_jouhdr 
\copy qcauto.gc_jouhdr from '/usr1/dump-qcserverless4-20250812/gc-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gc_jouhdr__recid_seq', (SELECT MAX(_recid) FROM qcauto.gc_jouhdr));
\echo Finish Table gc_jouhdr 
\echo . 
\echo Loading Table gc_journal 
\copy qcauto.gc_journal from '/usr1/dump-qcserverless4-20250812/gc-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gc_journal__recid_seq', (SELECT MAX(_recid) FROM qcauto.gc_journal));
\echo Finish Table gc_journal 
\echo . 
\echo Loading Table gc_pi 
\copy qcauto.gc_pi from '/usr1/dump-qcserverless4-20250812/gc-PI.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gc_pi__recid_seq', (SELECT MAX(_recid) FROM qcauto.gc_pi));
update qcauto.gc_pi set bez_array = array_replace(bez_array,NULL,''); 
update qcauto.gc_pi set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table gc_pi 
\echo . 
\echo Loading Table gc_piacct 
\copy qcauto.gc_piacct from '/usr1/dump-qcserverless4-20250812/gc-piacct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gc_piacct__recid_seq', (SELECT MAX(_recid) FROM qcauto.gc_piacct));
\echo Finish Table gc_piacct 
\echo . 
\echo Loading Table gc_pibline 
\copy qcauto.gc_pibline from '/usr1/dump-qcserverless4-20250812/gc-PIbline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gc_pibline__recid_seq', (SELECT MAX(_recid) FROM qcauto.gc_pibline));
\echo Finish Table gc_pibline 
\echo . 
\echo Loading Table gc_pitype 
\copy qcauto.gc_pitype from '/usr1/dump-qcserverless4-20250812/gc-piType.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gc_pitype__recid_seq', (SELECT MAX(_recid) FROM qcauto.gc_pitype));
\echo Finish Table gc_pitype 
\echo . 
\echo Loading Table genfcast 
\copy qcauto.genfcast from '/usr1/dump-qcserverless4-20250812/genfcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.genfcast__recid_seq', (SELECT MAX(_recid) FROM qcauto.genfcast));
update qcauto.genfcast set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genfcast 
\echo . 
\echo Loading Table genlayout 
\copy qcauto.genlayout from '/usr1/dump-qcserverless4-20250812/genlayout.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.genlayout__recid_seq', (SELECT MAX(_recid) FROM qcauto.genlayout));
update qcauto.genlayout set button_ext = array_replace(button_ext,NULL,''); 
update qcauto.genlayout set char_ext = array_replace(char_ext,NULL,''); 
update qcauto.genlayout set combo_ext = array_replace(combo_ext,NULL,''); 
update qcauto.genlayout set date_ext = array_replace(date_ext,NULL,''); 
update qcauto.genlayout set deci_ext = array_replace(deci_ext,NULL,''); 
update qcauto.genlayout set inte_ext = array_replace(inte_ext,NULL,''); 
update qcauto.genlayout set logi_ext = array_replace(logi_ext,NULL,''); 
update qcauto.genlayout set string_ext = array_replace(string_ext,NULL,''); 
update qcauto.genlayout set tchar_ext = array_replace(tchar_ext,NULL,''); 
update qcauto.genlayout set tdate_ext = array_replace(tdate_ext,NULL,''); 
update qcauto.genlayout set tdeci_ext = array_replace(tdeci_ext,NULL,''); 
update qcauto.genlayout set tinte_ext = array_replace(tinte_ext,NULL,''); 
update qcauto.genlayout set tlogi_ext = array_replace(tlogi_ext,NULL,''); 
\echo Finish Table genlayout 
\echo . 
\echo Loading Table genstat 
\copy qcauto.genstat from '/usr1/dump-qcserverless4-20250812/genstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.genstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.genstat));
update qcauto.genstat set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table genstat 
\echo . 
\echo Loading Table gentable 
\copy qcauto.gentable from '/usr1/dump-qcserverless4-20250812/gentable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gentable__recid_seq', (SELECT MAX(_recid) FROM qcauto.gentable));
update qcauto.gentable set char_ext = array_replace(char_ext,NULL,''); 
update qcauto.gentable set combo_ext = array_replace(combo_ext,NULL,''); 
\echo Finish Table gentable 
\echo . 
\echo Loading Table gk_field 
\copy qcauto.gk_field from '/usr1/dump-qcserverless4-20250812/gk-field.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gk_field__recid_seq', (SELECT MAX(_recid) FROM qcauto.gk_field));
\echo Finish Table gk_field 
\echo . 
\echo Loading Table gk_label 
\copy qcauto.gk_label from '/usr1/dump-qcserverless4-20250812/gk-label.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gk_label__recid_seq', (SELECT MAX(_recid) FROM qcauto.gk_label));
\echo Finish Table gk_label 
\echo . 
\echo Loading Table gk_notes 
\copy qcauto.gk_notes from '/usr1/dump-qcserverless4-20250812/gk-notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gk_notes__recid_seq', (SELECT MAX(_recid) FROM qcauto.gk_notes));
update qcauto.gk_notes set notes = array_replace(notes,NULL,''); 
\echo Finish Table gk_notes 
\echo . 
\echo Loading Table gl_acct 
\copy qcauto.gl_acct from '/usr1/dump-qcserverless4-20250812/gl-acct.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_acct__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_acct));
\echo Finish Table gl_acct 
\echo . 
\echo Loading Table gl_accthis 
\copy qcauto.gl_accthis from '/usr1/dump-qcserverless4-20250812/gl-accthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_accthis__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_accthis));
\echo Finish Table gl_accthis 
\echo . 
\echo Loading Table gl_coa 
\copy qcauto.gl_coa from '/usr1/dump-qcserverless4-20250812/gl-coa.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_coa__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_coa));
\echo Finish Table gl_coa 
\echo . 
\echo Loading Table gl_cost 
\copy qcauto.gl_cost from '/usr1/dump-qcserverless4-20250812/gl-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_cost__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_cost));
\echo Finish Table gl_cost 
\echo . 
\echo Loading Table gl_department 
\copy qcauto.gl_department from '/usr1/dump-qcserverless4-20250812/gl-department.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_department__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_department));
\echo Finish Table gl_department 
\echo . 
\echo Loading Table gl_fstype 
\copy qcauto.gl_fstype from '/usr1/dump-qcserverless4-20250812/gl-fstype.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_fstype__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_fstype));
\echo Finish Table gl_fstype 
\echo . 
\echo Loading Table gl_htljournal 
\copy qcauto.gl_htljournal from '/usr1/dump-qcserverless4-20250812/gl-htljournal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_htljournal__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_htljournal));
\echo Finish Table gl_htljournal 
\echo . 
\echo Loading Table gl_jhdrhis 
\copy qcauto.gl_jhdrhis from '/usr1/dump-qcserverless4-20250812/gl-jhdrhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_jhdrhis__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_jhdrhis));
\echo Finish Table gl_jhdrhis 
\echo . 
\echo Loading Table gl_jouhdr 
\copy qcauto.gl_jouhdr from '/usr1/dump-qcserverless4-20250812/gl-jouhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_jouhdr__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_jouhdr));
\echo Finish Table gl_jouhdr 
\echo . 
\echo Loading Table gl_jourhis 
\copy qcauto.gl_jourhis from '/usr1/dump-qcserverless4-20250812/gl-jourhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_jourhis__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_jourhis));
\echo Finish Table gl_jourhis 
\echo . 
\echo Loading Table gl_journal 
\copy qcauto.gl_journal from '/usr1/dump-qcserverless4-20250812/gl-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_journal__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_journal));
\echo Finish Table gl_journal 
\echo . 
\echo Loading Table gl_main 
\copy qcauto.gl_main from '/usr1/dump-qcserverless4-20250812/gl-main.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.gl_main__recid_seq', (SELECT MAX(_recid) FROM qcauto.gl_main));
\echo Finish Table gl_main 
\echo . 
\echo Loading Table golf_caddie 
\copy qcauto.golf_caddie from '/usr1/dump-qcserverless4-20250812/golf-caddie.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_caddie__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_caddie));
\echo Finish Table golf_caddie 
\echo . 
\echo Loading Table golf_caddie_assignment 
\copy qcauto.golf_caddie_assignment from '/usr1/dump-qcserverless4-20250812/golf-caddie-assignment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_caddie_assignment__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_caddie_assignment));
\echo Finish Table golf_caddie_assignment 
\echo . 
\echo Loading Table golf_course 
\copy qcauto.golf_course from '/usr1/dump-qcserverless4-20250812/golf-course.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_course__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_course));
\echo Finish Table golf_course 
\echo . 
\echo Loading Table golf_flight_reservation 
\copy qcauto.golf_flight_reservation from '/usr1/dump-qcserverless4-20250812/golf-flight-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_flight_reservation__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_flight_reservation));
\echo Finish Table golf_flight_reservation 
\echo . 
\echo Loading Table golf_flight_reservation_hist 
\copy qcauto.golf_flight_reservation_hist from '/usr1/dump-qcserverless4-20250812/golf-flight-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_flight_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_flight_reservation_hist));
\echo Finish Table golf_flight_reservation_hist 
\echo . 
\echo Loading Table golf_golfer_reservation 
\copy qcauto.golf_golfer_reservation from '/usr1/dump-qcserverless4-20250812/golf-golfer-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_golfer_reservation__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_golfer_reservation));
\echo Finish Table golf_golfer_reservation 
\echo . 
\echo Loading Table golf_golfer_reservation_hist 
\copy qcauto.golf_golfer_reservation_hist from '/usr1/dump-qcserverless4-20250812/golf-golfer-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_golfer_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_golfer_reservation_hist));
\echo Finish Table golf_golfer_reservation_hist 
\echo . 
\echo Loading Table golf_holiday 
\copy qcauto.golf_holiday from '/usr1/dump-qcserverless4-20250812/golf-holiday.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_holiday__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_holiday));
\echo Finish Table golf_holiday 
\echo . 
\echo Loading Table golf_main_reservation 
\copy qcauto.golf_main_reservation from '/usr1/dump-qcserverless4-20250812/golf-main-reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_main_reservation__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_main_reservation));
\echo Finish Table golf_main_reservation 
\echo . 
\echo Loading Table golf_main_reservation_hist 
\copy qcauto.golf_main_reservation_hist from '/usr1/dump-qcserverless4-20250812/golf-main-reservation-hist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_main_reservation_hist__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_main_reservation_hist));
\echo Finish Table golf_main_reservation_hist 
\echo . 
\echo Loading Table golf_rate 
\copy qcauto.golf_rate from '/usr1/dump-qcserverless4-20250812/golf-rate.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_rate__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_rate));
\echo Finish Table golf_rate 
\echo . 
\echo Loading Table golf_shift 
\copy qcauto.golf_shift from '/usr1/dump-qcserverless4-20250812/golf-shift.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_shift__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_shift));
\echo Finish Table golf_shift 
\echo . 
\echo Loading Table golf_transfer 
\copy qcauto.golf_transfer from '/usr1/dump-qcserverless4-20250812/golf-transfer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.golf_transfer__recid_seq', (SELECT MAX(_recid) FROM qcauto.golf_transfer));
\echo Finish Table golf_transfer 
\echo . 
\echo Loading Table guest 
\copy qcauto.guest from '/usr1/dump-qcserverless4-20250812/guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guest__recid_seq', (SELECT MAX(_recid) FROM qcauto.guest));
update qcauto.guest set notizen = array_replace(notizen,NULL,''); 
update qcauto.guest set vornamekind = array_replace(vornamekind,NULL,''); 
\echo Finish Table guest 
\echo . 
\echo Loading Table guest_pr 
\copy qcauto.guest_pr from '/usr1/dump-qcserverless4-20250812/guest-pr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guest_pr__recid_seq', (SELECT MAX(_recid) FROM qcauto.guest_pr));
\echo Finish Table guest_pr 
\echo . 
\echo Loading Table guest_queasy 
\copy qcauto.guest_queasy from '/usr1/dump-qcserverless4-20250812/guest-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guest_queasy__recid_seq', (SELECT MAX(_recid) FROM qcauto.guest_queasy));
\echo Finish Table guest_queasy 
\echo . 
\echo Loading Table guest_remark 
\copy qcauto.guest_remark from '/usr1/dump-qcserverless4-20250812/guest-remark.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guest_remark__recid_seq', (SELECT MAX(_recid) FROM qcauto.guest_remark));
update qcauto.guest_remark set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table guest_remark 
\echo . 
\echo Loading Table guestat 
\copy qcauto.guestat from '/usr1/dump-qcserverless4-20250812/guestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guestat__recid_seq', (SELECT MAX(_recid) FROM qcauto.guestat));
\echo Finish Table guestat 
\echo . 
\echo Loading Table guestat1 
\copy qcauto.guestat1 from '/usr1/dump-qcserverless4-20250812/guestat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guestat1__recid_seq', (SELECT MAX(_recid) FROM qcauto.guestat1));
\echo Finish Table guestat1 
\echo . 
\echo Loading Table guestbook 
\copy qcauto.guestbook from '/usr1/dump-qcserverless4-20250812/guestbook.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guestbook__recid_seq', (SELECT MAX(_recid) FROM qcauto.guestbook));
update qcauto.guestbook set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table guestbook 
\echo . 
\echo Loading Table guestbud 
\copy qcauto.guestbud from '/usr1/dump-qcserverless4-20250812/guestbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guestbud__recid_seq', (SELECT MAX(_recid) FROM qcauto.guestbud));
\echo Finish Table guestbud 
\echo . 
\echo Loading Table guestseg 
\copy qcauto.guestseg from '/usr1/dump-qcserverless4-20250812/guestseg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.guestseg__recid_seq', (SELECT MAX(_recid) FROM qcauto.guestseg));
\echo Finish Table guestseg 
\echo . 
\echo Loading Table h_artcost 
\copy qcauto.h_artcost from '/usr1/dump-qcserverless4-20250812/h-artcost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_artcost__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_artcost));
\echo Finish Table h_artcost 
\echo . 
\echo Loading Table h_artikel 
\copy qcauto.h_artikel from '/usr1/dump-qcserverless4-20250812/h-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_artikel__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_artikel));
\echo Finish Table h_artikel 
\echo . 
\echo Loading Table h_bill 
\copy qcauto.h_bill from '/usr1/dump-qcserverless4-20250812/h-bill.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_bill__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_bill));
\echo Finish Table h_bill 
\echo . 
\echo Loading Table h_bill_line 
\copy qcauto.h_bill_line from '/usr1/dump-qcserverless4-20250812/h-bill-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_bill_line__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_bill_line));
\echo Finish Table h_bill_line 
\echo . 
\echo Loading Table h_compli 
\copy qcauto.h_compli from '/usr1/dump-qcserverless4-20250812/h-compli.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_compli__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_compli));
\echo Finish Table h_compli 
\echo . 
\echo Loading Table h_cost 
\copy qcauto.h_cost from '/usr1/dump-qcserverless4-20250812/h-cost.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_cost__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_cost));
\echo Finish Table h_cost 
\echo . 
\echo Loading Table h_journal 
\copy qcauto.h_journal from '/usr1/dump-qcserverless4-20250812/h-journal.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_journal__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_journal));
\echo Finish Table h_journal 
\echo . 
\echo Loading Table h_menu 
\copy qcauto.h_menu from '/usr1/dump-qcserverless4-20250812/h-menu.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_menu__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_menu));
\echo Finish Table h_menu 
\echo . 
\echo Loading Table h_mjourn 
\copy qcauto.h_mjourn from '/usr1/dump-qcserverless4-20250812/h-mjourn.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_mjourn__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_mjourn));
\echo Finish Table h_mjourn 
\echo . 
\echo Loading Table h_oldjou 
\copy qcauto.h_oldjou from '/usr1/dump-qcserverless4-20250812/h-oldjou.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_oldjou__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_oldjou));
\echo Finish Table h_oldjou 
\echo . 
\echo Loading Table h_order 
\copy qcauto.h_order from '/usr1/dump-qcserverless4-20250812/h-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_order__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_order));
update qcauto.h_order set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table h_order 
\echo . 
\echo Loading Table h_queasy 
\copy qcauto.h_queasy from '/usr1/dump-qcserverless4-20250812/h-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_queasy__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_queasy));
\echo Finish Table h_queasy 
\echo . 
\echo Loading Table h_rezept 
\copy qcauto.h_rezept from '/usr1/dump-qcserverless4-20250812/h-rezept.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_rezept__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_rezept));
\echo Finish Table h_rezept 
\echo . 
\echo Loading Table h_rezlin 
\copy qcauto.h_rezlin from '/usr1/dump-qcserverless4-20250812/h-rezlin.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_rezlin__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_rezlin));
\echo Finish Table h_rezlin 
\echo . 
\echo Loading Table h_storno 
\copy qcauto.h_storno from '/usr1/dump-qcserverless4-20250812/h-storno.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_storno__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_storno));
\echo Finish Table h_storno 
\echo . 
\echo Loading Table h_umsatz 
\copy qcauto.h_umsatz from '/usr1/dump-qcserverless4-20250812/h-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.h_umsatz__recid_seq', (SELECT MAX(_recid) FROM qcauto.h_umsatz));
\echo Finish Table h_umsatz 
\echo . 
\echo Loading Table history 
\copy qcauto.history from '/usr1/dump-qcserverless4-20250812/history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.history__recid_seq', (SELECT MAX(_recid) FROM qcauto.history));
\echo Finish Table history 
\echo . 
\echo Loading Table hoteldpt 
\copy qcauto.hoteldpt from '/usr1/dump-qcserverless4-20250812/hoteldpt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.hoteldpt__recid_seq', (SELECT MAX(_recid) FROM qcauto.hoteldpt));
\echo Finish Table hoteldpt 
\echo . 
\echo Loading Table hrbeleg 
\copy qcauto.hrbeleg from '/usr1/dump-qcserverless4-20250812/hrbeleg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.hrbeleg__recid_seq', (SELECT MAX(_recid) FROM qcauto.hrbeleg));
\echo Finish Table hrbeleg 
\echo . 
\echo Loading Table hrsegement 
\copy qcauto.hrsegement from '/usr1/dump-qcserverless4-20250812/hrsegement.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.hrsegement__recid_seq', (SELECT MAX(_recid) FROM qcauto.hrsegement));
\echo Finish Table hrsegement 
\echo . 
\echo Loading Table htparam 
\copy qcauto.htparam from '/usr1/dump-qcserverless4-20250812/htparam.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.htparam__recid_seq', (SELECT MAX(_recid) FROM qcauto.htparam));
\echo Finish Table htparam 
\echo . 
\echo Loading Table htreport 
\copy qcauto.htreport from '/usr1/dump-qcserverless4-20250812/htreport.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.htreport__recid_seq', (SELECT MAX(_recid) FROM qcauto.htreport));
\echo Finish Table htreport 
\echo . 
\echo Loading Table iftable 
\copy qcauto.iftable from '/usr1/dump-qcserverless4-20250812/iftable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.iftable__recid_seq', (SELECT MAX(_recid) FROM qcauto.iftable));
\echo Finish Table iftable 
\echo . 
\echo Loading Table interface 
\copy qcauto.interface from '/usr1/dump-qcserverless4-20250812/interface.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.interface__recid_seq', (SELECT MAX(_recid) FROM qcauto.interface));
\echo Finish Table interface 
\echo . 
\echo Loading Table k_history 
\copy qcauto.k_history from '/usr1/dump-qcserverless4-20250812/k-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.k_history__recid_seq', (SELECT MAX(_recid) FROM qcauto.k_history));
\echo Finish Table k_history 
\echo . 
\echo Loading Table kabine 
\copy qcauto.kabine from '/usr1/dump-qcserverless4-20250812/kabine.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kabine__recid_seq', (SELECT MAX(_recid) FROM qcauto.kabine));
\echo Finish Table kabine 
\echo . 
\echo Loading Table kalender 
\copy qcauto.kalender from '/usr1/dump-qcserverless4-20250812/kalender.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kalender__recid_seq', (SELECT MAX(_recid) FROM qcauto.kalender));
update qcauto.kalender set note = array_replace(note,NULL,''); 
\echo Finish Table kalender 
\echo . 
\echo Loading Table kasse 
\copy qcauto.kasse from '/usr1/dump-qcserverless4-20250812/kasse.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kasse__recid_seq', (SELECT MAX(_recid) FROM qcauto.kasse));
\echo Finish Table kasse 
\echo . 
\echo Loading Table katpreis 
\copy qcauto.katpreis from '/usr1/dump-qcserverless4-20250812/katpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.katpreis__recid_seq', (SELECT MAX(_recid) FROM qcauto.katpreis));
\echo Finish Table katpreis 
\echo . 
\echo Loading Table kellne1 
\copy qcauto.kellne1 from '/usr1/dump-qcserverless4-20250812/kellne1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kellne1__recid_seq', (SELECT MAX(_recid) FROM qcauto.kellne1));
\echo Finish Table kellne1 
\echo . 
\echo Loading Table kellner 
\copy qcauto.kellner from '/usr1/dump-qcserverless4-20250812/kellner.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kellner__recid_seq', (SELECT MAX(_recid) FROM qcauto.kellner));
\echo Finish Table kellner 
\echo . 
\echo Loading Table kontakt 
\copy qcauto.kontakt from '/usr1/dump-qcserverless4-20250812/kontakt.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kontakt__recid_seq', (SELECT MAX(_recid) FROM qcauto.kontakt));
\echo Finish Table kontakt 
\echo . 
\echo Loading Table kontline 
\copy qcauto.kontline from '/usr1/dump-qcserverless4-20250812/kontline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kontline__recid_seq', (SELECT MAX(_recid) FROM qcauto.kontline));
\echo Finish Table kontline 
\echo . 
\echo Loading Table kontlink 
\copy qcauto.kontlink from '/usr1/dump-qcserverless4-20250812/kontlink.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kontlink__recid_seq', (SELECT MAX(_recid) FROM qcauto.kontlink));
\echo Finish Table kontlink 
\echo . 
\echo Loading Table kontplan 
\copy qcauto.kontplan from '/usr1/dump-qcserverless4-20250812/kontplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kontplan__recid_seq', (SELECT MAX(_recid) FROM qcauto.kontplan));
\echo Finish Table kontplan 
\echo . 
\echo Loading Table kontstat 
\copy qcauto.kontstat from '/usr1/dump-qcserverless4-20250812/kontstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kontstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.kontstat));
update qcauto.kontstat set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table kontstat 
\echo . 
\echo Loading Table kresline 
\copy qcauto.kresline from '/usr1/dump-qcserverless4-20250812/kresline.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.kresline__recid_seq', (SELECT MAX(_recid) FROM qcauto.kresline));
\echo Finish Table kresline 
\echo . 
\echo Loading Table l_artikel 
\copy qcauto.l_artikel from '/usr1/dump-qcserverless4-20250812/l-artikel.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_artikel__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_artikel));
update qcauto.l_artikel set lief_artnr = array_replace(lief_artnr,NULL,''); 
\echo Finish Table l_artikel 
\echo . 
\echo Loading Table l_bestand 
\copy qcauto.l_bestand from '/usr1/dump-qcserverless4-20250812/l-bestand.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_bestand__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_bestand));
\echo Finish Table l_bestand 
\echo . 
\echo Loading Table l_besthis 
\copy qcauto.l_besthis from '/usr1/dump-qcserverless4-20250812/l-besthis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_besthis__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_besthis));
\echo Finish Table l_besthis 
\echo . 
\echo Loading Table l_hauptgrp 
\copy qcauto.l_hauptgrp from '/usr1/dump-qcserverless4-20250812/l-hauptgrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_hauptgrp__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_hauptgrp));
\echo Finish Table l_hauptgrp 
\echo . 
\echo Loading Table l_kredit 
\copy qcauto.l_kredit from '/usr1/dump-qcserverless4-20250812/l-kredit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_kredit__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_kredit));
\echo Finish Table l_kredit 
\echo . 
\echo Loading Table l_lager 
\copy qcauto.l_lager from '/usr1/dump-qcserverless4-20250812/l-lager.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_lager__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_lager));
\echo Finish Table l_lager 
\echo . 
\echo Loading Table l_lieferant 
\copy qcauto.l_lieferant from '/usr1/dump-qcserverless4-20250812/l-lieferant.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_lieferant__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_lieferant));
update qcauto.l_lieferant set notizen = array_replace(notizen,NULL,''); 
\echo Finish Table l_lieferant 
\echo . 
\echo Loading Table l_liefumsatz 
\copy qcauto.l_liefumsatz from '/usr1/dump-qcserverless4-20250812/l-liefumsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_liefumsatz__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_liefumsatz));
\echo Finish Table l_liefumsatz 
\echo . 
\echo Loading Table l_op 
\copy qcauto.l_op from '/usr1/dump-qcserverless4-20250812/l-op.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_op__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_op));
\echo Finish Table l_op 
\echo . 
\echo Loading Table l_ophdr 
\copy qcauto.l_ophdr from '/usr1/dump-qcserverless4-20250812/l-ophdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_ophdr__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_ophdr));
\echo Finish Table l_ophdr 
\echo . 
\echo Loading Table l_ophhis 
\copy qcauto.l_ophhis from '/usr1/dump-qcserverless4-20250812/l-ophhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_ophhis__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_ophhis));
\echo Finish Table l_ophhis 
\echo . 
\echo Loading Table l_ophis 
\copy qcauto.l_ophis from '/usr1/dump-qcserverless4-20250812/l-ophis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_ophis__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_ophis));
\echo Finish Table l_ophis 
\echo . 
\echo Loading Table l_order 
\copy qcauto.l_order from '/usr1/dump-qcserverless4-20250812/l-order.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_order__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_order));
update qcauto.l_order set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_order 
\echo . 
\echo Loading Table l_orderhdr 
\copy qcauto.l_orderhdr from '/usr1/dump-qcserverless4-20250812/l-orderhdr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_orderhdr__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_orderhdr));
update qcauto.l_orderhdr set lief_fax = array_replace(lief_fax,NULL,''); 
\echo Finish Table l_orderhdr 
\echo . 
\echo Loading Table l_pprice 
\copy qcauto.l_pprice from '/usr1/dump-qcserverless4-20250812/l-pprice.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_pprice__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_pprice));
\echo Finish Table l_pprice 
\echo . 
\echo Loading Table l_quote 
\copy qcauto.l_quote from '/usr1/dump-qcserverless4-20250812/l-quote.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_quote__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_quote));
update qcauto.l_quote set reserve_char = array_replace(reserve_char,NULL,''); 
\echo Finish Table l_quote 
\echo . 
\echo Loading Table l_segment 
\copy qcauto.l_segment from '/usr1/dump-qcserverless4-20250812/l-segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_segment__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_segment));
\echo Finish Table l_segment 
\echo . 
\echo Loading Table l_umsatz 
\copy qcauto.l_umsatz from '/usr1/dump-qcserverless4-20250812/l-umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_umsatz__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_umsatz));
\echo Finish Table l_umsatz 
\echo . 
\echo Loading Table l_untergrup 
\copy qcauto.l_untergrup from '/usr1/dump-qcserverless4-20250812/l-untergrup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_untergrup__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_untergrup));
\echo Finish Table l_untergrup 
\echo . 
\echo Loading Table l_verbrauch 
\copy qcauto.l_verbrauch from '/usr1/dump-qcserverless4-20250812/l-verbrauch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_verbrauch__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_verbrauch));
\echo Finish Table l_verbrauch 
\echo . 
\echo Loading Table l_zahlbed 
\copy qcauto.l_zahlbed from '/usr1/dump-qcserverless4-20250812/l-zahlbed.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.l_zahlbed__recid_seq', (SELECT MAX(_recid) FROM qcauto.l_zahlbed));
\echo Finish Table l_zahlbed 
\echo . 
\echo Loading Table landstat 
\copy qcauto.landstat from '/usr1/dump-qcserverless4-20250812/landstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.landstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.landstat));
\echo Finish Table landstat 
\echo . 
\echo Loading Table masseur 
\copy qcauto.masseur from '/usr1/dump-qcserverless4-20250812/masseur.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.masseur__recid_seq', (SELECT MAX(_recid) FROM qcauto.masseur));
\echo Finish Table masseur 
\echo . 
\echo Loading Table mast_art 
\copy qcauto.mast_art from '/usr1/dump-qcserverless4-20250812/mast-art.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mast_art__recid_seq', (SELECT MAX(_recid) FROM qcauto.mast_art));
\echo Finish Table mast_art 
\echo . 
\echo Loading Table master 
\copy qcauto.master from '/usr1/dump-qcserverless4-20250812/master.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.master__recid_seq', (SELECT MAX(_recid) FROM qcauto.master));
\echo Finish Table master 
\echo . 
\echo Loading Table mathis 
\copy qcauto.mathis from '/usr1/dump-qcserverless4-20250812/mathis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mathis__recid_seq', (SELECT MAX(_recid) FROM qcauto.mathis));
\echo Finish Table mathis 
\echo . 
\echo Loading Table mc_aclub 
\copy qcauto.mc_aclub from '/usr1/dump-qcserverless4-20250812/mc-aclub.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mc_aclub__recid_seq', (SELECT MAX(_recid) FROM qcauto.mc_aclub));
\echo Finish Table mc_aclub 
\echo . 
\echo Loading Table mc_cardhis 
\copy qcauto.mc_cardhis from '/usr1/dump-qcserverless4-20250812/mc-cardhis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mc_cardhis__recid_seq', (SELECT MAX(_recid) FROM qcauto.mc_cardhis));
\echo Finish Table mc_cardhis 
\echo . 
\echo Loading Table mc_disc 
\copy qcauto.mc_disc from '/usr1/dump-qcserverless4-20250812/mc-disc.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mc_disc__recid_seq', (SELECT MAX(_recid) FROM qcauto.mc_disc));
\echo Finish Table mc_disc 
\echo . 
\echo Loading Table mc_fee 
\copy qcauto.mc_fee from '/usr1/dump-qcserverless4-20250812/mc-fee.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mc_fee__recid_seq', (SELECT MAX(_recid) FROM qcauto.mc_fee));
\echo Finish Table mc_fee 
\echo . 
\echo Loading Table mc_guest 
\copy qcauto.mc_guest from '/usr1/dump-qcserverless4-20250812/mc-guest.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mc_guest__recid_seq', (SELECT MAX(_recid) FROM qcauto.mc_guest));
\echo Finish Table mc_guest 
\echo . 
\echo Loading Table mc_types 
\copy qcauto.mc_types from '/usr1/dump-qcserverless4-20250812/mc-types.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mc_types__recid_seq', (SELECT MAX(_recid) FROM qcauto.mc_types));
\echo Finish Table mc_types 
\echo . 
\echo Loading Table mealcoup 
\copy qcauto.mealcoup from '/usr1/dump-qcserverless4-20250812/mealcoup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mealcoup__recid_seq', (SELECT MAX(_recid) FROM qcauto.mealcoup));
\echo Finish Table mealcoup 
\echo . 
\echo Loading Table messages 
\copy qcauto.messages from '/usr1/dump-qcserverless4-20250812/messages.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.messages__recid_seq', (SELECT MAX(_recid) FROM qcauto.messages));
update qcauto.messages set messtext = array_replace(messtext,NULL,''); 
\echo Finish Table messages 
\echo . 
\echo Loading Table messe 
\copy qcauto.messe from '/usr1/dump-qcserverless4-20250812/messe.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.messe__recid_seq', (SELECT MAX(_recid) FROM qcauto.messe));
\echo Finish Table messe 
\echo . 
\echo Loading Table mhis_line 
\copy qcauto.mhis_line from '/usr1/dump-qcserverless4-20250812/mhis-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.mhis_line__recid_seq', (SELECT MAX(_recid) FROM qcauto.mhis_line));
\echo Finish Table mhis_line 
\echo . 
\echo Loading Table nation 
\copy qcauto.nation from '/usr1/dump-qcserverless4-20250812/nation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.nation__recid_seq', (SELECT MAX(_recid) FROM qcauto.nation));
\echo Finish Table nation 
\echo . 
\echo Loading Table nationstat 
\copy qcauto.nationstat from '/usr1/dump-qcserverless4-20250812/nationstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.nationstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.nationstat));
\echo Finish Table nationstat 
\echo . 
\echo Loading Table natstat1 
\copy qcauto.natstat1 from '/usr1/dump-qcserverless4-20250812/natstat1.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.natstat1__recid_seq', (SELECT MAX(_recid) FROM qcauto.natstat1));
\echo Finish Table natstat1 
\echo . 
\echo Loading Table nebenst 
\copy qcauto.nebenst from '/usr1/dump-qcserverless4-20250812/nebenst.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.nebenst__recid_seq', (SELECT MAX(_recid) FROM qcauto.nebenst));
\echo Finish Table nebenst 
\echo . 
\echo Loading Table nightaudit 
\copy qcauto.nightaudit from '/usr1/dump-qcserverless4-20250812/nightaudit.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.nightaudit__recid_seq', (SELECT MAX(_recid) FROM qcauto.nightaudit));
\echo Finish Table nightaudit 
\echo . 
\echo Loading Table nitehist 
\copy qcauto.nitehist from '/usr1/dump-qcserverless4-20250812/nitehist.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.nitehist__recid_seq', (SELECT MAX(_recid) FROM qcauto.nitehist));
\echo Finish Table nitehist 
\echo . 
\echo Loading Table nitestor 
\copy qcauto.nitestor from '/usr1/dump-qcserverless4-20250812/nitestor.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.nitestor__recid_seq', (SELECT MAX(_recid) FROM qcauto.nitestor));
\echo Finish Table nitestor 
\echo . 
\echo Loading Table notes 
\copy qcauto.notes from '/usr1/dump-qcserverless4-20250812/notes.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.notes__recid_seq', (SELECT MAX(_recid) FROM qcauto.notes));
update qcauto.notes set note = array_replace(note,NULL,''); 
\echo Finish Table notes 
\echo . 
\echo Loading Table outorder 
\copy qcauto.outorder from '/usr1/dump-qcserverless4-20250812/outorder.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.outorder__recid_seq', (SELECT MAX(_recid) FROM qcauto.outorder));
\echo Finish Table outorder 
\echo . 
\echo Loading Table package 
\copy qcauto.package from '/usr1/dump-qcserverless4-20250812/package.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.package__recid_seq', (SELECT MAX(_recid) FROM qcauto.package));
\echo Finish Table package 
\echo . 
\echo Loading Table parameters 
\copy qcauto.parameters from '/usr1/dump-qcserverless4-20250812/parameters.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.parameters__recid_seq', (SELECT MAX(_recid) FROM qcauto.parameters));
\echo Finish Table parameters 
\echo . 
\echo Loading Table paramtext 
\copy qcauto.paramtext from '/usr1/dump-qcserverless4-20250812/paramtext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.paramtext__recid_seq', (SELECT MAX(_recid) FROM qcauto.paramtext));
\echo Finish Table paramtext 
\echo . 
\echo Loading Table pricecod 
\copy qcauto.pricecod from '/usr1/dump-qcserverless4-20250812/pricecod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.pricecod__recid_seq', (SELECT MAX(_recid) FROM qcauto.pricecod));
\echo Finish Table pricecod 
\echo . 
\echo Loading Table pricegrp 
\copy qcauto.pricegrp from '/usr1/dump-qcserverless4-20250812/pricegrp.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.pricegrp__recid_seq', (SELECT MAX(_recid) FROM qcauto.pricegrp));
\echo Finish Table pricegrp 
\echo . 
\echo Loading Table printcod 
\copy qcauto.printcod from '/usr1/dump-qcserverless4-20250812/printcod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.printcod__recid_seq', (SELECT MAX(_recid) FROM qcauto.printcod));
\echo Finish Table printcod 
\echo . 
\echo Loading Table printer 
\copy qcauto.printer from '/usr1/dump-qcserverless4-20250812/printer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.printer__recid_seq', (SELECT MAX(_recid) FROM qcauto.printer));
\echo Finish Table printer 
\echo . 
\echo Loading Table prmarket 
\copy qcauto.prmarket from '/usr1/dump-qcserverless4-20250812/prmarket.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.prmarket__recid_seq', (SELECT MAX(_recid) FROM qcauto.prmarket));
\echo Finish Table prmarket 
\echo . 
\echo Loading Table progcat 
\copy qcauto.progcat from '/usr1/dump-qcserverless4-20250812/progcat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.progcat__recid_seq', (SELECT MAX(_recid) FROM qcauto.progcat));
\echo Finish Table progcat 
\echo . 
\echo Loading Table progfile 
\copy qcauto.progfile from '/usr1/dump-qcserverless4-20250812/progfile.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.progfile__recid_seq', (SELECT MAX(_recid) FROM qcauto.progfile));
\echo Finish Table progfile 
\echo . 
\echo Loading Table prtable 
\copy qcauto.prtable from '/usr1/dump-qcserverless4-20250812/prtable.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.prtable__recid_seq', (SELECT MAX(_recid) FROM qcauto.prtable));
\echo Finish Table prtable 
\echo . 
\echo Loading Table queasy 
\copy qcauto.queasy from '/usr1/dump-qcserverless4-20250812/queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.queasy__recid_seq', (SELECT MAX(_recid) FROM qcauto.queasy));
\echo Finish Table queasy 
\echo . 
\echo Loading Table ratecode 
\copy qcauto.ratecode from '/usr1/dump-qcserverless4-20250812/ratecode.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.ratecode__recid_seq', (SELECT MAX(_recid) FROM qcauto.ratecode));
update qcauto.ratecode set char1 = array_replace(char1,NULL,''); 
\echo Finish Table ratecode 
\echo . 
\echo Loading Table raum 
\copy qcauto.raum from '/usr1/dump-qcserverless4-20250812/raum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.raum__recid_seq', (SELECT MAX(_recid) FROM qcauto.raum));
\echo Finish Table raum 
\echo . 
\echo Loading Table res_history 
\copy qcauto.res_history from '/usr1/dump-qcserverless4-20250812/res-history.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.res_history__recid_seq', (SELECT MAX(_recid) FROM qcauto.res_history));
\echo Finish Table res_history 
\echo . 
\echo Loading Table res_line 
\copy qcauto.res_line from '/usr1/dump-qcserverless4-20250812/res-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.res_line__recid_seq', (SELECT MAX(_recid) FROM qcauto.res_line));
\echo Finish Table res_line 
\echo . 
\echo Loading Table reservation 
\copy qcauto.reservation from '/usr1/dump-qcserverless4-20250812/reservation.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.reservation__recid_seq', (SELECT MAX(_recid) FROM qcauto.reservation));
\echo Finish Table reservation 
\echo . 
\echo Loading Table reslin_queasy 
\copy qcauto.reslin_queasy from '/usr1/dump-qcserverless4-20250812/reslin-queasy.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.reslin_queasy__recid_seq', (SELECT MAX(_recid) FROM qcauto.reslin_queasy));
\echo Finish Table reslin_queasy 
\echo . 
\echo Loading Table resplan 
\copy qcauto.resplan from '/usr1/dump-qcserverless4-20250812/resplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.resplan__recid_seq', (SELECT MAX(_recid) FROM qcauto.resplan));
\echo Finish Table resplan 
\echo . 
\echo Loading Table rg_reports 
\copy qcauto.rg_reports from '/usr1/dump-qcserverless4-20250812/rg-reports.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.rg_reports__recid_seq', (SELECT MAX(_recid) FROM qcauto.rg_reports));
update qcauto.rg_reports set metadata = array_replace(metadata,NULL,''); 
update qcauto.rg_reports set slice_name = array_replace(slice_name,NULL,''); 
update qcauto.rg_reports set view_name = array_replace(view_name,NULL,''); 
\echo Finish Table rg_reports 
\echo . 
\echo Loading Table rmbudget 
\copy qcauto.rmbudget from '/usr1/dump-qcserverless4-20250812/rmbudget.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.rmbudget__recid_seq', (SELECT MAX(_recid) FROM qcauto.rmbudget));
update qcauto.rmbudget set res_char = array_replace(res_char,NULL,''); 
\echo Finish Table rmbudget 
\echo . 
\echo Loading Table sales 
\copy qcauto.sales from '/usr1/dump-qcserverless4-20250812/sales.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sales__recid_seq', (SELECT MAX(_recid) FROM qcauto.sales));
\echo Finish Table sales 
\echo . 
\echo Loading Table salesbud 
\copy qcauto.salesbud from '/usr1/dump-qcserverless4-20250812/salesbud.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.salesbud__recid_seq', (SELECT MAX(_recid) FROM qcauto.salesbud));
\echo Finish Table salesbud 
\echo . 
\echo Loading Table salestat 
\copy qcauto.salestat from '/usr1/dump-qcserverless4-20250812/salestat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.salestat__recid_seq', (SELECT MAX(_recid) FROM qcauto.salestat));
\echo Finish Table salestat 
\echo . 
\echo Loading Table salestim 
\copy qcauto.salestim from '/usr1/dump-qcserverless4-20250812/salestim.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.salestim__recid_seq', (SELECT MAX(_recid) FROM qcauto.salestim));
\echo Finish Table salestim 
\echo . 
\echo Loading Table segment 
\copy qcauto.segment from '/usr1/dump-qcserverless4-20250812/segment.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.segment__recid_seq', (SELECT MAX(_recid) FROM qcauto.segment));
\echo Finish Table segment 
\echo . 
\echo Loading Table segmentstat 
\copy qcauto.segmentstat from '/usr1/dump-qcserverless4-20250812/segmentstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.segmentstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.segmentstat));
\echo Finish Table segmentstat 
\echo . 
\echo Loading Table sms_bcaster 
\copy qcauto.sms_bcaster from '/usr1/dump-qcserverless4-20250812/sms-bcaster.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sms_bcaster__recid_seq', (SELECT MAX(_recid) FROM qcauto.sms_bcaster));
\echo Finish Table sms_bcaster 
\echo . 
\echo Loading Table sms_broadcast 
\copy qcauto.sms_broadcast from '/usr1/dump-qcserverless4-20250812/sms-broadcast.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sms_broadcast__recid_seq', (SELECT MAX(_recid) FROM qcauto.sms_broadcast));
\echo Finish Table sms_broadcast 
\echo . 
\echo Loading Table sms_group 
\copy qcauto.sms_group from '/usr1/dump-qcserverless4-20250812/sms-group.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sms_group__recid_seq', (SELECT MAX(_recid) FROM qcauto.sms_group));
\echo Finish Table sms_group 
\echo . 
\echo Loading Table sms_groupmbr 
\copy qcauto.sms_groupmbr from '/usr1/dump-qcserverless4-20250812/sms-groupmbr.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sms_groupmbr__recid_seq', (SELECT MAX(_recid) FROM qcauto.sms_groupmbr));
\echo Finish Table sms_groupmbr 
\echo . 
\echo Loading Table sms_received 
\copy qcauto.sms_received from '/usr1/dump-qcserverless4-20250812/sms-received.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sms_received__recid_seq', (SELECT MAX(_recid) FROM qcauto.sms_received));
\echo Finish Table sms_received 
\echo . 
\echo Loading Table sourccod 
\copy qcauto.sourccod from '/usr1/dump-qcserverless4-20250812/Sourccod.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sourccod__recid_seq', (SELECT MAX(_recid) FROM qcauto.sourccod));
\echo Finish Table sourccod 
\echo . 
\echo Loading Table sources 
\copy qcauto.sources from '/usr1/dump-qcserverless4-20250812/sources.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sources__recid_seq', (SELECT MAX(_recid) FROM qcauto.sources));
\echo Finish Table sources 
\echo . 
\echo Loading Table sourcetext 
\copy qcauto.sourcetext from '/usr1/dump-qcserverless4-20250812/sourcetext.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.sourcetext__recid_seq', (SELECT MAX(_recid) FROM qcauto.sourcetext));
\echo Finish Table sourcetext 
\echo . 
\echo Loading Table telephone 
\copy qcauto.telephone from '/usr1/dump-qcserverless4-20250812/telephone.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.telephone__recid_seq', (SELECT MAX(_recid) FROM qcauto.telephone));
\echo Finish Table telephone 
\echo . 
\echo Loading Table texte 
\copy qcauto.texte from '/usr1/dump-qcserverless4-20250812/texte.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.texte__recid_seq', (SELECT MAX(_recid) FROM qcauto.texte));
\echo Finish Table texte 
\echo . 
\echo Loading Table tisch 
\copy qcauto.tisch from '/usr1/dump-qcserverless4-20250812/tisch.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.tisch__recid_seq', (SELECT MAX(_recid) FROM qcauto.tisch));
\echo Finish Table tisch 
\echo . 
\echo Loading Table tisch_res 
\copy qcauto.tisch_res from '/usr1/dump-qcserverless4-20250812/tisch-res.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.tisch_res__recid_seq', (SELECT MAX(_recid) FROM qcauto.tisch_res));
\echo Finish Table tisch_res 
\echo . 
\echo Loading Table uebertrag 
\copy qcauto.uebertrag from '/usr1/dump-qcserverless4-20250812/uebertrag.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.uebertrag__recid_seq', (SELECT MAX(_recid) FROM qcauto.uebertrag));
\echo Finish Table uebertrag 
\echo . 
\echo Loading Table umsatz 
\copy qcauto.umsatz from '/usr1/dump-qcserverless4-20250812/umsatz.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.umsatz__recid_seq', (SELECT MAX(_recid) FROM qcauto.umsatz));
\echo Finish Table umsatz 
\echo . 
\echo Loading Table waehrung 
\copy qcauto.waehrung from '/usr1/dump-qcserverless4-20250812/waehrung.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.waehrung__recid_seq', (SELECT MAX(_recid) FROM qcauto.waehrung));
\echo Finish Table waehrung 
\echo . 
\echo Loading Table wakeup 
\copy qcauto.wakeup from '/usr1/dump-qcserverless4-20250812/wakeup.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.wakeup__recid_seq', (SELECT MAX(_recid) FROM qcauto.wakeup));
\echo Finish Table wakeup 
\echo . 
\echo Loading Table wgrpdep 
\copy qcauto.wgrpdep from '/usr1/dump-qcserverless4-20250812/wgrpdep.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.wgrpdep__recid_seq', (SELECT MAX(_recid) FROM qcauto.wgrpdep));
\echo Finish Table wgrpdep 
\echo . 
\echo Loading Table wgrpgen 
\copy qcauto.wgrpgen from '/usr1/dump-qcserverless4-20250812/wgrpgen.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.wgrpgen__recid_seq', (SELECT MAX(_recid) FROM qcauto.wgrpgen));
\echo Finish Table wgrpgen 
\echo . 
\echo Loading Table zimkateg 
\copy qcauto.zimkateg from '/usr1/dump-qcserverless4-20250812/zimkateg.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zimkateg__recid_seq', (SELECT MAX(_recid) FROM qcauto.zimkateg));
\echo Finish Table zimkateg 
\echo . 
\echo Loading Table zimmer 
\copy qcauto.zimmer from '/usr1/dump-qcserverless4-20250812/zimmer.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zimmer__recid_seq', (SELECT MAX(_recid) FROM qcauto.zimmer));
update qcauto.zimmer set verbindung = array_replace(verbindung,NULL,''); 
\echo Finish Table zimmer 
\echo . 
\echo Loading Table zimmer_book 
\copy qcauto.zimmer_book from '/usr1/dump-qcserverless4-20250812/zimmer-book.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zimmer_book__recid_seq', (SELECT MAX(_recid) FROM qcauto.zimmer_book));
\echo Finish Table zimmer_book 
\echo . 
\echo Loading Table zimmer_book_line 
\copy qcauto.zimmer_book_line from '/usr1/dump-qcserverless4-20250812/zimmer-book-line.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zimmer_book_line__recid_seq', (SELECT MAX(_recid) FROM qcauto.zimmer_book_line));
\echo Finish Table zimmer_book_line 
\echo . 
\echo Loading Table zimplan 
\copy qcauto.zimplan from '/usr1/dump-qcserverless4-20250812/zimplan.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zimplan__recid_seq', (SELECT MAX(_recid) FROM qcauto.zimplan));
\echo Finish Table zimplan 
\echo . 
\echo Loading Table zimpreis 
\copy qcauto.zimpreis from '/usr1/dump-qcserverless4-20250812/zimpreis.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zimpreis__recid_seq', (SELECT MAX(_recid) FROM qcauto.zimpreis));
\echo Finish Table zimpreis 
\echo . 
\echo Loading Table zinrstat 
\copy qcauto.zinrstat from '/usr1/dump-qcserverless4-20250812/zinrstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zinrstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.zinrstat));
\echo Finish Table zinrstat 
\echo . 
\echo Loading Table zkstat 
\copy qcauto.zkstat from '/usr1/dump-qcserverless4-20250812/zkstat.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zkstat__recid_seq', (SELECT MAX(_recid) FROM qcauto.zkstat));
\echo Finish Table zkstat 
\echo . 
\echo Loading Table zwkum 
\copy qcauto.zwkum from '/usr1/dump-qcserverless4-20250812/zwkum.csv' delimiter ',' CSV QUOTE '"' ESCAPE '''' ENCODING 'UTF8' 
SELECT setval('qcauto.zwkum__recid_seq', (SELECT MAX(_recid) FROM qcauto.zwkum));
\echo Finish Table zwkum 
\echo . 
