""" Modul, um die Daten vom Broker zu erhalten.
"""

from datetime import datetime
import paho.mqtt.client as mqtt
import re
import threading

import ev
import prepare

class subData():
    """ Klasse, die die benötigten Topics abonniert, die Instanzen ertstellt, wenn z.b. ein Modul neu konfiguriert wird, 
    Instanzen löscht, wenn Module gelöscht werden, und die Werte in die Attribute der Instanzen schreibt.
    """

    #Instanzen
    cp_data={}
    cp_template_data={}
    pv_data={}
    pv_module_data={}
    ev_data={}
    ev_template_data={}
    ev_charge_template_data={}
    meter_data={}
    meter_module_data={}
    bat_data={}
    bat_module_data={}
    evu_data={}
    evu_module_data={}

    def __init__(self):
        self.ticker_prepare = threading.Event()
        self.prep=prepare.prepare()

    def sub_topics(self):
        """ abonniert alle Topics.
        """
        mqtt_broker_ip = "localhost"
        client = mqtt.Client("openWB-mqttsub-" + self.getserial())
        ipallowed='^[0-9.]+$'
        nameallowed='^[a-zA-Z ]+$'
        namenumballowed='^[0-9a-zA-Z ]+$'

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(mqtt_broker_ip, 1883)
        client.loop_forever()
        client.disconnect()

    def getserial(self):
        """ Extract serial from cpuinfo file
        """
        with open('/proc/cpuinfo','r') as f:
            for line in f:
                if line[0:6] == 'Serial':
                    return line[10:26]
            return "0000000000000000"

    def on_connect(self, client, userdata, flags, rc):
        """ connect to broker and subscribe to set topics
        """
        client.subscribe("openWB/#", 2)

    def on_message(self, client, userdata, msg):
        """ wartet auf eingehende Topics und ruft Funktionen zur weiteren Verarbeitung auf.
        """
        topic=msg.topic
        payload=msg.payload
        # log all messages before any error forces this process to die
        if (len(msg.payload.decode("utf-8")) >= 1):
            theTime = datetime.now()
            timestamp = theTime.strftime(format = "%Y-%m-%d %H:%M:%S")
            file = open('/var/www/html/openWB/ramdisk/mqtt.log', 'a')
            file.write( "%s Topic: %s Message: %s\n" % (timestamp, msg.topic, str(msg.payload.decode("utf-8"))) )
            file.close()

        print(msg.topic, msg.payload)

        if "openWB/vehicle" in topic:
            processVehicleTopic(topic, payload)
        elif "openWB/chargepoint" in topic:
            processChargepointTopic(topic, payload)
        elif "openWB/pv" in topic:
            processPvTopic(topic, payload)
        elif "openWB/bat" in topic:
            processBatTopic(topic, payload)
        elif "openWB/general" in topic:
            processGeneralTopic(topic, payload)
        elif "openWB/optional" in topic:
            processOptionalTopic(topic, payload)
        elif "openWB/counter" in topic:
            processCounterTopic(topic, payload)
        elif "openWB/graph" in topic:
            processGraphTopic(topic, payload)
        elif "openWB/smarthome" in topic:
            processSmarthomeTopic(topic, payload)
        else:
            print("Unknown topic: "+topic+", "+str(msg.payload.decode("utf-8")))

    def get_index(self, topic):
        """extrahiert den Index aus einemTtopic (zwischen zwei //)
        """
        index=re.search('(?!\/)([0-9]+)(?=\/)', topic)
        return index.group()

    def processVehicleTopic(self, topic, payload):
        """
        """
        if topic=="openWB/vehicle/general/chargeMode":

        elif topic=="openWB/vehicle/standard/matchEV":

        elif topic=="openWB/vehicle/standard/chargeTemplate":

        elif topic=="openWB/vehicle/standard/evTemplate":

        elif topic=="openWB/vehicle/template/chargeTemplate":
            index=self.get_index(topic)
            if "cp"+index not in ev_charge_template_data:
                ev_charge_template_data["cp"+index] = ev.chargeTemplate()
            if "name" in topic:

            elif "loadStandard" in topic:

            elif "prio" in topic:

            elif "chargeMode" in topic:
                if "immediateLoad/current" in topic:

                elif "immediateLoad/limit" in topic:

        elif topic=="openWB/vehicle/template/evTemplate":


        else:

    def processChargepointTopic(self, topic, payload):
        """
        """
        pass

    def processPvTopic(self, topic, payload):
        """
        """
        pass

    def processBatTopic(self, topic, payload):
        """
        """
        pass

    def processGeneralTopic(self, topic, payload):
        """
        """
        pass

    def processOptionalTopic(self, topic, payload):
        """
        """
        pass

    def processCounterTopic(self, topic, payload):
        """
        """
        pass

    def processGraphTopic(self, topic, payload):
        """
        """
        pass

    def processSmarthomeTopic(self, topic, payload):
        """
        """
        pass

        #keine Reihenfolge imner gucken, ob es Instanz schon gibt

        if topic=="openWB/chargepoint/1":
            if payload==True:
                cp1=chargepoint()
                data.cp_data.append(cp1)
            else
                data.cp_data[0].remove(cp1)
        elif topic == "openWB/chargepoint/1/config/template/autolock":
            if cp1 in data.cp_data:
                cp1=chargepoint()
                data.cp_data.append(cp1)
            if payload == True:
                data.cp_data[0].autolock=true
            else
                data.cp_data[0].autolock=false
        elif topic=="openWB/chargepoint/1/config/template":
            if payload!="none":
                data.cp_data[0].template=payload
        elif topic="openWB/general/controlInterval":
            
            self.ticker_prepare.clear()
            seconds = mqttpayload
            self.ticker_prepare.set()
            while not self.ticker_prepare.wait(seconds):
                self.prep.setup_algorithm()