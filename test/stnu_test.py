import json
import networkx as nx
import numpy as np
from src.structs.task import Task
from src.temporal_networks.stnu import Node, Constraint, STNU
from src.temporal_networks.simulator import Simulator

MAX_SEED = 2 ** 31 - 1
"""The maximum number a random seed can be."""

def get_stn_dict():
    """Reads an STNU from a json file and returns it as a dict"""
    with open('data/stnu_two_tasks.json') as json_file:
        stn_dict = json.load(json_file)
    return stn_dict


def create_stn_from_dict(stn_dict):
    stn = STNU()
    # Adding the zero timepoint
    zero_timepoint = Node(0)
    stn.add_node(0, data=zero_timepoint)

    for node in stn_dict['nodes']:
        task = Task.from_dict(node['task'])
        id = node['id']

        new_node = Node(id, task, start_task=node['is_task_start'], end_task=node['is_task_end'])

        stn.add_node(id, data=new_node)

        if node['is_task_start']:
            start_time = Constraint(zero_timepoint.id, new_node.id, task.earliest_start_time, task.latest_start_time)
            stn.add_constraint(start_time)
            # earliest_start_time = Edge(new_node.id, zero_timepoint.id, -task.earliest_start_time)
            # latest_start_time = Edge(zero_timepoint.id, new_node.id, task.latest_start_time)
            # stn.add_constraint(earliest_start_time)
            # stn.add_constraint(latest_start_time)

        elif node['is_task_end']:
            finish_time = Constraint(zero_timepoint.id, new_node.id, task.earliest_finish_time, task.latest_finish_time)
            stn.add_constraint(finish_time)
            # earliest_finish_time = Edge(new_node.id, zero_timepoint.id, -task.earliest_finish_time)
            # latest_finish_time = Edge(zero_timepoint.id, new_node.id, task.latest_finish_time)
            #
            # stn.add_constraint(earliest_finish_time)
            # stn.add_constraint(latest_finish_time)

    for constraint in stn_dict['constraints']:
        i = constraint['starting_node']
        j = constraint['ending_node']
        min_time = constraint['min_time']
        max_time = constraint['max_time']
        distribution = constraint['distribution']
        stn.add_constraint(Constraint(i, j, min_time, max_time, distribution))
        # if int(edge['starting_node']) > int(edge['ending_node']):
        #     new_constraint = Edge(edge['starting_node'], edge['ending_node'], -edge['weight'], edge['distribution'])
        # else:
        #     new_constraint = Edge(edge['starting_node'], edge['ending_node'], edge['weight'], edge['distribution'])
        #
        # stn.add_constraint(new_constraint)

    return stn


def simulate(starting_stn, execution_strategy, random_seed=None):
    if random_seed is None:
        random_seed = np.random.randint(MAX_SEED)
    else:
        random_seed = int(random_seed)

    seed_gen = np.random.RandomState(random_seed)
    seed = seed_gen.randint(MAX_SEED)
    simulator = Simulator(seed)

    simulator.simulate(starting_stn, execution_strategy)
    reschedule_count = simulator.num_reschedules
    sent_count = simulator.num_sent_schedules

    # print("Assigned Times: {}".format(simulator.get_assigned_times()))
    # print("Successful?: {}".format(ans))

    # response_dict = {"sample_results": [ans], "reschedules":
    #                  [reschedule_count], "sent_schedules": [sent_count]}
    # return response_dict



if __name__ == "__main__":

    stn_dict = get_stn_dict()
    stn = create_stn_from_dict(stn_dict)

    print("Nodes: {}\n".format(stn.nodes.data()))
    print("Edges: {}\n".format(stn.edges.data()))

    print("STNU:")
    print(stn)

    # print("Calculating the minimal STNU...")
    # minimal_stn = nx.floyd_warshall(stn)
    # print(minimal_stn)
    # print('')
    #
    # if stn.is_consistent(minimal_stn):
    #     stn.update_edges(minimal_stn)
    #     stn.update_time_schedule(minimal_stn)
    #
    # print("Completion time: ", stn.get_completion_time())
    # print("Makespan: ", stn.get_makespan())
    # nx.draw(stn, with_labels=True, font_weight='bold')
    # plt.show()

    # print('')
    print("Simulating execution of STNU")
    simulate(stn, 'srea')


        #print(stn.get_edge_data(0, i)['weight'])

    # stn.get_edge_data(0, i)['weight']


    #https://stackoverflow.com/questions/48543460/how-to-use-user-defined-class-object-as-a-networkx-node