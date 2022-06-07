print("\n\n\n")

projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
mediaPool = project.GetMediaPool()
rootFolder = mediaPool.GetRootFolder()
folders_dict = rootFolder.GetSubFolders()
folders = list(folders_dict.values())
print(folders, type(folders))

for folder in folders:
	print(folder.GetName())
	if folder.GetName() == "ToConvert":
		convert_folder = folder
		break

clips = convert_folder.GetClipList()

print([(int)(clip.GetName()[:-4]) for clip in clips])
sort_clips = sorted(clips, key=lambda clip:(int)(clip.GetName()[:-4])+7)

print(sort_clips)

names = [clip.GetName() for clip in sort_clips]
print(names)
fadeTool = bmd.readfile(comp.MapPath("Macros:/Right Fade.setting"))
print(fadeTool, type(fadeTool))
for i in range(1):
	toolName = f"Right Fade {i}"
	print(toolName)
 
	comp.Paste(fadeTool)
 	comp.DoAction("AddSetting", (filename: "Macros:/Right Fade.setting"))
	tool = comp.ActiveTool
	tool.Name = toolName
 	print(comp.ActiveTool.GetChildrenList(), comp.ActiveTool.GetChildrenList())
	for t in comp.ActiveTool.GetChildrenList():
		if t.Name[:5] == "Merge":
			t.Center = (0, 0)
 
print("end")