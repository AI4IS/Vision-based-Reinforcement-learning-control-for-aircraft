// -*- C++ -*-
//
#include "DataReaderListener.h"
#include "DemoTypeSupportC.h"
#include "DemoTypeSupportImpl.h"
#include <dds/DCPS/Service_Participant.h>
#include <ace/streams.h>

using namespace DemoIdlModule;

DataReaderListener::DataReaderListener()
    : num_reads_(0)
{
}

DataReaderListener::~DataReaderListener()
{
}

void DataReaderListener::on_data_available(DDS::DataReader_ptr reader)
{
    ++num_reads_;
    //0. 文件
    FILE* fp;
    //char c[] = "The counter is: 5";
    char c[50] = "2";
    char buffer[1200] = { 0 };
    long _counter = 0;
    char m_buffer[1200] = { 0 };
    /* 打开文件用于读写 */
    if (fp = fopen(".\\DDD.txt", "w+"))
        cout << "长机";



    try {
        DemoTopic1DataReader_var message_dr = DemoTopic1DataReader::_narrow(reader);
        if (CORBA::is_nil(message_dr.in())) {
            cerr << "read: _narrow failed." << endl;
            exit(1);
        }

        DemoTopic1 message;
        DDS::SampleInfo si;
        DDS::ReturnCode_t status = message_dr->take_next_sample(message, si);

        if (status == DDS::RETCODE_OK) {
            /*cout << "PP-Message: id    = " << message.id << endl
                << "         PP-DemoTopic1_Counter = " << message.counter << endl
                << "         PP-DemoTopic1_Text = " << message.text << endl;

            cout << "SampleInfo.sample_rank = " << si.sample_rank << endl;*/
            cout << "接收成功               消息计数：" << message.counter << endl;
            _counter = message.counter;
            memcpy(m_buffer, message.text, sizeof(message.text)+1);
        }
        else if (status == DDS::RETCODE_NO_DATA) {
            cerr << "ERROR: reader received DDS::RETCODE_NO_DATA!" << endl;
        }
        else {
            cerr << "ERROR: read Message: Error: " << status << endl;
        }
    }
    catch (CORBA::Exception& e) {
        cerr << "Exception caught in read:" << endl << e << endl;
        exit(1);
    }

    //ltoa(_counter, c, 10);

    /* 写入数据到文件 */
    //fwrite(c, strlen(c) + 1, 1, fp);
    fwrite(m_buffer, strlen(m_buffer) + 1, 1, fp);
    cout << "m_buffer:"<<m_buffer << endl;
    /* 查找文件的开头 */
    fseek(fp, 0, SEEK_SET);
    /* 读取并显示数据 */
    fread(buffer, strlen(m_buffer) + 1, 1, fp);
    cout << "当前订阅指令：" << buffer << endl;
    fclose(fp);
}

void DataReaderListener::on_requested_deadline_missed(
    DDS::DataReader_ptr,
    const DDS::RequestedDeadlineMissedStatus&)
{
    cerr << "DataReaderListener::on_requested_deadline_missed" << endl;
}

void DataReaderListener::on_requested_incompatible_qos(
    DDS::DataReader_ptr,
    const DDS::RequestedIncompatibleQosStatus&)
{
    cerr << "DataReaderListener::on_requested_incompatible_qos" << endl;
}

void DataReaderListener::on_liveliness_changed(
    DDS::DataReader_ptr,
    const DDS::LivelinessChangedStatus&)
{
    cerr << "DataReaderListener::on_liveliness_changed" << endl;
}

void DataReaderListener::on_subscription_matched(
    DDS::DataReader_ptr,
    const DDS::SubscriptionMatchedStatus&)
{
    cerr << "DataReaderListener::on_subscription_matched" << endl;
}

void DataReaderListener::on_sample_rejected(
    DDS::DataReader_ptr,
    const DDS::SampleRejectedStatus&)
{
    cerr << "DataReaderListener::on_sample_rejected" << endl;
}

void DataReaderListener::on_sample_lost(
    DDS::DataReader_ptr,
    const DDS::SampleLostStatus&)
{
    cerr << "DataReaderListener::on_sample_lost" << endl;
}

void DataReaderListener::on_subscription_disconnected(
    DDS::DataReader_ptr,
    const ::OpenDDS::DCPS::SubscriptionDisconnectedStatus&)
{
    cerr << "DataReaderListener::on_subscription_disconnected" << endl;
}

void DataReaderListener::on_subscription_reconnected(
    DDS::DataReader_ptr,
    const ::OpenDDS::DCPS::SubscriptionReconnectedStatus&)
{
    cerr << "DataReaderListener::on_subscription_reconnected" << endl;
}

void DataReaderListener::on_subscription_lost(
    DDS::DataReader_ptr,
    const ::OpenDDS::DCPS::SubscriptionLostStatus&)
{
    cerr << "DataReaderListener::on_subscription_lost" << endl;
}

void DataReaderListener::on_budget_exceeded(
    DDS::DataReader_ptr,
    const ::OpenDDS::DCPS::BudgetExceededStatus&)
{
    cerr << "DataReaderListener::on_budget_exceeded" << endl;
}
