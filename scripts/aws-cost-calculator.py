import yaml
with open('parameters.yaml','r') as file:
    params = yaml.safe_load(file)

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
            initialSnapshotCost = DiskVolumes[i] * SnapshotPrice * (SnapshotsRetention / Days)

        if (isinstance(SnapshotsDelta[i],list)):
            totalSnapshotCost = 0
            for delta in SnapshotsDelta[i]:
                snapshotCost = (float(delta) * SnapshotPrice * SnapshotsRetention)/(Days)
                totalSnapshotCost = totalSnapshotCost + snapshotCost
        else:
            totalSnapshotCost = Days * SnapshotsDelta[i] * SnapshotPrice * (SnapshotsRetention / Days)

        EBStotalCost.append((EBSmonthlyCost + initialSnapshotCost + totalSnapshotCost))

    return EBStotalCost

EC2confs = params['EC2-confs']
test = EC2cost(EC2confs['EC2-type-price'],EC2confs['Hours-online'],EC2confs['Days-online'])
print(test)

EBSconfs = params['EBS-confs']
testEBS = EBScost(EBSconfs['EBS-price'],EBSconfs['Snapshot-price'],EBSconfs['EBS-volumes'],EBSconfs['Days-in-month'],EBSconfs['Snapshots-retention'],EBSconfs['Snapshots-delta'],EBSconfs['Initial-snapshot'])
print(testEBS)