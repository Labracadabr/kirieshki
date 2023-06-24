import matplotlib.pyplot as plt

with open('add.txt', 'r', encoding='utf-8') as file:
    stats = [line.strip().split() for line in file.readlines() if line[0].isalpha()]

a = []
for i in stats:
    a.append(len(i))

print(a)

plt.bar(range(len(a)), a, color='purple')

plt.xlabel('Количество игр')
plt.ylabel('Названо городов')
plt.title('Игра в города')

plt.show()