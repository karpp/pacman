window_width = 580
window_height = 480
number_of_squares = 29  # количество клеточек на стороне поля
map_x = 0  # координаты начала поля
map_y = 0
square = 0  # сторона одной клетки поля
current_speed = 3  # Почему она объявляется здесь?
walls_on_map = [['' for _ in range(number_of_squares)] for _ in range(number_of_squares)]
# массив отображающий карту./- стена, & - проход без еды. еще есть 2 вида еды: обычная food и energizer
level = 4
maps_list = ['sample1.map', 'sample2.map', 'sample3.map']
energizer_time = 7
recordes_list = ['Recordes1.pac', 'Recordes2.pac', 'Recordes3.pac']
