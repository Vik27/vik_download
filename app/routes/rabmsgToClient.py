from app import app, db
import pika
from app.models import unit, project,hardwareSetup, devicetable, hwchassismap,\
 Module, acquisition, hwchaschanmap, channelsetup, quantity, queue
global answer
import json
import ctypes

int32=ctypes.c_int

def pikamsg(message):
  connection = pika.BlockingConnection(pika.ConnectionParameters(
  host='localhost'))
  channel = connection.channel()
  this=channel.queue_declare(queue='hello',
                             arguments= {'x-message-ttl' : 1000}
                            )



  print 'consumer count: '
  print this.method.consumer_count
  if this.method.consumer_count:
    channel.basic_publish(exchange='',
               routing_key='hello',
               body=json.dumps(message))
    print(" [x] Sent 'json'")
    msg='1T'
  else:
    msg= [1, None]#'Local M/C not connected! Please check the network.'
    print "not sent json"

  connection.close()
  return msg

def callback(ch, method, properties, body):
   print 'received reply'
   ch.stop_consuming()
   global answer
   answer = body
   print answer

def receive(q='hello2'):
   connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
   channel = connection.channel()
   channel.queue_declare(queue=q,
                          arguments= {'x-message-ttl' : 1000}
                        )
   channel.basic_consume(callback, queue=q, no_ack=True)
   print 'started queue: ' + q
   channel.start_consuming()
   global answer
   print 'received answer in receive function'
   print answer
   return answer

@app.route("/startdaq")
def startdaq():
       pikamsg('1')
       message=receive()
       return message

@app.route('/stopdaq')
def stop():
  message={'Task':'stop'}
  pikamsg(message)
  message=receive(q)
  return message


def verifyhw(hwsetupId):
  hwsetup = hardwareSetup.HardwareSetup.query.get(hwsetupId)

  hwchasmps = hwchassismap.Hwchassismap.query.filter\
     (hwchassismap.Hwchassismap.hwSetupID==hwsetup.id).all()

  device1=devicetable.Devicetable.query.get(hwsetup.deviceId)
  qrow=queue.Queue.query.get(device1.queueId)
  qname=qrow.queuename
  devices=[]
  devices.append({'name':device1.firmwarename})
  devices[0]["Modules"]=[]
  for hwchasmap in hwchasmps:
     if hwchasmap.moduleID:
             mod = Module.Module.query.get(hwchasmap.moduleID)

             devices[0]["Modules"].append({'deviceID':mod.daqmxDeviceId, 
                 'SlotNumber': hwchasmap.slotnumber, 'hwChasMapID': hwchasmap.id,'type': mod.type  })
  print "device for verify request: " + str(devices)
  message={'Task':'verify', 'Device': devices}
  R=pikamsg(message)
  print R
  if R =='1T':
    reply=receive(qname)
    print "reply from local after verify request: " + reply
    return (reply, devices, hwsetup.id, qname)
  else:
    return (R, 1, 1, 1)

def startProjSet(projectid):
  proj=project.Project.query.get(projectid)
  [reply, devices, hwsetupID, qname]=verifyhw(proj.hwsetupId)

  if reply=='verified':

    print "getting settings for project: " + str(projectid)
    acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.hwsetupId == proj.hwsetupId)\
    & (acquisition.Acquisition.name == 'Start')).first()
    acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.hwsetupId == proj.hwsetupId)\
    & (acquisition.Acquisition.name == 'Stop')).first()
    startevent = acqstart.event
    stopevent = acqstop.event

    for mod in devices[0]["Modules"]:
      if mod['type']=='Analog_Input':
        hwchasmap=hwchassismap.Hwchassismap.query.get(mod['hwChasMapID'])
        AIsamprate=hwchasmap.samplingrate

        chansCreated = hwchaschanmap.Hwchaschanmap.query.filter\
          (hwchaschanmap.Hwchaschanmap.hwchassId == mod['hwChasMapID']).order_by(hwchaschanmap.Hwchaschanmap.channelnumber).all()
        AIchans=[]
        MICchans=[]
        RPMchans=[]
        hwchaschanmapids=[]
        for chan in chansCreated:
          if chan.channelTemplateId:
            chansetup = channelsetup.Channelsetup.query.get(chan.channelTemplateId)
            quan= quantity.Quantity.query.get(unit.Unit.query.get(chansetup.unitId).quantityID)
            if quan.name=='Acceleration':

              AIchans.append({'name': devices[0]["name"]+'Mod'+str(hwchasmap.slotnumber)+'/AI'+str(chan.channelnumber),
                              'minRange':-1*chan.peakvalue , 
                              'maxRange': chan.peakvalue, 
                              'sensitivity': chansetup.sensitivity})

              hwchaschanmapids.append(chan.id)


            if quan.name=='Sound':
              MICchans.append({'name':devices[0]["name"]+'Mod'+str(hwchasmap.slotnumber)+'/AI'+str(chan.channelnumber) , 
                              'maxRange': chan.peakvalue , 
                              'sensitivity':chansetup.sensitivity})

              hwchaschanmapids.append(chan.id)

            if quan.name=='RPM':
              RPMchans.append({'name': devices[0]["name"]+'Mod'+str(hwchasmap.slotnumber)+'/AI'+str(chan.channelnumber),
                              'minRange':-1*chan.peakvalue , 
                              'maxRange': chan.peakvalue, 
                              'sensitivity': chansetup.sensitivity})

              hwchaschanmapids.append(chan.id)

      if mod['type']=='Digital_Input':
        hwchasmap=hwchassismap.Hwchassismap.query.get(mod['hwChasMapID'])
        chansCreated = hwchaschanmap.Hwchaschanmap.query.filter\
          (hwchaschanmap.Hwchaschanmap.hwchassId == mod['hwChasMapID']).all()

        for chan in chansCreated:
          if chan.channelTemplateId:
            chansetup = channelsetup.Channelsetup.query.get(chan.channelTemplateId)
            quan= quantity.Quantity.query.get(unit.Unit.query.get(chansetup.unitId).quantityID)

            if quan.name=='Trigger':  
              if startevent == 'Digital':
                start_settings = json.loads(acqstart.eventValue)
                chanmparow = hwchaschanmap.Hwchaschanmap.query.get(start_settings['digchanmaprowId'])
                startTrigChanName= devices[0]["name"] + 'Mod' + str(hwchasmap.slotnumber) + '/PFI' +\
                str(chanmparow.channelnumber)

              if startevent == 'Level-based':
                start_settings = json.loads(acqstart.eventValue)
                chanmparow = hwchaschanmap.Hwchaschanmap.query.get(start_settings['digchanmaprowId'])
                startTrigChanName= devices[0]["name"] + 'Mod' + str(hwchasmap.slotnumber) + '/PFI' +\
                str(chanmparow.channelnumber)

            if stopevent == 'Time-based':
              stop_settings = json.loads(acqstop.eventValue)
              numOfSamps=stop_settings['time']*AIsamprate
              taskType='startTask1'


            if stopevent == 'Digital':
              stop_settings = json.loads(acqstop.eventValue)
              numOfSamps=AIsamprate
              taskType='startTask2'

            if stopevent == 'Level-based':
              stop_settings = json.loads(acqstop.eventValue)
              numOfSamps=AIsamprate
              taskType='startTask2'


    stratSetting={'startTrigChanName':startTrigChanName,'AIchans':AIchans,'MICchans':MICchans,
                  'RPMchans':RPMchans,'AIsamprate':AIsamprate,'numOfSamps':numOfSamps, 
                  'hwchaschanmapids':hwchaschanmapids, 'projectid': projectid}
    message={'Task':taskType, 'settings': stratSetting}
    print "setting for Project from rabmsgToClient.startprojSet"
    print message
    pikamsg(message)
    reply=receive(qname)
    return reply

  else:
    return reply  


def getstatus(prjctid):
  message={'Task':'status'}
  print "Project Staus Requested"
  print message
  pikamsg(message)
  reply=receive(qname)
  return reply
