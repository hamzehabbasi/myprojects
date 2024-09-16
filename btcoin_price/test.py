import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# تعریف ماتریس A
A = np.array([
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, -1],
    [1, 1, 1, -2, 0],
    [1, 1, -3, 0, 0],
    [1, -(5-1), 0, 0, 0]
])

# بردار اولیه
x0 = np.array([1, 0, 0, 0, 0])

# تابعی که دستگاه دیفرانسیلی را تعریف می‌کند
def system(x, t):
    return A.dot(x)

# بازه زمانی
t = np.linspace(0, 10, 100)

# حل دستگاه
x_t = odeint(system, x0, t)

# رسم نتایج
plt.figure(figsize=(10, 6))
for i in range(x_t.shape[1]):
    plt.plot(t, x_t[:, i], label=f'x{i+1}(t)')
plt.xlabel('Time')
plt.ylabel('x(t)')
plt.legend()
plt.title('Solution of the Dynamical System')
plt.grid(True)
plt.show()
