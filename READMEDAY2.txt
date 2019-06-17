To install tesseract OCR

sudo apt-get install tesseract-ocr

sudo apt-get install imagemagick 

if that doesn't work, try

sudo apt-get update
sudo apt-get upgrade

and then retry imagemagick 

make the RUNME.txt file an executable:
navigate to that directory in 
/home/pi/IoTCurriculum/IOTDay2 

use command
chmod +x RUNME.txt

in order to run the file, name your snapshot in the same folder snapshot.png 
then execute the file with ./RUNME.txt and the output should be in a file called eng.txt



Using Google OCR it works!

test sample photo included. I took a picture of a document i printed
out from word that just said random text
and sent that to the google OCR API. So there are some steps


connecting to google cloud:

1. Download the JSON file from the google cloud platform
This should be provided to you with the package

in terminal:
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]" where PATH is the path to your json file
so  = /home/pi/SteamworksIOT-...

then install google cloud vision client libraries

pip install --upgrade google-cloud-vision

then install the python documentation samples which provide most of the code
 


git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git

create virtualenv with 
virtualenv env
source env/bin/activate

then go within the new folder you cloned from github, 

do cd /python-docs-samples/vision/cloud-client/detect

then you can run python detect.py /home/pi/Documents/IoTCurriculum/IOTDay2/OCRenv/snapshot.png
but you can replace that path with the path of whichever picture you took from the 
camera1.py picture. 


under your python doc samples in the detec.py function 
change it to 

# [START vision_text_detection]
def detect_text(path):
    detectFILE= open("speechfile.txt", "a")
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        text = str(text.description)
        detectFILE.write(text)
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    detectFILE.close()
    # [END vision_python_migration_text_detection]
# [END vision_text_detection]
this enables a file called speechfile.txt to be created 
within the directory /home/pi/Documents/IoTCurriculum/IOTDay2/OCRenv/python-docs-samples/vision/cloud-client/detect


For text to speech:

sudo apt-get install espeak
sudo apt-get install espeak python-espeak

****Try with speakers getting PCM errors

LSA lib pcm.c:2495:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.modem
ALSA lib pcm.c:2495:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.modem
ALSA lib pcm.c:2495:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.phoneline
ALSA lib pcm.c:2495:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.phoneline
ALSA lib confmisc.c:1281:(snd_func_refer) Unable to find definition 'defaults.bluealsa.device'
ALSA lib conf.c:4528:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:4996:(snd_config_expand) Args evaluate error: No such file or directory
ALSA lib pcm.c:2495:(snd_pcm_open_noupdate) Unknown PCM bluealsa
ALSA lib confmisc.c:1281:(snd_func_refer) Unable to find definition 'defaults.bluealsa.device'
ALSA lib conf.c:4528:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:4996:(snd_config_expand) Args evaluate error: No such file or directory
ALSA lib pcm.c:2495:(snd_pcm_open_noupdate) Unknown PCM bluealsa
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock

