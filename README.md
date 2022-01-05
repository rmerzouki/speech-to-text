# Transcriber : Audio_To_Text-app

# Running transcriber as a Streamlit app
To recreate this web app on your own computer, do the following.

### Create conda environment (Optional)
Firstly, we will create a conda environment called *transcriber_env*
```
conda create -n transcriber_env python=3.7.9
```
Secondly, we will login to the *transcriber_env* environment
```
conda activate transcriber_env
```

###  Download GitHub repo

```
git clone https://github.com/rmerzouki/speech-to-text.git
```

###  Pip install libraries
```
pip install -r requirements.txt
```

###  Launch the app

```
streamlit run audio_to_text.py
```


###  Deployment on Streamlit 
```
The app is deployed on Streamlit. It is accessible through the following path :
    
    https://share.streamlit.io/rmerzouki/speech-to-text/main/audio_to_text.py

 Steps to deploy the app on Streamlit :

    1 - Run your app locally, click on the Streamlit menu at the top right of the page and select "Deploy this app".
    2 - Apps are deployed directly from their Github repo. Enter the location of your app and the settings i.e. secrets, api key...
    3 - Save & Hit Deploy!
    4 - Once it is done, share your app path with the audience.

Streamlit Secrets Management allows you to store secrets securely and access them in your Streamlit app as environment variables. For further information on this topic, check out the following documentation :

 https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management

```