
import time

#type 1 = right, 2 = left, 3 = up, 4 = down
def pan(type, resolve, comp):
  projectManager = resolve.GetProjectManager()
  project = projectManager.GetCurrentProject()
  mediaPool = project.GetMediaPool()
  rootFolder = mediaPool.GetRootFolder()
  folders_dict = rootFolder.GetSubFolders()
  
  print(folders_dict)
  for i, folder in folders_dict.items():
    #print(folder:GetName())
    if folder.GetName() == "ToConvert":
      convert_folder = folder
      break

  clips = convert_folder.GetClipList()
  clips.sort(key=lambda x: x.GetName()[0: -4])

  print(clips)
  clips.pop(0)
  print([ar.GetName() for ar in clips])
  i = 1
  for clip in clips:
    i += 1
    if type == 1:
      toolName = f"Right Fade {i}"
    elif type == 2:
      toolName = f"Left Fade {i}"
    elif type == 3:
      toolName = f"Up Fade {i}"
    elif type == 4:
      toolName = f"Down Fade {i}"
      
    print(toolName)
    comp.Execute('comp:Paste(bmd.readfile(comp:MapPath("Macros:/Fade.setting")))')
    time.sleep(0.25)
    tool = comp.ActiveTool
    tool.SetAttrs({"TOOLS_Name": toolName})
    for j, t in comp.ActiveTool.GetChildrenList().items():
      #print(t.Name)
      if t.Name[:5] == "Merge":
        if type == 1:
          t.Center = [0, 0.5]
        elif type == 2:
          t.Center = [1, 0.5]
        elif type == 3:
          t.Center = [0.5, 0]
        elif type == 4:
          t.Center = [0.5, 1]
          
      if t.Name[:5] == "Image":
        #dump(t:GetAttrs("TOOLS_Clip_MediaID"))
        t.SetAttrs({"TOOLS_Clip_MediaID": clip.GetMediaId()})
        #dump(t.MediaID:SetAttrs({INPS_ID = 0}))
        t.MediaID = clip.GetMediaId()
        
      print(t.Name, t.Name[:4] == "Fade", i, len(clips))
      if t.Name[:4] == "Fade":
        if (i == len(clips)+1):
          print("last")
          t.Center = [0.5, 0.5]
          t.Width = 1
          t.Height = 1
        else:
          if type == 1:
            t.Center = [0.25, 0.5]
            t.Width = 0.5
            t.Height = 1
          elif type == 2:
            t.Center = [0.75, 0.5]
            t.Width = 0.5
            t.Height = 1
          elif type == 3:
            t.Center = [0.5, 0.25]
            t.Width = 1
            t.Height = 0.5
          elif type == 4:
            t.Center = [0.5, 0.75]
            t.Width = 1
            t.Height = 0.5
    time.sleep(0.25)