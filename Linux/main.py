import threading
import wx
from wx.lib import sized_controls
from subprocess import call

class CustomDialog(sized_controls.SizedDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)
        pane = self.GetContentsPane()
        self.SetSize((350, 140))

        msg = wx.StaticText(pane, -1, "Processing...Please wait...")
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        msg.SetFont(font)

class myThred(threading.Thread):

    command = ""
    action = ""
    key = ""
    inputFile = ""
    outputFile = ""
    def __init__(self, command, action, key, inputFile, outputFile):
        self.command = command
        self.action = action
        self.key = key
        self.inputFile = inputFile
        self.outputFile = outputFile
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        call([self.command, self.action, str(self.key), str(self.inputFile), str(self.outputFile)])
        print("####################### thread done #########################")

class windowClass(wx.Frame):

    dlg = ""
    def __init__(self, parent, title):
        super(windowClass, self).__init__(parent, title=title,size = (650,350), style = wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION)
        self.Center()
        self.Show()
        self.buildUi()

    def buildUi(self):
        panel = wx.Panel(self)

        #title
        titleText = wx.StaticText(panel, -1, "DES Encryption Tool", (170, 12))
        font = wx.Font(26, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        titleText.SetFont(font)

        #input File
        inputFileLabel = wx.StaticText(panel, -1, "Input File:", (33, 70))
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        inputFileLabel.SetFont(font)
        self.inputFileText = wx.TextCtrl(panel, size=(400, 40), pos=(150, 65))
        inputBrowseButton = wx.Button(panel, label="Browse", pos=(557, 67), size=(70, 35))
        self.Bind(wx.EVT_BUTTON, self.inputBrowseOnClick, inputBrowseButton)

        #Key File
        keyLabel = wx.StaticText(panel, -1, "Key:", (92, 120))
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        keyLabel.SetFont(font)
        self.keyText = wx.TextCtrl(panel, size=(400, 40), pos=(150, 115))
        keyBrowseButton = wx.Button(panel, label="Browse", pos=(557, 117), size=(70, 35))
        self.Bind(wx.EVT_BUTTON, self.keyBrowseOnClick, keyBrowseButton)

        #output File
        outputFileLabel = wx.StaticText(panel, -1, "Output File:", (15, 170))
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        outputFileLabel.SetFont(font)
        self.outPutFileText = wx.TextCtrl(panel, size=(400, 40), pos=(150, 165))
        keyBrowseButton = wx.Button(panel, label="Browse", pos=(557, 167), size=(70, 35))
        self.Bind(wx.EVT_BUTTON, self.outputBrowseOnClick, keyBrowseButton)

        #encrypt
        encryptButton = wx.Button(panel, label="Encrypt", pos=(150, 235), size=(80, 50))
        self.Bind(wx.EVT_BUTTON, self.encryptOnClick, encryptButton)

        #generate key
        generateKeyButton = wx.Button(panel, label="Generate Key", pos=(298, 235), size=(110, 50))
        self.Bind(wx.EVT_BUTTON, self.generateKeyOnClick, generateKeyButton)

        #decrypt
        decryptKeyButton = wx.Button(panel, label="Decrypt", pos=(470, 235), size=(80, 50))
        self.Bind(wx.EVT_BUTTON, self.decryptOnClick, decryptKeyButton)

    def inputBrowseOnClick(self, event):
        openFileDialog = wx.FileDialog(self, "Choose file", "", "", "", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_OK:
            self.inputFileText.SetValue(openFileDialog.GetPath())

        openFileDialog.Destroy()

    def keyBrowseOnClick(self, event):
        openFileDialog = wx.FileDialog(self, "Choose file", "", "", "", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_OK:
            self.keyText.SetValue(openFileDialog.GetPath())

        openFileDialog.Destroy()

    def outputBrowseOnClick(self, event):
        openFileDialog = wx.FileDialog(self, "Choose file", "", "", "", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if openFileDialog.ShowModal() == wx.ID_OK:
            self.outPutFileText.SetValue(openFileDialog.GetPath())

        openFileDialog.Destroy()

    def encryptOnClick(self, event):
        print("encryptOnClick")
        if self.checkFieldsAreFull():
            self.encryptDecrypt("-e")
        else:
            self.notFullMsg()


    def generateKeyOnClick(self, event):
        loc = ""
        flag = False
        openFileDialog = wx.FileDialog(self, "Where to save the key?", "", "", "", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if openFileDialog.ShowModal() == wx.ID_OK:
            loc = openFileDialog.GetPath()
            command = '../DES/key_gen '+loc
            call(['../DES/key_gen', str(loc)])
            print command
            flag = True

        openFileDialog.Destroy()

        if flag:
            dlg = wx.MessageDialog(self, "Operation completed", 'Operation completed', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def decryptOnClick(self, event):
        print("decryptOnClick")
        if self.checkFieldsAreFull():
            self.encryptDecrypt("-d")
        else:
            self.notFullMsg()

    def checkFieldsAreFull(self):
        if self.inputFileText.IsEmpty() or self.keyText.IsEmpty() or self.outPutFileText.IsEmpty():
            return False
        return True

    def notFullMsg(self):
        dlg = wx.MessageDialog(self, "Please fill all Fields", 'Error!', wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

    def operationDone(self):
        self.dlg.Destroy()
        dlg = wx.MessageDialog(self, "Operation completed", 'Operation completed', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def shellScript(self, command, action, key, inputFile, outputFile):
        call([command, str(action), str(key), str(inputFile), str(outputFile)])
        print("####################### thread done #########################")
        wx.CallAfter(self.operationDone)

    def encryptDecrypt(self, action):
        inputFile = self.inputFileText.GetValue()
        key = self.keyText.GetValue()
        outputFile = self.outPutFileText.GetValue()
        command = '../DES/des_action ' + action + ' ' + key  + ' ' + inputFile + ' ' + outputFile
        print command
        # t = myThred('../DES/des_action', action, key, inputFile, outputFile)
        t = threading.Thread(target=self.shellScript, args=("../DES/des_action", action, key, inputFile, outputFile))
        t.start()
        self.dlg = CustomDialog(self, title='Working')
        self.dlg.ShowModal()

        # call(['../DES/des_action', action, str(key), str(inputFile), str(outputFile)])

app = wx.App()
windowClass(None, title='DES Encryption Tool')

app.MainLoop()
