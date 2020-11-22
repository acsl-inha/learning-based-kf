import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import torch
from cvxpylayers.torch import CvxpyLayer

"""Initialize"""

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

"""probleom definition"""
x_dpp = cp.Variable((4, n + 1))
w_dpp = cp.Variable((2, n))
v_dpp = cp.Variable((2, n))

# quad_form means : WT * Q * W
Q_sqrt = cp.Parameter((2, 2))
quad_form = cp.sum_squares(Q_sqrt @ w_dpp[:, 0])
for t in range(1, n):
    quad_form += cp.sum_squares(Q_sqrt @ w_dpp[:, t])

objective_fn = quad_form + cp.sum_squares(v_dpp)

constraints = []
for t in range(n):
    constraints += [x_dpp[:, t + 1] == A @ x_dpp[:, t] + B @ w_dpp[:, t],
                    y[:, t] == C @ x_dpp[:, t] + v_dpp[:, t]]

problem = cp.Problem(cp.Minimize(objective_fn), constraints)
print(problem.is_dcp(dpp=True))
assert problem.is_dcp(dpp=True)

""" Learning """

x_target = torch.from_numpy(x_true.copy())
w_target = torch.from_numpy(w_true.copy())
v_target = torch.from_numpy(v_true.copy())

layer = CvxpyLayer(problem, parameters=[Q_sqrt], variables=[x_dpp, w_dpp, v_dpp])

# Q_sqrt_hat = torch.tensor([[1.1 , 0.01],[0.01 , 1.1]], requires_grad=True)
torch.manual_seed(25)
Q_sqrt_hat = torch.rand((2, 2), requires_grad=True)

opt = torch.optim.Adam([Q_sqrt_hat], lr=1e-2)

EPOCHS = 500
Qs = np.zeros((EPOCHS, 2, 2))

for ephoc in range(EPOCHS):
    xx_hat, ww_hat, vv_hat = layer(Q_sqrt_hat)

    loss = (xx_hat - x_target).norm()
    QQ_sqrt = Q_sqrt_hat.clone().detach().numpy()
    QQ = QQ_sqrt.T @ QQ_sqrt
    Qs[ephoc, :, :] = QQ
    opt.zero_grad()
    loss.backward(retain_graph=True)
    opt.step()

    print("ephoc = ", ephoc + 1)
    print(" - loss is ", loss)
    print(" - Q_sqrt is |", QQ_sqrt[0, 0], ",  ", QQ_sqrt[0, 1], "|")
    print("             |", QQ_sqrt[1, 0], ",  ", QQ_sqrt[1, 1], "|")
    print()
    print(" -    Q   is |", QQ[0, 0], ",  ", QQ[0, 1], "|")
    print("             |", QQ[1, 0], ",  ", QQ[1, 1], "|")
    print()

""" plot result """
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
plt.title(r'Trajectory')
plt.legend()
plt.xlabel(r'$x$ position')
plt.ylabel(r'$y$ position')
plt.xlim(-5, 15)
plt.ylim(-10, 25)

iterations = np.arange(1, EPOCHS + 1)

plt.figure(figsize=(12, 12))
plt.subplot(2, 2, 1)
plt.title('Q(1,1)')
plt.plot(iterations[:-200], Qs[:-200, 0, 0], '-', alpha=0.8, linewidth=2, label='True')
plt.xlabel('iterations')
plt.ylabel('Q(1,1)')

plt.subplot(2, 2, 2)
plt.title('Q(1,2) == Q(2,1)')
plt.plot(iterations[:-200], Qs[:-200, 0, 1], '-', alpha=0.8, linewidth=2, label='True')
plt.xlabel('iterations')
plt.ylabel('Q(1,2) == Q(2,1)')
plt.subplot(2, 2, 3)

plt.title('Q(2,1) == Q(1,2)')
plt.plot(iterations[:-200], Qs[:-200, 1, 0], '-', alpha=0.8, linewidth=2, label='True')
plt.xlabel('iterations')
plt.ylabel('Q(2,1) == Q(1,2)')
plt.subplot(2, 2, 4)

plt.title('Q(2,2)')
plt.plot(iterations[:-200], Qs[:-200, 1, 1], '-', alpha=0.8, linewidth=2, label='True')
plt.xlabel('iterations')
plt.ylabel('Q(2,2)')
