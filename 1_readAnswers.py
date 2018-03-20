# библиотеки
import pathlib
import csv

#count_answer = 0   # подсчёт количества списков ответов (должно совпадать с количеством нужных файлов из папки)

# вписывание данных в отдельный файл (таблицей)
with open('/Users/roman/untitled/data_task/data.csv', 'w', newline="") as my_file:
    columns = ["person", "day", "type task", "answers old", "count task", "answers new", 
               "correct", "uncorrect", "bad intervals", "bad 1", "bad 0", "sum bad"]
    writer = csv.DictWriter(my_file, fieldnames=columns)
    writer.writeheader()
# путь к папке, откуда будем брать файлы '/Users/roman/untitled/data_task'
# просим список файлов в папке и фильтруем его по расширению ()
    for vmrk_files in pathlib.Path('/Users/roman/untitled/data_task/Segmented').glob('*vmrk'):

# теперь раобтаем с каждым файлом по порядку
        f = open(vmrk_files, 'r')  # открываем файл для чтения

#n_row = sum(1 for l in open(vmrk_files, 'r')) # считаем количество строк в файле
#print(n_row)

        C = [] # будущий список ответов
        A = [] # бинарный список ответов
        #B = [] # бинарный список багов?
        #bad1 = 0
        #bad0 = 0
        #time = 1
        #r = 0
        segments = 0 # счётчик количества заданий (New Segment)
        seg_new = 0 # переменная для обозначения начала (1) / конца (0) сегмента
        correct = 0 # счётчик правильных ответов
        uncorrect = 0 # счётчик неправильный ответов / нет ответов

# работаем построчно
        for line in f:
            a = line  # вычленяем строку
            dl = len(line) # длина строки 
        
            name = a.find("DataFile=") # эта строчка с инф-ой про имя файла?
            if name!=-1: # если это имя файла, то...
                index_type = a.find("Mult") # индекс типа задания (Mult)
                index_p = a.find("_d")
            
                if index_type!=-1: # если это Mult, то...
                    type_f = a[index_type:index_type+4] # тип задания
                    day = a[index_type-4] #  день (1-ый или 5-ый)
            # нахождение номера респондента
                    if dl==38 or dl==43:  # однозначный номер (1 - 9)
                        person = a[index_p-1]
                    elif dl==39 or dl==45:   # двузначный номер (10 - 99)
                        person = a[index_p-2:index_p]
                    elif dl==46: # выброс
                        person = a[index_p-2:index_p]
                else:  # если это Subtr, то...
                    index_type = a.find("Subtr") # индекс типа задания (Subtr)
                    type_f = a[index_type:index_type+5] # тип задания
                    day = a[index_type-4]  # день (1-ый или 5-ый)
            # нахождение номера респондента
                    if dl==39 or dl==45:  # однозначный день (1 - 9)
                        person = a[index_p-1]
                    elif dl==40 or dl==46:   # двузначный день (10 - 99)
                        person = a[index_p-2:index_p]
                    elif dl==47: # выброс
                        person = a[index_p-2:index_p]  
                
           # bad_seg = a.find("Bad Interval") # баг?
            #if bad_seg!=-1: # если да, то ...
             #   bad1+=1 # +1 к багам
              #  count_bad+=1 # помощник в упоминании багов
                
            new_seg = a.find("New Segment") # начало нового сегмента?
            if new_seg!=-1:  # если да, то...
                segments+=1 # счётчик количества сегментов, то есть заданий (в конкретном файле)
                seg_new = 1 # начался сегмент
             #   if segments>1 and count_bad==0: # если сегментов больше одного, а багов не было, то..
              #      B.append('0')  # указать 0
               #     bad0+=1        # +1 к отсутсвию багов
                #elif count_bad!=0 and segments>1:
                 #   B.append('1')  # указать 1
                  #  count_bad-=1   # вычесть у помощника упоминание бага

        #    if a.find("Marker User Infos")!=-1 and count_bad==1:
         #       B.append('1')
          #      bad1+=1
           #     count_bad-=1
            #elif a.find("Marker User Infos")!=-1 and count_bad==0:
             #   B.append('0')
              #  bad0+=1
               # count_bad-=1
            
            b = a.rfind("Stimulus,S ")  # стимул?
            if b!=-1:  # если да , то...
                b=b+14 # индекс цифры, кодирующий (не)ответ 
                if seg_new==1: # если это первый стимул после начала сегмента, то...
                    C.append(a[b]) # добавить в список вычлененную циферку
                    seg_new = 0 # не считывать дальше в сегменте Stimulus
                    if a[b]=='1':
                        A.append('1')
                        correct+=1
                    elif a[b]!='1':
                        A.append('0')
                        uncorrect+=1
        
        row = {"person" : person, "day" : day, "type task" : type_f, "answers old" : C[0:len(C)], 
               "count task" : segments, "answers new" : A[0:len(A)], "correct" : correct, 
               "uncorrect" : uncorrect, #"bad intervals" : B[0:len(B)], "bad 1": bad1, 
              # "bad 0" : bad0, "?" : len(B) 
              }
        writer.writerow(row)


# ЧТО ЗАПИСЫВАЕТСЯ
#person # номер респондента
#day # день проверки (1-ый или 5-ый)
#type_f # тип задания
#C[] # список ответов (1 - correct / 2 - not / 3 - no answer)
#segments # количество заданий
#A[] # бинарный список ответов (1 - correct / 0 - not or no)
#correct # правильные ответы
#uncorrect # неправильные ответы или отсутствие ответа
