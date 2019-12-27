from Simulate import Simulation
import matplotlib.pyplot as plt
import numpy as np
import csv


'''
function to make the csv data file
Parameters: the output data
'''


def write_output_file(data):
    with open('output.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)
    writeFile.close()


'''
function the write the Another file for the rest of the data
Parameter: The period for the planets and the satalite meeting point
'''


def write_orbital_file(period, satalite_metting):
    peri = np.around(period, 2)
    sat = round(satalite_metting, 2)
    file1 = open("The_Orbital_period_and_satalite_intersection.txt", "w")
    file1.write("Orbital Period[Earth Years]:\n")
    file1.write("Mercury: "+str(peri[1]) + ","+"Venus: "+str(peri[2]) +
                ","+"Earth: "+str(peri[3]) + ","+"Mars: "+str(peri[4]) + "\n\n")
    file1.write("Satalite reaching mars[Earth Years]: \n"+str(sat) + "\n")
    file1.write("Satalite reaching mars[Days]: \n"+str(round(sat*365)))
    file1.close()


'''
A function to display the output
Parameters: The period for the planets and the satalite meeting point
'''


def printOut(periods, satalite_meeting):
    peri = np.around(periods, 2)
    print("Orbital Period[Earth Years]")
    sat = round(satalite_meeting, 2)
    print("Mercury: "+str(peri[1]) + ","+"Venus: "+str(peri[2]) +
          ","+"Earth: "+str(peri[3]) + ","+"Mars: "+str(peri[4]) + "\n")
    print("Satalite reaching Mars[Earth Years]: \n"+str((sat)))
    print("Satalite reaching Mars[Days]: \n"+str(round(sat*365)))


'''
Shows the unscaled graph
'''


def show_unscaled(plot):
    plt.title("TOTAL ENERGY V TIME\n(Unscaled)")
    plt.plot(plot[0], plot[1])
    plt.xlabel('Time(s)')
    plt.ylabel('Total Energy (J)')
    plt.show()


'''
Shows the scaled graph 
'''


def show_scaled(plot):
    plt.title("TOTAL ENERGY V TIME\n(Scaled)")
    plt.ylim(-7.0e33, 7.0e33)
    plt.plot(plot[0], plot[1])
    plt.xlabel('Time(s)')
    plt.ylabel('Total Energy (J)')
    plt.show()


'''
 The main function 
'''


def main():
    sim = Simulation()
    sim.run()
    printOut(sim.period/sim.period[3], sim.satalite_meeting/sim.period[3])
    write_orbital_file(
        sim.period/sim.period[3], sim.satalite_meeting/sim.period[3])
    tot_eng = np.array(sim.total_energy)
    plot = list(map(list, zip(*tot_eng)))
    data = [['Time(s)', 'Total Energy(J)']]+list(tot_eng)
    write_output_file(data)
    show_unscaled(plot)
    show_scaled(plot)


if __name__ == "__main__":
    main()
