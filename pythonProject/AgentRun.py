import numpy as np
import os
import random
import pickle
import os.path
import math
from m611env import *
import glob
import getframe

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import torch.autograd as autograd
import pdb

from IPython.display import clear_output
# from torch.utils.tensorboard import SummaryWriter

USE_CUDA = torch.cuda.is_available()
dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
Variable = lambda *args, **kwargs: autograd.Variable(
    *args, **kwargs).cuda() if USE_CUDA else autograd.Variable(*args, **kwargs)


class SumTree(object):
    write = 0

    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        self.data = np.zeros(capacity, dtype=object)  # dtype=object means that the array will store any type of objects
        self.n_entries = 0

    # update to the root node
    def _propagate(self, idx, change):
        parent = (idx - 1) // 2
        self.tree[parent] += change
        if parent != 0:
            self._propagate(parent, change)

    # find sample on leaf node
    def _retrieve(self, idx, s):
        left = 2 * idx + 1
        right = left + 1
        if left >= len(self.tree):
            return idx

        if s <= self.tree[left]:
            return self._retrieve(left, s)
        else:
            return self._retrieve(right, s - self.tree[left])

    # store priority and sample
    def add(self, p, data):
        idx = self.write + self.capacity - 1

        self.data[self.write] = data
        self.update(idx, p)  # update parent nodes

        self.write += 1
        if self.write >= self.capacity:
            self.write = 0

        if self.n_entries < self.capacity:
            self.n_entries += 1

    # update priority
    def update(self, idx, p):
        change = p - self.tree[idx]
        self.tree[idx] = p
        self._propagate(idx, change)

    # get priority and sample
    def get(self, s):
        idx = self._retrieve(0, s)
        dataIdx = idx - self.capacity + 1
        return (idx, self.tree[idx], self.data[dataIdx])

    def total(self):
        return self.tree[0]

class DQN(nn.Module):
    def __init__(self, in_channels=4, num_actions=6):
        super(DQN, self).__init__()
        self.model = nn.Sequential(
            # nn.Conv2d(in_channels, 32, kernel_size=8,
            #           stride=4),  # (4,84,84)->(32,20,20)
            # nn.ReLU(),
            # nn.Conv2d(32, 64, kernel_size=4, stride=2),  # (32,20,20)->(64,9,9)
            # nn.ReLU(),
            # # (64,9,9)->(64,7,7) feature map size
            # nn.Conv2d(64, 64, kernel_size=3, stride=1),
            # nn.ReLU(),
            # nn.Flatten(),
            # nn.Linear(7*7*64, 512),
            # nn.ReLU(),
            # nn.Linear(512, num_actions)

            nn.Linear(in_channels, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.Linear(16, num_actions)
        )

    def forward(self, x):
        return self.model(x)

class Memory_Buffer_PER(object):
    # stored as ( s, a, r, s_ ) in SumTree
    def __init__(self, memory_size=1000, a=0.6, e=0.01):
        self.tree = SumTree(memory_size)
        self.memory_size = memory_size
        self.prio_max = 0.1
        self.a = a
        self.e = e

    def push(self, state, action, reward, next_state, done):
        data = (state, action, reward, next_state, done)
        p = (np.abs(self.prio_max) + self.e) ** self.a  # proportional priority
        self.tree.add(p, data)

    def sample(self, batch_size):
        states, actions, rewards, next_states, dones = [], [], [], [], []
        idxs = []
        segment = self.tree.total() / batch_size
        priorities = []

        for i in range(batch_size):
            a = segment * i
            b = segment * (i + 1)
            s = random.uniform(a, b)
            idx, p, data = self.tree.get(s)

            state, action, reward, next_state, done = data
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            dones.append(done)
            priorities.append(p)
            idxs.append(idx)
        return idxs, np.concatenate(states), actions, rewards, np.concatenate(next_states), dones

    def update(self, idxs, errors):
        self.prio_max = max(self.prio_max, max(np.abs(errors)))
        for i, idx in enumerate(idxs):
            p = (np.abs(errors[i]) + self.e) ** self.a
            self.tree.update(idx, p)

    def size(self):
        return self.tree.n_entries

class DQN_PERAgent:
    def __init__(self, in_channels=1, action_num=2, USE_CUDA=False, memory_size=10000, prio_a=0.6, prio_e=0.001, epsilon=1, lr=1e-4):
        self.epsilon = epsilon
        self.action_num = action_num
        self.memory_buffer = Memory_Buffer_PER(memory_size, a=prio_a, e=prio_e)
        self.DQN = DQN(in_channels=in_channels, num_actions=action_num)
        self.DQN_target = DQN(in_channels=in_channels,
                              num_actions=action_num)
        self.DQN_target.load_state_dict(self.DQN.state_dict())

        self.USE_CUDA = USE_CUDA
        if USE_CUDA:
            self.DQN = self.DQN.cuda()
            self.DQN_target = self.DQN_target.cuda()
        self.optimizer = optim.RMSprop(
            self.DQN.parameters(), lr=lr, eps=0.001, alpha=0.95)

    def observe(self, lazyframe):
        # from Lazy frame to tensor
        # state = torch.from_numpy(
        #     np.array(lazyframe)[None]/255).float()  # (1,4,84,84)
        state = torch.tensor([lazyframe])
        if self.USE_CUDA:
            state = state.cuda()
        return state.to(torch.float)

    def value(self, state):
        q_values = self.DQN(state)
        return q_values

    def act(self, state, epsilon=None):
        """
        sample actions with epsilon-greedy policy
        recap: with p = epsilon pick random action, else pick action with highest Q(s,a)
        """
        if epsilon is None:
            epsilon = self.epsilon
        q_values = self.value(state).cpu().detach().numpy()
        # print("q_val:", q_values)
        if random.random() < epsilon:
            action = random.randrange(self.action_num)
        else:
            action = q_values.argmax(1)[0]
        return action

    def compute_td_loss(self, idxs, states, actions, rewards, next_states, is_done, gamma=0.99):
        """ Compute td loss using torch operations only. Use the formula above. """
        actions = torch.tensor(actions).long()    # shape: [batch_size]
        # shape: [batch_size]
        rewards = torch.tensor(rewards, dtype=torch.float)
        is_done = torch.tensor(is_done).bool()  # shape: [batch_size]

        if self.USE_CUDA:
            actions = actions.cuda()
            rewards = rewards.cuda()
            is_done = is_done.cuda()

        # get q-values for all actions in current states
        predicted_qvalues = self.DQN(states)

        # select q-values for chosen actions
        predicted_qvalues_for_actions = predicted_qvalues[
            range(states.shape[0]), actions
        ]

        # compute q-values for all actions in next states
        predicted_next_qvalues = self.DQN_target(next_states)  # YOUR CODE

        # compute V*(next_states) using predicted next q-values
        next_state_values = predicted_next_qvalues.max(-1)[0]  # YOUR CODE

        # compute "target q-values" for loss - it's what's inside square parentheses in the above formula.
        target_qvalues_for_actions = rewards + gamma * next_state_values  # YOUR CODE

        # at the last state we shall use simplified formula: Q(s,a) = r(s,a) since s' doesn't exist
        target_qvalues_for_actions = torch.where(
            is_done, rewards, target_qvalues_for_actions)

        # mean squared error loss to minimize
        errors = (predicted_qvalues_for_actions -
                  target_qvalues_for_actions).detach().cpu().squeeze().tolist()
        self.memory_buffer.update(idxs, errors)
        loss = F.smooth_l1_loss(
            predicted_qvalues_for_actions, target_qvalues_for_actions.detach())

        return loss

    def sample_from_buffer(self, batch_size):
        states, actions, rewards, next_states, dones = [], [], [], [], []
        idxs = []
        segment = self.memory_buffer.tree.total() / batch_size
        priorities = []

        for i in range(batch_size):
            a = segment * i
            b = segment * (i + 1)
            s = random.uniform(a, b)
            idx, p, data = self.memory_buffer.tree.get(s)

            frame, action, reward, next_frame, done = data
            states.append(self.observe(frame))
            actions.append(action)
            rewards.append(reward)
            next_states.append(self.observe(next_frame))
            dones.append(done)
            priorities.append(p)
            idxs.append(idx)
        return idxs, torch.cat(states), actions, rewards, torch.cat(next_states), dones

    def learn_from_experience(self, batch_size):
        if self.memory_buffer.size() > batch_size:
            idxs, states, actions, rewards, next_states, dones = self.sample_from_buffer(
                batch_size)
            td_loss = self.compute_td_loss(
                idxs, states, actions, rewards, next_states, dones)
            self.optimizer.zero_grad()
            td_loss.backward()
            for param in self.DQN.parameters():
                param.grad.data.clamp_(-1, 1)

            self.optimizer.step()
            return (td_loss.item())
        else:
            return (0)

class MyEnv(object):
    def __init__(self):
        self.reward = multiprocessing.Value('d', 0.0)
        self.s1 = multiprocessing.Value('d', 0.0)
        self.s2 = multiprocessing.Value('d', 0.0)
    def calangle(self, r_lon, r_lat, b_lon, b_lat):
        if b_lat < r_lat:
            # 第三象限
            if b_lon <= r_lon:
                m_angle = math.atan((b_lon - r_lon) * math.cos(b_lat) / (
                        b_lat - r_lat)) - math.pi
            # 第四象限
            elif b_lon > r_lon:
                m_angle = math.pi + math.atan(
                    (b_lon - r_lon) * math.cos(b_lat) / (
                            b_lat - r_lat))
        else:
            # 一二象限
            m_angle = math.atan((b_lon - r_lon) * math.cos(b_lat) / (
                    b_lat - r_lat))
        return m_angle

    def udp_server(self):
        try:
            # 变量声明
            port = 12046
            r_data = [1e-4, 1e-4, 1e-4]
            b_data = [2e-5, 2e-5, 2e-5]
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 重复使用绑定信息
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            address = ("127.0.0.1", port)
            server_socket.bind(address)
            while True:
                receive_data, client_address = server_socket.recvfrom(4096)
                unpack_data = struct.unpack(fmt, receive_data)
                # 判断是否为我机id
                if unpack_data[0] == 1:
                    r_data = unpack_data[1:]
                else:
                    b_data = unpack_data[1:]

                temp_s1 = self.calangle(r_data[0], r_data[1], b_data[0], b_data[1])
                self.s1.value = temp_s1 if temp_s1 > 0 else 2*math.pi + temp_s1
                temp_s2 = r_data[2]
                self.s2.value = temp_s2 if temp_s2 > 0 else 2*math.pi + temp_s2
                self.reward.value = math.cos(math.fabs(temp_s1 - temp_s2))
                # print(self.reward.value)

        finally:
            server_socket.close()
    def step(self, action):
        if action == 0:
            directkeys.turnleft(0.1)
        elif action == 1:
            directkeys.turnright(0.1)
    def reset(self):
        # return getframe.get4frame(True)
        return np.array([1.57, 1.57])




if __name__ == "__main__":

    env = MyEnv()
    # 通讯进程
    p1 = multiprocessing.Process(target=env.udp_server)
    p2 = multiprocessing.Process(target=env.udp_server)
    p1.start()
    p2.start()
    agent = DQN_PERAgent(in_channels=2,
                         action_num=2, USE_CUDA=USE_CUDA, lr=0.01)
    agent.DQN.load_state_dict(torch.load("./DQN_PER_dict.pth"))
    agent.DQN_target.load_state_dict(torch.load("./DQN_PER_dict.pth"))
    frame = np.array([1.57, 1.57])
    while True:
        epsilon = 1e-6
        # global frame
        state_tensor = agent.observe(frame)
        # print('state_tensor:', state_tensor)
        action = agent.act(state_tensor, epsilon)

        env.step(action)
        s11 = env.s1.value
        s22 = env.s2.value
        # print("s11:", s11)
        next_frame = np.array([s11, s22])
        done = False
        reward1 = env.reward.value
        # (next_frame, done), reward1 = env.step(action), reward.value

        frame = next_frame







