# 3D $N$-Body Orbital Simulator

An interactive 3D gravitational $N$-body simulator for the Solar System (Sun, 8 planets, and the Moon) built with Python, `NumPy`, `Matplotlib`, and `PyQt6`, using custom 4th-order Runge–Kutta (`rk4`) integration from [`physicslib`](https://github.com/Michu-star/physicslib).

## Physics & Numerical Model

The simulator integrates the coupled Newtonian equations of motion for $N = 10$ point masses in 3D Cartesian coordinates:

$$\ddot{\mathbf{r}}_i = -G \sum_{\substack{j=1 \\ j \neq i}}^{N} m_j \frac{\mathbf{r}_i - \mathbf{r}_j}{\|\mathbf{r}_i - \mathbf{r}_j\|^3}$$

- **System of Units**: Astronomical Units ($\text{AU}$) for distance, Earth years ($\text{yr}$) for time, and Earth masses ($M_\oplus$) for mass.
- **Time Integration**: Coupled 60-dimensional first-order state vector integrated over $t \in [0, 50]\;\text{yr}$ ($20\,000$ steps, $\Delta t = 2.5 \times 10^{-3}\;\text{yr}$) via explicit 4th-order Runge–Kutta (`rk4`).

## Conservation Diagnostics

To verify numerical accuracy and monitor integrator drift, the simulation tracks conserved mechanical quantities across all time steps:

1. **Relative Total Energy Error**:
   $$\frac{E(t) - E(0)}{E(0)}, \quad E = \sum_{i} \frac{1}{2} m_i \|\mathbf{v}_i\|^2 - \sum_{i < j} \frac{G m_i m_j}{\|\mathbf{r}_i - \mathbf{r}_j\|}$$
2. **Total Linear Momentum**:
   $$\mathbf{P}(t) = \sum_{i} m_i \mathbf{v}_i(t)$$
3. **Relative Center-of-Mass Angular Momentum Error**:
   $$\frac{L_z(t) - L_z(0)}{L_z(0)}, \quad \mathbf{L}_{\text{CM}} = \sum_{i} m_i (\mathbf{r}_i - \mathbf{r}_{\text{CM}}) \times (\mathbf{v}_i - \mathbf{v}_{\text{CM}})$$

## Interactive GUI (`PyQt6` + `Matplotlib`)

- **Time Scrubber (`QSlider`)**: Step through the 50-year trajectory history with synchronized vertical time markers on the energy, momentum, and angular momentum diagnostic plots.
- **Reference Frame Toggle (`QPushButton`)**: Switch dynamically between the heliocentric **Solar System view** ($\pm 31\;\text{AU}$) and a co-moving **Earth–Moon view** ($\pm 0.004\;\text{AU}$ centered on Earth).

## Project Structure

- `main.py` — `Body` and `Simulation` classes, ODE right-hand side, conservation law calculations, and solar system initial conditions.
- `gui.py` — `PyQt6` `MainWindow` embedding a multi-panel `Matplotlib` canvas, navigation toolbar, time slider, and view mode toggle.
- `plotting.py` — Scene rendering and conservation diagnostic subplot routines.

## Installation & Usage

```bash
pip install -r requirements.txt
python main.py
```
