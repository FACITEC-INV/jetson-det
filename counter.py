from datetime import datetime
from db import Detection

#(indice, orientacion, x1,y1,x2,y2)
countLines=[
    (0,"hr",0.25,0.16,0.20,0.39),
    (1,"vd",0.15,0.60,0.90,0.80)
]

counter=[0,0]

uk = [dict(),dict()]

def counter_init(net):
    global _net
    _net = net

def countVD(idx,rx1,ry1,rx2,ry2,m,x,y,detection):
    ly = int((m*(x-rx1))+ry1) if m != None else ry1
    if y <= ly and str(detection.TrackID) not in uk[idx] and x >= rx1 and x <= rx2:
        uk[idx][str(detection.TrackID)] = datetime.now()
    elif y > ly and str(detection.TrackID) in uk[idx] and x >= rx1 and x <= rx2:
        counter[idx] = counter[idx]+1
        Detection.create(zona=int(idx+1),clase=_net.GetClassDesc(detection.ClassID),fecha=uk[idx][str(detection.TrackID)],enviado=False)
        del uk[idx][str(detection.TrackID)]
        
def countVU(idx,rx1,ry1,rx2,ry2,m,x,y,detection):
    ly = int((m*(x-rx1))+ry1) if m != None else ry1
    if y >= ly and str(detection.TrackID) not in uk[idx] and x >= rx1 and x <= rx2:
        uk[idx][str(detection.TrackID)] = datetime.now()
    elif y < ly and str(detection.TrackID) in uk[idx] and x >= rx1 and x <= rx2:
        counter[idx] = counter[idx]+1
        Detection.create(zona=int(idx+1),clase=_net.GetClassDesc(detection.ClassID),fecha=uk[idx][str(detection.TrackID)],enviado=False)
        del uk[idx][str(detection.TrackID)]
        
def countHR(idx,rx1,ry1,rx2,ry2,m,x,y,detection):
    lx = int(((y-ry1)/m)+rx1) if m != None else rx1
    if x <= lx and str(detection.TrackID) not in uk[idx] and y >= ry1 and y <= ry2:
        uk[idx][str(detection.TrackID)] = datetime.now()
    elif x > lx and str(detection.TrackID) in uk[idx] and y >= ry1 and y <= ry2:
        counter[idx] = counter[idx]+1
        Detection.create(zona=int(idx+1),clase=_net.GetClassDesc(detection.ClassID),fecha=uk[idx][str(detection.TrackID)],enviado=False)
        del uk[idx][str(detection.TrackID)]
        
def countHL(idx,rx1,ry1,rx2,ry2,m,x,y,detection):
    lx = int(((y-ry1)/m)+rx1) if m != None else rx1
    if x >= lx and str(detection.TrackID) not in uk[idx] and y >= ry1 and y <= ry2:
        uk[idx][str(detection.TrackID)] = datetime.now()
    elif x < lx and str(detection.TrackID) in uk[idx] and y >= ry1 and y <= ry2:
        counter[idx] = counter[idx]+1
        Detection.create(zona=int(idx+1),clase=_net.GetClassDesc(detection.ClassID),fecha=uk[idx][str(detection.TrackID)],enviado=False)
        del uk[idx][str(detection.TrackID)]

def countUk(detection,x,y,img):
    for idx,o,px1,py1,px2,py2 in countLines:
        x1=int(img.width*px1)
        y1=int(img.height*py1)
        x2=int(img.width*px2)
        y2=int(img.height*py2)
        m = (y2-y1)/(x2-x1) if (x2-x1) != 0 else None
        print(detection)
        if o == "vd":
            countVD(idx,x1,y1,x2,y2,m,x,y,detection)
        if o == "vu":
            countVU(idx,x1,y1,x2,y2,m,x,y,detection)
        if o == "hl":
            countHL(idx,x1,y1,x2,y2,m,x,y,detection)
        if o == "hr":
            countHR(idx,x1,y1,x2,y2,m,x,y,detection)