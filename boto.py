import boto3
import json
try:
    # Getting list of Accounts from the Organizations
    org =boto3.client('organizations')
    response=org.list_accounts()
    
    data=[]

    # Storing ID of the Accounts from the Organizations
    
    for i in response["Accounts"]:
        accounts=int(i["Id"])
        data.append(accounts)
    print(data)

    # Loading User.json file to verify Account and proceed to adding user
    
    with open("user.json","r") as file:
        result=json.loads(file.read())
        
        for i in result["Accounts"]:
            # Checking if the Id in user.json is valid or not

            if (i["Id"] in data):

                print("Account Found with the ID: " ,i["Id"])
                
                # Assigning role with the respective ID of accounts
                
                role_arn=f'arn:aws:iam::{i["Id"]}:role/OrganizationAccountAccessRole'
                
                # Creating Sts Client to Assume the Above role
                sts_client = boto3.client('sts')
                try:
                    assumed_role_response = sts_client.assume_role(
                                RoleArn=role_arn,
                                RoleSessionName='AssumedRoleSession'
                                )
                    access_key_id = assumed_role_response['Credentials']['AccessKeyId']
                    secret_access_key = assumed_role_response['Credentials']['SecretAccessKey']
                    session_token = assumed_role_response['Credentials']['SessionToken']

                    # Creating Iam client object with the assumed access credentials 
                    
                    iam_client = boto3.client('iam', aws_access_key_id=access_key_id,
                             aws_secret_access_key=secret_access_key,
                             aws_session_token=session_token)
                    try:
                        # Creating Users for the accounts from the user.json
                        
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