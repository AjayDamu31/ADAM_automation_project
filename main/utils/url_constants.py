from .config_reader import Config


class URLConstant(object):
    AUTH_LOGIN = "/api/Authentication/Login"
    AUTH_REGISTER = "/api/Authentication/Register"

    COMPANY_COMPANY_BY_ID = "/api/Company/GetCompany/{Id}"
    COMPANY_LIST_OF_COMPANIES = "/api/Company/GetCompanies"

    INSPECTION_GET_INSPECTION = "/api/Inspection/GetInspection/{inspectionID}"
    INSPECTION_GET_INSPECTIONS_JOBID = "/api/Inspection/{jobID}/GetAllJobInspections"

    JOBS_GET_JOB = "/api/Job/{companyID}/GetAll"

    USER_GET_USERS = "/api/User/{companyID}/GetUsers"

    GROUP_GET_ALL = "/api/Group/{jobID}/GetAll"

    def get_url(self, url_key):
        base_url = Config.get_key_value('base_url')
        return base_url + url_key
