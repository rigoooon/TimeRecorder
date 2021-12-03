from datetime import datetime
from time import time
from pathlib import Path
from tkinter import Tk
import tkinter as tk
import time_recorder
import tkinter.simpledialog as sg
import tkinter.messagebox as mx

root = Tk()
root.withdraw()

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()
        
        #設定
        master.geometry("300x310")
        master.title("TIMER")
        master.config(bg="white")
        
        #初期化
        self.startTime = time()
        self.stopTime = 0.0
        self.elapsedTime = 0.0
        self.playTime = False
        
        #ここはストップウォッチの数字が表示されてるところの部分を描画するための処理
        self.canvas = tk.Canvas(master, width=300, height=80, bg="white")
        self.canvas.place(x=3, y=10)
        
        #ボタンを作る処理
        tk.Button(master, text="Start", command=self.startButtonClick,width=31, height=2).place(x=10, y=110)
        tk.Button(master, text="Stop", command=self.stopButtonClick,width=31, height=2).place(x=10, y=160)
        tk.Button(master, text="Reset", command=self.resetButtonClick,width=14, height=2).place(x=10, y=210)
        tk.Button(master, text="Record", command=self.recordButtonClick,width=14, height=2).place(x=160, y=210)
        tk.Button(master, text="Manual Input", command=self.manualButtonClick, width=31, height=2).place(x=10, y=260)

        #update関数を実行
        master.after(50, self.update)

    #ストップウォッチを開始する関数
    def startButtonClick(self):
        if not self.playTime:
            self.startTime = time() - self.elapsedTime
            self.playTime = True
        
    #ストップウォッチの時間を一時停止する関数
    def stopButtonClick(self):
        if self.playTime:
            self.stopTime = time() - self.startTime
            self.playTime = False

    #時間をリセットする関数
    def resetButtonClick(self):
        self.startTime = time()
        self.stopTime = 0.0
        self.elapsedTime = 0.0
        self.playTime = False
    
    #recordボタンを押すとcsvファイルに記録。同時にその月の合計時間を更新。
    def recordButtonClick(self):
        self.start_time = datetime.now()
        #パスとディレクトリの作成
        path = f'./data/{self.start_time.year}/'
        Path(path).mkdir(parents=True, exist_ok=True)
        Path(f'{path}time_record.csv').touch()
        #csvファイルに時間を記録
        with open(f'{path}time_record.csv', 'a', encoding='utf-8') as f:
            f.write(f'{self.start_time:%Y/%m/%d,%H:%M:%S},{round(self.stopTime)}\n')
        #初期化
        self.startTime = time()
        self.stopTime = 0.0
        self.elapsedTime = 0.0
        self.playTime = False

    #時間を手動入力する関数
    def manualButtonClick(self):
        #ボタンを押した時の時間を取得
        self.start_time = datetime.now()
        #パスとディレクトリを作成
        path = f'./data/{self.start_time.year}/'
        Path(path).mkdir(parents=True, exist_ok=True)
        #時間を入力する
        hour = sg.askstring('時間を記録', '時間を入力してください。')
        minute = sg.askstring('時間を記録', '分を入力してください。')
        mx.showinfo('時間を記録', '記録しました。')
        hour = int(hour) * 3600
        minute = int(minute) * 60
        total = hour + minute
        #ファイルに書き込む
        with open(f'{path}time_record.csv', 'a', encoding='utf-8') as f:
            f.write(f'{self.start_time:%Y/%m/%d,%H:%M:%S},{total}\n')


    #無限ループ
    #常に関数が実行され、値が更新され続けている状態
    #スタートボタンが押されて時間が進んでいる間はTrue
    def update(self):
        self.canvas.delete("Time")
        
        if self.playTime:#Trueのときはここが実行される
            #ここのself.startTimeはスタートボタンを押したときの時刻が入っている。
            self.elapsedTime = time() - self.startTime#elapsedtimeが更新され続けるからリアルタイムで表示される数値も変わり続ける
            if self.elapsedTime >= 60:
                self.displayTime = time_recorder.dmod(self.elapsedTime)
                self.canvas.create_text(280, 40, text=f'{self.displayTime}', 
                                        font=("Helvetica", 20, "bold"), fill="black", tag="Time", anchor="e")
            else:
                self.canvas.create_text(280, 40, text=f'0h0m{round(self.elapsedTime)}s', 
                                        font=("Helvetica", 20, "bold"), fill="black", tag="Time", anchor="e")
        else:#Falseのときはここ
            if int(self.stopTime) >= 60:
                self.displayTime = time_recorder.dmod(self.stopTime)#ここでself.stopTimeの値がstrになっているからエラー
                self.canvas.create_text(280, 40, text=f'{self.displayTime}', 
                                        font=("Helvetica", 20, "bold"), fill="black", tag="Time", anchor="e")
            else:
                self.canvas.create_text(280, 40, text=f'0h0m{round(self.stopTime)}s', 
                                        font=("Helvetica", 20, "bold"), fill="black", tag="Time", anchor="e")
        self.master.after(50,self.update)#50ミリ秒後にupdate関数実行

def main():
    win = tk.Tk()
    #win.resizable(width=False, height=False) #ウィンドウを固定サイズに
    app = Application(master=win)
    app.mainloop()

if __name__ == "__main__":
    main()
