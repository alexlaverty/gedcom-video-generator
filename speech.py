import boto3 
import config
import logging 

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

def process_speech_text(text):
    #text = text.replace(" Laverty ", " Lav Verty ")
    text = text.replace("&", "and")
    return text

def create_audio(path, text):
    logging.info("========== Creating Audio File From Text ==========")   
    logging.info("Path : " + path)
    
    text = process_speech_text(text)
    

    polly_client = boto3.Session(
                    aws_access_key_id=config.aws_access_key_id,                     
                    aws_secret_access_key=config.aws_secret_access_key,
                    region_name='us-west-2').client('polly')

    polly_text = f'<speak><prosody rate="85%">{text}</prosody></speak>'
    logging.info("Speech : " + polly_text)
    response = polly_client.synthesize_speech(
            Engine='neural',
            OutputFormat='mp3', 
            Text=polly_text,
            TextType='ssml',
            VoiceId='Olivia'
        )

    file = open(path, 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    logging.info("========== Finished Creating Audio File From Text ==========")   


