package myBluzePanel;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MqttDefaultFilePersistence;


public class myBluzePanel {
	

	@SuppressWarnings("resource")
	public static void main(String[] args) throws MqttException, InterruptedException {
		// TODO Auto-generated method stub
		//SimpleMqttCallBack call = new SimpleMqttCallBack();
		
		MqttClient client = new MqttClient("tcp://192.168.1.45:1883", MqttClient.generateClientId());
		String tmpDir = System.getProperty("java.io.tmpdir");
        String subscribeTopicName = "home/state/iface";
        String publishTopicName = "home/state/iface";
        String payload;
        MqttDefaultFilePersistence dataStore = new MqttDefaultFilePersistence(tmpDir);
        
        try {
        	client = new MqttClient("tcp://192.168.1.45:1883", "iface1", dataStore);
            MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
            mqttConnectOptions.setUserName("/:guest");
            mqttConnectOptions.setPassword("guest".toCharArray());
            mqttConnectOptions.setCleanSession(false);
            client.connect(mqttConnectOptions);
            System.out.println("Connected to Broker");
            
            client.subscribe(subscribeTopicName);
            
            System.out.println(client.getClientId() + " subscribed to topic: "+ subscribeTopicName);
            
            client.setCallback(new MqttCallback() {
            	
            	@Override                
                public void connectionLost(Throwable throwable) {
                	System.out.println("Connection lost to MQTT Broker");
                }

                @Override
                public void messageArrived(String topic, MqttMessage message) throws Exception {
                	System.out.println("-------------------------------------------------");
                    System.out.println("| Received ");
                    System.out.println("| Topic: "+ topic);
                    System.out.println("| Message: "+ new String(message.getPayload()));
                    System.out.println("| QoS: "+ message.getQos());
                    System.out.println("-------------------------------------------------");

                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
                	System.out.println("Delivery Complete");
                }
            });
            
            MqttMessage message = new MqttMessage();
            
            for (int i = 1; i < 6; i++) {
                payload = "Message " + i + " from Thing";
                message.setPayload(payload.getBytes());
                System.out.println("Set Payload: "+  payload);
                System.out.println(client.getClientId() + " published to topic: "+ publishTopicName);
                //Qos 1
                client.publish(publishTopicName, message);
            }
            
        } catch (MqttException me) {
        	System.out.println("ERROR " + me);
            me.printStackTrace();
        }

	}

}
