package myBluzePanel;

import org.eclipse.paho.client.mqttv3.*;

public class SimpleMqttCallBack implements MqttCallback  {

	  public void connectionLost(Throwable throwable) {
	    System.out.println("Connection to MQTT broker lost!");
	  }
	  
	  @Override
	  public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
	    System.out.println("Message received:\n\t"+ new String(mqttMessage.getPayload()) );
	  }

	  public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
	    // not used in this example
	  }
	}