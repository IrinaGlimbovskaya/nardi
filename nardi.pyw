import PySimpleGUI as sg
from random import randint
#окно победы
def win(points):
    print(points)
    layout = [[sg.Text('Поздравляем с победой', size=(20,2))],
                   [sg.Image('pobeda.png')],
              [sg.Text('Ваши очки', size=(10,2)),sg.Input(size = (5,1), k = 'point')],
              [sg.Button('Новая игра'),sg.Button('Выйти из игры')]
                  ]
    
    window = sg.Window('Победа', layout, finalize=True)
    window['point'].update(points)
    #обработка событий
    while True:             
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Новая игра':
            window.close()
            open_window()
        if event == 'Выйти из игры':
            window.close()
            
canvas_width = 1175 #ширина канвы
canvas_height = 580 #высота канвы

ch_images = [ 'ch_black.png','ch_white.png']  #список из картинок шашек
ch_size = 74 #размер клетки

#координаты левого верхнего узла сетки
x_beg = 45
y_beg = 49
#функция окна игры
def open_window():
    #класс шашки
    class Cheker:
        def __init__(self, x, y, val):
            self.x = x
            self.y = y
            self.val = val
            self.id = graph.draw_image(filename= ch_images[val], location =(self.x, self.y))

        def move(self, x, y):#функция перемещения шашки
            self.x = x
            self.y = y
            graph.relocate_figure(self.id, self.x , self.y)
            
        
    sg.theme('BlueMono')
    layout = [[sg.Graph(
                canvas_size=(canvas_width, canvas_height),
                graph_bottom_left=(0, canvas_height),
                graph_top_right=(canvas_width, 0),
                background_color="Sienna",
                key="graph"
            )],[sg.Text('состояние: '),sg.Input(size = (18,1), k = 'состояние')],
               [sg.Button('Начать'),  sg.Button('Походить'), sg.Button('Передать ход'), sg.Button('Новая игра')],                
               [sg.Text('Белые шашки: ', size=(12,1)),  sg.Input(size = (5,1), k = 'cube1'),sg.Input(size = (5,1), k = 'cube2')],
               [sg.Text('Черные шашки : ', size=(13,1)), sg.Input(size = (5,1),k = 'cube3'), sg.Input(size = (5,1), k = 'cube4')],
            
        ]

    window = sg.Window("Игра нарды", layout, location=(0,0), finalize=True, return_keyboard_events=True)

    graph = window['graph']
    graph.draw_image(filename="orig.PNG", location=(0,0))
    graph.bind('<Button-3>', 'right_click')
    graph.bind('<Button-1>', 'left_click')

    window['состояние'].update("начало")#первоначальное состояние игры

    #положение шашек на доске
    ls_b_bar = [ Cheker(130, 500 -y*1, 0) for y in range (2)] #

    ls_w_bar = [ Cheker(1010, y*1+50, 1) for y in range (15)]#

    dc_chekers={cheker.id:cheker for cheker in ls_b_bar + ls_w_bar} #словарь всех шашек

    dc_w_chekers={cheker.id:cheker for cheker in ls_w_bar} #словарь белых шашек
    dc_b_chekers={cheker.id:cheker for cheker in ls_b_bar} #словарь черных шашек

    cheker_id = 0
    ls_states = ["начало","ход белых","ход черных"] #состояния для кнопок
    state = "начало"

    #####################  сетка для ходов шашек
    '''
    for x in range(44,canvas_width,74): 
        graph.draw_line((x,0),(x,canvas_height), "yellow")
    for y in range(50,canvas_height,74):
        graph.draw_line((0,y),(canvas_width,y), "yellow")    
    '''
    #обработка событий
    while True:
        event, values = window.read()
        print ('event: ', event, ', values: ', values)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        #обработка кубика
        if event == 'Начать': 
            rand1 = randint(1, 6)
            window['cube1'].update(rand1)
            rand3 = randint(1, 6)
            window['cube3'].update(rand3)
            if rand1>rand3:
                window['состояние'].update("ход белых")
            elif rand1<rand3:
                window['состояние'].update("ход черных")
        #--- Обработка кнопки походить
        if event == 'Походить':
            if values['состояние']== "ход белых" :
                rand1 = randint(1, 6)
                window['cube1'].update(rand1)
                rand2 = randint(1, 6)
                window['cube2'].update(rand2)
                window['cube3'].update(0)
                window['cube4'].update(0)

            elif values['состояние']== "ход черных":
                rand3 = randint(1, 6)
                window['cube3'].update(rand3)
                rand4 = randint(1, 6)
                window['cube4'].update(rand4)
                window['cube1'].update(0)
                window['cube2'].update(0)
        #---Обработка кнопки Новая игра       
        if event == 'Новая игра':
            window.close()
            open_window()
        #обработка левой клавиши мыши        
        if event == 'graphleft_click':    
            if cheker_id:
                cheker = dc_chekers[cheker_id]
                x,y = values['graph'] #получения координат определенной шашки

                #уточнение позиции
                x = x_beg + ((x-x_beg)//ch_size)*ch_size +7
                y = y_beg + ((y-y_beg)//ch_size)*ch_size+7

                #условие удаления шашки(выходим за пределы поля)
                if (x<x_beg+ch_size) and cheker.val == 0:
                    del dc_b_chekers[cheker_id]
                    del dc_chekers[cheker_id]
                    graph.delete_figure(cheker_id)
                    del cheker
                     
                elif (x>x_beg+ch_size*13) and cheker.val == 1:
                    del dc_w_chekers[cheker_id]
                    del dc_chekers[cheker_id]
                    graph.delete_figure(cheker_id)
                    del cheker
                else:
                    cheker.move(x,y)
                cheker_id=0
                
            #условие победы              
            if  len( dc_b_chekers) < 1:
                b = len (dc_w_chekers)
                points = b * 10
                print (points)
                window.close()
                win(points)
                  
            if  len( dc_w_chekers) < 1:
                w = len (dc_b_chekers)
                points = w * 10
                print (points)
                window.close()
                win(points)
        #обработка правой клавиши мыши    
        if event == 'graphright_click':     
            x,y = values['graph']
            figs = graph.get_figures_at_location((x,y)) #получить шашку по координатам
            cheker_id = figs[-1] if len(figs)>1 else 0 
            print(cheker_id)
            if cheker_id != 0: # блокировка действий соперника
                cheker = dc_chekers[cheker_id]
                if cheker.val == 1 and values['состояние']== "ход черных":
                    cheker_id = 0
                if cheker.val == 0 and values['состояние']== "ход белых":
                    cheker_id = 0
        #---Обработка кнопки Передачи хода    
        if event == 'Передать ход':  
            if values['состояние']== "ход белых":
                window['состояние'].update("ход черных")
            elif values['состояние']== "ход черных":
                window['состояние'].update("ход белых")
            cheker_id = 0
#окно меню
def main():
    #переменная для правил игры
    about = '''Играют двое. Доска делится на две половины (левую и правую). У каждого игрока на доске по 15 шашек, которые расставляются на своей части доски вдоль правой стороны. Наборы шашек у игроков разного, обычно чёрного и белого цвета. Количество зар (кубиков) — 2. Игроки выбрасывают зары по очереди. Каждый игрок имеет право передвигать шашки только своего цвета.
Начальное расположение шашек на доске (позиция 12 и 24) называется «голова». Ход с этого положения называется «ход с головы». За один ход с головы можно взять только одну шашку (кроме первого броска).
Право первого хода, и соответственно белого цвета шашек, разыгрывается так: каждый игрок кидает один зар. Право первого хода и белый цвет шашек получает тот, у кого выпало большее количество очков. При одинаковом количестве выпавших очков бросок повторяется. Если игра состоит из нескольких конов, то цвет шашек меняется, и следующий кон начинает игрок, игравший предыдущий кон чёрным цветом.
Ход игрока — это бросок зар и последующее движение шашек после броска. Зары следует бросать из специального кожаного стаканчика. Бросать необходимо так, чтобы зары упали на одну половину доски и устойчиво легли на плоскость доски. Зары должны оставаться в том положении, в котором упали на доску, до завершения хода. Если зары упали на разные половины доски, или за её пределами, или остановились в неустойчивом положении (например, кубик «встал на ребро», опираясь на бортик доски или шашку), производится повторный бросок.
После броска игрок обязан передвинуть две свои шашки против часовой стрелки на столько лунок, сколько очков выпало на каждой из костей. Вместо ходов двумя разными шашками игрок может сделать два хода одной шашкой. Если на зарах выпало одинаковое количество очков (так называемый «дубль»), то бросок удваивается, то есть игрок должен сделать четыре движения шашками. Запрещено делать ход, в результате которого шашка встаёт на поле, занятое шашкой противника. Ходить надо строго на то число очков, которое выпало на зарах. Если ход на выпавшее количество очков невозможен, эти очки «сгорают», но если возможность хода имеется, то игрок обязан, даже в ущерб себе, использовать все выпавшие очки. Если есть два хода, один из которых использует одну кость, а другой — две, игрок обязан сделать ход, использующий обе кости (т. н. «правило полного хода»).'''

    layout = [ [sg.Text('Игра Нарды', size=(10,1))],
               [sg.Button('Начать игру')],
               [sg.Button('Правила игры')],
               [sg.Button('Выйти')]
               
            ]
    window = sg.Window('Игра Нарды', layout)
    while True:             
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Начать игру':
            window.close()
            open_window()
        if event == 'Правила игры':
            window.close()
            sg.popup_scrolled(about, size=(80, None))
        if event == 'Выйти':
            window.close()
            
    window.close()
    
if __name__ == "__main__":
    main()

