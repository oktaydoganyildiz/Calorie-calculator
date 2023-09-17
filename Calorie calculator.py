from Tkinter import*
import ttk
import csv
import re

class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.label_title = Label(self, text='Sehir Cafeteria', font=('', '15', 'italic'), background='blue',foreground='red', height=5, width=70)
        self.label_title.grid(row=0, column=0, columnspan=5)

        self.label_path = Label(self, text="File path:").grid(row=1, column=0)
        self.file = StringVar(self, value='FoodDB.csv')
        self.entry_path = Entry(self, textvariable=self.file)
        self.entry_path.grid(row=1, column=1, columnspan=4,sticky=E + W)
        self.label_diet = Label(self, text="Choose your diet:").grid(row=2, column=0)
        self.diet = IntVar()
        self.Radio_diet_1 = ttk.Radiobutton(self, text="1300 kcal", value=1300, variable=self.diet)
        self.Radio_diet_1.grid(row=2, column=1)
        self.Radio_diet_2 = ttk.Radiobutton(self, text="1800 kcal", value=1800, variable=self.diet)
        self.Radio_diet_2.grid(row=2, column=2)
        self.Radio_diet_3 = ttk.Radiobutton(self, text="2300 kcal", value=2300, variable=self.diet)
        self.Radio_diet_3.grid(row=2, column=3)

        self.label_choice = Label(self)
        self.label_choice_2 = Label(self)

        self.button_continue = Button(self, text="Continue",bg="red", command=self.button_expand)
        self.button_continue.grid(row=4)

        self.label_menu_title = Label(self, text='Choose Your Food')
        self.label_menu = Label(self, text="Food Menu")
        self.label_food = Label(self, text="My Food")

        self.list_menu = Listbox(self, width = 30)
        self.list_food = Listbox(self, width = 30)

        self.button_add = Button(self, text='Add Food', bg='red', command = Files().add_food)
        self.button_remove = Button(self, text='Remove Food', bg='red', command = Files().remove_food)

        self.button_continue_2 = Button(self, text='Continue', bg='red', command=self.button_expand_2)

        self.label_summary_title = Label(self, text='Summary and Data Saving')
        self.label_diet_2 = Label(self, text="Choose your diet:")

        self.label_result = Label(self)

        self.label_file_type = Label(self, text='Choose File Type')
        self.file_type = StringVar()
        self.radio_text = ttk.Radiobutton(self, text='Txt File', variable=self.file_type, value='txt')
        self.radio_csv = ttk.Radiobutton(self, text='CSV File', variable=self.file_type, value='csv')
        self.button_save = Button(self, text='Save File', bg='red', command=Files().save_file)

        self.grid()

    def button_expand(self):  # This function is  related to continue button, it expands program with widgets
        self.label_choice.grid(row=3)
        self.label_choice['text'] = "Your Diet Choice is %s kcal" %self.diet.get()
        self.label_menu_title.grid(row=5,column=0, columnspan=5)
        self.label_menu.grid(row=6, column=0)
        self.label_food.grid(row=6, column=3)
        self.list_menu.grid(row=7, rowspan=4, column=0)
        self.list_food.grid(row=7, rowspan=4, column=3)
        self.button_add.grid(row=9, column=1, columnspan=2)
        self.button_remove.grid(row=10, column=1, columnspan=2)
        self.button_continue_2.grid(row=11, column=0)
        Files().food_list()

    def button_expand_2(self):  # This function is third part of the program.
        self.label_summary_title.grid(row=12, column=0, columnspan=5)
        self.label_choice_2.grid(row=13)
        self.label_choice_2['text'] = "Your choice Diet Choice is %s kcal" % self.diet.get()
        self.label_result.grid(row=14, column=0, columnspan=4, sticky=W)
        self.label_file_type.grid(row=15, column=0)
        self.radio_text.grid(row=15, column=1)
        self.radio_csv.grid(row=15, column=2)
        self.button_save.grid(row=15, column=3)
        Files().check_calories()


class Files:
    def __init__(self):
        pass

    def food_list(self):  # it reads the input file from the directory and puts the each item to the list box for menu
        with open(app.file.get()) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            app.list_menu.insert(END, 'Choice - Price - Calorie')
            for row in reader:
                app.list_menu.insert(END, '%s, %sTL, %s kcal' % (row[1], row[2], row[0]))

    def add_food(self):  # it copies the selected item from menu to food list
        if app.list_menu.curselection()[0] == 0:
            raise Exception('That is not valid')
        else:
            app.list_food.insert(END, app.list_menu.get(app.list_menu.curselection()))

    def remove_food(self):  # it removes the selected item from food list
        app.list_food.delete(app.list_food.curselection())
        #app.list_food.delete

    def calculate_calories(self):  # it reads the items in the food list and sums the calories.
        sum = 0
        for i in app.list_food.get(0, END):
            sum += int(re.search(r'\d+', i.split(',')[-1]).group())
        return sum

    def check_calories(self):  # it compares the results with the selected calorie limit
        if self.calculate_calories() <= app.diet.get():
            app.label_result['text'] = 'Your Chosen Food Menu - Amount of Calories: %s kcal' % self.calculate_calories()
            app.label_result['bg'] = 'green'
        else:
            app.label_result['text'] = 'Your Chosen Food Menu - Amount of Calories: %s kcal Above Daily Limit' % self.calculate_calories()
            app.label_result['bg'] = 'red'

    def save_file(self): # it saves the file by th selected file type
        if app.file_type.get() == 'txt':
            file = open('My_Food_Choices.txt', 'w')
            for i in app.list_food.get(0, END):
                file.write('You ordered %s Price: %s Calories: %s \n' % (i.split(',')[1], i.split()[2], i.split()[0]))
            file.write('---------------\n')
            file.write('Total Calories: %s' % self.calculate_calories())
            file.close()
        else:
            with open('My_Food_Choices.csv','wb') as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow(['Your Order', 'Price','Calories', 'Total Calories'])
                for i in app.list_food.get(0, END):
                    filewriter.writerow([i.split(',')[0].encode('utf-8'), i.split()[1], i.split()[2]])
def main():
    global app
    root = Tk()
    root.title('Cafeteria')
    root.geometry()
    app = GUI(root)
    root.mainloop()
main()