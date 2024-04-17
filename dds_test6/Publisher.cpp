#include <dds/DCPS/Service_Participant.h>
#include <dds/DCPS/Marked_Default_Qos.h>
#include <dds/DCPS/PublisherImpl.h>
#include <dds/DCPS/transport/tcp/TcpInst.h>
#include "dds/DCPS/StaticIncludes.h"

#include <ace/streams.h>

#include "DemoTypeSupportImpl.h"
using namespace DemoIdlModule;


int ACE_TMAIN(int argc, ACE_TCHAR* argv[]) {
    try {
        // ��ʼ��������
        argv[1] = "-DCPSConfigFile";
        argv[2] = "config_Pub.ini";
        argc = 3;
#if 1   //0. �ļ� //���������ļ�������Ȼ����ΪDDS������������ݡ�
        FILE* fp;
        //char c[] = "The counter is: 5";
        char c[] = "2";
        char buffer[50] = { 0 };
        //    char* buffer = { 0 };
        //    int bufsize = 0;
        long _counter = 0; //��������6.�������ݵ� message.counter

        char fname[80] = ".\\AAA.txt";
        int charCount = 0;/** �����ļ����ַ����� **/
        /* ���ļ����ڶ� */
        if ((fp = fopen(fname, "r")) == NULL)
        {
            printf("Open file failed!!\n");
            exit(1);
        }
        while (fgetc(fp) != EOF) /** ͳ���ַ����� **/
            charCount++;
        /* �����ļ��Ŀ�ͷ */
        fseek(fp, 0, SEEK_SET);

        /* ��ȡ����ʾ���� */
     //  fread(buffer, strlen(buffer) + 1, 1, fp);
        fread(buffer, charCount + 1, 1, fp);
        cout << buffer << endl;
        fclose(fp);

        /* �ַ���ת��long */
        _counter = strtol(buffer, NULL, 10);
        cout << "Begin!!! _counter: " << _counter << endl;
#endif  
        // 1. ��ʼ��������
        DDS::DomainParticipantFactory_var dpf =
            TheParticipantFactoryWithArgs(argc, argv);

        DDS::DomainParticipant_var participant =
            dpf->create_participant(111,
                PARTICIPANT_QOS_DEFAULT,
                DDS::DomainParticipantListener::_nil(),
                ::OpenDDS::DCPS::DEFAULT_STATUS_MASK);
        if (CORBA::is_nil(participant.in())) {
            cerr << "create_participant failed." << endl;
            return 1;
        }

        // 2. ע����������
        //������Topic������Topics�����岻ͬ��������idl�ļ��
        DemoTopic1TypeSupportImpl* servant = new  DemoTopic1TypeSupportImpl();//�����Ҫ����XXXXTypeSupportImpl�е�ǰ׺��idl�ļ��е�Topic key����Ӧ�������Ｔ"DemoTopic1"
        OpenDDS::DCPS::LocalObject_var safe_servant = servant;

        if (DDS::RETCODE_OK != servant->register_type(participant.in(), "")) {
            cerr << "register_type failed." << endl;
            exit(1);
        }

        // 3. ��������
        CORBA::String_var type_name = servant->get_type_name();

        DDS::TopicQos topic_qos;
        participant->get_default_topic_qos(topic_qos);
        DDS::Topic_var topic =
            participant->create_topic("Movie Discussion List",
                type_name.in(),
                topic_qos,
                DDS::TopicListener::_nil(),
                ::OpenDDS::DCPS::DEFAULT_STATUS_MASK);
        if (CORBA::is_nil(topic.in())) {
            cerr << "create_topic failed." << endl;
            exit(1);
        }

        // 4. ����������
        DDS::Publisher_var pub =
            participant->create_publisher(PUBLISHER_QOS_DEFAULT,
                DDS::PublisherListener::_nil(),
                ::OpenDDS::DCPS::DEFAULT_STATUS_MASK);
        if (CORBA::is_nil(pub.in())) {
            cerr << "create_publisher failed." << endl;
            exit(1);
        }

        // 5. ��������д��
        DDS::DataWriterQos dw_qos;
        pub->get_default_datawriter_qos(dw_qos);
        DDS::DataWriter_var dw =
            pub->create_datawriter(topic.in(),
                dw_qos,
                DDS::DataWriterListener::_nil(),
                ::OpenDDS::DCPS::DEFAULT_STATUS_MASK);
        if (CORBA::is_nil(dw.in())) {
            cerr << "create_datawriter failed." << endl;
            exit(1);
        }
        DemoTopic1DataWriter_var message_dw //�����Ҫ����XXXXDataWriter_var��XXXXDataWriter�е�ǰ׺��idl�ļ��е�Topic key����Ӧ�������Ｔ"DemoTopic1"
            = DemoTopic1DataWriter::_narrow(dw.in());

        //
        // Get default Publisher QoS from a DomainParticipant:
        DDS::PublisherQos pub_qos;
        DDS::ReturnCode_t ret;
        ret = participant->get_default_publisher_qos(pub_qos);

        if (DDS::RETCODE_OK != ret) {
            std::cerr << "Could not get default publisher QoS" << std::endl;
        }

        // Get default Subscriber QoS from a DomainParticipant:
        DDS::SubscriberQos sub_qos;
        ret = participant->get_default_subscriber_qos(sub_qos);
        if (DDS::RETCODE_OK != ret) {
            std::cerr << "Could not get default subscriber QoS" << std::endl;
        }

        // Get default Topic QoS from a DomainParticipant:
        DDS::TopicQos topic_qos2;
        ret = participant->get_default_topic_qos(topic_qos2);
        if (DDS::RETCODE_OK != ret) {
            std::cerr << "Could not get default topic QoS" << std::endl;
        }

        // Get default DomainParticipant QoS from a DomainParticipantFactory:
        DDS::DomainParticipantQos dp_qos;
        ret = dpf->get_default_participant_qos(dp_qos);
        if (DDS::RETCODE_OK != ret) {
            std::cerr << "Could not get default participant QoS" << std::endl;
        }

        // Get default DataWriter QoS from a Publisher:
        DDS::DataWriterQos dw_qos2;
        ret = pub->get_default_datawriter_qos(dw_qos2);
        if (DDS::RETCODE_OK != ret) {
            std::cerr << "Could not get default data writer QoS" << std::endl;
        }


        // 6. ��������
        DemoTopic1 message;//�����Ҫ����idl�ļ��е�Topic key����Ӧ�������Ｔ"DemoTopic1"
        message.id = 99;
        ::DDS::InstanceHandle_t handle = message_dw->register_instance(message);
        //   message.counter = 0;
#if 1
        message.counter = _counter;
        //message.text = "3-1";
        cout << "			RETT-message!!!: " << message.counter << endl;
#endif

        char tMsg[1200] = { 0 };
        while (1)
        {
            char fname[80] = ".\\AAA.txt";
            int charCount = 0;/** �����ļ����ַ����� **/
            /* ���ļ����ڶ� */
            if ((fp = fopen(fname, "r")) == NULL)
            {
                printf("Open file failed!!\n");
                exit(1);
            }
            while (fgetc(fp) != EOF) /** ͳ���ַ����� **/
                charCount++;
            /* �����ļ��Ŀ�ͷ */
            fseek(fp, 0, SEEK_SET);

            /* ��ȡ����ʾ���� */
         //  fread(buffer, strlen(buffer) + 1, 1, fp);
            fread(buffer, charCount + 1, 1, fp);
            //cout << buffer << endl;
            fclose(fp);

            message.counter++;
            memset(tMsg, 0, 1200);
            //sprintf(tMsg, "RETT-Msg Counter : %d", message.counter);
            memcpy(tMsg, buffer, sizeof(buffer));
            message.text = ::TAO::String_Manager(tMsg);
            message_dw->write(message, handle);
            //ACE_OS::sleep(1);
            ::Sleep(40);
            cout << "��ǰ����ָ�" << message.text << endl;
            //cout << "RETT..." << endl;
            cout << "����----->�Ż�             ��Ϣ������" << message.counter << endl;
        }


        // 7. ʵ������
        participant->delete_contained_entities();
        dpf->delete_participant(participant);
        TheServiceParticipant->shutdown();
    }
    catch (CORBA::Exception& e)
    {
        cerr << "PUB: Exception caught in main.cpp:" << endl
            << e << endl;
        exit(1);
    }

    return 0;
}
