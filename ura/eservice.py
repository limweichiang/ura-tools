# For requests
import requests

# For read_json
import pandas as pd

# Used to get authentication token. This must be called by all API Call functions in the module.
def get_auth_token(access_key):
    res = requests.get(
        url='https://eservice.ura.gov.sg/uraDataService/insertNewToken/v1',
        headers = {
            "AccessKey": access_key,
            "user-agent": "curl"
        }
    )

    if res.status_code == 200 and res.json()["Status"] == "Success":
        return res.json()["Result"]
    else:
        return None

def get_private_residential_property_transactions(access_key):
    auth_token = get_auth_token(access_key)

    # Error Condition: Return no results. Check for None condition from caller.
    if auth_token == None:
        return None
    
    # Looping through all data batches to compile single dataset.
    ## From https://eservice.ura.gov.sg/maps/api/#private-residential-property
    ## Data are available for download in 4 batches. They are split by postal
    ## districts e.g. batch 1 is for postal district 01 to 07, batch 2 is for
    ## postal district 08 to 14 etc. To download for batch 1, pass in the value 1.
    data_batch_list = []
    for batch in range(1,4):
        res = requests.get(
            url='https://eservice.ura.gov.sg/uraDataService/invokeUraDS/v1?service=PMI_Resi_Transaction&batch=' + str(batch),
            headers = {
                "AccessKey": access_key,
                "Token": auth_token,
                "user-agent": "curl"
            }
        )    
        if res.status_code == 200 and res.json()["Status"] == "Success":
            data_batch_list.append(pd.json_normalize(
                res.json()["Result"],
                meta=["marketSegment", "project", "street", "x", "y"],
                record_path=["transaction"],
                errors='ignore'
            ))
    
    if len(data_batch_list) == 0:
        return None
    else:
        dataset = pd.concat(data_batch_list)
        return dataset.to_csv(index=False, index_label=False)