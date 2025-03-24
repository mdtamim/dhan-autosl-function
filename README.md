# dhan-autosl-function
Auto Stoploss placement code for dhan broker using python APIs

The code will be deployed to GCP as a  google cloud function.CLoud function needs main entry point and requirement.txt in root location

# deploying code in GCP

## login to CLI 

## clone git repo using command :
   git clone https://github.com/mdtamim/dhan-autosl-function.git
   pass github user name and PAT (Account -> Setting -> Developer Setting > Token)

## Retrigger deployment with below command
   Go inside root directory of github repo :
   cd dhan-autosl-function/

   Redeploy cloud function :
   gcloud functions deploy dhan-auto-sl     --runtime python311     --trigger-http     --allow-unauthenticated     --entry-point main     --region asia-south1     --source .


#Todo
Fix allow unauthenticated 
