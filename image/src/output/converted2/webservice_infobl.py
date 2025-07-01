#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def webservice_infobl():
    webservice_info_list = []
    vhplib_version:string = ""
    tomcat_path:string = ""
    run_path:List[string] = create_empty_list(5,"")
    usr_path:List[string] = create_empty_list(5,"")
    web_version:List[string] = create_empty_list(5,"")
    run_name:List[string] = create_empty_list(5,"")
    gethtml:List[string] = create_empty_list(5,"")
    getruntime:List[string] = create_empty_list(5,"")
    loop_i:int = 0

    webservice_info = None

    webservice_info_list, Webservice_info = create_model("Webservice_info", {"vhpwebbased1":string, "vhpwebbased2":string, "vhpwebbased3":string, "vhpwebbased4":string, "vhpwebbased5":string, "vhpwebbased1_appservicename":string, "vhpwebbased2_appservicename":string, "vhpwebbased3_appservicename":string, "vhpwebbased4_appservicename":string, "vhpwebbased5_appservicename":string, "vhplibweb_version":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal webservice_info_list, vhplib_version, tomcat_path, run_path, usr_path, web_version, run_name, gethtml, getruntime, loop_i


        nonlocal webservice_info
        nonlocal webservice_info_list

        return {"webservice-info": webservice_info_list}


    vhplib_version = "v8.7.17.16"

    if SEARCH ("/usr1/tomcat/apache-tomcat-9.0.39/webapps/VHPWebBased1/index.html") != None:
        tomcat_path = "/usr1/tomcat/apache-tomcat-9.0.39"

    if SEARCH ("/usr1/tomcat/apache-tomcat-9.0.74/webapps/VHPWebBased1/index.html") != None:
        tomcat_path = "/usr1/tomcat/apache-tomcat-9.0.74"

    if SEARCH ("/usr1/tomcat/apache-tomcat-8.5.100/webapps/VHPWebBased1/index.html") != None:
        tomcat_path = "/usr1/tomcat/apache-tomcat-8.5.100"
    usr_path[0] = tomcat_path + "/webapps/VHPWebBased1/index.html"
    usr_path[1] = tomcat_path + "/webapps/VHPWebBased2/index.html"
    usr_path[2] = tomcat_path + "/webapps/VHPWebBased3/index.html"
    usr_path[3] = tomcat_path + "/webapps/VHPWebBased4/index.html"
    usr_path[4] = tomcat_path + "/webapps/VHPWebBased5/index.html"
    run_path[0] = tomcat_path + "/webapps/VHPWebBased1/WEB-INF/adapters/runtime.props"
    run_path[1] = tomcat_path + "/webapps/VHPWebBased2/WEB-INF/adapters/runtime.props"
    run_path[2] = tomcat_path + "/webapps/VHPWebBased3/WEB-INF/adapters/runtime.props"
    run_path[3] = tomcat_path + "/webapps/VHPWebBased4/WEB-INF/adapters/runtime.props"
    run_path[4] = tomcat_path + "/webapps/VHPWebBased5/WEB-INF/adapters/runtime.props"

    if usr_path[0] != "":


        if usr_path[1] != "":


            if usr_path[2] != "":


                if usr_path[3] != "":


                    if usr_path[4] != "":


                        if run_path[0] != "":


                            if run_path[1] != "":


                                if run_path[2] != "":


                                    if run_path[3] != "":


                                        if run_path[4] != "":

                                            for loop_i in range(1,5 + 1) :
                                                web_version[loop_i - 1] = to_string(substring(gethtml[loop_i - 1], 0, 1053))
                                            web_version[loop_i - 1] = to_string(substring(web_version[loop_i - 1], 976, 85))
                                            web_version[loop_i - 1] = replace_str(web_version[loop_i - 1], "<br>", "")
                                            web_version[loop_i - 1] = replace_str(web_version[loop_i - 1], "<", "")
                                            web_version[loop_i - 1] = replace_str(web_version[loop_i - 1], ">", "")
                                            web_version[loop_i - 1] = replace_str(web_version[loop_i - 1], "\\r", "")
                                            web_version[loop_i - 1] = replace_str(web_version[loop_i - 1], "\\n", "")
                                            web_version[loop_i - 1] = trim(web_version[loop_i - 1])
                                        for loop_i in range(1,5 + 1) :
                                            run_name[loop_i - 1] = to_string(substring(getruntime[loop_i - 1], 0, 904))
                                            run_name[loop_i - 1] = to_string(substring(run_name[loop_i - 1], 842, 62))
                                            run_name[loop_i - 1] = replace_str(run_name[loop_i - 1], "<", "")
                                            run_name[loop_i - 1] = replace_str(run_name[loop_i - 1], ">", "")
                                            run_name[loop_i - 1] = replace_str(run_name[loop_i - 1], "/", "")
                                            run_name[loop_i - 1] = replace_str(run_name[loop_i - 1], "bpm:appServiceName", "")
                                            run_name[loop_i - 1] = replace_str(run_name[loop_i - 1], "\\r", "")
                                            run_name[loop_i - 1] = replace_str(run_name[loop_i - 1], "\\n", "")
                                            run_name[loop_i - 1] = trim(run_name[loop_i - 1])
                                        webservice_info = Webservice_info()
                                        webservice_info_list.append(webservice_info)

                                        webservice_info.vhpwebbased1 = web_version[0]
                                        webservice_info.vhpwebbased2 = web_version[1]
                                        webservice_info.vhpwebbased3 = web_version[2]
                                        webservice_info.vhpwebbased4 = web_version[3]
                                        webservice_info.vhpwebbased5 = web_version[4]
                                        webservice_info.vhpwebbased1_appservicename = run_name[0]
                                        webservice_info.vhpwebbased2_appservicename = run_name[1]
                                        webservice_info.vhpwebbased3_appservicename = run_name[2]
                                        webservice_info.vhpwebbased4_appservicename = run_name[3]
                                        webservice_info.vhpwebbased5_appservicename = run_name[4]
                                        webservice_info.vhplibweb_version = vhplib_version

    return generate_output()