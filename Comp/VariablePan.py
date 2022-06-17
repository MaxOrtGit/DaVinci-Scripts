
from lib import poly
import time

#if __name__ == "__main__":
#  points = [[-1, -1], [-1, 1], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [-1,1], [1, 1], [1, -1]]
#  poly.change_points(comp, points)
#  print("done")

  
if __name__ == "__main__":
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
  clips.sort(key=lambda x: x.GetName().split("-")[0])
  
  c1 = clips[0]
  
  clips.pop(0)
  print([ar.GetName() for ar in clips])
  n, x, y, s = c1.GetName()[:-4].split("-")
  n, x, y, s = int(n), float(x), float(y), float(s)
  print(n, x, y, s)
  
  edge_polygon, back_polygon = poly.get_diff_points(x, y, s)
  otool = comp.ActiveTool
  
  poly.change_points(comp, edge_polygon)
  time.sleep(0.25)
  tool = comp.ActiveTool
  tool.SetAttrs({"TOOLS_Name": f"Edge Mask {n}"})
  tool.SoftEdge = 0.1
  tool.BorderWidth = 0.2
  tool.Invert = 1
  
  if back_polygon != []:
    poly.change_points(comp, back_polygon)
    time.sleep(0.25)
    tool = comp.ActiveTool
    tool.SetAttrs({"TOOLS_Name": f"Back Mask {n}"})
    time.sleep(0.25)
  comp.SetActiveTool(otool)
  
  for clip in clips:
    toolName = f"Image {n}"
      
    print(toolName)
    comp.Execute('comp:Paste(bmd.readfile(comp:MapPath("Macros:/Fade.setting")))')
    time.sleep(1.5)
    tool = comp.ActiveTool
    tool.SetAttrs({"TOOLS_Name": toolName})
    for j, t in comp.ActiveTool.GetChildrenList().items():
      #print(t.Name)
      if t.Name[:5] == "Merge":
        t.Center = [x, y]
        t.Size = s
          
      if t.Name[:5] == "Image":
        t.SetAttrs({"TOOLS_Clip_MediaID": clip.GetMediaId()})
        t.MediaID = clip.GetMediaId()
    print(n, len(clips), n != len(clips))
    if n != len(clips):
      n, x, y, s = clip.GetName()[:-4].split("-")
      n, x, y, s = int(n), float(x), float(y), float(s)
      
      otool = comp.ActiveTool
      edge_polygon, back_polygon = poly.get_diff_points(x, y, s)

      poly.change_points(comp, edge_polygon)
      time.sleep(0.25)
      tool = comp.ActiveTool
      tool.SetAttrs({"TOOLS_Name": f"Edge Mask {n}"})
      tool.SoftEdge = 0.1
      tool.BorderWidth = 0.2
      tool.Invert = 1
      
      if back_polygon != []:
        poly.change_points(comp, back_polygon)
        time.sleep(0.25)
        tool = comp.ActiveTool
        tool.SetAttrs({"TOOLS_Name": f"Back Mask {n}"})
        time.sleep(0.25)
      comp.SetActiveTool(otool)
    