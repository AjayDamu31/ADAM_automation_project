import json

import pytest
from main import BaseClass


class TestAdam(BaseClass):

    @pytest.mark.adam
    def test_adam_api(self):
        print("restttttt")
        print(self.config.get_key_value('login')['email'])
        tok = self.api_utils.get_api_token()
        print(tok)
        url = self.url_util.get_url(self.url_util.COMPANY_LIST_OF_COMPANIES)
        print(url)
        res = self.api_utils.get_api_request(url, tok)
        print(res.json())
        self.allure_url.allure_attach_with_text("Token", str(tok))
        inspection_id = "f24fbde5-b9d3-4cc8-8adc-ce767596017d"
        inspection_url = self.url_util.INSPECTION_GET_INSPECTION.format(
            inspectionID=inspection_id)
        inspection_url = self.url_util.get_url(inspection_url)
        print(inspection_url)
        inspection_response = self.api_utils.get_api_request(inspection_url, tok)
        print(inspection_response.status_code)
        print(inspection_response.json())
        self.allure_url.allure_attach_with_text("URL", str(inspection_url))
        self.allure_url.allure_attach_with_text("Status code", str(inspection_response.status_code))
        self.allure_url.allure_attach_with_text("Message", str(inspection_response.json()))
        assert inspection_response.status_code == 200, "Status code mismatch"
        assert inspection_response.json()['id'] == inspection_id, "inspection id mismatch"
        # ----------Mysql validation -------------------------------
        inspection_query = f"select * from Inspections where ID = '{inspection_id}';"
        mysql_res = self.mysql_obj.sql_query_string(inspection_query)
        self.allure_url.allure_attach_with_text("Mysql query", str(inspection_query))
        self.allure_url.allure_attach_with_text("MySql response", str(mysql_res))
        assert mysql_res[0]['ID'] == inspection_response.json()['id'], "Inspection ID mismatch"

    @pytest.mark.adam
    # Login Test
    def test_login(self):
        tok = self.get_token()
        username = self.config.get_key_value('login')['email']
        password = self.config.get_key_value('login')['password']

        json_post_data = json.dumps({
            "email": username,
            "password": password
        })

        url = self.url_util.get_url(self.url_util.AUTH_LOGIN)
        login_response = self.api_utils.post_api_request_with_token(url, json_post_data, tok)
        print(login_response.status_code)
        print(login_response.json())
        self.allure_url.allure_attach_with_text("Login Status code", str(login_response.json()))
        assert login_response.status_code == 200, "Login Status Code mismatch"

    @pytest.mark.adam
    # List of Companies after login
    def test_list_of_companies(self):
        tok = self.get_token()
        url = self.url_util.get_url(self.url_util.COMPANY_LIST_OF_COMPANIES)
        list_of_companies_response = self.api_utils.get_api_request(url, tok)
        self.allure_url.allure_attach_with_text("Listing All Companies", str(list_of_companies_response.json()))
        print(len(list_of_companies_response.json()))
        print(list_of_companies_response.status_code)
        list_of_companies_query = "select * from Companies;"
        mysql_res = self.mysql_obj.sql_query_string(list_of_companies_query)
        self.allure_url.allure_attach_with_text("Mysql query", str(list_of_companies_query))
        self.allure_url.allure_attach_with_text("MySql response", str(mysql_res))
        assert len(mysql_res) == len(list_of_companies_response.json()), "Number of companies doesnt match"
        assert list_of_companies_response.status_code == 200, "Login Status Code mismatch"

    @pytest.mark.adam
    # Verifying Company ID, Billing Email, StateID & CompanyTypeID
    def test_company_by_id(self):
        tok = self.get_token()
        url = self.url_util.get_url(self.url_util.COMPANY_LIST_OF_COMPANIES)
        list_of_companies = self.api_utils.get_api_request(url, tok)
        company_id_list = []
        all_company_details = []
        # Getting all Company ID in a list
        for i in list_of_companies.json():
            company_id_list.append(i["id"])
        for company_id in company_id_list:
            url = self.url_util.get_url(self.url_util.COMPANY_COMPANY_BY_ID.format(Id=company_id))
            company_by_id_response = self.api_utils.get_api_request(url, tok)
            all_company_details.insert(company_id, company_by_id_response.json())
            self.allure_url.allure_attach_with_text("Company Details_Status Code",
                                                    str(company_by_id_response.status_code))
            self.allure_url.allure_attach_with_text(f"Details of Company Id - {company_id}",
                                                    str(company_by_id_response.json()))
            assert company_by_id_response.status_code == 200, "Company By ID status code mismatch"

        # ----------Mysql validation -------------------------------
        company_id_list_for_sql = [str(i) for i in company_id_list]
        company_by_id_query = f"select * from Companies where ID in ({','.join(company_id_list_for_sql)});"
        mysql_res = self.mysql_obj.sql_query_string(company_by_id_query)
        self.allure_url.allure_attach_with_text("Mysql query", str(company_by_id_query))
        self.allure_url.allure_attach_with_text("MySql response", str(mysql_res))
        for i, j in zip(mysql_res, all_company_details):
            assert i['ID'] == j['id'], "Company ID mismatch b/w API response and DB response"
            assert i['BillingEmail'] == j['billingEmail'], \
                "Company Billing Email mismatch b/w API response and DB response"
            assert i['StateID'] == j['stateId'], \
                "Company StateID mismatch b/w API response and DB response"
            assert i['CompanyTypeID'] == j['companyTypeId'], \
                "Company CompanyTypeID mismatch b/w API response and DB response"
            self.allure_url.allure_attach_with_text(f"ID, Billing Email, StateID & CompanyTypeID of "
                                                    f"Company ID {i['ID']} matches b/w API response and DB response",
                                                    str(""))

    @pytest.mark.adam
    # Verifying number of jobs of a company
    def test_jobs_of_company(self):
        # company_id = 1
        tok = self.get_token()
        url = self.url_util.get_url(self.url_util.COMPANY_LIST_OF_COMPANIES)
        list_of_companies = self.api_utils.get_api_request(url, tok)
        company_id_list = []
        jobs_of_all_companies = []
        # Getting all Company ID in a list
        for i in list_of_companies.json():
            company_id_list.append(i["id"])
        jobs_data = {f"No. of Jobs in CompanyID {key}": 0 for key in company_id_list}
        for company_id in company_id_list:
            jobs_url = self.url_util.JOBS_GET_JOB.format(
                companyID=company_id)
            jobs_url = self.url_util.get_url(jobs_url)
            jobs_of_company_response = self.api_utils.get_api_request(jobs_url, tok)
            self.allure_url.allure_attach_with_text(f"Jobs of CompanyID - {company_id}_Status code",
                                                    str(jobs_of_company_response.status_code))
            self.allure_url.allure_attach_with_text(f"Jobs of CompanyID - {company_id}_API response",
                                                    str(jobs_of_company_response.json()))
            assert jobs_of_company_response.status_code == 200, "No of Jobs_Status Code mismatch"
            self.allure_url.allure_attach_with_text(f"Number of jobs of CompanyID - {company_id} is ",
                                                    str(len(jobs_of_company_response.json()["jobs"])))
            jobs_data[f"No. of Jobs in CompanyID {company_id}"] += len(jobs_of_company_response.json()["jobs"])
        self.allure_url.allure_attach_with_text(f"Number of jobs in each company_API response_compiled ",
                                                str(jobs_data))
        # ----------Mysql validation -------------------------------
        company_id_list_for_sql = [str(i) for i in company_id_list]
        number_of_jobs_of_company_query = f"select * from Jobs where CompanyID in" \
                                          f" ({','.join(company_id_list_for_sql)});"
        mysql_res = self.mysql_obj.sql_query_string(number_of_jobs_of_company_query)
        # creating a dictionary for mapping number of jobs in each company
        jobs_data_db = {f"No. of Jobs in CompanyID {key['CompanyID']}": 0 for key in mysql_res}

        # Adding total number of Jobs for each company
        for response in mysql_res:
            if response["CompanyID"]:
                jobs_data_db[f"No. of Jobs in CompanyID {response['CompanyID']}"] += 1

        self.allure_url.allure_attach_with_text(f"Number of jobs in each company_DBresponse",
                                                str(jobs_data_db))

        # asserting number of jobs of each company
        for i in jobs_data_db.keys():
            if i in jobs_data:
                assert jobs_data_db[i] == jobs_data[i], "Total number of jobs of a Company doesnt match"

    @pytest.mark.adam
    def test_inspection_jobid(self):
        # Verification of Number of inspections under a specific Job ID & Verification of Unique ID of Inspection
        tok = self.get_token()
        # Getting all Job ID's
        url = self.url_util.get_url(self.url_util.COMPANY_LIST_OF_COMPANIES)
        list_of_companies = self.api_utils.get_api_request(url, tok)
        company_id_list = []
        jobs_data = []
        job_id_list = []
        inspection_data_list = []
        # Getting all Company ID in a list for feeding it to getting all JOBS API
        for i in list_of_companies.json():
            company_id_list.append(i["id"])
        for company in company_id_list:
            url = self.url_util.JOBS_GET_JOB.format(companyID=company)
            url = self.url_util.get_url(url)
            api_response = self.api_utils.get_api_request(url, tok)
            assert api_response.status_code == 200, "Status Code mismatch"
            jobs_data.extend(api_response.json()["jobs"])
        for i in jobs_data:
            job_id_list.append(i["id"])
            job_id_list.sort()
        api_response_collection = []
        for job in job_id_list:
            url = self.url_util.INSPECTION_GET_INSPECTIONS_JOBID.format(jobID=job)
            url = self.url_util.get_url(url)
            api_response = self.api_utils.get_api_request(url, tok)
            self.allure_url.allure_attach_with_text(f"Inspection under Job ID-{job}_statuscode",
                                                    str(api_response.status_code))
            assert api_response.status_code == 200, "Login Status Code mismatch"
            self.allure_url.allure_attach_with_text("NO. of Inspections of a JOB ID_Api response",
                                                    str(len(api_response.json())))
            self.allure_url.allure_attach_with_text(f"Inspection under Job ID-{job}_API response",
                                                    str(api_response.json()))
            api_response_collection.extend(api_response.json())
        self.allure_url.allure_attach_with_text(f"Total Number of Inspections of all companies_APIresponse",
                                                str(len(api_response.json())))

        # creating a dict with inspection id of all inspections as key
        api_response_data = {key['id']: [] for key in api_response_collection}
        # assigning UniqueId, inspecitonname & package to the respective inspection ID
        for key in api_response_collection:
            api_response_data[key['id']].append(key['uniqueId'])
            api_response_data[key['id']].append(key['inspectionName'])
            api_response_data[key['id']].append(key['package'])

        # ----------Mysql validation -----------------------------------
        job_id_list_sql = [str(i) for i in job_id_list]
        number_inspections_by_jobid_query = f"select * from Inspections where JobID in ({','.join(job_id_list_sql)});"
        mysql_res = self.mysql_obj.sql_query_string(number_inspections_by_jobid_query)
        self.allure_url.allure_attach_with_text("Mysql query", str(number_inspections_by_jobid_query))
        self.allure_url.allure_attach_with_text("MySql response", str(mysql_res))
        self.allure_url.allure_attach_with_text("Total Number of Inspections of all companies_DBresponse",
                                                str(len(mysql_res)))
        assert len(mysql_res) == len(api_response_collection), "Number of Inspections of a Job ID doesnt match with DB"
        # creating a dict with inspection id of all inspections as key
        db_response_data = {key['ID']: [] for key in mysql_res}
        # assigning UniqueId, inspection name & package to the respective inspection ID
        for key in mysql_res:
            db_response_data[key['ID']].append(key['UniqueID'])
            db_response_data[key['ID']].append(key['InspectionName'])
            db_response_data[key['ID']].append(key['Package'])

        # asserting API & DB data stored dictionaries. Verifiying if the data for the respective ID matches
        for i in api_response_data:
            if i in db_response_data:
                assert api_response_data[i] == db_response_data[i], "Data mismatch between API & DB responses"

    # @pytest.mark.adam
    # # Verification of all the ID's of all inspections under a specific company
    # def test_inspection_id(self):
    #     tok = self.get_token()
    #     job_id = 12
    #     url = self.url_util.INSPECTION_GET_INSPECTIONS_JOBID.format(jobID=job_id)
    #     url = self.url_util.get_url(url)
    #     api_response = self.api_utils.get_api_request(url, tok)
    #     print(api_response.status_code)
    #     print(api_response.json())
    #     # print(len(api_response.json()))
    #     # assert api_response.status_code == 200, "Login Status Code mismatch"
    #     # self.allure_url.allure_attach_with_text("GET_INSPECTIONS_ID_JOBID_statuscode", str(api_response.status_code))
    #     # inspection_id = []
    #     # for i in range(len(api_response.json())):
    #     #     inspection_id.append((api_response.json()[i]['id']))
    #     # self.allure_url.allure_attach_with_text("ID's of all Inspections", str(inspection_id))
    #     # ----------Mysql validation -------------------------------
    #     # number_inspections_by_jobid_query = f"select * from Inspections where JobID={job_id};"
    #     # mysql_res = self.mysql_obj.sql_query_string(number_inspections_by_jobid_query)
    #     # self.allure_url.allure_attach_with_text("Number of ID's of Inspections of a JOB ID_DBresponse",
    #     #                                         str(len(mysql_res)))
    #     # self.allure_url.allure_attach_with_text("Mysql query", str(number_inspections_by_jobid_query))
    #     # assert len(mysql_res) == len(
    #     #     (api_response.json())), "Number of Inspections of a Job ID doesnt match with DB"
    #     # inspection_id_db = []
    #     # for i in range(len(mysql_res)):
    #     #     assert mysql_res[i]['ID'] == api_response.json()[i]['id'], "Inspection ID mismatch"
    #     #     inspection_id_db.append(mysql_res[i]['ID'])
    #     # self.allure_url.allure_attach_with_text("ID's of Inspections as per DB",
    #     #                                         str(inspection_id_db))

    # @pytest.mark.adam
    # # Verification of Unique ID of inspections
    # def test_inspection_uniqueid(self):
    #     tok = self.get_token()
    #     job_id = 12
    #     url = self.url_util.INSPECTION_GET_INSPECTIONS_JOBID.format(jobID=job_id)
    #     url = self.url_util.get_url(url)
    #     api_response = self.api_utils.get_api_request(url, tok)
    #     print(api_response.status_code)
    #     print(api_response.json())
    #     print(len(api_response.json()))
    #     assert api_response.status_code == 200, "Status Code mismatch"
    #     self.allure_url.allure_attach_with_text("GET_INSPECTIONS_uniqueID_JOBID_statuscode",
    #                                             str(api_response.status_code))
    #     unique_id = []
    #     for i in range(len(api_response.json())):
    #         unique_id.append((api_response.json()[i]['uniqueId']))
    #     self.allure_url.allure_attach_with_text("Unique ID's of all Inspections", str(unique_id))
    #     # # ----------Mysql validation -------------------------------
    #     # number_inspections_by_jobid_query = f"select * from Inspections where JobID={job_id};"
    #     # mysql_res = self.mysql_obj.sql_query_string(number_inspections_by_jobid_query)
    #     # self.allure_url.allure_attach_with_text("Number of Unique ID's of Inspections of a JOB ID_DBresponse",
    #     #                                         str(len(mysql_res)))
    #     # self.allure_url.allure_attach_with_text("Mysql query", str(number_inspections_by_jobid_query))
    #     # assert len(mysql_res) == len(api_response.json()), "Number of Inspections of a Job ID doesnt match with DB"
    #     # unique_id_db = []
    #     # for i in range(len(mysql_res)):
    #     #     assert mysql_res[i]['UniqueID'] == api_response.json()[i]['uniqueId'], "Unique ID of Inspection mismatch"
    #     #     unique_id_db.append(mysql_res[i]['UniqueID'])
    #     # self.allure_url.allure_attach_with_text("unique ID's of Inspections as per DB",
    #     #                                         str(unique_id_db))

    @pytest.mark.adam
    def test_users(self):
        # Verification of Number of Users in company and few attributes of the users
        tok = self.get_token()
        # Getting all company ID's
        url = self.url_util.get_url(self.url_util.COMPANY_LIST_OF_COMPANIES)
        list_of_companies = self.api_utils.get_api_request(url, tok)
        assert list_of_companies.status_code == 200, "Status Code mismatch"
        list_of_companies_response = list_of_companies.json()
        company_id_list = []
        name_list = []
        users_of_company = []
        for company in list_of_companies_response:
            company_id_list.append(company["id"])
            company_id = company["id"]
            # Get request hit
            url = self.url_util.USER_GET_USERS.format(companyID=company_id)
            url = self.url_util.get_url(url)
            url_hit = self.api_utils.get_api_request(url, tok)
            assert url_hit.status_code == 200, "Status Code mismatch"
            users_company_response = url_hit.json()
            self.allure_url.allure_attach_with_text(f"USERS_of_CompanyID-{company_id}_statuscode",
                                                    str(url_hit.status_code))
            self.allure_url.allure_attach_with_text(f"Number of Users in CompanyID - {company_id}_APIresponse",
                                                    str(len(users_company_response)))
            self.allure_url.allure_attach_with_text(f"Data of Users in CompanyID - {company_id}_APIresponse",
                                                    str(users_company_response))
            for i in users_company_response:
                name_list.append(i["name"])
            users_of_company.extend(users_company_response)
        user_data = {key: [] for key in name_list}
        for data in users_of_company:
            if data["name"] in user_data:
                user_name = data["name"]
                user_data[f"{user_name}"].append(data["role"])
                user_data[f"{user_name}"].append(data["email"])
        self.allure_url.allure_attach_with_text("Total Number of Users of All Companies_APIresponse",
                                                str(len(users_of_company)))
        self.allure_url.allure_attach_with_text("All USERS_attributes_APIresponse",
                                                str(user_data))
        company_id_list_for_sql = [str(i) for i in company_id_list]
        # ------------------Mysql validation -------------------------------
        users_query = f"select * from Users where CompanyID in ({','.join(company_id_list_for_sql)});"
        mysql_res = self.mysql_obj.sql_query_string(users_query)
        self.allure_url.allure_attach_with_text("Mysql query", str(users_query))
        self.allure_url.allure_attach_with_text("Total Number of Users of All Companies_DBresponse",
                                                str(len(mysql_res)))
        self.allure_url.allure_attach_with_text("Users Data of All company_DBresponse", str(mysql_res))
        assert len(mysql_res) == len(users_of_company), "Total Number of Users mismatch"
        for i in mysql_res:
            if i["Name"] in user_data:
                name = i["Name"]
                assert i["Email"] in user_data[f"{name}"], "Email of User not matching"

    @pytest.mark.adam
    # Verification of Number of Groups under a JOB ID
    def test_number_of_groups(self):
        tok = self.get_token()
        # Getting all Job ID's
        url = self.url_util.get_url(self.url_util.COMPANY_LIST_OF_COMPANIES)
        list_of_companies = self.api_utils.get_api_request(url, tok)
        company_id_list = []
        jobs_data = []
        job_id_list = []
        groups_data = []
        # Getting all Company ID in a list for feeding it to getting all JOBS API
        for i in list_of_companies.json():
            company_id_list.append(i["id"])
        for i in company_id_list:
            url = self.url_util.JOBS_GET_JOB.format(companyID=i)
            url = self.url_util.get_url(url)
            api_response = self.api_utils.get_api_request(url, tok)
            assert api_response.status_code == 200, "Status Code mismatch"
            jobs_data.extend(api_response.json()["jobs"])
        for i in jobs_data:
            job_id_list.append(i["id"])
            job_id_list.sort()
        # Getting all groups API
        for i in job_id_list:
            url = self.url_util.GROUP_GET_ALL.format(jobID=i)
            url = self.url_util.get_url(url)
            api_response = self.api_utils.get_api_request(url, tok)
            assert api_response.status_code == 200, "Status Code mismatch"
            self.allure_url.allure_attach_with_text(f"Number of groups of the Job ID {i}_api response",
                                                    str(len(api_response.json())))
            self.allure_url.allure_attach_with_text(f"Group data of JOB ID {i}_APIresponse",
                                                    str(api_response.json()))
            groups_data.extend(api_response.json())
        group_from_api = {i["id"]: i["name"] for i in groups_data}
        group_from_api = {key: group_from_api[key] for key in sorted(group_from_api.keys())}
        # ----------Mysql validation -------------------------------
        job_id_list_for_sql = [str(i) for i in job_id_list]
        get_all_groups_query = f"select * from Groups where JobID in ({','.join(job_id_list_for_sql)});"
        mysql_res = self.mysql_obj.sql_query_string(get_all_groups_query)
        assert len(mysql_res) == len(groups_data), "Total Number of Groups mismatch"
        group_from_db = {i["ID"]: i["Name"] for i in mysql_res}
        self.allure_url.allure_attach_with_text(f"Total Number of groups_DB response",
                                                str(len(mysql_res)))
        self.allure_url.allure_attach_with_text(f"Groups_data_DB response",
                                                str(mysql_res))
