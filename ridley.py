import wx
import time
import wikipedia
import wolframalpha
import winspeech
import wolframalpha
from PIL import Image

from speech import speechutils
from utils.configreader import get_preferences, get_phrases

app_id = "RT2P2A-TKVHWP2EVY"
client = wolframalpha.Client(app_id)

hour = time.localtime().tm_hour
preferences = get_preferences()
title = preferences.get_user_title()  # mam? sir?
print_cmds = preferences.get_print_cmds_on_start()
i=1

if hour < 12:
    greeting = "Good morning {},".format(title)
else:
    greeting = "Good evening {},".format(title)

img = Image.open('greeting.jpg')
img.show()
winspeech.say(greeting + "My name is Ridley")
winspeech.say("Ask me anything!")


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
            pos=wx.DefaultPosition, size=wx.Size(450, 100),
            style=wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
             wx.CLOSE_BOX | wx.CLIP_CHILDREN,
            title="RIDLEY")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
        label="Hello I am Ridley, the Python Digital Assistant. How can I help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
         

        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def OnEnter(self, event):

        input = self.txt.GetValue()
        input = input.lower()
        winspeech.say(input)
        try:
        	res = client.query(input)
        	answer = next(res.results).text
        	print answer
                winspeech.say(answer)
                
       	except:
       		try:
				input = input.split(' ')
       				input = ' '.join(input[2:])
       				print wikipedia.summary(input)
       				qu = wikipedia.summary(input)
       				winspeech.say(qu)
       		except:
       			
       			print "Sorry, please try a different " 
       			winspeech.say("Try a different question")
       			
       			
			
       				

if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
