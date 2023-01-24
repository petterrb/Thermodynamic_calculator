# Thermodynamic Calculator
## User manual

Upon launch, you will be met with the following screen:
````
2      Properties of Saturated Water (Liquid-Vapor): Temperature Table
3      Properties of Saturated Water (Liquid-Vapor): Pressure Table
13     Properties of Saturated Ammonia (Liquid-Vapor): Temperature Table
14     Properties of Saturated Ammonia (Liquid-Vapor): Pressure Table
22     Ideal Gas Properties of Air
23     Ideal Gas Properties of Selected Gases
27     Logarithms to the Base 10 of the Equilibrium Constant K
140    Thermophysical Properties of Air at Atmospheric Pressure
141    Thermophysical Properties of Water Vapor (Steam) at Atmospheric Pressure
149    Thermophysical Properties of Nitrogen at Atmospheric Pressure
151    Thermophysical Properties of Engine Oil (Saturated Liquid)
160    Thermophysical Properties of Saturated Water
````

Enter the number on the left to access your desired table. Next you will be asked to enter a property and its value. For instance, if you selected table 2, you might want to know the enthalpy and pressure of saturated water at 50 °C. Enter "temp" and 50, and you will obtain the results on the following format:
````
You have chosen: Properties of Saturated Water (Liquid-Vapor): Temperature Table
Known property: temp
Value: 50
------------------------------------------
temp       50.0                  C         
press      0.1235                bar       
vf         1.0121     1.0e-03    m3/kg     
vg         12.032                m3/kg     
uf         209.32                kJ/kg     
ug         2 443.5               kJ/kg     
hf         209.33                kJ/kg     
hfg        2 382.7               kJ/kg     
hg         2 592.1               kJ/kg     
sf         0.7038                kJ/kgK    
sg         8.0763                kJ/kgK    
------------------------------------------
````

Note that, depending on your screen size, you may have to scroll back up a bit to view them, as the list of tables will be printed immediately after the results.

## Creating Your Own Tables
You may find that a table you need is not included in the repo. You can add a table yourself using the following steps:
* Add headers
    * table ID
    * table name
    * list of column names (properties)
    * list of units
    * list of multipliers (e.g. 1 or 1e-3)
* Add data

Below is an example:
````
160
Thermophysical Properties of Saturated Water
temp press vf vg hfg cp_f cp_g mu_f mu_g kf kg Pr_f Pr_g sigma_f beta_f
K bar m3/kg m3/kg kJ/kg kJ/kgK kJ/kgK Ns/m2 Ns/m2 W/mK W/mK - - N/m 1/K
1 1 1e-3 1 1 1 1 1e-6 1e-6 1e-3 1e-3 1 1 1e-3 1e-6
273.15 0.00611 1.000 206.3 2502 4.217 1.854 1750 8.02 569 18.2 12.99 0.815 75.5 -68.05
275 0.00697 1.000 181.7 2497 4.211 1.855 1652 8.09 574 18.3 12.22 0.817 75.3 -32.74
280 0.00990 1.000 130.4 2485 4.198 1.858 1422 8.29 582 18.6 10.26 0.825 74.8 46.04
285 0.01387 1.000 99.4 2473 4.189 1.861 1225 8.49 590 18.9 8.81 0.833 74.3 114.1
290 0.01917 1.001 69.7 2461 4.184 1.864 1080 8.69 598 19.3 7.56 0.841 73.7 174.0
295 0.02617 1.002 51.94 2449 4.181 1.868 959 8.89 606 19.5 6.62 0.849 72.7 227.5
300 0.03531 1.003 39.13 2438 4.179 1.872 855 9.09 613 19.6 5.83 0.857 71.7 276.1
...
````

## Using the GeneralTable class
The GeneralTable class can be used in scripts. This is especially useful when solving equations iteratively. Rather than provide an in depth documentation here, I would advise you to look in the exercises-folder to see how it has been implemented for various assignments.