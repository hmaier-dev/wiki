# Converting filetypes
If you want to convert a single ogg-file into mp3.
```bash
ffmpeg -i "file.ogg" "file.mp3"
```
If there are multiple files, instead of writing a script, you could use gnu/parallel to use all of your CPU cores.
```bash
parallel ffmpeg -i "{}" "{.}.mp3" ::: *.ogg
```


