# State Preparation

Establishing waveplate positions required for state preparation.

## Explicit Form

For a target state $\ket{\psi}_{\text{target}} = \alpha \ket{H} + \beta \ket{V}$, where $\alpha, \beta \in \mathbb{C}$ and assuming the inital state before the waveplates is $\ket{\psi}_{\text{initial}} = \ket{H}$, then the explicit form of the waveplate angles are given below, as:

$$
\begin{align}
\theta_{\mathrm{HWP}}(\alpha, \beta) &= \frac{1}{4} \arg\left( e^{-i \arg\left(\frac{\alpha - i \beta}{\sqrt{2}}\right)} \cdot \frac{\alpha + i \beta}{\sqrt{2}} \right) \nonumber \\
&\quad + \frac{1}{2} \arccos\left( e^{-i \arg\left(\frac{\alpha - i \beta}{\sqrt{2}}\right)} \cdot \frac{\alpha - i \beta}{\sqrt{2}} \right) - \frac{\pi}{8} \\
\theta_{\mathrm{QWP}}(\alpha, \beta) &= \frac{1}{2} \arg\left( e^{-i \arg\left( \frac{\alpha - i \beta}{\sqrt{2}} \right)} \cdot \frac{\alpha + i \beta}{\sqrt{2}} \right)
\end{align}
$$
