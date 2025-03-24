# dhan-autosl-function
Auto Stoploss placement code for dhan broker using python APIs

The code will be deployed to GCP as a  google cloud function.Cloud function needs main entry point and requirement.txt in root location

# Deploying code in GCP

### Login to GCP CLI
#### Clone git repo using command :
#### PAT (Account Setting -> Setting -> Developer Setting > Fine grained Token -> token -> Regenerate token)
#### git clone https://github.com/mdtamim/dhan-autosl-function.git
#### Pass github user name and regenerated PAT


### Retrigger deployment with below command
#### Go inside root directory of github repo :
#### cd dhan-autosl-function/

### Redeploy cloud function :
gcloud functions deploy dhan-auto-sl     --runtime python311     --trigger-http     --allow-unauthenticated     --entry-point main     --region asia-south1     --source .

# Test if deployment was successful : 
#### Calling the cloud function : https://asia-south1-dhan-algo.cloudfunctions.net/dhan-auto-sl
#### The get API should return "Task completed successfully" in the browser 

# Todos
Fix allow unauthenticated 
