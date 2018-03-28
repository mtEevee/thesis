# библиотеки
import pathlib
import csv

inputPath =  "/Users/roman/untitled/data_task/Segmented"
#inputPath = 'E:/Wavelet_analysis/Analyzer_export/'
outputPath = "/Users/roman/PycharmProjects/thesis/data.csv"
#outputPath = 'D:/Lisa/THESIS/DLproject/data.csv'

# вписывание данных в отдельный файл (таблицей)
with open(outputPath, 'w', newline="") as my_file:
    columns = ["person", "day", "type task", "answers old", "count task", "answers new", 
               "correct", "uncorrect", "bad intervals", "count bad"]
    writer = csv.DictWriter(my_file, fieldnames=columns)
    writer.writeheader()

# просим список файлов в папке и фильтруем его по расширению ()
    for vmrk_files in pathlib.Path(inputPath).glob('*wMarkers.vmrk'):

# теперь раобтаем с каждым файлом по порядку
        f = open(vmrk_files, 'r')  # открываем файл для чтения

        C = [] # будущий список ответов
        A = [] # бинарный список ответов
        B = [] # бинарный список багов
        time = -1999 #время сегментов
        time_bad = 1 #время багов
        pr_time_bad = time_bad
        count_bad = 0 #считает B.I. в файле
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
                
            new_seg = a.find("New Segment") # начало нового сегмента?
            if new_seg!=-1:  # если да, то...
                segments+=1 # счётчик количества сегментов, то есть заданий (в конкретном файле)
                seg_new = 1 # начался сегмент
                if segments==2 and len(B)==0:
                    B.append(False)
                time+=2000

            bad_seg = a.find("Bad Interval") # баг?
            if bad_seg!=-1: # если да, то...
                index_time_bad = a.find(",,") # ищем индекс запятых перед временем
                count_bad+=1
                pr_time_bad = int(time_bad)

                if time==-1999:
                    time_bad = 1
                elif time==1 or time+2000==2001:
                    time1 = a[index_time_bad + 2]
                    time2 = a[index_time_bad + 2:index_time_bad + 6]
                    if time2 == '2001':
                        time_bad = time2
                    elif time1 == '1':
                        time_bad = time1
                elif time<8001 and time+2000<=8001:
                    time_bad = a[index_time_bad+2:index_time_bad+6] # 4 цифры
                elif time==8001 and time+2000==10001:  # граница 8001 или 10001
                    time1 = a[index_time_bad+2:index_time_bad+6] # 4 цифры
                    time2 = a[index_time_bad+2:index_time_bad+7] # 5 цифр
                    if time1=='8001':
                        time_bad = time1
                    elif time2=='10001':
                        time_bad = time2
                elif time<98001 and time+2000<=98001:
                    time_bad = a[index_time_bad+2:index_time_bad+7] # 5 цифр
                elif time==98001 or time+2000==100001:
                    time1 = a[index_time_bad+2:index_time_bad+7] # 5 цифры
                    time2 = a[index_time_bad+2:index_time_bad+8] # 6 цифр
                    if time1=='98001':
                        time_bad = time1
                    elif time2=='100001':
                            time_bad = time2
                elif time<=980001:
                    time_bad = a[index_time_bad+2:index_time_bad+8] # 6 цифр

            if ((segments==1 and time_bad=='2001') or segments==2) and len(B)==0:
                B.append(False)

            if int(time_bad)==time:
                r = (time-pr_time_bad)//2000-1
            elif int(time_bad)==time+2000:
                r = (time-pr_time_bad)//2000
            while r>0:
                B.append(False)
                r-=1
            B.append(True)

            b = a.rfind("Stimulus,S ")  # стимул?
            if b!=-1:  # если да , то...
                b=b+14 # индекс цифры, кодирующий (не)ответ 
                if seg_new==1: # если это первый стимул после начала сегмента, то...
                    d = int(a[b])
                    C.append(d) # добавить в список вычлененную циферку
                    seg_new = 0 # не считывать дальше в сегменте Stimulus
                    if a[b]=='1':
                        A.append(1)
                        correct+=1
                    elif a[b]!='1':
                        A.append(0)
                        uncorrect+=1

            final = a.find("Marker User Infos") # конец документа?
            if final!=-1:
                r = (time-int(time_bad))//2000
                while r>0:
                    B.append(False)
                    r-=1

        row = {"person" : person, "day" : day, "type task" : type_f, "answers old" : C[0:len(C)], 
               "count task" : segments, "answers new" : A[0:len(A)], "correct" : correct, 
               "uncorrect" : uncorrect, "bad intervals" : B[0:len(B)], "count bad" : count_bad
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
#B[] # bad intervals
#count_bad # количество багов

import pandas as pd
table = pd.read_csv('data.csv')
print(table.head(10))