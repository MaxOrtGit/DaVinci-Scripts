function Main()
  print("\n\nstart")
  resolve = Resolve()
  projectManager = resolve:GetProjectManager()
  project = projectManager:GetCurrentProject()
  mediaPool = project:GetMediaPool()
  rootFolder = mediaPool:GetRootFolder()
  folders_dict = rootFolder:GetSubFolders()
  
  #dump(folders_dict)
  for i, folder in ipairs(folders_dict):
    #print(folder:GetName())
    if folder:GetName() == "ToConvert":
      convert_folder = folder
      break
    end
  end

  clips = convert_folder:GetClipList()
  array = {}
  for i, clip in ipairs(clips):
    array[i-1] = i
  end
  for i, clip in ipairs(clips):
    name = clip:GetName()
    snum = name:sub(1, -5)
    #print(i .. " " .. name .. " " .. snum)
    array[tonumber(snum)] = clip
  end

  table.remove(array, 1)
  for i, clip in ipairs(array):
    toolName = "Right Fade " .. i
    print(toolName)
    comp:Paste(bmd.readfile(comp:MapPath("Macros:/Fade.setting")))
    tool = comp.ActiveTool
    tool:SetAttrs({TOOLS_Name = toolName})
    for j,t in pairs(comp.ActiveTool:GetChildrenList()):
      print(t.Name)
      if string.sub(t.Name, 1, 5) == "Merge":
        t.Center = {0, 0.5}
      end
      if string.sub(t.Name, 1, 5) == "Image":
        #dump(t:GetAttrs("TOOLS_Clip_MediaID"))
        t:SetAttrs({TOOLS_Clip_MediaID = clip:GetMediaId()})
        #dump(t.MediaID:SetAttrs({INPS_ID = 0}))
        t.MediaID = clip:GetMediaId()
      end
      #print(i .. " " .. #array-1 .. " " .. tostring(i == (#array)) .. " ".. string.sub(t.Name, 1, 6))
      if i == (#array):
        print("first cond")
        if string.sub(t.Name, 1, 4) == "Fade":
          t.Center = {0.5, 0.5}
          t.Width = 1
        end
      end
    end
    wait(0.5)
  end
  print("end")
end

Main()