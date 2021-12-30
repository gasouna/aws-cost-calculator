def EC2cost(EC2price,HoursOn,DaysOn=22):
    monthEC2Cost = 0
    if((isinstance(EC2price,list)) and (isinstance(HoursOn,float) or isinstance(HoursOn,int))):
        for i in EC2price:
            dailyCost = float(i) * float(HoursOn)
            monthEC2Cost = monthEC2Cost + dailyCost
    elif((isinstance(EC2price,list)) and (isinstance(HoursOn,list))):
        if (len(EC2price) == len(HoursOn)):
            for i in range(0,len(HoursOn)):
                dailyCost = float(EC2price[i]) * float(HoursOn[i])
                monthEC2Cost = monthEC2Cost + dailyCost
        else:
            print('Vetores de custo e preço de EC2 possuem tamanhos diferentes.')
    elif((isinstance(EC2price,float) or isinstance(EC2price,int)) and (isinstance(HoursOn,list))):
        for i in HoursOn:
            dailyCost = float(i) * float(EC2price)
            monthEC2Cost = monthEC2Cost + dailyCost
    else:
        monthEC2Cost = float(EC2price) * float(HoursOn) * float(DaysOn)

    return monthEC2Cost

def EBScost(EBSprice,SnapshotPrice,DiskVolumes=[40,80],Days=30,SnapshotsRetention=7,SnapshotsDelta=[0,0],InitialSnapshot=True):
    EBStotalCost = []
    for i in range(0,2):
        EBSmonthlyCost = float(DiskVolumes[i]) * float(EBSprice)

        if (InitialSnapshot == True):
            initialSnapshotCost = DiskVolumes[i] * SnapshotPrice

        if (isinstance(SnapshotsDelta[i],list)):
            totalSnapshotCost = 0
            for delta in SnapshotsDelta[i]:
                snapshotCost = (float(delta) * SnapshotPrice * SnapshotsRetention)/(Days)
                totalSnapshotCost = totalSnapshotCost + snapshotCost
        else:
            totalSnapshotCost = Days * SnapshotsDelta[i] * SnapshotPrice * (SnapshotsRetention / Days)

        EBStotalCost.append((EBSmonthlyCost + initialSnapshotCost + totalSnapshotCost))

    return EBStotalCost

import yaml
with open('parameters.yaml','r') as file:
    params = yaml.safe_load(file)
    
# Estimativa 1 - Máquina m5.2xlarge ligada no agendamento padrão
EC2confsEO = params['Estimative-one']['EC2-confs']
EC2_EO = round(EC2cost(EC2confsEO['EC2-type-price'],EC2confsEO['Hours-online'],EC2confsEO['Days-online']),2)
print(f'O custo de EC2 da primeira estimativa é de {EC2_EO} USD.')

EBSconfsEO = params['Estimative-one']['EBS-confs']
EBS_EO = EBScost(EBSconfsEO['EBS-price'],EBSconfsEO['Snapshot-price'],EBSconfsEO['EBS-volumes'],EBSconfsEO['Days-in-month'],EBSconfsEO['Snapshots-retention'],EBSconfsEO['Snapshots-delta'],EBSconfsEO['Initial-snapshot'])
print('O custo de EBS da primeira estimativa é de ' + str(round(EBS_EO[0],2)) + ' USD para o disco principal e de ' + str(round(EBS_EO[1],2)) + ' USD para o disco hot.')

TotalEO = round(EC2_EO + EBS_EO[0] + EBS_EO[1],2)
print(f'\nO custo total da solução 1 é de {TotalEO} USD no mês.')

# Estimativa 2 - Máquina m5.2xlarge no agendamento padrão até 28/12. Depois trocada para c6i.32xlarge e mantida sem agendamento até 31/12
EC2confsET = params['Estimative-two']['EC2-confs']
EC2_ET = round(EC2cost(EC2confsET['EC2-type-price'],EC2confsET['Hours-online'],EC2confsET['Days-online']),2)
print(f'O custo de EC2 da segunda estimativa é de {EC2_ET} USD.')

EBSconfsET = params['Estimative-two']['EBS-confs']
EBS_ET = EBScost(EBSconfsET['EBS-price'],EBSconfsET['Snapshot-price'],EBSconfsET['EBS-volumes'],EBSconfsET['Days-in-month'],EBSconfsET['Snapshots-retention'],EBSconfsET['Snapshots-delta'],EBSconfsET['Initial-snapshot'])
print('O custo de EBS da segunda estimativa é de ' + str(round(EBS_ET[0],2)) + ' USD para o disco principal e de ' + str(round(EBS_ET[1],2)) + ' USD para o disco hot.')

TotalET = round(EC2_ET + EBS_ET[0] + EBS_ET[1],2)
print(f'\nO custo total da solução 2 é de {TotalET} USD no mês.')

# Estimativa 3 - Máquina m5a.2xlarge ligada no agendamento padrão
EC2confsE3 = params['Estimative-three']['EC2-confs']
EC2_E3 = round(EC2cost(EC2confsE3['EC2-type-price'],EC2confsE3['Hours-online'],EC2confsE3['Days-online']),2)
print(f'O custo de EC2 da terceira estimativa é de {EC2_E3} USD.')

EBSconfsE3 = params['Estimative-three']['EBS-confs']
EBS_E3 = EBScost(EBSconfsE3['EBS-price'],EBSconfsE3['Snapshot-price'],EBSconfsE3['EBS-volumes'],EBSconfsE3['Days-in-month'],EBSconfsE3['Snapshots-retention'],EBSconfsE3['Snapshots-delta'],EBSconfsE3['Initial-snapshot'])
print('O custo de EBS da terceira estimativa é de ' + str(round(EBS_E3[0],2)) + ' USD para o disco principal e de ' + str(round(EBS_E3[1],2)) + ' USD para o disco hot.')

TotalE3 = round(EC2_E3 + EBS_E3[0] + EBS_E3[1],2)
print(f'\nO custo total da solução 3 é de {TotalE3} USD no mês.')

# Estimativa 4 - Máquina r5.xlarge ligada no agendamento padrão
EC2confsE4 = params['Estimative-four']['EC2-confs']
EC2_E4 = round(EC2cost(EC2confsE4['EC2-type-price'],EC2confsE4['Hours-online'],EC2confsE4['Days-online']),2)
print(f'O custo de EC2 da terceira estimativa é de {EC2_E4} USD.')

EBSconfsE4 = params['Estimative-four']['EBS-confs']
EBS_E4 = EBScost(EBSconfsE4['EBS-price'],EBSconfsE4['Snapshot-price'],EBSconfsE4['EBS-volumes'],EBSconfsE4['Days-in-month'],EBSconfsE4['Snapshots-retention'],EBSconfsE4['Snapshots-delta'],EBSconfsE4['Initial-snapshot'])
print('O custo de EBS da terceira estimativa é de ' + str(round(EBS_E4[0],2)) + ' USD para o disco principal e de ' + str(round(EBS_E4[1],2)) + ' USD para o disco hot.')

TotalE4 = round(EC2_E4 + EBS_E4[0] + EBS_E4[1],2)
print(f'\nO custo total da solução 3 é de {TotalE4} USD no mês.')

# Estimativa 5 - Máquina r5.xlarge ligada 24/7
EC2confsE5 = params['Estimative-five']['EC2-confs']
EC2_E5 = round(EC2cost(EC2confsE5['EC2-type-price'],EC2confsE5['Hours-online'],EC2confsE5['Days-online']),2)
print(f'O custo de EC2 da terceira estimativa é de {EC2_E5} USD.')

EBSconfsE5 = params['Estimative-five']['EBS-confs']
EBS_E5 = EBScost(EBSconfsE5['EBS-price'],EBSconfsE5['Snapshot-price'],EBSconfsE5['EBS-volumes'],EBSconfsE5['Days-in-month'],EBSconfsE5['Snapshots-retention'],EBSconfsE5['Snapshots-delta'],EBSconfsE5['Initial-snapshot'])
print('O custo de EBS da terceira estimativa é de ' + str(round(EBS_E5[0],2)) + ' USD para o disco principal e de ' + str(round(EBS_E5[1],2)) + ' USD para o disco hot.')

TotalE5 = round(EC2_E5 + EBS_E5[0] + EBS_E5[1],2)
print(f'\nO custo total da solução 3 é de {TotalE5} USD no mês.')

import pandas as pd
dic = {'Estimativa-1':{'EC2-Cost_USD':EC2_EO,'EBS-Cost_USD':round((EBS_EO[0]+EBS_EO[1]),2)},'Estimativa-2':{'EC2-Cost_USD':EC2_ET,'EBS-Cost_USD':round((EBS_ET[0]+EBS_ET[1]),2)},
       'Estimativa-3':{'EC2-Cost_USD':EC2_E3,'EBS-Cost_USD':round((EBS_E3[0]+EBS_E3[1]),2)},'Estimativa-4':{'EC2-Cost_USD':EC2_E4,'EBS-Cost_USD':round((EBS_E4[0]+EBS_E4[1]),2)},
       'Estimativa-5':{'EC2-Cost_USD':EC2_E5,'EBS-Cost_USD':round((EBS_E5[0]+EBS_E5[1]),2)}}
tabela = pd.DataFrame(dic)
tabela
