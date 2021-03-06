using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using System;
using M2MqttUnity;
using Newtonsoft.Json.Linq;
using System.Linq ;
using Newtonsoft.Json;

[Serializable]
public class DataControl {
    public string device;
    public string status;

    public DataControl(string name, string isOn)
    {
        device = name;
        status = isOn;
    }
}


public class MqttUnityClient : M2MqttUnityClient
{
    public Text error;
    public Text nPeople;
    public Toggle doorToggle;
    public Toggle buzzerToggle;

    public InputField addressInputField;
    public InputField usernameInputField;
    public InputField passwordInputField;
    public Button connectButton;
    public CanvasGroup Panel1;
    public CanvasGroup Panel2;


    public List<string> topics = new List<string>();
    private bool updateUI = false;

    public void PublishTopics(String topic, String msg)
    {
        client.Publish(topic, System.Text.Encoding.UTF8.GetBytes(msg), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
        // Debug.Log("Publishing " + msg);
        error_msg("Test message published.");
    }

    public void Change_to_Panel_1()
    {
        Panel1.gameObject.SetActive(true);
        Panel2.gameObject.SetActive(false);
    }


    public void Change_to_Panel_2()
    {
        Panel1.gameObject.SetActive(false);
        Panel2.gameObject.SetActive(true);
    }

    public void Change_Door()
    {
        if (doorToggle.isOn)
        {
            PublishTopics(topics[2], "1");
        }
        else
        {
            PublishTopics(topics[2], "0");
        }
    }

    public void Change_Buzzer()
    {
        if (buzzerToggle.isOn)
        {
            PublishTopics(topics[1], "4");
        }
        else
        {
            PublishTopics(topics[1], "5");
        }
    }

    public void SetBrokerAddress(string brokerAddress)
    {
        if (addressInputField && !updateUI)
        {
            this.brokerAddress = brokerAddress;
        }
    }

    public void SetUsername(string username)
    {
        if (usernameInputField && !updateUI)
        {
            this.mqttUserName = username;
        }
    }

    public void SetPassword(string password)
    {
        if (passwordInputField && !updateUI)
        {
            this.mqttPassword = password;
        }
    }

    public void Message(string msg)
    {
        if (msg != null)
        {
            error.text = msg;
            updateUI = true;
        }
    }

    public void error_msg(string msg)
    {
        if (error != null)
        {
            error.text += msg + "\n";
            updateUI = true;
        }
    }

    protected override void OnConnecting()
    {
        base.OnConnecting();
        Message("Connecting to broker on " + brokerAddress + ":" + brokerPort.ToString() + "...\n");
    }

    protected override void OnConnected()
    {
        base.OnConnected();
        Message("Connected to broker on " + brokerAddress + "\n");
        SubscribeTopics();
        
        // client.Publish(topics[0], System.Text.Encoding.UTF8.GetBytes(JsonUtility.ToJson(new DataStatus(31f, 70f))), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
        Change_to_Panel_2();
    }

    protected override void SubscribeTopics()
    {
        foreach (string topic in topics)
        {
            client.Subscribe(new string[] { topic }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
        }
    }

    protected override void UnsubscribeTopics()
    {
        client.Unsubscribe(new string[] { topics[0] }); 
    }

    protected override void OnConnectionFailed(string errorMessage)
    {
        error_msg("CONNECTION FAILED! " + errorMessage);
    }

    protected override void OnDisconnected()
    {
        error_msg("Disconnected.");
    }

    protected override void OnConnectionLost()
    {
        error_msg("CONNECTION LOST!");
    }

    private void UpdateUI()
    {
        if (client == null)
        {
            if (connectButton != null)
            {
                connectButton.interactable = true;
            }
        }
        else
        {
            if (connectButton != null)
            {
                connectButton.interactable = !client.IsConnected;
            }
        }
        if (addressInputField != null && connectButton != null)
        {
            addressInputField.interactable = connectButton.interactable;
            addressInputField.text = brokerAddress;
        }
        if (usernameInputField != null && connectButton != null)
        {
            usernameInputField.interactable = connectButton.interactable;
            usernameInputField.text = mqttUserName;
        }
        if (passwordInputField != null && connectButton != null)
        {
            passwordInputField.interactable = connectButton.interactable;
            passwordInputField.text = mqttPassword;
        }
        updateUI = false;
    }

    protected override void Start()
    {
        updateUI = true;
        base.Start();
    }

    public void connectBtnOnClickStart()
    {
        autoConnect = true;
        SetBrokerAddress(this.addressInputField.text);
        SetUsername(this.usernameInputField.text);
        SetPassword(this.passwordInputField.text);
        base.Start();
    }

    protected override void DecodeMessage(string topic, byte[] message)
    {
        string msg = System.Text.Encoding.UTF8.GetString(message);
        Debug.Log("Received: " + msg);
        ProcessMessageStatus(topic, msg);
    }

    private void ProcessMessageStatus(string topic, string msg){
        if (topic == topics[0]){
            this.nPeople.text = msg;
        }
    }

    private void OnDestroy()
    {
        Disconnect();
    }

    private void OnValidate()
    {
        if (addressInputField != null)
        {
            addressInputField.text = brokerAddress;
        }
        if (usernameInputField != null)
        {
            usernameInputField.text = mqttUserName;
        }
        if (passwordInputField != null)
        {
            passwordInputField.text = mqttPassword;
        }
    }


}
