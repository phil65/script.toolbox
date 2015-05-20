Dialog call examples:

- DialogSelect

<onclick>SetProperty(Dialog.1.Label,Test)</onclick>
<onclick>SetProperty(Dialog.1.BuiltIn,builtin1)</onclick>
<onclick>SetProperty(Dialog.2.Label,Test 2)</onclick>
<onclick>SetProperty(Dialog.2.BuiltIn,builtin2)</onclick>
<onclick>SetProperty(Dialog.3.Label,Test 3)</onclick>
<onclick>SetProperty(Dialog.3.BuiltIn,builtin3)</onclick>
<onclick>SetProperty(Dialog.4.Label,Test 4)</onclick>
<onclick>SetProperty(Dialog.4.BuiltIn,builtin4)</onclick>
<onclick>RunScript(script.extendedinfo,info=selectdialog,header=This is a custom dialog)</onclick>


- DialogYesNo

<onclick>RunScript(script.toolbox,info=yesnodialog,header=SOME_TEXT,text=SOME_TEXT,yesaction=builtin,noaction=builtin,yeslabel=SOME_TEXT,nolabel=SOME_TEXT)</onclick>


- DialogOK

<onclick>RunScript(script.toolbox,info=okdialog,header=SOME_TEXT,text=SOME_TEXT)</onclick>


- DialogTextViewer

<onclick>RunScript(script.toolbox,info=textviewer,header=SOME_TEXT,text=SOME_TEXT)</onclick>


- Notification with extended options

<onclick>RunScript(script.toolbox,info=notification,header=SOME_TEXT,text=SOME_TEXT,icon=PATH_TO_ICON,time=SECONDS TO DISPLAY,sound=TRUE/FALSE)</onclick>


Notes:
- use "|" to append several builtins
- escape stuff like '"$INFO[xxx]"'



other calls:

<onclick>RunScript(script.toolbox,info=exportskinsettings)</onclick>
<onclick>RunScript(script.toolbox,info=importskinsettings)</onclick>
<onclick>RunScript(script.toolbox,info=blur,id=PATH_TO_IMAGE)</onclick>
