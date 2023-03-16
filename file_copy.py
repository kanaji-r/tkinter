import tkinter
from tkinter import ttk
import os
from PIL import Image
import shutil
import re


class Application(tkinter.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=750, height=600, borderwidth=4, relief='groove')
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        # ラジオボタン
        self.var_radio = tkinter.StringVar(value="A")
        self.radio_btn1 = tkinter.Radiobutton(self,text='リゲット',value="A",variable=self.var_radio,font=('',12,))
        self.radio_btn2 = tkinter.Radiobutton(self,text='Lステップ',value="B",variable=self.var_radio,font=('',12))
        self.radio_btn1.pack()
        self.radio_btn2.pack(padx=[13,0])
        #         # 実行ボタン
        # submit_btn2 = tkinter.Button(self)
        # submit_btn2['text'] = 'test'
        # submit_btn2['command'] = self.me
        # # submit_btn['command'] = self.input_num
        # submit_btn2.pack()
        # # メッセージ出力
        # self.message2 = tkinter.Message(self)
        # self.message2['width'] = 200
        # self.message2.pack()

        # テキストボックス
        self.text_box = tkinter.Text(self,font=('',13))
        self.text_box['width'] = 50
        self.text_box.pack(pady=20)
        # 実行ボタン
        submit_btn = tkinter.Button(self,font=('',14))
        submit_btn['text'] = '実行'
        submit_btn['command'] = self.copy_file
        # submit_btn['command'] = self.input_num
        submit_btn.pack()
        # メッセージ出力
        self.message = tkinter.Message(self,font=('',12))
        self.message['width'] = 200
        self.message.pack()

    def copy_file(self):
        try:
            # 置き換える文字列
            get_new_text = self.text_box.get('1.0', 'end -1c')
            new_texts = get_new_text.splitlines()
            # コピーするファイル数
            copy_file_number = len(new_texts)
            # コピー元ファイル情報取得
            dir_name = 'copy_file'
            files = os.listdir(dir_name)
            source_file = files[0]
            copy_source = os.path.join(dir_name, source_file)
            # ファイル名分割(メディア、連続番号、拡張子)
            _split = source_file.split('.')
            copy_file_name = _split[0]
            ext = _split[1]
            _name_split = copy_file_name.split('-', 1)
            media = _name_split[0]
            source_number = _name_split[1]
            # 連番順作成
            numberings = []
            rng = range(ord('a'), ord('z')+1)
            for i in rng:
                numberings.append(chr(i))
            for i in rng:
                for j in rng:
                    numberings.append(chr(i)+chr(j))
            # 指定の連番抽出
            start_index = numberings.index(source_number) + 1
            file_number = numberings[start_index]
            copy_numbers = numberings[start_index:start_index + copy_file_number]
            # ソースファイルを開いて置き換える文字列を取得
            replace_type = self.var_radio.get()
            with open(copy_source, encoding='utf-8') as f:
                html = f.read()
                if replace_type == 'A':
                    # リゲット文字列
                    word = re.search(r'https://webfree-info.com/register/(.+)/---AID---',html).group(1)
                elif replace_type == 'B':
                    # Lステップ文字列
                    word = re.search(r'https://liff.line.me/(.+)',html).group(0)
                    word = word.split('"')[0]
                # Lステップ新規作成時
                # word = re.search(r'###',html).group()
            # コピー
            for copy_number, new_text in zip(copy_numbers, new_texts):
                new_file = '{}-{}.{}'.format(media, copy_number, ext)
                create_file = shutil.copyfile(
                    copy_source, os.path.join(dir_name, new_file))
                # 　書き換えと保存
                replace = html.replace(word, new_text)
                with open(create_file, 'w', encoding='utf-8') as writer:
                    writer.write(replace)
            # ソースファイル削除
            # os.remove(copy_source)
            self.message['text'] = '成功しました'
        except:
            self.message['text'] = '失敗しました'




root = tkinter.Tk()
root.title('LPファイル複製')
root.geometry('800x600')
app = Application(root=root)
root.mainloop()
