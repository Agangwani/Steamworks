Day 4 and 5 curriculum.

For the first intro to raspberry pi cameras and networking
we're going to take it a step further and display the 
camera output onto a web server. 

taken from Raspberry pi sensors book on pakt pub
// not used
Commands to Run:
sudo apt-get update
sudo apt-get upgrade

sudo apt-get -y install bison
sudo apt-get -y install motion
sudo apt-get -y install v41-utile
// used

pip install picamera

sudo pip install flask 
git clone https://github.com/miguelgrinberg/flask-video-streaming.git

within the app.py file uncomment #from camera import camera 
by removing the #
save the file

run ifconfig and find your inet address or your IP address
from there you run the flask server with python app.py 

it should say 
: Running on https://0.0.0.0:5000/

go to your IP address so for example open web page and go to 

172.20.10.11:5000 
this should redirect you to a video of you live on the 
local webpage


doing face detect

pip3 install opencv-python 
sudo apt-get install libcblas-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test

now you should be able to successfullly run face_detect.py with
python3 face_detect.py


must run as "python3" face detect rather than python face detect

now we're going to implement face_detect with the original camera
stream to the webpage


