import boto3
import json
try:
    org =boto3.client('organizations')
    response=org.list_accounts()
    
    data=[]
    for i in response["Accounts"]:
        accounts=int(i["Id"])
        data.append(accounts)
    print(data)
        # Loading User.json to verify Account and proceed to adding user
    with open("user.json","r") as file:
        result=json.loads(file.read())
        for i in result["Accounts"]:
            
            if (i["Id"] in data):
                print("Account Found with the ID: " ,i["Id"])
                role_arn=f'arn:aws:iam::{i["Id"]}:role/OrganizationAccountAccessRole'
                sts_client = boto3.client('sts')
                try:
                    assumed_role_response = sts_client.assume_role(
                                RoleArn=role_arn,
                                RoleSessionName='AssumedRoleSession'
                                )
                    access_key_id = assumed_role_response['Credentials']['AccessKeyId']
                    secret_access_key = assumed_role_response['Credentials']['SecretAccessKey']
                    session_token = assumed_role_response['Credentials']['SessionToken']
                    iam_client = boto3.client('iam', aws_access_key_id=access_key_id,
                             aws_secret_access_key=secret_access_key,
                             aws_session_token=session_token)
                    try:
                        
                        for user in i["Users"]:
                            iam_client.create_user(UserName=user)
                    except Exception as e:
                        print("An error occured during User Creation: ", e)

                except Exception as e:
                    print("An error occurred during assuming role: ", e)


            else:
                print("No Account found with the ID: ",i["Id"])

        
except Exception as e:
    print(e)