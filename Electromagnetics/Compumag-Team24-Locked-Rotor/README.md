# Compumag TEAM-24: Nonlinear Time-Transient Rotational Test Rig

The benchmark case [1] is a transient magnetic problem involving eddy currents and nonlinear materials, solved using [case.py](case.py). The geometry is shown below:

<div align="center">
    <img src="data/Geometry.png" alt="Geometry" width="85%">
    <br/>
    Figure 1: The geometry consists of a rotor locked at 22°, a stator, and two coils surrounded by an air domain.
</div>
<br/>

The [mesh](geometry.mesh) was created using Netgen, with the mesh file exported to MFEM v1.3 format.

The goal of the benchmark is to calculate the torque acting at the rotor.

## Setup



### Updating the B-H curve 

The *rotor* and *stator* are made of iron material with a constant electrical conductivity of
$\sigma = 4.54 	\times 10^6 \frac{\rm{S}}{\rm{m}}$ and a nonlinear permeability specified through a B-H curve. 
However, as pointed out by [2], the provided [B-H curve](data/tables/Table_1_BH_curve.csv) lacks sufficient data 
between zero and the first data point, leading to significant errors. To address this issue, the modified Fröhlich
formula is used to fit the data (the modification ensures physical behavior [3]). The modified Fröhlich formula is given by:

$$
B(H) = \frac{1}{a + b H} + \mu_0 H \quad,
$$

where \(a\) and \(b\) are fitting parameters. We calculate these parameters based on the complete curve and use them to interpolate the initial part.

| [Original B-H Curve](data/tables/Table_1_BH_curve.csv) | [Modified B-H Curve](data/tables/Updated_BH_curve.csv) |
| ----------------- | ------------------------------- |
| ![B-H Curve](data/tables/Table_1_BH_curve.png) | ![B-H Curve](data/tables/Updated_BH_curve.png) |


### Setting the coils

The for coils, we apply a constant electric voltage of $U=23.1 \mathrm{V}$. This results in a current raise which is
compared to the [reference](data/tables/Table_3_Coil_Current.csv).

<div align="center">
    <img src="data/tables/Table_3_Coil_Current.png" alt="Coil Current" width="50%">
    <br/>
    Figure 3: The measured coil current rise for a constant applied voltage on the coils.
</div>
<br/>


### Skin-depth layered mesh

As the iron is conductive, eddy currents are observed in the stator and rotor parts. 
To accurately capture those, we use a mesh with a *prismatic boundary layer*. 
As a rule-of-thumb it is recommended to resolve about three layers, where a layer
is the skin-depth which for time-harmonic problems can be estimated by
$$
\delta_s =\sqrt{\frac{2}{\omega \mu \sigma}} \quad,
$$
where $\omega=2 \pi f$ and $f$ is the frequency of the excitation.
However, in time-transient problems there is no single frequency — instead, the response is governed by
the time scale of excitation (e.g. rise time $\tau$).

For a linear setup assuming only a single coil, where a voltage of $V$ is applied and
ignoring eddy currents, the current raise is given by
$$
I = \frac{V}{R} \left( 1 - \exp \left[ - \frac{t}{\tau} \right] \right) \quad,
$$
where $\tau = \frac{L}{R}$, $R$ is the resistance of the coil, and $L$ is the inductance.

We estimate the time constant $\tau$ by calculating the inductance matrix using the
[Magnetic Inductance Report](https://raiden-numerics.github.io/mufem-doc/models/electromagnetics/excitation_coil/reports/magnetic_inductance_report.html) and the resistance using the
[Resistance Report](https://raiden-numerics.github.io/mufem-doc/models/electromagnetics/excitation_coil/reports/resistance_report.html) for our case here using following snippet:

```python

sim.initialize()

inductance_report = MagneticInductanceReport("Coil Inductance")

print("Inductance Value:\n", inductance_report.evaluate())

resistance_report = MagneticInductanceReport("Coil Inductance")

print("Resistance Value:\n",  resistance_report.evaluate())
```

gives 

```bash
>>> Inductance Value:
    [0.0117051, 0.00197861]
    [0.00197861, 0.0117273]

>>> Resistance Value:
    0.5145621732484141
```
So the time scale is given by $\tau = L / R \sim 0.01 /  0.5 = 0.02$. Note that for this benchmark here we have
non-linear materials and include eddy currents so this only provides a ball park estimate.

Eddy currents penetrate into the material with a diffusion like behavior where the penetration depth
can be estimated by
$$
\delta = \sqrt{D \tau} \quad,
$$
where $\delta$ is the penetration depth, $D=\frac{1}{\mu \sigma}$ is the diffusivity constant and $\tau$ is the time-scale.

<div align="center">
    <img src="results/Scene_ElementType.png" alt="Element Type" width="50%">
    <br/>
    Figure 4: A prismatic boundary layer is used (Element Type: 6) to effectively capture the skin-depth effects. The
    interior is meshed with tetrahedral elements (Element Type: 4).
</div>
<br/>



### Torque calculation

Finally, we create a [Magnetic Torque Report](https://raiden-numerics.github.io/mufem-doc/models/electromagnetics/time_domain_magnetic/reports/magnetic_torque_report.html) to measure the magnetic torque on the locked rotor over time and compare it with the reference.


## Results


After installing mufem run the simulation by executing [case.py](case.py) with
```bash
> pymufem case.py
...
174 1.130105e-11
ReportMonitor: Rotor Torque Monitor : [0.026124448259359362, -0.002966364046512432, 1.320018800598565]
Time: 0.14500000000000005 of 0.15 with Δt=0.005
175 2.676986e-07
electromagnetic.TimeDomainMagneticModel,
176 3.036165e-11
177 1.210335e-11
178 1.184276e-11
179 1.172570e-11
180 1.173960e-11
ReportMonitor: Rotor Torque Monitor : [0.02618167920146705, -0.002974783431187636, 1.323128413798604]
Time: 0.15000000000000005 of 0.15 with Δt=0.005
Simulation done. Thank you for using the software.
```


The script [case.py](case.py) includes a subsequent analysis section that extracts the *coil current vs time* and 
*torque vs. time* data and creates a plot to compare to the [reference for the coil current](data/tables/Table_3_Coil_Current.csv)

<div align="center">
    <img src="results/Coil_Current_vs_Time.png" alt="Coil Current vs Time" width="50%">
    <br/>
    Figure 5: The coil current is well reproduced when comparing to the reference.
</div>
<br/>

and for the [reference for the rotor torque](data/tables/Table_4_Torque.csv)

<div align="center">
    <img src="results/Rotor_Torque_vs_Time.png" alt="Rotor Torque vs Time" width="50%">
    <br/>
    Figure 6: The rotor torque is well reproduced when comparing to the reference.
</div>
<br/>


To create the animation, make sure that in [case.py](case.py) we set following variable 
```python
output_for_animation = True
```

then run the case and finally run the script `paraview_gif.py`(paraview_fig.py) (requires the installation of
`ffmpeg`). This creates below animation:

<div align="center">
    <img src="results/Result_Animation.gif" alt="Result Animation" width="85%">
    <br/>
    Figure 7: The aninmation of the Electric Current Density.
</div>
<br/>


## References

[1] https://www.compumag.org/wp/wp-content/uploads/2018/06/problem24.pdf

[2] Rüberg, T., Kielhorn, L., and Zechner, J., 2021. Electromagnetic devices with moving parts—simulation with FEM/BEM coupling. *Mathematics*, 9(15), p.1804.

[3] Diez, P., and Webb, J.P., 2015. A Rational Approach to \( B \)–\( H \) Curve Representation. *IEEE Transactions on Magnetics*, 52(3), pp.1-4.