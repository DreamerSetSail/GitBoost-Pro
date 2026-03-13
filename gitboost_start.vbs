Set objShell = CreateObject("WScript.Shell")
strPath = WScript.ScriptFullName
strFolder = Left(strPath, InStrRev(strPath, "\") - 1)

' Run GitBoost Pro in background mode (silent)
objShell.Run "python """ & strFolder & "\gitboost_pro_all_in_one.py"" --background", 0, False
