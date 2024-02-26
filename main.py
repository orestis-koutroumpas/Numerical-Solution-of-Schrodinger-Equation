import numpy as np
from utils import *
### First git comment ###
def main():
    print_startup()
    
    while True:
        print("\nChoose Potential or Exit:")
        print("1. Finite Well")
        print("2. Harmonic Oscillator")
        print("3. Pöschl-Teller")
        print("4. Double Finite Well")
        print("5. Superlattice")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6) then press Enter: ")
        
        if choice == '1':
            finite_well(int(choice))
        elif choice == '2':
            harmonic_well(int(choice))
        elif choice == '3':
            poschl_teller_well(int(choice))
        elif choice == '4':
            double_finite_well(int(choice))
        elif choice == '5':
            superlattice(int(choice))
        elif choice == '6':
            print("\nExiting... \n")
            break
        else:
            print("Invalid Input. Please choose a number between 1 and 6.")

# Particle in a finite well of width (W) and depth (D)
def finite_well(Case, steps=2000):
    # Set well depth and width
    A=1.0 
    D=100.0 
    # Divide by two so a well from -W to W is of input width
    W=A/2.0
    # Create x-vector from -W to W
    xvec=np.linspace(-A,A,steps,dtype=np.float_)
    # Get step size
    h=xvec[1]-xvec[0]
    # Create the potential from step function
    U=-D*(step_func(xvec+W)-step_func(xvec-W))
    E,V,n = solve_schrodinger(U,h,steps)
    # Print output
    output(Case, ['Well Width','Well Depth'],[W*2,D],E,n)
    # Create plot
    well_plot(E,V,xvec,steps,n,Case,U)

# Particle in a harmonic well of depth (D) and angular frequency (omega)
def harmonic_well(Case, steps=2000):
    # Set well angular frequency and depth
    omega=0.5 
    D=2
    # Divide by two so a well from -W to W is of input width
    W=np.sqrt(np.abs(2.0*D)/(omega**2))
    # Set length variable for xvec
    A=W*2.0
    # create x-vector from -A to A
    xvec=np.linspace(-A,A,steps,dtype=np.float_)
    # Get step size
    h=xvec[1]-xvec[0]
    # Create the potential from harmonic potential function
    U=harmonic_potential(xvec,omega,D)
    E,V,n = solve_schrodinger(U,h,steps)
    # Print output
    output(Case,['k','Depth (a.u.)'],[1*omega**2,D],E,n) # m=1, k = mω^2 = ω^2
    # Create plot
    well_plot(E,V,xvec,steps,n,Case,U)

# Particle in a PÖSCHL-TELLER Potential with parameters (A, B, C)
def poschl_teller_well(Case,steps=2000):
    # Set parameters for the potential
    A = 20.0  # Parameter influencing the depth and shape of the potential well
    B = 5.0 # Parameter influencing the width of the potential well
    C = 5.0 # Constant term adjusting the overall energy scale of the potential
    # Calculate other required variables and components for the potential
    W = np.sqrt(np.abs(2.0 * C) / (A * (A + 1)))
    A_range = 2.0 * W
    # Create x-vector from -W to W
    xvec = np.linspace(-A_range, A_range, steps, dtype=np.float_)
    # Get step size
    h = xvec[1] - xvec[0]
    # Create the potential from poschl-teller function
    U = poschl_teller_potential(xvec, A, B, C)
    E,V,n = solve_schrodinger(U,h,steps)
    # Print output
    output(Case, ['A', 'B', 'C'], [A, B, C], E, n)
    # Create plot
    well_plot(E, V, xvec, steps, n, Case, U)
    
# Particle in a Double Finite Well of width (W), distance (B) apart
def double_finite_well(Case, steps=2000):
    # Set depths and widths of wells and the well separation
    W=1.0 
    D=100.0 
    B=1 
    # Set length variable for xvec
    A=2.0*((2*W)+B)
    # Divide by two so a separation from -B to B is of input size
    B=B/2.0
    # Create x-vector from -A to A
    xvec=np.linspace(-A,A,steps,dtype=np.float_)
    # Get step size
    h=xvec[1]-xvec[0]
    # Create the potential from step function
    U=-D*(step_func(xvec+W+B)-step_func(xvec+B)+\
        step_func(xvec-B)-step_func(xvec-W-B))
    E,V,n = solve_schrodinger(U,h,steps)
    # Print output
    output(Case,['Well Width','Well Depth','Distance Apart'],[W,D,B*2],E,n)
    # Create plot
    well_plot(E,V,xvec,steps,n,Case,U)
    
# Particle in Superlattice of period (period) and depth (D)
def superlattice(Case,steps=2000):
    # Set the period and depth of the superlattice potential
    period = 2.5
    D = 25
    # Set length variable for xvec
    A = 2.0 * period
    # Create x-vector from -A to A
    xvec = np.linspace(-A, A, steps, dtype=np.float_)
    # Get step size
    h = xvec[1] - xvec[0]
    # Create the periodic potential
    U = -D * (step_func(np.mod(xvec, period)) - 0.5)
    E,V,n = solve_schrodinger(U,h,steps)
    # Print output
    output(Case,['Period', 'Depth'],[period, D],E,n)
    # Create plot
    well_plot(E,V,xvec,steps,n,Case,U)

### Different Potentials ###

def step_func(x):
    return 0.5*(1+np.sign(x))

def harmonic_potential(x,omega,D):
    return 0.5*(omega**2)*(x**2)-D

def poschl_teller_potential(x, A, B, C):
    return -A * (A + 1) / np.cosh(B * x) ** 2 + C
   
if __name__ == "__main__":
    main()