# python-air-sensor
My python programs for the  particulate matter sensor 
### Run:
tmux new -s SDS  
python3 sds011_log.py  

mosquitto_sub -h mqtt.dioty.co -t /bernardo.brotas@gmail.com/air-quality/lx/aveua  -u bernardo.brotas@gmail.com -P xxxxx

