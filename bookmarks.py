import idaapi

Bookview=idaapi.simplecustviewer_t() # Custom view declaration

def OnKeydown(vkey,shift,t=Bookview):
    if vkey==46: # If "Delete" button pressed
        d=t.GetLineNo() # Get bookmark id
        path=GetIdbPath()[:-4]+".txt" # Get path to bookmarks file
        with open(path,"r") as f: # Read file
            temp=""
            ch=0 # String number
            for line in f:
                if d!=ch: # If string number != bookmark id
                    temp+=line # Read string
                ch+=1
        with open(path,"w") as f: # Write to file
            f.write(temp)
        t.DelLine(d) # Delete line from custom view

def OnDblClick(shift,t=Bookview):
    d=t.GetCurrentLine() # Read string
    d=d.split(" ")[0][2:] # Get address from the bookmark
    d=int(d,16)
    Jump(d) # Jump to address

Bookview.OnKeydown=OnKeydown
Bookview.OnDblClick=OnDblClick

def createbook(t=Bookview):
    name="Name ("+str(hex(ScreenEA()))[:-1]+"):" # Create string "Name (address):"
    b=AskStr(GetFunctionName(ScreenEA()),name) # Ask for bookmark name
    b=str(hex(ScreenEA()))[:-1]+" ... "+b+" ... "+GetFunctionName(ScreenEA()) # Create string with Address, Bookmark name and Function name
    if b is not None:
        t.AddLine(b) # Add to custom view
        b+="\n"
        path=GetIdbPath()[:-4]+".txt" # Bookmarks file
        try: # Read file
            with open(path,"r") as f:
                st=f.read()
                st+=b
                b=st
        except Exception as e:
            print(e)
        with open(path,"w") as f: # Write
            f.write(b)

def showbookmark(t=Bookview):
    t.Create("Bookmarks") # Create custom view "Bookmarks"
    t.Show() # Show view on screen
    path=GetIdbPath()[:-4]+".txt"
    try: # Read file
        with open(path,"r") as f:
            st=f.readlines()
            for i in range(len(st)):
                t.AddLine(st[i])
    except Exception as e:
        print(e)

class myplugin_t(idaapi.plugin_t):
    SHOWKEYS="Ctrl-F6" # Keys to show custom view
    ADDKEYS="Alt+u" # Keys to add bookmark
    flags=0 # No flags
    comment="Bookmarks plugin" # Plugin's comment
    help=("Press "+ SHOWKEYS +" to show bookmarks view.\n\
    Press "+ ADDKEYS +" to add bookmark.\n\
    Press 'Delete' to delete bookmark.") # Help text
    wanted_name="IDA_Bookmarks" # Plugin's name
    wanted_hotkey=SHOWKEYS # Keys to run plugin
    

    def init(self):
        idaapi.msg("Bookmarks plugin initialized.\n")
        idaapi.CompileLine('static Bookm(){RunPythonStatement("createbook()");}') # Idc function to run createbook()
        AddHotkey(self.ADDKEYS, "Bookm") # Run idc function Bookm() on hotkeys
        return idaapi.PLUGIN_KEEP # Plugin is working until base is closed

    def run(self,arg):
        showbookmark() # Run showbookmark() on startup

    def term(self):
        idaapi.msg("Bookmarks plugin terminated.\n")

def PLUGIN_ENTRY():
    return myplugin_t()