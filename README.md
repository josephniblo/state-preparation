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

or letting 
$$
\begin{align}
z &:= \frac{\alpha - i \beta}{\sqrt{2}} \\
w &:= \frac{\alpha + i \beta}{\sqrt{2}}
\end{align}
$$

this can be simplified to

$$
\begin{align}
\theta_{\mathrm{QWP}}(\alpha, \beta) &= \frac{1}{2} \left( \arg\left( w \right) - \arg \left( z \right) \right) \\

\theta_{\mathrm{HWP}}(\alpha, \beta) &= \frac{1}{2} \left(\theta_{\mathrm{QWP}} +  \arccos\left( |z| \right) - \frac{\pi}{4} \right)
\end{align}
$$

In the case that we start with a state other than $\ket{\psi} = \ket{H}$, say $\ket{\psi} = \ket{\phi}$, we need only rewrite $\ket{\psi}_{\text{target}} = \alpha' \ket{\phi} + \beta' \ket{\phi^\perp}$, where $\ket{\phi^\perp}$ is the state orthogonal to $\ket{\phi}$, then the expressions above hold, with $\left(\alpha, \beta\right) \to \left(\alpha', \beta' \right)$.