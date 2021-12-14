from numpy.lib.arraysetops import isin
from pomegranate import *
import pandas as pd

from pomegranate import *
from pomegranate import DiscreteDistribution, ConditionalProbabilityTable


risk_file_path = 'data/perceived_risk.csv'
distancing_file_path = 'data/distancing.csv'

class BayesianModel(object):
    def __init__(self):
        self.model = self.bake_model()

    def bake_model(self):
        risk_data = pd.read_csv('data/perceived_risk.csv')
        distancing_data = pd.read_csv('data/distancing.csv')
        risk_data = risk_data.to_numpy().tolist()
        distancing_data = distancing_data.to_numpy().tolist()

        # 0 is low, 1 is high
        density = Node(DiscreteDistribution({
            0: 0.5,
            1: 0.5
        }), name="density")

        mask = Node(DiscreteDistribution({
            False: 0.5,
            True: 0.5,
        }), name="mask")

        urgency = Node(DiscreteDistribution({
            1: 0.13284325,
            2: 0.17838325,
            3: 0.31686033,
            4: 0.25425658,
            5: 0.11775658
        }), name="urgency")

        perceived_risk = Node(ConditionalProbabilityTable(
                risk_data,
                [density.distribution, mask.distribution]), 
                name="percieved_risk"
            )

        distancing = Node(ConditionalProbabilityTable(
                distancing_data,
                [perceived_risk.distribution, urgency.distribution]), 
                name="distancing"
            )

        model = BayesianNetwork()
        model.add_states(density, mask, urgency, perceived_risk, distancing)

        model.add_edge(density, perceived_risk)
        model.add_edge(mask, perceived_risk)
        model.add_edge(perceived_risk, distancing)
        model.add_edge(urgency, distancing)

        model.bake()
        return model    
    

    def predict_proba(self, **data):
        predictions = self.model.predict_proba(data)        
        distancing_distribution = predictions[4].parameters[0]
        # print(data.get('urgency'))
        print('leniency in physical distancing')
        print(distancing_distribution)
        # print(distancing_distribution[1] + distancing_distribution[2] + distancing_distribution[3])
        return max(distancing_distribution, key=distancing_distribution.get)

# probability = model.probability([[0, True, 3, 2, 2]])


# predictions = model.predict_proba({
#     "density": 0,
#     "mask": True, 
#     "urgency": 1,    
# })


# for node, prediction in zip(model.states, predictions):
#     if isinstance(prediction, str) or isinstance(prediction, int) or isinstance(prediction, bool):
#         print(f"{node.name}: {prediction}")
#     else:        
#         print(f"{node.name}")
#         print(prediction.parameters)
#         # for value, probability in prediction.parameters[0].items():
#         #     print(f"    {value}: {probability:.4f}")
