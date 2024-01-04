from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, cudaFont, cudaAllocMapped, cudaResize, cudaDrawLine
import subprocess
import re
from counter import *
import send_data

net = detectNet("trafficcamnet", threshold=0.5)
camera = videoSource("csi://0")
#camera = videoSource("/home/jetson/Downloads/mapy.mp4")      # '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file
font = cudaFont()

cmd = ['xrandr']
cmd2 = ['grep', '*']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
p.stdout.close()
resolution_string, junk = p2.communicate()
resolution = resolution_string.split()[0]
sc_width, sc_height = re.findall(r'\d+', str(resolution))

display_result = True

net.SetTrackingEnabled(True)
net.SetTrackingParams(minFrames=3, dropFrames=15, overlapThreshold=0.5)
counter_init(net)
send_data.start()

while True:
    img = camera.Capture()

    if img is None: # capture timeout
        continue

    detections = net.Detect(img)

    if display_result == False:
        print(net.GetNetworkFPS())
    
    for detection in detections:
        if detection.TrackStatus >= 0:  # actively tracking
            countUk(detection,int((detection.Left+detection.Right)/2),int((detection.Top+detection.Bottom)/2),img)
            print(f"object {detection.TrackID} at ({detection.Left}, {detection.Top}) has been tracked for {detection.TrackFrames} frames")
            if display_result:
                font.OverlayText(img, text=f"{detection.TrackID}", 
                         x=int((detection.Left+detection.Right)/2), 
                         y=int((detection.Top+detection.Bottom)/2),
                         color=font.White, background=font.Gray)

    if display_result:
        imgOutput = cudaAllocMapped(width=int(sc_width)*0.8, 
                                         height=int(sc_height)*0.8, 
                                         format=img.format)
        for _,_,px1,py1,px2,py2 in countLines:
            x1=int(img.width*px1)
            y1=int(img.height*py1)
            x2=int(img.width*px2)
            y2=int(img.height*py2)
            cudaDrawLine(img, (x1,y1), (x2,y2), (255,0,200,200), 3)
        
        cudaResize(img,imgOutput)
        display.Render(imgOutput)
        display.SetStatus("Object Detection | Network {:.0f} FPS | Count {:.0f}, {:.0f}".format(net.GetNetworkFPS(),counter[0],counter[1]))

        # exit on input/output EOS
        if not display.IsStreaming():
            break
