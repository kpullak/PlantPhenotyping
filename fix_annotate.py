crs = open("annotate.txt", "r")

all_lines = []
for columns in ( raw.strip().split() for raw in crs ):
    all_lines.append(columns[0])

# initialization parameters
leaf_counter = 0
collar_counter = 0

x_diff_leaf = 0
y_diff_leaf = 0
x_diff_collar = 0
y_diff_collar = 0

for line in all_lines:
    image_name, x1, y1, x2, y2, annotation = line.split(',')
    if annotation == 'leaf':
        x_diff_leaf += abs(int(x2) - int(x1))
        y_diff_leaf += abs(int(y2) - int(y1))
        leaf_counter += 1
    elif annotation == 'collar':
        x_diff_collar += abs(int(x2) - int(x1))
        y_diff_collar += abs(int(y2) - int(y1))
        collar_counter += 1

print('leaf count is -', leaf_counter)
print('avg. leaf x diff is -' + str(x_diff_leaf/leaf_counter))
print('avg. leaf y diff is -' + str(y_diff_leaf/leaf_counter))

print('collar count is -', collar_counter)
print('avg. collar x diff is -' + str(x_diff_collar/collar_counter))
print('avg. collar y diff is -' + str(y_diff_collar/collar_counter))

avg_x_diff_leaf = int(abs(x_diff_leaf/leaf_counter))
avg_y_diff_leaf = int(abs(y_diff_leaf/leaf_counter))

avg_x_diff_collar = int(abs(x_diff_collar/collar_counter))
avg_y_diff_collar = int(abs(y_diff_collar/collar_counter))

avg_x_diff = max(avg_x_diff_leaf, avg_x_diff_collar)
avg_y_diff = max(avg_y_diff_leaf, avg_y_diff_collar)

new_stuff = []
for line in all_lines:

    image_name, x1, y1, x2, y2, annotation = line.split(',')
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    if annotation == 'leaf':
        if x1 < x2:
            x2 = x1 + avg_x_diff  # avg_x_diff_leaf
        elif x1 > x2:
            x2 = x1 - avg_x_diff  # avg_x_diff_leaf

        if y1 < y2:
            y2 = y1 + avg_y_diff  # avg_y_diff_leaf
        elif y1 > y2:
            y2 = y1 - avg_y_diff  # avg_y_diff_leaf

    elif annotation == 'collar':
        if x1 < x2:
            x2 = x1 + avg_x_diff  # avg_x_diff_collar
        elif x1 > x2:
            x2 = x1 - avg_x_diff  # avg_x_diff_collar

        if y1 < y2:
            y2 = y1 + avg_y_diff  # avg_y_diff_collar
        elif y1 > y2:
            y2 = y1 - avg_y_diff  # avg_y_diff_collar
    new_item = [image_name, str(x1), str(y1), str(x2), str(y2), annotation]
    new_item = ','.join(new_item)
    new_stuff.append(new_item)

print(avg_x_diff_leaf, avg_y_diff_leaf, avg_x_diff_collar, avg_y_diff_collar)
print(avg_x_diff, avg_y_diff)

with open('annotate_max_window.txt', 'w') as f:
    for item in new_stuff:
        f.write("%s\n" % item)
