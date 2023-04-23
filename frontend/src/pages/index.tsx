import { Inter } from 'next/font/google'
import {AutoComplete, Descriptions, Image, Input, Modal, Progress, Table, Tabs, Typography} from "antd";
import React, {useEffect, useState} from "react";
import _, {set} from "lodash";
import {ColumnsType} from "antd/lib/table";
const {Title, Text} = Typography;

// const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  const [options, setOptions] = useState<any[]>([]);
  const [activeResult, setActiveResult] = useState<string>('');
  const [activeTab, setActiveTab] = useState('clinicalTrials');
  const [selectedOptionCasesData, setSelectedOptionCasesData] = useState<any>(null);
  const [selectedOptionClinicalData, setSelectedOptionClinicalData] = useState<any>(null);
  const [progressBarPercent, setProgressBarPercent] = useState(0);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modalData, setModalData] = useState<any>(null);
  const [quote, setQuote] = useState<any>({quote: '', author: ''});
  const [loading, setLoading] = useState(false);
  const fetchSelectedOptionCasesData = (value: string) => {
        fetch(`http://127.0.0.1:5000/gdc_cases?primary_diagnosis=${value}`, {
            method: 'GET',
        }).then((response) => response.json())
            .then((data) => {
                setSelectedOptionCasesData(data)
            })
  }
    const fetchSelectedOptionClinicalData = (value: string) => {
        fetch(`http://127.0.0.1:5000/clinical_trials?expr=${value}`, {
            method: 'GET',
        }).then((response) => response.json())
            .then((data) => {
                setSelectedOptionClinicalData(data)
            })
        }
    useEffect(() => {
        if (!_.isNil(selectedOptionCasesData) && !_.isNil(selectedOptionClinicalData)) {
            setProgressBarPercent(100);
        }
        else {
            setTimeout(() => {
                getQuote();
            }, 5000)
        }
    }, [selectedOptionCasesData, selectedOptionClinicalData])
    const fetchNewClinicalTrials = (value: string, filterData: any) => {
      const getFilterParams = _.join(_.compact(_.map(_.keys(filterData), (item) => {
          if (!_.isEmpty(filterData[item])) {
              const filterName = item === 'age' ? 'age_filter' : item === 'gender' ? 'gender_filter' : item === 'phase' ? 'phase_filter' : 'status_filter';
              return `${filterName}=[${_.join(_.map(filterData[item], (filterValue) => {
                      return `\"${filterValue}\"`
                  }), ','
              )}]`
          }
          return undefined;
      })), '&');
      setLoading(true);
      fetch(`http://127.0.0.1:5000/clinical_trials?expr=${activeResult}&${getFilterParams}`)
          .then((response) => response.json())
          .then((data) => {
              setSelectedOptionClinicalData(data)
              setLoading(false);
          })
    }
  const getQuote = () => {
      fetch(`https://type.fit/api/quotes`, {
            method: 'GET',
      }).then((response) => response.json())
        .then((data) => {
            const randomIndex = _.random(0, data.length - 1);
            setQuote({
                quote: data[randomIndex].text,
                author: data[randomIndex].author,
            })
        })
  }
  const getNewOptions = (text: string) => {
      fetch(`http://127.0.0.1:5000/search_terms?term=${text}`, {
          method: 'GET',
      })
        .then((response) => response.json())
        .then((data) => {
            setOptions(data.map((item: any) => ({ value: item.term, label: item.term })))
        })
  }
  useEffect(() => {
      if (progressBarPercent === 0) {
          getQuote();
          setTimeout(() => {
              setProgressBarPercent(_.random(35, 40));
          }, 500)
          return;
      }
      if (progressBarPercent >= 35 && progressBarPercent <= 40) {
          setTimeout(() => {
              setProgressBarPercent(_.random(50, 56));
          }, 700)
          return;
      }
      if (progressBarPercent >= 50 && progressBarPercent <= 56) {
          setTimeout(() => {
              setProgressBarPercent(_.random(70, 80));
          }, 1200)
          return;
      }
  }, [progressBarPercent])
    const clinicalTrialColumns:ColumnsType<any> = [
        {
            title: 'Title',
            dataIndex: 'title',
            render: (text: string, record) => {
                return (
                    <a
                        style={{color: '#1890ff'}}
                        onClick={() => {
                            setModalData(record);
                            setIsModalVisible(true);
                        }}
                    >
                        {text}
                    </a>
                )
            }
        },
        {
            title: 'Age',
            dataIndex: 'age',
            render: (text: string, record) => {
                return (
                    _.join(_.split(text, ','), ', ')
                )
            },
            filters: [
                {
                    value: 'Child',
                    text: 'Child',
                },
                {
                    value: 'Adult',
                    text: 'Adult',
                },
                {
                    value: 'Older Adult',
                    text: 'Older Adult',
                }
            ]
        },
        {
            title: 'Gender',
            dataIndex: 'gender',
            filters: [
                {
                    text: 'All',
                    value: 'All',
                },
                {
                    text: 'Only Male',
                    value: 'Male',
                },
                {
                    text: 'Only Female',
                    value: 'Female'
                }
            ],
            filterMultiple: false,
        },
        {
            title: 'Phase',
            dataIndex: 'phase',
            render: (text: string, record) => {
                return (
                    _.join(_.split(text, ','), ', ')
                )
            },
            filters: [
                {
                    value: 'Early Phase 1',
                    text: 'Early Phase 1',
                },
                {
                    value: 'Phase 1',
                    text: 'Phase 1',
                },
                {
                    value: 'Phase 2',
                    text: 'Phase 2',
                },
                {
                    value: 'Phase 3',
                    text: 'Phase 3',
                },
                {
                    value: 'Phase 4',
                    text: 'Phase 4',
                },
                {
                    value: 'Not Applicable',
                    text: 'Not Applicable',
                }
            ],
        },
        {
            title: 'Status',
            dataIndex: 'status',
            filters: [
                {
                    value: 'Active, not recruiting',
                    text: 'Active, not recruiting',
                },
                {
                    value: 'Not yet recruiting',
                    text: 'Not yet recruiting',
                },
                {
                    value: 'Recruiting',
                    text: 'Recruiting',
                },
                {
                    value: 'Enrolling by invitation',
                    text: 'Enrolling by invitation',
                },
                {
                    value: 'Completed',
                    text: 'Completed',
                },
                {
                    value: 'Terminated',
                    text: 'Terminated',
                },
                {
                    value: 'Suspended',
                    text: 'Suspended',
                },
                {
                    value: 'Withdrawn',
                    text: 'Withdrawn',
                },
                {
                    value: 'Unknown status',
                    text: 'Unknown status',
                }
            ],
            filterMultiple: false,
        },
        {
            title: 'Term',
            dataIndex: 'term',
        },
    ]
    const caseStudiesColumns: ColumnsType<any> = [
        {
            title: 'Case ID',
            dataIndex: 'submitter_id',
            render: (text: string, record) => (
                <a
                    style={{color: '#1890ff'}}
                    href={`https://portal.gdc.cancer.gov/cases/${record.case_id}`}
                    target={'_blank'}>
                    {text}
                </a>
            )
        },
        {
            title: 'Age',
            dataIndex: 'age_at_diagnosis',
        },
        {
            title: 'Disease Type',
            dataIndex: 'disease_type',
        },
        {
            title: 'Primary Diagnosis',
            dataIndex: 'primary_diagnosis',
        },
        {
            title: 'Primary Site',
            dataIndex: 'primary_site',
        },
        {
            title: 'Site of Resection or Biopsy',
            dataIndex: 'site_of_resection_or_biopsy'
        },
        {
            title: 'Tissue Source Site',
            dataIndex: 'tissue_source_site',
        },
        {
            title: 'Year of Diagnosis',
            dataIndex: 'year_of_diagnosis',
        },
    ]
  return (
    <>
        <div style={{ display: 'flex', flexDirection: 'column', width: '100%', alignItems: 'center', justifyContent: 'center', marginTop: '2rem'}}>
            <Modal
                open={isModalVisible}
                width={'75vw'}
                onCancel={() => {
                    setIsModalVisible(false)
                }}
                footer={null}
                destroyOnClose={true}
                bodyStyle={{height: '75vh', overflowX: 'scroll'}}
            >
                <Title level={4} style={{marginTop: '0rem', marginBottom: '1rem'}}>
                    {modalData?.title}
                </Title>
                <Descriptions
                    title="Descriptive Information"
                    bordered
                    layout={'horizontal'}
                    style={{width: '100%'}}
                >
                    <Descriptions.Item label="Brief Title" span={3}>{modalData?.title}</Descriptions.Item>
                    <Descriptions.Item label="Official Title" span={3}>{modalData?.official_title}</Descriptions.Item>
                    <Descriptions.Item label="Brief Summary" span={3}>{modalData?.summary}</Descriptions.Item>
                    <Descriptions.Item label="Detailed Description" span={3}>{modalData?.description}</Descriptions.Item>
                    <Descriptions.Item label="Study Type" span={3}>{modalData?.study_type}</Descriptions.Item>
                    <Descriptions.Item label="Condition" span={3}>{modalData?.condition}</Descriptions.Item>
                </Descriptions>
                <Descriptions
                    title="Recruitment Information"
                    bordered
                    layout={'horizontal'}
                    style={{width: '100%', marginTop: '1rem'}}
                >
                    <Descriptions.Item label="Recruitment Status" span={3}>{modalData?.status}</Descriptions.Item>
                    <Descriptions.Item label="Actual Study Completion Date" span={3}>{modalData?.study_completion_date}</Descriptions.Item>
                    <Descriptions.Item label="Actual Primary Completion Date" span={3}>{modalData?.primary_completion_date}</Descriptions.Item>
                    <Descriptions.Item label="Detailed Description" span={3}>{modalData?.description}</Descriptions.Item>
                    <Descriptions.Item label="Eligibility Criteria" span={3}>{modalData?.eligibility_criteria}</Descriptions.Item>
                    <Descriptions.Item label="Sex/Gender" span={3}>{modalData?.gender}</Descriptions.Item>
                    <Descriptions.Item label="Ages" span={3}>{_.join(_.split(modalData?.age, ','), ', ')}</Descriptions.Item>
                    <Descriptions.Item label="Condition" span={3}>{modalData?.condition}</Descriptions.Item>
                </Descriptions>
                <Descriptions
                    title="Administrative Information"
                    bordered
                    layout={'horizontal'}
                    style={{width: '100%', marginTop: '1rem'}}
                >
                    <Descriptions.Item label="NCT Number" span={3}>{modalData?.nct_id}</Descriptions.Item>
                    <Descriptions.Item label="Collaborator" span={3}>{_.join(_.map(modalData?.collaborators, 'CollaboratorName'), ', ')}</Descriptions.Item>
                    <Descriptions.Item label="Investigators">
                        <pre>
                            {
                                _.join(_.map(modalData?.investigator, (investigatorData) => {
                                    return `${investigatorData?.OverallOfficialRole}:  ${investigatorData?.OverallOfficialName}   ${investigatorData.OverallOfficialAffiliation}`
                                }), '\n\n')
                            }
                        </pre>
                    </Descriptions.Item>
                </Descriptions>
            </Modal>
            <Image
                src={'/carets-logo.jpeg'}
                width={'15rem'}
                alt={''}
                height={'auto'}
                style={{
                    objectFit: 'cover',
                }}
                preview={false}
            />
            <AutoComplete
                options={options}
                style={{ marginTop: '2rem' }}
                onSelect={(value, option) => {
                    setSelectedOptionCasesData(undefined);
                    setSelectedOptionClinicalData(undefined);
                    setProgressBarPercent(0)
                    setActiveResult(value)
                    fetchSelectedOptionCasesData(value)
                    fetchSelectedOptionClinicalData(value)
                }}
                onSearch={(text) => getNewOptions(text)}
            >
                <Input
                    size="large"
                    placeholder="input here"
                    style={{width: '80vw'}}
                />
            </AutoComplete>
            {
                !_.isNil(activeResult) && !_.isNil(selectedOptionClinicalData) && !_.isNil(selectedOptionCasesData) ?
                <>
                    <Tabs
                        items={[{
                            label: 'Clinical Trials',
                            key: 'clinicalTrials',
                        }, {
                            label: 'Case Studies',
                            key: 'caseStudies',
                        }]}
                        defaultActiveKey={activeTab}
                        onChange={async (key) => {
                            setActiveTab(key)
                        }}
                        style={{ width: '80vw', marginTop: '2rem' }}
                    />
                    {
                        activeTab === 'clinicalTrials' ?
                        <Table
                            style={{width: '80vw'}}
                            dataSource={selectedOptionClinicalData}
                            columns={clinicalTrialColumns}
                            loading={loading}
                            onChange={(pagination, filters, sorter, extra) => {
                                fetchNewClinicalTrials(activeResult, filters)
                            }}
                        /> :
                        <Table style={{width: '80vw'}} dataSource={selectedOptionCasesData} columns={caseStudiesColumns} loading={loading}/>
                    }
                </> :
                !_.isEmpty(activeResult) ?
                <div style={{ width: '70vw', marginTop: '2rem' }}>
                    <Progress width={100} percent={progressBarPercent} />
                    <div style={{display: 'flex', width: '70vw', marginTop: '2rem', paddingLeft: '10vw',  paddingRight: '10vw', flexDirection: 'column'}}>
                        <Text style={{fontSize: '2rem'}}>
                            {quote.quote}
                        </Text>
                        <Text style={{fontSize: '1.5rem', color: '#656565'}}>
                            {'-'}{quote.author ?? 'Unknown'}
                        </Text>
                    </div>
                </div> :
                null
            }
        </div>
      {/*<Text style={{}}>*/}

      {/*</Text>*/}
    </>
  )
}
