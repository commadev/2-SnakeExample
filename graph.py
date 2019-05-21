import matplotlib.pyplot as plt

# Sample Line
# Generation : 1 - best_genome = [80, [9.5389, 8.8227, 9.1025, 9.9596], [0.8428, 0.2431, 0.2528, 0.8441, 0.1945, 0.3988]], avg_fitness = 19.5

x = []
y = []

read_file = open("result.txt", 'r')
read_list = read_file.readlines()
generation = 1
full_generation = len(read_list)

for line in read_list:
    print("Proceccing..." + str((generation/full_generation)*100) + "%")
    temp = line.split("avg_fitness =")
    avg_fitness = float(temp[1])

    x += [generation,]
    y += [avg_fitness,]
    generation += 1

plt.plot(x,y)
plt.show()
