const ENTITIES=[
{id:'E000',name:'Group Co',level:0,parent:'',l1:'',country:'UK',city:'London',address:'5 Aldermanbury Sq, London EC2V 7HR',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E001',name:'Bank Co',level:1,parent:'E000',l1:'Bank Co',country:'UK',city:'London',address:'8 Cornhill, London EC3V 3ND',rfi:'RFB',rf:'CORE',crr:''},
{id:'E002',name:'Property Co',level:1,parent:'E000',l1:'Property Co',country:'UK',city:'London',address:'1 Poultry, London EC2R 8EJ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E003',name:'Wealth Co',level:1,parent:'E000',l1:'Wealth Co',country:'UK',city:'London',address:'6 Lothbury, London EC2R 7HH',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E004',name:'Market Co',level:1,parent:'E000',l1:'Market Co',country:'UK',city:'London',address:'25 Old Broad St, London EC2N 1HQ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E005',name:'Retail Co',level:2,parent:'E001',l1:'Bank Co',country:'UK',city:'London',address:'30 St Mary Axe, London EC3A 8EP',rfi:'RFB',rf:'CORE',crr:''},
{id:'E006',name:'Corp Co',level:2,parent:'E001',l1:'Bank Co',country:'AU',city:'Sydney',address:'1 Martin Pl, Sydney NSW 2000',rfi:'RFB',rf:'NON CORE',crr:''},
{id:'E007',name:'Fin Co',level:2,parent:'E001',l1:'Bank Co',country:'UK',city:'London',address:'1 Poultry, London EC2R 8EJ',rfi:'RFB',rf:'CORE',crr:''},
{id:'E008',name:'Lend Co',level:3,parent:'E005',l1:'Bank Co',country:'UK',city:'London',address:'1 London Wall, London EC2Y 5AB',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E009',name:'Deposit Co',level:3,parent:'E007',l1:'Bank Co',country:'UK',city:'London',address:'1 Leadenhall St, London EC3V 1PP',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E010',name:'FX Co',level:3,parent:'E005',l1:'Bank Co',country:'UK',city:'London',address:'6 Lothbury, London EC2R 7HH',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E011',name:'Trade Co',level:3,parent:'E007',l1:'Bank Co',country:'UK',city:'London',address:'20 Fenchurch St, London EC3M 3BY',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E012',name:'Credit Co',level:3,parent:'E007',l1:'Bank Co',country:'UK',city:'London',address:'1 Poultry, London EC2R 8EJ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E013',name:'Issuer Co',level:3,parent:'E005',l1:'Bank Co',country:'UK',city:'London',address:'10 Gresham St, London EC2V 7JD',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E014',name:'Card Co',level:4,parent:'E010',l1:'Bank Co',country:'UK',city:'London',address:'10 Gresham St, London EC2V 7JD',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E015',name:'Repo Co',level:4,parent:'E008',l1:'Bank Co',country:'UK',city:'London',address:'8 Cornhill, London EC3V 3ND',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E016',name:'Settle Co',level:4,parent:'E010',l1:'Bank Co',country:'DE',city:'Berlin',address:'Unter den Linden 13, Berlin 10117',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E017',name:'Clear Co',level:4,parent:'E013',l1:'Bank Co',country:'UK',city:'London',address:'8 Cornhill, London EC3V 3ND',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E018',name:'Custody Co',level:4,parent:'E011',l1:'Bank Co',country:'UK',city:'London',address:'25 Old Broad St, London EC2N 1HQ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E019',name:'Vox Co',level:5,parent:'E018',l1:'Bank Co',country:'SG',city:'Singapore',address:'8 Marina Blvd, Singapore 018981',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E020',name:'Virtus Co',level:5,parent:'E014',l1:'Bank Co',country:'UK',city:'London',address:'1 London Wall, London EC2Y 5AB',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E021',name:'Verus Co',level:5,parent:'E016',l1:'Bank Co',country:'BR',city:'Sao Paulo',address:'Av Paulista 1374, Sao Paulo SP 01310-100',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E022',name:'Victor Co',level:6,parent:'E020',l1:'Bank Co',country:'UK',city:'London',address:'5 Aldermanbury Sq, London EC2V 7HR',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E023',name:'Resi Co',level:2,parent:'E002',l1:'Property Co',country:'US',city:'New York',address:'11 Times Sq, New York NY 10036',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E024',name:'Comm Co',level:2,parent:'E002',l1:'Property Co',country:'UK',city:'London',address:'25 Old Broad St, London EC2N 1HQ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E025',name:'Dev Co',level:3,parent:'E023',l1:'Property Co',country:'UK',city:'London',address:'30 St Mary Axe, London EC3A 8EP',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E026',name:'Lease Co',level:3,parent:'E023',l1:'Property Co',country:'UK',city:'London',address:'1 Angel Ct, London EC2R 7HJ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E027',name:'Asset Co',level:3,parent:'E024',l1:'Property Co',country:'AU',city:'Sydney',address:'60 Margaret St, Sydney NSW 2000',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E028',name:'Land Co',level:3,parent:'E024',l1:'Property Co',country:'CA',city:'Toronto',address:'200 Bay St, Toronto ON M5J 2J2',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E029',name:'Build Co',level:3,parent:'E023',l1:'Property Co',country:'JP',city:'Tokyo',address:'1-1 Marunouchi 2-chome, Tokyo Chiyoda 100-0005',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E030',name:'Infra Co',level:4,parent:'E026',l1:'Property Co',country:'DE',city:'Berlin',address:'Potsdamer Pl 1, Berlin 10785',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E031',name:'Mgmt Co',level:4,parent:'E026',l1:'Property Co',country:'UK',city:'London',address:'1 Angel Ct, London EC2R 7HJ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E032',name:'Hold Co',level:4,parent:'E028',l1:'Property Co',country:'UK',city:'London',address:'30 St Mary Axe, London EC3A 8EP',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E033',name:'REIT Co',level:4,parent:'E026',l1:'Property Co',country:'DE',city:'Berlin',address:'Kurfürstendamm 22, Berlin 10719',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E034',name:'Vita Co',level:5,parent:'E033',l1:'Property Co',country:'UK',city:'London',address:'30 St Mary Axe, London EC3A 8EP',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E035',name:'Valor Co',level:5,parent:'E033',l1:'Property Co',country:'UK',city:'London',address:'1 Poultry, London EC2R 8EJ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E036',name:'Via Co',level:6,parent:'E034',l1:'Property Co',country:'UK',city:'London',address:'30 St Mary Axe, London EC3A 8EP',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E037',name:'Priv Co',level:2,parent:'E003',l1:'Wealth Co',country:'JP',city:'Tokyo',address:'1-1 Marunouchi 2-chome, Tokyo Chiyoda 100-0005',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E038',name:'Trust Co',level:2,parent:'E003',l1:'Wealth Co',country:'UK',city:'London',address:'100 Cheapside, London EC2V 6DT',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E039',name:'Fund Co',level:3,parent:'E038',l1:'Wealth Co',country:'UK',city:'London',address:'1 Leadenhall St, London EC3V 1PP',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E040',name:'Fisc Co',level:3,parent:'E037',l1:'Wealth Co',country:'UK',city:'London',address:'8 Cornhill, London EC3V 3ND',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E041',name:'Plan Co',level:3,parent:'E038',l1:'Wealth Co',country:'SG',city:'Singapore',address:'30 Raffles Pl, Singapore 048622',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E042',name:'Heir Co',level:3,parent:'E038',l1:'Wealth Co',country:'UK',city:'London',address:'1 Poultry, London EC2R 8EJ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E043',name:'Endow Co',level:3,parent:'E038',l1:'Wealth Co',country:'CA',city:'Toronto',address:'100 King St W, Toronto ON M5X 1A9',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E044',name:'Invest Co',level:4,parent:'E041',l1:'Wealth Co',country:'JP',city:'Tokyo',address:'1-1 Marunouchi 2-chome, Tokyo Chiyoda 100-0005',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E045',name:'Annuity Co',level:4,parent:'E040',l1:'Wealth Co',country:'UK',city:'London',address:'30 St Mary Axe, London EC3A 8EP',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E046',name:'Pens Co',level:4,parent:'E043',l1:'Wealth Co',country:'HK',city:'Hong Kong',address:'1 Exchange Sq, Hong Kong Central HK',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E047',name:'Bond Co',level:4,parent:'E043',l1:'Wealth Co',country:'UK',city:'London',address:'1 Poultry, London EC2R 8EJ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E048',name:'Vigor Co',level:5,parent:'E044',l1:'Wealth Co',country:'BR',city:'Sao Paulo',address:'Av Brigadeiro Faria Lima 3400, Sao Paulo SP 04538-132',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E049',name:'Visus Co',level:5,parent:'E045',l1:'Wealth Co',country:'UK',city:'London',address:'100 Cheapside, London EC2V 6DT',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E050',name:'Aqua Co',level:6,parent:'E048',l1:'Wealth Co',country:'UK',city:'London',address:'20 Fenchurch St, London EC3M 3BY',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E051',name:'Equit Co',level:2,parent:'E004',l1:'Market Co',country:'HK',city:'Hong Kong',address:'8 Finance St, Hong Kong Central HK',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E052',name:'Deriv Co',level:2,parent:'E004',l1:'Market Co',country:'UK',city:'London',address:'20 Fenchurch St, London EC3M 3BY',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E053',name:'Trading Co',level:3,parent:'E051',l1:'Market Co',country:'US',city:'New York',address:'245 Park Ave, New York NY 10167',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E054',name:'Securities Co',level:3,parent:'E052',l1:'Market Co',country:'HK',city:'Hong Kong',address:'8 Finance St, Hong Kong Central HK',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E055',name:'Broker Co',level:4,parent:'E053',l1:'Market Co',country:'UK',city:'London',address:'1 Angel Ct, London EC2R 7HJ',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E056',name:'Agency Co',level:4,parent:'E053',l1:'Market Co',country:'AU',city:'Sydney',address:'8 Chifley Sq, Sydney NSW 2000',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E057',name:'Exec Co',level:4,parent:'E054',l1:'Market Co',country:'JP',city:'Tokyo',address:'1-1 Marunouchi 2-chome, Tokyo Chiyoda 100-0005',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E058',name:'Report Co',level:4,parent:'E054',l1:'Market Co',country:'UK',city:'London',address:'10 Gresham St, London EC2V 7JD',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E059',name:'Aura Co',level:5,parent:'E055',l1:'Market Co',country:'UK',city:'London',address:'1 London Wall, London EC2Y 5AB',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E060',name:'Axis Co',level:5,parent:'E056',l1:'Market Co',country:'UK',city:'London',address:'6 Lothbury, London EC2R 7HH',rfi:'NRFB',rf:'NRFB',crr:''},
{id:'E061',name:'Alba Co',level:6,parent:'E059',l1:'Market Co',country:'UK',city:'London',address:'1 Poultry, London EC2R 8EJ',rfi:'NRFB',rf:'NRFB',crr:''}
];

const LIMIT_TYPES=[
{product:'FX Forward',lt:'Hard',lst:'Traded'},
{product:'Committed Repo',lt:'Hard',lst:'Traded'},
{product:'Committed Loan',lt:'Hard',lst:'Lending'},
{product:'Overdraft',lt:'Hard',lst:'Lending'},
{product:'Bond Borrow',lt:'Hard',lst:'Traded'},
{product:'Xccy Swap',lt:'Hard',lst:'Traded'},
{product:'Payment Intraday',lt:'Soft',lst:'Settlement'}
];

const LIMITS_EXP=[
{id:'LIM0001',product:'Committed Repo',crid:'E021',deid:'E016',lim:499000,exp:-20000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0002',product:'Bond Borrow',crid:'E003',deid:'E047',lim:143176000,exp:63907000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0003',product:'Overdraft',crid:'E056',deid:'E033',lim:7292000,exp:3690000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0004',product:'Payment Intraday',crid:'E046',deid:'E050',lim:4034000,exp:2496000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0005',product:'Payment Intraday',crid:'E005',deid:'E043',lim:47519000,exp:-4773000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0006',product:'FX Forward',crid:'E041',deid:'E044',lim:14602000,exp:4135000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0007',product:'Committed Repo',crid:'E011',deid:'E001',lim:11513000,exp:10589000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0008',product:'Committed Repo',crid:'E002',deid:'E034',lim:128992000,exp:125387000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0009',product:'Payment Intraday',crid:'E054',deid:'E014',lim:13810000,exp:12565000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0010',product:'Committed Repo',crid:'E006',deid:'E034',lim:7780000,exp:-1338000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0011',product:'FX Forward',crid:'E025',deid:'E052',lim:28164000,exp:15727000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0012',product:'Overdraft',crid:'E005',deid:'E040',lim:29727000,exp:12726000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0013',product:'FX Forward',crid:'E007',deid:'E050',lim:53033000,exp:17584000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0014',product:'Committed Repo',crid:'E029',deid:'E052',lim:11260000,exp:7139000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0015',product:'Payment Intraday',crid:'E054',deid:'E012',lim:21833000,exp:16041000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0016',product:'FX Forward',crid:'E005',deid:'E059',lim:12236000,exp:-338000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0017',product:'Committed Repo',crid:'E006',deid:'E015',lim:74310000,exp:63648000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0018',product:'Committed Repo',crid:'E014',deid:'E033',lim:8500000,exp:-504000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0019',product:'FX Forward',crid:'E048',deid:'E015',lim:1027000,exp:-192000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0020',product:'Overdraft',crid:'E049',deid:'E023',lim:828000,exp:652000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0021',product:'Committed Loan',crid:'E020',deid:'E028',lim:1092000,exp:19000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0022',product:'Payment Intraday',crid:'E001',deid:'E026',lim:91744000,exp:30530000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0023',product:'Xccy Swap',crid:'E013',deid:'E043',lim:21879000,exp:-1599000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0024',product:'Payment Intraday',crid:'E039',deid:'E022',lim:24469000,exp:14905000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0025',product:'Payment Intraday',crid:'E010',deid:'E021',lim:28814000,exp:24752000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0026',product:'FX Forward',crid:'E023',deid:'E057',lim:42736000,exp:37977000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0027',product:'Bond Borrow',crid:'E052',deid:'E050',lim:14546000,exp:12731000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0028',product:'Xccy Swap',crid:'E023',deid:'E021',lim:66974000,exp:-582000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0029',product:'Payment Intraday',crid:'E018',deid:'E044',lim:9876000,exp:5927000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0030',product:'Committed Repo',crid:'E024',deid:'E026',lim:30904000,exp:18557000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0031',product:'Committed Repo',crid:'E040',deid:'E060',lim:26849000,exp:16146000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0032',product:'Overdraft',crid:'E045',deid:'E019',lim:7494000,exp:6291000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0033',product:'Committed Loan',crid:'E009',deid:'E055',lim:20040000,exp:-3921000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0034',product:'Bond Borrow',crid:'E027',deid:'E016',lim:10006000,exp:6071000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0035',product:'Payment Intraday',crid:'E043',deid:'E014',lim:24368000,exp:22411000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0036',product:'Overdraft',crid:'E011',deid:'E054',lim:14573000,exp:6372000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0037',product:'Payment Intraday',crid:'E035',deid:'E041',lim:1232000,exp:179000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0038',product:'Payment Intraday',crid:'E042',deid:'E061',lim:9918000,exp:4925000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0039',product:'Committed Loan',crid:'E057',deid:'E029',lim:9715000,exp:5360000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0040',product:'Committed Repo',crid:'E041',deid:'E037',lim:22943000,exp:22718000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0041',product:'Committed Repo',crid:'E046',deid:'E027',lim:2832000,exp:552000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0042',product:'Payment Intraday',crid:'E052',deid:'E057',lim:68767000,exp:44163000,currency:'GBP',crr:'Deriv Co_NRFB'},
{id:'LIM0043',product:'Committed Repo',crid:'E023',deid:'E060',lim:31988000,exp:1572000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0044',product:'Xccy Swap',crid:'E025',deid:'E054',lim:12097000,exp:9581000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0045',product:'Xccy Swap',crid:'E056',deid:'E032',lim:8920000,exp:3315000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0046',product:'Committed Repo',crid:'E006',deid:'E008',lim:79789000,exp:34135000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0047',product:'FX Forward',crid:'E004',deid:'E050',lim:80435000,exp:54734000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0048',product:'Xccy Swap',crid:'E031',deid:'E035',lim:367000,exp:67000,currency:'GBP',crr:'Resi Co_NRFB'},
{id:'LIM0049',product:'FX Forward',crid:'E010',deid:'E012',lim:12521000,exp:-1787000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0050',product:'Committed Loan',crid:'E027',deid:'E036',lim:5597000,exp:1830000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0051',product:'Payment Intraday',crid:'E040',deid:'E029',lim:6466000,exp:2467000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0052',product:'FX Forward',crid:'E011',deid:'E043',lim:17231000,exp:653000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0053',product:'Xccy Swap',crid:'E030',deid:'E046',lim:9610000,exp:4247000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0054',product:'Committed Repo',crid:'E042',deid:'E011',lim:24927000,exp:-493000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0055',product:'Xccy Swap',crid:'E003',deid:'E048',lim:88264000,exp:19832000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0056',product:'Bond Borrow',crid:'E045',deid:'E018',lim:7665000,exp:4088000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0057',product:'Committed Loan',crid:'E015',deid:'E006',lim:8142000,exp:2633000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0058',product:'Committed Repo',crid:'E013',deid:'E048',lim:15400000,exp:14784000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0059',product:'Overdraft',crid:'E042',deid:'E002',lim:27588000,exp:20744000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0060',product:'Bond Borrow',crid:'E045',deid:'E061',lim:4578000,exp:3440000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0061',product:'Payment Intraday',crid:'E052',deid:'E009',lim:17107000,exp:14855000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0062',product:'Committed Loan',crid:'E006',deid:'E030',lim:28505000,exp:-4141000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0063',product:'Committed Repo',crid:'E020',deid:'E021',lim:309000,exp:-58000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0064',product:'Committed Loan',crid:'E012',deid:'E036',lim:4585000,exp:1435000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0065',product:'Bond Borrow',crid:'E002',deid:'E024',lim:143040000,exp:116706000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0066',product:'FX Forward',crid:'E038',deid:'E050',lim:33249000,exp:4150000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0067',product:'Xccy Swap',crid:'E009',deid:'E013',lim:1538000,exp:1285000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0068',product:'Bond Borrow',crid:'E012',deid:'E027',lim:21753000,exp:15873000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0069',product:'FX Forward',crid:'E006',deid:'E028',lim:20912000,exp:12074000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0070',product:'Overdraft',crid:'E006',deid:'E036',lim:5324000,exp:4964000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0071',product:'Committed Repo',crid:'E050',deid:'E012',lim:318000,exp:-40000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0072',product:'Payment Intraday',crid:'E052',deid:'E015',lim:37297000,exp:-7315000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0073',product:'Overdraft',crid:'E037',deid:'E034',lim:10552000,exp:5338000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0074',product:'Bond Borrow',crid:'E015',deid:'E012',lim:1137000,exp:457000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0075',product:'Committed Repo',crid:'E009',deid:'E037',lim:21749000,exp:-1728000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0076',product:'Committed Repo',crid:'E034',deid:'E057',lim:312000,exp:214000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0077',product:'Committed Loan',crid:'E010',deid:'E053',lim:5867000,exp:2458000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0078',product:'Payment Intraday',crid:'E046',deid:'E058',lim:5546000,exp:453000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0079',product:'Overdraft',crid:'E028',deid:'E045',lim:12467000,exp:5905000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0080',product:'Bond Borrow',crid:'E009',deid:'E022',lim:10691000,exp:288000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0081',product:'FX Forward',crid:'E046',deid:'E004',lim:4508000,exp:803000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0082',product:'Committed Repo',crid:'E055',deid:'E043',lim:2865000,exp:2601000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0083',product:'Committed Loan',crid:'E010',deid:'E037',lim:6691000,exp:1589000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0084',product:'Xccy Swap',crid:'E005',deid:'E027',lim:27879000,exp:3135000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0085',product:'FX Forward',crid:'E024',deid:'E059',lim:31621000,exp:-969000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0086',product:'FX Forward',crid:'E002',deid:'E055',lim:84591000,exp:15359000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0087',product:'Payment Intraday',crid:'E018',deid:'E035',lim:972000,exp:-161000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0088',product:'Committed Loan',crid:'E008',deid:'E023',lim:23056000,exp:-2662000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0089',product:'Overdraft',crid:'E000',deid:'E011',lim:86434000,exp:70256000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0090',product:'Bond Borrow',crid:'E041',deid:'E033',lim:26406000,exp:19044000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0091',product:'Xccy Swap',crid:'E053',deid:'E019',lim:11001000,exp:-660000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0092',product:'FX Forward',crid:'E028',deid:'E007',lim:7371000,exp:1410000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0093',product:'Bond Borrow',crid:'E003',deid:'E055',lim:132476000,exp:7309000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0094',product:'Bond Borrow',crid:'E038',deid:'E034',lim:60778000,exp:-6493000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0095',product:'Committed Loan',crid:'E018',deid:'E047',lim:5068000,exp:4714000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0096',product:'Payment Intraday',crid:'E047',deid:'E030',lim:9312000,exp:1723000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0097',product:'Bond Borrow',crid:'E061',deid:'E039',lim:462000,exp:388000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0098',product:'Committed Repo',crid:'E054',deid:'E027',lim:2976000,exp:2709000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0099',product:'Bond Borrow',crid:'E024',deid:'E033',lim:11384000,exp:-2006000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0100',product:'Payment Intraday',crid:'E030',deid:'E041',lim:4248000,exp:1309000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0101',product:'Committed Loan',crid:'E000',deid:'E011',lim:148131000,exp:89074000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0102',product:'Overdraft',crid:'E060',deid:'E002',lim:1669000,exp:1426000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0103',product:'Payment Intraday',crid:'E006',deid:'E012',lim:56804000,exp:56689000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0104',product:'Payment Intraday',crid:'E040',deid:'E010',lim:6357000,exp:1922000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0105',product:'Bond Borrow',crid:'E037',deid:'E008',lim:27792000,exp:22752000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0106',product:'Xccy Swap',crid:'E041',deid:'E048',lim:4586000,exp:3202000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0107',product:'Overdraft',crid:'E049',deid:'E019',lim:300000,exp:45000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0108',product:'Payment Intraday',crid:'E026',deid:'E054',lim:23319000,exp:3917000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0109',product:'Xccy Swap',crid:'E024',deid:'E033',lim:18828000,exp:2634000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0110',product:'Payment Intraday',crid:'E007',deid:'E034',lim:42687000,exp:22897000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0111',product:'Bond Borrow',crid:'E033',deid:'E008',lim:4491000,exp:-119000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0112',product:'Xccy Swap',crid:'E000',deid:'E047',lim:229797000,exp:172834000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0113',product:'Overdraft',crid:'E000',deid:'E009',lim:97996000,exp:-19035000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0114',product:'Committed Repo',crid:'E052',deid:'E009',lim:27404000,exp:-1714000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0115',product:'Committed Repo',crid:'E042',deid:'E046',lim:24960000,exp:15274000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0116',product:'Committed Loan',crid:'E007',deid:'E040',lim:6886000,exp:5543000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0117',product:'FX Forward',crid:'E012',deid:'E023',lim:13847000,exp:13288000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0118',product:'Committed Repo',crid:'E025',deid:'E040',lim:11095000,exp:-1646000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0119',product:'Xccy Swap',crid:'E014',deid:'E057',lim:9161000,exp:7521000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0120',product:'Bond Borrow',crid:'E047',deid:'E041',lim:4390000,exp:1631000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0121',product:'Committed Repo',crid:'E006',deid:'E024',lim:59637000,exp:48541000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0122',product:'Bond Borrow',crid:'E028',deid:'E003',lim:18211000,exp:-303000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0123',product:'Committed Loan',crid:'E023',deid:'E008',lim:76628000,exp:35991000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0124',product:'Committed Loan',crid:'E049',deid:'E015',lim:1401000,exp:1020000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0125',product:'FX Forward',crid:'E003',deid:'E036',lim:140232000,exp:29701000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0126',product:'Committed Repo',crid:'E007',deid:'E014',lim:52155000,exp:19288000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0127',product:'Overdraft',crid:'E023',deid:'E035',lim:32947000,exp:18774000,currency:'GBP',crr:'Resi Co_NRFB'},
{id:'LIM0128',product:'Committed Repo',crid:'E054',deid:'E019',lim:29472000,exp:6545000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0129',product:'FX Forward',crid:'E002',deid:'E044',lim:86191000,exp:15178000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0130',product:'Xccy Swap',crid:'E009',deid:'E012',lim:29324000,exp:29112000,currency:'GBP',crr:'Fin Co_CORE'},
{id:'LIM0131',product:'Committed Repo',crid:'E011',deid:'E057',lim:20343000,exp:19894000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0132',product:'Xccy Swap',crid:'E004',deid:'E060',lim:160989000,exp:133399000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0133',product:'Committed Loan',crid:'E000',deid:'E034',lim:114087000,exp:33492000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0134',product:'Overdraft',crid:'E030',deid:'E019',lim:7491000,exp:-667000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0135',product:'Overdraft',crid:'E058',deid:'E004',lim:2478000,exp:1441000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0136',product:'Payment Intraday',crid:'E027',deid:'E021',lim:15717000,exp:-2430000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0137',product:'Committed Loan',crid:'E024',deid:'E050',lim:47114000,exp:-2132000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0138',product:'Payment Intraday',crid:'E037',deid:'E061',lim:60525000,exp:58866000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0139',product:'Xccy Swap',crid:'E002',deid:'E052',lim:152293000,exp:-27608000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0140',product:'Overdraft',crid:'E007',deid:'E035',lim:42246000,exp:27962000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0141',product:'Committed Repo',crid:'E008',deid:'E006',lim:5514000,exp:3134000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0142',product:'Payment Intraday',crid:'E006',deid:'E012',lim:73757000,exp:33868000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0143',product:'Payment Intraday',crid:'E012',deid:'E040',lim:25125000,exp:19581000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0144',product:'Xccy Swap',crid:'E013',deid:'E041',lim:8226000,exp:2239000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0145',product:'Payment Intraday',crid:'E018',deid:'E048',lim:1578000,exp:771000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0146',product:'FX Forward',crid:'E040',deid:'E013',lim:23837000,exp:11709000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0147',product:'Xccy Swap',crid:'E018',deid:'E053',lim:4295000,exp:2628000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0148',product:'Payment Intraday',crid:'E006',deid:'E019',lim:10953000,exp:7103000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0149',product:'Bond Borrow',crid:'E041',deid:'E019',lim:9796000,exp:-1958000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0150',product:'Xccy Swap',crid:'E006',deid:'E061',lim:23758000,exp:178000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0151',product:'Payment Intraday',crid:'E039',deid:'E060',lim:1516000,exp:658000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0152',product:'Overdraft',crid:'E008',deid:'E019',lim:11396000,exp:-73000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0153',product:'FX Forward',crid:'E011',deid:'E050',lim:5517000,exp:1966000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0154',product:'Xccy Swap',crid:'E011',deid:'E053',lim:10237000,exp:5712000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0155',product:'Bond Borrow',crid:'E014',deid:'E013',lim:720000,exp:201000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0156',product:'Overdraft',crid:'E038',deid:'E014',lim:20900000,exp:-1228000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0157',product:'Payment Intraday',crid:'E039',deid:'E061',lim:13282000,exp:2384000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0158',product:'FX Forward',crid:'E059',deid:'E046',lim:486000,exp:269000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0159',product:'Committed Repo',crid:'E010',deid:'E061',lim:29189000,exp:19109000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0160',product:'FX Forward',crid:'E057',deid:'E018',lim:2049000,exp:1372000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0161',product:'Committed Repo',crid:'E003',deid:'E032',lim:151235000,exp:17268000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0162',product:'Committed Repo',crid:'E015',deid:'E001',lim:6611000,exp:6551000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0163',product:'Overdraft',crid:'E023',deid:'E055',lim:28929000,exp:19789000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0164',product:'Overdraft',crid:'E006',deid:'E058',lim:47653000,exp:29989000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0165',product:'Overdraft',crid:'E004',deid:'E032',lim:103535000,exp:35778000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0166',product:'Committed Loan',crid:'E028',deid:'E039',lim:16537000,exp:8890000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0167',product:'Xccy Swap',crid:'E045',deid:'E033',lim:4682000,exp:-255000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0168',product:'FX Forward',crid:'E053',deid:'E022',lim:22144000,exp:-1070000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0169',product:'Bond Borrow',crid:'E045',deid:'E059',lim:4439000,exp:1994000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0170',product:'FX Forward',crid:'E043',deid:'E055',lim:4664000,exp:3235000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0171',product:'Payment Intraday',crid:'E004',deid:'E017',lim:65692000,exp:14131000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0172',product:'Payment Intraday',crid:'E058',deid:'E060',lim:2207000,exp:68000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0173',product:'Committed Repo',crid:'E056',deid:'E061',lim:5291000,exp:-1017000,currency:'GBP',crr:'Equit Co_NRFB'},
{id:'LIM0174',product:'Payment Intraday',crid:'E024',deid:'E032',lim:32506000,exp:29169000,currency:'GBP',crr:'Comm Co_NRFB'},
{id:'LIM0175',product:'Xccy Swap',crid:'E015',deid:'E021',lim:4656000,exp:4000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0176',product:'Committed Repo',crid:'E057',deid:'E052',lim:8035000,exp:2249000,currency:'GBP',crr:'Deriv Co_NRFB'},
{id:'LIM0177',product:'Payment Intraday',crid:'E046',deid:'E049',lim:3846000,exp:90000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0178',product:'Committed Loan',crid:'E039',deid:'E022',lim:23830000,exp:8963000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0179',product:'Committed Loan',crid:'E026',deid:'E032',lim:16542000,exp:-1518000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0180',product:'Overdraft',crid:'E003',deid:'E059',lim:148112000,exp:134543000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0181',product:'FX Forward',crid:'E039',deid:'E058',lim:6073000,exp:1401000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0182',product:'Committed Loan',crid:'E032',deid:'E044',lim:9198000,exp:8028000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0183',product:'Committed Repo',crid:'E055',deid:'E019',lim:6130000,exp:472000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0184',product:'Bond Borrow',crid:'E013',deid:'E057',lim:3284000,exp:1977000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0185',product:'Committed Repo',crid:'E002',deid:'E009',lim:40062000,exp:10677000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0186',product:'Committed Repo',crid:'E014',deid:'E017',lim:774000,exp:-32000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0187',product:'Committed Repo',crid:'E010',deid:'E036',lim:25420000,exp:-4863000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0188',product:'Committed Loan',crid:'E015',deid:'E016',lim:5102000,exp:3837000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0189',product:'Payment Intraday',crid:'E006',deid:'E046',lim:70675000,exp:-12193000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0190',product:'Committed Loan',crid:'E002',deid:'E005',lim:104476000,exp:-13407000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0191',product:'Committed Loan',crid:'E012',deid:'E024',lim:8170000,exp:7442000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0192',product:'FX Forward',crid:'E002',deid:'E019',lim:168476000,exp:-16730000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0193',product:'Bond Borrow',crid:'E030',deid:'E000',lim:6937000,exp:1249000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0194',product:'Bond Borrow',crid:'E018',deid:'E013',lim:8422000,exp:7155000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0195',product:'Payment Intraday',crid:'E009',deid:'E058',lim:15778000,exp:2161000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0196',product:'Overdraft',crid:'E057',deid:'E056',lim:9431000,exp:8171000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0197',product:'Committed Repo',crid:'E012',deid:'E005',lim:26364000,exp:25465000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0198',product:'Bond Borrow',crid:'E045',deid:'E016',lim:7109000,exp:-1097000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0199',product:'Payment Intraday',crid:'E000',deid:'E016',lim:431780000,exp:-78705000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0200',product:'FX Forward',crid:'E003',deid:'E002',lim:42200000,exp:-4953000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0201',product:'Committed Loan',crid:'E000',deid:'E055',lim:408736000,exp:319608000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0202',product:'Overdraft',crid:'E045',deid:'E015',lim:6095000,exp:1914000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0203',product:'Committed Loan',crid:'E025',deid:'E034',lim:27777000,exp:6260000,currency:'GBP',crr:'Resi Co_NRFB'},
{id:'LIM0204',product:'Committed Loan',crid:'E039',deid:'E043',lim:18364000,exp:10382000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0205',product:'Bond Borrow',crid:'E038',deid:'E006',lim:28714000,exp:16718000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0206',product:'Payment Intraday',crid:'E034',deid:'E011',lim:1130000,exp:784000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0207',product:'Payment Intraday',crid:'E004',deid:'E014',lim:41453000,exp:29166000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0208',product:'Overdraft',crid:'E007',deid:'E015',lim:68238000,exp:34499000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0209',product:'Payment Intraday',crid:'E056',deid:'E019',lim:2611000,exp:2088000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0210',product:'Xccy Swap',crid:'E044',deid:'E035',lim:6266000,exp:3847000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0211',product:'Bond Borrow',crid:'E024',deid:'E020',lim:77887000,exp:32933000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0212',product:'Overdraft',crid:'E004',deid:'E049',lim:116709000,exp:107442000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0213',product:'Payment Intraday',crid:'E043',deid:'E048',lim:15844000,exp:13334000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0214',product:'Xccy Swap',crid:'E052',deid:'E008',lim:10219000,exp:5342000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0215',product:'Bond Borrow',crid:'E052',deid:'E035',lim:48918000,exp:34857000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0216',product:'Overdraft',crid:'E012',deid:'E002',lim:6388000,exp:1492000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0217',product:'Bond Borrow',crid:'E054',deid:'E006',lim:6736000,exp:2768000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0218',product:'Committed Repo',crid:'E010',deid:'E012',lim:19275000,exp:7301000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0219',product:'Committed Repo',crid:'E006',deid:'E026',lim:20731000,exp:2775000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0220',product:'FX Forward',crid:'E008',deid:'E034',lim:22216000,exp:8419000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0221',product:'Xccy Swap',crid:'E031',deid:'E032',lim:2757000,exp:2572000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0222',product:'Bond Borrow',crid:'E053',deid:'E017',lim:9822000,exp:-1620000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0223',product:'Committed Loan',crid:'E024',deid:'E002',lim:6070000,exp:5609000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0224',product:'Committed Loan',crid:'E043',deid:'E041',lim:17283000,exp:-573000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0225',product:'Bond Borrow',crid:'E043',deid:'E054',lim:6269000,exp:1545000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0226',product:'Bond Borrow',crid:'E005',deid:'E003',lim:12722000,exp:-947000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0227',product:'Bond Borrow',crid:'E052',deid:'E021',lim:75717000,exp:21105000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0228',product:'Overdraft',crid:'E032',deid:'E034',lim:9947000,exp:5320000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0229',product:'Bond Borrow',crid:'E024',deid:'E055',lim:32652000,exp:6978000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0230',product:'Xccy Swap',crid:'E003',deid:'E044',lim:191297000,exp:143135000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0231',product:'Bond Borrow',crid:'E042',deid:'E046',lim:7053000,exp:526000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0232',product:'Committed Repo',crid:'E025',deid:'E006',lim:12101000,exp:7296000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0233',product:'Xccy Swap',crid:'E050',deid:'E058',lim:38000,exp:2000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0234',product:'Bond Borrow',crid:'E003',deid:'E026',lim:98651000,exp:54086000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0235',product:'Committed Loan',crid:'E008',deid:'E029',lim:24481000,exp:-2446000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0236',product:'Overdraft',crid:'E002',deid:'E022',lim:45964000,exp:36435000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0237',product:'Committed Repo',crid:'E055',deid:'E008',lim:5248000,exp:1930000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0238',product:'Committed Loan',crid:'E051',deid:'E050',lim:49000000,exp:42955000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0239',product:'Overdraft',crid:'E033',deid:'E047',lim:1574000,exp:121000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0240',product:'Committed Loan',crid:'E021',deid:'E032',lim:1404000,exp:310000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0241',product:'Overdraft',crid:'E035',deid:'E006',lim:1064000,exp:469000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0242',product:'Bond Borrow',crid:'E024',deid:'E056',lim:9284000,exp:580000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0243',product:'Xccy Swap',crid:'E003',deid:'E038',lim:93864000,exp:-16692000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0244',product:'Xccy Swap',crid:'E008',deid:'E019',lim:12264000,exp:-385000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0245',product:'Payment Intraday',crid:'E008',deid:'E026',lim:27302000,exp:16110000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0246',product:'Bond Borrow',crid:'E040',deid:'E038',lim:19362000,exp:-3131000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0247',product:'Payment Intraday',crid:'E007',deid:'E036',lim:70843000,exp:-2764000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0248',product:'Committed Repo',crid:'E053',deid:'E035',lim:8817000,exp:-471000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0249',product:'Bond Borrow',crid:'E025',deid:'E031',lim:23849000,exp:21690000,currency:'GBP',crr:'Resi Co_NRFB'},
{id:'LIM0250',product:'FX Forward',crid:'E039',deid:'E014',lim:3139000,exp:3096000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0251',product:'Xccy Swap',crid:'E032',deid:'E006',lim:3345000,exp:2623000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0252',product:'Xccy Swap',crid:'E025',deid:'E054',lim:2314000,exp:54000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0253',product:'Overdraft',crid:'E051',deid:'E058',lim:29641000,exp:944000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0254',product:'Bond Borrow',crid:'E011',deid:'E032',lim:18121000,exp:4995000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0255',product:'Overdraft',crid:'E007',deid:'E055',lim:44756000,exp:2683000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0256',product:'FX Forward',crid:'E041',deid:'E032',lim:14715000,exp:-1001000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0257',product:'Xccy Swap',crid:'E061',deid:'E039',lim:499000,exp:481000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0258',product:'Overdraft',crid:'E001',deid:'E035',lim:61244000,exp:4352000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0259',product:'Xccy Swap',crid:'E053',deid:'E047',lim:5142000,exp:560000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0260',product:'Overdraft',crid:'E016',deid:'E051',lim:4565000,exp:3797000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0261',product:'Xccy Swap',crid:'E013',deid:'E034',lim:27959000,exp:21595000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0262',product:'Payment Intraday',crid:'E038',deid:'E018',lim:14596000,exp:-2726000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0263',product:'Bond Borrow',crid:'E046',deid:'E012',lim:332000,exp:141000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0264',product:'Overdraft',crid:'E045',deid:'E056',lim:7261000,exp:5907000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0265',product:'FX Forward',crid:'E052',deid:'E049',lim:30874000,exp:20147000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0266',product:'FX Forward',crid:'E035',deid:'E013',lim:1629000,exp:741000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0267',product:'Committed Loan',crid:'E020',deid:'E022',lim:1780000,exp:-39000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0268',product:'Committed Loan',crid:'E002',deid:'E043',lim:37483000,exp:-3711000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0269',product:'Committed Loan',crid:'E052',deid:'E034',lim:42853000,exp:37887000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0270',product:'Committed Repo',crid:'E025',deid:'E014',lim:24730000,exp:5776000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0271',product:'Committed Loan',crid:'E003',deid:'E060',lim:179076000,exp:56564000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0272',product:'Bond Borrow',crid:'E008',deid:'E053',lim:23136000,exp:14585000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0273',product:'Bond Borrow',crid:'E015',deid:'E046',lim:2877000,exp:2875000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0274',product:'Bond Borrow',crid:'E026',deid:'E041',lim:1416000,exp:747000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0275',product:'Bond Borrow',crid:'E002',deid:'E018',lim:100568000,exp:6071000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0276',product:'Overdraft',crid:'E032',deid:'E048',lim:7109000,exp:78000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0277',product:'Payment Intraday',crid:'E027',deid:'E023',lim:23861000,exp:20060000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0278',product:'Committed Loan',crid:'E000',deid:'E038',lim:227297000,exp:195815000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0279',product:'Committed Repo',crid:'E013',deid:'E047',lim:17856000,exp:-2059000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0280',product:'Bond Borrow',crid:'E046',deid:'E037',lim:8490000,exp:152000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0281',product:'Committed Repo',crid:'E041',deid:'E060',lim:2399000,exp:-347000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0282',product:'Overdraft',crid:'E046',deid:'E022',lim:4613000,exp:3009000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0283',product:'Overdraft',crid:'E007',deid:'E017',lim:23593000,exp:19088000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0284',product:'Payment Intraday',crid:'E011',deid:'E044',lim:4104000,exp:3855000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0285',product:'Bond Borrow',crid:'E000',deid:'E009',lim:355290000,exp:-50555000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0286',product:'Committed Repo',crid:'E050',deid:'E027',lim:275000,exp:264000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0287',product:'Committed Repo',crid:'E048',deid:'E046',lim:731000,exp:632000,currency:'GBP',crr:'Trust Co_NRFB'},
{id:'LIM0288',product:'Committed Repo',crid:'E021',deid:'E019',lim:924000,exp:240000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0289',product:'Overdraft',crid:'E044',deid:'E019',lim:8565000,exp:6387000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0290',product:'Overdraft',crid:'E034',deid:'E017',lim:1412000,exp:652000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0291',product:'Bond Borrow',crid:'E018',deid:'E037',lim:4327000,exp:2581000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0292',product:'Committed Loan',crid:'E011',deid:'E034',lim:25760000,exp:5918000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0293',product:'Committed Loan',crid:'E010',deid:'E021',lim:2453000,exp:2323000,currency:'GBP',crr:'Retail Co_CORE'},
{id:'LIM0294',product:'Overdraft',crid:'E038',deid:'E016',lim:70079000,exp:57836000,currency:'GBP',crr:'NRFB_X'},
{id:'LIM0295',product:'Overdraft',crid:'E020',deid:'E027',lim:1208000,exp:94000,currency:'GBP',crr:'RFB_X'},
{id:'LIM0296',product:'Bond Borrow',crid:'E000',deid:'E033',lim:358074000,exp:189164000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0297',product:'Overdraft',crid:'E001',deid:'E007',lim:114042000,exp:58361000,currency:'GBP',crr:'RFB_INTERNAL'},
{id:'LIM0298',product:'Committed Loan',crid:'E009',deid:'E019',lim:17865000,exp:4861000,currency:'GBP',crr:'Fin Co_CORE'},
{id:'LIM0299',product:'Committed Repo',crid:'E003',deid:'E031',lim:119774000,exp:70508000,currency:'GBP',crr:'NRFB_CROSS'},
{id:'LIM0300',product:'Payment Intraday',crid:'E000',deid:'E036',lim:470383000,exp:27672000,currency:'GBP',crr:'NRFB_CROSS'}
];

// ── Build lookup maps from normalised data ────────────────────────────────────
const EMAP  = Object.fromEntries(ENTITIES.map(e=>[e.id,e]));
const LTMAP = Object.fromEntries(LIMIT_TYPES.map(t=>[t.product,t]));

function fmt(n){return new Intl.NumberFormat('en-GB').format(n);}
function fmtGBP(n){
  const a=Math.abs(n),s=a>=1e9?'£'+(a/1e9).toFixed(2)+'bn':a>=1e6?'£'+(a/1e6).toFixed(1)+'m':a>=1e3?'£'+(a/1e3).toFixed(0)+'k':'£'+a;
  return n<0?'-'+s:s;
}

function show(tab){
  const names=['entity','limtype','lim','map','tree'];
  names.forEach((t,i)=>document.querySelectorAll('.tab')[i].classList.toggle('active',t===tab));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('pf-'+tab).classList.add('active');
  if(tab==='limtype') renderLimitTypes();
  if(tab==='lim'){renderLimStats();renderLimits();}
  if(tab==='map') drawMap();
  if(tab==='tree') drawTree();
}

// ── df_legal_entity table ─────────────────────────────────────────────────────
function rfiBadge(v){return `<span class="badge b-${v}">${v}</span>`;}
function rfBadge(v){const c=v==='CORE'?'b-CORE':v==='NON CORE'?'b-NONCORE':'b-NRFB';return `<span class="badge ${c}">${v}</span>`;}

function renderEntities(){
  const lv=document.getElementById('f-level').value,dm=document.getElementById('f-dom').value,
        ri=document.getElementById('f-rfi').value,rf=document.getElementById('f-rf').value,
        l1=document.getElementById('f-l1e').value,q=document.getElementById('f-esearch').value.toLowerCase();
  const rows=ENTITIES.filter(e=>{
    if(lv&&e.level!=lv)return false;if(dm&&e.country!==dm)return false;
    if(ri&&e.rfi!==ri)return false;if(rf&&e.rf!==rf)return false;
    if(l1&&e.l1!==l1)return false;
    if(q&&!e.name.toLowerCase().includes(q)&&!e.id.toLowerCase().includes(q))return false;
    return true;
  });
  document.getElementById('ecount').textContent=rows.length+' / '+ENTITIES.length;
  document.getElementById('etbody').innerHTML=rows.map(e=>`<tr>
    <td style="font-family:var(--mono);font-size:11px">${e.id}</td>
    <td style="font-weight:500">${e.name}</td>
    <td><span class="badge b-l${e.level}">L${e.level}</span></td>
    <td style="font-family:var(--mono);font-size:11px;color:var(--text3)">${e.parent||'—'}</td>
    <td style="color:var(--text2)">${e.l1||'—'}</td>
    <td><span class="badge b-${e.country}">${e.country}</span></td>
    <td style="color:var(--text2)">${e.city}</td>
    <td>${rfiBadge(e.rfi)}</td>
    <td>${rfBadge(e.rf)}</td>
    <td style="color:var(--text3);font-size:11px">${e.crr||'—'}</td>
    <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;color:var(--text3)">${e.address}</td>
  </tr>`).join('');
}
renderEntities();

// ── df_limit_type table ───────────────────────────────────────────────────────
function renderLimitTypes(){
  document.getElementById('lttbody').innerHTML=LIMIT_TYPES.map(t=>`<tr>
    <td style="font-weight:500">${t.product}</td>
    <td><span class="badge b-${t.lt}">${t.lt}</span></td>
    <td><span class="badge b-${t.lst}">${t.lst}</span></td>
  </tr>`).join('');
}

// ── df_limits_exposures table ─────────────────────────────────────────────────
function crrBadgeClass(v){
  if(v==='RFB_X')return 'b-RFBX';
  if(v==='NRFB_X')return 'b-NRFBX';
  if(v==='RFB_INTERNAL')return 'b-RFBI';
  if(v==='NRFB_CROSS')return 'b-NRFBC';
  if(v.endsWith('_CORE'))return 'b-CORE2';
  if(v.endsWith('_NON_CORE'))return 'b-NONCORE2';
  return 'b-NRFB2';
}

function utilBar(lim,exp){
  const pct=Math.max(0,Math.min(1,exp/lim)),w=Math.round(pct*72);
  const col=pct>0.9?'#993C1D':pct>0.7?'#854F0B':'#0F6E56';
  return `<span class="util-bar-wrap"><span class="util-bar" style="width:${w}px;background:${col}"></span></span>${Math.round(pct*100)}%`;
}

function renderLimStats(){
  const tl=LIMITS_EXP.reduce((s,r)=>s+r.lim,0),te=LIMITS_EXP.reduce((s,r)=>s+r.exp,0);
  const neg=LIMITS_EXP.filter(r=>r.exp<0).length;
  const avg=LIMITS_EXP.reduce((s,r)=>s+(r.exp/r.lim),0)/LIMITS_EXP.length;
  const hard=LIMITS_EXP.filter(r=>LTMAP[r.product]&&LTMAP[r.product].lt==='Hard').length;
  document.getElementById('stat-cards').innerHTML=[
    {label:'Total limit',val:'£'+fmt(Math.round(tl/1e6))+'m'},
    {label:'Total exposure',val:(te<0?'-':'')+'£'+fmt(Math.round(Math.abs(te)/1e6))+'m'},
    {label:'Avg utilisation',val:Math.round(avg*100)+'%'},
    {label:'Hard limits',val:hard},
    {label:'Soft limits',val:LIMITS_EXP.length-hard},
    {label:'Negative exp.',val:neg+' records'},
  ].map(c=>`<div class="stat-card"><div class="stat-label">${c.label}</div><div class="stat-val">${c.val}</div></div>`).join('');
  // Populate CRR dropdown dynamically
  const crrSel=document.getElementById('lf-crr');
  if(crrSel.options.length<=1){
    [...new Set(LIMITS_EXP.map(r=>r.crr))].sort().forEach(t=>{
      const o=document.createElement('option');o.value=t;o.textContent=t;crrSel.appendChild(o);
    });
  }
}

function renderLimits(){
  const lt=document.getElementById('lf-lt').value,lst=document.getElementById('lf-lst').value,
        prod=document.getElementById('lf-prod').value,crr=document.getElementById('lf-crr').value,
        crl=document.getElementById('lf-crl').value,del=document.getElementById('lf-del').value,
        sign=document.getElementById('lf-sign').value,
        q=document.getElementById('lf-search').value.toLowerCase();
  const rows=LIMITS_EXP.filter(r=>{
    const lt_=LTMAP[r.product];
    const cr=EMAP[r.crid],dr=EMAP[r.deid];
    if(lt&&(!lt_||lt_.lt!==lt))return false;
    if(lst&&(!lt_||lt_.lst!==lst))return false;
    if(prod&&r.product!==prod)return false;
    if(crr&&r.crr!==crr)return false;
    if(crl&&cr&&cr.level!=crl)return false;
    if(del&&dr&&dr.level!=del)return false;
    if(sign==='pos'&&r.exp<0)return false;
    if(sign==='neg'&&r.exp>=0)return false;
    if(q){
      const crn=(cr?cr.name:'').toLowerCase(),den=(dr?dr.name:'').toLowerCase();
      if(!crn.includes(q)&&!den.includes(q)&&!r.product.toLowerCase().includes(q)&&
         !r.id.toLowerCase().includes(q)&&!r.crr.toLowerCase().includes(q))return false;
    }
    return true;
  });
  document.getElementById('lcount').textContent=rows.length+' / '+LIMITS_EXP.length;
  document.getElementById('ltbody').innerHTML=rows.map(r=>{
    const lt_=LTMAP[r.product]||{lt:'?',lst:'?'};
    const cr=EMAP[r.crid]||{name:'?',level:'?'};
    const dr=EMAP[r.deid]||{name:'?',level:'?'};
    return `<tr>
    <td style="font-family:var(--mono);font-size:11px">${r.id}</td>
    <td>${r.product}</td>
    <td><span class="badge b-${lt_.lt}">${lt_.lt}</span></td>
    <td><span class="badge b-${lt_.lst}">${lt_.lst}</span></td>
    <td style="font-family:var(--mono);font-size:11px">${r.crid}</td>
    <td style="font-weight:500">${cr.name}</td>
    <td><span class="badge b-l${cr.level}">L${cr.level}</span></td>
    <td style="font-family:var(--mono);font-size:11px">${r.deid}</td>
    <td style="font-weight:500">${dr.name}</td>
    <td><span class="badge b-l${dr.level}">L${dr.level}</span></td>
    <td style="text-align:right;font-family:var(--mono);font-size:11px">${fmtGBP(r.lim)}</td>
    <td style="text-align:right;font-family:var(--mono);font-size:11px" class="${r.exp<0?'neg':'pos'}">${fmtGBP(r.exp)}</td>
    <td>${utilBar(r.lim,r.exp)}</td>
    <td><span class="badge ${crrBadgeClass(r.crr)}" style="font-size:10px">${r.crr}</span></td>
  </tr>`;
  }).join('');
}

// ── Map ───────────────────────────────────────────────────────────────────────
const CITIES={London:{lat:51.5155,lon:-0.0922,color:'#534AB7'},Paris:{lat:48.8698,lon:2.3078,color:'#185FA5'},'New York':{lat:40.7484,lon:-73.9967,color:'#0F6E56'},Singapore:{lat:1.2847,lon:103.861,color:'#854F0B'},Tokyo:{lat:35.6895,lon:139.6917,color:'#993C1D'},Berlin:{lat:52.52,lon:13.405,color:'#993556'},Sydney:{lat:-33.868,lon:151.2093,color:'#3B6D11'},Toronto:{lat:43.6532,lon:-79.3832,color:'#3B6D11'},'Sao Paulo':{lat:-23.55,lon:-46.633,color:'#993C1D'},'Hong Kong':{lat:22.3193,lon:114.1694,color:'#854F0B'}};
const ABBR={London:'LON',Paris:'PAR','New York':'NYC',Singapore:'SGP',Tokyo:'TKY',Berlin:'BER',Sydney:'SYD',Toronto:'TOR','Sao Paulo':'GRU','Hong Kong':'HKG'};
const CITY_DOM={London:'UK',Paris:'FR','New York':'US',Singapore:'SG',Tokyo:'JP',Berlin:'DE',Sydney:'AU',Toronto:'CA','Sao Paulo':'BR','Hong Kong':'HK'};
function proj(lat,lon){const W=680,H=400,x=(lon+180)/360*W*0.95+W*0.02,lr=lat*Math.PI/180,y=(Math.PI/2-Math.log(Math.tan(Math.PI/4+lr/2)))/Math.PI*H*0.9+H*0.05;return{x,y};}
let mapBuilt=false;
function drawMap(){
  if(mapBuilt)return;mapBuilt=true;
  const counts={};ENTITIES.forEach(e=>{counts[e.city]=(counts[e.city]||0)+1;});
  const svg=document.getElementById('mapsvg');
  fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json').then(r=>r.json()).then(t=>renderMap(svg,counts,t)).catch(()=>renderMap(svg,counts,null));
}
function renderMap(svg,counts,topo){
  svg.innerHTML='';
  if(topo){
    const sc=topo.transform.scale,tr=topo.transform.translate;
    function da(i){let a=i<0?topo.arcs[~i]:topo.arcs[i],x=0,y=0,p=[];for(let v of a){x+=v[0];y+=v[1];p.push([x,y]);}if(i<0)p.reverse();return p;}
    function poly(arcs){let d='';arcs.forEach(ring=>{let f=true;ring.forEach(i=>{da(i).forEach((p,j)=>{const lon=p[0]*sc[0]+tr[0],lat=p[1]*sc[1]+tr[1];const{x,y}=proj(lat,lon);d+=(f&&j===0?`M${x.toFixed(1)} ${y.toFixed(1)}`:`L${x.toFixed(1)} ${y.toFixed(1)}`);f=false;});});d+='Z';});return d;}
    const g=document.createElementNS('http://www.w3.org/2000/svg','g');
    topo.objects.countries.geometries.forEach(geo=>{
      const path=document.createElementNS('http://www.w3.org/2000/svg','path');
      let d='';if(geo.type==='Polygon')d=poly(geo.arcs);else if(geo.type==='MultiPolygon')geo.arcs.forEach(a=>d+=poly(a));
      path.setAttribute('d',d);path.setAttribute('fill','#e8e6df');path.setAttribute('stroke','#f5f4f0');path.setAttribute('stroke-width','0.4');g.appendChild(path);
    });svg.appendChild(g);
  }
  const leg=document.getElementById('map-legend');leg.innerHTML='';
  Object.entries(CITIES).forEach(([city,info])=>{
    const cnt=counts[city]||0;if(!cnt)return;
    const{x,y}=proj(info.lat,info.lon),r=Math.max(12,Math.sqrt(cnt)*6);
    const g=document.createElementNS('http://www.w3.org/2000/svg','g');g.style.cursor='pointer';
    const c=document.createElementNS('http://www.w3.org/2000/svg','circle');
    c.setAttribute('cx',x);c.setAttribute('cy',y);c.setAttribute('r',r);c.setAttribute('fill',info.color);c.setAttribute('fill-opacity','0.8');c.setAttribute('stroke','rgba(255,255,255,0.4)');c.setAttribute('stroke-width','0.5');
    const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('x',x);t.setAttribute('y',y);t.setAttribute('text-anchor','middle');t.setAttribute('dominant-baseline','central');t.setAttribute('font-size','8');t.setAttribute('font-weight','500');t.setAttribute('fill','#fff');t.setAttribute('font-family','-apple-system,sans-serif');t.textContent=ABBR[city];
    const t2=document.createElementNS('http://www.w3.org/2000/svg','text');t2.setAttribute('x',x);t2.setAttribute('y',y+r+9);t2.setAttribute('text-anchor','middle');t2.setAttribute('font-size','8');t2.setAttribute('fill','#5a5a56');t2.setAttribute('font-family','-apple-system,sans-serif');t2.textContent=cnt;
    g.appendChild(c);g.appendChild(t);g.appendChild(t2);
    g.onclick=()=>{document.getElementById('f-dom').value=CITY_DOM[city];show('entity');renderEntities();};
    svg.appendChild(g);
    const s=document.createElement('span');s.innerHTML=`<span class="leg-dot" style="background:${info.color}"></span>${city} (${cnt})`;leg.appendChild(s);
  });
}

// ── Tree ──────────────────────────────────────────────────────────────────────
let treeBuilt=false;
function drawTree(){
  if(treeBuilt)return;treeBuilt=true;
  const svg=document.getElementById('treesvg');svg.innerHTML='';
  const lc={0:'#534AB7',1:'#0F6E56',2:'#185FA5',3:'#3B6D11',4:'#854F0B',5:'#993C1D',6:'#993356'};
  const lf={0:'#EEEDFE',1:'#E1F5EE',2:'#E6F1FB',3:'#EAF3DE',4:'#FAEEDA',5:'#FAECE7',6:'#FBEAF0'};
  const BW=90,BH=28,HG=12,VG=50;
  function ch(id){return ENTITIES.filter(e=>e.parent===id);}
  function sw(e){const c=ch(e.id);return c.length?Math.max(BW,c.reduce((s,x)=>s+sw(x),0)+(c.length-1)*HG):BW;}
  const pos={};
  function layout(e,x,y){const c=ch(e.id),s=sw(e);pos[e.id]={x:x+s/2-BW/2,y,w:BW,h:BH};if(!c.length)return;let cx=x;c.forEach(k=>{const ks=sw(k);layout(k,cx,y+BH+VG);cx+=ks+HG;});}
  const root=ENTITIES.find(e=>e.level===0);layout(root,20,30);
  let mx=0,my=0;Object.values(pos).forEach(p=>{mx=Math.max(mx,p.x+p.w+20);my=Math.max(my,p.y+p.h+20);});
  svg.setAttribute('viewBox',`0 0 ${mx} ${my}`);svg.setAttribute('width',Math.max(mx,680));svg.setAttribute('height',my);
  const defs=document.createElementNS('http://www.w3.org/2000/svg','defs');
  defs.innerHTML=`<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#aaa9a3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>`;
  svg.appendChild(defs);
  ENTITIES.forEach(e=>{
    if(!e.parent)return;const pp=pos[e.id],ppar=pos[e.parent];if(!pp||!ppar)return;
    const x1=ppar.x+ppar.w/2,y1=ppar.y+ppar.h,x2=pp.x+pp.w/2,y2=pp.y,mid=(y1+y2)/2;
    const path=document.createElementNS('http://www.w3.org/2000/svg','path');
    path.setAttribute('d',`M${x1} ${y1} L${x1} ${mid} L${x2} ${mid} L${x2} ${y2}`);path.setAttribute('fill','none');path.setAttribute('stroke','rgba(0,0,0,0.15)');path.setAttribute('stroke-width','0.5');path.setAttribute('marker-end','url(#arr)');svg.appendChild(path);
  });
  ENTITIES.forEach(e=>{
    const p=pos[e.id];if(!p)return;
    const g=document.createElementNS('http://www.w3.org/2000/svg','g');g.style.cursor='pointer';
    const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');
    rect.setAttribute('x',p.x);rect.setAttribute('y',p.y);rect.setAttribute('width',p.w);rect.setAttribute('height',p.h);rect.setAttribute('rx','4');rect.setAttribute('fill',lf[e.level]);rect.setAttribute('stroke',lc[e.level]);rect.setAttribute('stroke-width','0.5');
    const txt=document.createElementNS('http://www.w3.org/2000/svg','text');
    txt.setAttribute('x',p.x+p.w/2);txt.setAttribute('y',p.y+p.h/2);txt.setAttribute('text-anchor','middle');txt.setAttribute('dominant-baseline','central');txt.setAttribute('font-size',e.level<2?'10':'9');txt.setAttribute('font-weight',e.level<2?'500':'400');txt.setAttribute('fill',lc[e.level]);txt.setAttribute('font-family','-apple-system,sans-serif');
    txt.textContent=e.name.length>13?e.name.slice(0,12)+'…':e.name;
    g.appendChild(rect);g.appendChild(txt);
    g.onclick=()=>{show('entity');document.getElementById('f-esearch').value=e.name;renderEntities();};
    svg.appendChild(g);
  });
  let lx=20;[0,1,2,3,4,5,6].forEach(l=>{
    const g=document.createElementNS('http://www.w3.org/2000/svg','g');
    const r=document.createElementNS('http://www.w3.org/2000/svg','rect');r.setAttribute('x',lx);r.setAttribute('y',my-18);r.setAttribute('width',10);r.setAttribute('height',10);r.setAttribute('rx','2');r.setAttribute('fill',lf[l]);r.setAttribute('stroke',lc[l]);r.setAttribute('stroke-width','0.5');
    const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('x',lx+13);t.setAttribute('y',my-11);t.setAttribute('font-size','9');t.setAttribute('fill','#8a8a84');t.setAttribute('font-family','-apple-system,sans-serif');t.textContent='L'+l;
    g.appendChild(r);g.appendChild(t);svg.appendChild(g);lx+=34;
  });
}