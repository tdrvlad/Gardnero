from irigation_utils import Circuits, ActionTriggers, Handler

action_triggers = ActionTriggers(max_days_period = 4)
circuits = Circuits(action_triggers = action_triggers)

circuits.add_circuit(
    pump = 'tank1', 
    time = 8, 
    days_period = 2, 
    description = 'Ficus + Stefanotis birou')

circuits.add_circuit(
    pump = 'tank2', 
    time = 16, 
    days_period = 2, 
    description = 'Bonsai birou')

circuits.add_circuit(
    pump = 'tank3', 
    time = 15, 
    days_period = 2, 
    description = 'Plante sub birou')

circuits.add_circuit(
    pump = 'tank4', 
    time = 44, 
    days_period = 2, 
    description = 'Ficus + iedera')

handler = Handler(action_triggers = action_triggers)
handler.run()
