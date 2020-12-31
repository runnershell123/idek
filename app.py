from flask import Flask, render_template, request, Markup
app = Flask(__name__)
import math
from sigfig import round
import random
import pandas as pd 

#df = pd.read_csv("invasionprob.csv") 
df = pd.read_csv("data\invasionprob.csv")
risk = []

def getPortProbabilties(port_name):
    count = 0
    total = 0
    for index, row in df.iterrows():
        if(row['to_name'] == port_name):
            count = count + 1
            total = total + row['P']
    avg = total/count
    #avg = round(avg, sigfigs=3)
    avg = round(avg, 4)
    risk.append(avg)

def port_df(df, port_name):
    portdf = df.loc[df['from_name'] == port_name]
    prob = 0
    count = 0
    for p in portdf['P']:
        prob = prob + p
        count = count + 1
    #prob = round(prob/count, sigfigs=3)
    prob = round(prob/count, 4)
    risk.append(prob)

# TO
"""port_names = ['SHANGHAI', 'ZHOUSHAN', 'YANGSHAN', 'NINGBO', 'QINGDAO', 'XINGANG', 'YANTIAN', 'CHIWAN']
            
for name in port_names:
    getPortProbabilties(name)

print("done")   """


# FROM
port_names = ['SHANGHAI', 'ZHOUSHAN', 'YANGSHAN', 'HONG KONG', 'KAOHSIUNG', 'NINGBO', 'QINGDAO', 'XINGANG', 'YANTIAN', 'CHIWAN']

for name in port_names:
    port_df(df, name) 


def pAlienSpecies(distance, shapeParameter, geoScale):
    distance = float(distance)
    shapeParameter = float(shapeParameter)
    geoScale = float(geoScale)
    return pow(1 + (geoScale/distance), -1*shapeParameter)

def pIntroduction(cc, moralityRate, voyageTime, ballastAmount, pr):
    cc = float(cc)
    moralityRate = float(moralityRate)
    voyageTime = float(voyageTime)
    ballastAmount = float(ballastAmount)
    pr = float(pr)
    return (pr)*(1-(pow(math.e, -1*cc*ballastAmount)))*(pow(math.e, -1*moralityRate*voyageTime))

def pInvasion(basicProbability, sigmaT, sigmaS, deltaTemp, deltaSalinity):
    basicProbability = float(basicProbability)
    sigmaT = float(sigmaT)
    sigmaS = float(sigmaS)
    deltaTemp = float(deltaTemp)
    deltaSalinity = float(deltaSalinity)
    return (basicProbability) * pow(math.e, (-0.5)*(pow((deltaSalinity/sigmaS), 2) + pow((deltaSalinity/sigmaS), 2)))

def totalProb(p1, p2, p3):
    return p1*p2*p3

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/barChart')
def barChart():
    barLabels = port_names
    barValues = risk
    max =0 
    for r in risk:
        if r>max:
            max = r
    return render_template('chart.html', title ='Port Risk Rankings', labels=barLabels, values=barValues, max1=max) 

@app.route('/data', methods=['GET','POST'])
def data():
    distance = request.args['distance']
    shapeParameter = request.args['shapeParameter']
    geoScale = request.args['geoScale']
    p1 = pAlienSpecies(distance, shapeParameter, geoScale)

    cc = request.args['cc']
    moralityRate = request.args['moralityRate']
    voyageTime = request.args['voyageTime']
    ballastAmount = request.args['ballastAmount']
    pr = request.args['pr']
    p2 = pIntroduction(cc, moralityRate, voyageTime, ballastAmount, pr)

    basicProbability = request.args['basicProbability']
    sigmaT = request.args['sigmaT']
    sigmaS = request.args['sigmaS']
    deltaTemp = request.args['deltaTemp']
    deltaSalinity = request.args['deltaSalinity']
    p3 = pInvasion(basicProbability, sigmaT, sigmaS, deltaTemp, deltaSalinity)

    prob = totalProb(p1, p2, p3)
    p1 = round(p1, sigfigs=3)
    p2 = round(p2, sigfigs=3)
    p3 = round(p3, sigfigs=3)
    prob = round(prob, sigfigs=3)
    return render_template('data.html', p1=p1, p2=p2, p3=p3, prob=prob)
    
if __name__ == "__main__":
    app.run(debug=True)