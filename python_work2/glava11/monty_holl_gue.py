import random
import tkinter as tk
class Game(tk.Frame):
    doors = ['a', 'b', 'c']
    def __init__(self, parent):
        super(Game, self).__init__(parent)
        self.parent = parent
        self.img_file = 'all_closed.png'
        self.choice = ''
        self.winner = ''
        self.reveal = ''
        self.first_choice_win = 0
        self.pick_change_win = 0
        self.create_widgets()
    def create_widgets(self):
        img = tk.PhotoImage(file='all_closed.png')
        self.photo_lbl = tk.Label(self.parent, image=img, text='', borderwidth=0)
        self.photo_lbl.grid(row=0, column=0, columnspan=10, sticky='W')
        self.photo_lbl.image = img
        instr_input = [
            ('За одной дверью НАЛИЧНЫЕ!', 1, 0, 5, 'W'),
            ('Позади остальных: КОЗЫ!!!', 2, 0, 5, 'W'),
            ('Выбери дверь:', 1, 3, 1, 'E')
            ]
        for text, row, column, columnspan, sticky in instr_input:
            instr_lbl = tk.Label(self.parent, text=text)
            instr_lbl.grid(row=row, column=column, columnspan=columnspan, sticky=sticky, ipadx=30)
        self.door_choice = tk.StringVar()
        self.door_choice.set(None)
        a = tk.Radiobutton(self.parent, text='A', variable=self.door_choice, value='a', command=self.win_reveal)
        b = tk.Radiobutton(self.parent, text='B', variable=self.door_choice, value='b', command=self.win_reveal)
        c = tk.Radiobutton(self.parent, text='C', variable=self.door_choice, value='c', command=self.win_reveal)
        self.change_door = tk.StringVar()
        self.change_door.set(None)
        instr_lbl = tk.Label(self.parent, text='Сменить двери?')
        instr_lbl.grid(row=2, column=3, columnspan=1, sticky='E')
        self.yes = tk.Radiobutton(self.parent, state='disabled', text='Y', variable=self.change_door, value='y', command=self.show_final)
        self.no = tk.Radiobutton(self.parent, state='disabled', text='N', variable=self.change_door, value='n', command=self.show_final)
        defaultbg = self.parent.cget('bg')
        self.unchanged_wins_txt = tk.Text(self.parent, width=20, height=1, wrap=tk.WORD, bg=defaultbg, fg='black', borderwidth=0)
        self.changed_wins_txt = tk.Text(self.parent, width=20, height=1, wrap=tk.WORD, bg=defaultbg, fg='black', borderwidth=0)
        a.grid(row=1, column=4, sticky='W', padx=20)
        b.grid(row=1, column=4, sticky='N', padx=20)
        c.grid(row=1, column=4, sticky='E', padx=20)
        self.yes.grid(row=2, column=4, sticky='W', padx=20)
        self.no.grid(row=2, column=4, sticky='N', padx=20)
        self.unchanged_wins_txt.grid(row=1, column=5, columnspan=5)
        self.changed_wins_txt.grid(row=2, column=5, columnspan=5)
    def update_image(self):
        img = tk.PhotoImage(file=self.img_file)
        self.photo_lbl.configure(image=img)
        self.photo_lbl.image = img
    def win_reveal(self):
        door_list = list(self.doors)
        self.choice = self.door_choice.get()
        self.winner = random.choice(door_list)
        door_list.remove(self.winner)
        if self.choice in door_list:
            door_list.remove(self.choice)
            self.reveal = door_list[0]
        else:
            self.reveal = random.choice(door_list)
        self.img_file = ('reveal_{}.png'.format(self.reveal))
        self.update_image()
        self.yes.config(state='normal')
        self.no.config(state='normal')
        self.change_door.set(None)
        self.img_file = 'all_closed.png'
        self.parent.after(2000, self.update_image)
    def show_final(self):
        door_list = list(self.doors)
        switch_doors = self.change_door.get()
        if switch_doors == 'y':
            door_list.remove(self.choice)
            door_list.remove(self.reveal)
            new_pick = door_list[0]
            if new_pick == self.winner:
                self.img_file = 'money_{}.png'.format(new_pick)
                self.pick_change_win += 1
            else:
                self.img_file = 'goat_{}.png'.format(new_pick)
                self.first_choice_win += 1
        elif switch_doors == 'n':
            if self.choice == self.winner:
                self.img_file = 'money_{}.png'.format(self.choice)
                self.first_choice_win += 1
            else:
                self.img_file = 'goat_{}.png'.format(self.choice)
                self.pick_change_win += 1
        self.update_image()
        self.unchanged_wins_txt.delete(1.0, 'end')
        self.unchanged_wins_txt.insert(1.0, 'Неизменные выигрыши = {:d}'.format(self.first_choice_win))
        self.changed_wins_txt.delete(1.0, 'end')
        self.changed_wins_txt.insert(1.0, 'Измененные победы = {:d}'.format(self.pick_change_win))
        self.yes.config(state='disabled')
        self.no.config(state='disabled')
        self.door_choice.set(None)
        self.img_file = 'all_closed.png'
        self.parent.after(2000, self.update_image)  
root = tk.Tk()
root.title('Задача Монти Холла')
root.geometry('1280x820')
game = Game(root)
root.mainloop
game()