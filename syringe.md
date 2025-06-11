Materials

-   Raspberry pi 4 8GB
    
-   6V DC power supply
    
-   Panel mount barrel jack receptacle
    
-   Power distribution block
    
-   Linear servo actuator, Actuonix L16-100-63-6-R
    
-   M12 4-pin connector
    
-   M12 4-pin panel mount socket
    
-   M3 brass heat set inserts
    
-   22g Hookup wire
    
-   1/8” expandable wiring sleeve
    
-   Misc. M3 and M4 hardware
    
-   Jubilee tool vitamins (wedge plate and tool balls)
    

  

### Software

Directions for initiating the flask server on the Pi and configuring it for headless use for syringe control can be found [here](https://github.com/pozzo-research-group/digital_pipette_server/blob/main/readme.md)
  

Other Jubilee documentation can be found [here](https://science-jubilee.readthedocs.io/en/latest/index.html)

  
Additional documentation for the software can be found on the [github](https://github.com/machineagency/science-jubilee)

  

General recommendations

-   Ensure a static IP for the raspberry pi has been set
    

#### Required Imports

```python

from science_jubilee.Machine import Machine

from science_jubilee.tools import HTTPSyringe

from science_jubilee.decks import Deck # necessary for using labware

```

#### Prompts

```python

m = Machine(address = 'xxx.xxx.x.xx') # ip address of jubilee

m.load_tool(syringe_name)

deck = m.load_deck("deck_name")

  

syringe_name = HTTPSyringe.HTTPSyringe.from_config(2, '/home/clgould99/science-jubilee/src/science_jubilee/tools/configs/20_cc_glass1.json')

# file path to config file of the syringe

  

syringe_name.load_syringe(400, 1500) # set syringe location somewhere in the middle to start

  

# slowly jog the pulsewidth up and down to find your syringe's empty and full positions.

syinge_name.set_pulsewidth(1500, s = 200)

  

syringe_name.aspirate(volume, jubile_labware_location_to_aspriate_from) # aspirate command

```

Adjustments to duet configuration files

-   Tool post location
    
-   Set offsets so that there is no interference between syringe and other components
    

### Syringe Construction

1.  Heat set 7 M3 brass heat inserts. The preferred method for this was to pick up the heat insert using a soldering iron and then apply gentle downward pressure until the inserts were in the correct position The locations are shown below in red. Next, screw in 3 tool balls (shown below in blue).
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXe5L671D7JNMa5kHvGpgcBuzbHrwryKyIxwZZMFUAxzMpniX9tE9Y5iKDHCAPnrh-Md8n5xz4ExFaDMJ0xUxOV48Q2Yovo44yyRZNIAEKPN_Dc0g4zfnNk-Zvdff60FwzqzGnwI?key=sqBBidSwI9k4JZm9atlH3jcD)

2.  Screw the tool holder plate into the syringe holder
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXc-xWfwdJmQe7hKCJCnOXiCXE3W6EJF6dxt0l09TY9xejLU8rnuX7NP7Xy7wAHmcc5LRyp_bIrZ-i8f_k_BDwlizm2mJmyrWYRxwY8QcwPYFFK6FO_6UTWWZTOKUHRuRlxO3ztiOA?key=sqBBidSwI9k4JZm9atlH3jcD)

3.  Use 3 more heat inserts to secure the tool holder locking mechanism (wedge plate).
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXc1vfnB0muoRRVp-OsOimUdtNUUfuFo3RXxeTnhbkGsUUXITsxQJAGcrXr-IzeqSPAR8S-V8aVUTGZMOOMSS6XoBhcKZCZGYov4UTrBQD4vP8uui1Ab-kgOx9YjhPqGxnLhTPzWXQ?key=sqBBidSwI9k4JZm9atlH3jcD)

4.  Place 4 rubber O-rings on the wings.
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfPsAKTxNSFNVQvc9KzzYGv-f0xWGRFp5RH3ie9CYTddKPwKZWe1NtxAPQyQ7Bq4LuKBb9FxqkBXwPUoYHZ0XBKi0AcpeZWwAqsnu0iuTalkS-VZvJYVRYIGbUoQFdBfinB_CO5aw?key=sqBBidSwI9k4JZm9atlH3jcD)

5.  Install 2 m3 brass heat inserts on the tool holder bracket
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfcV_MjmjNJ_1BFfdu4ILO8f_tAX8LDvoU8j4RXRJt1xwBCVvkLz_ax2u16grUsYG5dCpPSDal8HoNv8qw5WSuJnud9UzlEkF5LjZlBq41jtw5zUV75eoUvT6dTNQJkjBPDBfK5eg?key=sqBBidSwI9k4JZm9atlH3jcD)

6.  Screw in the syringe plunger holder and secure using hex nut![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeoXu3R3ym8npgbDEwpzK9YcWew7g8y8cS4EX8nRAeTr0d-ed6XRognryDonOOQtULurNxWIWDKPcSKeeU6ghCoxmPvmOhRyphONSeEzEDPCxqc-sA67H-qQNVl9hGll_9h9XaS?key=sqBBidSwI9k4JZm9atlH3jcD)
    
7.  Install the actuator
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXehH4SWYfXMJ5Bnc4SloCuZ3eL59h45k57fLLKZtQ_z_a-c3r2MMUP3pqKw6Dt59NZv-vxVvjI0DahjNHDeHPCtifTOuNmgCiMANDM93qL9jjnOtFvAqm9BOu77SVCXZaAlH35o9w?key=sqBBidSwI9k4JZm9atlH3jcD)

  

8.  Slot the syringe into place and secure using 2 m4 screws
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXccjL4uXr3qNn5pFpIL9OxiYK0YjS0rt_1jPZOtnMYvwgDaZa7d0vPqkOOV7SowS_zilVpUpiKpSJI6BVzafIemt-qNjhX52QVmMhzIE912ixZ8jk1Q-h9PQ4ToisEXZD19Jjcx?key=sqBBidSwI9k4JZm9atlH3jcD)

  
  

### Control Box Construction

1.  Solder 22 gauge wire of a length approximately 7” to M12 4 Pin Male
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdIibmsuzerd1NnAU-2dvhp4d5YgBp1Oxd64-int5fDKWWsYfwmiEnsUZaRWdiU-n86XuZGKrZqX7lxN-EIKk5A9qMcq0wvKKNN4CZQSDv3P2PGl95Sv65YdIi5tXdON7HVohHR5Q?key=sqBBidSwI9k4JZm9atlH3jcD)

2.  Place threaded barrel jack power adapter through hole in control box pictured below
    
3.  Connect the 22 gauge wire in step 2 to ports A1 and B1 by unscrewing and rescrewing corresponding screws
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXejqYpn_8LmsC8jrgteyN1-oY0EFQJWSfl7uhhNk6qbieMbPCN0b7J2UUyF_p0jrhrhPDljlt3SA29m2jh8C3ZqOkSpsgjO6NdlTsC0V3ds1Yb8vIpxwBwiB-vALoB1hfYkSf66cQ?key=sqBBidSwI9k4JZm9atlH3jcD)

4.  Repeat steps 1-3 for each additional syringe/pipette unit
    
5.  Screw power distribution block into standoffs housing using M.2 6mm screws
    

  

6.  Connect power distribution block to Threaded Barrel Jack power adapter
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeBB6wusbjlwdsjauM7kn-takTpTBZDaTJ0BZtWbRU6BNl2kFb4V4liqvi6ralr8oW-Lwj7L4rUEe1a5MlYo_d-r7b2qHReRukVDVwU6arZ7nLCcBRpWzwgarg6WE1erUGYgcNA?key=sqBBidSwI9k4JZm9atlH3jcD)  ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXftZ64p76j6XbfAsaAoXJq50lt6QcuLE4cQTuDlOZOaCi7E1a_MnPO9dzwotzPdFaVyU-spmg2hOpbrVx7-kunz3EUThy8i7JYSMa7SOPKpVD1eNAv3irdZ3FheYj_n5JYFoCzcig?key=sqBBidSwI9k4JZm9atlH3jcD)

  

7.  Connect male M12 4 Pin to female m12 4 pin and attach to linear actuator (note that that the pins that the 22 gauge wires are connected to on the male need to match the pins that coming of out of the female connector)
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXc5Mx2V0pDSTudaZS3i9pJVCZ_WCzOo1gJN0Ce9pyKWDG8pX7IT0KeRNPOvCgui_elC2LwW_YKEjaqOlCBKtiDhQ8liqvthSYNPRvMDSQbZIO353-spbyq5crzovMoybPgRaOEy?key=sqBBidSwI9k4JZm9atlH3jcD)

8.  Connect power, ground, and input to raspberry pi. Any signal GPIO pin can be used as long it is correctly indicated on the configuration file. Refer to Raspberry Pi documentation for pinout.
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXe7tJXw0gNK5cf_EmxZ8nNzdBPT02FdVC4yVWxLdvK0z50APIY_YKA3ErHI6CilXtl6QgXbW_REvF_5EE0KCqUDE8DSJn_bLY47pOOPdEk_kxvl4TTQLB2k_6lxgLg4_NOvDg367g?key=sqBBidSwI9k4JZm9atlH3jcD)

9.  Install in control box as shown below after testing (May need to remove heatsink from Pi)
    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeLZFrillUThdTAy58jjcOgaAKd0p6L5YlttZt_asvxgPia2Mm-LaNkKKLH1iCGXtKx4i_w2LjM1J-14NWv0G_X2judOtfaGqe22uuoHk0e91Ceg-PkRgB_f9h930uqHhjG6mvw?key=sqBBidSwI9k4JZm9atlH3jcD)
