import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import torch
from cvxpylayers.torch import CvxpyLayer

"""initialzie"""
n = 1000  # number of timesteps
T = 50  # time will vary from 0 to T with step delt
ts = np.linspace(0, T, n + 1)
delt = T / n
gamma = .05  # damping, 0 is no damping

A = np.zeros((4, 4))
B = np.zeros((4, 2))
C = np.zeros((2, 4))

A[0, 0] = 1
A[1, 1] = 1
A[0, 2] = (1 - gamma * delt / 2) * delt
A[1, 3] = (1 - gamma * delt / 2) * delt
A[2, 2] = 1 - gamma * delt
A[3, 3] = 1 - gamma * delt

B[0, 0] = delt ** 2 / 2
B[1, 1] = delt ** 2 / 2
B[2, 0] = delt
B[3, 1] = delt

C[0, 0] = 1
C[1, 1] = 1

np.random.seed(6)

x = np.zeros((4, n + 1))
x[:, 0] = [0, 0, 0, 0]
y = np.zeros((2, n))

w = np.random.randn(2, n)
v = np.random.randn(2, n)

for t in range(n):
    y[:, t] = C.dot(x[:, t]) + v[:, t]
    x[:, t + 1] = A.dot(x[:, t]) + B.dot(w[:, t])

x_true = x.copy()
w_true = w.copy()
v_true = v.copy()

"""problem definition"""

x_dpp = cp.Variable((4, n + 1))
w_dpp = cp.Variable((2, n))
v_dpp = cp.Variable((2, n))
tau_dpp = cp.Parameter((1, 1), nonneg=True)

objective_fn = cp.sum_squares(w_dpp) + tau_dpp * cp.sum_squares(v_dpp)
constraints = []
for t in range(n):
    constraints += [x_dpp[:, t + 1] == A @ x_dpp[:, t] + B @ w_dpp[:, t],
                    y[:, t] == C @ x_dpp[:, t] + v_dpp[:, t]]

problem = cp.Problem(cp.Minimize(objective_fn), constraints)
print(problem.is_dcp(dpp=True))

assert problem.is_dcp(dpp=True)

"""Learning"""
x_target = torch.from_numpy(x_true.copy())

layer = CvxpyLayer(problem, parameters=[tau_dpp], variables=[x_dpp, w_dpp, v_dpp])

torch.manual_seed(3)
tau_dpp_hat = torch.randn((1, 1), requires_grad=True)

opt = torch.optim.Adam([tau_dpp_hat], lr=1e-2)
taus = []

EPOCHS = 300

for ephoc in range(EPOCHS):
    xx_hat, ww_hat, vv_hat = layer(tau_dpp_hat)

    loss = (xx_hat - x_target).norm()
    taus.append(tau_dpp_hat.clone().detach())
    opt.zero_grad()
    loss.backward(retain_graph=True)
    opt.step()

    print("ephoc = ", ephoc + 1)
    print(" - loss is ", loss)
    print(" - loss gradient is ", loss.grad)
    print(" - tau_hat is", tau_dpp_hat)
    print(" - tau_hat gradient is", tau_dpp_hat.grad)
    print()

tau_kf_dpp = tau_dpp_hat.detach().numpy()
print("result : learned tau is ", tau_kf_dpp[0][0])

""" plot """
x_kf_dpp = xx_hat.detach().numpy()

w_kf_vec_dpp = ww_hat.detach().numpy()
v_kf_vec_dpp = vv_hat.detach().numpy()

plt.figure(figsize=(8, 6))
plt.subplot(2, 2, 1)
plt.plot(ts, x[0, :])
plt.plot(ts, x_kf_dpp[0, :])
plt.xlabel('time')
plt.ylabel('x position')
plt.subplot(2, 2, 2)
plt.plot(ts, x[1, :])
plt.plot(ts, x_kf_dpp[1, :])
plt.xlabel('time')
plt.ylabel('y position')
plt.subplot(2, 2, 3)
plt.plot(ts, x[2, :])
plt.plot(ts, x_kf_dpp[2, :])
plt.xlabel('time')
plt.ylabel('x velocity')
plt.subplot(2, 2, 4)
plt.plot(ts, x[3, :])
plt.plot(ts, x_kf_dpp[3, :])
plt.xlabel('time')
plt.ylabel('y velocity')

plt.figure(figsize=(8, 6))
plt.plot(x[0, :], x[1, :], '-', alpha=0.8, linewidth=5, label='True')
plt.plot(y[0, :], y[1, :], 'ko', alpha=0.1, label='Measurement')
plt.plot(x_kf_dpp[0, :], x_kf_dpp[1, :], '-', alpha=0.8, linewidth=5, label='KF_dpp estimates')
plt.title(r'Trajectory $\tau$ = %f' % tau_kf_dpp[0][0])
plt.legend()
plt.xlabel(r'$x$ position')
plt.ylabel(r'$y$ position')
plt.xlim(-5, 15)
plt.ylim(-10, 25)

taus_t = np.zeros(EPOCHS)

for i in range(EPOCHS):
    taus_t[i] = taus[i][0][0].detach().numpy()

iterations = np.arange(1, EPOCHS + 1)

plt.figure(figsize=(8, 6))
plt.plot(iterations[:-200], taus_t[:-200], '-', alpha=0.8, linewidth=5, label='tau')
plt.title('taus')
plt.legend()
plt.xlabel(r'iteration')
plt.ylabel(r'$\tau$')
