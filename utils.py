import os
import scipy.linalg as spla
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
try:
    from colorama import Fore,Back,Style
    from colorama import init
    init(autoreset=True)
    print_color=True
except:
    print_color=False

titles={
    1: "Particle in a Finite Well",
    2: "Particle in a Harmonic well",
    3: "Particle in a Poschl-Teller Potential",
    4: "Particle in a Double Finite Well",
    5: "Particle in Superlattice"}
 
### Input / Output Functions ###

def print_center_text(s):
    count = len(s)
    pad = (101 - count) // 2
    print(' ' * pad + s)

def print_startup():
    clear_screen()
    print("\n" + '=' * 101)
    print_center_text('Welcome')
    print_center_text('Program for solving the time independent Schrödinger equation!')
    print('=' * 101)

def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Mac and Linux
    else:
        _ = os.system('clear')
        
def output(Case,input_fields,input_values,E,n):
    print("")
    print('='*101)
    print_center_text(f'Solution of Schrödinger equation for option {Case}')
    print('='*101)
    print_center_text(titles[Case])
    print("\t\tInput:")
    for i,j in zip(input_fields,input_values):
        print_center_text(str(i)+' : '+str(j))
    print("")
    print("\t\t{} Eigenvalues of Energy:".format(n))
    for i in range(n):
        print_center_text(f"E({i})=" + "{:.5f}".format(E[i]))
    print('='*101)
    print("")

### Solving Schrödinger equation using 3-point finite-difference method ###

def solve_schrodinger(U,h,steps):
    # Atomic Units
    hbar=1.0
    m=1.0
    # Create Laplacian via 3-point finite-difference method
    Laplacian=(-2.0*np.diag(np.ones(steps))+np.diag(np.ones(steps-1),1)\
        +np.diag(np.ones(steps-1),-1))/(float)(h**2)
    # Create the Hamiltonian Matrix
    Hamiltonian=np.zeros((steps,steps))
    [i,j]=np.indices(Hamiltonian.shape)
    Hamiltonian[i==j]=U
    Hamiltonian+=(-0.5)*((hbar**2)/m)*Laplacian
    # Diagonalize the Hamiltonian yielding the wavefunctions and energies
    diagonalize_hamiltonian = lambda Hamiltonian: spla.eigh(Hamiltonian)
    E,V=diagonalize_hamiltonian(Hamiltonian)
    # Determine theoretical number of energy levels (n)
    n=0
    while E[n]<0:
        n+=1
    return E, V, n

### Plot Functions ###

def well_plot(E, V, xvec, steps, n, Case, U):
    # Scale potential and prepare for plotting
    V_new, ScaleFactor, U_new, n = well_plot_scaling(E, V, U, n, steps)
    # Create a figure with larger size
    f = plt.figure(figsize=(10, 6))
    # Add plot to the figure
    ax = f.add_subplot(111)
    # Plot V(x)
    potential_line, = ax.plot(xvec, U_new, c='#333333', label='V(x)')
    legend_handles = [potential_line]
    # Find appropriate x limits
    MinX = 0
    MaxX = len(xvec) - 1
    while U_new[MinX] == 0:
        MinX += 1
    while U_new[MaxX] == 0:
        MaxX -= 1
    for m in range(n):
        V_old = V_new[MinX + 1, m]
        while (np.abs(V_old - V_new[MinX, m]) > 1e-6 and MinX > 0):
            V_old = V_new[MinX, m]
            MinX -= 1
        V_old = V_new[MaxX - 1, m]
        while (np.abs(V_old - V_new[MaxX, m]) > 1e-6 and MaxX < len(xvec) - 1):
            V_old = V_new[MaxX, m]
            MaxX += 1
    plt.xlim(xvec[MinX], xvec[MaxX])
    # Set x and y limits for visibility
    if (np.max(V_new) > 0):
        if (np.min(V_new) > np.min(U_new)):
            plt.ylim(1.05 * np.min(U_new), np.max(V_new) + abs(0.05 * np.min(U_new)))
        else:
            plt.ylim(1.05 * np.min(V_new), np.max(V_new) + abs(0.05 * np.min(U_new)))
    else:
        if (np.min(V_new) > np.min(U_new)):
            plt.ylim(1.05 * np.min(U_new), np.max(U_new) + abs(0.05 * np.min(U_new)))
        else:
            plt.ylim(1.05 * np.min(V_new), np.max(U_new) + abs(0.05 * np.min(U_new)))
    # Plot wave functions
    for i in np.arange(n - 1, -1, -1):
        color = mpl.cm.jet_r((i) / (float)(n), 1)
        wavefunc = ax.plot(xvec, V_new[0:steps, i], c=color, label='E(a.u.)={}'.format(np.round(E[i] * 1000) / 1000.0))
        ax.axhline(y=V_new[0, i], xmin=-10, xmax=10, c=color, ls='--')
        legend_handles.append(wavefunc[0])
    # Set plot title, x-label, and y-label
    ax.set_title('{}'.format(titles[Case]))
    plt.xlabel('Width / (a.u.)')
    plt.ylabel('Energy / (a.u.)')
    # Modify tick marks
    ax.set_yticklabels(np.round(ax.yaxis.get_ticklocs() * ScaleFactor))
    # Add plot legend to the right of the plot
    plt.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, 0.7 * box.width, box.height])
    
    plt.show()

def well_plot_scaling(E,V,U,n,steps):
    # scale the wave functions
    order=np.argsort(E)  # Sort energy eigenvalues to determine order
    Converged=False # Initialize convergence check
    # Convergence loop for scaling
    while(Converged is False):
        E_copy=E[0:n] # Copy energy values
        # Extract and order the potential values
        V_copy=V[0:steps,order]
        V_copy=V[0:steps,0:n]
        # Initialize step determination
        found_step = False
        step = 1
        # Find a suitable step value
        while found_step is False:
            if(E_copy[step]-E_copy[0]<0.2):
                step+=1
            else:
                found_step = True
        # Initialize scaling factors
        ScaleFactorStep=0.05
        ScaleFactor=1.00
        # Overlap check for scaling
        Overlap=1
        while(Overlap==1):
            for i in range(0,n,step):
                MaxV2=np.max(V_copy[0:steps,i])+E_copy[i]/ScaleFactor
                MinV2=np.min(V_copy[0:steps,i])+E_copy[i]/ScaleFactor
                MaxV1=np.max(V_copy[0:steps,i-step])+E_copy[i-step]/ScaleFactor
                 # Check for overlap conditions
                if((MaxV2-MinV2)<(np.abs(MinV2-MaxV1)*10)):
                    Overlap=1
                else:
                    Overlap=0
                    break
             # Adjust scaling factor
            ScaleFactor=ScaleFactor+ScaleFactorStep
        # Calculate new scaled potential and wave functions
        V_copy_new=(E_copy/ScaleFactor)+V_copy
        # Check for convergence based on the maximum value of the new scaled wave function
        if np.max(V_copy_new[n])>0:
            Converged=True
            n=n-1
        else:
            n=n+1
        # Store the final scaled wave functions and potential
        V_copy_old=V_copy_new
    # Finalize scaled wave functions and potential
    V_new=V_copy_old
    U_new=U/ScaleFactor
    # Return scaled values and parameters
    return V_new,ScaleFactor,U_new,n    
